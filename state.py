from typing import TypedDict, Annotated, List
from langgraph.graph.message import add_messages
from operator import add
from langgraph.graph import StateGraph, START, END

class MyState(TypedDict):
    counter: int
    user_name: str

class ChatState(TypedDict):
    user_message: str
    chat_history: list
    user_context: dict
    system_status: str
    messages: Annotated[list, add_messages]
    user_name: str

class BasicState(TypedDict):
    current_step:str
    user_id: str

# def conversation_node(state: ChatState):
#     context = "\n".join(state["chat_history"][-3:])
#     response = generate_contextual_response(state["user_message"], context)
#     return {"ai_response": response}

def get_fix_current_state():
    return {"current_step": "시작", "user_id": "user123"}

def get_update_1(state):
    print("처리중")
    return {"current_step": "처리중"}

def get_update_2(state):
    print("완료")
    return {"current_step": "완료"}
graph = StateGraph(BasicState)
# 초기 상태
# state = {"current_step": "시작", "user_id": "user123"}

graph.add_node("update_1", get_update_1)
graph.add_node("update_2", get_update_2)

graph.add_edge(START, "update_1")
graph.add_edge("update_1", "update_2")
graph.add_edge("update_2", END)


app = graph.compile()
result = app.invoke(get_fix_current_state())

print(f"최종 결과: {result}")
# 노드 1 실행
# update1 = {"current_step": "처리중"}
# 결과: {"current_step": "처리중", "user_id": "user123"}

# 노드 2 실행  
# update2 = {"current_step": "완료"}
# 결과: {"current_step": "완료", "user_id": "user123"}


