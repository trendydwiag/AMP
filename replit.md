# Kabulhaden CMS

A production-grade Django CMS for managing a radio station's digital presence.

## Tech Stack

- **Backend:** Django 5.0, Python 3.13, PostgreSQL (Replit-managed)
- **Frontend:** Tailwind CSS, AlpineJS, HTMX
- **Apps:** Users, Radio, Broadcast, Podcast, News, Media Manager, Sponsor, Community, Website, Platform, Studio

## How to Run

The **Start application** workflow runs the Django dev server on port 5000.

```bash
python3 manage.py runserver 0.0.0.0:5000
```

## Environment

| Variable | Source | Notes |
|---|---|---|
| `DJANGO_SECRET_KEY` | Replit Secret | Cryptographic signing key |
| `DATABASE_URL` | Replit (auto-injected) | PostgreSQL connection string |
| `DJANGO_DEBUG` | Replit Env Var | `True` for development |
| `DJANGO_ALLOWED_HOSTS` | Replit Env Var | `*` for development |
| `DJANGO_SETTINGS_MODULE` | Replit Env Var | `config.settings.development` |

## First-time Setup (already done)

```bash
pip install -r requirements/base.txt Pillow django-debug-toolbar pytest-django
npm install && npm run build:dev
python3 manage.py migrate
python3 manage.py init_settings
python3 manage.py createsuperuser  # create your admin account
```

## Useful Commands

```bash
# Create an admin user
python3 manage.py createsuperuser

# Rebuild Tailwind CSS
npm run build:dev          # dev (unminified)
npm run build              # production (minified)
npm run watch              # watch mode

# Run tests
python3 manage.py test --verbosity=2

# Django shell
python3 manage.py shell
```

## URL Structure

| Prefix | Module |
|---|---|
| `/` | Public website |
| `/akun/` | Authentication |
| `/studio/` | Dashboard (login redirect) |
| `/pengaturan/` | Settings |
| `/media/` | Media manager |
| `/radio/` | Radio engine |
| `/broadcast/` | Broadcast management |
| `/admin/` | Django admin |

## Architecture

Follows the **Service-Repository pattern**: all data access goes through `BaseRepository[T]` → `BaseService[R]` → Views. See `docs/32_SERVICES_REPOSITORIES.md` for details.

## User Preferences

- Indonesian language for all user-facing strings
- UUID primary keys on all models
- Coffee-themed color palette (see `docs/07_COLOR_PALETTE.md`)
- Poppins + Inter typography
