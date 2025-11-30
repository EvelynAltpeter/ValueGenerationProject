# VGP Technical Proficiency Platform

**Version 2.0** - Rebuilt with MongoDB and Apple-style UI

A standardized adaptive technical assessment platform that allows candidates to "test once, apply everywhere" while enabling employers to filter and match applicants using verifiable proficiency scores.

## 🎯 Project Overview

### Business Model (Blue Ocean Strategy)
- **For Candidates**: Take one standardized test per skill track, share verified scores with multiple employers
- **For Employers**: Access pre-screened candidates with standardized proficiency scores
- **For Universities**: Provide job-ready certification to graduates

### Key Features
- ✅ Adaptive testing engine that adjusts difficulty based on performance
- ✅ Standardized scoring with percentile rankings (R-SCOR-01)
- ✅ Privacy-compliant candidate sharing (R-PRIV-01)
- ✅ Separate landing pages and dashboards for candidates vs employers
- ✅ Apple-style minimalist UI design
- ✅ MongoDB persistent storage
- ✅ LeetCode problem scraper integration

## 🏗️ Architecture

```
Input → Adaptive Test Engine → Scoring Engine → Score Report → Employer Matching → Logs
```

### Tech Stack
- **Backend**: FastAPI (Python), MongoDB (Motor/PyMongo)
- **Frontend**: React 19, React Router, Vite
- **Design**: Apple-inspired minimalist UI
- **Data**: LeetCode scraper for item bank population

## 📋 System Rules (Compliance)

| Rule ID | Description | Status |
|---------|-------------|--------|
| R-PRIV-01 | All candidate data stored securely, never shared without explicit consent | ✅ |
| R-PERF-01 | Code submissions evaluated within 3 seconds per test case | ✅ |
| R-SCOR-01 | Standardized scoring algorithm (raw → scaled → percentile) | ✅ |
| R-UX-01 | Clear, non-technical, actionable error messages | ✅ |
| R-ETH-01 | Fairness ensured - no demographic-based question differences | ✅ |
| R-REP-01 | Every score report includes score, percentile, strengths, weaknesses | ✅ |
| R-LOG-01 | All test events logged for auditability | ✅ |

## 🚀 Getting Started

### Prerequisites
- Python 3.11+
- Node.js 18+
- MongoDB (local or cloud)

### 1. Install MongoDB

**macOS (using Homebrew):**
```bash
brew tap mongodb/brew
brew install mongodb-community
brew services start mongodb-community
```

**Linux/Ubuntu:**
```bash
sudo apt-get install -y mongodb
sudo systemctl start mongodb
sudo systemctl enable mongodb
```

**Windows/Cloud Option:**
Use MongoDB Atlas (cloud): https://www.mongodb.com/cloud/atlas

### 2. Backend Setup

```bash
cd /Users/evelynaltpeter/Desktop/ValueGenerationProject/backend

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start the API server
uvicorn app.main:app --reload --port 8000
```

**Backend runs at:** http://localhost:8000
**API docs:** http://localhost:8000/docs

### 3. Populate Sample Data

```bash
# In a new terminal, with venv activated
cd /Users/evelynaltpeter/Desktop/ValueGenerationProject/backend
python scripts/populate_sample_data.py
```

This creates:
- 3 sample employers
- 3 sample jobs with requirements
- 5 sample candidates with completed scores

### 4. Frontend Setup

```bash
cd /Users/evelynaltpeter/Desktop/ValueGenerationProject/frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

**Frontend runs at:** http://localhost:5173

## 🎨 UI/UX Design

### Apple-Style Minimalism
- High whitespace and breathing room
- Subtle depth with shadows
- Thin dividers and clean borders
- SF Pro font family (system fonts)
- Calm, precise visual hierarchy
- Clear call-to-action buttons

### Separate User Flows
1. **Landing Page** (`/`) - Role selection: Candidate or Employer
2. **Candidate Flow** (`/candidate`) - Auth → Dashboard → Test → Score Report
3. **Employer Flow** (`/employer`) - Auth → Dashboard → Job Management → Candidate Filtering

## 📖 Usage Guide

### For Candidates

1. **Navigate to:** http://localhost:5173
2. **Click:** "I'm a Candidate"
3. **Create Profile:** Enter name, email, GitHub, education details
4. **Select Track:** Choose Python, SQL, or JavaScript
5. **Take Test:** Answer adaptive questions (30-minute session)
6. **View Score:** See overall score, percentile, strengths/weaknesses
7. **Share:** Enter employer ID to grant access to your scores

### For Employers

1. **Navigate to:** http://localhost:5173
2. **Click:** "I'm an Employer"
3. **Create Account:** Enter company name
4. **Note Your ID:** Copy your Employer ID (needed for candidate sharing)
5. **Create Job:** Define job ID, skill track, minimum score threshold
6. **Share ID:** Give Employer ID to candidates so they can share scores
7. **View Candidates:** Click "View Candidates" to see eligible matches

### Employer IDs from Sample Data
After running the population script, check the console output for employer IDs, or create your own through the UI.

## 🔧 Admin Features

### LeetCode Scraper
Populate the item bank with real LeetCode problems:

```bash
# Using curl
curl -X POST "http://localhost:8000/api/admin/scrape-leetcode" \
  -H "Content-Type: application/json" \
  -d '{"limit": 50}'

