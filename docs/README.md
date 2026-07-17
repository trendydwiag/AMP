# Kabulhaden CMS — Documentation

## Project Purpose

Kabulhaden is a production-grade Django CMS for managing a radio station's digital presence. It provides:

- **Authentication & RBAC** — Custom User model, 4 roles, 2FA, session management, audit logging
- **Core Settings** — 10 singleton configuration models (Site, SEO, Email, Security, Appearance, Notification, Social Media, Content, Language, Media)
- **Media Manager** — File uploads, folders, tags, thumbnails, compression, search API
- **Radio Engine** — Multi-provider adapter pattern (AzuraCast, Icecast, RadioBOSS, Shoutcast), now-playing, listener stats, stream health, analytics
- **Broadcast Management** — 11 models for scheduling, playlists, programs, episodes
- **Podcast** — Series and episodes with metadata
- **News** — Articles, categories, tags
- **Sponsor** — Partner profiles and advertisement slots
- **Community** — Discussion threads and replies
- **Public Website** — 21 CBVs, 19 URL patterns, homepage with live radio player, sticky player, newsletter, contact form

**Tech Stack:** Django 5.0.x, PostgreSQL 16, Python 3.10, Docker, Tailwind CSS, AlpineJS, HTMX

## Documentation Structure

```
docs/
├── README.md                          ← You are here
├── 01_PRODUCT_VISION.md               ← Why this project exists
├── 02_TARGET_AUDIENCE.md              ← Who uses it
├── 03_USER_PERSONAS.md                ← Detailed user profiles
├── 04_FEATURE_BACKLOG.md              ← Feature list with status
├── 05_SITEMAP.md                      ← Page hierarchy
├── 06_USER_FLOWS.md                   ← Key user journeys
├── 07_COLOR_PALETTE.md                ← Coffee palette specification
├── 08Typography.md                    ← Poppins + Inter spec
├── 09_LAYOUT_SYSTEM.md                ← Grid, spacing, max-widths
├── 10_RESPONSIVE_GUIDE.md             ← Breakpoint behavior
├── 11_COMPONENT_LIBRARY.md            ← Reusable UI components
├── 12_DASHBOARD_LAYOUT.md             ← Admin panel layout
├── 13_NAVIGATION_SYSTEM.md            ← Sidebar, navbar, breadcrumbs
├── 14_FORM_DESIGN.md                  ← Form patterns and validation UX
├── 15_TABLE_DESIGN.md                 ← Data table patterns
├── 16_MODAL_DESIGN.md                 ← Dialog patterns
├── 17_TOAST_NOTIFICATION.md           ← Feedback messages
├── 18_LOADING_STATES.md               ← Skeletons, spinners, progress
├── 19_EMPTY_STATES.md                 ← No-data placeholders
├── 20_ERROR_PAGES.md                  ← 403, 404, 500
├── 21_ICONS_AND_ILLUSTRATIONS.md      ← Icon set, usage
├── 22_ANIMATION_GUIDE.md              ← Transitions, micro-interactions
├── 23_ACCESSIBILITY.md                ← WCAG compliance
├── 24_DARK_MODE.md                    ← Future dark theme
├── 25_TAILWIND_CONFIG.md              ← Tailwind customization reference
├── 26_ALPINEJS_PATTERNS.md            ← Alpine component patterns
├── 27_FUTURE_MOBILE_GUIDE.md          ← Mobile app considerations
├── 28_FUTURE_DESKTOP_GUIDE.md         ← Desktop app considerations
├── 29_PROJECT_STRUCTURE.md            ← Directory layout
├── 30_MODELS_DATABASE.md              ← All models, ERD, migrations
├── 31_VIEWS_URLS.md                   ← View layer, URL routing
├── 32_SERVICES_REPOSITORIES.md        ← Service-Repository pattern
├── 33_FORMS_VALIDATORS.md             ← Form classes, custom validators
├── 34_AUTH_SYSTEM.md                  ← Authentication, RBAC, 2FA
├── 35_SECURITY.md                     ← Axes, CSP, HSTS, middleware
├── 36_API_REFERENCE.md                ← JSON API endpoints
├── 37_MANAGEMENT_COMMANDS.md          ← CLI commands
├── 38_DEPLOYMENT.md                   ← Docker, production config
├── 39_TESTING.md                      ← Test strategy, coverage
├── 40_PROJECT_GLOSSARY.md             ← Terminology
├── erd.md                             ← Mermaid ERD
├── url_list.md                        ← All URL patterns
├── permission_matrix.md               ← RBAC matrix
├── test_coverage.md                   ← Test breakdown
├── folder_tree.txt                    ← Directory listing
├── future_extensions.md               ← Roadmap
└── adr/                               ← Architecture Decision Records
    ├── README.md                      ← ADR index
    ├── 0001-use-django.md
    ├── 0002-postgresql-database.md
    ├── 0003-service-repository-pattern.md
    ├── 0004-uuid-primary-keys.md
    ├── 0005-custom-user-model.md
    ├── 0006-tailwind-css.md
    ├── 0007-alpinejs-for-interactivity.md
    ├── 0008-htmx-for-dynamic-content.md
    ├── 0009-docker-containerization.md
    ├── 0010-multi-provider-radio-engine.md
    ├── 0011-singleton-settings-pattern.md
    ├── 0012-white-noise-static-files.md
    ├── 0013-axes-brute-force-protection.md
    ├── 0014-session-timeout-middleware.md
    ├── 0015-indonesian-language-ui.md
    ├── 0016-coffee-color-palette.md
    ├── 0017-poppins-inter-typography.md
    ├── 0018-website-pure-presentation.md
    ├── 0019-factory-function-settings-views.md
    └── 0020-caching-strategy.md
```

