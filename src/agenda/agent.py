# Módulo del agente de IA para la agenda
# - Configura el modelo de lenguaje (OpenAI)
# - Registra herramientas de la agenda (agregar, eliminar, consultar, listar)
# - Añade memoria de conversación con LangGraph (checkpointer)
# - Provee una función de invocación con historial y thread_id
import os
from typing import Optional
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langgraph.checkpoint.memory import MemorySaver
from .excel_store import AgendaStore
from .tools import build_tools


def build_agent(store: Optional[AgendaStore] = None, llm: Optional[object] = None):
    # Construye el agente de IA con herramientas y memoria
    # - `store`: instancia de AgendaStore para operaciones sobre Excel
    # - `llm`: modelo de lenguaje (si no se pasa, se lee de OPENAI_MODEL)
    store = store or AgendaStore()
    # Construcción de herramientas de agenda
    tools = build_tools(store)
    if llm is None:
        # Modelo por defecto configurable vía OPENAI_MODEL (gpt-5-nano)
        llm = ChatOpenAI(model=os.getenv("OPENAI_MODEL", "gpt-5-nano"))
    # Crear agente con soporte de tool calling
    agent = create_agent(model=llm, tools=tools)
    # Añadir memoria de conversación con checkpointer (persistencia en RAM)
    checkpointer = MemorySaver()
    agent = agent.with_config({"checkpointer": checkpointer})
    return agent


def invoke_text(agent, text: str, history: Optional[list] = None, thread_id: Optional[str] = None):
    # Invoca el agente con historial y soporte de memoria por hilo
    # - `history`: lista de tuplas ("user"|"assistant", contenido) para contexto
    # - `thread_id`: identificador único de conversación (persistencia del estado)
    sysmsg = SystemMessage(content="Eres un asistente de IA para gestionar una agenda. Usa herramientas para agregar, consultar y eliminar eventos. Responde en español y valida formatos de fecha y hora.")
    msgs = [sysmsg]
    if history:
        # Convertimos el historial de la UI en mensajes del agente
        for role, content in history:
            if role == "user":
                msgs.append(HumanMessage(content=content))
            else:
                msgs.append(AIMessage(content=content))
    # Prompt actual del usuario
    msgs.append(HumanMessage(content=text))
    # Configuración del hilo para el checkpointer
    config = {"configurable": {"thread_id": thread_id or "default"}}
    return agent.invoke({"messages": msgs}, config=config)
