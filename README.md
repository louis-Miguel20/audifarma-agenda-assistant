# Asistente de IA: Agenda con LangChain y Streamlit

## Arquitectura
- `src/agenda/excel_store.py`: Persistencia en `agenda.xlsx` con columnas `Evento`, `Fecha`, `Hora`.
- `src/agenda/tools.py`: Herramientas LangChain para agregar, consultar, eliminar y listar eventos.
- `src/agenda/agent.py`: Agente con `create_tool_calling_agent` que decide qué herramienta usar según lenguaje natural.
- `src/app.py`: Interfaz en Streamlit con historial de chat y tabla lateral de eventos.
- `data/`: Se crea automáticamente el archivo `agenda.xlsx` la primera vez que se ejecuta.

## Flujo de datos
- El usuario escribe una instrucción en la UI.
- El agente interpreta la intención y ejecuta la herramienta correspondiente.
- Las herramientas interactúan con `AgendaStore` que lee/escribe sobre `agenda.xlsx`.
- La respuesta se muestra en el chat y se actualiza la tabla de eventos.

## Requisitos
- Python 3.12
- Variables de entorno:
  - `OPENAI_API_KEY` obligatoria para el LLM
  - `OPENAI_MODEL` opcional (`gpt-4o-mini` por defecto)

## Ejecución
1. Crear entorno y dependencias:
   - `make setup`
2. Ejecutar la app:
   - `make run`
   - Abrir `http://localhost:8501`
3. Pruebas:
   - `make test`

## Docker
- Construir imagen: `make docker-build`
- Ejecutar contenedor: `make docker-run`

## Notas de calidad
- Código modular, sin rutas ni claves hardcodeadas.
- Manejo de errores básico en UI.
- Se incluye CI con pruebas y lint.

