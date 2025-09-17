FROM python:3.11-slim

RUN pip install uv

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN uv sync --no-cache

COPY ./Telegram_bot/ .

CMD ["./.venv/bin/python", "main.py"]