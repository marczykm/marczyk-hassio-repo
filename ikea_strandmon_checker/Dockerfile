ARG BUILD_FROM
FROM $BUILD_FROM

RUN \
  apk add --no-cache \
    python3 py3-pip

COPY main.py /
COPY requirements.txt /

WORKDIR /

RUN pip install -r requirements.txt

CMD [ "/usr/bin/python3", "/main.py" ]
