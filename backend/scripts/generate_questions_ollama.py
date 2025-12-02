#!/usr/bin/env python3
"""
Generate Questions for All Tracks using Ollama
Saves questions as JSON files for future use
"""

import asyncio
import json
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.services.ollama_generator import OllamaGenerator
from app.models.domain import SkillTrack


async def main():
    """Generate questions for all tracks and save as JSON"""
    
    print("🚀 Starting question generation with Ollama...")
    print("⚠️  Make sure Ollama is running: ollama serve")
    print("⚠️  Make sure you have a model pulled: ollama pull llama3.1:8b\n")
    
    generator = OllamaGenerator(model="llama3.1:8b")
    
    tracks = [
        SkillTrack.python_core_v1,
        SkillTrack.sql_core_v1,
        SkillTrack.javascript_core_v1
    ]
    
    output_dir = Path(__file__).parent.parent / "app" / "data" / "generated_questions"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    all_questions = []
    
    for track in tracks:
        print(f"\n📝 Generating questions for {track.value}...")
        try:
            questions = await generator.generate_question_set(track, questions_per_difficulty=5)
            
            # Save track-specific questions
            track_file = output_dir / f"{track.value}_questions.json"
            with open(track_file, "w") as f:
                json.dump(questions, f, indent=2)
            print(f"✅ Saved {len(questions)} questions to {track_file}")
            
            all_questions.extend(questions)
            
        except Exception as e:
            print(f"❌ Failed to generate questions for {track.value}: {e}")
            continue
    
    # Save all questions together
    all_file = output_dir / "all_questions.json"
    with open(all_file, "w") as f:
        json.dump(all_questions, f, indent=2)
    print(f"\n✅ Saved {len(all_questions)} total questions to {all_file}")
    
    print("\n✨ Question generation complete!")
    print(f"📁 Questions saved in: {output_dir}")
    print("\n💡 Next step: Run 'python scripts/load_questions.py' to load into database")


if __name__ == "__main__":
    asyncio.run(main())

