# prepare base Docker image
FROM python:3.8.1

# create app root directory 
RUN mkdir /app

# create static directory
RUN mkdir /app/static

# copy project files to Docker's root directory
ADD . /app/

# set env variables for AWS S3 storage
ENV HEROKU=True
ENV AWS_ACCESS_KEY_ID=AKIA2NB7TG5EAM3FJXFN
ENV AWS_SECRET_ACCESS_KEY=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
ENV AWS_STORAGE_BUCKET_NAME=rs-django-todo-list-staging

# set DB url

ENV DATABASE_URL=postgres://kyuyifqtpbiojt:d742d9029b84770b9c5efb256881877e4e68f2f6dcd2505f78543be781a4a944@ec2-54-155-35-88.eu-west-1.compute.amazonaws.com:5432/d4u27jpbjdfggs

# change cd to root directory
WORKDIR /app

# upgrade pip and install requirements
RUN pip install --upgrade pip \
&& pip install -r requirements.txt \
&& python3 manage.py migrate --noinput \
&& python3 manage.py collectstatic --noinput --verbosity 3

# EXPOSE 8000

# CMD ["gunicorn", "superlists.wsgi", "--bind", "0.0.0.0:8000"]

CMD gunicorn superlists.wsgi --bind 0.0.0.0:$PORT

# TO DO - przekminic czemu Docker + Heroku deploy nie widzi statykow....
# przekmin python manage.py collectstatic --noinput
