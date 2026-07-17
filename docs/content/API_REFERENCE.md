# API Reference

> Current service layer API, repository pattern, and planned REST endpoints.

## Architecture Overview

The Kabulhaden CMS uses a **Service-Repository** pattern that naturally supports API
extraction. Business logic is HTTP-agnostic, enabling both web views and REST APIs
to share the same service layer.

```
┌──────────────────┐     ┌──────────────────┐
│   Web Views (CBV)│     │  REST API (planned)│
├──────────────────┤     ├──────────────────┤
│                  │     │                  │
│  Services Layer  │◄────┤  Services Layer  │
│  (shared)        │     │  (shared)        │
├──────────────────┤     ├──────────────────┤
│  Repositories    │     │  Repositories    │
│  (shared)        │◄────┤  (shared)        │
├──────────────────┤     ├──────────────────┤
│  Django ORM      │     │  Django ORM      │
└──────────────────┘     └──────────────────┘
```

## Current Service Layer API

### ContentCategoryService

```python
# apps/content/services.py
class ContentCategoryService(BaseService[ContentCategoryRepository]):
    get_active(content_type=None)     # QuerySet of active categories
    get_roots(content_type=None)      # Top-level categories
    get_children(parent_id)           # Child categories
    search(query, content_type=None)  # Search by name/description
    create_category(data: dict)       # Create new category (atomic)
    update_category(category_id, data)# Update existing category (atomic)
    toggle_active(category_id)        # Toggle active flag
    reorder(category_ids: list)       # Reorder display_order
```

### ContentTagService

```python
class ContentTagService(BaseService[ContentTagRepository]):
    get_popular(limit=20)    # Most-used tags
    search(query)            # Search by name
    get_or_create(name)      # Get existing or create new
    bulk_create(names: list) # Batch tag creation
    increment_usage(tag_id)  # Increment usage_count (F-expression)
```

### AuthorService

```python
class AuthorService(BaseService[AuthorRepository]):
    get_active()              # Active authors
    get_by_user(user_id)      # Author linked to user
    search(query)             # Search by name/email
    create_author(data: dict) # Create author (atomic)
    update_author(author_id, data)  # Update author (atomic)
```

### SEOService

```python
class SEOService(BaseService[SEORepository]):
    get_for_content(content_type_label, object_id)  # Get SEO for content
    get_or_create(content_type_label, object_id, data)  # Create/update SEO
    get_low_score(threshold=50)   # Entries below score threshold
    calculate_score(content_type_label, object_id)  # Get 0-100 score
```

### ContentVersionService

```python
class ContentVersionService(BaseService[ContentVersionRepository]):
    create_version(content_type, content_id, data, author, summary)
    get_current(content_type, content_id)
    get_history(content_type, content_id, limit=20)
    get_by_version(content_type, content_id, version_number)
    rollback_to(content_type, content_id, version_number, author)
```

### PublishingQueueService

```python
class PublishingQueueService(BaseService[PublishingQueueRepository]):
    schedule(content_type, content_id, scheduled_at, user)
    get_due()                  # Items where scheduled_at <= now
    get_pending()              # All pending items
    mark_published(queue_id)   # Mark as published
    mark_failed(queue_id, error_message)  # Mark as failed
    cancel(queue_id)           # Cancel pending item
    retry(queue_id)            # Retry failed item
```

### ContentHighlightService

```python
class ContentHighlightService(BaseService[ContentHighlightRepository]):
    get_active(highlight_type=None)   # Active highlights within date range
    get_for_homepage()                # Homepage-ready highlights
    create_highlight(data: dict)      # Create highlight (atomic)
    update_highlight(highlight_id, data)  # Update highlight (atomic)
    toggle_active(highlight_id)       # Toggle active flag
```

## Repository Pattern

### BaseRepository

```python
# utils/repositories.py
class BaseRepository(Generic[T]):
    model: Type[T]

    get_by_id(pk)          # Returns model instance or None
    list_all()             # Returns all records
    create(**fields)       # Create and save new record
    update(obj, **fields)  # Update fields and save
    delete(obj)            # Delete record
```

### Repository Implementations

| Repository | Model | Custom Methods |
|-----------|-------|---------------|
| `ContentCategoryRepository` | `ContentCategory` | `get_active`, `get_roots`, `get_children`, `search` |
| `ContentTagRepository` | `ContentTag` | `get_popular`, `search`, `get_or_create_by_name` |
| `AuthorRepository` | `Author` | `get_active`, `get_by_user`, `search` |
| `SEORepository` | `SEOModel` | `get_for_content`, `get_low_score` |
| `ContentVersionRepository` | `ContentVersion` | `get_current`, `get_history`, `get_by_version` |
| `PublishingQueueRepository` | `PublishingQueue` | `get_pending`, `get_due`, `get_by_content` |
| `ContentHighlightRepository` | `ContentHighlight` | `get_active_highlights`, `get_for_homepage` |

