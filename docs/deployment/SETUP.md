# Kabulhaden CMS — Setup Guide

Complete guide for setting up the Kabulhaden CMS locally and in production.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Local Development Setup](#local-development-setup)
3. [Docker Development Setup](#docker-development-setup)
4. [Production Setup](#production-setup)
5. [Post-Installation](#post-installation)

---

## Prerequisites

### Local Development
- Python 3.10+
- PostgreSQL 16 (or use SQLite for quick start)
- Node.js 18+ (for Tailwind CSS)
- Git

### Docker Development
- Docker Desktop 4.x+
- Docker Compose v2+

### Production Server
- Ubuntu 22.04+ / Debian 12+
- Docker 24+ & Docker Compose v2
- 2GB+ RAM, 20GB+ disk
- Domain name with DNS configured

---

## Local Development Setup

### 1. Clone & Configure

```bash
git clone <repo-url> kabulhaden
cd kabulhaden

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements/development.txt

# Install frontend dependencies
npm install

# Configure environment
cp .env.example .env
```

### 2. Edit `.env`

```env
DJANGO_SECRET_KEY=your-local-secret-key
DJANGO_DEBUG=True
DJANGO_SETTINGS_MODULE=config.settings.development
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

# SQLite (default, no config needed)
# DATABASE_URL=sqlite:///db.sqlite3

# Or PostgreSQL
DATABASE_URL=postgres://kabulhaden_user:password@localhost:5432/kabulhaden_db
```

### 3. Setup Database

**Option A: SQLite (zero config)**
```bash
python manage.py migrate
```

**Option B: PostgreSQL**
```bash
# Create database
createdb kabulhaden_db

# Run migrations
python manage.py migrate

# Create admin user
python manage.py createsuperuser
```

### 4. Build Frontend Assets

```bash
# Development (watch mode)
npm run watch

# Production build
npm run build
```

### 5. Start Development Server

```bash
python manage.py runserver 0.0.0.0:8000
```

Access:
- **Application**: http://localhost:8000
- **Admin Panel**: http://localhost:8000/admin/
- **Tailwind Watcher**: Runs in separate terminal via `npm run watch`

### 6. Optional: Django Debug Toolbar

```bash
pip install django-debug-toolbar
```

It auto-activates in development mode.

---

## Docker Development Setup

### 1. Clone & Configure

```bash
git clone <repo-url> kabulhaden
cd kabulhaden
cp .env.example .env
```

### 2. Start Containers

```bash
docker compose -f docker-compose.dev.yml up --build
```

This starts:
- **PostgreSQL** on `localhost:5432`
- **Django** dev server on `localhost:8000`
- **Tailwind watcher** (auto-rebuilds CSS)

### 3. Setup Database

```bash
docker compose -f docker-compose.dev.yml exec web python manage.py migrate
docker compose -f docker-compose.dev.yml exec web python manage.py createsuperuser
```

### 4. Useful Commands

```bash
# Shell into web container
docker compose -f docker-compose.dev.yml exec web bash

# Django management commands
docker compose -f docker-compose.dev.yml exec web python manage.py <command>

# View logs
docker compose -f docker-compose.dev.yml logs -f web

# Stop all containers
docker compose -f docker-compose.dev.yml down

# Stop and remove volumes (fresh start)
docker compose -f docker-compose.dev.yml down -v
```

---

## Production Setup

### Option A: Docker Compose (Recommended)

#### 1. Server Preparation

```bash
# Run setup script on fresh server
sudo bash scripts/setup.sh your-domain.com
```

#### 2. Configure Environment

```bash
cd /var/www/kabulhaden
cp .env.example .env
nano .env  # Fill in production values
```

**Critical `.env` values for production:**

```env
DJANGO_SECRET_KEY=<generate-50-char-random-key>
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=your-domain.com,www.your-domain.com
DJANGO_SETTINGS_MODULE=config.settings.production

POSTGRES_PASSWORD=<strong-password>
DATABASE_URL=postgres://kabulhaden_user:<strong-password>@db:5432/kabulhaden_db

SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True

EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

#### 3. Build & Deploy

```bash
docker compose up -d --build

# Initial setup
docker compose exec web python manage.py migrate
docker compose exec web python manage.py collectstatic --noinput
docker compose exec web python manage.py createsuperuser
```

#### 4. Configure SSL (Certbot)

```bash
# Install certbot on host
sudo apt install certbot python3-certbot-nginx

# Get certificate
sudo certbot --nginx -d your-domain.com -d www.your-domain.com

# Auto-renewal
sudo certbot renew --dry-run
```

### Option B: Bare Metal (Systemd)

#### 1. Server Setup

```bash
sudo bash scripts/setup.sh your-domain.com
```

#### 2. Create Virtual Environment

```bash
cd /var/www/kabulhaden
sudo -u kabulhaden python3 -m venv venv
sudo -u kabulhaden venv/bin/pip install -r requirements/production.txt
```

#### 3. Configure Systemd

```bash
sudo cp docs/deployment/systemd/kabulhaden.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable kabulhaden
sudo systemctl start kabulhaden
```

#### 4. Configure Nginx

```bash
# Copy nginx config
sudo cp nginx.conf /etc/nginx/sites-available/kabulhaden
sudo ln -s /etc/nginx/sites-available/kabulhaden /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx
```

---

## Post-Installation

### Create Superuser

```bash
# Docker
docker compose exec web python manage.py createsuperuser

# Bare metal
sudo -u kabulhaden /var/www/kabulhaden/venv/bin/python manage.py createsuperuser
```

### Verify Deployment

```bash
# Health check
./scripts/health_check.sh

# Test HTTP
curl -I https://your-domain.com
curl -I https://your-domain.com/admin/
```

### Setup Automated Backups

```bash
# Add cron job for daily backups at 2 AM
crontab -e
# Add:
0 2 * * * /var/www/kabulhaden/scripts/backup.sh >> /var/www/kabulhaden/logs/backup.log 2>&1
```

### Management Commands

```bash
# Create superadmin
python manage.py create_superadmin

# Reset admin password
python manage.py reset_admin

# Reset specific user password
python manage.py reset_password <username>

# Unlock a locked user
python manage.py unlock_user <username>

# Repair permissions
python manage.py repair_permissions
```
