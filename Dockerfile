# prepare base Docker image
FROM python:3.8.1

# create app root directory 
RUN mkdir /app

# copy project files to Docker's root directory
ADD . /app/

# change cd to root directory
WORKDIR /app

# upgrade pip and install requirements
RUN pip install --upgrade pip \
&& pip install -r requirements.txt \
&& python3 manage.py collectstatic --noinput

# EXPOSE 8000

# CMD ["gunicorn", "superlists.wsgi", "--bind", "0.0.0.0:8000"]

CMD gunicorn superlists.wsgi --bind 0.0.0.0:$PORT

# TO DO - przekminic czemu Docker + Heroku deploy nie widzi statykow....
# przekmin python manage.py collectstatic --noinput