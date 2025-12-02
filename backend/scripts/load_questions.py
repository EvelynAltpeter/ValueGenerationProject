#!/usr/bin/env python3
"""
Load Questions from JSON files into the database
Can be run standalone or called from admin API
"""

import asyncio
import json
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.database import MongoDB
from app.models.domain import QuestionMetadata
from app.database import get_item_bank_collection


async def load_questions_from_json():
    """Load questions from JSON files into database"""
    
    print("🔄 Loading questions into database...")
    
    # Connect to database
    await MongoDB.connect_db()
    
    try:
        collection = get_item_bank_collection()
        
        # Try to load from multiple possible locations
        data_dir = Path(__file__).parent.parent / "app" / "data"
        
        # Check for generated questions first
        generated_dir = data_dir / "generated_questions"
        json_files = []
        
        if generated_dir.exists():
            all_questions_file = generated_dir / "all_questions.json"
            if all_questions_file.exists():
                json_files.append(all_questions_file)
                print(f"📁 Found: {all_questions_file}")
            else:
                # Load individual track files
                for track_file in generated_dir.glob("*_questions.json"):
                    json_files.append(track_file)
                    print(f"📁 Found: {track_file}")
        
        # Fallback to original item_bank.json
        if not json_files:
            item_bank_file = data_dir / "item_bank.json"
            if item_bank_file.exists():
                json_files.append(item_bank_file)
                print(f"📁 Found: {item_bank_file}")
        
        if not json_files:
            print("❌ No question JSON files found!")
            print("   Run generate_demo_questions.py first or ensure item_bank.json exists")
            return
        
        total_loaded = 0
        errors = []
        
        for json_file in json_files:
            try:
                with open(json_file, "r") as f:
                    questions_data = json.load(f)
                
                # Ensure it's a list
                if isinstance(questions_data, dict):
                    questions_data = [questions_data]
                
                print(f"\n📖 Processing {json_file.name}...")
                
                for q_data in questions_data:
                    try:
                        # Validate and convert to QuestionMetadata
                        question = QuestionMetadata(**q_data)
                        
                        # Insert or update (upsert based on questionId)
                        await collection.update_one(
                            {"questionId": question.questionId},
                            {"$set": question.model_dump()},
                            upsert=True
                        )
                        total_loaded += 1
                        
                    except Exception as e:
                        errors.append(f"Error loading question {q_data.get('questionId', 'unknown')}: {str(e)}")
                        continue
                        
            except Exception as e:
                errors.append(f"Error reading file {json_file}: {str(e)}")
                continue
        
        print(f"\n✅ Successfully loaded {total_loaded} questions into database")
        
        if errors:
            print(f"\n⚠️  {len(errors)} errors encountered:")
            for error in errors[:5]:  # Show first 5 errors
                print(f"   - {error}")
            if len(errors) > 5:
                print(f"   ... and {len(errors) - 5} more")
    
    finally:
        await MongoDB.close_db()


if __name__ == "__main__":
    asyncio.run(load_questions_from_json())

