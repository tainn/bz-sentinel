FROM fedora:36 AS builder
RUN dnf install python3-pip -y
RUN dnf install git -y
WORKDIR /app
ENV PYTHONPATH="/app:$PYTHONPATH"

FROM builder
COPY src /app
COPY requirements.txt /app
RUN pip3 install -r requirements.txt
ENTRYPOINT ["python3", "-u"]
