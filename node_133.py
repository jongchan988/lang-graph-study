from langgraph.graph import StateGraph, START, END
from typing_extensions import TypedDict

class State(TypedDict):
    counter: int

def increment(state:State) -> dict:
    return {"counter": state["counter"] + 1}

graph = StateGraph(State)
graph.add_node("increment", increment)
graph.add_edge(START, "increment")
graph.add_edge("increment", END)

app = graph.compile()
result = app.invoke({"counter":0})
print(result)

def simple_node(state:State) -> dict:
    return {"key":"value"}

from langchain_core.runnables import RunnableConfig
def node_with_config(state: State, config: RunnableConfig) -> dict:
    thread_id = config.get("configurable", {}).get("thread_id")
    print(f"Thread ID: {thread_id}")
    return {"processed": True}

from langgraph.types import Runtime, BaseStore, StreamWriter

def node_with_runtime(
        state: State,
        config: RunnableConfig,
        *,
        store: BaseStore,
        stream_writer: StreamWriter
) -> dict:
    stream_writer({"progress": "50%"})
    return {"status": "done"}

def some_computation(data):
    pass

def sync_node(state: State) -> dict:
    result = some_computation(state["data"])
    return {"result": result}

async def async_api_call(query:str):
    pass

async def async_node(state:State) -> dict:
    result = await async_api_call(state["query"])
    return {"response": result}

result = await app.ainvoke({"query": "검색어"})


def my_node(state:State)->dict:
    return {"key": "value"}

graph.add_node("my_node", my_node)
graph.add_node(my_node)


from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4")
graph.add_node("llm", llm)

from langgraph.graph import START

graph.add_edge(START, "first_node")

from langgraph.graph import END

graph.add_edge("last_node", END)

from langgraph.cache import InMemoryCache, CachePolicy

# 캐시 정책 정의
policy = CachePolicy(
    ttl=300,  # 5분간 캐시 유지
    key_func=lambda state: hash(state["query"])  # 캐시 키 생성 함수
)

# 노드에 캐시 정책 적용
graph.add_node("expensive_node", expensive_function, cache_policy=policy)

# 캐시와 함께 컴파일
app = graph.compile(cache=InMemoryCache())
