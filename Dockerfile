FROM python:3.12.4-alpine3.20

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app:$PYTHONPATH

WORKDIR /app

RUN apk add git

COPY src /app/src
COPY pyproject.toml /app
RUN python3 -m pip install .
