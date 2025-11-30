"""
Candidate Service - MongoDB Implementation
R-PRIV-01: Secure candidate data storage
R-LOG-01: All operations logged
"""

from datetime import timedelta
from typing import List
from fastapi import HTTPException, status

from ..models.domain import Candidate, CandidateProfile, SkillTrack, TestSession
from ..database import get_candidates_collection, get_test_sessions_collection
from ..utils.ids import new_id
from ..utils.time import minutes_from_now_iso, utc_now_iso
from ..utils.trace_logger import log_event


TEST_DURATION_MINUTES = 30


async def create_candidate(profile: CandidateProfile) -> Candidate:
    """Create a new candidate (R-PRIV-01: secure storage)"""
    candidate_id = new_id("cand")
    candidate = Candidate(id=candidate_id, profile=profile)
    
    collection = get_candidates_collection()
    await collection.insert_one(candidate.model_dump())
    
    log_event("candidate.created", candidate_id, {"email": profile.email})
    return candidate


async def list_candidates() -> List[Candidate]:
    """List all candidates"""
    collection = get_candidates_collection()
    cursor = collection.find({})
    candidates = []
    async for doc in cursor:
        doc.pop('_id', None)  # Remove MongoDB internal ID
        candidates.append(Candidate(**doc))
    return candidates


async def get_candidate(candidate_id: str) -> Candidate:
    """Get candidate by ID (R-PRIV-01: access control)"""
    collection = get_candidates_collection()
    doc = await collection.find_one({"id": candidate_id})
    
    if not doc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Candidate not found")
    
    doc.pop('_id', None)
    return Candidate(**doc)


async def select_track(candidate_id: str, track: SkillTrack) -> TestSession:
    """
    Start a test session for a candidate
    R-LOG-01: Log session creation
    """
    candidate = await get_candidate(candidate_id)
    
    # Update selected tracks
    if track not in candidate.selectedTracks:
        candidate.selectedTracks.append(track)
        collection = get_candidates_collection()
        await collection.update_one(
            {"id": candidate_id},
            {"$set": {"selectedTracks": [t.value for t in candidate.selectedTracks]}}
        )
    
    # Create test session
    session_id = new_id("sess")
    session = TestSession(
        sessionId=session_id,
        candidateId=candidate_id,
        trackId=track,
        status="in_progress",
        startedAt=utc_now_iso(),
        expiresAt=minutes_from_now_iso(TEST_DURATION_MINUTES),
    )
    
    sessions_collection = get_test_sessions_collection()
    await sessions_collection.insert_one(session.model_dump())
    
    log_event(
        "session.created",
        candidate_id,
        {"sessionId": session_id, "trackId": track.value},
    )
    return session


async def share_with_employer(candidate_id: str, employer_id: str) -> Candidate:
    """
    Share candidate data with employer (R-PRIV-01: explicit consent)
    """
    candidate = await get_candidate(candidate_id)
    
    if employer_id not in candidate.sharedEmployers:
        candidate.sharedEmployers.append(employer_id)
        
        collection = get_candidates_collection()
        await collection.update_one(
            {"id": candidate_id},
            {"$addToSet": {"sharedEmployers": employer_id}}
        )
        
        log_event(
            "candidate.share",
            candidate_id,
            {"employerId": employer_id},
        )
    
    return candidate
