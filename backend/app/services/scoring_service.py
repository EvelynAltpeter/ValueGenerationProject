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

    report = CandidateScoreReport(
        candidateId=session.candidateId,
        trackId=session.trackId,
        overallScore=overall,
        subscores=score_breakdown,
        percentile=percentile,
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
