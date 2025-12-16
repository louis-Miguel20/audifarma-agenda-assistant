import os
import streamlit as st
from dotenv import load_dotenv
from agenda.agent import build_agent, invoke_text
from agenda.excel_store import AgendaStore


load_dotenv()
st.set_page_config(page_title="Asistente de Agenda", page_icon="🗓️", layout="wide")

def aplicar_tema():
    # Aplica estilos visuales personalizados a la interfaz (CSS embebido)
    st.markdown(
        """
        <style>
        .main {background: linear-gradient(135deg, #f6f9fc 0%, #ffffff 100%);}
        .stChatMessage .stMarkdown {font-size: 1.05rem;}
        .agenda-header {background: #004aad; color: white; padding: 14px 18px; border-radius: 8px; margin-bottom: 16px;}
        .pill {display: inline-block; background: #eaf2ff; color: #004aad; padding: 6px 10px; border-radius: 999px; margin-right: 8px; font-weight: 600;}
        .danger {background: #ffefef; color: #b00020;}
        .ok {background: #eaffea; color: #1b5e20;}
        </style>
        """,
        unsafe_allow_html=True,
    )

aplicar_tema()
# Encabezado visual de la aplicación
st.markdown('<div class="agenda-header">🗓️ Asistente de IA: Agenda</div>', unsafe_allow_html=True)

HAS_KEY = bool(os.getenv("OPENAI_API_KEY"))

if "messages" not in st.session_state:
    # Historial de conversación: lista de tuplas (role, content)
    st.session_state.messages = []
if "store" not in st.session_state:
    # Instancia de almacén de agenda
    st.session_state.store = AgendaStore()
if "agent" not in st.session_state:
    # Construcción condicional del agente (requiere OPENAI_API_KEY)
    st.session_state.agent = build_agent(st.session_state.store) if HAS_KEY else None
if "thread_id" not in st.session_state:
    # Identificador de hilo de memoria (LangGraph checkpointer)
    st.session_state.thread_id = "session-" + str(id(st.session_state))

with st.sidebar:
    st.header("Estado")
    # Mostrar ruta del archivo Excel y tabla de eventos
    st.write(f"Archivo: {st.session_state.store.path}")
    events = st.session_state.store.all_events()
    if events:
        st.subheader("Eventos")
        st.dataframe(events, use_container_width=True)
    else:
        st.caption("Sin eventos")
    if not HAS_KEY:
        st.markdown('<span class="pill danger">Configura OPENAI_API_KEY</span>', unsafe_allow_html=True)
    else:
        st.markdown(f'<span class="pill">Modelo: {os.getenv("OPENAI_MODEL","gpt-5-nano")}</span>', unsafe_allow_html=True)
    # Botón para reiniciar conversación y memoria
    if st.button("🧹 Reiniciar conversación"):
        st.session_state.messages = []
        st.session_state.thread_id = "session-" + str(id(st.session_state))
        st.success("Conversación reiniciada")

# Reimprimir historial en el chat
for role, content in st.session_state.messages:
    with st.chat_message(role):
        st.markdown(content)

# Entrada del usuario (deshabilitada si falta la API key)
prompt = st.chat_input("Escribe qué quieres hacer", disabled=not HAS_KEY)
if prompt:
    # Añadir mensaje al historial y pintar en el chat
    st.session_state.messages.append(("user", prompt))
    with st.chat_message("user"):
        st.markdown(prompt)
    try:
        # Invocar el agente con historial y thread_id para memoria
        result = invoke_text(st.session_state.agent, prompt, st.session_state.messages, st.session_state.thread_id)
        msgs = result.get("messages", [])
        output = msgs[-1].content if msgs else ""
    except Exception as e:
        # Mostrar errores en el chat del asistente
        output = f"Error: {e}"
    st.session_state.messages.append(("assistant", output))
    with st.chat_message("assistant"):
        st.markdown(output)
