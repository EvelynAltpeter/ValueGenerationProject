# VGP Technical Proficiency Platform

Demo implementation of the standardized adaptive technical assessment described in `VGP_Technical_Proficiency_Platform_Spec.md`.

This platform implements a **Blue Ocean** strategy, creating a standardized, cross-employer technical assessment system that allows candidates to "test once, apply everywhere" while enabling employers to filter and match applicants using verifiable proficiency scores.

## Architecture Overview
- **Backend:** FastAPI app (`backend/app`) exposing candidate, test, scoring, employer, and trace APIs. Uses in-memory storage plus JSON data files for the item bank and percentiles.
- **Frontend:** React + Vite single-page app (`frontend/`) with candidate and employer flows per R-UX-01.
- **Trace Logging:** All major actions stream to `logs/trace.jsonl` and `logs/prompt_trace.jsonl` (R-LOG-01).
- **Rules Compliance:** All system rules (R-PRIV-01, R-PERF-01, R-SCOR-01, R-UX-01, R-ETH-01, R-REP-01, R-LOG-01) are enforced throughout the system.

## Getting Started

### 1. Backend API
```bash
cd /Users/jetulven/Desktop/VGP
source .venv/bin/activate  # if not already active
uvicorn backend.app.main:app --reload --port 8000
```
Key endpoints:
- `POST /api/candidates` → register candidate
- `POST /api/candidates/{id}/tracks` → start test session
- `GET /api/tests/{sessionId}/next` → fetch adaptive question (timer included)
- `POST /api/tests/{sessionId}/responses` → record response with security metrics
- `POST /api/tests/{sessionId}/submit` → deterministic scoring + normalization
- `POST /api/employers` + `/jobs` + `/eligible` → configure filters and retrieve eligible candidates
- `GET /api/trace` → latest trace entries

### 2. Frontend App
```bash
cd /Users/jetulven/Desktop/VGP/frontend
npm install  # already run but safe to re-run
npm run dev -- --host 5173
```
Candidate instructions, timers, and submission states are visible. Employers can define thresholds and see transparent match explanations.

### 3. Testing
```bash
cd /Users/jetulven/Desktop/VGP
source .venv/bin/activate
pytest backend/tests
npm run build --prefix frontend
```

## Local URLs
- **Backend API + docs:** http://localhost:8000 (FastAPI docs at `/docs`)
- **Frontend SPA:** http://localhost:5173

## System Rules (Rule IDs)

All rules defined in the spec sheet are enforced:

- **R-PRIV-01:** All candidate data stored securely and never shared without explicit consent
- **R-PERF-01:** Code submissions evaluated within 3 seconds per test case
- **R-SCOR-01:** Standardized scoring algorithm (raw → scaled → percentile)
- **R-UX-01:** Clear, non-technical, actionable error messages
- **R-ETH-01:** Fairness ensured - tests cannot show different questions based on demographics
- **R-REP-01:** Every score report includes score, percentile, strengths, and weaknesses
- **R-LOG-01:** All test events logged for auditability

## Repository Structure
```
backend/
  app/
    api/            # FastAPI routers
    data/           # Item bank, adaptive metadata
    models/         # Pydantic schemas
    services/       # Candidate, test, scoring, employer logic
    utils/          # Trace logging, helpers
  tests/            # Pytest coverage
frontend/
  src/              # React candidate/employer flows
logs/
  trace.jsonl
  prompt_trace.jsonl
```

## Notes & Next Steps
- In-memory stores simplify the demo; swap `backend/app/state.py` with a persistence layer for production.
- Adaptive logic currently uses a 3-band heuristic; plug in IRT or ML models as data matures.
- Fairness analytics hooks can consume trace data plus stored subscores for subgroup analysis.
