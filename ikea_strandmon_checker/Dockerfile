ARG BUILD_FROM
FROM $BUILD_FROM

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
