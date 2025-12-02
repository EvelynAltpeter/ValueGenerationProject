from enum import Enum
from typing import Dict, List, Optional
from pydantic import BaseModel, EmailStr, Field


class SkillTrack(str, Enum):
    python_core_v1 = "python_core_v1"
    sql_core_v1 = "sql_core_v1"
    javascript_core_v1 = "javascript_core_v1"


class DifficultyBand(str, Enum):
    easy = "easy"
    medium = "medium"
    hard = "hard"


class CandidateProfile(BaseModel):
    name: str
    email: EmailStr
    github: Optional[str] = None
    educationLevel: Optional[str] = None
    graduationYear: Optional[int] = None


class Candidate(BaseModel):
    id: str
    profile: CandidateProfile
    selectedTracks: List[SkillTrack] = Field(default_factory=list)
    sharedEmployers: List[str] = Field(default_factory=list)


class TrackSelection(BaseModel):
    trackId: SkillTrack
    level: Optional[str] = "core"


class QuestionMetadata(BaseModel):
    questionId: str
    trackId: SkillTrack
    prompt: str
    questionType: str  # mcq | coding
    difficulty: DifficultyBand
    tags: List[str]
    subskill: str
    options: Optional[List[str]] = None
    referenceSolution: Optional[str] = None
    answerKey: Optional[str] = None
    timeLimitSeconds: int = 300


class AdaptiveStats(BaseModel):
    averageScore: float
    discrimination: float
    difficultyEstimate: float
    attempts: int


class CandidateResponse(BaseModel):
    questionId: str
    responseType: str
    answer: Optional[str]
    code: Optional[str]
    timeTakenSeconds: int
    copiedCharacters: int = 0


class TestSession(BaseModel):
    sessionId: str
    candidateId: str
    trackId: SkillTrack
    status: str
    currentBand: DifficultyBand = DifficultyBand.medium
    currentQuestionId: Optional[str] = None
    questionIds: List[str] = Field(default_factory=list)
    responses: List[CandidateResponse] = Field(default_factory=list)
    startedAt: str
    expiresAt: str


class ScoreBreakdown(BaseModel):
    algorithms: int
    data_structures: int
    code_quality: int


class CandidateScoreReport(BaseModel):
    candidateId: str
    trackId: SkillTrack
    overallScore: int
    subscores: ScoreBreakdown
    percentile: int
    strengths: List[str] = Field(default_factory=list)  # R-REP-01: Required in all reports
    weaknesses: List[str] = Field(default_factory=list)  # R-REP-01: Required in all reports
    completedAt: str


class JobRequirement(BaseModel):
    jobId: str
    employerId: str
    requiredTracks: List[SkillTrack]
    minScores: Dict[SkillTrack, int]
    preferredExperienceYears: Optional[int]


class Employer(BaseModel):
    id: str
    name: str
    jobs: List[JobRequirement] = Field(default_factory=list)


class EligibleCandidate(BaseModel):
    candidateId: str
    name: str
    trackScores: Dict[SkillTrack, int]
    matchScore: int
    matchExplanation: Optional[str] = None


class EligibleCandidateList(BaseModel):
    jobId: str
    eligibleCandidates: List[EligibleCandidate]


class RoleMatch(BaseModel):
    jobId: str
    company: str
    matchScore: int


class RoleMatchList(BaseModel):
    candidateId: str
    recommendedJobs: List[RoleMatch]


class TraceEvent(BaseModel):
    eventType: str
    actorId: Optional[str]
    payload: Dict[str, str]
    timestamp: str
