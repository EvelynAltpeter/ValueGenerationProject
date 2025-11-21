from __future__ import annotations

from typing import Dict

from .models.domain import Candidate, CandidateScoreReport, Employer, JobRequirement, TestSession


class InMemoryDB:
    def __init__(self) -> None:
        self.candidates: Dict[str, Candidate] = {}
        self.test_sessions: Dict[str, TestSession] = {}
        self.score_reports: Dict[str, CandidateScoreReport] = {}
        self.employers: Dict[str, Employer] = {}
        self.jobs: Dict[str, JobRequirement] = {}


db = InMemoryDB()
