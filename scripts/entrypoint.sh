#!/bin/bash
set -e

# Function to wait for database if POSTGRES_HOST is specified
wait_for_db() {
  if [ -n "$POSTGRES_HOST" ]; then
    echo "Waiting for PostgreSQL at $POSTGRES_HOST:$POSTGRES_PORT..."
    while ! nc -z "$POSTGRES_HOST" "${POSTGRES_PORT:-5432}"; do
      sleep 0.5
    done
    echo "PostgreSQL is up and running!"
  fi
}

# Wait for DB
wait_for_db

# Run Django migrations
echo "Applying database migrations..."
python manage.py migrate --noinput

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

# Start application server based on DJANGO_SETTINGS_MODULE
if [ "$DJANGO_SETTINGS_MODULE" = "config.settings.production" ]; then
  echo "Starting production WSGI server (Gunicorn)..."
  exec gunicorn config.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers ${GUNICORN_WORKERS:-3} \
    --access-logfile - \
    --error-logfile - \
    --log-level info
else
  echo "Starting development server..."
  exec python manage.py runserver 0.0.0.0:8000
fi
