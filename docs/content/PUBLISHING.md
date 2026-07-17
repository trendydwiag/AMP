# Publishing System

> Scheduled publishing, queue management, and content lifecycle.

## Overview

The Kabulhaden CMS publishing system provides:

- **Immediate publishing** — Publish content instantly
- **Scheduled publishing** — Queue content for future publication
- **Auto-publish** — Management command processes the queue
- **Publish/unpublish workflow** — Controlled content lifecycle
- **Content expiry** — Automatic removal after a date

## PublishingQueue Model

### Location

```python
# apps/content/models.py — line 243
class PublishingQueue(UUIDPrimaryKeyMixin, TimeStampedModel):
```

### Fields

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `id` | `UUIDField` | auto | Primary key |
| `created_at` | `DateTimeField` | auto | Creation timestamp |
| `updated_at` | `DateTimeField` | auto | Last update timestamp |
| `content_type` | `CharField(25)` | required | Type of content to publish |
| `content_id` | `UUIDField` | required | ID of content to publish |
| `scheduled_at` | `DateTimeField` | required | When to publish |
| `published_at` | `DateTimeField` | `None` | When it was actually published |
| `status` | `CharField(20)` | `'PENDING'` | Queue status |
| `created_by` | `FK(User)` | `None` | Who scheduled it |
| `error_message` | `TextField` | `''` | Error details on failure |
| `retry_count` | `PositiveIntegerField` | `0` | Number of retry attempts |

### Content Type Choices

```python
CONTENT_TYPE_CHOICES = [
    ('ARTICLE', 'Artikel'),
    ('PODCAST', 'Podcast'),
    ('PODCAST_EPISODE', 'Episode Podcast'),
    ('PROGRAM', 'Program'),
    ('EPISODE', 'Episode Siaran'),
    ('ANNOUNCEMENT', 'Pengumuman'),
]
```

### Queue Status Values

| Status | Description |
|--------|-------------|
| `PENDING` | Waiting to be published |
| `PUBLISHED` | Successfully published |
| `FAILED` | Publishing failed |
| `CANCELLED` | Cancelled by user |

### Ordering

```python
ordering = ['scheduled_at']
```

Items are processed in chronological order.

## Queue Service

### Service Class

```python
# apps/content/services.py — line 183
class PublishingQueueService(BaseService[PublishingQueueRepository]):
```

### Methods

| Method | Parameters | Description |
|--------|-----------|-------------|
| `schedule()` | `content_type, content_id, scheduled_at, user` | Add item to queue |
| `get_due()` | — | Get items where `scheduled_at <= now` |
| `get_pending()` | — | Get all pending items |
| `mark_published()` | `queue_id` | Mark as published |
| `mark_failed()` | `queue_id, error_message` | Mark as failed |
| `cancel()` | `queue_id` | Cancel a pending item |
| `retry()` | `queue_id` | Retry a failed item |

### Scheduling Content

```python
# Schedule an article for tomorrow at 9 AM
from apps.content.services import PublishingQueueService
from django.utils import timezone
from datetime import timedelta

service = PublishingQueueService()
tomorrow_9am = timezone.now() + timedelta(days=1)
tomorrow_9am = tomorrow_9am.replace(hour=9, minute=0, second=0, microsecond=0)

queue_item = service.schedule(
    content_type='ARTICLE',
    content_id=article.id,
    scheduled_at=tomorrow_9am,
    user=request.user,
)
```

### Processing Due Items

```python
# Get items that are due for publishing
service = PublishingQueueService()
due_items = service.get_due()

for item in due_items:
    try:
        # Publish the content
        publish_content(item.content_type, item.content_id)
        service.mark_published(item.id)
    except Exception as e:
        service.mark_failed(item.id, str(e))
```

## Scheduled Publishing

### Workflow

```
1. Content reaches APPROVED status
   │
2. User clicks "Jadwalkan" (Schedule)
   │
3. PublishingQueue entry created
   │   ├── content_type = 'ARTICLE'
   │   ├── content_id = article.id
   │   ├── scheduled_at = future datetime
   │   └── status = 'PENDING'
   │
4. Management command runs periodically
   │
5. Due items processed
   │   ├── Success → status = 'PUBLISHED'
   │   └── Failure → status = 'FAILED'
   │
6. Content appears on public website
```

### CMS Schedule View

