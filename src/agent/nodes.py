import os
import yaml
from pathlib import Path
from langchain_openai import ChatOpenAI
from langchain_core.messages import ToolMessage
from langgraph.graph import END
from .state import AgentState
from src.tools import all_tools
from src.retrieval import hybrid_search
from src.retrieval.weaviate_client import get_client, create_schema

config_path = Path(__file__).parent.parent / "config" / "agent.yaml"
with open(config_path) as f:
    config = yaml.safe_load(f)

_base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1"
_api_key = os.getenv("DASHSCOPE_API_KEY")

llm_analyze = ChatOpenAI(
    model=config["model"]["analyze"],
    temperature=config["model"]["temperature"],
    api_key=_api_key,
    base_url=_base_url,
)

llm_generate = ChatOpenAI(
    model=config["model"]["generate"],
    temperature=config["model"]["temperature"],
    api_key=_api_key,
    base_url=_base_url,
)


_llm_with_tools = llm_analyze.bind_tools(all_tools)


def analyze_node(state: AgentState) -> dict:
    """Analyze query and decide next action."""
    if state.get("intent"):
        return {}
    system_prompt = config["nodes"]["analyze"]["system_prompt"]
    response = _llm_with_tools.invoke([
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": state["query"]}
    ])
    if response.tool_calls:
        return {"intent": "tool_call", "tool_calls": response.tool_calls}
    intent = "retrieve_docs" if "retrieve" in response.content.lower() else "generate_answer"
    return {"intent": intent}


def tool_node(state: AgentState) -> dict:
    """Execute tool calls and return results as messages."""
    tool_map = {t.name: t for t in all_tools}
    messages = list(state.get("messages", []))
    for tc in state["tool_calls"]:
        result = tool_map[tc["name"]].invoke(tc["args"])
        messages.append(ToolMessage(content=str(result), tool_call_id=tc["id"]))
    return {"messages": messages, "intent": "generate"}


def retrieve_node(state: AgentState) -> dict:
    """Retrieve documents via hybrid search."""
    client = get_client()
    create_schema(client)
    docs = hybrid_search(client, state["query"])
    return {"retrieved_docs": docs, "intent": "generate"}


def generate_node(state: AgentState) -> dict:
    """Generate final answer using LLM."""
    context = "\n".join([doc["content"] for doc in state["retrieved_docs"]])
    response = llm_generate.invoke([
        {"role": "user", "content": f"Query: {state['query']}\n\nContext:\n{context}"}
    ])
    return {"final_answer": response.content, "intent": "done"}


def should_continue(state: AgentState) -> str:
    """Determine next node or end."""
    if state["intent"] == "tool_call":
        return "tool"
    elif state["intent"] == "retrieve_docs":
        return "retrieve"
    elif state["intent"] == "generate_answer":
        return "generate"
    elif state["intent"] == "done" or state["iteration_count"] > 3:
        return END
    return END
