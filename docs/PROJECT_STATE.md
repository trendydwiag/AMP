# PROJECT_STATE.md — AMP Studio
**Source of Truth for Project Status**
**Last Updated:** Sprint 4.5 — July 20, 2026

> This document is the **authoritative source of truth** for AMP Studio's current state.
> For architecture reference, see `docs/AI_CONTEXT.md`.
> For technical debt, see `docs/architecture/TECH_DEBT.md`.
> For feature inventory, see `docs/architecture/feature-status.md`.

---

## Current Version

**AMP Studio v0.4.6** (after Sprint 4.4.2 Demo Freeze & UI Consistency)

---

## 🔒 DEMO LOCK ACTIVE

**Frozen commit:** `34e4db68f9e582471d9abdfb3e0547d8fcade4cf`  
**Frozen at:** July 21, 2026 — for 18:00 WIB client demo  
**Score:** 98 / 100 — 0 critical blockers  
See: `docs/changelog/sprint-4.5-demo-freeze.md`

---

## Current Sprint

**Sprint 4.5 — Demo Readiness Verification & End-to-End Acceptance**

- Type: QA / Demo Lock
- Objective: Full verification audit, button white-on-white fixes, demo readiness confirmation
- Status: ✅ DONE — 🔒 FROZEN
- Result: 98/100 demo readiness — 0 critical blockers, 32+ routes OK, all CRUD flows verified

---

## Completed Sprints

| Sprint | Title | Type | Date | Status |
|---|---|---|---|---|
| 1.x | Project Setup & Foundation | Backend | — | ✅ DONE |
| 2.x | Core modules (users, settings, media) | Backend | — | ✅ DONE |
| 3.0–3.3 | Broadcast, Radio, Podcast, News, Content | Backend | — | ✅ DONE |
| 3.4 | Live Radio Engine (multi-provider, now-playing API) | Backend | July 2026 | ✅ DONE |
| 3.4D | Streaming integration + now-playing cache | Backend + Frontend | July 17, 2026 | ✅ DONE |
| 3.5 | Founder Experience (wizard, tour, dark mode, health widget) | Frontend | July 17, 2026 | ✅ DONE |
| 3.6 | Platform UI Consistency (amp_studio/base migration, breadcrumbs) | Frontend | July 17, 2026 | ✅ DONE |
| 3.6+ | Logo/footer DB integration, contact fields, social media icons | Frontend | July 17, 2026 | ✅ DONE |
| 3.7 | UX/Visual regressions (dark mode .dark class, streaming 500) | Bug Fix | July 17, 2026 | ✅ DONE |
| 4.0 | Knowledge Base Refresh & Project Reindex | Documentation | July 17, 2026 | ✅ DONE |
| 4.1 | Demo Readiness & Founder Experience | Frontend Polish | July 17, 2026 | ✅ DONE |
| 4.2 | Media Pipeline Engine | Backend Architecture | July 17, 2026 | ✅ DONE |
| 4.3 | Radio Live Player Stabilization | Bug Fix | July 20, 2026 | ✅ DONE |
| 4.0.1 | Knowledge Base Governance & Documentation Sync | Documentation | July 20, 2026 | ✅ DONE |
| 4.4 | Live Broadcast Intelligence (TD-001) | Backend + Frontend | July 20, 2026 | ✅ DONE |
| 4.4.1B | Production Audit (67 URLs; 5 bugs fixed) | QA + Bug Fix | July 20, 2026 | ✅ DONE |
| 4.5 | Demo Freeze Validation (93/100; 4 bugs fixed) | QA + Bug Fix | July 20, 2026 | ✅ DONE |
| 4.4.2 | Demo Freeze & UI Consistency (97/100; playlist CRUD, real calendar, dark mode) | Polish | July 20, 2026 | ✅ DONE |
| 4.5 | Demo Readiness Verification & End-to-End Acceptance (98/100; button fixes, full route audit) | QA + Demo Lock | July 21, 2026 | ✅ DONE |

---

## Current Demo Status

**Target Demo:** Radio Kabulhaden — July 21, 2026 pukul 18:00
**Demo Environment:** Replit (port 5000)
**Settings Module:** `config.settings.development`
**Last Verified:** Sprint 4.5 — July 21, 2026

### Demo Ready: YES ✅

**Score: 98/100. 0 critical blockers.**

Semua 32+ route utama HTTP 200. Semua CRUD flow berfungsi. Semua 4 role auth OK. Public website penuh tanpa error. Live radio API lengkap. Button white-on-white sudah diperbaiki (Sprint 4.5).

