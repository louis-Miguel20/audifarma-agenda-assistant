from agenda.excel_store import AgendaStore
from agenda.tools import build_tools
from agenda.agent import build_agent
from langchain_openai import ChatOpenAI


def test_agent_tools_add_and_query(tmp_path):
    store = AgendaStore(path=str(tmp_path / "agenda.xlsx"))
    tools = build_tools(store)
    for t in tools:
        if t.name == "agregar_evento":
            t.invoke({"evento": "Almuerzo", "fecha": "2025-12-21", "hora": "13:00"})
            break
    llm = ChatOpenAI(model="gpt-5-nano", api_key="sk-test")
    agent = build_agent(store=store, llm=llm)
    rows = store.query_by_date("2025-12-21")
    assert len(rows) == 1
    assert rows[0]["Hora"] == "13:00"
