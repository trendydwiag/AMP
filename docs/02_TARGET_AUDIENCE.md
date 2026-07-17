# 02 — Target Audience

## Who Uses Kabulhaden CMS

Kabulhaden serves three distinct audience groups, each with different needs, access levels, and interaction patterns.

---

## 1. Radio Station Staff (Internal Users)

The primary users who log into the CMS daily to manage content, configure systems, and oversee operations. They authenticate via `/akun/masuk/` and interact with the admin dashboard at `/`.

### Staff Sub-Roles

| Role | RBAC Level | Primary Focus | Access Scope |
|---|---|---|---|
| **Station Manager** | SUPERUSER | Full system control | Everything — system config, user management, all content, analytics |
| **Technical Administrator** | ADMINISTRATOR | System configuration & operations | Settings, radio engine, media, user management (no destructive system changes) |
| **Content Editor** | EDITOR | Content creation & publishing | Programs, broadcasts, episodes, news, podcasts, media uploads |
| **Staff Viewer** | VIEWER | Read-only monitoring | View dashboards, schedules, and published content only |

### How They Access the System

- **CMS Dashboard**: Sidebar-based admin interface at `/` (extends `dashboard_base.html`)
- **Django Admin Panel**: Superuser-only at `/admin/` for low-level data management
- **Module Pages**: Each CMS module has its own URL namespace:
  - Radio: `/radio/`
  - Broadcast: `/broadcast/`
  - Media: `/media/`
  - Settings: `/pengaturan/`

---

## 2. Website Visitors (Public Audience)

Listeners and general audience who visit the station's public website. They do **not** authenticate — all content is publicly accessible unless the site is in maintenance mode.

### Visitor Sub-Types

| Type | Behavior | Key Pages |
|---|---|---|
| **Regular Listener** | Checks schedule, listens to live radio | `/` (homepage), `/jadwal/`, `/radio-live/` |
| **Podcast Consumer** | Browses and listens to podcast episodes | `/podcast/`, `/podcast/<slug>/` |
| **News Reader** | Reads articles and station updates | `/berita/`, `/berita/<slug>/` |
| **Community Participant** | Joins discussions, posts replies | `/komunitas/`, `/komunitas/<slug>/` |
| **Sponsor/Partner Visitor** | Views partner listings | `/mitra/`, `/sponsor/` |
| **Contact Inquirer** | Reaches out to the station | `/kontak/` |
| **Newsletter Subscriber** | Subscribes for updates via AJAX POST | `/newsletter/subscribe/` |

### How They Interact

- **No authentication required** — all public pages are open
- **AlpineJS-powered** interactions: mobile menu toggle, search modal (⌘K), sticky radio player, announcement dismissal
- **HTMX partial updates** for newsletter subscription without full page reload
- **Responsive design** — adapts from mobile (< 640px) to desktop (> 1024px)
- **SEO-optimized** — structured data (JSON-LD), Open Graph tags, meta descriptions

---

## 3. Developers (Technical Maintainers)

Engineers who maintain, extend, and deploy the Kabulhaden system.

### Developer Concerns

| Area | Details |
|---|---|
| **Codebase** | 11 Django apps, service layer pattern, repository pattern |
| **Testing** | 509 tests across all modules — `python manage.py test` |
| **Database** | PostgreSQL 16 with UUID primary keys, migrations per app |
| **Deployment** | Docker Compose (web + db services), Gunicorn WSGI |
| **Configuration** | `config/settings/base.py`, `development.py`, `production.py` with django-environ |
| **Frontend** | Tailwind CSS build pipeline, AlpineJS CDN, HTMX CDN |
| **Documentation** | `/docs/` directory with ADR, ERD, API endpoints, test coverage, permissions matrix |

---

## RBAC Role Matrix

The four system roles defined in `utils/choices.py` map to real-world station positions:

```
SUPERUSER (Super User)
├── Full system access
├── User management (create, suspend, delete)
├── System settings (all 10 config modules)
├── Django Admin panel access
└── Can assign any role

ADMINISTRATOR (Administrator)
├── System settings (read/write)
├── Radio engine configuration
├── Media management
├── User management (view, create — no delete)
└── No Django Admin access

EDITOR (Editor/Penulis)
├── Content creation (programs, episodes, news, podcasts)
├── Broadcast schedule management
├── Media uploads
├── Community moderation
└── Read-only settings access

VIEWER (Viewer/Pembaca)
├── View all dashboards
├── View published content
├── Export reports
└── No create/edit/delete operations
```

---

## User Journey Overview

```
Station Manager ──────► Login → Dashboard → Settings → Users → Radio Config → Broadcast Schedule
                              │
Technical Admin ──────► Login → Dashboard → Radio Engine → Media Manager → Settings
                              │
Content Editor ───────► Login → Dashboard → Programs → Episodes → News → Podcasts
                              │
Staff Viewer ─────────► Login → Dashboard → View Reports → View Schedules
                              │
Website Visitor ──────► Homepage → Live Radio → Programs → Schedule → Podcast → News → Community
```
