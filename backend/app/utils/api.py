from typing import Any, Dict

from .ids import new_id


def envelope(data: Any) -> Dict[str, Any]:
    return {"data": data, "traceId": new_id("trace")}
