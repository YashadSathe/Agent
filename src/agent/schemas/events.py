from pydantic import BaseModel, Field
from typing import Any, Literal
from datetime import datetime, timezone

class PerformEvent(BaseModel):
    type: Literal["status", "token", "tool", "error", "done"]
    agent: str
    timestamp: str = Field(default_factory = lambda: datetime.now(timezone.utc).isoformat())
    data: dict[str, Any]