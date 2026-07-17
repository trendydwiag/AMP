# Version History and Rollback

> Content versioning, comparison, and rollback mechanisms.

## Overview

Kabulhaden CMS implements automatic content versioning to provide:

- Complete edit history for all content
- Ability to rollback to any previous version
- Audit trail for compliance and debugging
- Data safety against accidental changes

## ContentVersion Model

### Location

```python
# apps/content/models.py — line 171
class ContentVersion(UUIDPrimaryKeyMixin, TimeStampedModel):
```

### Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | `UUIDField` | Primary key |
| `created_at` | `DateTimeField` | Auto-set on creation |
| `updated_at` | `DateTimeField` | Auto-updated |
| `content_type` | `CharField(25)` | Type of content |
| `content_id` | `UUIDField` | ID of the content object |
| `version_number` | `PositiveIntegerField` | Sequential version number |
| `title` | `CharField(300)` | Content title at time of version |
| `data_snapshot` | `JSONField` | Full content snapshot |
| `change_summary` | `CharField(500)` | Description of change |
| `author` | `ForeignKey(User)` | Who made the change |
| `is_current` | `BooleanField` | Whether this is the active version |

### Content Type Choices

```python
CONTENT_TYPE_CHOICES = [
    ('ARTICLE', 'Artikel'),
    ('PODCAST', 'Podcast'),
    ('PODCAST_EPISODE', 'Episode Podcast'),
    ('PROGRAM', 'Program'),
    ('EPISODE', 'Episode Siaran'),
    ('ANNOUNCEMENT', 'Pengumuman'),
    ('DISCUSSION', 'Diskusi'),
]
```

### Unique Constraint

```python
unique_together = ['content_type', 'content_id', 'version_number']
```

Each version number is unique per content object.

## Automatic Version Creation

### When Versions Are Created

Versions are created automatically at these lifecycle points:

| Event | Trigger | Description |
|-------|---------|-------------|
| Content creation | `create_version()` | Initial version (v1) |
| Content update | `create_version()` | New version on save |
| Status change | Workflow action | Version snapshot on publish/approve |
| Rollback | `rollback_to()` | New version from old snapshot |

### Version Creation Process

```python
# apps/content/models.py — line 206
@classmethod
def create_version(cls, content_type, content_id, data, author=None, summary=''):
    # 1. Find the last version number
    last = cls.objects.filter(
        content_type=content_type, content_id=content_id
    ).order_by('-version_number').first()
    version_number = (last.version_number + 1) if last else 1

    # 2. Mark previous version as non-current
    if last:
        last.is_current = False
        last.save(update_fields=['is_current'])

    # 3. Create new version
    return cls.objects.create(
        content_type=content_type,
        content_id=content_id,
        version_number=version_number,
        data_snapshot=data,
        change_summary=summary,
        author=author,
        is_current=True,
    )
```

### Snapshot Data Structure

The `data_snapshot` field stores a JSON representation of the content:

```json
{
  "title": "Article Title",
  "slug": "article-title",
  "excerpt": "Article excerpt text...",
  "content": "<p>Full article content in HTML...</p>",
  "content_format": "RICH_TEXT",
  "status": "DRAFT",
  "featured_image": "news/articles/featured.jpg",
  "seo_title": "SEO Title",
  "seo_description": "SEO description...",
  "og_title": "OG Title",
  "og_description": "OG description...",
  "category": "category-uuid",
  "tags": ["tag-1-uuid", "tag-2-uuid"],
  "author": "author-uuid"
}
```

### Version Numbering

- Starts at `1` for new content
- Increments by `1` for each version
- Never reused, even after rollback
- Sequential per content type + content ID

## Version Service

### Service Methods

