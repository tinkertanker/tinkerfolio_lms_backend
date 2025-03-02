FROM python:3.11-bullseye
ENV PYTHONUNBUFFERED=1
WORKDIR /django

# Install PostgreSQL client libraries
RUN apt-get update && apt-get install -y \
    libpq-dev \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /django
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
