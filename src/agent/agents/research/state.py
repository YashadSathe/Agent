from typing import TypedDict, Annotated, Sequence, Optional
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

class ResearchAgentState(TypedDict):

    messages: Annotated[Sequence[BaseMessage], add_messages]
    needs_research: bool
    search_query: Optional[str]
    research_results: list[str]