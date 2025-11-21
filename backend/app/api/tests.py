from fastapi import APIRouter

from ..models.domain import CandidateResponse
from ..services import scoring_service, test_engine
from ..utils.api import envelope

router = APIRouter(prefix="/api/tests", tags=["tests"])


@router.get("/{session_id}/next")
def next_question(session_id: str):
    data = test_engine.next_question(session_id)
    return envelope(data)


@router.post("/{session_id}/responses")
def record_response(session_id: str, response: CandidateResponse):
    result = test_engine.submit_response(session_id, response)
    return envelope(result)


@router.post("/{session_id}/submit")
def finalize(session_id: str):
    report = scoring_service.finalize_session(session_id)
    return envelope(report.model_dump())
