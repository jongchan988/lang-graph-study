from typing_extensions import TypedDict
from operator import add
from typing import Annotated

class SimpleState(TypedDict):
    counter: int
    current_user: str
    status: str

def update_counter(state: SimpleState) -> SimpleState:
    return {"counter": state["counter"]+1}

def update_multiple(state:SimpleState) -> SimpleState:
    return {
        "counter": 0,
        "status": "completed"
    }

class AddState(TypedDict):
    messages: Annotated[list[str], add]
    log_text: Annotated[str, add]

def add_message(state: AddState) -> AddState:
    return {
        "messages": ["새 메시지"],
        "log_text": "새 로그 항목 \n"
    }
initial_state = {
    "messages": ["안녕하세요"],
    "log_text": "시작\n"
}

from langgraph.graph.message import add_messages
from langchain_core.messages import HumanMessage, AIMessage
class ChatState(TypedDict):
    messages: Annotated[list, add_messages]

def process_user_input(state: ChatState) -> ChatState:
    return {
        "messages": [HumanMessage(content="사용자 입력", id="msg_001")]
    }

from langgraph.graph import MessagesState

class MyState(MessagesState):
    """MessagesState를 상속받으면 messages 필드와 add_messages 리듀서가 자동 포함"""
    documents: list[str]  # 추가 필드 정의 가능


def max_reducer(existing: int, new: int) -> int:
    return max(existing or 0, new or 0)

class MaxState(TypedDict):
    highest_score: Annotated[int, max_reducer]
    current_score: int

def update_score(state:MaxState) -> MaxState:
    new_score = 85
    return {
        "highest_score": new_score,
        "current_score": new_score
    }

def merge_dict_reducer(existing: dict, new: dict) -> dict:
    if not existing:
        return new or {}
    if not new:
        return existing
    
    result = existing.copy()
    for key, value in new.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = merge_dict_reducer(result[key], value)
        else:
            result[key] = value
    return result

class ConfigState(TypedDict):
    settings: Annotated[dict, merge_dict_reducer]

def update_ui_settings(state: ConfigState) -> ConfigState:
    return {
        "settings": {
            "ui": {"theme": "dark"}
        }
    }
def update_performance_settings(state: ConfigState) -> ConfigState:
    """성능 설정만 업데이트"""
    return {
        "settings": {
            "performance": {"cache_size": 1000}  # performance.cache_size만 변경
        }
    }

def update_by_id_reducer(existing: list[dict], new: list[dict]) -> list[dict]:
    if not existing:
        existing = []
    if not new:
        return existing
    
    existing_dict = {item.get("id"): item for item in existing}

    for item in new:
        item_id = item.get("id")
        if item_id:
            existing_dict[item_id] = item
    return list(existing_dict.values)

class EntityState(TypedDict):
    users: Annotated[list[dict], update_by_id_reducer]

def update_user(state: EntityState) -> EntityState:
    return {
        "users": [
            {"id": "user1", "name": "김철수", "age": 31},  # user1 업데이트
            {"id": "user3", "name": "박영수", "age": 28}   # user3 추가
        ]
    }
