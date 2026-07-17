#!/bin/bash
# Post-merge setup for Kabulhaden Online (Django 5.0 / Python 3.13)
# Runs automatically after every task merge.
# Must be: idempotent, non-interactive, fast.
set -e

echo "==> Running database migrations..."
python manage.py migrate --no-input

echo "==> Collecting static files..."
python manage.py collectstatic --no-input --clear -v 0

echo "==> Post-merge setup complete."