## Who Reads What

| Audience | Start Here |
|---|---|
| **New developers** | `29_PROJECT_STRUCTURE.md`, `01_PRODUCT_VISION.md`, `40_PROJECT_GLOSSARY.md` |
| **Frontend developers** | `07_COLOR_PALETTE.md` → `27_FUTURE_MOBILE_GUIDE.md` (docs 07–27) |
| **Backend developers** | `28_FUTURE_DESKTOP_GUIDE.md` → `40_PROJECT_GLOSSARY.md` (docs 28–40) |
| **Designers** | `07_COLOR_PALETTE.md`, `08Typography.md`, `09_LAYOUT_SYSTEM.md`, `11_COMPONENT_LIBRARY.md` |
| **DevOps** | `38_DEPLOYMENT.md`, `35_SECURITY.md` |
| **AI assistants** | `README.md` (this file), then all referenced docs |

## Development Workflow

```bash
# Local development
python manage.py migrate
python manage.py init_settings
python manage.py createsuperuser
python manage.py runserver 0.0.0.0:8089

# Frontend assets
npm install
npm run dev          # Tailwind watch mode
npm run build        # Production build

# Testing
python manage.py test --verbosity=2

# Docker
docker-compose up --build
```

## AI Assistant Rules

When working on this codebase, you MUST:

1. **Read this documentation first** — Every doc in `docs/` is the source of truth
2. **Never modify application code** when writing docs — documents only
3. **Follow the Service-Repository pattern** — All data access through `BaseRepository[T]` → `BaseService[R]` → Views
4. **Use Indonesian** for all user-facing strings
5. **Use UUID primary keys** on all models via `UUIDPrimaryKeyMixin`
6. **Extend `TimeStampedModel`** for automatic `created_at`/`updated_at`
7. **Use `_settings_view` factory** for settings views
8. **Website module is presentation-only** — never queries models directly, always consumes Services
9. **URL prefixes**: auth `/akun/`, settings `/pengaturan/`, media `/media/`, radio `/radio/`, broadcast `/broadcast/`, website `''` (root)
10. **Test coverage must not decrease** — run `python manage.py test --verbosity=2` after changes
