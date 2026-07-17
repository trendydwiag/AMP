# Aradhana Media Platform - Architecture

## Overview

The Aradhana Media Platform (AMP) transforms from a single radio station CMS into a **reusable commercial platform** for unlimited independent media partners. One codebase, infinite partners.

## Directory Structure

```
apps/platform/
├── __init__.py
├── apps.py                  # PlatformConfig
├── choices.py               # PartnerStatus, PartnerTier, ProviderCategory, ThemeMode, etc.
├── context_processors.py    # partner_context, platform_settings (with branding)
├── models.py                # Re-exports all models for Django discovery
├── urls.py                  # Platform admin URLs
├── views.py                 # Platform dashboard, partner CRUD, provider/flag/theme management
├── tests.py                 # 64 tests: resolver, middleware, service, feature flags, domain, security
├── partner/
│   ├── models.py            # Partner, PartnerMembership, PartnerDomain, PartnerInvitation
│   ├── middleware.py         # PartnerMiddleware (session override for admin users)
│   ├── resolver.py           # PartnerResolver (domain, subdomain, header, session, default)
│   ├── context.py            # PartnerContext dataclass (with config, branding helpers)
│   ├── service.py            # PartnerService: CRUD, switch, config loading, member management
│   └── __init__.py           # Exports all partner components
├── providers/
│   ├── base.py               # Abstract provider interfaces (Streaming, Storage, Email, AI, etc.)
│   ├── registry.py           # Provider registry and resolution
│   ├── local_storage.py      # Default local storage provider
│   └── django_email.py       # Default Django email provider
├── feature_flags/
│   ├── models.py             # FeatureFlag, FeatureFlagPartner, FeatureFlagLog
│   ├── service.py            # FeatureFlagService (caching, overrides, tier gating)
│   └── templatetags/
│       └── feature_tags.py   # {% feature_enabled %}, {% feature_config %}, {% feature_gate %}
├── plugins/
│   ├── base.py               # PluginBase, PluginMeta, PluginHook + built-in hooks
│   └── registry.py           # Plugin and hook registry
├── themes/
│   ├── models.py             # PartnerTheme, ThemePreset
│   ├── service.py            # ThemeService (CSS generation, presets)
│   └── templatetags/
│       └── theme_tags.py     # {% partner_css_variables %}, {% partner_theme_class %}, {% partner_logo %}
├── domains/
│   └── engine.py             # DomainEngine: domain resolution, subdomain generation, DNS verification
├── security/
│   └── tenant.py             # TenantIsolation, AuditLogger, require_partner_access decorator
├── management/
│   └── commands/
│       └── seed_platform.py  # Seed default partner + 10 feature flags
├── utils/
│   └── __init__.py           # require_partner, get_partner_from_request, partner_required_json
└── templates/platform/       # Admin templates for platform management
```

## Core Concepts

### 1. Partner (Tenant)
Every piece of content, user, and configuration belongs to a **Partner**. Partners are resolved per-request via the PartnerMiddleware.

**Resolution Order (with Admin Override):**
1. Admin Session Override: SUPERUSER/ADMINISTRATOR can switch partners via AMP Studio
2. Domain (primary_domain or PartnerDomain table)
3. Subdomain (subdomain.kabulhaden.com)
4. HTTP Header (X-Partner-ID / X-Partner-Slug)
5. Session
6. Default (configured PLATFORM_DEFAULT_PARTNER_SLUG)

### 2. Provider Pattern
All external services (streaming, storage, email, AI, etc.) are abstracted behind provider interfaces. Partners can override which provider to use.

### 3. Feature Flags
Features are toggleable per-partner via database-backed flags. Supports tier-based gating and percentage rollouts.

### 4. Plugin Architecture
Extensibility via plugins that hook into content publishing, user login, stream events, and dashboard rendering.

### 5. Theme Engine
Per-partner theming via CSS custom property overrides. Supports presets and custom CSS.

## Integration Points

### Middleware Stack
```
PartnerMiddleware (after AuthenticationMiddleware)
```

### Template Context
```django
{{ partner_context }}        # PartnerContext object
{{ current_partner }}        # Partner model instance
{{ partner_name }}           # Partner name string
{{ partner_tier }}           # Partner tier string
{{ partner_primary_color }}  # Partner primary hex color
{{ partner_secondary_color }}# Partner secondary hex color
{{ partner_accent_color }}   # Partner accent hex color
{{ partner_logo_url }}       # Partner logo URL (if set)
{{ partner_tagline }}        # Partner tagline
{{ partner_features }}       # Dict of feature overrides
{{ platform_name }}          # "Aradhana Media Platform"
{{ platform_version }}       # "1.0.0"
```

### Settings
```python
PLATFORM_BASE_DOMAIN = 'kabulhaden.com'
PLATFORM_DEFAULT_PARTNER_SLUG = 'kabulhaden-online'
PLATFORM_FEATURE_FLAGS_ENABLED = True
PLATFORM_PLUGINS_ENABLED = True
```

## Database Schema

### Partner Models (9 tables)
| Model | Purpose |
|-------|---------|
| Partner | Tenant entity with limits, branding, domain config, soft delete |
| PartnerMembership | User-Partner relationship with role |
| PartnerDomain | Custom domain mapping |
| PartnerInvitation | Pending user invitations |
| FeatureFlag | Global feature toggle |
| FeatureFlagPartner | Partner-specific flag override |
| FeatureFlagLog | Audit trail for flag changes |
| PartnerTheme | Per-partner theme configuration |
| ThemePreset | Pre-defined theme templates |

### Partner FK on Business Entities (Tenant Isolation)
| Model | FK Field | Purpose |
|-------|----------|---------|
| news.Category | partner | News categories per partner |
| news.Tag | partner | Tags per partner |
| news.Article | partner | Articles per partner |
| podcast.Podcast | partner | Podcasts per partner |
| podcast.PodcastEpisode | partner | Episodes per partner |
| radio.RadioStation | partner | Radio stations per partner |
| broadcast.Program | partner | Broadcast programs per partner |
| broadcast.Episode | partner | Broadcast episodes per partner |
| media_manager.Folder | partner | Media folders per partner |
| media_manager.MediaFile | partner | Media files per partner |

## URL Structure
```
/platform/                     # Platform dashboard
/platform/partners/            # Partner list
/platform/partners/create/     # Create partner
/platform/partners/<uuid>/     # Partner detail
/platform/partners/<uuid>/edit/ # Edit partner
/platform/providers/           # Provider list
/platform/features/            # Feature flag list
/platform/themes/              # Theme list
/platform/themes/<uuid>/edit/  # Edit theme

/studio/partner/switch/<uuid>/ # Partner switch (AJAX)
/studio/partner/list/          # Partner list (JSON for switcher)
```

## Security

### Tenant Isolation
- `TenantIsolation.get_partner_queryset(model, partner)` — Filter any model by partner
- `TenantIsolation.check_object_access(obj, request)` — Verify user can access object
- `@require_partner_access` — Decorator enforcing partner access on views

### Audit Logging
- `AuditLogger.log_action(action, user, partner, ...)` — Log security-relevant actions

## Seeding
```bash
python manage.py seed_platform
```
Creates Kabulhaden Online partner + 10 feature flags (podcast, article, ads, community, analytics, sponsor, media_library, api, themes, plugins) + domain entries.
