# API Contracts — VGP Technical Proficiency Platform

All responses wrap `{ "data": ..., "traceId": "..." }` unless noted. Authentication uses demo headers:
- `x-user-type`: `candidate` | `employer`
- `x-user-id`: ID string returned at registration.

## Candidate-Facing Endpoints

### POST /api/candidates
Create candidate profile.
Request Body: `CandidateProfile`
Response: `{ "candidateId": "cand-123", "magicToken": "..." }`

### POST /api/candidates/{candidateId}/tracks
Select skill track + open session.
Body: `{ "trackId": "python_core_v1" }
Response: `{ "sessionId": "sess-123", "expiresAt": ISO8601 }`

### GET /api/tests/{sessionId}/next
Fetch next question metadata including timer.
Response: `{ "question": QuestionMetadata, "timeRemaining": 900, "band": "medium" }`

### POST /api/tests/{sessionId}/responses
Submit response for current question.
Body: `CandidateResponse`
Response: `{ "status": "recorded", "nextBand": "hard" }`

### POST /api/tests/{sessionId}/submit
Finalize session; triggers scoring.
Response: `CandidateScoreReport`

### GET /api/candidates/{candidateId}/scores/{trackId}
Retrieve score report.
Response: `CandidateScoreReport`

### GET /api/candidates/{candidateId}/matches
Return `RoleMatchList` using shared employers + thresholds.

## Employer-Facing Endpoints

### POST /api/employers
Create employer account.
Body: `{ "name": "TechNova" }`
Response: `{ "employerId": "emp-456" }`

### POST /api/employers/{employerId}/jobs
Create/update job proficiency requirements.
Body: `JobRequirement`
Response: `{ "jobId": "backend-dev-123" }`

### GET /api/employers/{employerId}/jobs/{jobId}/eligible
Return `EligibleCandidateList` with match scores + threshold explanation.

### POST /api/employers/{employerId}/candidates/{candidateId}/share
Record candidate-sharing consent (R-PRIV-01).

## Admin / Shared

### GET /api/trace
Paginated list of trace events (admin only).
Query: `limit`, `eventType`.
Response: `[TraceEvent]`

### GET /health
Returns `{ "status": "ok" }`.

## Error Model
```
{
  "error": {
    "code": "not_authorized",
    "message": "Candidate has not shared scores with employer."
  },
  "traceId": "..."
}
```

## Deterministic Scoring Rules
- MCQ correct = 1 point, incorrect = 0; convert to 0-100 by `(correct/total)*100`.
- Coding tasks return `% test cases passed`; convert to subscore buckets: algorithms (40%), data_structures (40%), code_quality (20% static rubric placeholder).
- Overall score = weighted average of subscores; percentile derived from static lookup table in `backend/app/data/percentiles.json`.
