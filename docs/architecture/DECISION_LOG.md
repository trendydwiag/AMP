# AMP Studio — Architecture Decision Log

This document is the engineering history of AMP Studio. Every significant architectural decision is recorded here with its rationale, alternatives considered, trade-offs, and future migration path.

---

## ADR-001 — Provider-Agnostic Live Radio API Layer
**Sprint:** 3.4D
**Date:** July 17, 2026
**Status:** Accepted

### Decision
Introduce a single internal endpoint (`GET /api/v1/radio/live/`) that all UI components consume for live radio data. The upstream provider URL and credentials live exclusively in Django settings. No template, JS file, or component references the provider URL directly.

### Reason
The demo deadline (July 21, 2026) required wiring real stream data from Broadcastindo quickly without coupling every widget to a specific provider. A provider-agnostic layer allows the integration to be "temporary" in the right way: swappable by changing two env vars, not by editing templates.

### Alternatives Considered
1. **Hardcode `a7.siar.us` in JS fetch calls** — Rejected: couples the UI to a specific provider; impossible to swap without hunting down every template. Also exposes the provider URL publicly.
2. **Use the existing `/radio/api/status/` endpoint** — Rejected: that endpoint is tied to the DB-backed `RadioStation`/`RadioProvider` models and requires a configured station record. No station record exists in the demo environment.
3. **Proxy via Nginx** — Rejected: over-engineered for a temporary integration; adds infrastructure dependency without architectural benefit.
4. **Direct AzuraCast adapter on existing views** — Rejected: the existing radio views are DB-model-driven; adapting them would have required model changes, risking data integrity.

### Trade-offs
| Pro | Con |
|-----|-----|
| Zero UI changes to swap providers | `program` field is always `null` until schedule integration is wired |
| Offline fallback is centralized — one place to fix | Single endpoint is a new cache invalidation surface |
| Cache layer (20 s) reduces upstream hammering | Cache means listeners may see data up to 20 s stale |
| No provider URL in any client-facing file | Adds a new URL namespace (`/api/v1/`) that must be documented |

### Impact
- All widgets (`radio-player.js`, `amp-studio.js`, `streaming_center.html`) now share a single data contract
- Future providers require only: a new adapter file + one ADAPTER_MAP entry + two env var changes
- No DB migration required

### Future Migration Path
When the official AMP Streaming Connector is ready:
1. Create `apps/streaming/connectors/BroadcastindoConnector` implementing the full connector protocol
2. Register it in the connector registry
3. Change `STREAM_PROVIDER` env var to the new key
4. Delete `apps/radio/adapters/broadcastindo.py` — no other files change

---

## ADR-002 — BroadcastindoAdapter Inherits from RadioProviderAdapter
**Sprint:** 3.4D
**Date:** July 17, 2026
**Status:** Accepted

### Decision
The Broadcastindo adapter fits the existing `RadioProviderAdapter` abstract base class in `apps/radio/adapters/base.py` and is registered in the same `ADAPTER_MAP` alongside AzuraCast, Icecast, RadioBoss, and Shoutcast.

### Reason
The existing adapter pattern was purpose-built for exactly this use case. Fitting into the pattern instead of creating a one-off class costs nothing and keeps the codebase consistent.

### Alternatives Considered
1. **Standalone function (not a class)** — Rejected: would be inconsistent with the adapter pattern and couldn't be injected by the `get_adapter()` factory.
2. **Subclass of AzuraCastAdapter** — Considered, since Siar.us returns AzuraCast-format JSON. Rejected: the Broadcastindo endpoint is a full nowplaying URL, not the `/api/station/<sc>/nowplaying` pattern that `AzuraCastAdapter` constructs. Parsing is sufficiently different to warrant a separate class.

### Trade-offs
- Slight code duplication of JSON parsing logic vs. AzuraCast — acceptable for clarity and isolation
- Both `get_now_playing()` and `get_listener_count()` call `_fetch_nowplaying_data()` internally (one HTTP request per call pair) — an optimization to note if the endpoint becomes slow

### Impact
- Maintains the single-adapter-per-provider principle
- `get_adapter('BROADCASTINDO')` works identically to all other providers

### Future Migration Path
When replaced by the AMP Streaming Connector, remove `BroadcastindoAdapter` and the `'BROADCASTINDO'` ADAPTER_MAP entry. The connector registry handles its own dispatch.

---

## ADR-003 — Django Cache for Live Radio Response (20 s TTL)
**Sprint:** 3.4D
**Date:** July 17, 2026
**Status:** Accepted

### Decision
`LiveRadioAPIView` caches the upstream provider response in Django's default cache backend for 20 seconds (configurable via `STREAM_CACHE_TTL`).

### Reason
Without caching, every widget poll (radio-player.js: 25 s, streaming_center: 30 s) would hit the upstream provider directly. With multiple concurrent users, this would produce hammering behavior. 20 s is a safe floor: stale enough to reduce load, fresh enough for the listener count to feel real-time.

### Alternatives Considered
1. **No cache** — Rejected: too aggressive on upstream; each page load triggers a provider fetch.
2. **60-second cache** — Too stale for a live stream context; listener count changes frequently.
3. **Redis / separate cache** — Overkill for dev/demo; Django's default cache (in-memory or DB-backed) is sufficient.

### Trade-offs
- Cache means widgets may see data up to 20 s stale — acceptable for listener counts and track metadata
- Cache key `'amp_v1_live_radio'` is a single global key — not per-user or per-station (correct, since there is one station)
- Cache survives between requests; if the provider returns bad data once, it's served for up to 20 s

### Impact
- Upstream provider receives at most 3 requests/minute regardless of concurrent users
- TTL is env-var configurable (`STREAM_CACHE_TTL`) for tuning without code changes

### Future Migration Path
When multiple stations are supported, the cache key should incorporate station ID: `f'amp_v1_live_radio_{station_id}'`.

---

## ADR-004 — Polling Interval Standardized to 20–30 s
**Sprint:** 3.4D
**Date:** July 17, 2026
**Status:** Accepted

### Decision
All client-side polling intervals updated: `radio-player.js` 10 s → 25 s, `streamStatus()` 15 s → 25 s, `streaming_center.html` stays at 30 s.

### Reason
The previous 10 s polling in `radio-player.js` was set when the status endpoint was a cheap DB read. The new endpoint makes an HTTP call to an external provider (cached at 20 s). Polling faster than the cache TTL is wasteful — the client would receive identical cached responses. 25 s aligns with the cache TTL.

### Alternatives Considered
1. **Server-Sent Events (SSE) or WebSocket push** — Ideal long-term; deferred because it requires async server support (Diegand ASGI + Channels) beyond the sprint scope.
2. **Keep 10 s** — Rejected: wasteful; 60%+ of requests would return cached identical data.

### Trade-offs
- 25 s polling means a listener count change takes up to 25 s to appear on the widget — acceptable
- Interval is hardcoded in JS; making it configurable would require passing a Django setting to the frontend (future improvement)

### Future Migration Path
Replace polling with a WebSocket feed once Django Channels is introduced. The widget bindings (`$store.radio.*`) won't need to change — only the data source.
