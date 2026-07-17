# 0018. Website Module is Presentation-Only

**Status:** Accepted
**Date:** 2024-07-15

## Context

The public website module (`apps/website/`) serves as the visitor-facing frontend for Kabulhaden CMS. It displays:

- Homepage with live radio player, programs, episodes, articles
- Program listing and detail pages
- Podcast listing, detail, and episode pages
- News articles and categories
- Schedule and broadcast information
- Community discussions
- Partner/sponsor pages
- Contact, privacy, and terms pages

The concern is that website views might bypass the Service-Repository pattern and query models directly, leading to:

- Duplicated query logic between admin and public views
- Inconsistent business rules
- Difficulty testing website behavior independently
- Tight coupling to model schema changes

## Decision

The website module **never queries models directly**. All data access goes through Service classes:

```python
# CORRECT — services/website/views.py
from apps.broadcast.services import ProgramService, EpisodeService, BroadcastService

class HomeView(TemplateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        program_svc = ProgramService()
        context['featured_programs'] = program_svc.get_featured_programs()

        episode_svc = EpisodeService()
        context['latest_episodes'] = episode_svc.get_published().select_related('program')[:6]

        broadcast_svc = BroadcastService()
        context['today_schedule'] = broadcast_svc.get_today_schedule()
        context['current_broadcast'] = broadcast_svc.get_current_broadcast()
        return context
```

Every view wraps service calls in try/except to gracefully degrade:

```python
try:
    podcast_svc = PodcastService()
    context['featured_podcasts'] = podcast_svc.get_featured()[:4]
except Exception:
    context['featured_podcasts'] = []
```

## Consequences

**Positive:**

- Website views are decoupled from model internals — changing a model field only requires updating the repository.
- Service classes are shared between admin views and website views, ensuring consistent behavior.
- Each website view is independently testable by mocking services.
- Graceful degradation ensures the website renders even if one module's service fails.
- No direct `Model.objects.filter()` calls in website views.

**Negative:**

- Extra indirection adds a small performance overhead per request.
- Service classes must expose enough query methods to cover website display needs.
- Each new website section requires wiring up the corresponding service.

**Mitigations:**

- The overhead is negligible for a server-rendered CMS (sub-millisecond per service call).
- Service methods like `get_featured_programs()`, `get_published()`, `get_active()` are designed to serve both admin list views and website listings.
- The `try/except` pattern prevents one broken service from crashing the entire page.
