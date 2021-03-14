FROM python:3.6-slim

ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /pybuilder-bandit

COPY . /pybuilder-bandit/

RUN pip install pybuilder
RUN pyb
