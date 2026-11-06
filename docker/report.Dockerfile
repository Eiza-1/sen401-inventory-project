# Report service: console client that fetches the stock report from the API
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN pip install --no-cache-dir "pydantic>=2.7"

COPY inventory_app ./inventory_app
COPY app.py .

CMD ["python", "app.py"]
