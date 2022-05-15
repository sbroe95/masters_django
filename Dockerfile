# syntax=docker/dockerfile:1
FROM python:3.9
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
RUN apt-get update \
    && apt-get -y install curl \
    && apt-get -y install vim \
    && apt-get -y install netcat
COPY . /code/
