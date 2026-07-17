# AMP Studio — Current Project Map
**Generated:** Sprint 4.0 (July 17, 2026)
**Status:** Authoritative — reflects actual codebase state

---

## Project Overview

**Product:** Kabulhaden CMS / AMP Studio
**Stack:** Django 5.0.14 | Python 3.13 | PostgreSQL | Alpine.js 3 | Tailwind CDN | HTMX
**Pattern:** Service-Repository-View | Multi-Tenant (Partner) | Singleton Settings
**Deployment:** Replit (dev) + Gunicorn + WhiteNoise

---

## Project Tree (Top Level)

```
/
├── apps/               # All Django applications (14 apps)
│   ├── broadcast/      # Broadcast lifecycle management
│   ├── community/      # Community discussions
│   ├── content/        # Shared content metadata (tags, authors, SEO)
│   ├── core/           # Global utilities, context processors, error handlers
│   ├── media_manager/  # File upload and asset organization
│   ├── news/           # Article publishing
│   ├── platform/       # Multi-tenant partner engine
│   │   ├── feature_flags/  # Feature flag system
│   │   ├── partner/        # Partner management
│   │   └── themes/         # Per-partner theming
│   ├── podcast/        # Podcast series and episodes
│   ├── radio/          # Radio engine and streaming
│   ├── settings/       # Singleton site configuration
│   ├── sponsor/        # Sponsorship and advertisement management
│   ├── studio/         # AMP Studio CMS dashboard views
│   ├── users/          # Authentication, RBAC, user management
│   └── website/        # Public-facing website views
├── config/
│   ├── settings/
│   │   ├── base.py
│   │   ├── development.py
│   │   └── production.py
│   └── urls.py
├── docs/               # Documentation (Sprint 4.0: actively maintained)
│   ├── adr/            # Architecture Decision Records (26 ADRs)
│   ├── architecture/   # Architecture inventories (this sprint)
│   ├── changelog/      # Per-sprint changelogs
│   ├── sprint/         # Sprint reports
│   └── sprints/        # Next sprint planning
├── requirements/
│   ├── base.txt
│   ├── development.txt
│   └── production.txt
├── static/
│   ├── css/
│   │   ├── amp-studio/         # AMP Studio CSS system
│   │   │   ├── amp-studio.css  # Main (imports tokens, components, layout)
│   │   │   ├── design-tokens.css
│   │   │   ├── components.css
│   │   │   └── layout.css
│   │   ├── styles.css          # Compiled Tailwind (public website)
│   │   ├── dashboard.css       # Legacy dashboard styles
│   │   └── homepage.css        # Public homepage styles
│   └── js/
│       ├── alpine.min.js       # Alpine.js (served locally)
│       ├── radio-player.js     # Public website radio player
│       ├── editor.js           # Rich text editor
│       └── amp-studio/
│           └── amp-studio.js   # AMP Studio Alpine components + theme engine
├── templates/
│   ├── amp_studio/             # AMP Studio layout + all CMS page templates
│   │   ├── base.html           # THE base template for all CMS pages
│   │   ├── components/         # sidebar, header, player_bar, notifications, etc.
│   │   ├── dashboard.html
│   │   ├── streaming_center.html
│   │   ├── community.html
│   │   ├── iklan.html
│   │   ├── analytics.html
│   │   └── ...
│   ├── broadcast/              # Broadcast CMS templates (all → amp_studio/base.html)
│   ├── content/                # Content metadata CMS templates
│   ├── media_manager/          # Media manager templates
│   ├── news/                   # News/article CMS templates
│   ├── podcast/cms/            # Podcast CMS templates
│   ├── radio/                  # Radio management templates
│   ├── settings/               # Settings pages (with own sidebar via settings/base.html)
│   ├── website/                # Public website templates (own CSS/JS)
│   └── users/                  # Auth + admin user templates (→ amp_studio/base.html)
└── utils/
    ├── services.py             # BaseService (transaction wrapper)
    └── repositories.py         # BaseRepository (generic CRUD)
```

---

## Apps Inventory

| App | Namespace | Mount | Purpose |
|---|---|---|---|
| `users` | `users` | `/akun/` | Auth, RBAC, user management |
| `core` | — | `/` | Context processors, error handlers, health |
| `studio` | `studio` | `/studio/` | AMP Studio CMS hub |
| `settings` | `settings` | `/pengaturan/` | Singleton site config |
| `media_manager` | `media_manager` | `/media/` | File asset management |
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

## Dependencies

### Core Python Requirements
```
Django>=5.0.7,<5.1.0
django-axes>=6.4.0        # Brute-force protection
django-csp>=3.8           # Content Security Policy
django-environ>=0.11.2    # .env management
gunicorn>=22.0.0          # WSGI server
psycopg[binary]>=3.2.1    # PostgreSQL driver
whitenoise[brotli]>=6.7.0 # Static file serving
```

