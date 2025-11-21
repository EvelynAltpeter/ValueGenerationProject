from fastapi import APIRouter
from pydantic import BaseModel

from ..models.domain import JobRequirement
from ..services import candidate_service, employer_service
from ..utils.api import envelope

router = APIRouter(prefix="/api/employers", tags=["employers"])


class EmployerCreateRequest(BaseModel):
    name: str


@router.post("")
def create_employer(request: EmployerCreateRequest):
    employer = employer_service.create_employer(request.name)
    return envelope({"employerId": employer.id})


@router.post("/{employer_id}/jobs")
def upsert_job(employer_id: str, requirement: JobRequirement):
    job = employer_service.upsert_job(employer_id, requirement)
    return envelope({"jobId": job.jobId})


@router.get("/{employer_id}/jobs/{job_id}/eligible")
def eligible(employer_id: str, job_id: str):
    data = employer_service.eligible_candidates(employer_id, job_id)
    return envelope(data.model_dump())


@router.post("/{employer_id}/candidates/{candidate_id}/share")
def employer_share(employer_id: str, candidate_id: str):
    candidate_service.share_with_employer(candidate_id, employer_id)
    return envelope({"sharedWith": employer_id})
