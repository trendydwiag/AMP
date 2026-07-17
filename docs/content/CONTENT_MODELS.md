# Content Models

> Detailed documentation of all models in the Kabulhaden CMS content platform.

## Table of Contents

- [Shared Infrastructure](#shared-infrastructure)
- [Article Model](#article-model)
- [Podcast Model](#podcast-model)
- [PodcastEpisode Model](#podcastepisode-model)
- [Program Model](#program-model)
- [Episode Model](#episode-model)
- [Model Relationships](#model-relationships)

## Shared Infrastructure

All shared models live in `apps.content.models` and use the `UUIDPrimaryKeyMixin` and
`TimeStampedModel` abstract base classes.

### ContentCategory

Hierarchical category system scoped by content type.

```python
# apps/content/models.py — line 7
class ContentCategory(UUIDPrimaryKeyMixin, TimeStampedModel):
```

| Field | Type | Constraints | Default |
|-------|------|------------|---------|
| `name` | `CharField(200)` | — | required |
| `slug` | `SlugField(250)` | `unique=True` | auto-generated from name |
| `description` | `TextField` | — | `''` |
| `content_type` | `CharField(20)` | choices | required |
| `parent` | `ForeignKey(self)` | `CASCADE, null=True` | `None` |
| `icon` | `CharField(100)` | — | `''` |
| `color` | `CharField(7)` | — | `'#6B4226'` |
| `active` | `BooleanField` | — | `True` |
| `display_order` | `PositiveIntegerField` | — | `0` |

**Content Type Choices:**
- `ARTICLE` — Artikel
- `PODCAST` — Podcast
- `PROGRAM` — Program
- `EPISODE` — Episode
- `BROADCAST` — Siaran

**Meta:**
- `ordering = ['display_order', 'name']`
- `unique_together = ['name', 'content_type']`

**Behavior:**
- Slug auto-generated from `name` on save if blank
- Self-referencing FK enables parent/child hierarchy via `parent` field
- Categories queried via `get_roots()`, `get_children()`, `get_active()`

---

### ContentTag

Global tags shared across all content types.

```python
# apps/content/models.py — line 43
class ContentTag(UUIDPrimaryKeyMixin, TimeStampedModel):
```

| Field | Type | Constraints | Default |
|-------|------|------------|---------|
| `name` | `CharField(100)` | `unique=True` | required |
| `slug` | `SlugField(150)` | `unique=True` | auto-generated |
| `color` | `CharField(7)` | — | `'#6B4226'` |
| `usage_count` | `PositiveIntegerField` | — | `0` |

**Meta:**
- `ordering = ['name']`

**Behavior:**
- `usage_count` incremented via `ContentTagService.increment_usage()` using `F()` expression
- `get_or_create()` pattern for tag creation in services layer
- `bulk_create()` for batch tag creation

---

### Author

Author profiles linked optionally to Django User accounts.

```python
# apps/content/models.py — line 63
class Author(UUIDPrimaryKeyMixin, TimeStampedModel):
```

| Field | Type | Constraints | Default |
|-------|------|------------|---------|
| `user` | `OneToOneField(AUTH_USER_MODEL)` | `SET_NULL, null=True` | `None` |
| `name` | `CharField(200)` | — | required |
| `slug` | `SlugField(250)` | `unique=True` | auto-generated |
| `bio` | `TextField` | — | `''` |
| `avatar` | `ImageField` | upload to `content/authors/avatars/` | blank |
| `email` | `EmailField` | — | `''` |
| `website` | `URLField(500)` | — | `''` |
| `social_links` | `JSONField` | — | `{}` |
| `active` | `BooleanField` | — | `True` |

**Properties:**
- `article_count` — Filters `content_author` reverse relation by `content_type='ARTICLE'`
- `podcast_count` — Filters `content_author` reverse relation by `content_type='PODCAST'`

**Meta:**
- `ordering = ['name']`

---

### SEOModel

Generic SEO metadata using Django's ContentType framework.

```python
# apps/content/models.py — line 99
class SEOModel(UUIDPrimaryKeyMixin, TimeStampedModel):
```

| Field | Type | Constraints | Default |
|-------|------|------------|---------|
| `content_type` | `ForeignKey(ContentType)` | `CASCADE` | required |
| `object_id` | `UUIDField` | — | required |
| `title` | `CharField(200)` | — | `''` |
| `description` | `TextField(500)` | — | `''` |
| `keywords` | `CharField(500)` | — | `''` |
| `og_title` | `CharField(200)` | — | `''` |
| `og_description` | `TextField(500)` | — | `''` |
| `og_image` | `ImageField` | upload to `content/seo/og/` | blank |
| `og_type` | `CharField(50)` | — | `'article'` |
| `twitter_card` | `CharField(20)` | — | `'summary_large_image'` |
| `twitter_title` | `CharField(200)` | — | `''` |
| `twitter_description` | `TextField(500)` | — | `''` |
| `twitter_image` | `ImageField` | upload to `content/seo/twitter/` | blank |
| `canonical_url` | `URLField(500)` | — | `''` |
| `robots` | `CharField(30)` | — | `'index,follow'` |
| `schema_markup` | `JSONField` | — | `{}` |

**Computed Properties:**
- `seo_score` — 0–100 score based on field completeness
- `seo_grade` — Letter grade (A–F) derived from score
- `effective_title` — Falls back to `title`
- `effective_description` — Falls back through description chain

**Unique Constraint:**
- `unique_together = ['content_type', 'object_id']` — One SEO entry per content object

**Scoring Algorithm:**

| Criterion | Points |
|-----------|--------|
| Has `title` | +20 |
| Title length 30–60 chars | +10 |
| Has `description` | +20 |
| Description length 120–160 chars | +10 |
| Has `og_title` | +10 |
| Has `og_description` | +10 |
| Has `og_image` | +10 |
| Has `keywords` | +10 |

**Grade Mapping:**

| Score | Grade |
|-------|-------|
| 90–100 | A |
| 70–89 | B |
| 50–69 | C |
| 30–49 | D |
| 0–29 | F |

---

### ContentVersion

Automatic version snapshots for content rollback and audit trails.

```python
# apps/content/models.py — line 171
class ContentVersion(UUIDPrimaryKeyMixin, TimeStampedModel):
```

| Field | Type | Constraints | Default |
|-------|------|------------|---------|
| `content_type` | `CharField(25)` | choices | required |
| `content_id` | `UUIDField` | — | required |
| `version_number` | `PositiveIntegerField` | — | `1` |
| `title` | `CharField(300)` | — | `''` |
| `data_snapshot` | `JSONField` | — | `{}` |
| `change_summary` | `CharField(500)` | — | `''` |
| `author` | `ForeignKey(AUTH_USER_MODEL)` | `SET_NULL, null=True` | `None` |
| `is_current` | `BooleanField` | — | `True` |

**Content Type Choices:**
- `ARTICLE`, `PODCAST`, `PODCAST_EPISODE`, `PROGRAM`, `EPISODE`, `ANNOUNCEMENT`, `DISCUSSION`

**Class Methods:**
- `create_version(content_type, content_id, data, author, summary)` — Creates new version, marks old as non-current
- `get_current(content_type, content_id)` — Returns current version
- `get_history(content_type, content_id, limit=20)` — Returns version list

**Unique Constraint:**
- `unique_together = ['content_type', 'content_id', 'version_number']`

---

### PublishingQueue

Scheduled publishing queue with retry support.

```python
# apps/content/models.py — line 243
class PublishingQueue(UUIDPrimaryKeyMixin, TimeStampedModel):
```

| Field | Type | Constraints | Default |
|-------|------|------------|---------|
| `content_type` | `CharField(25)` | choices | required |
| `content_id` | `UUIDField` | — | required |
| `scheduled_at` | `DateTimeField` | — | required |
| `published_at` | `DateTimeField` | `null=True` | `None` |
| `status` | `CharField(20)` | — | `'PENDING'` |
| `created_by` | `ForeignKey(AUTH_USER_MODEL)` | `SET_NULL, null=True` | `None` |
| `error_message` | `TextField` | — | `''` |
| `retry_count` | `PositiveIntegerField` | — | `0` |

**Status Values:**
- `PENDING` — Waiting to be published
- `PUBLISHED` — Successfully published
- `FAILED` — Publishing failed
- `CANCELLED` — Cancelled by user

---

### ContentHighlight

Homepage content highlights with scheduling and override capabilities.

```python
# apps/content/models.py — line 273
class ContentHighlight(UUIDPrimaryKeyMixin, TimeStampedModel):
```

| Field | Type | Constraints | Default |
|-------|------|------------|---------|
| `highlight_type` | `CharField(20)` | choices | required |
| `content_type` | `CharField(25)` | choices | required |
| `content_id` | `UUIDField` | — | required |
| `title_override` | `CharField(300)` | — | `''` |
| `description_override` | `TextField` | — | `''` |
| `image_override` | `ImageField` | upload to `content/highlights/` | blank |
| `display_order` | `PositiveIntegerField` | — | `0` |
| `active` | `BooleanField` | — | `True` |
| `start_date` | `DateTimeField` | `null=True` | `None` |
| `end_date` | `DateTimeField` | `null=True` | `None` |

**Highlight Type Choices:**
- `HERO` — Hero Section
- `FEATURED` — Unggulan
- `TRENDING` — Trending
- `LATEST` — Terbaru
- `EDITORS_PICK` — Pilihan Editor

**Property:**
- `is_active_now` — Checks active flag and date range validity

## Article Model

```python
# apps/news/models.py — line 48
class Article(UUIDPrimaryKeyMixin, TimeStampedModel):
```

| Field | Type | Default |
|-------|------|---------|
| `title` | `CharField(300)` | required |
| `slug` | `SlugField(350)` | auto-generated |
| `excerpt` | `CharField(500)` | `''` |
| `content` | `TextField` | required |
| `featured_image` | `ImageField` | blank |
| `category` | `FK(news.Category)` | `None` |
| `tags` | `M2M(news.Tag)` | — |
| `author_name` | `CharField(200)` | `'Redaksi'` |
| `content_format` | `CharField(15)` | `RICH_TEXT` |
| `status` | `CharField(18)` | `DRAFT` |
| `priority` | `CharField(10)` | `NORMAL` |
| `featured` | `BooleanField` | `False` |
| `allow_comments` | `BooleanField` | `True` |
| `word_count` | `PositiveIntegerField` | `0` (auto-calculated) |
| `reading_time_minutes` | `PositiveIntegerField` | `0` (auto-calculated) |
| `version` | `PositiveIntegerField` | `1` |
| `last_published_at` | `DateTimeField` | `None` |
| `publish_date` | `DateTimeField` | `None` |
| `scheduled_at` | `DateTimeField` | `None` |
| `publish_end_date` | `DateTimeField` | `None` |
| `view_count` | `PositiveIntegerField` | `0` |
| `seo_title` | `CharField(200)` | `''` |
| `seo_description` | `CharField(500)` | `''` |
| `og_title` | `CharField(200)` | `''` |
| `og_description` | `CharField(500)` | `''` |
| `og_image` | `ImageField` | blank |
| `twitter_card` | `CharField(20)` | `'summary_large_image'` |
| `canonical_url` | `URLField(500)` | `''` |
| `robots` | `CharField(30)` | `'index,follow'` |
| `schema_markup` | `JSONField` | `{}` |
| `related_articles` | `M2M(self)` | — |
| `author` | `FK(content.Author)` | `None` |
| `tags_content` | `M2M(content.ContentTag)` | — |

**Computed Fields (auto on save):**
- `word_count` — Strips HTML tags, counts words
- `reading_time_minutes` — `max(1, word_count // 200)`
- `slug` — Auto-generated from title if blank

**Properties:**
- `is_published` — `True` if status is PUBLISHED and `last_published_at` is set

## Podcast Model

```python
# apps/podcast/models.py — line 7
class Podcast(UUIDPrimaryKeyMixin, TimeStampedModel):
```

| Field | Type | Default |
|-------|------|---------|
| `title` | `CharField(300)` | required |
| `slug` | `SlugField(350)` | auto-generated |
| `description` | `TextField` | `''` |
| `short_description` | `CharField(500)` | `''` |
| `thumbnail` | `ImageField` | blank |
| `banner` | `ImageField` | blank |
| `author_name` | `CharField(200)` | `'Redaksi'` |
| `category` | `CharField(20)` | `OTHER` |
| `language` | `CharField(10)` | `'id'` |
| `episode_count` | `PositiveIntegerField` | `0` |
| `itunes_url` | `URLField` | `''` |
| `spotify_url` | `URLField` | `''` |
| `google_url` | `URLField` | `''` |
| `active` | `BooleanField` | `True` |
| `featured` | `BooleanField` | `False` |
| `seo_title` | `CharField(200)` | `''` |
| `seo_description` | `CharField(500)` | `''` |
| `status` | `CharField(15)` | `DRAFT` |
| `priority` | `CharField(10)` | `NORMAL` |
| `version` | `PositiveIntegerField` | `1` |
| `last_published_at` | `DateTimeField` | `None` |
| `author` | `FK(content.Author)` | `None` |
| `tags_content` | `M2M(content.ContentTag)` | — |
| `og_title`, `og_description`, `og_image` | various | `''`/blank |
| `twitter_card` | `CharField(20)` | `'summary_large_image'` |
| `canonical_url` | `URLField(500)` | `''` |
| `robots` | `CharField(30)` | `'index,follow'` |
| `schema_markup` | `JSONField` | `{}` |
| `content_format` | `CharField(15)` | `RICH_TEXT` |

## PodcastEpisode Model

```python
# apps/podcast/models.py — line 80
class PodcastEpisode(UUIDPrimaryKeyMixin, TimeStampedModel):
```

| Field | Type | Default |
|-------|------|---------|
| `podcast` | `FK(Podcast)` | CASCADE, required |
| `title` | `CharField(300)` | required |
| `slug` | `SlugField(350)` | auto-generated |
| `description` | `TextField` | `''` |
| `audio_file` | `FileField` | required |
| `audio_url` | `URLField` | `''` |
| `cover_image` | `ImageField` | blank |
| `duration` | `PositiveIntegerField` | `0` (seconds) |
| `episode_number` | `PositiveIntegerField` | `1` |
| `season_number` | `PositiveIntegerField` | `1` |
| `published` | `BooleanField` | `False` |
| `publish_date` | `DateTimeField` | `None` |
| `download_count` | `PositiveIntegerField` | `0` |
| `status` | `CharField(15)` | `DRAFT` |
| `content_format` | `CharField(15)` | `RICH_TEXT` |
| `transcript` | `TextField` | `''` |
| `version` | `PositiveIntegerField` | `1` |
| `last_published_at` | `DateTimeField` | `None` |
| `scheduled_at` | `DateTimeField` | `None` |
| `og_title`, `og_description`, `og_image` | various | `''`/blank |
| `twitter_card` | `CharField(20)` | `'summary_large_image'` |
| `canonical_url` | `URLField(500)` | `''` |
| `robots` | `CharField(30)` | `'index,follow'` |

## Program Model

```python
# apps/broadcast/models.py — line 7
class Program(UUIDPrimaryKeyMixin, TimeStampedModel):
```

| Field | Type | Default |
|-------|------|---------|
| `title` | `CharField(200)` | required |
| `slug` | `SlugField(250)` | auto-generated |
| `short_description` | `CharField(500)` | `''` |
| `full_description` | `TextField` | `''` |
| `thumbnail` | `ImageField` | blank |
| `banner` | `ImageField` | blank |
| `category` | `CharField(100)` | `''` |
| `language` | `CharField(10)` | `'id'` |
| `genre` | `CharField(100)` | `''` |
| `target_audience` | `CharField(100)` | `''` |
| `content_rating` | `CharField(5)` | `G` (General) |
| `featured` | `BooleanField` | `False` |
| `active` | `BooleanField` | `True` |
| `seo_title` | `CharField(200)` | `''` |
| `seo_description` | `CharField(500)` | `''` |
| `created_by` | `FK(AUTH_USER_MODEL)` | `None` |
| `updated_by` | `FK(AUTH_USER_MODEL)` | `None` |
| `status` | `CharField(20)` | `DRAFT` |
| `priority` | `CharField(10)` | `NORMAL` |
| `content_format` | `CharField(15)` | `RICH_TEXT` |
| `version` | `PositiveIntegerField` | `1` |
| `last_published_at` | `DateTimeField` | `None` |
| `author` | `FK(content.Author)` | `None` |
| `tags_content` | `M2M(content.ContentTag)` | — |
| `og_title`, `og_description`, `og_image` | various | `''`/blank |
| `twitter_card`, `canonical_url`, `robots`, `schema_markup` | various | defaults |

**Property:**
- `hosts` — Returns `host_members.select_related('host')`

## Episode Model

```python
# apps/broadcast/models.py — line 185
class Episode(UUIDPrimaryKeyMixin, TimeStampedModel):
```

| Field | Type | Default |
|-------|------|---------|
| `broadcast_session` | `FK(BroadcastSession)` | `None` |
| `program` | `FK(Program)` | CASCADE, required |
| `episode_number` | `PositiveIntegerField` | `1` |
| `title` | `CharField(300)` | required |
| `description` | `TextField` | `''` |
| `cover_image` | `ImageField` | blank |
| `recording_audio` | `FileField` | blank |
| `recording_video` | `FileField` | blank |
| `published` | `BooleanField` | `False` |
| `publish_date` | `DateTimeField` | `None` |
| `status` | `CharField(20)` | `DRAFT` |
| `content_format` | `CharField(15)` | `RICH_TEXT` |
| `transcript` | `TextField` | `''` |
| `version` | `PositiveIntegerField` | `1` |
| `last_published_at` | `DateTimeField` | `None` |
| `scheduled_at` | `DateTimeField` | `None` |
| `og_title`, `og_description`, `og_image` | various | `''`/blank |
| `twitter_card`, `canonical_url`, `robots` | various | defaults |
| `featured` | `BooleanField` | `False` |

## Model Relationships

```
Article ──FK──→ Author (content.Author)
Article ──FK──→ Category (news.Category)
Article ──M2M──→ Tag (news.Tag)
Article ──M2M──→ ContentTag (content.ContentTag)
Article ──M2M──→ Article (self, related_articles)

Podcast ──FK──→ Author (content.Author)
Podcast ──M2M──→ ContentTag (content.ContentTag)
PodcastEpisode ──FK──→ Podcast

Program ──FK──→ Author (content.Author)
Program ──M2M──→ ContentTag (content.ContentTag)
Program ──FK──→ User (created_by, updated_by)
Episode ──FK──→ Program
Episode ──FK──→ BroadcastSession

HostMember ──FK──→ Host
HostMember ──FK──→ Program
Schedule ──FK──→ Program
BroadcastSession ──FK──→ Program
BroadcastSession ──FK──→ Schedule

ContentCategory ──FK──→ self (parent)
SEOModel ──FK──→ ContentType
ContentVersion ──FK──→ User (author)
PublishingQueue ──FK──→ User (created_by)
```

## Migration History

### content app

| Migration | Description |
|-----------|-------------|
| `0001_initial` | Creates all 7 shared models: ContentHighlight, ContentTag, Author, PublishingQueue, ContentCategory, ContentVersion, SEOModel |

### news app

| Migration | Description |
|-----------|-------------|
| `0001_initial` | Creates Article, Category, Tag models |

### podcast app

| Migration | Generated by Django 5.0.9 | Creates Podcast, PodcastEpisode models |

### broadcast app

| Migration | Description |
|-----------|-------------|
| `0001_initial` | Creates Program, Host, HostMember, Schedule, BroadcastSession, Episode, GuestStar, EpisodeGuest, Playlist, PlaylistItem, Announcement |
| `0002_alter_program_slug` | Modifies Program slug field |
| `0003_*` | Adds SEO fields to Episode model |
