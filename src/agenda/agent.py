import os
from typing import Optional
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage, SystemMessage
from .excel_store import AgendaStore
from .tools import build_tools


def build_agent(store: Optional[AgendaStore] = None, llm: Optional[object] = None):
    store = store or AgendaStore()
    tools = build_tools(store)
    if llm is None:
        llm = ChatOpenAI(model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"))
    agent = create_agent(model=llm, tools=tools)
    return agent


def invoke_text(agent, text: str):
    sysmsg = SystemMessage(
        content="Eres un asistente de IA para gestionar una agenda. Usa herramientas para agregar, consultar y eliminar eventos. Responde en español y valida formatos de fecha y hora."
    )
    return agent.invoke({"messages": [sysmsg, HumanMessage(content=text)]})
