#!/bin/sh

python manage.py makemigrations --noinput
python manage.py migrate --noinput

gunicorn --bind 0.0.0.0:${PORT:-8000} -w 2 -k uvicorn.workers.UvicornWorker backend.asgi:application