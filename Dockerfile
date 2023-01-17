FROM fedora:36 AS builder
WORKDIR /app
COPY requirements.txt /app
RUN dnf install python3-pip -y
RUN dnf install git -y
RUN pip3 install -r requirements.txt

FROM builder
COPY src /app
ENTRYPOINT ["python3", "-u"]
