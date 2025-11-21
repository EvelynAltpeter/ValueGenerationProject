# VGP Technical Proficiency Platform

Demo implementation of the standardized adaptive technical assessment described in `spec.md`.

## Architecture Overview
- **Backend:** FastAPI app (`backend/app`) exposing candidate, test, scoring, employer, and trace APIs. Uses in-memory storage plus JSON data files for the item bank and percentiles.
- **Frontend:** React + Vite single-page app (`frontend/`) with candidate and employer flows per R-UX-01/02.
- **Trace Logging:** All major actions stream to `logs/trace.jsonl` and `logs/prompt_trace.jsonl` (R-TRACE-01).

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
- Backend API + docs: http://localhost:8000 (FastAPI docs at `/docs`)
- Frontend SPA: http://localhost:5173

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
