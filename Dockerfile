FROM python:3.10-alpine

WORKDIR /app

COPY requirements.txt requirements.txt
COPY setup.py setup.py
COPY moviebot moviebot
COPY config.yml config.yml

RUN apk update && apk add python3-dev \
                        gcc \
                        libc-dev

RUN python3 -m venv env
RUN /app/env/bin/pip3 install -r requirements.txt

CMD [ "/app/env/bin/bot-run", "./config.yml" ]