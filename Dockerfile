FROM python:3.7.3-alpine

MAINTAINER togglecorp info@togglecorp.com

ENV PYTHONUNBUFFERED 1
ENV PYTHON3 /usr/local/bin/python3
ENV PIP3 /usr/local/bin/pip3

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN apk add --no-cache --virtual .build-deps \
        python3-dev \
    && $PIP3 install --upgrade pip \
    && $PIP3 install --no-cache-dir -r requirements.txt \
    && apk del --no-cache .build-deps

COPY . /code/

CMD ./deploy/scripts/run_server.sh
