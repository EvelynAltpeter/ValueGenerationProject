# 🚀 Quick Start Guide

**Get the VGP Platform running in 5 minutes**

## Prerequisites Check

```bash
# Check Python version (need 3.11+)
python3 --version

# Check Node.js version (need 18+)
node --version

# Check MongoDB (or install it)
mongod --version
```

## Step 1: Install MongoDB (if needed)

### macOS
```bash
brew tap mongodb/brew
brew install mongodb-community
brew services start mongodb-community
```

### Linux/Ubuntu
```bash
sudo apt-get update
sudo apt-get install -y mongodb
sudo systemctl start mongodb
sudo systemctl enable mongodb
```

### Verify MongoDB is running
```bash
mongosh --eval "db.version()"
```

## Step 2: Start Backend

```bash
# Navigate to project
cd /Users/evelynaltpeter/Desktop/ValueGenerationProject/backend

# Create virtual environment (first time only)
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies (first time only)
pip install -r requirements.txt

# Start the server
uvicorn app.main:app --reload --port 8000
```

✅ **Backend should now be running at:** http://localhost:8000

Test it: Open http://localhost:8000/docs in your browser

## Step 3: Populate Sample Data

**Open a NEW terminal** (keep backend running)

```bash
cd /Users/evelynaltpeter/Desktop/ValueGenerationProject/backend

# Activate venv
source venv/bin/activate

# Run population script
python scripts/populate_sample_data.py
```

You should see output like:
```
🚀 Connecting to MongoDB...
✅ Connected to MongoDB
📝 Creating sample employers...
✅ Created employers: emp_xxx, emp_yyy, emp_zzz
...
✨ Sample data population complete!
```

**Save the Employer IDs** shown in the output - you'll need these for testing!

## Step 4: Start Frontend

**Open a NEW terminal** (keep backend running)

```bash
cd /Users/evelynaltpeter/Desktop/ValueGenerationProject/frontend

# Install dependencies (first time only)
npm install

# Start development server
npm run dev
```

✅ **Frontend should now be running at:** http://localhost:5173

## Step 5: Test the Application

### Test Candidate Flow

1. Open http://localhost:5173
2. Click **"I'm a Candidate"**
3. Fill in the form:
   - Name: `Test User`
   - Email: `test@example.com`
   - (Fill other fields)
4. Click **"Create Profile & Continue"**
5. Click **"🐍 Python Core"** to start a test
6. Answer a few questions
7. Click **"Finish Test"**
8. View your score report with strengths/weaknesses
9. In "Share With Employers", enter one of the employer IDs from Step 3
10. Click **"Share"**

### Test Employer Flow

1. Open http://localhost:5173 in a NEW incognito/private window
2. Click **"I'm an Employer"**
3. Enter company name: `Test Company`
4. Click **"Create Account & Continue"**
5. **Copy your Employer ID** (shown at top of dashboard)
6. Fill in job form:
   - Job ID: `test-job-001`
   - Track: `Python Core`
   - Min Score: `70`
7. Click **"Create Job Requirement"**
8. Click **"View Candidates"** on your job
9. You should see candidates from the sample data who meet your criteria!

## 🎯 Quick Test Checklist

- [ ] Backend running at http://localhost:8000
- [ ] Frontend running at http://localhost:5173
- [ ] MongoDB is running (`brew services list` or `systemctl status mongodb`)
- [ ] Sample data populated (5 candidates, 3 employers)
- [ ] Can create candidate profile
- [ ] Can take a test and see score report
- [ ] Can create employer account
- [ ] Can create job requirements
- [ ] Can view eligible candidates

## 🐛 Common Issues

### "Connection refused" error
**Problem:** Backend isn't running or wrong port

**Solution:**
```bash
# Check if something is running on port 8000
lsof -ti:8000

# If yes, kill it and restart backend
lsof -ti:8000 | xargs kill -9
uvicorn app.main:app --reload --port 8000
```

### "Unable to connect to MongoDB"
**Problem:** MongoDB isn't running

**Solution:**
```bash
# macOS
brew services start mongodb-community

# Linux
sudo systemctl start mongodb

# Verify
mongosh --eval "db.version()"
```

### Frontend shows "Unable to create profile"
**Problem:** Backend isn't accessible

**Solution:**
1. Verify backend is running at http://localhost:8000
2. Try opening http://localhost:8000/health
3. Check browser console for CORS errors

### "No eligible candidates" in employer view
**Problem:** Candidates haven't shared scores

**Solution:**
1. Go to candidate flow
2. After getting a score, use "Share With Employers"
3. Enter the employer ID you copied
4. Go back to employer view and refresh

## 🎨 UI Features to Show Off

### Apple-Style Design
- Clean, high-contrast typography
- Subtle shadows and depth
- Smooth transitions and animations
- Consistent spacing and alignment
- Professional color palette

### User Experience
- Separate landing pages for clarity
- Clear call-to-action buttons
- Real-time status messages
- Timer visibility during tests
- Transparent match explanations

### Data Visualization
- Large score displays
- Score breakdowns
- Strengths/weaknesses tags
- Match percentage badges
- Clean data tables

## 📊 Sample Data Overview

After running the population script:

**Employers:**
- TechCorp Inc
- DataSystems LLC
- CodeFactory

**Candidates:** (all shared with all employers)
- Alice Johnson - Python: 85 (82nd percentile)
- Bob Smith - Python: 72 (68th percentile)
- Carol White - SQL: 90 (88th percentile)
- David Lee - JavaScript: 78 (74th percentile)
- Emma Davis - Python: 95 (94th percentile)

**Jobs:**
- TechCorp: Python role, min score 70
- DataSystems: SQL role, min score 65
- CodeFactory: Python + JavaScript, min score 75

## 🎓 Demo Script

**For presentation:**

1. **Show landing page** - "Clean role selection"
2. **Candidate flow** - "Create profile in seconds"
3. **Take test** - "Adaptive difficulty adjustment"
4. **Score report** - "Comprehensive feedback with strengths"
5. **Employer flow** - "Simple job requirement setup"
6. **Candidate filtering** - "Privacy-compliant matching"
7. **Match quality** - "Transparent score explanations"

## 📝 Next Steps

Once everything is working:

1. ✅ Familiarize yourself with both flows
2. ✅ Try different test scenarios
3. ✅ Test privacy features (sharing/not sharing)
4. ✅ Explore the API docs at http://localhost:8000/docs
5. ✅ Review the README for full documentation

## 🆘 Need Help?

1. Check `README.md` for detailed documentation
2. Check `IMPLEMENTATION_SUMMARY.md` for technical details
3. Check backend logs in terminal
4. Check browser console for frontend errors
5. Verify MongoDB is running

---

**Happy Testing! 🎉**

