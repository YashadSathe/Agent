from pydantic import BaseModel, Field
from typing import Any, Literal
from datetime import datetime, timezone

def _get_utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()

class PlatformEvent(BaseModel):
    type: Literal["status", "token", "tool", "error", "done"]
    agent: str
    timestamp: str = Field(default_factory = _get_utc_now)
    data: dict[str, Any]