**Untuk demo terbaik:** Jalankan pada jam 18:00 WIB — schedule CadasPersada (TUE 18:00–19:00) akan aktif dan `current_program` akan tampil.

---

## Working Features

### Authentication & User Management
- Custom User Model (UUID PK, 4 RBAC roles)
- Login with Brute-Force Protection (django-axes, 5 attempts / 15 min)
- User Registration, Email Verification, Password Reset
- Two-Factor Authentication (TOTP)
- User Profile, Session Timeout, Audit Logging
- Admin User CRUD (`/akun/admin/pengguna/`)

### AMP Studio CMS Hub
- Dashboard with aggregated stats
- Dark Mode Toggle (data-theme + .dark class)
- Sidebar Navigation (collapsible, role-filtered)
- Command Palette (Ctrl+K)
- Notification Panel
- Radio Player Bar (Alpine.store('radio'))
- Setup Wizard (5 steps)
- Guided Tour (localStorage)
- Health Widget (stream health in header)
- Partner Switcher Dropdown
- Calendar View
- Media Explorer
- Streaming Center
- Community Hub
- Iklan/Sponsor Hub

### Broadcast Management
- Program CRUD, Host CRUD, Schedule CRUD
- Broadcast Sessions, Episodes, Guest Stars
- Playlist + Items (drag-reorder)
- Announcements, Calendar View
- CMS Workflow (program/episode review/publish)
- Public APIs (programs, schedule, current, next, playlist)

### Radio Engine
- Multi-Provider Framework (5 adapters: Broadcastindo, AzuraCast, Icecast, Shoutcast, RadioBoss)
- Live Radio API (`/api/v1/radio/live/`) — normalized, provider-agnostic, cached 20s
- Program resolution from broadcast schedule (`CurrentProgramResolver` service)
- DB-first provider resolution with settings fallback
- Direct stream URL (bypasses Replit proxy)
- Stream Health Monitoring, Listener Statistics
- Station CRUD, Provider CRUD
- Analytics View, CSV/Excel Export
- Media Inspector (`/media/inspector/`)

### Media Manager
- File Upload with Pipeline Engine (8 stages, stages 4-6 are stubs)
- Storage Abstraction (local active, S3/R2/MinIO stubs)
- Event System (6 events, pub/sub dispatcher)
- Folder Organization, Tag System
- Media Inspector with pipeline status

### Podcast
- Podcast Series CRUD, Episode CRUD
- Season/Episode Numbering
- External Platform Links (Spotify, iTunes, Google Podcasts)

### News
- Article CRUD, Draft/Published Workflow
- Article Scheduling, View Count, SEO per Article
- Autosave (HTMX), Related Articles

### Content Management
- Content Tags, Authors, SEO Model
- Content Versions, Publishing Queue
- Content Highlights

### Settings
- 10 Singleton Configuration Models (Site, SEO, Email, Security, Appearance, Notification, Social Media, Content, Language, Media)
- Settings Sidebar Navigation

### Platform / Multi-Tenant
- Partner Model with tiers, branding, limits
- Partner Membership, Domain Resolution
- Partner Invitation System
- Feature Flags (per-partner override)
- Per-Partner Theme Engine

### Public Website
- Homepage with live radio player
- Program Listing, Broadcast Schedule
- Podcast Listing, News Feed
- Community Forum, Partner/Sponsor Pages
- Contact, Newsletter, Search
- Privacy/Terms, Maintenance Mode
- Offline Page (PWA)

---

## Resolved Technical Debt

| ID | Issue | Resolved In | Resolution |
|---|---|---|---|
| TD-002 | No Fallback Stream URL | Sprint 4.3 | `listen_url_fallback` from DB provider, used in try/except |
| TD-001 | `program` field always null | — | **STILL OPEN** (not resolved) |

---

## Open Technical Debt

