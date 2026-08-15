from config import MODEL
from langchain.agents import create_agent
from langchain_ollama import ChatOllama
from prompts import PRIMARY_PROMPT
from tools.bash import execute_bash,start_process
from tools.hyprland import fullscreen, getAllWindows,switch_workspace
from memory import memory

llm = ChatOllama(
    model=MODEL,
    temperature=0,
    
)

agent = create_agent(
    model=llm,
    tools=[
        execute_bash,
        getAllWindows,
        fullscreen,
        start_process,
        switch_workspace,
    ],
    system_prompt=PRIMARY_PROMPT,
    checkpointer=memory
)


