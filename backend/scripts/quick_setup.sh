#!/bin/bash
# Quick setup script to load questions and sample candidates

echo "🚀 Quick Setup - Loading Questions and Sample Candidates"
echo ""

cd "$(dirname "$0")/.."

# Load questions
echo "📚 Loading questions..."
python scripts/load_questions.py

echo ""
echo "👥 Loading sample candidates..."
python scripts/populate_sample_candidates.py

echo ""
echo "✅ Setup complete!"
echo ""
echo "The database now contains:"
echo "  - Questions for all 3 tracks (Python, SQL, JavaScript)"
echo "  - 20 sample candidates with scores"
echo "  - Sample employers"
echo ""
echo "💡 Note: Since we're using in-memory database, run this script after each backend restart"

