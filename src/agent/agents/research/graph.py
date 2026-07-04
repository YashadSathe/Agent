from typing import Literal, cast
from langgraph.graph import StateGraph, START, END
from langgraph.types import Command
from langchain_core.messages import SystemMessage
from langchain_community.tools import DuckDuckGoSearchRun
from agent.agents.research.state import ResearchAgentState
from agent.agents.research.schemas import PlannerDecision
from agent.services.llm import get_llm

def planner_node(state: ResearchAgentState) -> Command[Literal["research", "generator"]]:
    print("Node: Planner [Invoking LLM for routing decision...]")
    
    llm = get_llm(temperature=0.0)
    structured_llm = llm.with_structured_output(PlannerDecision)
    
    system_prompt = (
        "You are the orchestration planner for a Research Agent. Your sole job is to read the "
        "conversation history and determine if external web research is necessary to accurately "
        "and safely answer the user's latest request. "
        "Turn 'needs_research' to True if the query requires up-to-date facts, current events, "
        "software version comparisons, or specific external documentation. "
        "Turn 'needs_research' to False if the query is a greeting, conversational filler, a fundamental "
        "concept explanation (like basic math or code logic), or a continuation of an already clear topic."
    )
    
    messages = [{"role": "system", "content": system_prompt}] + list(state["messages"])
    decision = cast(PlannerDecision, structured_llm.invoke(messages))
    
    print(f"Decision: needs_research={decision.needs_research}")
    print(f"Reasoning: {decision.reasoning}")
    
    if decision.needs_research:
        return Command(
            goto = "research",
            update = {
                "needs_research": True,
                "search_query": decision.search_query
            }
        )
    else:
        return Command(
            goto="generator",
            update = {
                "needs_research": False,
                "search_query": None
            }
        )

def research_node(state: ResearchAgentState) -> dict:
    query = state.get("search_query")
    print(f"Node: Research [Executing live search for: '{query}']")
          
    if not query:
        print("Warning: Research node reached but no search query was found in state.")
        return {"research_results": ["No query provided."]}

    try:
        search_tool = DuckDuckGoSearchRun()

        raw_results = search_tool.run(query)

        print("Search successful. Captured live data chunks.")
        return {"research_results": [raw_results]}

    except Exception as e:
        print(f"Search failed. Error details: {e}")
        return {"research_results": [f"Search error occurred: {str(e)}"]}

def generator_node(state: ResearchAgentState) -> dict:
    print("Node: Generator [Formulating final response...]")

    llm = get_llm(temperature = 0.7)

    system_prompt = (
        "You are an intelligent Research Assistant. Answer the user's latest query accurately. "
        "If external research was provided below, you MUST use it to inform your answer. "
        "Do not mention that you 'performed a web search' or 'used a tool', just integrate the facts naturally."
    )

    # inject live data (if research ran)
    if state.get("research_results"):
        system_prompt +="\n\n External Research Data \n"
        for result in state["research_results"]:
            system_prompt += f"{result} \n"

    messages = [SystemMessage(content = system_prompt)] + list(state["messages"])

    response = llm.invoke(messages)

    return {"messages": response}


builder = StateGraph(ResearchAgentState)
builder.add_node("planner", planner_node)
builder.add_node("research", research_node)
builder.add_node("generator", generator_node)

builder.add_edge(START, "planner")
builder.add_edge("research", "generator")
builder.add_edge("generator", END)

research_agent_graph = builder.compile()