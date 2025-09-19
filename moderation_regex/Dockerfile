FROM python:3.11-slim

RUN pip install uv

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN uv sync --no-cache --frozen

COPY ./moderation_regex/ .

EXPOSE 8002

CMD ["uv", "run", "moder_api.py"]