```python
# apps/content/services.py — line 148
class ContentVersionService(BaseService[ContentVersionRepository]):
    def create_version(self, content_type, content_id, data, author=None, summary=''):
        """Create a new version snapshot."""
        return ContentVersion.create_version(
            content_type=content_type,
            content_id=content_id,
            data=data,
            author=author,
            summary=summary,
        )

    def get_current(self, content_type, content_id):
        """Get the current (latest) version."""
        return self.repository.get_current(content_type, content_id)

    def get_history(self, content_type, content_id, limit=20):
        """Get version history, most recent first."""
        return self.repository.get_history(content_type, content_id, limit)

    def get_by_version(self, content_type, content_id, version_number):
        """Get a specific version by number."""
        return self.repository.get_by_version(content_type, content_id, version_number)

    def rollback_to(self, content_type, content_id, version_number, author=None):
        """Rollback content to a specific version."""
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

### Repository Methods

```python
# apps/content/repos.py — line 87
class ContentVersionRepository(BaseRepository):
    def get_current(self, content_type, content_id):
        """Get version with is_current=True."""
        return self.model.objects.filter(
            content_type=content_type,
            content_id=content_id,
            is_current=True,
        ).first()

    def get_history(self, content_type, content_id, limit=20):
        """Get ordered version history."""
        return self.model.objects.filter(
            content_type=content_type,
            content_id=content_id,
        ).order_by('-version_number')[:limit]

    def get_by_version(self, content_type, content_id, version_number):
        """Get specific version by number."""
        return self.model.objects.filter(
            content_type=content_type,
            content_id=content_id,
            version_number=version_number,
        ).first()
```

## Version Comparison

### How Comparison Works

Version comparison works by comparing `data_snapshot` fields between two versions:

1. Retrieve both versions from the database
2. Decode their `data_snapshot` JSON
3. Compare field-by-field
4. Highlight differences

### Comparison Fields

| Field | Comparison Type |
|-------|----------------|
| `title` | Text diff |
| `content` | HTML/Markdown diff |
| `excerpt` | Text diff |
| `status` | State change |
| `seo_title` | Text diff |
| `seo_description` | Text diff |
| `featured_image` | Image URL change |

### CMS Version Views

| URL | View | Description |
|-----|------|-------------|
| `/konten/versions/` | `ContentVersionListView` | List all versions |
| `/konten/versions/<uuid>/` | `ContentVersionDetailView` | View version details |

### Version List Display

```
┌─────────────────────────────────────────────────────────────┐
│ Riwayat Versi                                    Filter: [▾] │
├─────────────────────────────────────────────────────────────┤
│ ┌─────────┬──────────┬────────────┬────────────┬──────────┐ │
│ │ Versi   │ Konten   │ Ringkasan  │ Penulis    │ Tanggal  │ │
│ ├─────────┼──────────┼────────────┼────────────┼──────────┤ │
│ │ v5  ●   │ Article  │ Updated    │ admin      │ 15 Jul   │ │
│ │ v4      │ Article  │ Published  │ editor     │ 14 Jul   │ │
│ │ v3      │ Article  │ Revised    │ admin      │ 14 Jul   │ │
│ │ v2      │ Article  │ Draft      │ admin      │ 13 Jul   │ │
│ │ v1      │ Article  │ Created    │ admin      │ 12 Jul   │ │
│ └─────────┴──────────┴────────────┴────────────┴──────────┘ │
└─────────────────────────────────────────────────────────────┘
```

## Rollback Mechanism

### How Rollback Works

```
Version Timeline:
  v1 ──▶ v2 ──▶ v3 ──▶ v4 (current)
                          │
                   User selects v2
                          │
                          ▼
  v1 ──▶ v2 ──▶ v3 ──▶ v4 ──▶ v5 (new, snapshot from v2)
                                     ↑
                               is_current = True
                               v4.is_current = False
```

### Rollback Process

1. **User selects target version** (e.g., v2) from version history
2. **Service retrieves snapshot** from v2's `data_snapshot`
3. **New version (v5) is created** with v2's data
4. **v5 is marked as current** (`is_current = True`)
5. **v4 is marked as non-current** (`is_current = False`)
6. **Change summary records** the rollback: "Rollback to v2"
7. **Original content is updated** with v2's data
8. **Audit log records** the rollback action

### Rollback Safety

| Property | Description |
|----------|-------------|
| Non-destructive | Old versions are never deleted |
| Traceable | Rollback creates its own version |
| Auditable | Logged in audit trail |
| Recoverable | Can rollback to any version, including after a rollback |

### Rollback Example

```python
# Rollback article to version 3
service = ContentVersionService()
new_version = service.rollback_to(
    content_type='ARTICLE',
    content_id=article_id,
    version_number=3,
    author=request.user,
)
# Result: New version created with v3's snapshot
# change_summary = "Rollback to v3"
```

## Audit Trail

### Version-Based Audit

Every version entry provides an audit record:

| Field | Audit Value |
|-------|-------------|
| Who | `author` field (User FK) |
| When | `created_at` timestamp |
| What | `content_type` + `content_id` |
| Change | `change_summary` description |
| State | `data_snapshot` (full content state) |

### Audit Log View

The CMS provides a dedicated audit log view:

```
GET /konten/audit-log/?content_type={type}
```

```python
# apps/content/views.py — line 415
class ContentAuditLogView(LoginRequiredMixin, AuditLogMixin, ListView):
    model = ContentVersion
    template_name = 'content/audit_log.html'
    context_object_name = 'audit_entries'
    paginate_by = 50
