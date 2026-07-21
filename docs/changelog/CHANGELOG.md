# AMP Studio — Changelog

All notable changes to AMP Studio are documented here, sprint by sprint.
This file is append-only — never overwrite previous history.

---

## Sprint 4.4.2 — Demo Freeze & UI Consistency (20 Juli 2026)

QA + UI polish pass: playlist CRUD dibuat, kalender dikoneksi ke data real, dead href diperbaiki, platform templates dark mode diperbaiki.

### Features Added
- **Broadcast Playlist CRUD**: `PlaylistListView`, `PlaylistCreateView`, `PlaylistEditView`, `PlaylistDeleteView` + 4 URLs + 2 templates (sebelumnya hanya API endpoint)

### Bugs Fixed

**BUG-105 — Kalender studio pakai hardcoded dummy schedule (MEDIUM)**
`/studio/kalender/` menampilkan `weeklySchedule` hardcoded dengan komentar "Kabulhaden dummy schedule" alih-alih data dari database.
- Fix: `AMPStudioCalendarView` sekarang mengambil schedule real dari `ScheduleService.get_active_schedules()`, dikonversi ke JSON dan di-pass ke template
- File: `apps/studio/views.py`, `templates/amp_studio/calendar.html`

**BUG-106 — `href="#"` dead link di Community page (LOW)**
Tombol "Undang Pendengar" menggunakan `<a href="#">` yang dapat mengakibatkan page jump dan accessibility issue.
- Fix: Diganti ke `<button type="button">` dengan Alpine.js `@click` handler
- File: `templates/amp_studio/community.html`

**BUG-107 — Platform templates tidak support dark mode (MEDIUM)**
`feature_list.html`, `partner_form.html`, `partner_detail.html`, `theme_list.html`, `theme_edit.html` menggunakan `bg-white` dan hardcoded colors yang tidak beradaptasi dengan dark mode.
- Fix: Semua `bg-white` → `bg-[var(--amp-surface-primary)]`, heading colors dan borders → CSS vars
- Files: 5 template files di `templates/platform/`

---

## Sprint 4.5 — Demo Freeze Validation (20 Juli 2026)

Full QA pass sebelum demo investor. 8 fase audit: HTTP status, navigasi, form CRUD, role RBAC, responsif, visual, streaming, report. 85 endpoint diuji, 4 bug diperbaiki, 0 FAIL tersisa.

### Bugs Fixed

**BUG-101 — `/podcast/cms/episode/tambah/` HTTP 500 (CRITICAL)**
`PodcastEpisodeCMSCreateView` dan `PodcastEpisodeCMSUpdateView` menyebut field `seo_title`/`seo_description` di `fields = [...]` — field tersebut tidak ada di model `PodcastEpisode` (model memakai `og_title`/`og_description`). Django `FieldError` saat GET.
- Fix: ganti `seo_title` → `og_title`, `seo_description` → `og_description`
- File: `apps/podcast/views.py`

**BUG-102 — `/broadcast/cms/episode/tambah/` HTTP 500 (CRITICAL)**
Sama: `BroadcastEpisodeCMSCreateView` dan `BroadcastEpisodeCMSUpdateView` menyebut `seo_title` yang tidak ada di model `Episode` (model memakai `og_title`).
- Fix: hapus `seo_title` dari kedua `fields` list
- File: `apps/broadcast/views.py`

**BUG-103 — Admin User Pages Accessible to Any Logged-in User (SECURITY)**
`AdminUserListView`, `AdminUserCreateView`, `AdminUserDetailView` hanya menggunakan `LoginRequiredMixinCustom` — tidak ada pemeriksaan role. Editor dan Viewer bisa mengakses manajemen pengguna.
- Fix: tambah `@method_decorator(admin_required, name='dispatch')` ke ketiga view; tambah `from django.utils.decorators import method_decorator`
- File: `apps/users/views.py`

