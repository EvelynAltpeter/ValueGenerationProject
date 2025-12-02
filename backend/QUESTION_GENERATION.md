# Question Generation Guide

This guide explains how to generate and load test questions for the VGP Platform.

## Quick Start - Load Existing Questions

If questions already exist in JSON files (they should be in `app/data/generated_questions/`):

```bash
cd backend
source venv/bin/activate  # or use ./venv/bin/python directly

# Load questions into database
python scripts/load_questions.py

# Or via API (if backend is running)
curl -X POST http://localhost:8000/api/admin/load-questions
```

**Note**: Questions are automatically loaded on backend startup if the database is empty.

## Generate New Questions with Ollama

### Prerequisites

1. **Ollama must be installed and running**:
   ```bash
   # Check if Ollama is installed
   which ollama
   
   # Start Ollama server (in a separate terminal)
   ollama serve
   
   # Pull a model if needed
   ollama pull llama3.1:8b
   # or
   ollama pull llama2
   ```

### Generate Questions

```bash
cd backend
source venv/bin/activate

# Generate questions using Ollama (takes several minutes)
python scripts/generate_questions_ollama.py
```

This will:
- Generate questions for Python, SQL, and JavaScript tracks
- Create questions at easy, medium, and hard difficulty levels
- Include both MCQ and coding questions
- Save questions as JSON files in `app/data/generated_questions/`

### Load Generated Questions

After generation, load them into the database:

```bash
# Via script
python scripts/load_questions.py

# Or via API
curl -X POST http://localhost:8000/api/admin/load-questions
```

## Question Storage

All generated questions are saved as JSON files in:
```
backend/app/data/generated_questions/
├── all_questions.json              # All questions combined
├── python_core_v1_questions.json   # Python questions only
├── sql_core_v1_questions.json      # SQL questions only
└── javascript_core_v1_questions.json # JavaScript questions only
```

**These JSON files are committed to the repo** and can be reused across deployments.

## Auto-Load on Startup

The backend automatically tries to load questions from JSON files when it starts **if the database is empty**. This ensures questions are available even with in-memory databases.

## API Endpoints

### Load Questions
```bash
POST /api/admin/load-questions
```

### Check Question Stats
```bash
GET /api/admin/item-bank-stats
```

Example response:
```json
{
  "data": {
    "total": 22,
    "byTrack": {
      "python_core_v1": 10,
      "sql_core_v1": 6,
      "javascript_core_v1": 6
    },
    "byDifficulty": {
      "easy": 11,
      "medium": 7,
      "hard": 4
    }
  }
}
```

## Question Format

Each question follows this structure:

```json
{
  "questionId": "py-easy-1",
  "trackId": "python_core_v1",
  "prompt": "Question text here",
  "questionType": "mcq" or "coding",
  "difficulty": "easy" | "medium" | "hard",
  "tags": ["tag1", "tag2"],
  "subskill": "data_structures" | "algorithms" | "code_quality",
  "timeLimitSeconds": 120,
  
  // For MCQ questions:
  "options": ["option1", "option2", "option3", "option4"],
  "answerKey": "correct option",
  
  // For coding questions:
  "referenceSolution": "def solution(): ..."
}
```

## Troubleshooting

### "No questions found" error
- Check that JSON files exist in `app/data/generated_questions/`
- Verify JSON format is valid
- Run `python scripts/load_questions.py` manually
- Check backend logs for errors

### Ollama connection error
- Make sure Ollama is running: `ollama serve`
- Check if model is available: `ollama list`
- Pull the model if missing: `ollama pull llama3.1:8b`

### Questions not appearing in tests
- Verify questions are loaded: `GET /api/admin/item-bank-stats`
- Check that questions match the track (python_core_v1, sql_core_v1, javascript_core_v1)
- Verify questions have correct difficulty levels
- Restart backend to trigger auto-load