```

### Audit Log Display

```
┌──────────────────────────────────────────────────────────────┐
│ Audit Log                                       Filter: [▾]  │
├──────────────────────────────────────────────────────────────┤
│ ┌────────────────┬──────────┬────────────┬─────────────────┐ │
│ │ Timestamp      │ Action   │ User       │ Details         │ │
│ ├────────────────┼──────────┼────────────┼─────────────────┤ │
│ │ 15 Jul 12:00   │ Create   │ admin      │ Article v1      │ │
│ │ 15 Jul 14:30   │ Update   │ admin      │ Article v2      │ │
│ │ 15 Jul 16:00   │ Publish  │ editor     │ Article v3      │ │
│ │ 16 Jul 09:00   │ Rollback │ admin      │ Article v4→v2   │ │
│ └────────────────┴──────────┴────────────┴─────────────────┘ │
└──────────────────────────────────────────────────────────────┘
```

### Security Logger

Audit events are also written to the security logger:

```python
# utils/mixins.py
security_logger.info(
    f"[AUDIT] Action: {action} | User: {username} | IP: {ip_addr} | Details: {details}"
)
```

## Querying Version History

### Common Queries

```python
from apps.content.models import ContentVersion

# Get current version
current = ContentVersion.get_current('ARTICLE', article_id)

# Get last 20 versions
history = ContentVersion.get_history('ARTICLE', article_id, limit=20)

# Get specific version
version = ContentVersion.get_by_version('ARTICLE', article_id, version_number=3)

# Get all versions for a content type
all_versions = ContentVersion.objects.filter(
    content_type='ARTICLE'
).order_by('-created_at')[:100]

# Get versions by author
my_versions = ContentVersion.objects.filter(
    author=current_user
).order_by('-created_at')

# Get versions with data snapshot
for version in history:
    print(version.data_snapshot)  # Full JSON dict
    print(version.version_number)  # Version number
    print(version.change_summary)  # Change description
```

## Best Practices

### For Content Authors

1. **Write meaningful change summaries** — Help future editors understand changes
2. **Review version history** before making major edits
3. **Use rollback cautiously** — It creates a new version, doesn't delete
4. **Check current version** before editing to avoid conflicts

### For Administrators

1. **Monitor audit logs** for unusual activity
2. **Review version counts** — High counts may indicate excessive saving
3. **Use rollback for data recovery** — Not for routine edits
4. **Set up version retention** — Consider archiving very old versions

### Version Management Tips

- Each version stores the full content snapshot (not a diff)
- Disk usage grows with version count
- Consider cleanup strategy for very old versions
- Version numbers are never reused
- `is_current` flag always points to exactly one version per content

## Database Schema

### Migration Reference

```python
# apps/content/migrations/0001_initial.py — line 125
migrations.CreateModel(
    name='ContentVersion',
    fields=[
        ('id', models.UUIDField(...)),
        ('created_at', models.DateTimeField(auto_now_add=True)),
        ('updated_at', models.DateTimeField(auto_now=True)),
        ('content_type', models.CharField(max_length=25)),
        ('content_id', models.UUIDField()),
        ('version_number', models.PositiveIntegerField(default=1)),
        ('title', models.CharField(max_length=300)),
        ('data_snapshot', models.JSONField(default=dict)),
        ('change_summary', models.CharField(max_length=500)),
        ('author', models.ForeignKey(...)),
        ('is_current', models.BooleanField(default=True)),
    ],
    options={
        'unique_together': {('content_type', 'content_id', 'version_number')},
        'ordering': ['-version_number'],
    },
)
```
