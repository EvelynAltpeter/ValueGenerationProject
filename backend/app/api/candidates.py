"""
Candidate API Endpoints
R-PRIV-01: Privacy-compliant data access
R-UX-01: Clear error messages
R-LOG-01: All operations logged
"""

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from ..models.domain import CandidateProfile, SkillTrack
from ..rules import format_user_error
from ..services import candidate_service, employer_service, scoring_service
from ..utils.api import envelope

router = APIRouter(prefix="/api/candidates", tags=["candidates"])


class TrackSelectionRequest(BaseModel):
    trackId: SkillTrack


class ShareRequest(BaseModel):
    employerId: str


@router.post("")
async def register_candidate(profile: CandidateProfile):
    """Register a new candidate"""
    candidate = await candidate_service.create_candidate(profile)
    return envelope({"candidateId": candidate.id})


@router.post("/{candidate_id}/tracks")
async def select_track(candidate_id: str, request: TrackSelectionRequest):
    """Start a test session for a skill track"""
    session = await candidate_service.select_track(candidate_id, request.trackId)
    return envelope({"sessionId": session.sessionId, "expiresAt": session.expiresAt})


@router.get("/{candidate_id}/scores/{track_id}")
async def get_score(candidate_id: str, track_id: SkillTrack):
    """Get score report for a candidate and track (R-REP-01: includes strengths/weaknesses)"""
    report = await scoring_service.get_report(candidate_id, track_id.value)
    if not report:
        # R-UX-01: Clear, non-technical error message
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=format_user_error("score not found", f"Track: {track_id.value}")
        )
    return envelope(report.model_dump())


@router.get("/{candidate_id}/matches")
async def matches(candidate_id: str):
    """Get recommended jobs for a candidate"""
    result = await employer_service.candidate_matches(candidate_id)
    return envelope(result.model_dump())


@router.post("/{candidate_id}/share")
async def share(candidate_id: str, request: ShareRequest):
    """Share candidate data with an employer (R-PRIV-01: explicit consent)"""
    candidate = await candidate_service.share_with_employer(candidate_id, request.employerId)
    return envelope({"sharedWith": candidate.sharedEmployers})
