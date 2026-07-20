# Next Sprint Recommendations
**Based on:** Sprint 4.0.1 completion (Documentation Synchronization)
**Demo date:** July 21, 2026
**Prepared:** July 20, 2026

---

## Current Status

| Sprint | Title | Status |
|---|---|---|
| 4.1 | Demo Readiness & Founder Experience | ✅ DONE |
| 4.2 | Media Pipeline Engine | ✅ DONE |
| 4.3 | Radio Live Player Stabilization | ✅ DONE |
| 4.0.1 | Knowledge Base Governance & Documentation Sync | ✅ DONE |

---

## Sprint Recommendations (Post-Demo)

### 🔴 PRIORITY 0 — Critical for Production

**Sprint 4.4 — Wire Program Name to Live API (TD-001)**

**Task:** Connect broadcast schedule to live API
- In `LiveRadioAPIView.get()`, query `apps/broadcast` for currently active schedule slot by current day/time
- Populate `program` field with the on-air program name
- Cache together with upstream data (20s TTL)
- Currently `program` is always null — looks broken in demo

**Effort:** 2–4 hours
**Files:** `apps/radio/views.py` (LiveRadioAPIView), `apps/broadcast/repositories.py` (ScheduleRepository)

---

### 🔴 PRIORITY 1 — Technical Debt

**Sprint 4.5 — Superuser Setup & Platform Migrations (TD-006, TD-007)**

**Task:** Ensure superuser exists and platform migrations are applied
- Run `python manage.py showmigrations` to verify pending migrations
- Apply if safe: `python manage.py migrate`
- Verify superuser login works
- Fix demo_seed admin `is_superuser=True` bug (NEW-002)

**Effort:** 1 hour

---

**Sprint 4.6 — AMP Studio Dashboard Service Extraction (NEW-001)**

**Task:** Extract inline ORM queries from `AMPStudioDashboardView`
- Move ~25+ inline queries to a new `StudioService` or `DashboardService`
- Follow Service-Repository pattern
- Add caching for expensive queries (storage calculation, system health)

**Effort:** 4–6 hours

---

### 🟡 PRIORITY 2 — Medium Priority

**Sprint 4.7 — Automated Tests for LiveRadioAPIView (TD-003)**
- Create `apps/radio/tests/test_live_api.py`
- Test happy path, offline fallback, cache behavior, provider errors
- Mock adapter's `_make_request` method

**Sprint 4.8 — CSP Security Hardening (NEW-003)**
- Add `django-csp` to INSTALLED_APPS and MIDDLEWARE
- Verify CSP headers are actually sent
- Test that media streaming works with CSP restrictions

**Sprint 4.9 — Analytics Dashboard (Real Data)**
- Aggregate `ListenerStatistic` records to dashboard analytics
- Chart listener over time
- Status: view + template exist, data not yet aggregated

---

### ⚪ PRIORITY 3 — Low Priority / Future

| Item | Effort | Notes |
|---|---|---|
| BroadcastindoAdapter optimization (TD-004) | 1 hour | Cache within adapter instance |
| Configurable polling intervals (TD-005) | 1–2 hours | Pass STREAM_CACHE_TTL to frontend via meta tag |
| content/repos.py rename (NEW-004) | 30 min | Rename to repositories.py per convention |
| pyproject.toml cleanup (NEW-005) | 30 min | Sync deps, fix name from "repl-nix-workspace" |
| WebSocket/SSE real-time updates | Multi-day | Requires Django Channels |
| Mobile app | Future scope | — |

---

## Post-Demo Scope

| Item | Reason Deferred |
|---|---|
| WebSocket/SSE real-time updates | Requires Django Channels — multi-day effort |
| Full AMP Streaming Connector | Post-demo replacement for Broadcastindo adapter |
| Mobile app | Future scope |
| Listener history charts with real data | DB records not yet populated from live stream |
| Merge duplicate tag/category models | Breaking change, needs careful migration |
