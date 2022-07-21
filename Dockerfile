FROM python:3.10-alpine

WORKDIR /app

COPY requirements.txt requirements.txt
COPY setup.py setup.py
COPY dist/Moviebot-0.1-py3-none-any.whl Moviebot-0.1-py3-none-any.whl
COPY config.yml config.yml

RUN apk update && apk add python3-dev \
                        gcc \
                        libc-dev

RUN python3 -m venv env
RUN /app/env/bin/pip3 install ./Moviebot-0.1-py3-none-any.whl

CMD [ "/app/env/bin/bot-run", "./config.yml" ]