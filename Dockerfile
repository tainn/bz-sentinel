FROM python:3.12.3-alpine3.19

ENV PYTHONPATH="/src:$PYTHONPATH"
ENV PYTHONUNBUFFERED=1
ENV CRUNTIME=1

COPY src /src
COPY pyproject.toml /

RUN apk add git
RUN python3 -m pip install .

ENTRYPOINT ["python3"]
