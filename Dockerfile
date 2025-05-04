# syntax=docker/dockerfile:1
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY photoalbum/requirements.txt ./requirements.txt
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

COPY photoalbum /app

CMD ["gunicorn", "photoalbum.wsgi:application", "--bind", "0.0.0.0:8000"] 