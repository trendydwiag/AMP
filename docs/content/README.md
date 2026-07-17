# Kabulhaden CMS Content Platform

> Comprehensive documentation for the Content Management System.

## Architecture Overview

Kabulhaden CMS follows the **Service-Repository Pattern**, a layered architecture
that separates business logic from data access and presentation concerns.

### Layer Diagram

```
┌─────────────────────────────────────────────────────┐
│                    Views (CBV)                       │
│  LoginRequiredMixin + AuditLogMixin                 │
├─────────────────────────────────────────────────────┤
│                  Services Layer                      │
│  BaseService[R] — Business logic, transactions      │
├─────────────────────────────────────────────────────┤
│                Repository Layer                      │
│  BaseRepository[T] — Django ORM encapsulation       │
├─────────────────────────────────────────────────────┤
│                   Models (ORM)                       │
│  UUID PK, TimeStamped, Django models               │
└─────────────────────────────────────────────────────┘
```

### Key Design Decisions

- **UUID v4 primary keys** on all models (`UUIDPrimaryKeyMixin`)
- **Auto timestamps** via `TimeStampedModel` (`created_at`, `updated_at`)
- **Generic type parameters** on BaseService and BaseRepository for type safety
- **Audit logging** via `AuditLogMixin` on all write views
- **Login required** on every CMS endpoint

## Content Models

### Primary Content Types

| Model | App | Description |
|-------|-----|-------------|
| `Article` | `apps.news` | News articles with rich text, Markdown, or HTML content |
| `Podcast` | `apps.podcast` | Podcast series (container for episodes) |
| `PodcastEpisode` | `apps.podcast` | Individual podcast episodes with audio files |
| `Program` | `apps.broadcast` | Broadcast/radio program definitions |
| `Episode` | `apps.broadcast` | Broadcast episodes tied to a Program |

### Shared Infrastructure

| Model | App | Description |
|-------|-----|-------------|
| `ContentCategory` | `apps.content` | Hierarchical categories scoped by content type |
| `ContentTag` | `apps.content` | Tags with usage counts, shared across content types |
| `Author` | `apps.content` | Author profiles linked optionally to User accounts |
| `SEOModel` | `apps.content` | Generic SEO metadata via Django ContentType framework |
| `ContentVersion` | `apps.content` | Version snapshots for rollback and audit |
| `PublishingQueue` | `apps.content` | Scheduled publish/unpublish queue |
| `ContentHighlight` | `apps.content` | Homepage highlights (hero, featured, trending, etc.) |

## Workflow States

Content follows a standard editorial workflow:

```
DRAFT → PENDING_REVIEW → APPROVED → SCHEDULED → PUBLISHED → ARCHIVED
                                    ↓
                                 REJECTED
```

### State Definitions

| State | Description |
|-------|-------------|
| `DRAFT` | Initial state. Content is being written/edited. |
| `PENDING_REVIEW` | Submitted for editorial review. |
| `APPROVED` | Approved by editor/manager. Ready to publish. |
| `SCHEDULED` | Queued for future publication via `PublishingQueue`. |
| `PUBLISHED` | Live on the public website. |
| `ARCHIVED` | Removed from public view but retained. |
| `REJECTED` | Rejected during review. Returns to editing. |

### Workflow Actions

| Action | From → To |
|--------|-----------|
| Submit for Review | DRAFT → PENDING_REVIEW |
| Approve | PENDING_REVIEW → APPROVED |
| Reject | PENDING_REVIEW → REJECTED |
| Schedule | APPROVED → SCHEDULED |
| Publish | APPROVED/SCHEDULED → PUBLISHED |
| Unpublish | PUBLISHED → DRAFT |
| Archive | PUBLISHED → ARCHIVED |
| Restore | ARCHIVED → DRAFT |

## URL Structure

| Prefix | App | Description |
|--------|-----|-------------|
| `/berita/cms/` | `apps.news` | News article CMS management |
| `/podcast/cms/` | `apps.podcast` | Podcast and episode CMS |
| `/broadcast/cms/` | `apps.broadcast` | Broadcast program/episode CMS |
| `/konten/` | `apps.content` | Shared content infrastructure |
| `/konten/categories/` | `apps.content` | Category management |
| `/konten/tags/` | `apps.content` | Tag management |
| `/konten/authors/` | `apps.content` | Author management |
| `/konten/seo/` | `apps.content` | SEO metadata management |
| `/konten/versions/` | `apps.content` | Version history |
| `/konten/schedule/` | `apps.content` | Publishing queue |
| `/konten/highlights/` | `apps.content` | Content highlights |
| `/konten/search/` | `apps.content` | Global search |
| `/konten/audit-log/` | `apps.content` | Audit trail |

## Template Hierarchy

```
base.html
└── dashboard_base.html
    ├── dashboard/home.html
    ├── content/dashboard.html
    ├── content/category_list.html
    ├── content/tag_list.html
    ├── content/author_*.html
    ├── content/seo_*.html
    ├── content/version_*.html
    ├── content/publishing_queue*.html
    ├── content/highlight_*.html
    ├── content/audit_log.html
    ├── content/search_results.html
    ├── news/cms/article_*.html
    ├── podcast/cms/podcast_*.html
    ├── podcast/cms/episode_*.html
    ├── broadcast/cms/program_*.html
    └── broadcast/cms/episode_*.html
```

### Shared Components

- `dashboard/components/sidebar_menu.html` — Full sidebar navigation
- `dashboard/components/sidebar_collapsed.html` — Icon-only sidebar
- `dashboard/components/quick_actions.html` — Mobile FAB quick actions

## API Preparation Notes

The current architecture is designed with future REST API support in mind:

- **Service layer** is HTTP-agnostic and can be consumed by API views
- **Repository layer** provides a clean data access interface
- **ContentVersion** creates automatic snapshots for API consistency
- **PublishingQueue** supports headless scheduled publishing

### Planned API Prefixes

- `/api/v1/news/` — Article endpoints
- `/api/v1/podcast/` — Podcast and episode endpoints
- `/api/v1/broadcast/` — Program and broadcast endpoints
- `/api/v1/content/` — Shared infrastructure endpoints

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Backend | Django 5.0.9 |
| Frontend | Tailwind CSS, Alpine.js, HTMX |
| Database | SQLite (dev) / PostgreSQL (prod) |
| Editor | Toast UI Editor (rich text) |
| Primary Keys | UUID v4 |
| Design System | Coffee color palette |

## Directory Structure

```
apps/
├── content/          # Shared content infrastructure
│   ├── models.py     # ContentCategory, Tag, Author, SEO, Version, Queue, Highlight
│   ├── services.py   # Business logic layer
│   ├── repos.py      # Repository layer
│   ├── views.py      # CMS views
│   ├── forms.py      # Django forms
│   └── urls.py       # URL routing
├── news/             # Article management
├── podcast/          # Podcast management
├── broadcast/        # Broadcast management
└── ...
```

## See Also

- [Content Models](CONTENT_MODELS.md) — Detailed field documentation
- [Workflow](WORKFLOW.md) — State machine and transitions
- [Editor Guide](EDITOR_GUIDE.md) — Rich text editor usage
- [SEO](SEO.md) — SEO module reference
- [Search](SEARCH.md) — Search functionality
- [Versioning](VERSIONING.md) — Version history and rollback
- [Publishing](PUBLISHING.md) — Publishing system
- [CMS Templates](CMS_TEMPLATES.md) — Template documentation
- [API Reference](API_REFERENCE.md) — API preparation docs
