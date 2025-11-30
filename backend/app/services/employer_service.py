"""
Employer Service - MongoDB Implementation
R-PRIV-01: Privacy-compliant candidate filtering
R-LOG-01: All operations logged
"""

from typing import List
from fastapi import HTTPException, status

from ..models.domain import (
    Candidate, EligibleCandidate, EligibleCandidateList, 
    Employer, JobRequirement, RoleMatch, RoleMatchList, SkillTrack
)
from ..rules import check_privacy_consent
from ..database import get_employers_collection, get_jobs_collection, get_candidates_collection
from ..utils.ids import new_id
from ..utils.trace_logger import log_event
from .scoring_service import get_report


async def _ensure_employer(employer_id: str) -> Employer:
    """Get employer or raise 404"""
    collection = get_employers_collection()
    doc = await collection.find_one({"id": employer_id})
    if not doc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employer not found")
    doc.pop('_id', None)
    return Employer(**doc)


async def create_employer(name: str) -> Employer:
    """Create a new employer"""
    employer_id = new_id("emp")
    employer = Employer(id=employer_id, name=name)
    
    collection = get_employers_collection()
    await collection.insert_one(employer.model_dump())
    
    log_event("employer.created", employer_id, {"name": name})
    return employer


async def upsert_job(employer_id: str, requirement: JobRequirement) -> JobRequirement:
    """Create or update a job requirement"""
    employer = await _ensure_employer(employer_id)
    requirement.employerId = employer_id
    
    # Store job
    jobs_collection = get_jobs_collection()
    await jobs_collection.update_one(
        {"jobId": requirement.jobId},
        {"$set": requirement.model_dump()},
        upsert=True
    )
    
    # Update employer's jobs list
    employers_collection = get_employers_collection()
    await employers_collection.update_one(
        {"id": employer_id},
        {"$addToSet": {"jobs": requirement.model_dump()}}
    )
    
    log_event("job.upserted", employer_id, {"jobId": requirement.jobId})
    return requirement


async def eligible_candidates(employer_id: str, job_id: str) -> EligibleCandidateList:
    """
    Get eligible candidates for a job
    R-PRIV-01: Only returns candidates who have explicitly shared
    """
    employer = await _ensure_employer(employer_id)
    
    jobs_collection = get_jobs_collection()
    job_doc = await jobs_collection.find_one({"jobId": job_id})
    
    if not job_doc or job_doc.get("employerId") != employer_id:
        raise HTTPException(status_code=404, detail="Job not found")
    
    job_doc.pop('_id', None)
    job = JobRequirement(**job_doc)
    
    eligible: List[EligibleCandidate] = []
    
    # Get all candidates who have shared with this employer
    candidates_collection = get_candidates_collection()
    cursor = candidates_collection.find({"sharedEmployers": employer_id})
    
    async for doc in cursor:
        doc.pop('_id', None)
        candidate = Candidate(**doc)
        
        # R-PRIV-01: Double-check privacy consent
        if not check_privacy_consent(candidate.id, employer_id, candidate.sharedEmployers):
            continue
        
        if not await _meets_requirements(candidate, job):
            continue
        
        track_scores: dict[SkillTrack, int] = {}
        for track in job.requiredTracks:
            report = await get_report(candidate.id, track.value)
            if not report:
                break
            track_scores[track] = report.overallScore
        else:
            match_score, explanation = _match_score(job, track_scores)
            eligible.append(
                EligibleCandidate(
                    candidateId=candidate.id,
                    name=candidate.profile.name,
                    trackScores=track_scores,
                    matchScore=match_score,
                    matchExplanation=explanation,
                )
            )
    
    log_event("job.filter_run", employer_id, {"jobId": job_id, "resultCount": str(len(eligible))})
    return EligibleCandidateList(jobId=job_id, eligibleCandidates=eligible)


async def _meets_requirements(candidate: Candidate, job: JobRequirement) -> bool:
    """Check if candidate meets job requirements"""
    for track in job.requiredTracks:
        report = await get_report(candidate.id, track.value)
        if not report:
            return False
        threshold = job.minScores.get(track)
        if threshold is None or report.overallScore < threshold:
            return False
    return True


def _match_score(job: JobRequirement, track_scores: dict[SkillTrack, int]) -> tuple[int, str]:
    """Calculate match score and explanation"""
    scores = []
    components = []
    for track in job.requiredTracks:
        candidate_score = track_scores[track]
        threshold = job.minScores.get(track, 1)
        ratio = candidate_score / max(threshold, 1)
        score_component = min(int(ratio * 100), 120)
        scores.append(score_component)
        components.append(f"{track.value}: {candidate_score}/{threshold}")
    avg = int(sum(scores) / len(scores)) if scores else 0
    explanation = "; ".join(components)
    return min(avg, 100), explanation


async def candidate_matches(candidate_id: str) -> RoleMatchList:
    """Get recommended jobs for a candidate"""
    candidates_collection = get_candidates_collection()
    candidate_doc = await candidates_collection.find_one({"id": candidate_id})
    
    if not candidate_doc:
        raise HTTPException(status_code=404, detail="Candidate not found")
    
    candidate_doc.pop('_id', None)
    candidate = Candidate(**candidate_doc)
    
    matches: List[RoleMatch] = []
    
    # Get jobs from employers candidate has shared with
    jobs_collection = get_jobs_collection()
    cursor = jobs_collection.find({"employerId": {"$in": candidate.sharedEmployers}})
    
    async for job_doc in cursor:
        job_doc.pop('_id', None)
        job = JobRequirement(**job_doc)
        
        if not await _meets_requirements(candidate, job):
            continue
        
        track_scores: dict[SkillTrack, int] = {}
        for track in job.requiredTracks:
            report = await get_report(candidate.id, track.value)
            if not report:
                break
            track_scores[track] = report.overallScore
        else:
            match_score, _ = _match_score(job, track_scores)
            employer = await _ensure_employer(job.employerId)
            matches.append(
                RoleMatch(jobId=job.jobId, company=employer.name, matchScore=match_score)
            )
    
    return RoleMatchList(candidateId=candidate_id, recommendedJobs=matches)
