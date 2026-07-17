# Kabulhaden CMS — Performance Optimization Guide

Performance tuning for the Kabulhaden CMS at every layer.

---

## Table of Contents

1. [Gunicorn Tuning](#gunicorn-tuning)
2. [Database Optimization](#database-optimization)
3. [Static Files & WhiteNoise](#static-files--whitenoise)
4. [Nginx Optimization](#nginx-optimization)
5. [Django Optimization](#django-optimization)
6. [Frontend Optimization](#frontend-optimization)
7. [Docker Resource Limits](#docker-resource-limits)
8. [Caching Strategy](#caching-strategy)

---

## Gunicorn Tuning

Configuration in `gunicorn.conf.py`:

### Worker Count

```python
# Rule: (2 × CPU cores) + 1
# For a 2-core server:
workers = 5

# For a 4-core server:
workers = 9
```

### Worker Class

```python
# Use gthread for I/O-bound work (recommended for Django)
worker_class = "gthread"
threads = 2  # per worker

# Total concurrent requests = workers × threads = 5 × 2 = 10
```

### Timeouts

```python
timeout = 120        # Kill workers after 120s (adjust for slow endpoints)
graceful_timeout = 30  # Time for graceful shutdown
keepalive = 5        # Keep-alive for connections
```

### Environment Variables

```env
GUNICORN_WORKERS=5
GUNICORN_THREADS=2
GUNICORN_TIMEOUT=120
```

---

## Database Optimization

### Connection Pooling

For high-traffic, consider PgBouncer:

```yaml
# Add to docker-compose.yml
services:
  pgbouncer:
    image: edoburu/pgbouncer:1.21.0
    environment:
      DATABASE_URL: postgres://kabulhaden_user:password@db:5432/kabulhaden_db
      POOL_MODE: transaction
      MAX_CLIENT_CONN: 200
      DEFAULT_POOL_SIZE: 20
    depends_on:
      - db
```

### Query Optimization

```python
# Use select_related for ForeignKey joins
articles = Article.objects.select_related('author', 'category').all()

# Use prefetch_related for reverse FK / M2M
articles = Article.objects.prefetch_related('tags', 'comments').all()

# Use only() to limit columns
articles = Article.objects.only('title', 'slug', 'published_at')

# Use values() for dictionaries (less ORM overhead)
titles = Article.objects.values_list('title', flat=True)[:100]
```

### Database Indexes

```python
# In models.py
class Article(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    status = models.CharField(max_length=20)
    published_at = models.DateTimeField(null=True)

    class Meta:
        indexes = [
            models.Index(fields=['status', '-published_at']),
            models.Index(fields=['slug']),
        ]
```

### PostgreSQL Tuning

```sql
-- Check slow queries
SELECT query, mean_exec_time, calls
FROM pg_stat_statements
ORDER BY mean_exec_time DESC LIMIT 10;

-- Check table bloat and recommend vacuum
SELECT relname, n_live_tup, n_dead_tup,
       round(n_dead_tup::numeric / NULLIF(n_live_tup, 0) * 100, 1) AS dead_pct
FROM pg_stat_user_tables
WHERE n_dead_tup > 10000
ORDER BY n_dead_tup DESC;
```

---

## Static Files & WhiteNoise

### WhiteNoise Configuration

Already configured in `base.py`:

```python
STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}
```

This provides:
- **Brotli compression** (best ratio)
- **Gzip fallback** (for older browsers)
- **Cache-busting hashes** in filenames
- **Manifest file** for efficient lookups

### Static File Best Practices

```bash
# Always collect static in production
python manage.py collectstatic --noinput --clear

# Pre-compress static files (run once after deploy)
python manage.py collectstatic --noinput
```

### WhiteNoise Middleware Order

```python
# Must be right after SecurityMiddleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # ← Second
    ...
]
```

---

## Nginx Optimization

### Gzip Settings

```nginx
gzip on;
gzip_vary on;
gzip_proxied any;
gzip_comp_level 6;
gzip_min_length 256;
gzip_types text/plain text/css text/xml text/javascript
           application/json application/javascript application/xml
           application/rss+xml image/svg+xml;
```

### Static File Caching

```nginx
location /static/ {
    alias /app/static_root/;
    expires 30d;
    add_header Cache-Control "public, immutable";
    access_log off;
}
```

### Connection Tuning

```nginx
worker_processes auto;
worker_connections 1024;
multi_accept on;
keepalive_timeout 65;
tcp_nopush on;
tcp_nodelay on;
```

### Rate Limiting

```nginx
# Add to http block
limit_req_zone $binary_remote_addr zone=login:10m rate=5r/m;

# Apply to login endpoint
location /akun/masuk/ {
    limit_req zone=login burst=3 nodelay;
    proxy_pass http://django;
}
```

---

## Django Optimization

### Template Caching

```django
{% load cache %}

{# Cache block for 5 minutes (300 seconds) #}
{% cache 300 sidebar %}
    {% include "partials/sidebar.html" %}
{% endcache %}
```

### QuerySet Caching

```python
from django.core.cache import cache

def get_recent_articles():
    cache_key = 'articles:recent:10'
    articles = cache.get(cache_key)
    if articles is None:
        articles = list(Article.objects.filter(status='published')
                       .select_related('author')
                       .order_by('-published_at')[:10])
        cache.set(cache_key, articles, timeout=300)  # 5 minutes
    return articles
```

### Radio Engine Caching

Already configured via env vars:

```env
RADIO_CACHE_TTL_NOW_PLAYING=15    # 15 seconds
RADIO_CACHE_TTL_LISTENER=30       # 30 seconds
RADIO_CACHE_TTL_HEALTH=60         # 60 seconds
```

---

## Frontend Optimization

### Tailwind CSS

```bash
# Production: minified build
npm run build

# Dev: unminified for debugging
npm run build:dev
```

### Asset Loading

```django
{# Use defer for non-critical scripts #}
<script src="{% static 'js/app.js' %}" defer></script>

{# Preload critical CSS #}
<link rel="preload" href="{% static 'css/styles.css' %}" as="style">

{# Lazy load images #}
<img src="..." loading="lazy" alt="...">
```

### Alpine.js & HTMX

```html
{# HTMX: Use hx-boost for full-page transitions #}
<div hx-boost="true">

{# Alpine.js: Use x-cloak to prevent FOUC #}
<style>[x-cloak] { display: none !important; }</style>
<div x-data x-cloak>...</div>
```

---

## Docker Resource Limits

```yaml
services:
  web:
    deploy:
      resources:
        limits:
          cpus: '2.0'
          memory: 1G
        reservations:
          cpus: '1.0'
          memory: 512M

  db:
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 512M

  nginx:
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 256M
```

---

## Caching Strategy

### Layer 1: Browser Cache

Nginx serves static files with long expiry (30 days). WhiteNoise's cache-busting hashes ensure new versions are fetched.

### Layer 2: Application Cache

```python
# Django cache framework (add to settings)
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://redis:6379/1',
    }
}
```

### Layer 3: Database Cache

```python
# Session storage via database (default)
SESSION_ENGINE = 'django.contrib.sessions.backends.db'

# For high traffic, switch to cache-backed sessions
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'default'
```

### Layer 4: CDN (Future)

For global reach, consider Cloudflare or similar CDN in front of Nginx.
