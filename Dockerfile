FROM python:3.8.1

MAINTAINER Radosław Skałbania

RUN mkdir /todo_app

ADD . /todo_app/

WORKDIR /todo_app

EXPOSE 8000

RUN pip install --upgrade pip \

	&& pip install -r requirements.txt

CMD ["gunicorn", "superlists.wsgi", "--bind", "0.0.0.0:8000"]