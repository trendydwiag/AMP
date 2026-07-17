# 39. Deployment Guide

## Overview

This guide covers the deployment process for Kabulhaden CMS, including Docker setup, environment configuration, and production best practices.

---

## Deployment Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         Production Environment                               │
│                                                                              │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐         │
│  │   Web Server     │    │   Database      │    │   Media Storage │         │
│  │   (Django)       │    │   (PostgreSQL)  │    │   (S3/local)    │         │
│  │                  │    │                 │    │                 │         │
│  │   Gunicorn       │───▶│   PostgreSQL    │    │   AWS S3        │         │
│  │   Port: 8000     │    │   Port: 5432    │    │                 │         │
│  └────────┬────────┘    └─────────────────┘    └─────────────────┘         │
│           │                                                                  │
│           ▼                                                                  │
│  ┌─────────────────┐    ┌─────────────────┐                                │
│  │   Reverse Proxy  │    │   Static Files  │                                │
│  │   (Nginx)        │    │   (WhiteNoise)  │                                │
│  │                  │    │                 │                                │
│  │   Port: 80/443   │    │   /static/      │                                │
│  └─────────────────┘    └─────────────────┘                                │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Docker Setup

### Dockerfile (Multi-Stage Build)

```dockerfile
# Dockerfile

# ============= Stage 1: Build =============
FROM python:3.13-slim as builder

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements/ /app/requirements/
RUN pip install --no-cache-dir --prefix=/install -r /app/requirements/production.txt

# ============= Stage 2: Production =============
FROM python:3.13-slim

WORKDIR /app

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Copy installed packages
COPY --from=builder /install /usr/local

# Copy application code
COPY . /app

# Create non-root user
RUN addgroup --system django && \
    adduser --system --ingroup django django && \
    chown -R django:django /app

# Switch to non-root user
USER django

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:8000/ || exit 1

# Run application
CMD ["gunicorn", "config.wsgi:application", \
     "--bind", "0.0.0.0:8000", \
     "--workers", "4", \
     "--threads", "2", \
     "--timeout", "120", \
     "--access-logfile", "-", \
     "--error-logfile", "-"]
```

### docker-compose.yml

```yaml
version: '3.8'

services:
  app:
    build: .
    command: gunicorn config.wsgi:application --bind 0.0.0.0:8000
    volumes:
      - static_volume:/app/staticfiles
      - media_volume:/app/media
    env_file:
      - .env
    depends_on:
      - db
    networks:
      - cms_network
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 30s

  db:
    image: postgres:16-alpine
    volumes:
      - postgres_data:/var/lib/postgresql/data/
    env_file:
      - .env
    ports:
      - "5432:5432"
    networks:
      - cms_network
    restart: unless-stopped
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U $${POSTGRES_USER} -d $${POSTGRES_DB}"]
      interval: 10s
      timeout: 5s
      retries: 5

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
      - ./nginx/ssl:/etc/nginx/ssl:ro
      - static_volume:/app/staticfiles:ro
      - media_volume:/app/media:ro
    depends_on:
      - app
    networks:
      - cms_network
    restart: unless-stopped

volumes:
  postgres_data:
  static_volume:
  media_volume:

networks:
  cms_network:
    driver: bridge
```

---

## Environment Configuration

### Environment Variables

```bash
# .env

# Django
DJANGO_SECRET_KEY=your-super-secret-key-here
DJANGO_DEBUG=False
DJANGO_SETTINGS_MODULE=config.settings.production
DJANGO_ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Database
DATABASE_URL=postgres://kabulhaden_user:securepassword@db:5432/kabulhaden_db
POSTGRES_USER=kabulhaden_user
POSTGRES_PASSWORD=securepassword
POSTGRES_DB=kabulhaden_db
POSTGRES_HOST=db
POSTGRES_PORT=5432

# Security
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
SECURE_HSTS_SECONDS=31536000

# Email
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=Kabulhaden <noreply@yourdomain.com>

# Media (S3 Optional)
USE_S3=False
# AWS_ACCESS_KEY_ID=your-access-key
# AWS_SECRET_ACCESS_KEY=your-secret-key
# AWS_STORAGE_BUCKET_NAME=your-bucket

# Timezone
TIME_ZONE=Asia/Jakarta
LANGUAGE_CODE=id
```

---

## Entrypoint Script

```bash
#!/bin/bash
# scripts/entrypoint.sh

set -e

echo "Waiting for PostgreSQL..."
while ! pg_isready -h $POSTGRES_HOST -p $POSTGRES_PORT -U $POSTGRES_USER; do
  sleep 1
done
echo "PostgreSQL is ready."

echo "Running migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Initializing settings..."
python manage.py init_settings

echo "Starting application..."
exec "$@"
```

---

## Gunicorn Configuration

```python
# config/gunicorn.py
import multiprocessing

bind = "0.0.0.0:8000"
workers = multiprocessing.cpu_count() * 2 + 1
threads = 2
timeout = 120
keepalive = 5
max_requests = 1000
max_requests_jitter = 50

accesslog = "-"
errorlog = "-"
loglevel = "info"
```

---

## Nginx Configuration

