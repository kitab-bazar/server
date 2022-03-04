#!/bin/bash
python manage.py collectstatic --noinput &
python manage.py migrate --noinput &
# start
gunicorn config.wsgi:application --timeout=40 --bind 0.0.0.0:8020 &
# celery
celery -A config worker --loglevel=INFO