## Planned REST API Endpoints

### Authentication

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/auth/login/` | POST | Obtain auth token |
| `/api/v1/auth/logout/` | POST | Invalidate token |
| `/api/v1/auth/me/` | GET | Current user profile |

### Articles (`/api/v1/news/`)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/news/articles/` | GET | List articles (paginated) |
| `/api/v1/news/articles/` | POST | Create article |
| `/api/v1/news/articles/{uuid}/` | GET | Get article detail |
| `/api/v1/news/articles/{uuid}/` | PUT | Update article |
| `/api/v1/news/articles/{uuid}/` | DELETE | Delete article |
| `/api/v1/news/articles/{uuid}/workflow/` | POST | Workflow action |
| `/api/v1/news/articles/{uuid}/versions/` | GET | Version history |
| `/api/v1/news/categories/` | GET | List categories |
| `/api/v1/news/categories/` | POST | Create category |

### Podcasts (`/api/v1/podcast/`)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/podcast/` | GET | List podcasts |
| `/api/v1/podcast/` | POST | Create podcast |
| `/api/v1/podcast/{uuid}/` | GET | Get podcast detail |
| `/api/v1/podcast/{uuid}/` | PUT | Update podcast |
| `/api/v1/podcast/{uuid}/` | DELETE | Delete podcast |
| `/api/v1/podcast/{uuid}/episodes/` | GET | List episodes |
| `/api/v1/podcast/episodes/{uuid}/` | GET | Get episode detail |
| `/api/v1/podcast/episodes/{uuid}/` | PUT | Update episode |

### Broadcast (`/api/v1/broadcast/`)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/broadcast/programs/` | GET | List programs |
| `/api/v1/broadcast/programs/` | POST | Create program |
| `/api/v1/broadcast/programs/{uuid}/` | GET | Get program detail |
| `/api/v1/broadcast/programs/{uuid}/` | PUT | Update program |
| `/api/v1/broadcast/episodes/` | GET | List episodes |
| `/api/v1/broadcast/schedule/` | GET | Get schedule |
| `/api/v1/broadcast/hosts/` | GET | List hosts |

### Shared Content (`/api/v1/content/`)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/content/categories/` | GET | List categories |
| `/api/v1/content/tags/` | GET | List tags |
| `/api/v1/content/authors/` | GET | List authors |
| `/api/v1/content/seo/{uuid}/` | GET | Get SEO metadata |
| `/api/v1/content/seo/{uuid}/` | PUT | Update SEO metadata |
| `/api/v1/content/versions/` | GET | List versions |
| `/api/v1/content/versions/{uuid}/` | GET | Get version detail |
| `/api/v1/content/schedule/` | GET | List publishing queue |
| `/api/v1/content/highlights/` | GET | List highlights |
| `/api/v1/content/search/` | GET | Global search |

## Authentication and Permissions

### Role-Based Access Control

```python
# utils/choices.py
class UserRole(models.TextChoices):
    SUPERUSER = 'SUPERUSER', 'Super User'
    ADMINISTRATOR = 'ADMINISTRATOR', 'Administrator'
    EDITOR = 'EDITOR', 'Editor/Penulis'
    VIEWER = 'VIEWER', 'Viewer/Pembaca'
```

### Permission Matrix

| Action | SUPERUSER | ADMINISTRATOR | EDITOR | VIEWER |
|--------|-----------|---------------|--------|--------|
| Create content | Yes | Yes | Yes | No |
| Edit own content | Yes | Yes | Yes | No |
| Edit any content | Yes | Yes | No | No |
| Delete content | Yes | Yes | No | No |
| Approve content | Yes | Yes | No | No |
| Publish content | Yes | Yes | No | No |
| Manage categories | Yes | Yes | No | No |
| Manage tags | Yes | Yes | No | No |
| Manage authors | Yes | Yes | No | No |
| View SEO | Yes | Yes | Yes | Yes |
| Edit SEO | Yes | Yes | Yes | No |
| View versions | Yes | Yes | Yes | Yes |
| Rollback versions | Yes | Yes | No | No |
| Manage queue | Yes | Yes | No | No |
| View audit log | Yes | Yes | Yes | No |
| Manage users | Yes | Yes | No | No |

### API Authentication (Planned)

```python
# Token-based authentication
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}
```

### Permission Classes (Planned)

```python
class IsEditor(BasePermission):
    def has_permission(self, request, view):
        return request.user.role in ['SUPERUSER', 'ADMINISTRATOR', 'EDITOR']

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.role in ['SUPERUSER', 'ADMINISTRATOR']
```

## Content Serialization

### Article Serializer (Planned)

