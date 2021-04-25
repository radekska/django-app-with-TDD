# prepare base Docker image
FROM python:3.8.1

# create app root directory 
RUN mkdir /app

# create static directory
RUN mkdir /app/static

# copy project files to Docker's root directory
ADD . /app/

# change cd to root directory
WORKDIR /app

ARG HEROKU="True"

ARG AWS_ACCESS_KEY_ID="default"
ARG AWS_SECRET_ACCESS_KEY="default"
ARG AWS_STORAGE_BUCKET_NAME="default"

ARG EMAIL_HOST_USER="default"
ARG EMAIL_HOST_PASSWORD="default"

ARG DATABASE_URL="default"

# upgrade pip and install requirements
RUN pip install --upgrade pip \
&& pip install -r requirements.txt \
&& python3 manage.py migrate --noinput \
&& python3 manage.py collectstatic --noinput --verbosity 3

# EXPOSE 8000

# CMD ["gunicorn", "superlists.wsgi", "--bind", "0.0.0.0:8000"]

CMD gunicorn superlists.wsgi --bind 0.0.0.0:$PORT
