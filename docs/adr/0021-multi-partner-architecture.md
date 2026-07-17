# ADR-0021: Multi-Partner Architecture via Partner Engine

## Status
Accepted

## Date
2026-07-17

## Context
The platform must evolve from a single radio station CMS into a multi-partner media platform capable of serving unlimited independent media partners (radio stations, podcasts, news outlets). Each partner must have isolated data, settings, themes, and domain configuration while sharing the same codebase and infrastructure.

## Decision
We introduce a **Partner Engine** as the core multi-tenant layer, using a shared-database, shared-schema approach with a `partner` foreign key on all partner-scoped models.

### Key Design Decisions:

1. **Partner as Tenant**: Internally the concept is "tenant" but exposed as "Partner" in UI and API. The `Partner` model in `apps.platform.partner` is the central tenant entity.

2. **Resolution Order**: Partner is resolved per-request via middleware in this order:
   - Domain matching (primary_domain or PartnerDomain table)
   - Subdomain matching (subdomain.kabulhaden.com)
   - HTTP Header (X-Partner-ID / X-Partner-Slug)
   - Session-based (stored in session)
   - Default (first active partner)

3. **PartnerContext**: Attached to `request.partner_context` after resolution. All views, templates, and services can access the current partner.

4. **PartnerMembership**: Users belong to partners with roles (OWNER, ADMINISTRATOR, EDITOR, PRESENTER, VIEWER). A user can belong to multiple partners.

5. **PartnerDomain**: Custom domain mapping with SSL support, verification status, and primary designation.

6. **Partner Limits**: Configurable per-partner limits for users, storage, articles, podcasts, episodes based on tier.

7. **Feature/Provider Overrides**: Partners can override global feature flags and provider selections via JSON fields.

## Consequences
- All new models from Sprint 3.1+ must include a `partner` ForeignKey
- Existing models will be migrated to include optional `partner` FK in future sprints
- The PartnerMiddleware must be added after AuthenticationMiddleware
- Template context always has `partner_context` available
- Backward compatible: existing single-tenant data is associated with a default partner

## References
- `apps/platform/partner/models.py` - Partner, PartnerMembership, PartnerDomain, PartnerInvitation
- `apps/platform/partner/middleware.py` - PartnerMiddleware
- `apps/platform/partner/resolver.py` - PartnerResolver
- `apps/platform/partner/context.py` - PartnerContext
- ADR-0005: Custom User Model
