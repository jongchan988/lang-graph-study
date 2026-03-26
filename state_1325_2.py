from typing import TypedDict
from langgraph.graph import StateGraph, START, END

# 입력 스키마
class InputState(TypedDict):
    question: str

# 출력 스키마
class OutputState(TypedDict):
    answer: str

# 내부 전체 상태 (입출력 + 비공개)
class OverallState(TypedDict):
    question: str           # 입력에서 옴
    answer: str             # 출력으로 나감
    intermediate_data: str  # 내부용
    processing_steps: list  # 내부용

def analyze_node(state: InputState) -> dict:
    """입력을 분석하고 중간 데이터 생성"""
    return {
        "intermediate_data": f"분석됨: {state['question']}",
        "processing_steps": ["analyze"]
    }

def process_node(state: OverallState) -> dict:
    """중간 데이터를 처리"""
    steps = state["processing_steps"] + ["process"]
    return {
        "intermediate_data": state["intermediate_data"] + " -> 처리됨",
        "processing_steps": steps
    }

def answer_node(state: OverallState) -> OutputState:
    """최종 답변 생성"""
    return {
        "answer": f"답변: {state['intermediate_data']} (단계: {len(state['processing_steps'])})"
    }

# 입출력 스키마를 명시적으로 지정
builder = StateGraph(
    OverallState,
    input=InputState,
    output=OutputState
)

builder.add_node("analyze", analyze_node)
builder.add_node("process", process_node)
builder.add_node("answer", answer_node)

builder.add_edge(START, "analyze")
builder.add_edge("analyze", "process")
builder.add_edge("process", "answer")
builder.add_edge("answer", END)

graph = builder.compile()

# 실행 - InputState로 입력
result = graph.invoke({"question": "LangGraph란?"})
print(result)
# {'answer': '답변: 분석됨: LangGraph란? -> 처리됨 (단계: 2)'}

# 출력에는 OutputState의 필드만 포함됨
# intermediate_data, processing_steps는 노출되지 않음
