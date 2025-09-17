FROM python:3.11-slim

RUN pip install uv

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN uv sync --no-cache

COPY ./Telegram_bot/ .

EXPOSE 8000

CMD ["uv run", "main.py"]