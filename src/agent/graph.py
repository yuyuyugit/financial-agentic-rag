from langgraph.graph import StateGraph, END
from .state import AgentState
from .nodes import analyze_node, retrieve_node, generate_node, should_continue

graph = StateGraph(AgentState)

graph.add_node("analyze", analyze_node)
graph.add_node("retrieve", retrieve_node)
graph.add_node("generate", generate_node)

graph.set_entry_point("analyze")

graph.add_conditional_edges(
    "analyze",
    should_continue,
    {"retrieve": "retrieve", "generate": "generate", END: END}
)

graph.add_edge("retrieve", "generate")

graph.add_conditional_edges(
    "generate",
    should_continue,
    {END: END, "retrieve": "retrieve"}
)

agent_graph = graph.compile()


def run_agent(query: str) -> str:
    """Run the agent with the given query and return the final answer."""
    initial_state = {
        "messages": [],
        "query": query,
        "intent": "",
        "retrieved_docs": [],
        "tool_calls": [],
        "final_answer": "",
        "iteration_count": 0
    }
    result = agent_graph.invoke(initial_state)
    return result["final_answer"]
