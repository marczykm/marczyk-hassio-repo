ARG BUILD_FROM=ghcr.io/hassio-addons/base:12.2.2
FROM $BUILD_FROM
#FROM ghcr.io/hassio-addons/base:12.2.2

RUN \
  apk add --no-cache \
    python3 py3-pip

COPY run.sh /
COPY main.py /
COPY requirements.txt /

WORKDIR /

RUN pip install -r requirements.txt

RUN chmod a+x /run.sh

CMD [ "./run.sh" ]
