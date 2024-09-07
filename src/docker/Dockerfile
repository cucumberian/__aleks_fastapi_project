FROM python:3.12-slim-bullseye

ENV HOME_DIR /home/python/
ENV APP_DIR ${HOME_DIR}/app/

RUN mkdir -p ${APP_DIR}

WORKDIR ${APP_DIR}

COPY requirements.txt .

RUN pip3 install -U pip && pip3 install --no-cache-dir -r requirements.txt

COPY . .