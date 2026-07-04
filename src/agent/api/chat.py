import json
from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from agent.schemas.api import ChatRequest
from agent.agents.research.agent import run_research_agent

router = APIRouter()

async def sse_formatter(event_generator):
    async for event in event_generator:
        # Dump the Pydantic model to a JSON string and format as SSE
        yield f"data: {event.model_dump_json()}\n\n"

@router.post("/chat", tags=["Agent Execution"])
async def chat_endpoint(request: ChatRequest):
    execution_stream = run_research_agent(request.message)

    return StreamingResponse(
        sse_formatter(execution_stream), 
        media_type="text/event-stream"
    )