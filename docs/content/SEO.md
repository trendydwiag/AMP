# SEO Module

> Search Engine Optimization tools and metadata management.

## Overview

The Kabulhaden CMS provides comprehensive SEO management at two levels:

1. **Per-content SEO fields** — Embedded directly on Article, Podcast, Program, and Episode models
2. **SEOModel** — Generic SEO metadata using Django's ContentType framework for centralized management

## Per-Content SEO Fields

Every major content model includes these SEO-related fields:

### Standard SEO Fields

| Field | Type | Max Length | Default | Description |
|-------|------|-----------|---------|-------------|
| `seo_title` | `CharField` | 200 | `''` | Meta title for search engines |
| `seo_description` | `CharField` | 500 | `''` | Meta description |
| `og_title` | `CharField` | 200 | `''` | OpenGraph title |
| `og_description` | `CharField` | 500 | `''` | OpenGraph description |
| `og_image` | `ImageField` | — | blank | OpenGraph image |
| `twitter_card` | `CharField` | 20 | `'summary_large_image'` | Twitter card type |
| `canonical_url` | `URLField` | 500 | `''` | Canonical URL |
| `robots` | `CharField` | 30 | `'index,follow'` | Robots directive |
| `schema_markup` | `JSONField` | — | `{}` | Custom Schema.org data |

### Models With SEO Fields

| Model | Location | SEO Fields |
|-------|----------|-----------|
| `Article` | `apps/news/models.py:84` | Full set |
| `Podcast` | `apps/podcast/models.py:27` | Full set |
| `PodcastEpisode` | `apps/podcast/models.py:115` | Full set |
| `Program` | `apps/broadcast/models.py:44` | Full set |
| `Episode` | `apps/broadcast/models.py:205` | Full set |

## OpenGraph Metadata

### Purpose

OpenGraph tags control how content appears when shared on social media platforms
(Facebook, LinkedIn, Discord, Slack, etc.).

### Generated Tags

```html
<meta property="og:title" content="{og_title|title}">
<meta property="og:description" content="{og_description|description}">
<meta property="og:image" content="{og_image_url}">
<meta property="og:type" content="article">
<meta property="og:url" content="{canonical_url|current_url}">
<meta property="og:site_name" content="Kabulhaden">
```

### Field Mapping

| OG Property | Source Field | Fallback |
|------------|-------------|----------|
| `og:title` | `og_title` | `seo_title` → `title` |
| `og:description` | `og_description` | `seo_description` → `excerpt` |
| `og:image` | `og_image` | `featured_image` |
| `og:type` | Hardcoded `'article'` | — |
| `og:url` | `canonical_url` | Current URL |

### Image Specifications

| Property | Recommendation |
|----------|---------------|
| Aspect ratio | 1200×630px (1.91:1) |
| Minimum size | 600×315px |
| Maximum file size | 1MB |
| Format | JPEG or PNG |
| Upload path | `news/articles/og/`, `podcast/og/`, etc. |

### og_type Values

| Value | Use For |
|-------|---------|
| `article` | News articles, blog posts |
| `website` | Homepage, landing pages |
| `product` | Product pages (future) |
| `profile` | Author pages (future) |

## Twitter Card Configuration

### Card Types

```python
class TwitterCard(models.TextChoices):
    SUMMARY = 'summary', 'Summary'
    SUMMARY_LARGE_IMAGE = 'summary_large_image', 'Summary Large Image'
```

### Generated Tags

```html
<meta name="twitter:card" content="{twitter_card}">
<meta name="twitter:title" content="{twitter_title|og_title|title}">
<meta name="twitter:description" content="{twitter_description|og_description|description}">
<meta name="twitter:image" content="{twitter_image_url}">
```

### Field Mapping

| Twitter Property | Source Field | Fallback |
|-----------------|-------------|----------|
| `twitter:card` | `twitter_card` | `'summary_large_image'` |
| `twitter:title` | `twitter_title` | `og_title` → `title` |
| `twitter:description` | `twitter_description` | `og_description` |
| `twitter:image` | `twitter_image` | `og_image` |

### SEOModel Twitter Fields

The `SEOModel` provides additional Twitter-specific fields:

| Field | Type | Default |
|-------|------|---------|
| `twitter_title` | `CharField(200)` | `''` |
| `twitter_description` | `TextField(500)` | `''` |
| `twitter_image` | `ImageField` | blank |
| `twitter_card` | `CharField(20)` | `'summary_large_image'` |

## Schema.org / JSON-LD Markup

### Template-Based Schema

The CMS includes pre-built Schema.org templates:

| Template | Path | Use For |
|----------|------|---------|
| Article | `website/seo/article_schema.html` | News articles |
| Podcast | `website/seo/podcast_schema.html` | Podcast episodes |
| Breadcrumb | `website/seo/breadcrumb_schema.html` | Navigation breadcrumbs |
| Website | `website/seo/website_schema.html` | Site-wide metadata |
| Organization | `website/seo/organization_schema.html` | Organization info |

### Article Schema Example

```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "Article Title",
  "description": "Article description...",
  "author": {
    "@type": "Person",
    "name": "Author Name"
  },
  "datePublished": "2026-07-15T10:00:00+07:00",
  "dateModified": "2026-07-15T12:00:00+07:00",
  "image": "https://kabulhaden.com/media/news/articles/...",
  "publisher": {
    "@type": "Organization",
    "name": "Kabulhaden",
    "logo": "https://kabulhaden.com/static/logo.png"
  }
}
```

### Custom Schema Markup

Content models include a `schema_markup` JSONField for custom structured data:

```python
# Set via SEO form
article.schema_markup = {
    "@type": "NewsArticle",
    "wordCount": 850,
    "articleSection": "Berita"
}
```

## Canonical URLs

### Purpose

Canonical URLs prevent duplicate content issues by specifying the preferred URL
for each piece of content.

### Configuration

| Field | Model | Description |
|-------|-------|-------------|
| `canonical_url` | Article, Podcast, Episode, Program | Full URL of canonical version |

### Auto-Generation Rules

1. If `canonical_url` is set → use it
2. If not set → use current request URL
3. For paginated content → canonical to first page

### Example

```html
<link rel="canonical" href="https://kabulhaden.com/berita/artikel/my-article-slug/">
```

## Robots Directives

### Available Directives

```python
class RobotsMeta(models.TextChoices):
    INDEX_FOLLOW = 'index,follow', 'Index & Follow'
    NOINDEX_FOLLOW = 'noindex,follow', 'No Index, Follow'
    INDEX_NOFOLLOW = 'index,nofollow', 'Index, No Follow'
    NOINDEX_NOFOLLOW = 'noindex,nofollow', 'No Index, No Follow'
```

### Common Usage

| Directive | When to Use |
|-----------|-------------|
| `index,follow` | Default for published content |
| `noindex,follow` | Draft content, internal pages |
| `index,nofollow` | User-generated content links |
| `noindex,nofollow` | Private/admin pages |

### Generated Tag

```html
<meta name="robots" content="index,follow">
```

## SEO Scoring (0–100)

### Algorithm

The SEO score is computed by `SEOModel.seo_score` property:

```python
@property
def seo_score(self):
    score = 0
    if self.title: score += 20           # Has meta title
    if 30 <= len(self.title) <= 60: score += 10  # Optimal title length
    if self.description: score += 20      # Has meta description
    if 120 <= len(self.description) <= 160: score += 10  # Optimal desc length
    if self.og_title: score += 10         # Has OG title
    if self.og_description: score += 10   # Has OG description
    if self.og_image: score += 10         # Has OG image
    if self.keywords: score += 10         # Has keywords
    return min(score, 100)
```

### Scoring Breakdown

| Criterion | Points | Optimal Value |
|-----------|--------|--------------|
| Meta title exists | 20 | Non-empty string |
| Title length optimal | 10 | 30–60 characters |
| Meta description exists | 20 | Non-empty string |
| Description length optimal | 10 | 120–160 characters |
| OG title exists | 10 | Non-empty string |
| OG description exists | 10 | Non-empty string |
| OG image exists | 10 | Non-blank ImageField |
| Keywords exist | 10 | Non-empty string |
| **Maximum** | **100** | |

### Grade Mapping

```python
@property
def seo_grade(self):
    score = self.seo_score
    if score >= 90: return 'A'
    elif score >= 70: return 'B'
    elif score >= 50: return 'C'
    elif score >= 30: return 'D'
    return 'F'
```

