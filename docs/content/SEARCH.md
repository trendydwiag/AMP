# Search Functionality

> Global and per-module search implementation in the Kabulhaden CMS.

## Overview

The Kabulhaden CMS provides search functionality at two levels:

1. **Global Search** — Cross-module search across Articles, Podcasts, and Programs
2. **Per-Module Search** — Filtered search within individual content types

Both implementations use **HTMX** for instant, partial-page updates.

## Global Search

### Implementation

The global search is implemented in `GlobalSearchView`:

```python
# apps/content/views.py — line 373
class GlobalSearchView(LoginRequiredMixin, TemplateView):
    template_name = 'content/search_results.html'
```

### URL

```
GET /konten/search/?q={query}&content_type={type}
```

### How It Works

1. User enters query in the search input
2. HTMX sends GET request after 300ms debounce
3. View queries Article, Podcast, and Program models
4. Results are rendered in `content/search_results.html`
5. HTMX swaps the results into the DOM

### HTMX Configuration

```python
# apps/content/forms.py — line 119
class GlobalSearchForm(forms.Form):
    q = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Cari konten...',
            'hx-get': '/cms/search/',
            'hx-trigger': 'input changed delay:300ms',
            'hx-target': '#search-results',
        })
    )
```

### Search Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `q` | string | Search query |
| `content_type` | string | Filter by type (optional) |

### Content Type Filter

| Value | Label | Searches |
|-------|-------|----------|
| (empty) | Semua | All content types |
| `ARTICLE` | Artikel | Articles only |
| `PODCAST` | Podcast | Podcasts only |
| `PROGRAM` | Program | Programs only |

## Per-Module Search

### Article Search

Articles support search via the list view:

```
GET /berita/cms/artikel/?q={query}
```

The Article CMS list view filters by title and content:

```python
# apps/news/views.py
qs = qs.filter(
    Q(title__icontains=query) | Q(content__icontains=query)
)
```

### Podcast Search

Podcasts support search via the list view:

```
GET /podcast/cms/podcast/?q={query}
```

```python
# apps/podcast/views.py
qs = qs.filter(
    Q(title__icontains=query) | Q(description__icontains=query)
)
```

### Category Search

Content categories support search:

```
GET /konten/categories/?q={query}&content_type={type}
```

```python
# apps/content/views.py — line 50
qs = qs.filter(
    Q(name__icontains=query) | Q(description__icontains=query)
)
```

### Tag Search

Tags support search by name:

```
GET /konten/tags/?q={query}
```

```python
# apps/content/views.py — line 106
qs = qs.filter(name__icontains=query)
```

### Author Search

Authors support search by name and email:

```
GET /konten/authors/?q={query}
```

```python
# apps/content/views.py — line 158
qs = qs.filter(
    Q(name__icontains=query) | Q(email__icontains=query)
)
```

### SEO Entry Search

SEO entries support search:

```
GET /konten/seo/?q={query}
```

```python
# apps/content/views.py — line 216
qs = qs.filter(
    Q(title__icontains=query) | Q(description__icontains=query)
)
```

## Search Result Formatting

### Result Structure

The global search returns results grouped by content type:

```python
ctx['results'] = [
    {'type': 'article', 'items': articles[:5]},
    {'type': 'podcast', 'items': podcasts[:5]},
    {'type': 'program', 'items': programs[:5]},
]
```

### Result Limits

| Content Type | Max Results |
|-------------|-------------|
| Articles | 5 |
| Podcasts | 5 |
| Programs | 5 |

### Template

Results are rendered in `content/search_results.html`:

```html
<!-- For each content type group -->
<div class="search-group">
  <h3>{{ result.type|title }}</h3>
  {% for item in result.items %}
    <a href="..." class="search-result-item">
      <h4>{{ item.title }}</h4>
      <p>{{ item.excerpt|truncatewords:20 }}</p>
    </a>
  {% endfor %}
</div>
```

## HTMX Integration

### Search Input Pattern

The search input uses HTMX for instant results:

```html
<input
    type="text"
    name="q"
    hx-get="/konten/search/"
    hx-trigger="input changed delay:300ms"
    hx-target="#search-results"
    hx-indicator="#search-spinner"
    placeholder="Cari konten..."
    class="form-input"
>
```

### HTMX Attributes

| Attribute | Value | Description |
|-----------|-------|-------------|
| `hx-get` | `/konten/search/` | URL to fetch results |
| `hx-trigger` | `input changed delay:300ms` | Debounced input trigger |
| `hx-target` | `#search-results` | Target element for swap |
| `hx-indicator` | `#search-spinner` | Loading indicator |

### Partial Page Updates

HTMX replaces only the search results container:

```html
<div id="search-results">
    <!-- HTMX swaps this content -->
    {% include 'content/search_results.html' %}
</div>
```

### Keyboard Navigation

The search modal supports keyboard shortcuts:

| Shortcut | Action |
|----------|--------|
| `Cmd+K` / `Ctrl+K` | Open search modal |
| `Escape` | Close search modal |
| `↑` / `↓` | Navigate results |
| `Enter` | Open selected result |

