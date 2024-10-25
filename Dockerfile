FROM ghcr.io/astral-sh/uv:0.4.24-python3.12-alpine

RUN apk add build-base
RUN apk add git

ENV PYTHONPATH=/app:$PYTHONPATH
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY pyproject.toml /app/pyproject.toml
COPY src /app/src

RUN uv venv
RUN uv pip install -r pyproject.toml
