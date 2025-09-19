FROM python:3.10-slim

RUN pip install uv

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN uv sync --group moder-nlp --no-cache --frozen

COPY ./moderation_nlp/ .

EXPOSE 8001

CMD ["uv", "run", "moder_nlp_api.py"]