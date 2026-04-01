from typing import TypedDict, Dict, Any
from langgraph.graph import StateGraph

class State(TypedDict):
    counter: int
    messages: list
    status: str

def increment(state: State) -> Dict[str, Any]:
    current_counter = state["counter"]
    new_counter = current_counter + 1

    return {
        "counter": new_counter,
        "messages": [
            f"카운터가 {new_counter}로 증가했습니다.",
        ],
        "status": "incremented"
    }

def process_data(data):
    return f"Processed: {data}"

def standard_node(state:State) -> Dict[str, Any]:
    input_data = state.get("input_filed", "default_value")
    processed_data = process_data(input_data)

    return {
        "output_filed": process_data,
        "processed": True
    }

graph = StateGraph(State)
graph.add_node("increment", increment)