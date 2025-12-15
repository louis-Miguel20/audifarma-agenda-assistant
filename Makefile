PY?=py -3
STREAMLIT?=streamlit

.PHONY: setup run test lint docker-build docker-run

setup:
	$(PY) -m pip install --user -r requirements.txt

run:
	$(STREAMLIT) run src/app.py

test:
	$(PY) -m pytest -q

lint:
	ruff check .

docker-build:
	docker build -t agenda-assistant:latest .

docker-run:
	docker run --rm -p 8501:8501 --env OPENAI_API_KEY --env OPENAI_MODEL agenda-assistant:latest
