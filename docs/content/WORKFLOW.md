# Workflow Engine

> Content lifecycle management, state machine, and approval processes.

## Status State Machine

All content types in Kabulhaden CMS follow a standard editorial workflow defined
by the `ContentStatus` choices in `utils/choices.py`.

```
                    ┌─────────────┐
                    │             │
                    ▼             │
┌─────────┐   ┌──────────┐   ┌───────────┐   ┌────────────┐   ┌───────────┐   ┌──────────┐
│  DRAFT  │──▶│ PENDING_ │──▶│ APPROVED  │──▶│ SCHEDULED  │──▶│ PUBLISHED │──▶│ ARCHIVED │
│         │   │  REVIEW  │   │           │   │            │   │           │   │          │
└─────────┘   └──────────┘   └───────────┘   └────────────┘   └───────────┘   └──────────┘
                    │                              │                │
                    │                              │                │
                    ▼                              │                │
              ┌───────────┐                        │                │
              │ REJECTED  │                        │                │
              └───────────┘                        │                │
                    │                              │                │
                    └──────────▶ DRAFT ◀───────────┘                │
                                                    │               │
                                                    └──▶ DRAFT ◀───┘
```

## ContentStatus Choices

Defined in `utils/choices.py`:

```python
class ContentStatus(models.TextChoices):
    DRAFT = 'DRAFT', 'Draft'
    PENDING_REVIEW = 'PENDING_REVIEW', 'Menunggu Review'
    APPROVED = 'APPROVED', 'Disetujui'
    SCHEDULED = 'SCHEDULED', 'Terjadwal'
    PUBLISHED = 'PUBLISHED', 'Diterbitkan'
    ARCHIVED = 'ARCHIVED', 'Diarsipkan'
    REJECTED = 'REJECTED', 'Ditolak'
```

## Valid Transitions

### From DRAFT

| Action | Target State | Description |
|--------|-------------|-------------|
| Submit for Review | `PENDING_REVIEW` | Content sent to editor |
| Save as Draft | `DRAFT` | Continue editing (no state change) |

### From PENDING_REVIEW

| Action | Target State | Description |
|--------|-------------|-------------|
| Approve | `APPROVED` | Editor approves content |
| Reject | `REJECTED` | Editor rejects with feedback |

### From APPROVED

| Action | Target State | Description |
|--------|-------------|-------------|
| Publish Now | `PUBLISHED` | Immediately publish |
| Schedule | `SCHEDULED` | Queue for future publish |
| Reject | `REJECTED` | Revoke approval |

### From SCHEDULED

| Action | Target State | Description |
|--------|-------------|-------------|
| Auto-Publish | `PUBLISHED` | System publishes at scheduled time |
| Cancel Schedule | `APPROVED` | Return to approved state |
| Unpublish | `DRAFT` | Withdraw from queue |

### From PUBLISHED

| Action | Target State | Description |
|--------|-------------|-------------|
| Unpublish | `DRAFT` | Remove from public view |
| Archive | `ARCHIVED` | Archive for historical record |

### From ARCHIVED

| Action | Target State | Description |
|--------|-------------|-------------|
| Restore | `DRAFT` | Restore to draft state |

### From REJECTED

| Action | Target State | Description |
|--------|-------------|-------------|
| Revise | `DRAFT` | Return to editing |

## WorkflowAction Choices

Defined in `utils/choices.py`:

```python
class WorkflowAction(models.TextChoices):
    SUBMIT_REVIEW = 'SUBMIT_REVIEW', 'Kirim ke Review'
    APPROVE = 'APPROVE', 'Setujui'
    REJECT = 'REJECT', 'Tolak'
    PUBLISH = 'PUBLISH', 'Terbitkan'
    UNPUBLISH = 'UNPUBLISH', 'Cabut Publikasi'
    ARCHIVE = 'ARCHIVE', 'Arsipkan'
    RESTORE = 'RESTORE', 'Pulihkan'
    SCHEDULE = 'SCHEDULE', 'Jadwalkan'
```

## Approval Flow

### Step-by-Step

1. **Author creates content** → Status starts as `DRAFT`
2. **Author submits for review** → Status changes to `PENDING_REVIEW`
3. **Editor reviews content** → Either `APPROVED` or `REJECTED`
4. **If approved** → Content can be published immediately or scheduled
5. **If rejected** → Author revises and resubmits (back to `DRAFT`)

### Per-Content-Type Views

Each content type has dedicated workflow views:

- **Articles:** `ArticleCMSWorkflowView` at `/berita/cms/artikel/<uuid>/workflow/`
- **Podcasts:** `PodcastCMSWorkflowView` at `/podcast/cms/podcast/<uuid>/workflow/`
- **Podcast Episodes:** `PodcastEpisodeCMSWorkflowView` at `/podcast/cms/episode/<uuid>/workflow/`
- **Programs:** `ProgramCMSWorkflowView` at `/broadcast/cms/program/<uuid>/workflow/`
- **Broadcast Episodes:** `BroadcastEpisodeCMSWorkflowView` at `/broadcast/cms/episode/<uuid>/workflow/`

### Workflow View Pattern