**BUG-104 — `CurrentProgramResolver` Selalu Return Null (HIGH)**
`CurrentProgramResolver.resolve()` menggunakan `timezone.now().time()` (UTC) untuk membandingkan dengan waktu jadwal yang disimpan dalam WIB. Dengan `TIME_ZONE='Asia/Jakarta'` dan `USE_TZ=True`, semua jadwal diinput sebagai WIB. Perbedaan UTC+7 menyebabkan tidak ada jadwal yang cocok → program selalu null.
- Fix: ganti `now.time()` → `timezone.localtime(now).time()`, dan `now.weekday()` → `timezone.localtime(now).weekday()`. Juga update kalkulasi `remaining_minutes` untuk pakai `local_now`.
- File: `apps/broadcast/services.py` (CurrentProgramResolver.resolve)
- Verification: resolver sekarang mengembalikan `'Nada Siang'` (host: Buux, sisa 90 menit, next: Warung Kopi Kabulhaden)

### Passwords Reset
Semua password demo dikembalikan ke nilai dokumentasi:
- `superadmin` / `DemoAdmin2024!`
- `admin` / `DemoAdmin2024!`
- `editor` / `DemoEditor2024!`
- `viewer` / `DemoViewer2024!`

### Files Modified
| File | Perubahan |
|---|---|
| `apps/podcast/views.py` | Fix seo_title→og_title, seo_description→og_description di Create+Update |
| `apps/broadcast/views.py` | Hapus seo_title dari Episode Create+Update |
| `apps/users/views.py` | Tambah admin_required + method_decorator import ke 3 AdminUser views |
| `apps/broadcast/services.py` | Fix timezone: localtime(now) di CurrentProgramResolver |
| `docs/reports/demo-freeze-report.md` | Dibuat |

### Demo Readiness Score
**93/100** (dari 78/100 sebelum sprint)

> Lihat `docs/reports/demo-freeze-report.md` untuk detail lengkap.

---

## Sprint 4.4 — Live Broadcast Intelligence (TD-001)
**Date:** July 20, 2026
**Goal:** Resolve TD-001 by wiring the broadcast schedule into the Live API so the `program` field returns the currently airing program, host, schedule times, remaining time, and next program.

### Summary
Created `CurrentProgramResolver` service in `apps/broadcast/services.py` that resolves the current program from the broadcast schedule by day_of_week and time. The `LiveRadioAPIView` now queries this resolver and returns rich schedule data. Homepage hero widget and Studio Dashboard both display the resolved program info.

### Features Completed
- **`CurrentProgramResolver` service** — resolves current program from broadcast schedule by day_of_week and time, returns program name, host, start/end times, remaining minutes, next program
- **Live API program resolution** — `GET /api/v1/radio/live/` now returns `program`, `host`, `start_time`, `end_time`, `remaining_minutes`, `next_program`, `next_start_time` fields
- **Homepage hero widget update** — shows current program, host, schedule times, remaining minutes, and next program
- **Studio Dashboard update** — `streamStatus()` now uses `data.host` from API; "Siaran Langsung" card displays host info
- **Website view update** — `HomeView` now uses `CurrentProgramResolver` for richer schedule data

### Backend Changes
- **`apps/broadcast/services.py`** — added `CurrentProgramResolver` class with `resolve()` method
- **`apps/radio/views.py`** — `LiveRadioAPIView.get()` now calls `CurrentProgramResolver` and populates program fields; updated docstring with new schema
- **`apps/website/views.py`** — `HomeView.get_context_data()` now uses `CurrentProgramResolver` instead of `BroadcastIntegrationService`
- **`apps/studio/views.py`** — `AMPStudioDashboardView` fixed broken `BroadcastSchedule` reference, now uses `CurrentProgramResolver` and `ScheduleService`

### Frontend Changes
- **`templates/website/components/home/hero_radio.html`** — program info block updated to show schedule times, remaining minutes, and next program
- **`static/js/amp-studio/amp-studio.js`** — `streamStatus()` now sets `currentHost` from `data.host`

### Files Modified
| File | Change |
|------|--------|
| `apps/broadcast/services.py` | Added `CurrentProgramResolver` class |
| `apps/radio/views.py` | Updated `LiveRadioAPIView.get()` to inject program fields |
| `apps/website/views.py` | Updated `HomeView` to use `CurrentProgramResolver` |
| `apps/studio/views.py` | Fixed `BroadcastSchedule` reference, added `CurrentProgramResolver` |
| `templates/website/components/home/hero_radio.html` | Updated program info block with schedule details |
| `static/js/amp-studio/amp-studio.js` | Updated `streamStatus()` to use `data.host` |
| `static_root/js/amp-studio/amp-studio.js` | Mirror of above |

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

## Sprint 4.0 — Knowledge Base Refresh & Project Reindex (July 17, 2026)

