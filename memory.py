from langgraph.checkpoint.memory import InMemorySaver

memory = InMemorySaver()

config = {
    "configurable": {
        "thread_id": "user_1"
    }
}