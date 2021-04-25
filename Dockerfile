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

# need to declare those vars as needed at Docker container build time.
ARG AWS_ACCESS_KEY_ID
ARG AWS_SECRET_ACCESS_KEY
ARG AWS_STORAGE_BUCKET_NAME

ARG EMAIL_HOST_USER
ARG EMAIL_HOST_PASSWORD

ARG DATABASE_URL

# upgrade pip and install requirements
RUN pip install --upgrade pip \
&& pip install -r requirements.txt \
&& python3 manage.py migrate --noinput \
&& python3 manage.py collectstatic --noinput --verbosity 3

# need to decleare env vars as well as needed in run time.
ENV AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}
ENV AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}
ENV AWS_STORAGE_BUCKET_NAME=${AWS_STORAGE_BUCKET_NAME}

ENV EMAIL_HOST_USER=${EMAIL_HOST_USER}
ENV EMAIL_HOST_PASSWORD=%{EMAIL_HOST_PASSWORD}

ENV DATABASE_URL=%{DATABASE_URL}

CMD gunicorn superlists.wsgi --bind 0.0.0.0:$PORT
