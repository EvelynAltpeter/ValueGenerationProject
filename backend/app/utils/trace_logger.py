import json
from pathlib import Path
from typing import Any, Dict, Optional

from .time import utc_now_iso

TRACE_PATH = Path(__file__).resolve().parents[3] / "logs" / "trace.jsonl"
PROMPT_TRACE_PATH = Path(__file__).resolve().parents[3] / "logs" / "prompt_trace.jsonl"


def _write_line(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(payload) + "\n")


def log_event(event_type: str, actor_id: Optional[str], payload: Dict[str, Any]) -> None:
    """
    R-LOG-01: Log all test events for auditability.
    
    This function logs every user action, system response, rule update, and test result
    to ensure full traceability and debugging capability.
    """
    record = {
        "timestamp": utc_now_iso(),
        "eventType": event_type,
        "actorId": actor_id,
        "payload": payload,
        "ruleCompliance": "R-LOG-01",  # Mark as compliant with logging rule
    }
    _write_line(TRACE_PATH, record)
    _write_line(PROMPT_TRACE_PATH, record)
