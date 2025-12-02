# Demo Setup Guide

## Quick Setup for Demo

After starting the backend, the demo data is automatically loaded on startup. If you need to reload it manually:

### Option 1: Via API (Recommended)

```bash
# Load questions and demo candidates
curl -X POST http://localhost:8000/api/admin/load-questions
curl -X POST http://localhost:8000/api/admin/populate-demo-data
```

### Option 2: Via Scripts

```bash
cd backend
python scripts/load_questions.py
python scripts/populate_sample_candidates.py
```

## Demo Employer

**Employer ID**: `emp-demo-test`  
**Company Name**: Demo Company

This employer has access to **20 sample candidates** with scores.

### Using in Frontend

1. Go to `/employer` page
2. Click **"Use Demo Account"** button
3. You'll be logged in as "Demo Company"
4. Create a job requirement (e.g., Python Core, min score 70)
5. Click "View Candidates" to see all eligible candidates

## Sample Candidates

All 20 candidates have scores for Python, SQL, and JavaScript:

- **High Performers**: Alice (Python: 87), Bob (Python: 91), Olivia (Python: 90), Tina (Python: 92)
- **Mid Performers**: David (Python: 78), Frank (Python: 82), Maya (Python: 83)
- **Lower Performers**: Jack (Python: 65), Noah (Python: 68), Sam (Python: 71)

## Testing Different Scenarios

### Python Developer Role
- **Track**: Python Core
- **Min Score**: 70
- **Expected**: ~15 candidates

### SQL Specialist
- **Track**: SQL Core  
- **Min Score**: 80
- **Expected**: ~10 candidates

### Full Stack Developer
- **Tracks**: Python Core + JavaScript Core
- **Min Scores**: 75 each
- **Expected**: ~8 candidates

## Auto-Load on Startup

The backend automatically:
1. ✅ Loads questions from JSON files (if database is empty)
2. ✅ Creates demo employer (`emp-demo-test`)
3. ✅ Creates 20 sample candidates with scores

**Note**: Since we're using in-memory database, you need to restart the backend for auto-load to run again, or manually call the API endpoints.

