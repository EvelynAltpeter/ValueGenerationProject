import json
from functools import lru_cache
from pathlib import Path
from typing import List

from ..models.domain import DifficultyBand, QuestionMetadata, SkillTrack

DATA_DIR = Path(__file__).resolve().parents[1] / "data"


@lru_cache(maxsize=1)
def _load_questions() -> List[QuestionMetadata]:
    path = DATA_DIR / "item_bank.json"
    raw = json.loads(path.read_text(encoding="utf-8"))
    return [QuestionMetadata(**item) for item in raw]


def get_questions_for_track(track: SkillTrack, band: DifficultyBand | None = None) -> List[QuestionMetadata]:
    questions = [q for q in _load_questions() if q.trackId == track]
    if band:
        questions = [q for q in questions if q.difficulty == band]
    return questions


def get_question(question_id: str) -> QuestionMetadata | None:
    for q in _load_questions():
        if q.questionId == question_id:
            return q
    return None
