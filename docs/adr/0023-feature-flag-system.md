# ADR-0023: Feature Flag System

## Status
Accepted

## Date
2026-07-17

## Context
The platform needs to control feature availability per-partner and globally. Features like podcast, community, AI, advertisement, membership, donation, analytics, themes, and plugins should be toggleable without code changes or deployments.

## Decision
We implement a **Feature Flag System** with database-backed flags, caching, partner-specific overrides, and template tags.

### Architecture:
- **FeatureFlag model**: Global flag with `key`, `is_enabled`, `scope` (GLOBAL/PARTNER), `rollout_percentage`, `config` (JSON), `category`, `required_tier`
- **FeatureFlagPartner model**: Partner-specific overrides with `flag` FK, `partner` FK, `is_enabled`, `config`
- **FeatureFlagLog model**: Audit trail for flag changes
- **FeatureFlagService**: Business logic with caching (5-min TTL)
- **Template tags**: `{% feature_enabled 'key' %}`, `{% feature_config 'key' %}`, `{% feature_gate 'key' %}`

### Resolution Order:
1. Check if flag exists and is globally enabled
2. Check tier requirement (COMMUNITY < STARTER < PROFESSIONAL < ENTERPRISE)
3. Check partner's `feature_overrides` JSON field
4. Check `FeatureFlagPartner` table for explicit override
5. Return result with caching

### Template Usage:
```django
{% load feature_tags %}
{% feature_enabled 'podcast' as podcast_enabled %}
{% if podcast_enabled %}
    <div>Podcast section</div>
{% endif %}

{% feature_gate 'community' %}
    <div>Community forum</div>
{% endfeature_gate %}
```

## Consequences
- Feature flags are checked via cached service calls (minimal DB impact)
- Partners can override global flags without platform admin intervention
- Tier-based gating enforces subscription limits
- All flag changes are audited via FeatureFlagLog
- Template tags make it easy to gate features in any template

## References
- `apps/platform/feature_flags/models.py` - FeatureFlag, FeatureFlagPartner, FeatureFlagLog
- `apps/platform/feature_flags/service.py` - FeatureFlagService
- `apps/platform/feature_flags/templatetags/feature_tags.py` - Template tags
