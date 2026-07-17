# 0020. Use Redis Caching (Future)

**Status:** Planned
**Date:** 2024-07-15

## Context

The application currently uses Django's default file-based cache and the database for session storage and caching. As the system grows, performance bottlenecks will emerge from:

- Repeated database queries for singleton settings (loaded on every request)
- Radio now-playing data fetched from external APIs every 15-60 seconds
- Session data stored in the database or file system
- Celery task queue (if adopted) requiring a message broker

File-based caching has limitations:

- No atomic operations for cache invalidation
- File locking under concurrent access
- No TTL-based expiration without custom logic
- Cannot be shared across multiple application instances

## Decision (Planned)

Migrate to **Redis** for:

### 1. Application Caching

```python
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': env.str('REDIS_URL', 'redis://127.0.0.1:6379/1'),
        'TIMEOUT': 300,
        'OPTIONS': {
            'MAX_ENTRIES': 1000,
        }
    }
}
```

Use cases:

- Cache `SiteSettings.load()`, `SEOSettings.load()`, and other singleton settings (TTL: 5 minutes)
- Cache radio now-playing responses (TTL: 15 seconds)
- Cache listener statistics (TTL: 30 seconds)
- Cache health check results (TTL: 60 seconds)

### 2. Session Storage

```python
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'default'
```

### 3. Future Celery Broker

```python
CELERY_BROKER_URL = env.str('REDIS_URL', 'redis://127.0.0.1:6379/0')
CELERY_RESULT_BACKEND = env.str('REDIS_URL', 'redis://127.0.0.1:6379/0')
```

### Current State

Currently, `django.core.cache.cache` is used with file-based backend:

```python
from django.core.cache import cache

# In RadioStationService
cache_key = f'now_playing_{station_id}'
cached = cache.get(cache_key)
if cached:
    return cached
# ... fetch from API ...
cache.set(cache_key, data, timeout=CACHE_TTL_NOW_PLAYING)
```

## Consequences

**Positive:**

- Redis provides atomic operations and TTL-based expiration out of the box.
- In-memory caching is 10-100x faster than file-based cache.
- Redis can be shared across multiple application instances (horizontal scaling).
- Session storage in Redis eliminates file-based session locking.
- Single Redis instance can serve caching, sessions, and Celery broker roles.
- Django 5.0 has built-in `django.core.cache.backends.redis.RedisCache`.

**Negative:**

- Redis adds an infrastructure dependency (another service to run and monitor).
- Memory usage grows with cached entries (mitigated by TTL and `MAX_ENTRIES`).
- Cache invalidation requires careful design to avoid stale data.

**Mitigations:**

- Redis Alpine image is lightweight (~30MB) and fast to start.
- TTL-based expiration handles most invalidation automatically.
- `docker-compose.yml` can add a Redis service with minimal configuration.
- File-based cache continues to work as a fallback during migration.

## Migration Path

When performance profiling indicates the need:

1. Add `redis` service to `docker-compose.yml`
2. Update `CACHES` setting in `config/settings/base.py`
3. Set `SESSION_ENGINE` to cache-backed sessions
4. Update `requirements/base.txt` with `django>=5.0` (built-in Redis support)
5. No code changes required — `django.core.cache.cache` API is unchanged
