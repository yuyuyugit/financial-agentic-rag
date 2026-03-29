from typing import TypedDict, Annotated
import operator


class AgentState(TypedDict):
    messages: Annotated[list, operator.add]
    query: str
    intent: str
    retrieved_docs: list[dict]
    tool_calls: list[dict]
    final_answer: str
    iteration_count: int
