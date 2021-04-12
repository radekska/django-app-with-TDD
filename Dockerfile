FROM python:3.8.1

MAINTAINER Radosław Skałbania

RUN mkdir /todo_app

ADD . /todo_app/

WORKDIR /todo_app

RUN apt-get update && apt-get upgrade -y

RUN pip install -r requirements.txt