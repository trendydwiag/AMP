# Kabulhaden CMS — Deployment & Operations

Complete deployment, DevOps, and engineering documentation for the Kabulhaden CMS platform.

## Architecture Overview

```
┌─────────────┐     ┌──────────────┐     ┌────────────────┐
│   Nginx     │────▶│   Gunicorn   │────▶│   Django 5.0   │
│  :443/:80   │     │   :8000      │     │   (WSGI)       │
└─────────────┘     └──────────────┘     └───────┬────────┘
                                                  │
                              ┌────────────────────┼──────────────────┐
                              │                    │                  │
                     ┌────────▼───────┐  ┌────────▼──────┐  ┌───────▼────────┐
                     │  PostgreSQL 16 │  │  WhiteNoise   │  │  Media Files   │
                     │    :5432       │  │  Static Files │  │  /media/       │
                     └────────────────┘  └───────────────┘  └────────────────┘
```

## Tech Stack

| Layer           | Technology                           |
|-----------------|--------------------------------------|
| Web Server      | Nginx (reverse proxy, SSL, static)   |
| WSGI Server     | Gunicorn 22.x                        |
| Framework       | Django 5.0.x                         |
| Language        | Python 3.10                          |
| Database        | PostgreSQL 16                         |
| Static Files    | WhiteNoise (Brotli compressed)       |
| Frontend        | Tailwind CSS + Alpine.js + HTMX      |
| Container       | Docker + Docker Compose              |
| Process Mgmt    | Systemd (bare-metal) or Docker       |

## Project Structure

```
kabulhaden/
├── apps/                    # 12 Django applications
│   ├── users/               # Authentication & user management
│   ├── core/                # Core utilities, middleware, management commands
│   ├── settings/            # System settings
│   ├── media_manager/       # Media file management
│   ├── radio/               # Live radio streaming engine
│   ├── broadcast/           # Broadcast/schedule management
│   ├── podcast/             # Podcast episodes & RSS
│   ├── news/                # News articles & CMS
│   ├── sponsor/             # Sponsor management
│   ├── community/           # Community features
│   ├── website/             # Public-facing website
│   └── content/             # General content management
├── config/                  # Django project config
│   ├── settings/
│   │   ├── base.py          # Shared settings
│   │   ├── development.py   # Local dev settings
│   │   └── production.py    # Production settings
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── templates/               # Django templates
├── static/                  # Static assets (CSS, JS, images)
├── media/                   # User-uploaded files
├── logs/                    # Application logs
├── scripts/                 # Operational scripts
├── requirements/            # Python dependencies (split by env)
│   ├── base.txt
│   ├── development.txt
│   └── production.txt
├── Dockerfile               # Multi-stage Docker build
├── docker-compose.yml       # Production compose
├── docker-compose.dev.yml   # Development compose
├── nginx.conf               # Nginx configuration
├── gunicorn.conf.py         # Gunicorn tuning
└── manage.py
```

## Documentation Index

| Document | Purpose |
|----------|---------|
| [SETUP.md](SETUP.md) | Complete local & production setup guide |
| [Dockerfile](Dockerfile) | Multi-stage Docker build |
| [docker-compose.yml](docker-compose.yml) | Production container orchestration |
| [docker-compose.dev.yml](docker-compose.dev.yml) | Development containers |
| [nginx.conf](nginx.conf) | Nginx reverse proxy config |
| [gunicorn.conf.py](gunicorn.conf.py) | Gunicorn worker tuning |
| [requirements.txt](requirements.txt) | Python dependency list |
| [env.example](env.example) | Environment variables template |
| [systemd/kabulhaden.service](systemd/kabulhaden.service) | Systemd service unit |
| [scripts/deploy.sh](scripts/deploy.sh) | Zero-downtime deployment |
| [scripts/backup.sh](scripts/backup.sh) | Automated database backup |
| [scripts/restore.sh](scripts/restore.sh) | Database restore |
| [scripts/setup.sh](scripts/setup.sh) | Initial server provisioning |
| [scripts/health_check.sh](scripts/health_check.sh) | Application health check |
| [MONITORING.md](MONITORING.md) | Monitoring & logging guide |
| [PERFORMANCE.md](PERFORMANCE.md) | Performance optimization |
| [SECURITY.md](SECURITY.md) | Security hardening |
| [BACKUP.md](BACKUP.md) | Backup & disaster recovery |
| [TROUBLESHOOTING.md](TROUBLESHOOTING.md) | Common issues & fixes |
| [RUNBOOK.md](RUNBOOK.md) | Operations runbook |
| [GIT_WORKFLOW.md](GIT_WORKFLOW.md) | Git branching & workflow |
| [AI_DEVELOPMENT.md](AI_DEVELOPMENT.md) | AI-assisted dev guidelines |
| [CHANGELOG.md](CHANGELOG.md) | Project changelog |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Contribution guidelines |

## Quick Start

```bash
# 1. Clone and configure
git clone <repo-url> kabulhaden && cd kabulhaden
cp .env.example .env
# Edit .env with your values

# 2. Docker development
docker compose -f docker-compose.dev.yml up --build

# 3. Access
# Admin: http://localhost:8000/admin/
# Public: http://localhost:8000/
```

## Production Deployment

```bash
# On the server
git clone <repo-url> /var/www/kabulhaden && cd /var/www/kabulhaden
cp .env.example .env
# Configure .env for production

docker compose up -d --build
docker compose exec web python manage.py migrate
docker compose exec web python manage.py collectstatic --noinput
docker compose exec web python manage.py createsuperuser
```

## Ports

| Service   | Dev  | Production |
|-----------|------|------------|
| Nginx     | —    | 80/443     |
| Gunicorn  | —    | 8000       |
| Django    | 8000 | —          |
| PostgreSQL| 5432 | 5432       |
