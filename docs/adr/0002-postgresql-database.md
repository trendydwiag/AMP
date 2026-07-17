# 0002. Use PostgreSQL in Production

**Status:** Accepted
**Date:** 2024-07-01

## Context

The CMS requires a production database that supports:

- Complex relational queries across 10+ models per module
- `JSONField` for storing raw API responses (radio adapter data, settings)
- Full-text search capabilities for articles, programs, and podcasts
- Reliable concurrent access for multiple admin users
- Extensibility for future needs (pg_trgm, UUID generation)

For local development, a zero-configuration database is preferred to reduce onboarding friction.

## Decision

- **Production:** PostgreSQL 16 (Alpine image via Docker)
- **Development:** SQLite3 (`db.sqlite3`) as the default fallback

The connection is configured via `django-environ`:

```python
DATABASES = {
    'default': env.db('DATABASE_URL', default='sqlite:///db.sqlite3')
}
```

In Docker, `DATABASE_URL` points to the `db` service:

```
postgres://kabulhaden_user:kabulhaden_pass@db:5432/kabulhaden_db
```

## Consequences

**Positive:**

- `JSONField` is natively supported by PostgreSQL (used extensively in radio adapter `raw_response` fields).
- Full-text search with `SearchVector` and `SearchQuery` for content search without external dependencies.
- ACID compliance ensures data integrity for concurrent admin operations.
- `psycopg[binary]` provides a fast, pip-installable adapter.
- PostgreSQL 16 Alpine image is lightweight (~80MB) and fast to start.

**Negative:**

- SQLite lacks some PostgreSQL features (JSON operators, full-text search syntax).
- Developers must be aware of PostgreSQL-specific behavior when testing locally.

**Mitigations:**

- Use Django ORM abstractions that work across both backends.
- CI/CD runs tests against PostgreSQL to catch compatibility issues.
- `docker-compose up` provides PostgreSQL locally with zero manual setup.
