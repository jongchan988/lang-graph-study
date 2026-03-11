from typing import Annotated
from typing_extensions import TypedDict
from operator import add
from langgraph.graph import StateGraph, START, END

def keep_last_n(existing: list, new: list, n: int = 5) -> list:
    """최근 n개 항목만 유지하는 리듀서"""
    combined = (existing or []) + (new or [])
    return combined[-n:]  # 마지막 n개만 반환
 
def keep_max(existing: float, new: float) -> float:
    return max (existing, new)

# 부분 함수로 리듀서 생성
from functools import partial
keep_last_5 = partial(keep_last_n, n=5)

class AdvancedState(TypedDict):
    total_tokens: Annotated[int, add]           # 토큰 수 누적
    max_score: Annotated[float, keep_max]            # 최고 점수 유지
    recent_actions: Annotated[list, keep_last_5] # 최근 5개 액션만 유지
    current_status: str                          # 현재 상태 (덮어쓰기)

def process_input(state: AdvancedState) -> AdvancedState:
    """사용자 입력 처리"""
    return {
        "total_tokens": 150,  # 150 토큰 추가
        "max_score": 0.85,    # 점수 0.85
        "recent_actions": ["input_received"],
        "current_status": "processing"
    }

def analyze_content(state: AdvancedState) -> AdvancedState:
    """콘텐츠 분석"""
    return {
        "total_tokens": 200,  # 200 토큰 추가
        "max_score": 0.92,    # 더 높은 점수
        "recent_actions": ["analysis_started", "analysis_completed"],
        "current_status": "analyzed"
    }

def generate_response(state: AdvancedState) -> AdvancedState:
    """응답 생성"""
    return {
        "total_tokens": 300,  # 300 토큰 추가
        "max_score": 0.88,    # 낮은 점수 (무시됨)
        "recent_actions": ["response_generated"],
        "current_status": "completed"
    }

# 그래프 구성 및 실행
graph = StateGraph(AdvancedState)
graph.add_node("process", process_input)
graph.add_node("analyze", analyze_content)
graph.add_node("generate", generate_response)

graph.add_edge(START, "process")
graph.add_edge("process", "analyze")
graph.add_edge("analyze", "generate")
graph.add_edge("generate", END)

compiled_graph = graph.compile()

result = compiled_graph.invoke({
    "total_tokens": 0,
    "max_score": 0.0,
    "recent_actions": [],
    "current_status": "idle"
})

print("=== 최종 상태 ===")
print(f"총 토큰 수: {result['total_tokens']}")  # 650 (150+200+300)
print(f"최고 점수: {result['max_score']}")      # 0.92 (최대값)
print(f"최근 액션: {result['recent_actions']}")  # 최근 5개
print(f"현재 상태: {result['current_status']}")  # "completed"