### Frontend Dependencies (CDN)
- Tailwind CSS CDN (Play mode, `darkMode: 'class'`, coffee palette registered)
- Alpine.js 3 (served locally: `static/js/alpine.min.js`)
- Alpine Collapse plugin (CDN)
- HTMX 1.9.10 (CDN)

---

## Service Layer

All business logic lives in `apps/*/services.py`. Services extend `BaseService` from `utils/services.py`.

| Module | Services |
|---|---|
| `broadcast` | ProgramService, HostService, ScheduleService, BroadcastService, EpisodeService, PlaylistService, AnnouncementService, CalendarService |
| `radio` | RadioStationService, RadioProviderService, StreamHealthService, ListenerService, NowPlayingService |
| `podcast` | PodcastService, PodcastEpisodeService |
| `news` | ArticleService, CategoryService, TagService |
| `content` | ContentTagService, AuthorService, ContentVersionService, PublishingQueueService, ContentHighlightService, SEOService |
| `media_manager` | MediaFileService, FolderService, TagService |
| `settings` | SiteSettingsService, SEOSettingsService, EmailSettingsService, SecuritySettingsService, AppearanceSettingsService, NotificationSettingsService, SocialMediaSettingsService, ContentSettingsService, LanguageSettingsService, MediaSettingsService |
| `users` | UserService, ProfileService, AuthService |
| `community` | DiscussionService, ReplyService |
| `sponsor` | PartnerService, AdvertisementService |

---

## Repository Layer

All ORM queries live in `apps/*/repositories.py`. Repositories extend `BaseRepository` from `utils/repositories.py`.

| Module | Repository | Key Query Methods |
|---|---|---|
| `broadcast` | ProgramRepository, HostRepository, ScheduleRepository, EpisodeRepository, AnnouncementRepository | active, featured, upcoming |
| `radio` | RadioStationRepository, RadioProviderRepository, StreamHealthRepository, ListenerRepository | by_station, latest_health |
| `podcast` | PodcastRepository, PodcastEpisodeRepository | published, by_partner |
| `news` | ArticleRepository, CategoryRepository, TagRepository | published, by_category |
| `media_manager` | MediaFileRepository, FolderRepository, TagRepository | by_folder, by_type |
| `settings` | All settings repositories (singleton `.load()` pattern) | load, save |
| `users` | UserRepository, ProfileRepository | by_role, by_status |
| `community` | DiscussionRepository, ReplyRepository | by_discussion |
| `sponsor` | SponsorRepository, AdvertisementRepository | active, by_tier |

---

## Broadcast Layer

**App:** `apps/broadcast`
**Models:** Program → Schedule (day+time) → BroadcastSession → Episode
**Flow:** Program is assigned to Hosts (via HostMember), linked to Schedules. Schedules generate BroadcastSessions. Sessions have Episodes with recordings. Playlists belong to Programs.

## Content Layer

**App:** `apps/content` (shared across broadcast, news, podcast)
**Models:** ContentCategory, ContentTag (M2M linked to Program/Article/Podcast), Author (O2O User), SEOModel (generic FK), ContentVersion, PublishingQueue, ContentHighlight

## Podcast Layer

**App:** `apps/podcast`
**Models:** Podcast → PodcastEpisode
**External:** Spotify, iTunes, Google Podcasts URL fields

## Analytics Layer

**Status:** ⚪ PLANNED — `apps/studio/views.py::AMPStudioAnalyticsView` exists but renders stub template. Listener stats from radio module are available but not aggregated into a full analytics dashboard.

## Authentication Layer

**App:** `apps/users`
**Roles:** SUPERUSER → ADMINISTRATOR → EDITOR → VIEWER
**Features:** TOTP 2FA, session timeout, axes brute-force, login history, password history, audit log, email verification, account locking

## Partner Layer

**App:** `apps/platform`
**Concept:** Every content item (Program, Article, Podcast, MediaFile) has a `FK → Partner`. The middleware resolves the active partner from the request. Superusers can switch partners via the sidebar dropdown. Each partner can have custom themes, feature flags, and usage limits.

---

## Public API

| Endpoint | Method | View | Description |
|---|---|---|---|
| `/api/v1/radio/live/` | GET | `LiveRadioAPIView` | Live stream status + now-playing (cached 20s) |
| `/broadcast/api/programs/` | GET | — | Public program listing |
| `/broadcast/api/schedule/` | GET | — | Current day schedule |
| `/broadcast/api/current/` | GET | — | Currently active program |
| `/broadcast/api/next/` | GET | — | Next scheduled program |
| `/broadcast/api/playlist/` | GET | — | Current playlist |
| `/radio/api/status/` | GET | — | Stream on/offline status |
| `/radio/api/now-playing/` | GET | — | Now playing song/metadata |
| `/radio/api/health/` | GET | — | Stream health check result |
| `/radio/api/player-config/` | GET | — | Player config (volume, autoplay) |
| `/health/` | GET | `health_check` | System health check |

