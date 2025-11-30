"""
Test Engine - MongoDB Implementation
R-PERF-01: Performance requirements (3 seconds per test case)
R-UX-01: Clear, non-technical error messages
R-ETH-01: Fairness enforcement
R-LOG-01: All test events logged
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Dict, Optional

from fastapi import HTTPException, status

from ..models.domain import CandidateResponse, DifficultyBand, QuestionMetadata, TestSession
from ..rules import format_user_error
from ..database import get_test_sessions_collection
from ..utils.trace_logger import log_event
from .item_bank import get_question, get_questions_for_track

BAND_SEQUENCE = [DifficultyBand.easy, DifficultyBand.medium, DifficultyBand.hard]


async def get_session(session_id: str) -> TestSession:
    """Get test session by ID"""
    collection = get_test_sessions_collection()
    doc = await collection.find_one({"sessionId": session_id})
    
    if not doc:
        # R-UX-01: Clear, non-technical error message
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=format_user_error("session not found")
        )
    
    doc.pop('_id', None)
    return TestSession(**doc)


def _time_remaining(session: TestSession) -> int:
    """Calculate remaining time for session"""
    expires = datetime.fromisoformat(session.expiresAt)
    remaining = int((expires - datetime.now(timezone.utc)).total_seconds())
    return max(0, remaining)


async def _select_question(session: TestSession) -> Optional[QuestionMetadata]:
    """
    Select next question based on adaptive algorithm
    R-ETH-01: Selection is based only on performance, not demographics
    """
    asked = set(session.questionIds)
    candidates = await get_questions_for_track(session.trackId, session.currentBand)
    candidates = [q for q in candidates if q.questionId not in asked]
    if candidates:
        return candidates[0]
    # fallback search other bands
    for band in BAND_SEQUENCE:
        alt = [q for q in await get_questions_for_track(session.trackId, band) if q.questionId not in asked]
        if alt:
            session.currentBand = band
            return alt[0]
    return None


async def next_question(session_id: str) -> Dict:
    """
    Get next question for a test session
    R-PERF-01: Fast question retrieval
    """
    session = await get_session(session_id)
    
    if session.status != "in_progress":
        # R-UX-01: Clear error message
        raise HTTPException(
            status_code=400,
            detail=format_user_error("session is not active", f"Status: {session.status}")
        )
    
    if _time_remaining(session) <= 0:
        # Update session status
        collection = get_test_sessions_collection()
        await collection.update_one(
            {"sessionId": session_id},
            {"$set": {"status": "expired"}}
        )
        # R-UX-01: Clear error message
        raise HTTPException(
            status_code=400,
            detail=format_user_error("session expired")
        )

    question: QuestionMetadata
    if session.currentQuestionId:
        question = await get_question(session.currentQuestionId)
        if not question:
            raise HTTPException(status_code=404, detail="Question not found")
    else:
        question = await _select_question(session)
        if not question:
            raise HTTPException(status_code=400, detail="No remaining questions; please submit test")
        
        # Update session with new question
        session.currentQuestionId = question.questionId
        if question.questionId not in session.questionIds:
            session.questionIds.append(question.questionId)
            
            collection = get_test_sessions_collection()
            await collection.update_one(
                {"sessionId": session_id},
                {"$set": {
                    "currentQuestionId": question.questionId,
                    "questionIds": session.questionIds
                }}
            )
            
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
    
    RT-02: Protection against infinite loops
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


async def submit_response(session_id: str, response: CandidateResponse) -> Dict:
    """
    Submit response and update adaptive difficulty
    R-LOG-01: Log all responses
    """
    session = await get_session(session_id)
    
    if session.currentQuestionId != response.questionId:
        raise HTTPException(status_code=400, detail="Question mismatch")

    session.responses.append(response)
    question = await get_question(response.questionId)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    correct = _evaluate_immediate(question, response)
    session.currentQuestionId = None

    session.currentBand = _next_band(session.currentBand, correct)
    
    # Update session in database
    collection = get_test_sessions_collection()
    await collection.update_one(
        {"sessionId": session_id},
        {"$set": {
            "responses": [r.model_dump() for r in session.responses],
            "currentQuestionId": None,
            "currentBand": session.currentBand.value
        }}
    )
    
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
    """Adaptive difficulty adjustment based on performance"""
    idx = BAND_SEQUENCE.index(current)
    if correct and idx < len(BAND_SEQUENCE) - 1:
        return BAND_SEQUENCE[idx + 1]
    if not correct and idx > 0:
        return BAND_SEQUENCE[idx - 1]
    return current
