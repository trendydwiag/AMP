# 0011. Use Singleton Pattern for Settings

**Status:** Accepted
**Date:** 2024-07-15

## Context

The CMS requires system-wide configuration for:

- Site identity (name, logo, tagline)
- SEO metadata
- Email (SMTP) configuration
- Security policies (session timeout, 2FA, lockout)
- Appearance (colors, fonts, dark mode)
- Notification preferences
- Social media links
- Content defaults (pagination, comments)
- Language and timezone
- Media storage settings

Each configuration category needs exactly one row in the database. Multiple rows would create ambiguity about which settings are active.

## Decision

We use a **singleton model pattern** where each settings model enforces a single instance via `pk=1`:

```python
class SiteSettings(TimeStampedModel):
    site_name = models.CharField(max_length=200, default='Kabulhaden CMS')
    # ... other fields ...

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj
```

This pattern is applied to all 10 settings models:

| Model | Purpose |
|-------|---------|
| `SiteSettings` | Site name, tagline, logo, favicon, maintenance mode |
| `SEOSettings` | Meta tags, Open Graph, Google Analytics, custom scripts |
| `EmailSettings` | SMTP backend, host, port, TLS, from address |
| `SecuritySettings` | Session timeout, login attempts, password policy, 2FA |
| `AppearanceSettings` | Colors, fonts, sidebar, compact mode |
| `NotificationSettings` | Email notification triggers |
| `SocialMediaSettings` | Social media profile URLs |
| `ContentSettings` | Pagination, comments, upload limits |
| `LanguageSettings` | Language, date/time format, timezone |
| `MediaSettings` | Storage backend, compression, thumbnails |

Initialization via management command:

```bash
python manage.py init_settings
```

## Consequences

**Positive:**

- `SiteSettings.load()` always returns the single settings instance, creating it if needed.
- No admin UI needed for selecting "which settings to use" — there is only one.
- `TimeStampedModel` tracks when settings were last updated.
- `init_settings` command creates all 10 singleton rows in one operation.
- Settings are easily cacheable (see ADR-0020).

**Negative:**

- Every settings save touches `pk=1`, which can cause row-locking contention under heavy concurrent admin use.
- The `save()` override must be remembered in every subclass.
- Database stores settings that could theoretically be in environment variables.

**Mitigations:**

- Admin settings are updated infrequently (not a hot path).
- The pattern is consistent across all 10 models, reducing cognitive load.
- Environment variables (via `django-environ`) handle secrets and deployment-specific values.
