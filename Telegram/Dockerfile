FROM python:3.12.6 as builder

RUN pip install uv

WORKDIR /app

COPY pyproject.toml uv.lock ./

# Установка зависимостей с помощью uv
RUN uv sync --lock-file uv.lock

FROM python:3.12.6

WORKDIR /app

COPY . .

CMD ["python", "main.py"]