| ID | Issue | Priority | Status | Evidence |
|---|---|---|---|---|
| TD-001 | `program` field always null in live API | 🔴 HIGH | **OPEN** | `apps/radio/views.py:543`: `'program': None` hardcoded |
| TD-003 | No automated tests for LiveRadioAPIView | 🟡 MEDIUM | **OPEN** | No test file found in `apps/radio/tests/` |
| TD-004 | BroadcastindoAdapter makes 2 HTTP calls per cache miss | ⚪ LOW | **OPEN** | `broadcastindo.py`: `get_now_playing()` and `get_listener_count()` both call `_fetch_nowplaying_data()` |
| TD-005 | Hardcoded polling intervals in JS | ⚪ LOW | **OPEN** | `radio-player.js`, `amp-studio.js`, `streaming_center.html` have hardcoded intervals |
| TD-006 | Platform app has pending unapplied migrations | 🟡 MEDIUM | **OPEN** | `python manage.py showmigrations` shows pending |
| TD-007 | No superuser account in dev environment | 🔴 HIGH | **OPEN** | Must run `demo_seed` or `create_superadmin` first |
| TD-008 | ngrok URL must be updated manually per restart | 🟡 MEDIUM | **OPEN** | By design for free-tier ngrok |
| NEW | AMPStudioDashboardView has ~25+ inline ORM queries | 🔴 HIGH | **OPEN** | `apps/studio/views.py:12-334` — violates Service-Repository pattern |
| NEW | `admin` user (ADMINISTRATOR) gets `is_superuser=True` in demo_seed | 🟡 MEDIUM | **OPEN** | `apps/core/management/commands/demo_seed.py` |
| NEW | CSP settings defined but not active | 🟡 MEDIUM | **OPEN** | `django-csp` not in INSTALLED_APPS or MIDDLEWARE |
| NEW | `content/repos.py` uses non-standard filename | ⚪ LOW | **OPEN** | Should be `repositories.py` per project convention |
| NEW | pyproject.toml drift with requirements/base.txt | ⚪ LOW | **OPEN** | Different deps, different mutagen version pin |

---

## Current Stream Provider

| Setting | Value |
|---|---|
| Active Provider | Icecast (via ngrok tunnel) |
| Provider Type | `ICECAST` |
| Primary Adapter | `IcecastAdapter` |
| Fallback Adapter | `BroadcastindoAdapter` (temporary, Siar.us) |
| All Registered Adapters | BROADCASTINDO, AZURACAST, ICECAST, SHOUTCAST, RADIOBOSS |
| Stream URL | Dynamic (ngrok URL changes per restart) |
| Metadata URL | Dynamic (ngrok URL + `/status-json.xsl`) |
| Cache TTL | 20 seconds |
| ngrok Header Fix | ✅ `ngrok-skip-browser-warning: true` in `base.py` |

---

## Current Authentication

| Feature | Status |
|---|---|
| Custom User Model | ✅ UUID PK, 4 RBAC roles |
| Authentication Backend | django-axes + ModelBackend |
| Login URL | `/akun/masuk/` |
| Login Redirect | `/studio/` |
| Brute Force Protection | ✅ 5 attempts / 15 min lockout |
| Session Timeout | 60 minutes |
| Password Policy | 12 char min, history enforcement |
| 2FA (TOTP) | ✅ RFC 6238 |
| Account Lock/Unlock | ✅ Time-based + admin manual |

---

## Current Demo Credentials

| Username | Password | Role | is_staff | is_superuser |
|---|---|---|---|---|
| `superadmin` | `DemoAdmin2024!` | SUPERUSER | True | True |
| `admin` | `DemoAdmin2024!` | ADMINISTRATOR | True | True |
| `editor` | `DemoEditor2024!` | EDITOR | False | False |
| `viewer` | `DemoViewer2024!` | VIEWER | False | False |

**Note:** The `admin` user is incorrectly created with `is_superuser=True` in `demo_seed.py`. This gives unintended Django admin access beyond the ADMINISTRATOR role.

---

## Current Partner

| Field | Value |
|---|---|
| Name | Kabulhaden Online |
| Slug | `kabulhaden-online` |
| Tier | ENTERPRISE |
| Status | ACTIVE |
| Owner | superadmin user |
| Timezone | Asia/Jakarta |
| Language | id |

---

## Current Build Status

| Item | Status |
|---|---|
| Python | 3.13 |
| Django | 5.0.14 |
| Database | SQLite (dev default), PostgreSQL (production) |
| Migrations | Applied for all apps (platform has pending — TD-006) |
| Static Files | WhiteNoise + Brotli |
| Dev Server | Gunicorn on port 5000 |
| Deployment | Replit |

---

## Demo Readiness

See `docs/reports/documentation-audit.md` for the full feature-by-feature demo readiness checklist.

**Overall: ✅ DEMO READY** — All core modules functional. Live radio player produces audio. Known limitations documented (TD-001: program field null).

---

## Known Remaining Issues Before Demo

1. **TD-001:** `program` field in live API always null — shows "Tidak ada program" on dashboard
2. **TD-007:** No superuser in fresh dev DB — must run `demo_seed` or `create_superadmin`
3. **TD-008:** ngrok URL changes on tunnel restart — must update DB manually
4. **Network:** `a7.siar.us` unreachable from some environments — graceful offline fallback handles this

---

## Last Updated

**Sprint 4.0.1** — July 20, 2026
**Updated by:** AI Documentation Audit
