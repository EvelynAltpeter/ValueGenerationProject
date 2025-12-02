"""
Item Bank Service - MongoDB Implementation
Retrieves questions from MongoDB
"""

from typing import List, Optional
from ..models.domain import DifficultyBand, QuestionMetadata, SkillTrack
from ..database import get_item_bank_collection


async def get_questions_for_track(track: SkillTrack, band: Optional[DifficultyBand] = None) -> List[QuestionMetadata]:
    """Get questions for a specific track and optional difficulty band"""
    collection = get_item_bank_collection()
    query = {"trackId": track.value}
    if band:
        query["difficulty"] = band.value
    
    cursor = collection.find(query)
    questions = []
    async for doc in cursor:
        doc.pop('_id', None)
        questions.append(QuestionMetadata(**doc))
    return questions


async def get_question(question_id: str) -> Optional[QuestionMetadata]:
    """Get a specific question by ID"""
    collection = get_item_bank_collection()
    doc = await collection.find_one({"questionId": question_id})
    if not doc:
        return None
    doc.pop('_id', None)
    return QuestionMetadata(**doc)
