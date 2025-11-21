import json
from pathlib import Path

from fastapi import APIRouter

from ..utils.api import envelope

router = APIRouter(prefix="/api/trace", tags=["trace"])
TRACE_PATH = Path(__file__).resolve().parents[2] / "logs" / "trace.jsonl"


@router.get("")
def list_events(limit: int = 20):
    if not TRACE_PATH.exists():
        return envelope([])
    lines = TRACE_PATH.read_text(encoding="utf-8").strip().splitlines()
    data = [json.loads(line) for line in lines[-limit:]]
    return envelope(data)
