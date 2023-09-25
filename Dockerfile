FROM python:3.11.5-alpine3.18

ENV PYTHONPATH="/src:$PYTHONPATH"
ENV PYTHONUNBUFFERED=1
ENV CRUNTIME=1

RUN apk add git

COPY src /src
COPY requirements.txt /
RUN python3 -m pip install -r requirements.txt
ENTRYPOINT ["python3"]
