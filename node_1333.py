from typing import TypedDict, Dict, Any, Optional
from langgraph.graph import StateGraph
from datetime import datetime
from typing import Annotated
import operator, asyncio

class State(TypedDict):
    count: int

def perform_sync_operation(data):
    import time
    time.sleep(0.1)
    return f"Sync result: {data}"

def sync_node(state: State) -> Dict[str, Any]:
    result = perform_sync_operation(state["input"])
    return {"output": result}

def perform_sync_operation(data):
    import time
    time.sleep(0.1)
    return f"Sync result: {data}"

async def async_node(state:State) -> Dict[str, Any]:
    result = await perform_sync_operation(state["input"])
    results = await asyncio.gather(
        fetch_data_1(),
        fetch_data_2(),
        fetch_data_3()
    )
    return {
        "output": result,
        "additional_data": results
    }

async def perform_async_operation(data):
    await asyncio.sleep(0.1)
    return f"Async result: {data}"

async def fetch_data_1():
    await asyncio.sleep(0.05)
    return "data_1"

async def fetch_data_2():
    await asyncio.sleep(0.05)
    return "data_2"

async def fetch_data_3():
    await asyncio.sleep(0.05)
    return "data_3"

def condtional_node(state:State) -> Dict[str, Any]:
    mode = state.get("mode", "default")

    if mode == "fast":
        result = quick_process(state)
        excution_time = "fast"
    elif mode == "thorough":
        result = thorough_process(state)
        excution_time = "slow"
    else:
        result = default_process(state)
        execution_time = "normal"
    
    return {
        "result": result,
        "execution_time": execution_time,
        "mode_used": mode
    }

def quick_process(state):
    return {
        "status": "quick",
        "data": state.get("input", "")[:10]
    }

def thorough_process(state):
    return {
        "status": "thorough",
        "data": analyze_deeply(state.get("input", ""))
    }

def default_process(state):
    return {
        "status": "default",
        "data": state.get("input", "")
    }

def analyze_deeply(data):
    return f"Deeply analyzed: {data}"

class ValidationState(TypedDict):
    input_data: Any
    validation_errors: list[str]
    is_valid: bool

def validation_node(state: ValidationState) -> Dict[str, Any]:
    input_data = state["input_data"]
    errors = []
    
    if not input_data:
        errors.append("입력 데이터가 비어있습니다.")

    if isinstance(input_data, str):
        if len(input_data) < 3:
            errors.append("문자열이 너무 짧습니다. (최소 3자).")
        if len(input_data) > 1000:
            errors.append("문자열이 너무 깁니다 (최대 1000자).")
        if not input_data.isascii():
            errors.append("ASCII 문자만 허용됩니다.")

    elif isinstance(input_data, (int, float)):
        if input_data < 0:
            errors.append("음수는 허용되지 않습니다.")
        if input_data > 1000000:
            errors.append("값이 너무 큽니다. (최대 1,000,000)")
    
    elif isinstance(input_data, list):
        if len(input_data) == 0:
            errors.append("리스트가 비어있습니다.")
        if len(input_data) > 100:
            errors.append("리스트 항목이 너무 많습니다. (최대 100개)")
    
    return {
        "validation_errors": errors,
        "is_valid": len(errors) == 0
    }