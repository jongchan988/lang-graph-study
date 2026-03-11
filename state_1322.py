from typing_extensions import TypedDict, NotRequired
from typing import Annotated
from operator import add
from dataclasses import dataclass, field
from pydantic import BaseModel, Field
class Mystate(TypedDict):
    query: str
    results: Annotated[list[str], add]
    count: NotRequired[int]

class AgentSate(TypedDict):
    messages: list
    query: str
    context: NotRequired[str]
    metadata: NotRequired[dict]

@dataclass
class MyState:
    query: str = ""
    results: Annotated[list[str], add] = field(default_factory=list)
    count: int = 0

class MyState(BaseModel):
    query: str = ""
    results: Annotated[list[str], add] = Field(default_factory=list)
    count: int = Field(default=0, ge=0)

class BasicState(TypedDict):
    user_input: str
    ai_response: str
    conversation_history: Annotated[list[str], add]

def chatbot_node(state: BasicState) -> dict:
    response = f"{state['user_input']}' 에 대한 응답입니다."
    return {
        "ai_response": response,
        "conversation_history": [f"User: {state['user_input']}", f"AI: {response}"]
    }

class InputState(TypedDict):
    question: str

class OutputState(TypedDict):
    answer: str

class OverallState(InputState, OutputState):
    intermediate_data: str
    search_results: list[str]

def search_node (state: InputState) -> dict:
    return {
        "search_results": ["결과1", "결과2"],
        "intermediate_data": f"'{state['question']}' 검색 완료"
    }

def answer_node(state: OverallState) -> OutputState:
    return {"answer": f"검색 결과: {state['search_results'][0]}"}