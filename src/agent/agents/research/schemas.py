from pydantic import BaseModel, Field
from typing import Optional

class PlannerDecision (BaseModel):
    needs_research: bool = Field (
        description = "True if the request requires current real-time information, external data, documentation, or comparisons not found in static knowledge. False if it is general knowledge, greeting, or philosophical clarification."
    )
    reasoning: str = Field (
        default="No reasoning provided by the model.",
        description = "A brief execution thought process explaining why research is or is not required."
    )
    search_query: Optional[str] = Field (
        default = None,
        description = "If needs_research is True, provide a crisp, optimized search engine query (keywords only, no natural language filler). If False, leave this empty or None."
    )