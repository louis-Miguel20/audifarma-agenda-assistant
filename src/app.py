import os
import streamlit as st
from dotenv import load_dotenv
from agenda.agent import build_agent, invoke_text
from agenda.excel_store import AgendaStore


load_dotenv()
st.set_page_config(page_title="Asistente de Agenda", page_icon="🗓️", layout="centered")
st.title("Asistente de IA: Agenda")

if "messages" not in st.session_state:
    st.session_state.messages = []
if "store" not in st.session_state:
    st.session_state.store = AgendaStore()
if "agent" not in st.session_state:
    st.session_state.agent = build_agent(st.session_state.store)

with st.sidebar:
    st.header("Estado")
    st.write(f"Archivo: {st.session_state.store.path}")
    events = st.session_state.store.all_events()
    if events:
        st.subheader("Eventos")
        st.dataframe(events, use_container_width=True)
    else:
        st.caption("Sin eventos")

for role, content in st.session_state.messages:
    with st.chat_message(role):
        st.markdown(content)

prompt = st.chat_input("Escribe qué quieres hacer")
if prompt:
    st.session_state.messages.append(("user", prompt))
    with st.chat_message("user"):
        st.markdown(prompt)
    try:
        result = invoke_text(st.session_state.agent, prompt)
        msgs = result.get("messages", [])
        output = msgs[-1].content if msgs else ""
    except Exception as e:
        output = f"Error: {e}"
    st.session_state.messages.append(("assistant", output))
    with st.chat_message("assistant"):
        st.markdown(output)
