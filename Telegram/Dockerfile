FROM python:3.11-slim

RUN pip install uv

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN uv sync

WORKDIR /app

COPY . .

CMD ["./.venv/bin/python", "main.py"]