from typing import TypedDict, Dict, Any
from langgraph.graph import StateGraph
from datetime import datetime
from typing import Annotated
import operator

class DataState(TypedDict):
    raw_data: str
    processed_data: dict
    meta: dict

def data_processor_node(state: DataState) -> Dict[str, Any]:
    raw_data = state["raw_data"]

    lines = raw_data.strip().split('\n')

    processed = {
        "total_lines": len(lines),
        "content": lines,
        "first_line": lines[0] if lines else "",
        "last_line": lines[-1] if lines else ""
    }

    metadata = {
        "processed_at": datetime.now().isoformat(),
        "processor_version": "1.0.0",
        "data_size": len(raw_data)
    }

    return {
        "processed_data": processed,
        "metadata": metadata
    }

class CalculationState(TypedDict):
    numbers: list[float]
    operation: str
    result: float
    history: list[dict]

def calculator_node(state:CalculationState) -> Dict[str, Any]:
    numbers = state["numbers"]
    operation = state["operation"]

    if operation == "sum":
        result = sum(numbers)
    elif operation == "multiply":
        result = 1
        for num in numbers:
            result *= num
    elif operation == "average":
        result = sum(numbers) / len (numbers) if numbers else 0

    history_entry = {
        "operation": operation,
        "inputs": numbers,
        "result": result,
        "timestamp": datetime.now().isoformat()
    }

    return {
        "result": result,
        "history": [history_entry]
    }

class UpdateState(TypedDict):
    counter: int
    items: Annotated[list, operator.add]
    flags: dict

def update_node(state: UpdateState) -> Dict[str, Any]:
    new_counter = state["counter"] + 1
    new_items = ["new_item"]
    updated_flags = state["flags"].copy()
    updated_flags["processed"] = True
    updated_flags["node_name"] = "update_node"

    return {
        "counter": new_counter,
        "items": new_items,
        "flags": updated_flags
    }
    