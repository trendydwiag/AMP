# AI_CONTEXT.md — AMP Studio (Aradhana Media Platform)
**Permanent Architecture Document**
**Last verified:** Sprint 4.0.1 — July 20, 2026

> This document is the **permanent architecture reference** for AMP Studio.
> It does NOT contain sprint progress, tech debt tracking, or project status.
> For project status, see `docs/PROJECT_STATE.md`.
> For tech debt, see `docs/architecture/TECH_DEBT.md`.
> For feature status, see `docs/architecture/feature-status.md`.

---

## Project Vision

**Kabulhaden CMS** (codename: **AMP Studio**) is a Django-based content management system built specifically for radio stations. It replaces the patchwork of disconnected tools (separate streaming systems, spreadsheet schedules, static websites) with a single unified platform.

**One platform for:** live radio stream → broadcast schedules → episodes → podcasts → news → community → sponsors → public website.

First client: **Radio Kabulhaden**.

---

## Stack

| Layer | Technology | Version |
|---|---|---|
| **Backend** | Django | 5.0.14 |
| **Language** | Python | 3.13 |
| **Database** | PostgreSQL (psycopg3) | 16 |
| **Frontend JS** | Alpine.js 3 (local) | 3.x |
| **CSS** | Tailwind CSS CDN (Play mode) | 3.x |
| **Dynamic Content** | HTMX | 1.9.10 |
| **Static Files** | WhiteNoise + Brotli | 6.7+ |
| **WSGI Server** | Gunicorn | 22+ |
| **Config** | django-environ | 0.11+ |
| **Security** | django-axes, django-csp | Axes 6.4, CSP 3.8 |
| **Audio Metadata** | mutagen | 1.47+ |

---

## Architecture

### Layer Architecture
```
Request → Django URL routing
        → View (LoginRequiredMixin + AuditLogMixin)
        → Service (business logic, transactions)
        → Repository (ORM queries)
        → Model (Django ORM)
        → PostgreSQL
```

- All business logic lives in `apps/*/services.py`
- All ORM queries live in `apps/*/repositories.py`
- Views only orchestrate — no direct ORM queries in views
- **Known exception:** `AMPStudioDashboardView` has inline queries (technical debt)

### Multi-Tenant Architecture
Every content item (Program, Article, Podcast, MediaFile) has a `FK → platform.Partner`. Middleware resolves the active partner from the request. Superusers can switch partners via the sidebar dropdown. Each partner can have custom themes, feature flags, and usage limits.

### Service-Repository Pattern
- `BaseRepository` (`utils/repositories.py`): generic CRUD operations
- `BaseService` (`utils/services.py`): transaction wrapper with `execute_in_transaction(fn)`
- App repositories extend `BaseRepository[Model]`
- App services extend `BaseService[Repository]`

---

## Folder Convention

```
apps/<app_name>/
    models.py        # Data models
    services.py      # Business logic (no direct ORM)
    repositories.py  # ORM queries only
    views.py         # Orchestration only
    urls.py          # URL patterns + namespace
    forms.py         # Django forms
    templatetags/    # Custom template tags

templates/
    amp_studio/      # All CMS Studio templates
        base.html    # THE single base template for all CMS pages
        components/  # Header, sidebar, player_bar, etc.
    broadcast/       # Broadcast CMS templates
    settings/        # Settings templates (own base.html)
    website/         # Public website templates
    users/           # Auth + user admin templates

static/
    css/amp-studio/  # AMP Studio CSS system (design-tokens, components, layout)
    js/amp-studio/   # amp-studio.js (Alpine components + theme engine)
```

### 14 Django Apps

| App | Namespace | Mount | Purpose |
|---|---|---|---|
| `users` | `users` | `/akun/` | Auth, RBAC, user management |
| `core` | `core` | `/` | Context processors, error handlers, health |
| `studio` | `studio` | `/studio/` | AMP Studio CMS hub |
| `settings` | `settings` | `/pengaturan/` | Singleton site config |
| `media_manager` | `media_manager` | `/media/` | File asset management + pipeline engine |
| `radio` | `radio` | `/radio/` | Radio engine, streaming, now-playing |
| `broadcast` | `broadcast` | `/broadcast/` | Programs, schedules, episodes |
| `podcast` | `podcast` | `/podcast/` | Podcast series and episodes |
| `news` | `news` | `/berita/` | Article publishing |
| `content` | `content` | `/konten/` | Shared tags, authors, SEO, versions |
| `community` | — | (inline in studio) | Discussions, replies |
| `sponsor` | — | (inline in studio) | Sponsors, advertisements |
| `platform` | `platform` | `/platform/` | Partner/tenant management |
| `website` | `website` | `/` | Public-facing website |