```python
class ArticleSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.name', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    tags = serializers.SlugRelatedField(
        many=True, slug_field='name', queryset=Tag.objects.all()
    )
    word_count = serializers.IntegerField(read_only=True)
    reading_time_minutes = serializers.IntegerField(read_only=True)

    class Meta:
        model = Article
        fields = [
            'id', 'title', 'slug', 'excerpt', 'content', 'content_format',
            'featured_image', 'category', 'category_name', 'tags',
            'author_name', 'status', 'priority', 'featured',
            'word_count', 'reading_time_minutes', 'version',
            'publish_date', 'scheduled_at', 'publish_end_date',
            'seo_title', 'seo_description', 'og_title', 'og_description',
            'og_image', 'twitter_card', 'canonical_url', 'robots',
            'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'slug', 'word_count', 'reading_time_minutes',
                           'version', 'created_at', 'updated_at']
```

### Podcast Serializer (Planned)

```python
class PodcastSerializer(serializers.ModelSerializer):
    episode_count = serializers.IntegerField(read_only=True)
    author_name = serializers.CharField(source='author.name', read_only=True)

    class Meta:
        model = Podcast
        fields = [
            'id', 'title', 'slug', 'description', 'short_description',
            'thumbnail', 'banner', 'category', 'language', 'episode_count',
            'author_name', 'status', 'featured', 'active',
            'seo_title', 'seo_description', 'og_title', 'og_description',
            'created_at', 'updated_at',
        ]
```

### SEO Serializer (Planned)

```python
class SEOSerializer(serializers.ModelSerializer):
    seo_score = serializers.IntegerField(read_only=True)
    seo_grade = serializers.CharField(read_only=True)

    class Meta:
        model = SEOModel
        fields = [
            'id', 'content_type', 'object_id',
            'title', 'description', 'keywords',
            'og_title', 'og_description', 'og_image', 'og_type',
            'twitter_card', 'twitter_title', 'twitter_description',
            'twitter_image', 'canonical_url', 'robots', 'schema_markup',
            'seo_score', 'seo_grade',
        ]
```

## Query Parameters

### Pagination

| Parameter | Default | Description |
|-----------|---------|-------------|
| `page` | 1 | Page number |
| `page_size` | 20 | Items per page (max 100) |

### Filtering

| Parameter | Applicable To | Description |
|-----------|--------------|-------------|
| `status` | Articles, Podcasts, Programs | Filter by ContentStatus |
| `category` | Articles, Podcasts | Filter by category |
| `tags` | Articles, Podcasts | Filter by tag (comma-separated) |
| `author` | Articles | Filter by author UUID |
| `featured` | Articles, Podcasts, Programs | Filter featured content |
| `priority` | Articles, Podcasts, Programs | Filter by priority |
| `content_type` | Categories, Versions, SEO | Filter by content type |
| `highlight_type` | Highlights | Filter by highlight type |
| `q` | All list endpoints | Search query |

### Ordering

| Parameter | Default | Description |
|-----------|---------|-------------|
| `ordering` | `-created_at` | Sort field (prefix `-` for descending) |

**Sortable fields:** `title`, `created_at`, `updated_at`, `publish_date`, `status`, `priority`, `view_count`, `version`

### Search

| Parameter | Description |
|-----------|-------------|
| `q` | Full-text search query |

## Response Format (Planned)

### Success Response

```json
{
    "status": "success",
    "data": {
        "id": "uuid-string",
        "title": "Article Title",
        "status": "DRAFT",
        "created_at": "2026-07-15T10:00:00Z",
        "updated_at": "2026-07-15T12:00:00Z"
    }
}
```

### Paginated Response

```json
{
    "status": "success",
    "data": [...],
    "pagination": {
        "page": 1,
        "page_size": 20,
        "total": 150,
        "total_pages": 8
    }
}
```

### Error Response

```json
{
    "status": "error",
    "errors": {
        "title": ["This field is required."],
        "content": ["This field may not be blank."]
    }
}
```

## Rate Limiting (Planned)

| Endpoint Type | Limit |
|--------------|-------|
| Read (GET) | 1000/hour |
| Write (POST/PUT/DELETE) | 200/hour |
| Search | 500/hour |
| Auth (login) | 10/minute |

## API Versioning (Planned)

- URL-based versioning: `/api/v1/...`
- Backwards-compatible changes within version
- New version for breaking changes
- Deprecated endpoints maintained for 6 months

## Integration Points

### Broadcast API (Existing)

The broadcast app already has API views:

| Endpoint | Description |
|----------|-------------|
| `/broadcast/api/programs/` | List programs |
| `/broadcast/api/program/{slug}/` | Program detail |
| `/broadcast/api/schedule/` | Full schedule |
| `/broadcast/api/today/` | Today's schedule |
| `/broadcast/api/current/` | Current broadcast |
| `/broadcast/api/next/` | Next broadcast |
| `/broadcast/api/hosts/` | List hosts |
| `/broadcast/api/episodes/` | List episodes |
| `/broadcast/api/playlist/` | Current playlist |

These serve as a reference implementation for the planned content API.
