from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class PublicState(TypedDict):
    user_query: str
    final_answer: str

class PrivateState(TypedDict):
    intermediate_result: str
    processing_metadata: dict

def node_1(state: PublicState) -> PrivateState:
    query = state["user_query"]

    return {
        "intermediate_result": f"처리됨: {query}",
        "processing_metadata": {
            "step": 1,
            "status": "preprocessed"
        }
    }

def node_2(state:PrivateState) -> PublicState:
    intermediate = state["intermediate_result"]
    metadata = state["processing_metadata"]

    return{
        "final_answer": f"완료! {intermediate} (딘계: {metadata['step']})"
    }

def node_3(state: PublicState) -> dict:
    return {
        "final_answer": state["final_answer"] + " [검증됨]"
    }

builder = StateGraph(PublicState)
builder.add_node("node_1", node_1)
builder.add_node("node_2", node_2)
builder.add_node("node_3", node_3)

builder.add_edge(START, "node_1")
builder.add_edge("node_1", "node_2")
builder.add_edge("node_2", "node_3")
builder.add_edge("node_3", END)

graph = builder.compile()

result = graph.invoke({"user_query": "Python이란?"})
print(result)