---

## Coding Rules

### Mandatory
1. **All ORM queries in repositories** — no `Model.objects.filter()` directly in views
2. **All business logic in services** — views only orchestrate
3. **UUID primary keys** — via `UUIDPrimaryKeyMixin`
4. **TimeStampedModel** — all models have `created_at`, `updated_at`
5. **Indonesian language in UI** — all labels, breadcrumbs, navigation in Bahasa Indonesia
6. **AMP Studio base template** — all CMS pages extend `amp_studio/base.html`
7. **AuditLogMixin** — all CMS write views must include audit logging
8. **LoginRequiredMixin** — all CMS views must be protected

### Forbidden
1. No direct ORM queries in views or templates
2. No hardcoded hex colors in templates — use CSS variables `var(--amp-coffee-*)`
3. No hardcoded localhost in application code — use relative URLs
4. No new base templates — use the existing `amp_studio/base.html`
5. No refactoring without approved task
6. No deleting documentation — mark `DEPRECATED` if no longer relevant
7. No committing credentials or secrets to git

### Alpine.js
- Use `Alpine.store('radio')` — not `x-data="radioPlayer()"`
- Global store `ampStudio` already exists in `amp-studio.js` — do not duplicate
- For dark mode toggle: set `data-theme` attribute AND `.dark` class on `<html>` **simultaneously**

---

## Naming Convention

| Element | Convention | Example |
|---|---|---|
| URL name (Indonesian) | snake_case Indonesia | `program_list`, `jadwal_buat` |
| Template file | lowercase_underscore | `program_list.html` |
| View class | PascalCase + suffix | `ProgramListView`, `ProgramCreateView` |
| Service class | PascalCase + Service | `ProgramService` |
| Repository class | PascalCase + Repository | `ProgramRepository` |
| Model field | snake_case | `start_time`, `is_active` |
| CSS class (AMP) | `amp-` prefix | `amp-badge`, `amp-card` |
| URL namespace | lowercase app name | `broadcast`, `radio`, `podcast` |

---

## Design System

### Color Palette — Coffee
| Token | Hex | Usage |
|---|---|---|
| coffee-50 | #FAF7F3 | Page background (light) |
| coffee-100 | #F5F0EA | Card surfaces (light) |
| coffee-200 | #E7DDD3 | Borders (light) |
| coffee-300 | #C89B6D | Accent light |
| coffee-400 | #8C5A3C | Primary action |
| coffee-500 | #6B4226 | Primary dark |
| coffee-600 | #4E2F1F | **Brand primary** |
| coffee-700 | #3A2318 | Header background |
| coffee-800 | #2B1A13 | Surface (dark mode) |
| coffee-900 | #1A0F0B | Background (dark mode) |

CSS variables: `var(--amp-coffee-600)` etc. Defined in `static/css/amp-studio/design-tokens.css`.

### Typography
- **Heading:** Poppins (CDN Google Fonts)
- **Body:** Inter (CDN Google Fonts)

### Dark Mode
- AMP Studio CSS uses selector `[data-theme="dark"]`
- Tailwind `dark:` variants require `.dark` class on `<html>`
- **BOTH must be set simultaneously** in `amp-studio.js`: `data-theme` attribute + `.dark` class
- Tailwind CDN config: `darkMode: 'class'` + coffee palette → in `templates/amp_studio/base.html`

### Tailwind Config (amp_studio/base.html)
```js
window.tailwind = {
  config: {
    darkMode: 'class',
    corePlugins: { preflight: false },
    theme: {
      extend: {
        colors: {
          coffee: { 50:'#FAF7F3', 100:'#F5F0EA', 200:'#E7DDD3', 300:'#C89B6D',
                    400:'#8C5A3C', 500:'#6B4226', 600:'#4E2F1F', 700:'#3A2318',
                    800:'#2B1A13', 900:'#1A0F0B' }
        }
      }
    }
  }
};
```

---

## Business Rules

### RBAC Roles
| Role | Level | Access |
|---|---|---|
| SUPERUSER | 4 | Everything — including platform management, partner switch |
| ADMINISTRATOR | 3 | All CMS modules, user management |
| EDITOR | 2 | Create/edit content, cannot delete users |
| VIEWER | 1 | Read-only in all modules |

