# 0001. Use Django as Web Framework

**Status:** Accepted
**Date:** 2024-07-01

## Context

Kabulhaden CMS needs a web framework that can handle:

- Server-rendered HTML with complex form handling
- Built-in admin interface for content management
- Robust ORM for relational data modeling
- Authentication, authorization, and session management out of the box
- Large ecosystem of third-party packages
- Mature documentation and community support

The team has Python expertise, and the project targets small-to-medium deployment environments where rapid development and maintainability are priorities over raw throughput.

## Decision

We use **Django 5.0.x** as the sole web framework for both the admin CMS and the public-facing website.

Key selections:

- **Django 5.0.7+** — Latest LTS-aligned release with `STORAGES` API, field groupings, and modern Python support.
- **Django template engine** — Server-side rendering with `{% extends %}`, `{% block %}`, context processors.
- **Class-based views** — `TemplateView`, `ListView`, `DetailView` for the website module; function-based views for API endpoints.
- **Django admin** — Used as the base for the internal management panel with custom `ModelAdmin` classes.

## Consequences

**Positive:**

- Built-in admin saves months of UI work for internal content management.
- ORM handles complex relations (ForeignKey, OneToOne, JSONField) with Pythonic query syntax.
- Django's `AUTH_USER_MODEL` mechanism supports our custom User model from day one.
- Massive ecosystem: `django-axes`, `django-environ`, `whitenoise`, and more.
- Template inheritance and context processors simplify HTML organization.

**Negative:**

- Django's synchronous request cycle limits WebSocket/SSE support without ASGI channels.
- Template language is less expressive than Jinja2 for complex frontend logic.
- ORM migrations can become complex with heavy schema changes over time.

**Mitigations:**

- Alpine.js and HTMX handle client-side interactivity without a JavaScript framework.
- Django 5.0 supports ASGI for future async needs.
- `django-environ` manages environment-specific configuration cleanly.