| URL | Method | Description |
|-----|--------|-------------|
| `/konten/schedule/` | GET | List publishing queue |
| `/konten/schedule/create/` | GET/POST | Create scheduled item |
| `/konten/schedule/<uuid>/cancel/` | POST | Cancel scheduled item |

### Schedule Form Fields

```python
# apps/content/forms.py — line 88
class PublishingQueueForm(forms.ModelForm):
    class Meta:
        model = PublishingQueue
        fields = ['content_type', 'content_id', 'scheduled_at']
        widgets = {
            'scheduled_at': forms.DateTimeInput(
                attrs={'type': 'datetime-local'}
            ),
        }
```

## Auto-Publish Management Command

### Command

```bash
python manage.py publish_scheduled
```

### How It Works

1. Queries `PublishingQueue` for items where:
   - `status = 'PENDING'`
   - `scheduled_at <= timezone.now()`
2. For each due item:
   - Updates the content's status to `PUBLISHED`
   - Sets `last_published_at` timestamp
   - Marks queue item as `PUBLISHED`
3. On failure:
   - Marks queue item as `FAILED`
   - Stores error message
   - Increments retry count

### Cron Configuration

```bash
# Process queue every minute
* * * * * cd /path/to/kabulhaden && python manage.py publish_scheduled >> logs/publish.log 2>&1
```

### Systemd Timer (Alternative)

```ini
# /etc/systemd/system/kabulhaden-publish.service
[Unit]
Description=Kabulhaden CMS Scheduled Publishing
After=network.target

[Service]
Type=oneshot
User=www-data
WorkingDirectory=/path/to/kabulhaden
ExecStart=/path/to/venv/bin/python manage.py publish_scheduled
```

```ini
# /etc/systemd/system/kabulhaden-publish.timer
[Unit]
Description=Run Kabulhaden publish every minute

[Timer]
OnBootSec=60
OnUnitActiveSec=60

[Install]
WantedBy=timers.target
```

## Publish/Unpublish Workflow

### Publishing Content

Content can be published via multiple methods:

#### Method 1: Direct Publish

```
1. Content status = APPROVED
2. Click "Terbitkan" (Publish)
3. Status → PUBLISHED
4. last_published_at set
5. Version snapshot created
```

#### Method 2: Scheduled Publish

```
1. Content status = APPROVED
2. Click "Jadwalkan" (Schedule)
3. Set scheduled_at datetime
4. Queue item created with status PENDING
5. Management command processes at scheduled time
6. Status → PUBLISHED
```

#### Method 3: Workflow Action

```
1. POST to workflow endpoint with action=PUBLISH
2. Content status → PUBLISHED
3. Version snapshot created
4. Audit log updated
```

### Unpublishing Content

```
1. Content status = PUBLISHED
2. Click "Cabut Publikasi" (Unpublish)
3. Status → DRAFT
4. Version snapshot created
5. Content removed from public view
```

### CMS Workflow Endpoints

| Content Type | Endpoint | Actions |
|-------------|----------|---------|
| Article | `/berita/cms/artikel/<uuid>/workflow/` | submit, approve, reject, publish, unpublish |
| Podcast | `/podcast/cms/podcast/<uuid>/workflow/` | submit, approve, reject, publish, unpublish |
| Podcast Episode | `/podcast/cms/episode/<uuid>/workflow/` | submit, approve, reject, publish, unpublish |
| Program | `/broadcast/cms/program/<uuid>/workflow/` | submit, approve, reject, publish, unpublish |
| Broadcast Episode | `/broadcast/cms/episode/<uuid>/workflow/` | submit, approve, reject, publish, unpublish |

### CMS Publish/Unpublish Endpoints

| Content Type | Publish | Unpublish | Schedule |
|-------------|---------|-----------|----------|
| Article | `/berita/cms/artikel/<uuid>/publish/` | `/berita/cms/artikel/<uuid>/unpublish/` | `/berita/cms/artikel/<uuid>/schedule/` |

## Content Expiry

### Publish End Date

Articles support a `publish_end_date` field:

```python
# apps/news/models.py
publish_end_date = models.DateTimeField(null=True, blank=True)
```

### Expiry Behavior

When `publish_end_date` is set and the date passes:

1. Content status changes from `PUBLISHED` to `ARCHIVED`
2. Content is removed from public listings
3. Direct URL still accessible (404 or archive page)
4. Version snapshot is created

### Expiry Check