## Search UX Patterns

### Loading States

```html
<div id="search-spinner" class="htmx-indicator">
    <svg class="animate-spin h-5 w-5" ...>
        <!-- Spinner SVG -->
    </svg>
    Mencari...
</div>
```

### Empty States

```html
<div id="search-results">
    <div class="text-center py-8">
        <svg class="w-12 h-12 mx-auto text-coffee-300" ...>
            <!-- Search icon -->
        </svg>
        <p class="mt-2 text-sm text-coffee-400">
            Ketik untuk mulai mencari...
        </p>
    </div>
</div>
```

### No Results State

```html
<div class="text-center py-8">
    <p class="text-sm text-coffee-400">
        Tidak ada hasil untuk "{{ query }}"
    </p>
</div>
```

### Search Result Cards

Each result is rendered as a clickable card:

```html
<a href="{% url 'news:cms_article_detail' item.pk %}"
   class="block p-4 rounded-xl hover:bg-coffee-50 dark:hover:bg-coffee-700/50 transition-colors">
    <div class="flex items-center gap-3">
        <div class="w-10 h-10 rounded-lg bg-coffee-100 dark:bg-coffee-700 flex items-center justify-center">
            <!-- Content type icon -->
        </div>
        <div class="flex-1 min-w-0">
            <p class="text-sm font-medium text-coffee-700 dark:text-coffee-200 truncate">
                {{ item.title }}
            </p>
            <p class="text-xs text-coffee-400 truncate">
                {{ item.excerpt|truncatewords:15 }}
            </p>
        </div>
        <span class="px-2 py-0.5 text-xs rounded-full bg-coffee-100 dark:bg-coffee-700 text-coffee-500">
            {{ item.get_content_type_display }}
        </span>
    </div>
</a>
```

## Search Architecture

### Repository Layer

Search queries are encapsulated in repository classes:

```python
# apps/content/repos.py
class ContentCategoryRepository(BaseRepository):
    def search(self, query, content_type=None):
        qs = self.model.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )
        if content_type:
            qs = qs.filter(content_type=content_type)
        return qs.order_by('display_order', 'name')

class ContentTagRepository(BaseRepository):
    def search(self, query):
        return self.model.objects.filter(
            Q(name__icontains=query)
        ).order_by('-usage_count', 'name')

class AuthorRepository(BaseRepository):
    def search(self, query):
        return self.model.objects.filter(
            Q(name__icontains=query) | Q(email__icontains=query)
        ).order_by('name')
```

### Service Layer

Search is exposed through service methods:

```python
# apps/content/services.py
class ContentCategoryService(BaseService[ContentCategoryRepository]):
    def search(self, query, content_type=None):
        return self.repository.search(query, content_type)

class ContentTagService(BaseService[ContentTagRepository]):
    def search(self, query):
        return self.repository.search(query)

class AuthorService(BaseService[AuthorRepository]):
    def search(self query):
        return self.repository.search(query)
```

### View Layer

Views consume service methods and format results:

```python
# apps/content/views.py
class GlobalSearchView(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        query = self.request.GET.get('q', '').strip()
        if query:
            articles = Article.objects.filter(
                Q(title__icontains=query) | Q(content__icontains=query)
            )[:5]
            # ... format and return results
```

## Search Performance

### Database Indexes

Search performance is optimized with database indexes:

| Field | Model | Index Type |
|-------|-------|-----------|
| `title` | Article | B-tree (via unique constraint) |
| `slug` | Article | B-tree (unique) |
| `name` | ContentCategory | B-tree |
| `slug` | ContentCategory | B-tree (unique) |
| `name` | ContentTag | B-tree (unique) |
| `name` | Author | B-tree |

### Query Optimization

- `icase` lookups use database indexes efficiently
- Results are limited with `[:5]` slices
- `select_related()` and `prefetch_related()` used where applicable
- Pagination limits list view queries

### Future Improvements

Potential enhancements for production:

1. **Full-text search** — PostgreSQL `SearchVector` / `SearchQuery`
2. **Search indexing** — Background job for index updates
3. **Fuzzy matching** — Handle typos and partial matches
4. **Search analytics** — Track popular queries
5. **Auto-suggest** — Real-time suggestions as user types
6. **Highlight matches** — Bold matching text in results

## Public Website Search

### Search Modal

The public website includes a search modal component:

```html
<!-- templates/website/components/search_modal.html -->
<div x-show="searchOpen" class="fixed inset-0 z-50 ...">
    <input
        type="search"
        hx-get="/search/"
        hx-trigger="input changed delay:300ms"
        hx-target="#search-results"
        placeholder="Cari artikel, podcast, program..."
    >
    <div id="search-results"></div>
</div>
```

### Search Results Page

A dedicated search results page exists:

```html
<!-- templates/website/search.html -->
{% extends 'website/main.html' %}
<!-- Full-page search results with filters -->
```

### URL

```
GET /search/?q={query}
```
