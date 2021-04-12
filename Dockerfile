# prepare base Docker image
FROM python:3.8.1

# create app root directory 
RUN mkdir /todo_app

# copy project files to Docker's root directory
ADD . /todo_app/

# change cd to root directory
WORKDIR /todo_app

# upgrade pip and install requirements
RUN pip install --upgrade pip \
&& pip install -r requirements.txt \
&& python manage.py collectstatic --noinput

# EXPOSE 8000

# CMD ["gunicorn", "superlists.wsgi", "--bind", "0.0.0.0:8000"]

CMD gunicorn superlists.wsgi --bind 0.0.0.0:$PORT