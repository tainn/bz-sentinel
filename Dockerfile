FROM fedora:38 as builder
ENV PYTHONPATH="/src:$PYTHONPATH"
ENV CONTAINERIZED=1
RUN dnf install -y python3-pip
RUN dnf install -y git

FROM builder
COPY src /src
COPY requirements.txt /
RUN python3 -m pip install -r requirements.txt
ENTRYPOINT ["python3", "-u"]
