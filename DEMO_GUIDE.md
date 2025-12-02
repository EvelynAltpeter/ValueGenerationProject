# Demo Guide - Testing the VGP Platform

## Quick Demo Setup

### Demo Employer ID (for testing candidate search)

**Employer ID**: `emp-demo-test`  
**Company Name**: Demo Company

This employer has access to all 20 sample candidates with scores.

### Using the Demo Employer

1. **Option 1: Use the demo employer directly**
   - Go to the Employer Dashboard
   - If you see an employer ID field, enter: `emp-demo-test`
   - Create a job requirement (e.g., Python Core, min score 70)
   - Click "View Candidates" to see all eligible candidates

2. **Option 2: Create your own employer**
   - Go to the Employer Auth page
   - Create a new employer account
   - Copy your Employer ID from the dashboard
   - The sample candidates are shared with all employers, so you'll see them too!

### Sample Candidates Available

All 20 candidates are shared with the demo employer and have scores for:
- **Python Core** (scores range from 65-92)
- **SQL Core** (scores range from 69-95)
- **JavaScript Core** (scores range from 68-92)

**Example candidates:**
- Alice Johnson - Python: 87, SQL: 92, JavaScript: 85
- Bob Smith - Python: 91, SQL: 88, JavaScript: 89
- Olivia Rodriguez - Python: 90, SQL: 84, JavaScript: 88
- Tina Zhang - Python: 92, SQL: 89, JavaScript: 90

### Quick Setup After Backend Restart

Since we're using an in-memory database, run this after each backend restart:

```bash
cd backend
./scripts/quick_setup.sh
```

Or manually:
```bash
cd backend
python scripts/load_questions.py
python scripts/populate_sample_candidates.py
```

### Testing the Flow

1. **Candidate Flow:**
   - Create a candidate profile
   - Take a test (Python, SQL, or JavaScript)
   - View your score report
   - Share with employer ID: `emp-demo-test`

2. **Employer Flow:**
   - Use employer ID: `emp-demo-test` (or create your own)
   - Create a job requirement (e.g., Python Core, min score 70)
   - View eligible candidates - you should see all candidates who meet the criteria
   - See match scores and explanations

### Sample Job Requirements for Testing

- **Python Developer**: Python Core, min score 70
  - Should show ~15 candidates

- **SQL Specialist**: SQL Core, min score 80
  - Should show ~10 candidates

- **Full Stack Developer**: Python Core + JavaScript Core, min scores 75 each
  - Should show ~8 candidates

### Troubleshooting

**No candidates showing?**
- Make sure you ran `populate_sample_candidates.py`
- Verify the employer ID is correct
- Check that job requirements match the candidates' scores

**Questions not loading?**
- Run `python scripts/load_questions.py`
- Or restart the backend (it auto-loads if database is empty)

