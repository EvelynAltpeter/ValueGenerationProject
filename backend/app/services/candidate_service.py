from datetime import timedelta
from typing import List

from fastapi import HTTPException, status

from ..models.domain import Candidate, CandidateProfile, SkillTrack, TestSession
from ..state import db
from ..utils.ids import new_id
from ..utils.time import minutes_from_now_iso, utc_now_iso
from ..utils.trace_logger import log_event


TEST_DURATION_MINUTES = 30


def create_candidate(profile: CandidateProfile) -> Candidate:
    candidate_id = new_id("cand")
    candidate = Candidate(id=candidate_id, profile=profile)
    db.candidates[candidate_id] = candidate
    log_event("candidate.created", candidate_id, {"email": profile.email})
    return candidate


def list_candidates() -> List[Candidate]:
    return list(db.candidates.values())


def get_candidate(candidate_id: str) -> Candidate:
    candidate = db.candidates.get(candidate_id)
    if not candidate:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Candidate not found")
    return candidate


def select_track(candidate_id: str, track: SkillTrack) -> TestSession:
    candidate = get_candidate(candidate_id)
    if track not in candidate.selectedTracks:
        candidate.selectedTracks.append(track)
    session_id = new_id("sess")
    session = TestSession(
        sessionId=session_id,
        candidateId=candidate_id,
        trackId=track,
        status="in_progress",
        startedAt=utc_now_iso(),
        expiresAt=minutes_from_now_iso(TEST_DURATION_MINUTES),
    )
    db.test_sessions[session_id] = session
    log_event(
        "session.created",
        candidate_id,
        {"sessionId": session_id, "trackId": track.value},
    )
    return session


def share_with_employer(candidate_id: str, employer_id: str) -> Candidate:
    candidate = get_candidate(candidate_id)
    if employer_id not in candidate.sharedEmployers:
        candidate.sharedEmployers.append(employer_id)
        log_event(
            "candidate.share",
            candidate_id,
            {"employerId": employer_id},
        )
    return candidate
