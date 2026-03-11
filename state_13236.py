from typing import Annotated
from operator import add
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END


class State(TypedDict):
    message_count: int
    conversation: Annotated[list[str], add]

def node_1(state: State) -> State:
    print(f"Node 1 - 현재 대화: {state.get('conversation', [])}")
    return {
        "message_count": 1,
        "conversation": ["안녕하세요!"]
    }

def node_2(state: State) -> State:
    print(f"Node 2 - 현재 대화: {state['conversation']}")
    return {
        "conversation": ["어떻게 도와드릴까요?"]
    }

graph = StateGraph(State)
graph.add_node("node_1", node_1)
graph.add_node("node_2", node_2)

graph.add_edge(START, "node_1")
graph.add_edge("node_1", "node_2")
graph.add_edge("node_2", END)

compiled_graph = graph.compile()

inital_state = {"message_count": 0, "conversation":[]}
result = compiled_graph.invoke(inital_state)

print("\n=== 최종 결과 ===")
print(f"메시지 수: {result['message_count']}")
print(f"대화 내용: {result['conversation']}")