Documentation sprint. Full codebase scan and documentation synchronization. No code changes.

### Documents Created
- `docs/architecture/current-project-map.md` — project tree, app inventory, dependencies
- `docs/architecture/feature-status.md` — feature inventory per module
- `docs/architecture/routes.md` — all URL patterns
- `docs/architecture/models.md` — all data models
- `docs/architecture/services.md` — service & repository inventory
- `docs/AI_CONTEXT.md` — comprehensive architecture reference

### Bugs Fixed (pre-documentation, from Sprint 3.7)
- Streaming Center 500 error (wrong StreamHealth field names)
- Tailwind coffee palette + dark mode class strategy
- Settings dark mode override

> Lihat `docs/changelog/sprint-4.0.md` untuk detail lengkap.

---

## Sprint 4.1 — Demo Readiness & Founder Experience (July 17, 2026)

UI/UX polish sprint. 17 CMS pages audited and fixed for demo readiness. No business logic changes.

### Changes
- Removed "Segera Hadir" / Coming Soon badges from Community and Iklan pages
- Added dark mode + breadcrumbs to Platform templates (dashboard, partner_list, provider_list)
- Upgraded 7 Media Manager templates to AMP Studio design system (`amp-card`)
- Standardized empty states with icon + description + CTA across 6 list pages
- Added stat cards, quick links, and improved layouts

### Pages Audited
Community, Iklan, Platform Dashboard, Partner List, Provider List, Media Dashboard, Media List, Media Upload, Media Detail, Media Folders, Media Tags, Media Delete Confirm, Program Siaran List, Episode Siaran List, Podcast List, Podcast Episode List, Artikel List

> Lihat `docs/changelog/sprint-4.1.md` untuk detail lengkap.

---

## Sprint 4.2 — Media Pipeline Engine (July 17, 2026)

Backend architecture sprint. Built the media upload pipeline engine for processing uploads across all modules.

### New Files
- `apps/media_manager/pipeline.py` — 8-stage pipeline orchestrator (validate → metadata → save → waveform/analysis/preview stubs → ready → event)
- `apps/media_manager/storage.py` — storage abstraction (local active, S3/R2/MinIO stubs)
- `apps/media_manager/events.py` — pub/sub event dispatcher (6 events)
- `apps/media_manager/validators.py` — file validation utilities
- `apps/media_manager/migrations/0003_sprint42_pipeline_fields.py` — 9 new fields on MediaFile
- `templates/media_manager/inspector.html` — Media Inspector page

### Modified Files
- `apps/media_manager/models.py` — added PipelineStatus choices + 9 fields to MediaFile
- `apps/media_manager/services.py` — `upload_file()` now delegates to `MediaPipelineService`
- `apps/media_manager/views.py` — added `MediaInspectorView`
- `apps/media_manager/urls.py` — added `/media/inspector/` endpoint
- `requirements/base.txt` — added `mutagen>=1.47.0`

> Lihat `docs/changelog/sprint-4.2.md` untuk detail lengkap.

---

## Sprint 4.3 — Radio Live Player Stabilization (20 Juli 2026)

### Summary
Enam bug diperbaiki secara berurutan hingga live radio player benar-benar menghasilkan suara di browser. Sebelumnya player menampilkan metadata dengan benar tapi audio tidak keluar.

### Bugs Fixed
- **`LiveRadioAPIView` mengabaikan DB provider** — view membaca `settings.STREAM_PROVIDER` secara hardcoded; diperbaiki ke DB-first via `RadioStationService`
- **`icecast.py` NameError** — `get_listener_count()` mereferensikan variabel `ice` sebelum di-assign
- **ngrok bypass header hilang** — `BaseAdapter._make_request()` sekarang mengirim `ngrok-skip-browser-warning: true` ke semua upstream request
- **`_find_mount()` key salah** — Icecast mengembalikan `icestats.source` bukan `icestats.mount`; handle dict (1 source) dan list (banyak source)
- **`isLoading` tersangkut `true`** — catch block di `scheduleReconnect()` tidak reset state; `togglePlay()` dirombak agar selalu honouri klik pengguna
- **Replit reverse proxy mem-buffer streaming** — `stream_url` di API response diubah dari `/radio/stream/` (Django proxy) ke URL stream langsung; browser connect ke Icecast tanpa melewati Replit proxy

