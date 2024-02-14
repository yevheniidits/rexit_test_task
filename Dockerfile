FROM python:3.12-slim

RUN apt-get update -y && \
    apt-get install -y git build-essential python3-dev python3-cffi libssl-dev

WORKDIR /app/

COPY requirements.txt /app/

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN pip install --upgrade pip
RUN pip install ipython
RUN pip install -r requirements.txt --no-cache-dir

COPY . /app
RUN git config --global --add safe.directory /app
EXPOSE 8000