```python
# Check if article has expired
from django.utils import timezone

if article.publish_end_date and timezone.now() > article.publish_end_date:
    # Content has expired
    article.status = ContentStatus.ARCHIVED
    article.save()
```

### Management Command (Future)

```bash
# Check and archive expired content
python manage.py archive_expired
```

## Queue Dashboard

### Publishing Queue View

```
GET /konten/schedule/?status={status}
```

### Dashboard Stats

| Stat | Description |
|------|-------------|
| `pending_count` | Items waiting to be published |
| `published_count` | Successfully published items |
| `failed_count` | Failed items requiring attention |

### Queue Display

```
┌─────────────────────────────────────────────────────────────────┐
│ Jadwal Publikasi                    Filter: [▾ Semua Status]   │
├─────────────────────────────────────────────────────────────────┤
│ Statistik: ● 5 Menunggu  ● 12 Terbitkan  ● 2 Gagal            │
├─────────────────────────────────────────────────────────────────┤
│ ┌──────────┬────────────┬──────────────┬──────────┬──────────┐ │
│ │ Tipe     │ ID         │ Jadwal       │ Status   │ Aksi     │ │
│ ├──────────┼────────────┼──────────────┼──────────┼──────────┤ │
│ │ Artikel  │ #abc-123   │ 16 Jul 09:00 │ Menunggu │ [Batal]  │ │
│ │ Podcast  │ #def-456   │ 17 Jul 14:00 │ Menunggu │ [Batal]  │ │
│ │ Program  │ #ghi-789   │ 15 Jul 10:00 │ Terbitkan│    —     │ │
│ └──────────┴────────────┴──────────────┴──────────┴──────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

### Cancellation

Pending items can be cancelled:

```python
# View: PublishingQueueCancelView
# POST /konten/schedule/<uuid>/cancel/
queue.status = 'CANCELLED'
queue.save(update_fields=['status'])
```

### Retry Failed Items

Failed items can be retried:

```python
service.retry(queue_id)
# Resets status to PENDING, clears error_message, increments retry_count
```

## Retry Mechanism

### How Retry Works

```
FAILED ──retry()──▶ PENDING ──process──▶ PUBLISHED
                        │
                        └──▶ FAILED (if error again)
```

### Retry Parameters

| Parameter | Description |
|-----------|-------------|
| `retry_count` | Incremented on each retry |
| `error_message` | Cleared on retry, set on failure |

### Retry Limits

Currently no automatic retry limit. The system relies on:

1. Manual monitoring via the queue dashboard
2. Admin intervention for persistent failures
3. `retry_count` field for tracking attempts

## PublishingQueue Repository

### Repository Methods

```python
# apps/content/repos.py — line 111
class PublishingQueueRepository(BaseRepository):
    def get_pending(self):
        """Get all pending items ordered by scheduled time."""
        return self.model.objects.filter(
            status='PENDING'
        ).order_by('scheduled_at')

    def get_due(self):
        """Get items where scheduled_at <= now."""
        return self.model.objects.filter(
            status='PENDING',
            scheduled_at__lte=timezone.now(),
        ).order_by('scheduled_at')

    def get_by_content(self, content_type, content_id):
        """Get queue history for a specific content item."""
        return self.model.objects.filter(
            content_type=content_type,
            content_id=content_id,
        ).order_by('-scheduled_at')
```

## Best Practices

### Scheduling

1. **Schedule during off-peak hours** — Avoid 9 AM and 6 PM spikes
2. **Check timezone** — Scheduled times are in the site's timezone
3. **Verify content is approved** — Only APPROVED content can be scheduled
4. **Monitor the queue** — Check the dashboard daily
5. **Set up cron reliably** — Ensure the management command runs every minute

### Publishing

1. **Preview before publish** — Always preview content before going live
2. **Check SEO score** — Aim for grade B or higher before publishing
3. **Set featured image** — Required for social sharing
4. **Verify categories and tags** — Helps with content discovery
5. **Set publish_end_date** — For time-sensitive content

### Unpublishing

1. **Communicate changes** — Inform team before unpublishing popular content
2. **Check inbound links** — Other sites may link to the content
3. **Consider archiving** — Archive instead of unpublish for historical value
4. **Update related content** — Remove references to unpublished content

### Queue Management

1. **Review failed items daily** — Check error messages for patterns
2. **Cancel stale items** — Remove old pending items that are no longer relevant
3. **Monitor retry counts** — High counts indicate systemic issues
4. **Keep queue clean** — Cancel items for deleted content
