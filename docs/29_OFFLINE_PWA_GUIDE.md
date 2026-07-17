# 29. Offline PWA Guide (Future)

## Overview

This guide covers implementing a Progressive Web App (PWA) for Kabulhaden CMS to enable offline access, installability, and better mobile experiences. This is a future enhancement to the existing Django web application.

---

## Current State

| Aspect | Status |
|--------|--------|
| Web CMS | Django-based, fully responsive |
| Service Worker | Not implemented |
| Offline Support | None |
| PWA Manifest | Not present |

---

## PWA Architecture for Django

```
┌─────────────────────────────────────────────────┐
│                  Browser                         │
│  ┌─────────────────────────────────────────────┐ │
│  │              Service Worker                  │ │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐   │ │
│  │  │  Cache   │ │ Background│ │  Push    │   │ │
│  │  │  API     │ │  Sync    │ │  API     │   │ │
│  │  └──────────┘ └──────────┘ └──────────┘   │ │
│  └─────────────────────────────────────────────┘ │
│  ┌─────────────────────────────────────────────┐ │
│  │              Web App Manifest               │ │
│  │  - name, icons, theme_color, start_url      │ │
│  │  - display: standalone                      │ │
│  └─────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────┐
│              Django Backend                      │
│  - API endpoints for offline data sync          │
│  - Push notification server (webpush)           │
│  - Cache control headers                        │
└─────────────────────────────────────────────────┘
```

---

## Required Components

### 1. Web App Manifest

```json
// static/manifest.json
{
  "name": "Kabulhaden CMS",
  "short_name": "Kabulhaden",
  "description": "Community Radio Content Management System",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#1e3a5f",
  "theme_color": "#1e3a5f",
  "orientation": "any",
  "icons": [
    {
      "src": "/static/icons/icon-192x192.png",
      "sizes": "192x192",
      "type": "image/png",
      "purpose": "any maskable"
    },
    {
      "src": "/static/icons/icon-512x512.png",
      "sizes": "512x512",
      "type": "image/png",
      "purpose": "any maskable"
    }
  ]
}
```

### 2. Service Worker

```javascript
// static/sw.js
const CACHE_NAME = 'kabulhaden-v1';
const STATIC_CACHE = 'kabulhaden-static-v1';
const DYNAMIC_CACHE = 'kabulhaden-dynamic-v1';

const STATIC_ASSETS = [
  '/',
  '/static/css/main.css',
  '/static/js/main.js',
  '/manifest.json',
];

// Install: Cache static assets
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(STATIC_CACHE)
      .then((cache) => cache.addAll(STATIC_ASSETS))
  );
});

// Activate: Clean old caches
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(
        keys.filter((key) => key !== STATIC_CACHE)
            .map((key) => caches.delete(key))
      )
    )
  );
});

// Fetch: Cache-first for static, network-first for API
self.addEventListener('fetch', (event) => {
  const { request } = event;
  
  if (request.url.includes('/api/')) {
    // Network-first for API calls
    event.respondWith(networkFirst(request));
  } else {
    // Cache-first for static assets
    event.respondWith(cacheFirst(request));
  }
});

async function cacheFirst(request) {
  const cached = await caches.match(request);
  return cached || fetch(request);
}

async function networkFirst(request) {
  try {
    const response = await fetch(request);
    const cache = await caches.open(DYNAMIC_CACHE);
    cache.put(request, response.clone());
    return response;
  } catch (error) {
    return caches.match(request);
  }
}
```

### 3. Django Template Tag

```python
# templatetags/pwa_tags.py
from django import template

register = template.Library()

@register.inclusion_tag('pwa/manifest.html')
def pwa_manifest():
    return {
        'manifest_url': '/static/manifest.json'
    }

@register.simple_tag
def sw_scope():
    return '/'
```

---

## Offline Data Strategy

### Content Cache (Read-Only)

| Content Type | Cache Duration | Priority |
|--------------|----------------|----------|
| News articles | 24 hours | High |
| Program schedules | 12 hours | High |
| Podcast episodes | 7 days | Medium |
| Static pages | 7 days | High |
| User profile | Session | Low |

### Offline Queue (Write Operations)

```python
# Hypothetical offline sync model
class OfflineOperation(models.Model):
    """Queue operations performed while offline."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    operation = models.CharField(max_length=20)  # CREATE, UPDATE, DELETE
    model_name = models.CharField(max_length=100)
    object_id = models.CharField(max_length=100)
    payload = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    synced = models.BooleanField(default=False)
    sync_attempts = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['created_at']
```

---

## Push Notifications

### Server Setup (Django)

```python
# requirements: pywebpush, django-webpush

# settings.py
WEBPUSH_SETTINGS = {
    'VAPID_PUBLIC_KEY': env('VAPID_PUBLIC_KEY'),
    'VAPID_PRIVATE_KEY': env('VAPID_PRIVATE_KEY'),
    'VAPID_CLAIMS': {
        'sub': 'mailto:admin@kabulhaden.id'
    }
}
```

### Notification Types

| Trigger | Payload | Offline? |
|---------|---------|----------|
| Stream live | `{ title: "Radio is live!", body: "Tune in now" }` | No |
| New content | `{ title: "New article published", body: "..." }` | No |
| Scheduled publish | `{ title: "Your content was published" }` | Queue |
| Error alert | `{ title: "Stream disconnected" }` | No |

---

## Installation UX

### Browser Prompt

```
┌────────────────────────────────────┐
│  Install Kabulhaden CMS?           │
│                                    │
│  ✓ Works offline                   │
│  ✓ Fast loading                    │
│  ✓ Access from home screen         │
│                                    │
│  [Cancel]        [Install]         │
└────────────────────────────────────┘
```

### After Installation

```
┌────────────────────────────────────┐
│  ✓ Kabulhaden installed!           │
│                                    │
│  You can now access the CMS from   │
│  your home screen or app drawer.   │
│                                    │
│  [Open]          [Dismiss]         │
└────────────────────────────────────┘
```

---

## Testing PWA Features

### Lighthouse Audit

```bash
# Run Lighthouse PWA audit
npx lighthouse http://localhost:8000 --view \
  --only-categories=pwa \
  --output=html
```

### PWA Checklist

| Criterion | Target |
|-----------|--------|
| HTTPS | Required for production |
| Manifest | Valid, linked in HTML |
| Service Worker | Registered, controls page |
| Offline | App shell loads offline |
| Installable | Meets installability criteria |
| Icons | 192px and 512px provided |

---

## Limitations

| Limitation | Mitigation |
|------------|------------|
| iOS Safari: No push notifications | Use in-app alerts |
| iOS Safari: Limited offline storage | Cache essential content only |
| Storage limit (~50MB) | Aggressive cache eviction |
| No background sync on all browsers | Feature detection + fallback |

---

## Development Roadmap

| Phase | Scope |
|-------|-------|
| 1 | Add manifest.json + basic icons |
| 2 | Service worker for static assets |
| 3 | Offline read-only content cache |
| 4 | Push notifications (pywebpush) |
| 5 | Offline write queue + sync |

---

## Related Documentation

- `28_FUTURE_DESKTOP_GUIDE.md` - Desktop considerations
- `27_FUTURE_MOBILE_GUIDE.md` - Mobile-specific patterns
- `10_RESPONSIVE_GUIDE.md` - Responsive design
- `18_LOADING_STATES.md` - Loading indicators during sync

---

*Last updated: 2026-07-15*
