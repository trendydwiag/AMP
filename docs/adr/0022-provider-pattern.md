# ADR-0022: Provider Pattern for Platform Services

## Status
Accepted

## Date
2026-07-17

## Context
The platform needs to support multiple external service providers for streaming, storage, email, AI, notifications, analytics, and payments. Different partners may use different providers (e.g., one partner uses Icecast, another uses RadioBoss). The existing radio adapter pattern is excellent but limited to radio streaming.

## Decision
We generalize the adapter pattern into a **Provider Pattern** with abstract base classes and a central registry.

### Provider Categories:
1. **StreamingProvider** - Audio streaming (RadioBoss, Icecast, AzuraCast, Shoutcast)
2. **StorageProvider** - File storage (Local, S3, GCS)
3. **EmailProvider** - Email delivery (Django SMTP, SendGrid, Mailgun)
4. **AIProvider** - AI services (OpenAI, local LLM)
5. **NotificationProvider** - Push notifications, SMS
6. **AnalyticsProvider** - Pageviews, visitor stats
7. **PaymentProvider** - Payment processing (future)

### Architecture:
- All providers inherit from `BaseProvider` with `configure()`, `health_check()`, `get_info()`
- Category-specific providers add domain methods (e.g., `StreamingProvider.get_stream_url()`)
- `ProviderResult` dataclass wraps all return values (success, data, error, metadata)
- **Global Registry** maps `(category, slug)` -> provider class
- Partners can override providers via `Partner.provider_overrides` JSON field
- `get_provider_for_partner(partner, category)` resolves the correct provider

### Default Providers:
- **LocalStorageProvider** - Django's default file storage
- **DjangoEmailProvider** - Django's SMTP email backend

### Radio Adapters Integration:
- Existing `RadioProviderAdapter` in `apps/radio/adapters/` continues to work
- Future: Radio adapters will be wrapped as `StreamingProvider` implementations
- No disruption to existing radio functionality

## Consequences
- All provider implementations must handle errors and return `ProviderResult`
- New providers are registered via `register_provider(category, slug, class)` at import time
- Partner overrides take precedence over global defaults
- Provider health checks can be exposed in platform dashboard
- Backward compatible: existing radio adapters are untouched

## References
- `apps/platform/providers/base.py` - Abstract provider interfaces
- `apps/platform/providers/registry.py` - Provider registry
- `apps/platform/providers/local_storage.py` - Default storage provider
- `apps/platform/providers/django_email.py` - Default email provider
- `apps/radio/adapters/base.py` - Existing radio adapter (reference)
- ADR-0010: Multi-Provider Radio Engine
