from typing import List

from fastapi import HTTPException, status

from ..models.domain import Candidate, EligibleCandidate, EligibleCandidateList, Employer, JobRequirement, RoleMatch, RoleMatchList, SkillTrack
from ..state import db
from ..utils.ids import new_id
from ..utils.trace_logger import log_event
from .candidate_service import get_candidate
from .scoring_service import get_report


def _ensure_employer(employer_id: str) -> Employer:
    employer = db.employers.get(employer_id)
    if not employer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employer not found")
    return employer


def create_employer(name: str) -> Employer:
    employer_id = new_id("emp")
    employer = Employer(id=employer_id, name=name)
    db.employers[employer_id] = employer
    log_event("employer.created", employer_id, {"name": name})
    return employer


def upsert_job(employer_id: str, requirement: JobRequirement) -> JobRequirement:
    employer = _ensure_employer(employer_id)
    requirement.employerId = employer_id
    db.jobs[requirement.jobId] = requirement
    existing = [job for job in employer.jobs if job.jobId == requirement.jobId]
    if existing:
        employer.jobs = [job if job.jobId != requirement.jobId else requirement for job in employer.jobs]
    else:
        employer.jobs.append(requirement)
    log_event("job.upserted", employer_id, {"jobId": requirement.jobId})
    return requirement


def eligible_candidates(employer_id: str, job_id: str) -> EligibleCandidateList:
    employer = _ensure_employer(employer_id)
    job = db.jobs.get(job_id)
    if not job or job.employerId != employer_id:
        raise HTTPException(status_code=404, detail="Job not found")

    eligible: List[EligibleCandidate] = []
    for candidate in db.candidates.values():
        if employer_id not in candidate.sharedEmployers:
            continue
        if not _meets_requirements(candidate, job):
            continue
        track_scores: dict[SkillTrack, int] = {}
        for track in job.requiredTracks:
            report = get_report(candidate.id, track.value)
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
            continue
        # if loop breaks due to missing report, skip candidate
        continue

    log_event("job.filter_run", employer_id, {"jobId": job_id, "resultCount": str(len(eligible))})
    return EligibleCandidateList(jobId=job_id, eligibleCandidates=eligible)


def _meets_requirements(candidate: Candidate, job: JobRequirement) -> bool:
    for track in job.requiredTracks:
        report = get_report(candidate.id, track.value)
        if not report:
            return False
        threshold = job.minScores.get(track)
        if threshold is None or report.overallScore < threshold:
            return False
    return True


def _match_score(job: JobRequirement, track_scores: dict[SkillTrack, int]) -> tuple[int, str]:
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


def candidate_matches(candidate_id: str) -> RoleMatchList:
    candidate = get_candidate(candidate_id)
    matches: List[RoleMatch] = []
    for job in db.jobs.values():
        if job.employerId not in candidate.sharedEmployers:
            continue
        if not _meets_requirements(candidate, job):
            continue
        track_scores: dict[SkillTrack, int] = {}
        for track in job.requiredTracks:
            report = get_report(candidate.id, track.value)
            if not report:
                break
            track_scores[track] = report.overallScore
        else:
            match_score, _ = _match_score(job, track_scores)
            employer = _ensure_employer(job.employerId)
            matches.append(
                RoleMatch(jobId=job.jobId, company=employer.name, matchScore=match_score)
            )
    return RoleMatchList(candidateId=candidate_id, recommendedJobs=matches)
