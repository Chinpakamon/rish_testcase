#!/bin/sh

echo "Running migrations..."
python manage.py migrate --noinput

echo "Loading initial data..."
python manage.py loaddata initial_data || echo "Fixtures already loaded"

echo "Starting server..."
python manage.py runserver 0.0.0.0:8000
