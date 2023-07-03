FROM python:3.9.16
ENV PYTHONUNBUFFERED=1
WORKDIR /django
COPY requirements.txt /django
RUN pip install --upgrade pip
RUN pip install django-on-heroku
RUN pip install -r requirements.txt
