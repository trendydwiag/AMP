# 0012. Use WhiteNoise for Static Files

**Status:** Accepted
**Date:** 2024-07-15

## Context

Django's built-in `staticfiles` app is designed for development, not production. Serving static files in production requires:

- Efficient serving without Django's overhead
- Brotli/Gzip compression
- Cache headers for browsers
- Handling `Cache-Control` and `ETag` headers
- Works behind reverse proxies

CDN-based solutions (CloudFront, Cloudflare) are ideal for high-traffic sites but add cost and complexity for a radio station CMS.

## Decision

We use **WhiteNoise 6.7+** with Brotli compression for serving static files directly from Django.

Configuration in `config/settings/base.py`:

```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Immediately after SecurityMiddleware
    # ...
]

STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}
```

WhiteNoise is installed via `requirements/base.txt`:

```
whitenoise[brotli]>=6.7.0
```

## Consequences

**Positive:**

- Brotli compression reduces CSS/JS transfer size by 15-25% vs. Gzip alone.
- `CompressedManifestStaticFilesStorage` creates fingerprinted files for aggressive caching.
- No external service or CDN required — works entirely within Django.
- Positioned as the second middleware (after SecurityMiddleware) for optimal header handling.
- Handles `robots.txt`, `favicon.ico`, and other root static files automatically.

**Negative:**

- Static files are served by Django/Gunicorn, not a dedicated web server (Nginx).
- For very high traffic, this adds load to the application server.
- Manifest storage requires running `collectstatic` after every CSS/JS change.

**Mitigations:**

- A reverse proxy (Nginx) can still serve static files in production if needed.
- WhiteNoise is battle-tested and handles most use cases efficiently.
- `npm run build` + `python manage.py collectstatic` is part of the deployment pipeline.
