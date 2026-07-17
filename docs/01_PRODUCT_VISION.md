# 01 — Product Vision

## Why Kabulhaden Exists

Kabulhaden CMS is a purpose-built content management system designed for **radio stations** to manage their entire digital presence from a single platform. It bridges the gap between on-air broadcasting and online audience engagement — giving station staff a unified tool to manage live radio streams, broadcast schedules, podcasts, news, sponsors, community interaction, and the public-facing website.

Radio stations today rely on a patchwork of disconnected tools: one system for streaming, another for scheduling, spreadsheets for playlists, social media for community, and a static website that's always out of date. Kabulhaden eliminates this fragmentation.

---

## Core Value Proposition

| Problem | Solution |
|---|---|
| Scattered broadcast data across multiple tools | Centralized broadcast, schedule, and episode management |
| No integrated live stream player on the website | Built-in radio engine with real-time now-playing, listener stats, and health monitoring |
| Static websites that require a developer to update | Dynamic Django-powered website with self-service CMS modules |
| No audience engagement channel | Community discussions, newsletter subscriptions, and podcast distribution |
| Complex user management for station staff | Role-based access control with 4 permission tiers |

---

## Core Modules

Kabulhaden is organized into **11 Django applications** (`apps/`) that cover every aspect of a radio station's digital operations:

### 1. Authentication & RBAC (`apps/users`)
Custom user model with UUID primary keys, 4 RBAC roles (SUPERUSER, ADMINISTRATOR, EDITOR, VIEWER), two-factor authentication (TOTP), session timeout, brute-force protection via django-axes, login audit trail, and password history enforcement.

### 2. Core System (`apps/core`)
Global context processors, health check endpoint (`/health/`), custom error handlers (400/403/404/500), and audit logging middleware.

### 3. Settings (`apps/settings`)
Singleton configuration models for: Site identity, SEO, Email (SMTP), Security policies, Appearance/theming, Notifications, Social media links, Content defaults, Language & localization, and Media/storage preferences.

### 4. Media Manager (`apps/media_manager`)
File upload and organization with folders, tags, bulk operations, media search API, and support for images, videos, audio, and documents.

### 5. Radio Engine (`apps/radio`)
Multi-provider radio streaming integration (RadioBoss, Icecast, Shoutcast, AzuraCast). Real-time now-playing cache, listener statistics, stream health monitoring, live session tracking, and player configuration APIs.

### 6. Broadcast Management (`apps/broadcast`)
Full broadcast lifecycle: Programs, Hosts, Schedules (day-of-week + time), Broadcast Sessions (scheduled/live/finished/cancelled), Episodes with recordings, Playlists, Guest Stars, and Announcements. Calendar view for visual schedule management.

### 7. Podcast (`apps/podcast`)
Podcast series management with episodes, season/episode numbering, audio file storage, external platform links (Spotify, iTunes, Google Podcasts), and download tracking.

### 8. News (`apps/news`)
Article publishing with categories, tags, draft/published workflow, view counting, and SEO metadata per article.

### 9. Sponsor (`apps/sponsor`)
Partner management (sponsor/partner/media partner) with tier classifications (platinum/gold/silver/bronze), and advertisement management with impression/click tracking and scheduling.

### 10. Community (`apps/community`)
Discussion threads with replies, pinning, locking, view counts, and author management. Fosters audience interaction directly on the station's website.

### 11. Website (`apps/website`)
Public-facing website with: Homepage (live radio hero, today's programs, weekly schedule, latest content), Program directory, Schedule view, Podcast library, News feed, Community forum, Partner/Sponsor pages, Contact, Search, Newsletter, and Maintenance mode.

---

## Tech Stack

| Layer | Technology | Version |
|---|---|---|
| **Backend** | Python | 3.10+ |
| **Framework** | Django | 5.0.x |
| **Database** | PostgreSQL | 16 (Alpine) |
| **Containerization** | Docker + Docker Compose | 3.8 |
| **CSS Framework** | Tailwind CSS | 3.x |
| **JavaScript** | AlpineJS + HTMX | Alpine 3.14, HTMX 1.9.12 |
| **Fonts** | Google Fonts (Poppins + Inter) | CDN |
| **Static Files** | WhiteNoise (Brotli compressed) | 6.7+ |
| **Security** | django-axes, django-csp | Axes 6.4, CSP 3.8 |
| **Config** | django-environ | 0.11+ |
| **WSGI Server** | Gunicorn | 22+ |

---

## Architecture Decisions

- **Custom User Model** (`AUTH_USER_MODEL = 'users.User'`): UUID primary keys, role field, TOTP support — set before first migration.
- **Service Layer Pattern**: Each app exposes `*Service` classes that encapsulate business logic, keeping views thin and testable.
- **Repository Pattern**: Services delegate to repositories for data access, enabling clean separation of concerns.
- **Singleton Settings**: All `apps/settings` models use `pk=1` constraint with `load()` class method for global configuration.
- **Indonesian Language UI**: Page titles, labels, URL slugs, and form text use Bahasa Indonesia (e.g., `/akun/masuk/`, `/pengaturan/`, "Buat", "Hapus").
- **Tailwind + AlpineJS + HTMX**: Server-rendered Django templates enhanced with AlpineJS for client-side interactivity and HTMX for partial page updates — no heavy JS framework needed.

---

## Quality Metrics

| Metric | Value |
|---|---|
| **Total Tests** | 509 (all passing) |
| **Django Apps** | 11 custom applications |
| **URL Patterns** | 100+ endpoints across admin, CMS, and public API |
| **Models** | 30+ database models |
| **Template Files** | 100+ HTML templates |
| **Settings Modules** | 10 singleton configuration models |

---

## Project Structure

```
kabulhaden/
├── apps/                    # 11 Django applications
│   ├── users/               # Authentication & RBAC
│   ├── core/                # System utilities
│   ├── settings/            # CMS configuration
│   ├── media_manager/       # File management
│   ├── radio/               # Radio streaming engine
│   ├── broadcast/           # Broadcast lifecycle
│   ├── podcast/             # Podcast management
│   ├── news/                # Article publishing
│   ├── sponsor/             # Partners & ads
│   ├── community/           # Discussions
│   └── website/             # Public website
├── config/                  # Django settings (base/dev/prod)
├── templates/               # Global + module templates
├── static/                  # Static assets
├── utils/                   # Shared utilities, choices, mixins
├── media/                   # User uploads
├── logs/                    # Application logs
├── requirements/            # Python dependencies
├── docs/                    # Project documentation
├── docker-compose.yml       # Docker orchestration
├── Dockerfile               # Container build
└── tailwind.config.js       # Tailwind CSS configuration
```
