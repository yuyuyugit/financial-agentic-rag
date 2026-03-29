import os
import yaml
from pathlib import Path
from langchain_openai import ChatOpenAI
from langgraph.graph import END
from .state import AgentState

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


def analyze_node(state: AgentState) -> dict:
    """Analyze query and decide next action."""
    system_prompt = config["nodes"]["analyze"]["system_prompt"]
    response = llm_analyze.invoke([
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": state["query"]}
    ])
    intent = "retrieve_docs" if "retrieve" in response.content.lower() else "generate_answer"
    return {"intent": intent}


def retrieve_node(state: AgentState) -> dict:
    """Retrieve documents (placeholder)."""
    return {
        "retrieved_docs": [{"content": f"Mock document for: {state['query']}", "source": "mock"}],
        "intent": "generate"
    }


def generate_node(state: AgentState) -> dict:
    """Generate final answer using LLM."""
    context = "\n".join([doc["content"] for doc in state["retrieved_docs"]])
    response = llm_generate.invoke([
        {"role": "user", "content": f"Query: {state['query']}\n\nContext:\n{context}"}
    ])
    return {"final_answer": response.content, "intent": "done"}


def should_continue(state: AgentState) -> str:
    """Determine next node or end."""
    if state["intent"] == "retrieve_docs":
        return "retrieve"
    elif state["intent"] == "generate_answer":
        return "generate"
    elif state["intent"] == "done" or state["iteration_count"] > 3:
        return END
    return END
