# Migration service: one-shot job that copies data/inventory.json into SQLite
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN pip install --no-cache-dir "pydantic>=2.7"

COPY inventory_app ./inventory_app
COPY data/inventory.json ./data/inventory.json

CMD ["python", "-m", "inventory_app.migrate"]
