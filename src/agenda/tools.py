from typing import Optional, List
from langchain_core.tools import StructuredTool
from .excel_store import AgendaStore


def build_tools(store: AgendaStore):
    # Crea herramientas estructuradas para operar sobre la agenda:
    # - agregar_evento: añade una fila
    # - eliminar_evento: elimina según filtros
    # - consultar_por_fecha: devuelve lista de dicts
    # - listar_todos: todos los eventos
    def agregar_evento(evento: str, fecha: str, hora: str) -> str:
        # Agrega un evento con fecha y hora al almacén
        store.add_event(evento=evento, fecha=fecha, hora=hora)
        return "Evento agregado"

    def eliminar_evento(evento: str, fecha: Optional[str] = None, hora: Optional[str] = None) -> str:
        # Elimina eventos por nombre y filtros opcionales de fecha/hora
        removed = store.delete_event(evento=evento, fecha=fecha, hora=hora)
        if removed == 0:
            return "No se encontró el evento"
        return f"Evento(s) eliminado(s): {removed}"

    def consultar_por_fecha(fecha: str) -> List[dict]:
        # Consulta eventos que coinciden con una fecha YYYY-MM-DD
        return store.query_by_date(fecha=fecha)

    def listar_todos() -> List[dict]:
        # Lista todos los eventos de la agenda
        return store.all_events()

    return [
        StructuredTool.from_function(agregar_evento, name="agregar_evento", description="Agregar evento con fecha y hora"),
        StructuredTool.from_function(eliminar_evento, name="eliminar_evento", description="Eliminar evento por nombre y opcionalmente fecha/hora"),
        StructuredTool.from_function(consultar_por_fecha, name="consultar_por_fecha", description="Consultar eventos por fecha YYYY-MM-DD"),
        StructuredTool.from_function(listar_todos, name="listar_todos", description="Listar todos los eventos"),
    ]