# Or use the API docs at /docs
```

### Item Bank Statistics
```bash
curl "http://localhost:8000/api/admin/item-bank-stats"
```

## 🧪 Testing

### Backend Tests
```bash
cd backend
source venv/bin/activate
pytest tests/
```

### Manual Testing Flow

**Test Candidate Flow:**
1. Register as candidate
2. Start Python Core test
3. Answer 3-5 questions
4. Submit test
5. Verify score report shows:
   - Overall score
   - Percentile
   - Strengths
   - Weaknesses
6. Share with employer ID: `emp_xxx` (from sample data)

**Test Employer Flow:**
1. Register as employer
2. Create job requirement (Python, min score 70)
3. Copy employer ID
4. Have candidate share scores with your ID
5. View eligible candidates
6. Verify match scores and explanations display

## 📂 Project Structure

```
├── backend/
│   ├── app/
│   │   ├── api/              # API routers (candidates, employers, tests, admin)
│   │   ├── models/           # Pydantic domain models
│   │   ├── services/         # Business logic (scoring, test engine, scraper)
│   │   ├── utils/            # Helpers (IDs, time, logging)
│   │   ├── data/             # Static data (percentiles, etc.)
│   │   ├── database.py       # MongoDB connection
│   │   ├── rules.py          # System rule enforcement
│   │   └── main.py           # FastAPI app
│   ├── scripts/              # Data population scripts
│   └── tests/                # Unit tests
├── frontend/
│   └── src/
│       ├── pages/            # React pages (Landing, Auth, Dashboards)
│       ├── App.jsx           # Router configuration
│       ├── App.css           # Apple-style design system
│       └── main.jsx          # React entry point
├── docs/                     # Additional documentation
└── logs/                     # Trace logs (R-LOG-01)
```

## 🔐 Environment Variables

Create `.env` files if needed:

**Backend** (optional):
```
MONGODB_URL=mongodb://localhost:27017
```

**Frontend** (optional):
```
VITE_API_BASE=http://localhost:8000
```

## 📊 Key Endpoints

### Candidates
- `POST /api/candidates` - Register candidate
- `POST /api/candidates/{id}/tracks` - Start test session
- `GET /api/candidates/{id}/scores/{track}` - Get score report
- `POST /api/candidates/{id}/share` - Share with employer

### Tests
- `GET /api/tests/{sessionId}/next` - Get next question
- `POST /api/tests/{sessionId}/responses` - Submit response
- `POST /api/tests/{sessionId}/submit` - Finalize test

### Employers
- `POST /api/employers` - Register employer
- `POST /api/employers/{id}/jobs` - Create job requirement
- `GET /api/employers/{id}/jobs/{jobId}/eligible` - Get eligible candidates

### Admin
- `POST /api/admin/scrape-leetcode` - Scrape LeetCode problems
- `GET /api/admin/item-bank-stats` - View item bank statistics

## 🐛 Troubleshooting

### MongoDB Connection Issues
```bash
# Check if MongoDB is running
brew services list  # macOS
sudo systemctl status mongodb  # Linux

# Restart MongoDB
brew services restart mongodb-community  # macOS
sudo systemctl restart mongodb  # Linux
```

### Port Already in Use
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9

# Kill process on port 5173
lsof -ti:5173 | xargs kill -9
```

### Frontend Not Connecting to Backend
1. Verify backend is running at http://localhost:8000
2. Check browser console for CORS errors
3. Verify VITE_API_BASE in frontend

## 🎓 Demo Preparation

Before your demo:

1. ✅ Start MongoDB
2. ✅ Start backend API
3. ✅ Run sample data population script
4. ✅ Start frontend
5. ✅ Open http://localhost:5173
6. ✅ Test both candidate and employer flows
7. ✅ Note employer IDs for sharing demonstration

## 📝 Spec Compliance

This implementation follows the complete spec sheet at:
`VGP_Technical_Proficiency_Platform_Spec.md`

All requirements from Parts A-D are implemented and tested.

## 🤝 Contributing

This is a class project. For questions, see the spec sheet or contact the project team.

## 📜 License

Academic project - Northeastern University, Fall 2025
