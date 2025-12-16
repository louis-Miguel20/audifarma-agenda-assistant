from agenda.excel_store import AgendaStore


def test_store_create_and_basic_ops(tmp_path):
    path = tmp_path / "agenda.xlsx"
    store = AgendaStore(path=str(path))
    store.add_event("Reunión", "2025-12-20", "09:30")
    rows = store.query_by_date("2025-12-20")
    assert len(rows) == 1
    assert rows[0]["Evento"] == "Reunión"
    deleted = store.delete_event("Reunión", "2025-12-20", "09:30")
    assert deleted == 1
    assert store.query_by_date("2025-12-20") == []

