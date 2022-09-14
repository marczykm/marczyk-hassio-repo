ARG BUILD_FROM=ghcr.io/hassio-addons/base:12.2.2
FROM $BUILD_FROM

RUN \
  apk add --no-cache \
    python3 py3-pip

WORKDIR /data

COPY main.py /
COPY requirements.txt /

RUN ls

RUN pip install -r /requirements.txt

CMD [ "python3", "/main.py" ]
