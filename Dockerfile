FROM python:slim

COPY main.py PetkitW5BLEMQTT/ /src/

WORKDIR /src/

RUN python -m pip install -r PetkitW5BLEMQTT/requirements.txt

ENV ADDRESS=""
ENV BROKER=""
ENV PORT=""
ENV USER=""
ENV PASSWORD=""
ENV LOG_LEVEL="INFO"

CMD ["python", "./main.py", "--address $ADDRESS", "--mqtt", "--mqtt_broker $BROKER", "--mqtt_port $PORT", "--mqtt_user $USER", "--mqtt_password $PASSWORD", "--logging_level $LOG_LEVEL"] 