| Score | Grade | Visual | Meaning |
|-------|-------|--------|---------|
| 90–100 | A | Green | Excellent optimization |
| 70–89 | B | Blue | Good, minor improvements possible |
| 50–69 | C | Yellow | Average, needs attention |
| 30–49 | D | Orange | Poor, significant issues |
| 0–29 | F | Red | Critical SEO problems |

## SEO Preview Widget

The CMS includes an SEO preview widget that shows how content will appear
in search engine results and social media shares.

### Google Preview

```
┌─────────────────────────────────────────┐
│ kabilhaden.com › berita › artikel       │
│                                         │
│ Article Title — Kabulhaden              │
│ https://kabulhaden.com/berita/artikel/  │
│ Description text appears here, showing  │
│ how the meta description will look...   │
└─────────────────────────────────────────┘
```

### Facebook/OG Preview

```
┌─────────────────────────────────────────┐
│ ┌──────────────┐                        │
│ │              │ Article Title           │
│ │   OG IMAGE   │                        │
│ │   1200×630   │ Description text from   │
│ │              │ og_description field...  │
│ └──────────────┘                        │
│ KABULHADEN.COM                          │
└─────────────────────────────────────────┘
```

### Twitter Card Preview

```
┌─────────────────────────────────────────┐
│ ┌──────────────┐                        │
│ │              │                        │
│ │  TWITTER     │ Article Title           │
│ │  IMAGE       │ Description text from   │
│ │              │ twitter_description...  │
│ └──────────────┘                        │
│                                         │
└─────────────────────────────────────────┘
```

## SEOModel (Generic Metadata)

### Purpose

The `SEOModel` provides a centralized, ContentType-based SEO metadata system
for any model in the system.

### Location

```python
# apps/content/models.py — line 99
class SEOModel(UUIDPrimaryKeyMixin, TimeStampedModel):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.UUIDField()
    # ... SEO fields
```

### Unique Constraint

```python
unique_together = ['content_type', 'object_id']
```

One SEO record per content object.

### Service Layer

```python
# apps/content/services.py
class SEOService(BaseService[SEORepository]):
    def get_for_content(self, content_type_label, object_id):
        # content_type_label = 'news.article' or 'podcast.podcast'
        ...

    def get_or_create(self, content_type_label, object_id, data):
        # Creates or updates SEO entry
        ...

    def get_low_score(self, threshold=50):
        # Returns entries below score threshold
        ...

    def calculate_score(self, content_type_label, object_id):
        # Returns 0-100 score
        ...
```

### CMS Management

SEO entries are managed at `/konten/seo/`:

| URL | View | Description |
|-----|------|-------------|
| `/konten/seo/` | `SEOListView` | List all SEO entries |
| `/konten/seo/create/` | `SEOCreateView` | Create new SEO entry |
| `/konten/seo/<uuid>/edit/` | `SEOUpdateView` | Edit SEO entry |

## Best Practices

### Title Tags

1. Keep between 30–60 characters
2. Include primary keyword near the beginning
3. Include brand name: "Article Title — Kabulhaden"
4. Make it unique for each page
5. Use action words when possible

### Meta Descriptions

1. Keep between 120–160 characters
2. Include a call to action
3. Summarize the page content accurately
4. Include primary keyword naturally
5. Make each description unique

### OpenGraph Images

1. Use 1200×630px dimensions
2. Include text overlay with article title
3. Use brand colors and fonts
4. Keep file size under 1MB
5. Use JPEG for photos, PNG for graphics

### URL Structure

1. Use descriptive, keyword-rich slugs
2. Keep URLs short and readable
3. Use hyphens to separate words
4. Avoid special characters and parameters
5. Set canonical URL for all content

### Schema.org

1. Use appropriate @type for content
2. Include required properties for each type
3. Validate with Google Rich Results Test
4. Keep structured data in sync with visible content
5. Use the built-in templates as a starting point

## SEO Checklist

Before publishing any content:

- [ ] Meta title is 30–60 characters
- [ ] Meta description is 120–160 characters
- [ ] OG image is 1200×630px
- [ ] OG title and description are set
- [ ] Twitter card type is appropriate
- [ ] Canonical URL is correct
- [ ] Robots directive is appropriate
- [ ] Keywords are relevant (3–5)
- [ ] SEO score is grade B or higher
- [ ] Schema.org markup is accurate