## Internal API

| Endpoint | Purpose |
|---|---|
| `/studio/partner/switch/<uuid>/` | POST — switch active partner (SUPERUSER/ADMIN only) |
| `/akun/admin/pengguna/` | User admin CRUD |
| All `/broadcast/cms/*` | Content workflow management |
| All `/berita/cms/*` | Article workflow management |
| All `/podcast/cms/*` | Podcast workflow management |

---

## Data Flow

```
Public Website → website views → context processors → templates/website/
     ↑ radio player polls
     /api/v1/radio/live/ → LiveRadioAPIView → [cache 20s] → RadioProvider adapter
                                                              → Broadcastindo/AzuraCast/etc

CMS User → /studio/ → AMPStudioDashboardView → aggregates stats from all apps
         → /broadcast/ → BroadcastDashboardView → ProgramService → ProgramRepository → DB
         → /radio/ → RadioDashboardView → RadioStationService → RadioProviderService → DB
         → /pengaturan/ → Settings views → Singleton services → DB (pk=1)
```

---

## Routing

**Root config:** `config/urls.py`

```
/studio/        → apps.studio.urls      (namespace: studio)
/admin/         → Django admin
/akun/          → apps.users.urls       (namespace: users)
/pengaturan/    → apps.settings.urls
/media/         → apps.media_manager.urls (namespace: media_manager)
/radio/         → apps.radio.urls       (namespace: radio)
/api/v1/        → apps.radio.api_v1_urls
/broadcast/     → apps.broadcast.urls   (namespace: broadcast)
/berita/        → apps.news.urls        (namespace: news)
/podcast/       → apps.podcast.urls     (namespace: podcast)
/konten/        → apps.content.urls     (namespace: content)
/platform/      → apps.platform.urls
/              → apps.website.urls + apps.core.urls
```

---

## Background Jobs

There are no Celery or background task workers configured. All async-like operations run:
- Via **management commands** (manually or via cron)
- Via **Django request cycle** (cache-backed polling)

---

## Management Commands

| Command | App | Purpose |
|---|---|---|
| `create_superadmin` | core/users | Create initial superuser |
| `demo_seed [--reset]` | core | Seed ~340 Kabulhaden demo records |
| `repair_permissions` | users | Fix broken permission assignments |
| `reset_admin` | users | Reset admin password |
| `reset_password` | users | Reset any user's password |
| `unlock_user` | users | Unlock locked account |
| `cleanup_media` | media_manager | Remove orphaned media files |
| `compress_media` | media_manager | Compress uploaded images |
| `generate_thumbnails` | media_manager | Regenerate media thumbnails |
| `seed_platform` | platform | Seed platform/partner records |
| `init_settings` | settings | Initialize default settings records |
| `check_stream_health` | radio | Probe stream health and save result |
| `cleanup_cache` | radio | Clear radio-related cache keys |
| `refresh_listener` | radio | Update listener count from provider |
| `refresh_now_playing` | radio | Update now-playing cache |
| `refresh_radio_all` | radio | Run all radio refresh commands |

---

## Storage

- **Database:** PostgreSQL (via `psycopg[binary]`)
- **Media files:** Django `MEDIA_ROOT` (local filesystem in dev, Replit persistent storage)
- **Static files:** WhiteNoise (brotli compression in production)
- **Caching:** Django default cache (in-memory/db). No Redis configured yet (ADR-020: Planned).

## Media

Uploaded via `apps/media_manager`. Stored under `MEDIA_ROOT/`. Subdirectories: `settings/site/` (logo, favicon), `users/avatars/`, `broadcast/`, `podcast/`, `news/`, etc.

## Caching

| Key | TTL | Usage |
|---|---|---|
| `amp_v1_live_radio` | 20s (env: `STREAM_CACHE_TTL`) | Live radio API response |
| `amp_radio_health_*` | varies | Stream health check results |
| `amp_listener_count_*` | varies | Listener count |

---

## External Integrations

| Service | Type | Status | Notes |
|---|---|---|---|
| Broadcastindo (`a7.siar.us`) | Radio metadata API | ✅ Active | Primary now-playing adapter |
| AzuraCast | Radio metadata API | 🟡 Adapter exists | Not configured in dev |
| Icecast / Shoutcast / RadioBOSS | Stream providers | ⚪ Planned adapters | Multi-provider framework in place |
| SMTP (email) | Email delivery | ⚪ Configured in settings | Not verified in dev |
| Spotify / iTunes / Google Podcasts | Podcast distribution | 🟡 URL fields only | No API integration |
| GitHub | Version control | ✅ Active | `GITHUB_PAT` secret configured |