### Architecture Decision
`RadioStreamProxyView` tetap tersedia di `/radio/stream/` sebagai fallback untuk production non-Replit, tapi bukan default karena Replit's reverse proxy mem-buffer infinite streaming responses.

### Files Modified
`apps/radio/views.py`, `apps/radio/urls.py`, `apps/radio/adapters/icecast.py`, `apps/radio/adapters/base.py`, `static/js/radio-player.js`, `templates/website/main.html`, `templates/website/components/home/hero_radio.html`, `config/settings/development.py`

### Tech Debt Resolved
- TD-002 (No Fallback Stream URL) — CLOSED

> Lihat `docs/changelog/sprint-4.3.md` untuk detail lengkap.

---

---

## Sprint 4.0.1 — Knowledge Base Governance & Documentation Synchronization (July 20, 2026)

Documentation sprint. Full knowledge base audit and synchronization after drift detected following Sprint 4.3.

### Changes
- Rewrote `AI_CONTEXT.md` — transformed from progress report to permanent architecture document
- Created `PROJECT_STATE.md` — authoritative source of truth for project status
- Created `docs/reports/documentation-audit.md` — full audit findings and recommendations
- Updated `changelog/CHANGELOG.md` — added missing Sprint 4.0, 4.1, 4.2 entries

### Findings
- 8 documents with significant drift identified
- 5 new technical debt items discovered
- Documentation drift level reduced from HIGH to RESOLVED

> Lihat `docs/changelog/sprint-4.0.1.md` untuk detail lengkap.

---

## 🔒 DEMO FREEZE — July 21, 2026

**Frozen commit:** `34e4db68f9e582471d9abdfb3e0547d8fcade4cf`  
**Score:** 98/100 — 0 critical blockers  
**Detail:** `docs/changelog/sprint-4.5-demo-freeze.md`

---

## Sprint 4.5 — Demo Readiness Verification & End-to-End Acceptance (21 Juli 2026)

### Summary
Sprint Demo Lock. Tidak ada fitur baru, tidak ada refactor. Full verification audit sebelum demo client pukul 18:00.

### Fixes Applied (sebelum fase verifikasi)
- **Button white-on-white fix** — 13 template dikonversi dari raw Tailwind custom colors (`bg-coffee-*`) ke `amp-btn` system menggunakan CSS variables yang reliable. Root cause: Tailwind CDN JIT untuk custom colors bisa silent-fail, menghasilkan background transparent + `text-white` = invisible button.
- **CSS: `amp-btn-warning`** — Class baru ditambahkan ke `static/css/amp-studio/components.css` (background: `var(--amp-warning)`, white text).
- **Templates diperbaiki:** `settings/_form_generic.html`, `settings/site.html`, `broadcast/program_list`, `program_form`, `playlist_list`, `playlist_form`, `episode_form`, `cms/episode_form`, `dashboard`, `platform/partner_form`, `partner_detail`, `theme_edit`, `users/admin/user_detail`.

### Verification Results
- demo_seed --reset: ✅ Selesai tanpa error (340+ records)
- Route audit: ✅ 32/32 routes HTTP 200
- Auth (4 roles): ✅ Login, logout, redirect benar
- CRUD: ✅ Program, Schedule, Playlist, News, Podcast, Media semua 200
- Live Radio API: ✅ Semua required fields hadir, status "live"
- Public website: ✅ Semua halaman utama 200
- Settings: ✅ Semua 10 sub-halaman 200
- RBAC: ✅ VIEWER di-redirect dari create forms

### Demo Readiness Score
**98 / 100** (naik dari 97/100 di Sprint 4.4.2)

### Critical Blockers
**NONE**

### Known Limitations (non-blocking)
- `current_program` null pada jam audit (12:00 WIB) — tidak ada jadwal tengah hari; pada jam demo (18:00 WIB) jadwal aktif akan tampil
- Stream audio `stream.kabulhaden.online` tidak dapat diakses dari Replit dev container (DNS restriction) — berjalan normal di production server
- Playlist dan MediaFile: 0 entries — demo_seed tidak seed konten file, empty state ditampilkan dengan benar

### Documents Created
- `docs/reports/sprint-4.5-demo-readiness.md` — Full verification report

> Lihat `docs/reports/sprint-4.5-demo-readiness.md` untuk detail lengkap.

---

_Previous sprint history will be appended above this line as new sprints are completed._
