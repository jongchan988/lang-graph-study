from langchain_core.runnables import RunnableConfig
from typing import TypedDict, Dict, Any

class State(TypedDict):
    count: int

def process_with_model(input_data, model, temperature):
    """모델을 사용한 처리 (시뮬레이션)"""
    return f"Processed with {model} at temperature {temperature}: {input_data}"

def configurable_node(state: State, config: RunnableConfig) -> Dict[str, Any]:
    model_name = config.get("configurable", {}).get("model", "default")
    temperature = config.get("configurable", {}).get("temperature", 0.7)
    max_retries = config.get("configurable", {}).get("max_retries", 3)

    print(f"Using model: {model_name}, temperature: {temperature}")

    result = None
    for attempt in range(max_retries):
        try:
            result = process_with_model(
                state["input"],
                model= model_name,
                temperature=temperature
            )
            break
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt == max_retries - 1:
                result = "Failed after all retries"
    
    return {
        "output": result,
        "config_used":{
            "model": model_name,
            "temperature": temperature,
            "retries": max_retries
        }
    }