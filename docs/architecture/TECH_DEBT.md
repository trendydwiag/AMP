# AMP Studio — Technical Debt Register

All known unresolved issues and architectural shortcuts are documented here.
Do not hide problems — document them so they can be planned and resolved.

---

## TD-001 — `program` Field Always Returns Null in Live API
**Sprint introduced:** 3.4D
**Priority:** High (visible in demo)
**Status:** ✅ RESOLVED — Sprint 4.4

### Resolution
`CurrentProgramResolver` service created in `apps/broadcast/services.py` resolves the currently airing program from the broadcast schedule. `LiveRadioAPIView.get()` now queries this resolver and populates `program`, `host`, `start_time`, `end_time`, `remaining_minutes`, `next_program`, and `next_start_time` in the API response. Homepage hero widget and Studio Dashboard both display the resolved program info. The resolver queries `Schedule` by current day_of_week and time, then resolves lead host via `HostMemberRepository`.

---

## TD-002 — No Fallback Stream URL
**Sprint introduced:** 3.4D
**Priority:** High (playback failure)
**Status:** ✅ RESOLVED — Sprint 4.3

### Resolution
`LiveRadioAPIView` sekarang memiliki fallback eksplisit:
```python
listen_url_fallback = db_provider.stream_url  # set sebelum try block
stream_url = raw_response.get('listen_url') or listen_url_fallback
```
`listen_url_fallback` selalu tersedia di except block sehingga bahkan jika upstream API gagal total, URL stream masih dikembalikan ke browser.

---

## TD-003 — No Automated Tests for LiveRadioAPIView
**Sprint introduced:** 3.4D
**Priority:** Medium (demo risk)
**Status:** Open — tracked as Task #9

### Description
The `LiveRadioAPIView` endpoint has no unit or integration tests. There is no automated check that:
- The offline fallback returns HTTP 200 with `status: "offline"`
- The normalized schema contains all required fields
- The cache layer is populated and served correctly
- Provider errors don't leak stack traces

### Impact
A misconfiguration or regression before July 21 would not be caught until someone manually checks the endpoint. Silent failure is possible.

### Suggested Solution
Create `apps/radio/tests/test_live_api.py` with Django `TestCase` + `unittest.mock.patch` on the adapter's `_make_request` method. Test both the happy path and the error path.

### Estimated Effort
2–3 hours.

---

## TD-004 — Broadcastindo Adapter Makes Two HTTP Calls Per Request Pair
**Sprint introduced:** 3.4D
**Priority:** Low (performance)
**Status:** Open

### Description
`BroadcastindoAdapter.get_now_playing()` and `get_listener_count()` both call `_fetch_nowplaying_data()` independently. If `LiveRadioAPIView` calls both in sequence (which it does), the adapter makes two HTTP requests to the same upstream URL. The Django cache in `LiveRadioAPIView` prevents this from affecting most requests, but on cache-miss the upstream is hit twice.

### Impact
On cache-miss: 2× upstream requests, ~2× latency. In production with a 20 s TTL this happens at most 3 times per minute — low severity.

### Suggested Solution
Cache `_fetch_nowplaying_data()` result within the adapter instance (request-scoped), or restructure `LiveRadioAPIView` to parse a single raw response directly instead of calling `get_now_playing()` + `get_listener_count()` separately.

### Estimated Effort
1 hour.

---

## TD-005 — Hardcoded Polling Intervals in JS
**Sprint introduced:** 3.4D
**Priority:** Low (maintainability)
**Status:** Open

### Description
The polling intervals (25 000 ms in `radio-player.js` and `amp-studio.js`, 30 000 ms in `streaming_center.html`) are hardcoded in JavaScript. If the `STREAM_CACHE_TTL` setting is changed, the intervals won't update automatically — a developer must remember to change both the Django setting and the JS constants.

### Impact
If cache TTL is reduced (e.g. to 10 s for a high-frequency demo), but JS intervals stay at 25 s, widgets will appear slow to update even though fresh data is available.

### Suggested Solution
Pass `STREAM_CACHE_TTL` as a template context variable and render it into a `<meta>` tag or a JS constant block in `base.html`:
```html
<meta name="stream-poll-interval" content="{{ STREAM_CACHE_TTL|add:5000 }}">
```
JS reads `parseInt(document.querySelector('meta[name="stream-poll-interval"]').content)`.

### Estimated Effort
1–2 hours.

---

## TD-008 — ngrok URL Harus Diupdate Manual Setiap Restart
**Sprint introduced:** 4.3
**Priority:** Medium (operasional)
**Status:** Open — by design untuk development

### Description
`RadioProvider.stream_url` dan `RadioProvider.api_url` di DB menyimpan URL ngrok yang berubah setiap kali tunnel di-restart. Tidak ada mekanisme otomatis untuk mendeteksi URL baru.

### Impact
Setelah ngrok restart, `LiveRadioAPIView` mengembalikan URL lama → browser menerima 404 dari Icecast → `NotSupportedError` di audio element.

### Suggested Solution
Simpan URL base ngrok sebagai environment variable (`NGROK_BASE_URL`) dan buat `RadioProvider` model membaca dari env saat `stream_url` kosong. Atau gunakan ngrok paid plan dengan static domain.

### Estimated Effort
1–2 jam.

---

## TD-006 — Platform App Has Pending Unapplied Migrations
**Sprint introduced:** Pre-existing (discovered 3.4D)
**Priority:** Medium (latent risk)
**Status:** Open

### Description
`python manage.py showmigrations` shows unapplied migrations in `apps/platform`. Django prints a warning on startup but the app continues to function. If a migration creates a required table or column, features that depend on it will fail silently.

### Impact
`apps/platform` features may behave unexpectedly if they depend on the unapplied schema changes.

### Suggested Solution
Run `python manage.py migrate` in a maintenance window and verify no data is lost. Check what the pending migrations do before applying.

### Estimated Effort
30 minutes (plus review of migration content).

---

## TD-007 — No Superuser Account in Development Environment
**Sprint introduced:** Pre-existing (discovered 3.4D)
**Priority:** High (blocks all AMP Studio verification)
**Status:** Open — tracked as Task #2

### Description
There is no superuser account in the development database. All AMP Studio pages (`/studio/*`) require login. This blocks manual QA of every studio feature.

### Impact
Cannot visually verify dashboard, streaming center, or any authenticated page without creating an account.

### Suggested Solution
Run `python manage.py createsuperuser` or use `python manage.py demo_seed` which creates demo users. Task #2 covers this.

### Estimated Effort
5 minutes.
