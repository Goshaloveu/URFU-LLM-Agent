FROM python:3.10-slim

RUN pip install uv

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN uv sync --no-cache

COPY ./moderation_nlp/ .

EXPOSE 8001

CMD ["gunicorn", "moder_nlp_api:app", "--workers", "1", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8001"]