"""
Test API Endpoints
R-PERF-01: Fast question retrieval and response processing
R-UX-01: Clear error messages
R-LOG-01: All test events logged
"""

from fastapi import APIRouter

from ..models.domain import CandidateResponse
from ..services import scoring_service, test_engine
from ..utils.api import envelope

router = APIRouter(prefix="/api/tests", tags=["tests"])


@router.get("/{session_id}/next")
async def next_question(session_id: str):
    """Get next question for test session (R-PERF-01: fast retrieval)"""
    data = await test_engine.next_question(session_id)
    return envelope(data)


@router.post("/{session_id}/responses")
async def record_response(session_id: str, response: CandidateResponse):
    """Record candidate response and adjust difficulty adaptively"""
    result = await test_engine.submit_response(session_id, response)
    return envelope(result)


@router.post("/{session_id}/submit")
async def finalize(session_id: str):
    """Finalize test and generate score report (R-SCOR-01, R-REP-01)"""
    report = await scoring_service.finalize_session(session_id)
    return envelope(report.model_dump())
