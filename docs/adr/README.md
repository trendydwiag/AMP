# Architecture Decision Records (ADRs)

This directory contains Architecture Decision Records for the Kabulhaden CMS project.

## What is an ADR?

An Architecture Decision Record captures a significant architectural decision along with its context and consequences. Each ADR describes:

- **Context** — The forces at play (technical, political, social, project-related).
- **Decision** — The change that was proposed and agreed upon.
- **Consequences** — The resulting outcomes, both positive and negative.

ADRs are immutable once accepted. If a decision is reversed, a new ADR is written rather than editing the original.

## How to Use

- **New developers**: Read the ADRs in order to understand why the system is designed the way it is.
- **Contributors**: Check existing ADRs before proposing changes to established patterns.
- **Proposing a new ADR**: Create a new numbered file (`NNNN-title.md`) following the template below.

## ADR Template

```markdown
# NNNN. Title

**Status:** Accepted | Deprecated | Superseded by ADR-NNNN | Planned
**Date:** YYYY-MM-DD

## Context

What is the issue that motivates this decision?

## Decision

What is the change being proposed or decided?

## Consequences

What are the positive and negative outcomes?
```

## Index

| # | Title | Status | Date |
|---|-------|--------|------|
| [0001](0001-use-django.md) | Use Django as Web Framework | Accepted | 2024-07-01 |
| [0002](0002-postgresql-database.md) | Use PostgreSQL in Production | Accepted | 2024-07-01 |
| [0003](0003-service-repository-pattern.md) | Use Service-Repository Pattern | Accepted | 2024-07-01 |
| [0004](0004-uuid-primary-keys.md) | Use UUID Primary Keys | Accepted | 2024-07-01 |
| [0005](0005-custom-user-model.md) | Use Custom User Model | Accepted | 2024-07-01 |
| [0006](0006-tailwind-css.md) | Use Tailwind CSS | Accepted | 2024-07-01 |
| [0007](0007-alpinejs-for-interactivity.md) | Use Alpine.js for Interactivity | Accepted | 2024-07-01 |
| [0008](0008-htmx-for-dynamic-content.md) | Use HTMX for Dynamic Content | Accepted | 2024-07-01 |
| [0009](0009-docker-containerization.md) | Use Docker for Containerization | Accepted | 2024-07-01 |
| [0010](0010-multi-provider-radio-engine.md) | Use Adapter Pattern for Radio Providers | Accepted | 2024-07-15 |
| [0011](0011-singleton-settings-pattern.md) | Use Singleton Pattern for Settings | Accepted | 2024-07-15 |
| [0012](0012-white-noise-static-files.md) | Use WhiteNoise for Static Files | Accepted | 2024-07-15 |
| [0013](0013-axes-brute-force-protection.md) | Use django-axes for Brute Force Protection | Accepted | 2024-07-15 |
| [0014](0014-session-timeout-middleware.md) | Use Custom Session Timeout Middleware | Accepted | 2024-07-15 |
| [0015](0015-indonesian-language-ui.md) | Use Indonesian for UI Strings | Accepted | 2024-07-15 |
| [0016](0016-coffee-color-palette.md) | Use Coffee Color Palette | Accepted | 2024-07-15 |
| [0017](0017-poppins-inter-typography.md) | Use Poppins + Inter Typography | Accepted | 2024-07-15 |
| [0018](0018-website-pure-presentation.md) | Website Module is Presentation-Only | Accepted | 2024-07-15 |
| [0019](0019-factory-function-settings-views.md) | Use _settings_view Factory for Settings Views | Accepted | 2024-07-15 |
| [0020](0020-caching-strategy.md) | Use Redis Caching (Future) | Planned | 2024-07-15 |
| [0021](0021-multi-partner-architecture.md) | Multi-Partner Architecture via Partner Engine | Accepted | 2026-07-17 |
| [0022](0022-provider-pattern.md) | Provider Pattern for Platform Services | Accepted | 2026-07-17 |
| [0023](0023-feature-flag-system.md) | Feature Flag System | Accepted | 2026-07-17 |
| [0024](0024-plugin-architecture.md) | Plugin Architecture | Accepted | 2026-07-17 |
| [0025](0025-per-partner-theme-engine.md) | Per-Partner Theme Engine | Accepted | 2026-07-17 |
