from __future__ import annotations

from datetime import datetime, timezone
from typing import Dict, Optional

from fastapi import HTTPException, status

from ..models.domain import CandidateResponse, DifficultyBand, QuestionMetadata, TestSession
from ..rules import RULE_PERFORMANCE, RULE_UX, PERFORMANCE_TIMEOUT_SECONDS, format_user_error
from ..state import db
from ..utils.trace_logger import log_event
from .item_bank import get_question, get_questions_for_track

BAND_SEQUENCE = [DifficultyBand.easy, DifficultyBand.medium, DifficultyBand.hard]


def get_session(session_id: str) -> TestSession:
    session = db.test_sessions.get(session_id)
    if not session:
        # R-UX-01: Clear, non-technical error message
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=format_user_error("session not found")
        )
    return session


def _time_remaining(session: TestSession) -> int:
    expires = datetime.fromisoformat(session.expiresAt)
    remaining = int((expires - datetime.now(timezone.utc)).total_seconds())
    return max(0, remaining)


def _select_question(session: TestSession) -> Optional[QuestionMetadata]:
    asked = set(session.questionIds)
    candidates = get_questions_for_track(session.trackId, session.currentBand)
    candidates = [q for q in candidates if q.questionId not in asked]
    if candidates:
        return candidates[0]
    # fallback search other bands
    for band in BAND_SEQUENCE:
        alt = [q for q in get_questions_for_track(session.trackId, band) if q.questionId not in asked]
        if alt:
            session.currentBand = band
            return alt[0]
    return None


def next_question(session_id: str) -> Dict:
    session = get_session(session_id)
    if session.status != "in_progress":
        # R-UX-01: Clear error message
        raise HTTPException(
            status_code=400,
            detail=format_user_error("session is not active", f"Status: {session.status}")
        )
    if _time_remaining(session) <= 0:
        session.status = "expired"
        # R-UX-01: Clear error message
        raise HTTPException(
            status_code=400,
            detail=format_user_error("session expired")
        )

    question: QuestionMetadata
    if session.currentQuestionId:
        question = get_question(session.currentQuestionId)
        if not question:
            raise HTTPException(status_code=404, detail="Question not found")
    else:
        question = _select_question(session)
        if not question:
            raise HTTPException(status_code=400, detail="No remaining questions; please submit test")
        session.currentQuestionId = question.questionId
        if question.questionId not in session.questionIds:
            session.questionIds.append(question.questionId)
            log_event(
                "session.question_assigned",
                session.candidateId,
                {"sessionId": session.sessionId, "questionId": question.questionId, "band": session.currentBand.value},
            )

    question_payload = question.model_dump()
    question_payload.pop("answerKey", None)
    question_payload.pop("referenceSolution", None)

    return {
        "question": question_payload,
        "timeRemaining": _time_remaining(session),
        "band": session.currentBand.value,
    }


def _evaluate_immediate(question: QuestionMetadata, response: CandidateResponse) -> bool:
    """
    R-PERF-01: Code evaluation should complete within 3 seconds per test case.
    For demo purposes, we use simple pattern matching. In production, this would
    run in a sandboxed container with timeout enforcement.
    """
    if question.questionType == "mcq" and question.answerKey:
        return (response.answer or "").strip() == question.answerKey
    if question.questionType == "coding" and response.code:
        # R-PERF-01: In production, this would execute in a sandbox with timeout
        # For now, use pattern matching as a proxy
        code = response.code.lower()
        # Check for infinite loops (RT-02 protection)
        if "while(true)" in code or "while(1)" in code or "for(;;)" in code:
            # Would timeout in real execution
            return False
        return "return" in code and ("for" in code or "while" in code)
    return False


def submit_response(session_id: str, response: CandidateResponse) -> Dict:
    session = get_session(session_id)
    if session.currentQuestionId != response.questionId:
        raise HTTPException(status_code=400, detail="Question mismatch")

    session.responses.append(response)
    question = get_question(response.questionId)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    correct = _evaluate_immediate(question, response)
    session.currentQuestionId = None

    session.currentBand = _next_band(session.currentBand, correct)
    log_event(
        "session.response_recorded",
        session.candidateId,
        {
            "sessionId": session.sessionId,
            "questionId": response.questionId,
            "correct": str(correct),
            "nextBand": session.currentBand.value,
        },
    )

    return {"status": "recorded", "nextBand": session.currentBand.value}


def _next_band(current: DifficultyBand, correct: bool) -> DifficultyBand:
    idx = BAND_SEQUENCE.index(current)
    if correct and idx < len(BAND_SEQUENCE) - 1:
        return BAND_SEQUENCE[idx + 1]
    if not correct and idx > 0:
        return BAND_SEQUENCE[idx - 1]
    return current
