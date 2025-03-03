FROM ghcr.io/astral-sh/uv:0.4.24-python3.12-alpine
RUN apk add build-base git
ENV PYTHONPATH=/app:$PYTHONPATH PYTHONUNBUFFERED=1
WORKDIR /app
COPY pyproject.toml /app/pyproject.toml
COPY src /app/src
RUN uv venv && uv pip install -r pyproject.toml
