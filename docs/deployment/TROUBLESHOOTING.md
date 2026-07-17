# Kabulhaden CMS — Troubleshooting Guide

Common issues and their solutions.

---

## Table of Contents

1. [Docker Issues](#docker-issues)
2. [Database Issues](#database-issues)
3. [Django Issues](#django-issues)
4. [Static Files Issues](#static-files-issues)
5. [Nginx Issues](#nginx-issues)
6. [Authentication Issues](#authentication-issues)
7. [Performance Issues](#performance-issues)
8. [Email Issues](#email-issues)

---

## Docker Issues

### Container won't start

```bash
# Check logs
docker compose logs web
docker compose logs db

# Check container status
docker compose ps

# Rebuild from scratch
docker compose down
docker compose up --build
```

### "Port already in use"

```bash
# Find process using the port
lsof -i :8000
lsof -i :5432
lsof -i :80

# Kill the process
kill -9 <PID>

# Or change ports in docker-compose.yml
```

### "Cannot connect to database"

```bash
# Check if db container is healthy
docker compose ps db

# Test connection from web container
docker compose exec web python -c "
import environ, os
env = environ.Env()
print(env.db('DATABASE_URL'))
"

# Check DATABASE_URL format
echo $DATABASE_URL
```

### Volume permission denied

```bash
# Fix ownership
sudo chown -R 1000:1000 /var/www/kabulhaden/media
sudo chown -R 1000:1000 /var/www/kabulhaden/logs

# Or run as root temporarily
docker compose exec -u root web bash
```

### Container keeps restarting

```bash
# Check restart count
docker inspect kabulhaden_web | grep RestartCount

# Check logs for crash reason
docker compose logs --tail=50 web

# Enter container for debugging
docker compose exec web bash
```

---

## Database Issues

### "Connection refused"

```bash
# Check PostgreSQL is running
docker compose ps db

# Check PostgreSQL logs
docker compose logs db

# Test connection
docker exec kabulhaden_db pg_isready -U kabulhaden_user

# Check if database exists
docker exec kabulhaden_db psql -U kabulhaden_user -l
```

### "FATAL: password authentication failed"

```bash
# Verify credentials in .env match docker-compose.yml
grep POSTGRES .env

# Reset PostgreSQL password
docker compose exec db psql -U kabulhaden_user -d postgres -c \
  "ALTER USER kabulhaden_user WITH PASSWORD 'new_password';"

# Update .env with new password
# Restart web container
docker compose restart web
```

### "database does not exist"

```bash
# Create database
docker compose exec db psql -U kabulhaden_user -d postgres -c \
  "CREATE DATABASE kabulhaden_db OWNER kabulhaden_user;"

# Run migrations
docker compose exec web python manage.py migrate --noinput
```

### "relation does not exist"

```bash
# Migrations not applied
docker compose exec web python manage.py migrate --noinput

# Check migration status
docker compose exec web python manage.py showmigrations
```

### Slow queries

```bash
# Enable query logging temporarily
docker compose exec db psql -U kabulhaden_user -d kabulhaden_db -c \
  "SET log_min_duration_statement = 1000;"

# Check pg_stat_statements
docker compose exec db psql -U kabulhaden_user -d kabulhaden_db -c \
  "SELECT query, mean_exec_time FROM pg_stat_statements ORDER BY mean_exec_time DESC LIMIT 10;"
```

---

## Django Issues

### "ModuleNotFoundError"

```bash
# Ensure virtualenv is activated
source .venv/bin/activate

# Or for Docker
docker compose exec web pip list
docker compose exec web python -c "import django; print(django.get_version())"

# Reinstall requirements
pip install -r requirements/production.txt
```

### "DJANGO_SECRET_KEY not set"

```bash
# Check .env file exists and has SECRET_KEY
cat .env | grep DJANGO_SECRET_KEY

# Generate new key
python3 -c "import secrets; print(secrets.token_urlsafe(50))"
```

### "You have unapplied migrations"

```bash
python manage.py migrate --noinput

# Check which migrations are pending
python manage.py showmigrations --list
```

### Admin panel 500 error

```bash
# Check error log
tail -50 logs/error.log

# Common causes:
# 1. Missing superuser → python manage.py create_superadmin
# 2. Database tables missing → python manage.py migrate
# 3. Static files missing → python manage.py collectstatic
```

### CSRF verification failed

```bash
# Check CSRF_COOKIE_SECURE in production
# Must match protocol (HTTPS = True, HTTP = False)

# Check ALLOWED_HOSTS includes your domain
grep ALLOWED_HOSTS .env
```

---

## Static Files Issues

### "404: Static files not found"

```bash
# Collect static files
python manage.py collectstatic --noinput --clear

# Check STATIC_ROOT
python manage.py shell -c "from django.conf import settings; print(settings.STATIC_ROOT)"

# Check WhiteNoise is in middleware (right after SecurityMiddleware)
python manage.py shell -c "from django.conf import settings; print(settings.MIDDLEWARE)"
```

### "ManifestMissingFileError"

```bash
# This happens when using CompressedManifestStaticFilesStorage
# without running collectstatic

python manage.py collectstatic --noinput

# Or switch to basic storage for dev
# (already configured in settings/development.py)
```

### CSS not loading

```bash
# Rebuild Tailwind CSS
npm run build

# Check output file exists
ls -la static/css/styles.css

# Check WhiteNoise is serving /static/
curl -I http://localhost:8000/static/css/styles.css
```

---

## Nginx Issues

### "502 Bad Gateway"

```bash
# Check if Gunicorn is running
docker compose ps web

# Check Gunicorn logs
docker compose logs web

# Check Nginx upstream config
# Ensure "upstream django" points to "web:8000"

# Test direct connection
curl http://localhost:8000/health/
```

### "413 Request Entity Too Large"

```nginx
# Increase in nginx.conf
client_max_body_size 50M;  # or higher for media uploads
```

### Nginx won't reload

```bash
# Test configuration
nginx -t

# Check error log
tail -20 /var/log/nginx/error.log

# Common issues:
# 1. Syntax error in nginx.conf
# 2. Missing upstream server
# 3. Port conflicts
```

### SSL certificate errors

```bash
# Check certificate files
ls -la /etc/nginx/certs/

# Test certificate
openssl x509 -in /etc/nginx/certs/fullchain.pem -text -noout

# Renew certificate
sudo certbot renew
```

---

## Authentication Issues

### "Account locked" (Axes)

```bash
# Check lockout status
grep "locked" logs/security.log | tail -5

# Manually unlock user
python manage.py unlock_user <username>

# Reset lockout counter
python manage.py shell -c "
from axes.models import AccessAttempt
AccessAttempt.objects.filter(username='<username>').delete()
"
```

### "Session timeout" keeps happening

```bash
# Check session timeout setting
python manage.py shell -c "from django.conf import settings; print(settings.SESSION_TIMEOUT_MINUTES)"

# Check middleware order
# SessionTimeoutMiddleware must be present
```

### Password reset not working

```bash
# Check email configuration
python manage.py shell -c "
from django.conf import settings
print(settings.EMAIL_BACKEND)
print(settings.EMAIL_HOST)
"

# Test email sending
python manage.py shell -c "
from django.core.mail import send_mail
send_mail('Test', 'Test body', 'from@example.com', ['to@example.com'])
"
```

---

## Performance Issues

### Slow page loads

```bash
# Check response time
time curl -s -o /dev/null http://localhost:8000/

# Enable Django debug toolbar (dev only)
pip install django-debug-toolbar

# Check database queries
python manage.py shell -c "
from django.db import connection
from django.test.utils import override_settings
print(len(connection.queries))
"

# Check for N+1 queries in templates
# Use select_related() and prefetch_related()
```

### High memory usage

```bash
# Check container memory
docker stats kabulhaden_web

# Reduce Gunicorn workers if memory is tight
GUNICORN_WORKERS=2  # instead of 4

# Check for memory leaks
docker exec kabulhaden_web ps aux | sort -nrk 4 | head -5
```

### High CPU usage

```bash
# Check what's consuming CPU
docker stats kabulhaden_web

# Reduce worker count
GUNICORN_WORKERS=2

# Check for infinite loops in tasks
# Check for heavy template rendering
```

---

## Email Issues

### Emails not sending

```bash
# Check email backend
python manage.py shell -c "from django.conf import settings; print(settings.EMAIL_BACKEND)"

# For development, use console backend
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend

# For production, verify SMTP settings
python manage.py shell -c "
from django.conf import settings
print(f'Host: {settings.EMAIL_HOST}')
print(f'Port: {settings.EMAIL_PORT}')
print(f'TLS: {settings.EMAIL_USE_TLS}')
print(f'User: {settings.EMAIL_HOST_USER}')
"

# Test connection
python manage.py shell -c "
import smtplib
s = smtplib.SMTP('smtp.gmail.com', 587)
s.starttls()
s.login('user@gmail.com', 'app-password')
s.quit()
print('Connection successful')
"
```

### Gmail "less secure apps" error

Use App Passwords instead:
1. Enable 2-Factor Authentication on Google account
2. Generate App Password at https://myaccount.google.com/apppasswords
3. Use the 16-character app password as `EMAIL_HOST_PASSWORD`
