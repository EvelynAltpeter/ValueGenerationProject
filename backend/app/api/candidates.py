from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from ..models.domain import CandidateProfile, SkillTrack
from ..services import candidate_service, employer_service, scoring_service
from ..utils.api import envelope

router = APIRouter(prefix="/api/candidates", tags=["candidates"])


class TrackSelectionRequest(BaseModel):
    trackId: SkillTrack


class ShareRequest(BaseModel):
    employerId: str


@router.post("")
def register_candidate(profile: CandidateProfile):
    candidate = candidate_service.create_candidate(profile)
    return envelope({"candidateId": candidate.id})


@router.post("/{candidate_id}/tracks")
def select_track(candidate_id: str, request: TrackSelectionRequest):
    session = candidate_service.select_track(candidate_id, request.trackId)
    return envelope({"sessionId": session.sessionId, "expiresAt": session.expiresAt})


@router.get("/{candidate_id}/scores/{track_id}")
def get_score(candidate_id: str, track_id: SkillTrack):
    report = scoring_service.get_report(candidate_id, track_id.value)
    if not report:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Score not found")
    return envelope(report.model_dump())


@router.get("/{candidate_id}/matches")
def matches(candidate_id: str):
    result = employer_service.candidate_matches(candidate_id)
    return envelope(result.model_dump())


@router.post("/{candidate_id}/share")
def share(candidate_id: str, request: ShareRequest):
    candidate = candidate_service.share_with_employer(candidate_id, request.employerId)
    return envelope({"sharedWith": candidate.sharedEmployers})
