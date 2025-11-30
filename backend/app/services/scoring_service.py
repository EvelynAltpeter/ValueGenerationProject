import json
from pathlib import Path

from fastapi import HTTPException

from ..models.domain import CandidateScoreReport, ScoreBreakdown
from ..state import db
from ..utils.time import utc_now_iso
from ..utils.trace_logger import log_event
from .item_bank import get_question
from .test_engine import get_session

PERCENTILES_PATH = Path(__file__).resolve().parents[1] / "data" / "percentiles.json"
PERCENTILE_TABLE = json.loads(PERCENTILES_PATH.read_text(encoding="utf-8"))

SUBSKILLS = ["algorithms", "data_structures", "code_quality"]


def _coding_score(code: str | None) -> int:
    if not code:
        return 0
    score = 0
    lowered = code.lower()
    if "def" in lowered:
        score += 30
    if "return" in lowered:
        score += 30
    if "for" in lowered or "while" in lowered:
        score += 20
    if "dict" in lowered or "{" in lowered:
        score += 20
    return min(score, 100)


def _mcq_score(question, answer: str | None) -> int:
    if question.answerKey and answer:
        return 100 if answer.strip() == question.answerKey else 0
    return 0


def _percentile(score: int) -> int:
    sorted_scores = sorted(int(k) for k in PERCENTILE_TABLE.keys())
    percentile = 50
    for key in sorted_scores:
        if score >= key:
            percentile = PERCENTILE_TABLE[str(key)]
    return percentile


def _calculate_strengths_weaknesses(session, breakdown: dict) -> tuple[list[str], list[str]]:
    """R-REP-01: Calculate strengths and weaknesses from performance data."""
    strengths = []
    weaknesses = []
    
    # Analyze subskill performance
    threshold_high = 75
    threshold_low = 50
    
    if breakdown.get("algorithms", 0) >= threshold_high:
        strengths.append("algorithms")
    elif breakdown.get("algorithms", 0) < threshold_low:
        weaknesses.append("algorithms")
    
    if breakdown.get("data_structures", 0) >= threshold_high:
        strengths.append("data_structures")
    elif breakdown.get("data_structures", 0) < threshold_low:
        weaknesses.append("data_structures")
    
    if breakdown.get("code_quality", 0) >= threshold_high:
        strengths.append("code_quality")
    elif breakdown.get("code_quality", 0) < threshold_low:
        weaknesses.append("code_quality")
    
    # Analyze question tags for more specific strengths/weaknesses
    tag_performance: dict[str, list[int]] = {}
    for response in session.responses:
        question = get_question(response.questionId)
        if not question:
            continue
        score = _mcq_score(question, response.answer) if question.questionType == "mcq" else _coding_score(response.code)
        for tag in question.tags:
            tag_performance.setdefault(tag, []).append(score)
    
    for tag, scores in tag_performance.items():
        avg_score = sum(scores) / len(scores) if scores else 0
        if avg_score >= threshold_high and tag not in strengths:
            strengths.append(tag)
        elif avg_score < threshold_low and tag not in weaknesses:
            weaknesses.append(tag)
    
    # Ensure we have at least some strengths/weaknesses
    if not strengths and not weaknesses:
        if breakdown.get("algorithms", 0) > breakdown.get("data_structures", 0):
            strengths.append("algorithms")
            weaknesses.append("data_structures")
        else:
            strengths.append("data_structures")
            weaknesses.append("algorithms")
    
    return strengths, weaknesses


def finalize_session(session_id: str) -> CandidateScoreReport:
    session = get_session(session_id)
    if session.status not in {"in_progress", "responses_complete"}:
        raise HTTPException(status_code=400, detail="Session already finalized")
    session.status = "submitted"

    subskill_scores: dict[str, list[int]] = {k: [] for k in SUBSKILLS}

    for response in session.responses:
        question = get_question(response.questionId)
        if not question:
            continue
        if question.questionType == "mcq":
            score = _mcq_score(question, response.answer)
        else:
            score = _coding_score(response.code)
        subskill_scores.setdefault(question.subskill, []).append(score)

    breakdown = {}
    for sub in SUBSKILLS:
        scores = subskill_scores.get(sub, [])
        breakdown[sub] = int(sum(scores) / len(scores)) if scores else 0

    score_breakdown = ScoreBreakdown(**breakdown)
    overall = int(0.4 * score_breakdown.algorithms + 0.4 * score_breakdown.data_structures + 0.2 * score_breakdown.code_quality)
    percentile = _percentile(overall)

    # R-REP-01: Calculate strengths and weaknesses based on performance
    strengths, weaknesses = _calculate_strengths_weaknesses(session, breakdown)

    report = CandidateScoreReport(
        candidateId=session.candidateId,
        trackId=session.trackId,
        overallScore=overall,
        subscores=score_breakdown,
        percentile=percentile,
        strengths=strengths,
        weaknesses=weaknesses,
        completedAt=utc_now_iso(),
    )
    db.score_reports[f"{session.candidateId}:{session.trackId.value}"] = report
    log_event(
        "session.scored",
        session.candidateId,
        {
            "sessionId": session.sessionId,
            "overall": str(overall),
            "percentile": str(percentile),
        },
    )
    return report


def get_report(candidate_id: str, track_id: str) -> CandidateScoreReport | None:
    return db.score_reports.get(f"{candidate_id}:{track_id}")
