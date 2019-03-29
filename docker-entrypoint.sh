#!/bin/bash

echo "Collect static files"
python manage.py collectstatic --noinput


echo "Add database migrations"
python manage.py makemigrations

echo "Apply database migrations"
python manage.py migrate --fake-initial

echo "Starting server"
python manage.py runserver 0.0.0.0:8000