```python
# Each workflow view:
# 1. Receives POST with 'action' field matching WorkflowAction choices
# 2. Validates the transition is allowed from current state
# 3. Updates status field
# 4. Creates a ContentVersion snapshot
# 5. Logs the action via AuditLogMixin
# 6. Returns redirect with success message
```

## Scheduled Publishing

### Mechanism

Scheduled publishing uses the `PublishingQueue` model:

1. Content with status `APPROVED` can be scheduled
2. A `PublishingQueue` entry is created with `scheduled_at` datetime
3. A management command (`publish_scheduled`) runs periodically
4. Due items are processed: status → `PUBLISHED`, queue → `PUBLISHED`
5. Failed items are marked `FAILED` with error details

### PublishingQueue States

```
PENDING ──▶ PUBLISHED  (success)
    │
    ├──▶ FAILED  (error during publish)
    │       │
    │       └──▶ PENDING  (retry)
    │
    └──▶ CANCELLED  (user cancelled)
```

### Management Command

```bash
# Process due items in the publishing queue
python manage.py publish_scheduled

# Recommended: Run via cron every minute
* * * * * cd /path/to/project && python manage.py publish_scheduled
```

### Queue Service Methods

From `apps.content.services.PublishingQueueService`:

- `schedule(content_type, content_id, scheduled_at, user)` — Add to queue
- `get_due()` — Get items where `scheduled_at <= now`
- `get_pending()` — Get all pending items
- `mark_published(queue_id)` — Mark as published
- `mark_failed(queue_id, error_message)` — Mark as failed
- `cancel(queue_id)` — Cancel a pending item
- `retry(queue_id)` — Retry a failed item

## Rollback Mechanism

Content rollback uses the `ContentVersion` model:

### How Rollback Works

1. User selects a version number to rollback to
2. `ContentVersionService.rollback_to()` is called
3. The target version's `data_snapshot` is retrieved
4. A new version is created with the old snapshot data
5. The new version is marked as `is_current`
6. Original content record is updated with snapshot data

### Rollback API

```python
# apps/content/services.py — line 170
def rollback_to(self, content_type, content_id, version_number, author=None):
    version = self.get_by_version(content_type, content_id, version_number)
    if not version:
        return None
    return self.create_version(
        content_type=content_type,
        content_id=content_id,
        data=version.data_snapshot,
        author=author,
        summary=f"Rollback to v{version_number}",
    )
```

### Rollback Safety

- A rollback itself creates a new version (never destructive)
- Original versions are never deleted
- Rollback is logged in the audit trail
- The `change_summary` records which version was rolled back to

## Version History Tracking

### Automatic Version Creation

Versions are created automatically when:

1. Content is created (version 1)
2. Content is updated via CMS workflow
3. Content status changes (publish, unpublish, etc.)
4. Rollback is performed

### Version Snapshot Structure

```json
{
  "title": "Article Title",
  "content": "<p>Article body HTML...</p>",
  "status": "DRAFT",
  "excerpt": "...",
  "seo_title": "...",
  "seo_description": "..."
}
```

### Querying History

```python
# Get current version
ContentVersion.get_current('ARTICLE', article_id)

# Get last 20 versions
ContentVersion.get_history('ARTICLE', article_id, limit=20)

# Get specific version
ContentVersion.get_by_version('ARTICLE', article_id, version_number=3)
```

## Priority Levels

Content priority affects editorial queue ordering:

```python
class ContentPriority(models.TextChoices):
    LOW = 'LOW', 'Rendah'
    NORMAL = 'NORMAL', 'Normal'
    HIGH = 'HIGH', 'Tinggi'
    URGENT = 'URGENT', 'Mendesak'
```

Priority is available on Article, Podcast, and Program models.

## Audit Trail

Every workflow action is logged via `AuditLogMixin`:

```python
# From apps/content/views.py
self.log_action(
    request.user,
    'CONTENT_CATEGORY_CREATE',
    f"Created category: {form.instance.name}"
)
```

### Audit Action Types for Content

| Action | Description |
|--------|-------------|
| `CONTENT_CATEGORY_CREATE` | Category created |
| `CONTENT_CATEGORY_UPDATE` | Category updated |
| `CONTENT_CATEGORY_DELETE` | Category deleted |
| `CONTENT_TAG_CREATE` | Tag created |
| `CONTENT_TAG_UPDATE` | Tag updated |
| `CONTENT_TAG_DELETE` | Tag deleted |
| `CONTENT_AUTHOR_CREATE` | Author created |
| `CONTENT_AUTHOR_UPDATE` | Author updated |
| `CONTENT_AUTHOR_DELETE` | Author deleted |
| `CONTENT_SEO_CREATE` | SEO entry created |
| `CONTENT_SEO_UPDATE` | SEO entry updated |
| `CONTENT_SCHEDULE` | Content scheduled for publish |
| `CONTENT_UNSCHEDULE` | Schedule cancelled |
| `CONTENT_HIGHLIGHT_CREATE` | Highlight created |
| `CONTENT_HIGHLIGHT_UPDATE` | Highlight updated |
| `CONTENT_HIGHLIGHT_DELETE` | Highlight deleted |

### Security Logging

Audit entries are written to the `security` logger:

```python
# utils/mixins.py
security_logger.info(
    f"[AUDIT] Action: {action} | User: {username} | IP: {ip_addr} | Details: {details}"
)
```
