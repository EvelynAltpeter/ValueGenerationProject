"""
Employer API Endpoints
R-PRIV-01: Privacy-compliant candidate access
R-LOG-01: All operations logged
"""

from fastapi import APIRouter
from pydantic import BaseModel

from ..models.domain import JobRequirement
from ..services import candidate_service, employer_service
from ..utils.api import envelope

router = APIRouter(prefix="/api/employers", tags=["employers"])


class EmployerCreateRequest(BaseModel):
    name: str


@router.post("")
async def create_employer(request: EmployerCreateRequest):
    """Create a new employer"""
    employer = await employer_service.create_employer(request.name)
    return envelope({"employerId": employer.id})


@router.post("/{employer_id}/jobs")
async def upsert_job(employer_id: str, requirement: JobRequirement):
    """Create or update a job requirement"""
    job = await employer_service.upsert_job(employer_id, requirement)
    return envelope({"jobId": job.jobId})


@router.get("/{employer_id}/jobs/{job_id}/eligible")
async def eligible(employer_id: str, job_id: str):
    """Get eligible candidates for a job (R-PRIV-01: only shared candidates)"""
    data = await employer_service.eligible_candidates(employer_id, job_id)
    return envelope(data.model_dump())


@router.post("/{employer_id}/candidates/{candidate_id}/share")
async def employer_share(employer_id: str, candidate_id: str):
    """Share candidate with employer (R-PRIV-01: explicit consent)"""
    await candidate_service.share_with_employer(candidate_id, employer_id)
    return envelope({"sharedWith": employer_id})
