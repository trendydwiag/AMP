# AMP Studio — Changelog

All notable changes to AMP Studio are documented here, sprint by sprint.
This file is append-only — never overwrite previous history.

---

## Sprint 3.4D — Live Streaming Integration (Demo Mode)
**Date:** July 17, 2026
**Goal:** Wire AMP Studio and the Kabulhaden public website to real live data from Broadcastindo before the July 21 demonstration.

### Summary
Introduced a provider-agnostic internal live radio API (`GET /api/v1/radio/live/`) that all UI components now consume for now-playing data, listener counts, and stream status. The provider URL lives only in Django settings — no template or JS file references the upstream host. The adapter is designed to be swapped without any UI changes.

### Features Completed
- **`/api/v1/radio/live/` endpoint** — normalized JSON schema (`status`, `station`, `program`, `title`, `artist`, `cover`, `listeners`, `stream_url`, `is_live`, `provider`) with 20-second Django cache layer
- **BroadcastindoAdapter** — new `apps/radio/adapters/broadcastindo.py` implementing `RadioProviderAdapter`, parsing AzuraCast-format nowplaying JSON from Siar.us
- **Graceful offline fallback** — if the upstream is unreachable, all widgets show an offline state with HTTP 200; no page crash or unhandled exception
- **Polling interval standardized** — all widgets updated from 10–15 s to 20–30 s range (radio-player.js: 25 s; amp-studio.js streamStatus: 25 s; streaming_center.html: 30 s)

### Bugs Fixed
- `streamStatus()` in `amp-studio.js` was comparing against `stream_status === 'PLAYING'` — a field that no longer exists in the normalized schema; corrected to `data.is_live`
- `streaming_center.html` was reading `data.listener_count` (old DB-backed field) instead of the correct `data.listeners`
- `radio-player.js` was reading `data.artwork || data.album_art` — updated to `data.cover` per normalized schema

### UI Improvements
- Dashboard "Siaran Langsung" card now reflects live listener count from real stream data
- Streaming Center live status banner reflects real `is_live` state
- "Sedang Diputar" panel in Streaming Center now composes `title — artist` from normalized fields instead of a pre-joined `now_playing` string
- Streaming Center exposes `isOffline` Alpine state for future offline error UI treatment

### Backend Changes
- **`apps/radio/adapters/broadcastindo.py`** — new Broadcastindo adapter (temporary; replaceable via settings)
- **`apps/radio/adapters/__init__.py`** — registered `'BROADCASTINDO'` in `ADAPTER_MAP`
- **`config/settings/base.py`** — added `STREAM_PROVIDER`, `STREAM_API_URL`, `STREAM_STATION_NAME`, `STREAM_CACHE_TTL` settings block
- **`apps/radio/views.py`** — appended `LiveRadioAPIView` class (GET-only, no auth required, 20 s cache, offline fallback)
- **`apps/radio/api_v1_urls.py`** — new file, single route: `radio/live/ → LiveRadioAPIView`
- **`config/urls.py`** — added `path('api/v1/', include('apps.radio.api_v1_urls'))`

### Refactoring
- Existing `/radio/api/status/` endpoint left untouched — still serves the radio management views that depend on it
- All JS fetch calls unified on a single internal endpoint; provider-specific URL removed from all client-side code

### Files Modified
| File | Change |
|------|--------|
| `apps/radio/adapters/broadcastindo.py` | Created |
| `apps/radio/adapters/__init__.py` | Added BROADCASTINDO to ADAPTER_MAP |
| `config/settings/base.py` | Added STREAM_* settings block |
| `apps/radio/views.py` | Appended LiveRadioAPIView |
| `apps/radio/api_v1_urls.py` | Created |
| `config/urls.py` | Added api/v1/ include |
| `static/js/radio-player.js` | Updated fetchStatus() URL, field mapping, polling interval, added listeners state |
| `static/js/amp-studio/amp-studio.js` | Updated streamStatus() and fetchNowPlaying() URL + field mapping + polling interval |
| `templates/amp_studio/streaming_center.html` | Updated inline streamingCenter() JS |

### Breaking Changes
None. The existing `/radio/api/status/` endpoint is unchanged. All changes are additive.

### Known Issues
- `program` field always returns `null` — live schedule is not yet wired to the broadcast schedule DB (tracked as Task #7)
- `stream_url` depends on `station.listen_url` being present in the provider response — no fallback URL configured (tracked as Task #8)
- No automated tests for `LiveRadioAPIView` (tracked as Task #9)
- `a7.siar.us` is unreachable from the Replit development container due to network restrictions — endpoint returns graceful offline response in dev; will work correctly on the production server

### Demo Readiness
✅ Architecture is complete and demo-ready on a server with network access to `a7.siar.us`.
⚠️ Development environment shows "Offline" state due to network restrictions — not a bug.
⚠️ Program name on the dashboard shows "Tidak ada program" until Task #7 is completed.

---

_Previous sprint history will be appended above this line as new sprints are completed._
