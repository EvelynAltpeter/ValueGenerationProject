# VGP Technical Proficiency Platform — Build Plan

## 1. Guiding Principles
- Follow `spec.md` as source of truth and enforce rules R-PRIV-01 through R-TRACE-01.
- Keep demo deterministic, transparent, and lightweight; mock complex services but preserve contracts.
- Log every major interaction to `logs/trace.jsonl`.

## 2. Tech Stack & Repo Layout
```
/Users/jetulven/Desktop/VGP
├── backend/            # FastAPI app
│   ├── app/
│   │   ├── main.py
│   │   ├── api/        # routers per module
│   │   ├── models/     # Pydantic schemas
│   │   ├── services/   # business logic modules
│   │   ├── data/       # mock item bank & adaptive metadata
│   │   └── utils/      # logging, security helpers
│   ├── tests/
│   └── requirements.txt
├── frontend/           # React Vite app
│   ├── src/
│   ├── public/
│   └── package.json
├── logs/
│   ├── trace.jsonl
│   └── prompt_trace.jsonl
├── docs/
│   ├── build_plan.md
│   └── api_contracts.md
├── scripts/
└── README.md
```

## 3. Module-by-Module Plan (Build Order)

### Module 1: Core Data Models & API Contracts
- Deliverables: `docs/api_contracts.md`, Pydantic models for Candidate, Employer, Track, Question, Submission, Score, JobRequirement, TraceEvent.
- Activities:
  - Define enums/constants (skill tracks, difficulty bands, security flags).
  - Publish REST contract covering registration, login (magic link stub), track selection, test session CRUD, submission, scoring, employer job config, filtering, report retrieval, trace fetch.
- Exit criteria: Contracts reviewed; `backend/app/models` scaffolding ready; tests covering schema validation.

### Module 2: Candidate Registration & Track Selection
- Deliverables: FastAPI router `api/candidates.py`, service `services/candidate_service.py`, in-memory store (later persisted to JSON/SQLite).
- Behavior:
  - POST `/candidates` create profile.
  - POST `/candidates/{id}/tracks` select track; schedule test session; log trace.
  - Include basic auth token stub + privacy safeguards.
- Exit criteria: Endpoints tested via pytest + HTTPX; trace events captured.

### Module 3: Test Delivery (Item Bank + Adaptive Flow)
- Deliverables: `services/test_engine.py`, router `api/tests.py`, mock item bank JSON, adaptive difficulty service using 3-band logic.
- Behavior:
  - GET `/tests/{sessionId}/next` returns next question with UI metadata (timer, instructions, band info).
  - POST `/tests/{sessionId}/responses` stores answer, updates difficulty, logs security metrics.
  - Enforce timers and simple security flags (copy/paste count placeholder).
- Exit criteria: Unit tests simulate correct/incorrect sequences; trace logs adaptation decisions.

### Module 4: Scoring Engine & Reports
- Deliverables: `services/scoring_service.py`, router `api/scoring.py`.
- Behavior:
  - Evaluate MCQ answers vs answer key.
  - Execute coding submissions via restricted Python runner (mocked) returning pass counts.
  - Compute subscores (algorithms/data structures/code quality) and overall; persist CandidateScoreReport; ensure R-SCORE-01 determinism.
  - Generate fairness-ready data structures (store anonymized demographics placeholders) for future analytics.
- Exit criteria: Automated tests verifying deterministic scores and JSON outputs; Candidate report endpoint available.

### Module 5: Employer Configuration & Filtering
- Deliverables: `api/employers.py`, `services/employer_service.py`.
- Behavior:
  - Employers create jobs with required tracks + thresholds.
  - GET `/employers/{id}/jobs/{jobId}/eligible` returns EligibleCandidateList with transparent match score formula.
  - Candidate-side `/candidates/{id}/matches` surfaces RoleMatchList.
- Exit criteria: Tests confirm filtering respects thresholds and privacy; trace entries recorded.

### Module 6: Trace Logging + Security/ Fairness Hooks
- Deliverables: `utils/trace_logger.py`, middleware logging prompts/responses; scheduled task stub computing fairness summaries stored in `AssessmentAnalytics` data structure.
- Behavior:
  - Provide helper to append to `logs/trace.jsonl` and `logs/prompt_trace.jsonl`.
  - Integrate hooks across modules; add CLI to read/pretty-print trace.
- Exit criteria: Manual test run shows trace lines for candidate registration, test steps, scoring, employer filtering.

### Module 7: Frontend (Vite + React)
- Candidate app pages:
  - `Landing`, `SignUp`, `TrackSelection`, `TestPlayer`, `ScoreReport`.
  - Implement instructions/timer UI, question navigation, submission handling.
- Employer app pages:
  - `EmployerDashboard`, `JobConfig`, `CandidateList` with filtering explanation.
- Shared: call backend via fetch, maintain state store (Zustand/Context).
- Exit criteria: Local `npm run dev` shows working flows hitting backend (mock data for now); instructions/timer visible.

### Module 8: Demo Data & Testing Harness
- Seed script populating sample candidates, tracks, employers, item bank.
- Add pytest suite covering API happy-path + red-team scenarios from Part C.
- Document manual test steps.

## 4. Risk & Assumption Log
- Simplified adaptive logic accepted for demo.
- Email token auth sufficient.
- Local JSON stores acceptable; can swap for DB later.
- Fairness metrics stub uses synthetic demographic buckets.

## 5. Success Criteria
- Backend + frontend run locally with `uvicorn` and `npm run dev`.
- Demo supports candidate completing Python track sample and employer filtering per TC-01 & TC-02.
- Trace logs capture full flow; README documents setup.
