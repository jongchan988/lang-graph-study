# Sample1
# messages = [
#     {"role": "user", "content": "안녕하세요"},
#     {"role": "assistant", "content": "안녕하세요! 무엇을 도와드릴까요?"},
#     {"role": "user", "content": "날씨가 어때요?"},
# ]

# Sample2
# from operator import add
# from typing import Annotated
# from typing_extensions import TypedDict

# class SimpleState(TypedDict):
#     messages: Annotated[list, add]

# state = {
#     "messages": [
#         {
#             "id": "msg1",
#             "content": "안녕하세요"
#         }
#     ]
# }

# update = {
#     "messages": [
#         {
#             "id": "msg1",
#             "content": "안녕하세요! (수정됨)"
#         }
#     ]
# }

# from langgraph.graph.message import add_messages
# from typing import Annotated
# from typing_extensions import TypedDict

# class ChatState(TypedDict):
#     messages: Annotated[list, add_messages]

# # 동일한 상황에서 add_messages 사용
# # 기존 상태
# state = {
#     "messages": [
#         {
#             "id": "msg1",
#             "content": "안녕하세요"
#         }
#     ]
# }

# update = {
#     "messages": [
#         {
#             "id": "msg1",
#             "content": "안녕하세요! (수정됨)"
#         }
#     ]
# }

# from langgraph.graph import StateGraph, MessagesState, START, END
# from langchain_core.messages import HumanMessage, AIMessage

# from typing import Optional

# class MyState(MessagesState):
#     pass # messages 필드가 자동으로 포함 

# class ChatbotState(MessagesState):
#     user_name: str
#     language: str
#     context: Optional[list[str]]
#     turn_count: int

# class ChatState(MessagesState):
#     user_name: str

# def greet_user(state:ChatState) -> dict:
#     user_msg = state["messages"][-1]
#     response = AIMessage(
#         content=f"안녕하세요, {state['user_name']}님! 무엇을 도와드릴까요?"
#     )
#     return {"messages": [response]}

# def process_question(state: ChatState) -> dict:
#     user_msg = state["messages"][-1]
#     response = AIMessage (
#         content=f"'{user_msg.content}'에 대한 답변입니다."
#     )
#     return {"messages": [response]}

# graph = StateGraph(ChatState)
# graph.add_node("greet", greet_user)
# graph.add_node("answer", process_question)

# graph.add_edge(START, "greet")
# graph.add_edge("greet", "answer")
# graph.add_edge("answer", END)

# app = graph.compile()

# result = app.invoke({
#     "messages": [HumanMessage(content="안녕하세요")],
#     "user_name": "홍길동"
# })

# print(f"메시지 수 {len(result['messages'])}")
# for msg in result["messages"]:
#     role = "User" if isinstance(msg, HumanMessage) else "AI"
#     print(f"{role}: {msg.content}")

from langchain_core.messages import HumanMessage, AIMessage
from langgraph.graph import StateGraph, MessagesState, START, END, RemoveMessage

msg_with_id = HumanMessage(
    content="안녕하세요",
    id = "user_msg_001"
)

msg_auto_id = HumanMessage(content="안녕하세요")
print(msg_auto_id.id)
class ChatState(MessagesState):
    user_name: str
def edit_message_node(state: ChatState) -> dict:
    """특정 메시지를 수정하는 노드"""
    last_ai_msg = state["messges"][-1]

    edited_msg = AIMessage(
        content=last_ai_msg.content + "(검토 완료)",
        id=last_ai_msg.id
    )
    return {"messages": [edited_msg]}

def cleanup_messages(state: ChatState)-> dict:
    messages_to_remove = state["messages"][2:]
    return{
        "messages": [
            RemoveMessage(id=msg.id)
            for msg in messages_to_remove
        ]
    }

from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

def get_recent_exchanges(state: ChatState, n: int = 3) -> list:
    """최근 n개의 사용자-AI 대화쌍 추출"""
    messages = state["messages"]

    # 시스템 메시지 제외
    exchanges = [
        msg for msg in messages 
        if not isinstance(msg, SystemMessage)
    ]

    # 최근 n개 쌍 (2*n개 메시지)
    return exchanges[-(n*2):]

from langchain_core.messages import SystemMessage

class SummarizableState(MessagesState):
    summary: str  # 이전 대화 요약

def maybe_summarize(state: SummarizableState) -> dict:
    """메시지가 많아지면 요약"""
    if len(state["messages"]) <= 10:
        return {}  # 변경 없음

    # 처음 8개 메시지를 요약 (실제로는 LLM 호출)
    old_messages = state["messages"][:8]
    summary_text = "이전 대화 요약: ..."

    # 요약을 저장하고 오래된 메시지 삭제
    return {
        "summary": summary_text,
        "messages": [
            RemoveMessage(id=msg.id) 
            for msg in old_messages
        ]
    }