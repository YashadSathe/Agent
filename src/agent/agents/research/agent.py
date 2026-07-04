from typing import AsyncGenerator
from langchain_core.messages import HumanMessage

from agent.schemas.events import PlatformEvent
from agent.agents.research.graph import research_agent_graph

async def run_research_agent(user_input: str) -> AsyncGenerator[PlatformEvent, None]:
    initial_state: dict = {
        "messages": [HumanMessage(content=user_input)],
        "needs_research": False,
        "search_query": None,
        "research_results": []
    }

    try:
        current_query = None
        final_response = "Execution complete, but no final message was generated."

        async for step_output in research_agent_graph.astream(initial_state):
            for node_name, state_update in step_output.items():

                if "search_query" in state_update and state_update["search_query"]:
                    current_query = state_update["search_query"]

                yield PlatformEvent(
                    type="status",
                    agent="research",
                    data={
                        "step": node_name,
                        "message": f"Completed execution of {node_name}."
                    }
                )

                if node_name == "research" and state_update and "research_results" in state_update:
                    yield PlatformEvent(
                        type="tool",
                        agent="research",
                        data={
                            "tool_name": "DuckDuckGo",
                            "query": current_query, # Now this will populate correctly!
                            "status": "success"
                        }
                    )

                if node_name == "generator" and state_update and "messages" in state_update:
                    messages_update = state_update["messages"]
                    final_msg = messages_update[-1] if isinstance(messages_update, list) else messages_update
                    final_response = final_msg.content
                    
        yield PlatformEvent(
            type="done",
            agent="research",
            data={
                "message": final_response
            }
        )

    except Exception as e:
        yield PlatformEvent(
            type="error",
            agent="research",
            data={"message": str(e)}
        )