### Partner Concept
- Each radio station is one `Partner`
- First partner = Kabulhaden (seeded via `init_settings` + `seed_platform`)
- Users can have membership in multiple partners
- SUPERUSER can switch partners without membership

### Settings Singleton
- All settings (`SiteSettings`, `SocialMediaSettings`, etc.) have `pk=1`
- Access via `.load()` class method
- Do NOT use `SiteSettings.objects.first()` — use `SiteSettings.load()`
- Context processor exposes all settings to all templates automatically

### Live Radio API
- Endpoint: `GET /api/v1/radio/live/`
- Response cached 20 seconds (env: `STREAM_CACHE_TTL`)
- Active provider: Icecast via ngrok (primary), Broadcastindo (fallback)
- `program` field always returns null (not yet wired to broadcast schedule)
- Frontend polling: 25 seconds (matches cache TTL)

### StreamHealth Field Names
| CORRECT | WRONG (do not use) |
|---|---|
| `provider_status` | `status` |
| `last_checked` | `checked_at` |
| `stream_bitrate` | `bitrate` |
| `stream_format` | `codec` |
| `response_time` | `listener_count` |
| `get_provider_status_display` | `get_status_display` |
| Status values: HEALTHY/DEGRADED/DOWN/TIMEOUT | healthy/degraded/down |

### Demo Seed
- Run: `python manage.py demo_seed [--reset]`
- Seeds ~340 records of real Kabulhaden data (from pitch deck)
- Must run after `python manage.py migrate`

---

## Broadcast Concept

```
Program (radio show)
  └── Schedule (broadcast schedule: day + time)
      └── BroadcastSession (broadcast instance: scheduled → live → finished)
          └── Episode (recording from session)
              └── EpisodeGuest (guest star)
  └── HostMember (permanent program host)
  └── Playlist → PlaylistItem (songs played)
```

Announcements (`Announcement`) are independent from programs — global scope.

## Podcast Concept

```
Podcast (serial/show)
  └── PodcastEpisode (episode: season/episode number, audio file)
```

Distribution links (Spotify, iTunes, Google) are at the Podcast level, not Episode.

## Media Pipeline Concept

```
MediaFileService.upload_file()
  → MediaPipelineService.process(file, context)
      → validate → extract_metadata → save → generate_waveform (stub)
      → analyze_audio (stub) → generate_preview (stub)
      → mark READY → dispatch_event
```

Stages 4–6 (waveform, analysis, preview) are stubs. Storage backends: local (active), S3/R2/MinIO (stubs).

---

## Analytics Concept

Analytics are currently **stub** — views and templates exist but data is not real. Listener data from `ListenerStatistic` is available but not aggregated into the analytics dashboard.

---

## Documentation Hierarchy

When there is a conflict between documents, follow this priority order:

1. **Actual Source Code** — the ultimate source of truth
2. **`docs/PROJECT_STATE.md`** — current project status, sprint, demo readiness
3. **`docs/architecture/TECH_DEBT.md`** — technical debt register
4. **`docs/architecture/feature-status.md`** — feature inventory with status
5. **`docs/AI_CONTEXT.md`** — this document (architecture reference)
6. **`docs/sprints/`** — roadmap and sprint planning
7. **`docs/changelog/`** — sprint changelogs

**Rule:** If documentation conflicts with code, trust the code. If documentation conflicts with PROJECT_STATE, trust PROJECT_STATE.

---

## Best Practices

1. **Read first:** AI_CONTEXT.md → PROJECT_STATE.md → roadmap → latest sprint changelog
2. **Check tech debt register** before starting any sprint
3. **Demo seed first** before screenshots or live testing
4. **Test in authenticated session** — almost all views require login
5. **Restart workflow** after code changes, check logs before screenshots
6. **Commit to GitHub** after each sprint completes
7. **Management commands** for init: `init_settings` → `seed_platform` → `demo_seed`
8. **Login demo:** `admin` / `DemoAdmin2024!` (via `create_superadmin` or `demo_seed`)

---

## DO NOT

1. **Do not edit business logic** without an approved task
2. **Do not refactor** without explicit instruction
3. **Do not create new features** without sprint planning
4. **Do not hardcode** colors, URLs, or credentials
5. **Do not duplicate** the base template — one base, `amp_studio/base.html`
6. **Do not delete** documentation — mark DEPRECATED if no longer relevant
7. **Do not commit** secrets/credentials to the repository
8. **Do not use wrong field names** in `StreamHealth` — see table above
9. **Do not poll** faster than cache TTL (20s) — wastes upstream bandwidth
10. **Do not assume** — check documentation before implementing