```nginx
# nginx/nginx.conf
events {
    worker_connections 1024;
}

http {
    include       /etc/nginx/mime.types;
    default_type  application/octet-stream;

    # Logging
    access_log /var/log/nginx/access.log;
    error_log /var/log/nginx/error.log;

    # Gzip
    gzip on;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml;

    # Rate limiting
    limit_req_zone $binary_remote_addr zone=general:10m rate=10r/s;

    upstream django {
        server app:8000;
    }

    server {
        listen 80;
        server_name yourdomain.com;

        # Redirect to HTTPS
        return 301 https://$server_name$request_uri;
    }

    server {
        listen 443 ssl http2;
        server_name yourdomain.com;

        ssl_certificate /etc/nginx/ssl/fullchain.pem;
        ssl_certificate_key /etc/nginx/ssl/privkey.pem;

        # Security headers
        add_header X-Frame-Options "DENY" always;
        add_header X-Content-Type-Options "nosniff" always;
        add_header X-XSS-Protection "1; mode=block" always;

        # Static files
        location /static/ {
            alias /app/staticfiles/;
            expires 30d;
            add_header Cache-Control "public, immutable";
        }

        # Media files
        location /media/ {
            alias /app/media/;
            expires 7d;
        }

        # Django
        location / {
            limit_req zone=general burst=20 nodelay;
            
            proxy_pass http://django;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }
}
```

---

## Deployment Steps

### 1. Initial Setup

```bash
# Clone repository
git clone https://github.com/your-org/kabulhaden.git
cd kabulhaden

# Copy environment file
cp .env.example .env
# Edit .env with production values

# Start services
docker-compose up -d

# Initialize database
docker-compose exec app python manage.py migrate
docker-compose exec app python manage.py createsuperuser
docker-compose exec app python manage.py init_settings
```

### 2. SSL Certificate

```bash
# Using Certbot
docker-compose exec nginx sh
apk add certbot
certbot certonly --webroot -w /app/staticfiles \
    -d yourdomain.com \
    -d www.yourdomain.com

# Or mount existing certificates
# Place in nginx/ssl/
```

### 3. Deploy Updates

```bash
# Pull latest changes
git pull origin main

# Rebuild and restart
docker-compose build app
docker-compose up -d

# Run migrations
docker-compose exec app python manage.py migrate

# Collect static files
docker-compose exec app python manage.py collectstatic --noinput
```

---

## Management Commands

| Command | Purpose |
|---------|---------|
| `python manage.py migrate` | Run database migrations |
| `python manage.py collectstatic` | Collect static files |
| `python manage.py createsuperuser` | Create admin user |
| `python manage.py init_settings` | Initialize singleton settings |
| `python manage.py cleanup_media` | Remove orphaned media |
| `python manage.py compress_media` | Compress media files |
| `python manage.py generate_thumbnails` | Generate thumbnails |
| `python manage.py refresh_radio_all` | Refresh radio data |
| `python manage.py check_stream_health` | Check stream health |

---

## Monitoring

### Health Check Endpoint

```python
# apps/broadcast/views.py
class HealthCheckView(View):
    def get(self, request):
        from django.db import connection
        from apps.radio.models import Station
        
        db_ok = True
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
        except Exception:
            db_ok = False
        
        stations_ok = Station.objects.filter(is_active=True).exists()
        
        status = {
            'status': 'healthy' if db_ok and stations_ok else 'unhealthy',
            'database': 'ok' if db_ok else 'error',
            'radio': 'ok' if stations_ok else 'error',
            'timestamp': timezone.now().isoformat(),
        }
        
        return JsonResponse(status, status=200 if status['status'] == 'healthy' else 503)
```

### Log Management

```python
# config/settings/production.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs' / 'django.log',
            'formatter': 'verbose',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': True,
        },
        'apps': {
            'handlers': ['file', 'console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
```

---

## Backup Strategy

### Database Backup

```bash
# Daily backup cron
#!/bin/bash
# scripts/backup_db.sh

BACKUP_DIR="/backups/postgres"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
FILENAME="kabulhaden_${TIMESTAMP}.sql.gz"

docker-compose exec -T db pg_dump -U $POSTGRES_USER $POSTGRES_DB | gzip > "${BACKUP_DIR}/${FILENAME}"

# Keep last 30 days
find ${BACKUP_DIR} -name "*.sql.gz" -mtime +30 -delete
```

### Media Backup

```bash
# Sync media to S3
aws s3 sync /app/media s3://your-backup-bucket/media/ --delete
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Database connection refused | Check PostgreSQL container is running: `docker-compose ps` |
| Migration errors | Run `docker-compose exec app python manage.py migrate` |
| Static files not loading | Run `docker-compose exec app python manage.py collectstatic` |
| Permission denied | Check file ownership: `chown -R django:django /app` |
| Memory issues | Increase workers or reduce `max_requests` |
| Stream disconnecting | Check encoder health: `python manage.py check_stream_health` |

---

## Related Documentation

- `.env.example` - Environment variable reference
- `28_FUTURE_DESKTOP_GUIDE.md` - Desktop considerations
- `32_AUTHENTICATION_AUTHORIZATION_GUIDE.md` - Security settings
- `36_MEDIA_MANAGEMENT_GUIDE.md` - Media storage

---

*Last updated: 2026-07-15*
