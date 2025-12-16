# Asistente de IA: Agenda con LangChain y Streamlit

## Arquitectura
- `src/agenda/excel_store.py`: Persistencia en `agenda.xlsx` con columnas `Evento`, `Fecha`, `Hora`.
- `src/agenda/tools.py`: Herramientas LangChain para agregar, consultar, eliminar y listar eventos.
- `src/agenda/agent.py`: Agente con `create_agent` y memoria con LangGraph `MemorySaver`.
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
  - `OPENAI_MODEL` opcional (`gpt-5-nano` por defecto)

## Ejecución
1. Crear entorno y dependencias:
   - `make setup` o `pip install --user -r requirements.txt`
2. Ejecutar la app:
   - `make run` o `streamlit run src/app.py`
   - Abrir `http://localhost:8501`
3. Pruebas:
   - `make test` o `pytest tests/`

## Memoria de conversación
- La memoria se gestiona con LangGraph y `MemorySaver` por hilo de conversación.
- La UI establece un `thread_id` de sesión; puedes reiniciarlo desde el botón “Reiniciar conversación”.
- Requiere `OPENAI_API_KEY` para uso del agente; sin clave, la UI muestra solo el estado.

## Capacidades del programa
- Agregar eventos con fecha (`YYYY-MM-DD`) y hora (`HH:MM` 24h).
- Consultar eventos por fecha especificando `YYYY-MM-DD`.
- Eliminar eventos por nombre y opcionalmente por fecha y hora.
- Listar todos los eventos almacenados en la agenda.
- Memoria conversacional por sesión, con contexto de mensajes previos.
- Manejo resiliente del archivo Excel: si se detecta corrupción, se regenera automáticamente.
- Interfaz moderna en Streamlit con tema personalizado, chips de estado y acciones rápidas.
- Configuración por variables de entorno (`OPENAI_API_KEY`, `OPENAI_MODEL`).
- Pruebas unitarias para el almacén y las herramientas.
- Docker y Makefile para facilitar ejecución y despliegue.
- CI/CD con GitHub Actions (lint y tests).

## Ejemplos de uso (prompts)
- “Agrega ‘Reunión equipo’ el 2025-12-21 a las 09:30”
- “¿Qué eventos hay el 2025-12-21?”
- “Elimina ‘Reunión equipo’ del 2025-12-21 a las 09:30”
- “Lista todos los eventos”

## Personalización del modelo
- Por defecto se usa `gpt-5-nano`. Para cambiarlo:
  - Exporta en la sesión: `$env:OPENAI_MODEL="gpt-5-nano"`
  - O define en `.env`: `OPENAI_MODEL=gpt-5-nano`

## Persistencia de memoria avanzada (opcional)
- Si deseas memoria persistente entre reinicios, puedes cambiar `MemorySaver` por `SqliteSaver("data/checkpoints.sqlite")` en `src/agenda/agent.py`, manteniendo el `thread_id` por conversación.

## Docker
- Construir imagen:
  - `docker build -t agenda-assistant:latest .`
- Ejecutar contenedor:
  - `docker run --rm -p 8503:8501 -e OPENAI_API_KEY=sk-... -e OPENAI_MODEL=gpt-5-nano agenda-assistant:latest`
  - Abrir `http://localhost:8503`
  - Nota: si no defines `OPENAI_API_KEY`, la UI cargará pero el agente quedará deshabilitado.

## Notas de calidad
- Código modular, sin rutas ni claves hardcodeadas.
- Manejo de errores básico en UI.
- Se incluye CI con pruebas y lint.
