# AMP Studio — UI Changelog

Visual and interaction changes across all interfaces, documented sprint by sprint.

---

## Sprint 3.4D — Live Streaming Integration
**Date:** July 17, 2026

### 1. Dashboard — "Siaran Langsung" Card (Live Broadcast Widget)

**Component:** `templates/amp_studio/dashboard.html` — Live Broadcast card (line ~230)
**Alpine component:** `streamStatus()` in `static/js/amp-studio/amp-studio.js`

| | Before | After |
|---|---|---|
| **Data source** | `/radio/api/status/` — DB-backed, required a configured RadioStation | `/api/v1/radio/live/` — settings-driven, works without DB station |
| **Live detection** | `data.stream_status === 'PLAYING' \|\| data.is_active` | `data.is_live` (boolean) |
| **Listener count** | `data.current_listeners` | `data.listeners` |
| **Program name** | `data.current_program` | `data.program` (currently `null`; Task #7) |
| **Polling interval** | 15 000 ms | 25 000 ms |

**Visual result:** No visual change to the card layout. The data it shows is now real (when network allows) rather than database-fallback values.

---

### 2. Dashboard — "Pendengar Online" Metric Card

**Component:** `templates/amp_studio/dashboard.html` — metric card (line ~48)
**Alpine component:** `streamStatus()` (shared with Live Broadcast widget)

| | Before | After |
|---|---|---|
| **Listener count source** | DB-backed via `/radio/api/status/` | Real upstream listener count via `/api/v1/radio/live/` |
| **Offline state** | Shows "0" with no indication of source failure | Shows "0" with `isOffline` flag available for future styling |

**Affected pages:** `studio/` (Dashboard)

---

### 3. Streaming Center — Live Status Banner

**Component:** `templates/amp_studio/streaming_center.html` — live status banner (line ~52)
**Alpine component:** `streamingCenter()` inline script (line ~364)

| | Before | After |
|---|---|---|
| **Data source** | `/radio/api/status/` | `/api/v1/radio/live/` |
| **Live detection** | `data.is_live` | `data.is_live` (same field name, now from normalized schema) |
| **Listener count** | `data.listener_count` | `data.listeners` |
| **Now-playing string** | `data.now_playing` (pre-joined string from DB) | Composed client-side: `` `${data.title} — ${data.artist}` `` |
| **Current program** | `data.current_program` | `data.program` |
| **Offline state** | Silently showed empty strings | Sets `isOffline: true`; future-ready for error UI treatment |

**Visual result:** "Sedang Diputar" panel now shows real track title and artist from the live stream. Previously this panel was always empty (no DB cache was populated).

**Affected pages:** `studio/streaming-center/`

---

### 4. Public Website — Hero Player & Sticky Player

**Component:** `templates/website/components/home/hero_radio.html`, `sticky_player.html`
**Data binding:** `$store.radio` (Alpine global store)
**JS driver:** `static/js/radio-player.js`

| | Before | After |
|---|---|---|
| **Data source** | `/radio/api/status/` | `/api/v1/radio/live/` |
| **Track title binding** | `data.title \|\| data.track_title \|\| 'Kabulhaden Radio'` | `data.title \|\| 'Kabulhaden Radio'` |
| **Artist binding** | `data.artist \|\| data.track_artist \|\| 'Siaran Langsung'` | `data.artist \|\| 'Siaran Langsung'` |
| **Artwork binding** | `data.artwork \|\| data.album_art \|\| ''` | `data.cover \|\| ''` |
| **Listener count** | Not displayed | `$store.radio.listeners` available to all templates |
| **Polling interval** | 10 000 ms | 25 000 ms |

**Visual result:** Track title and artist on the hero and sticky player now show real now-playing data from the live stream rather than the default fallback strings. Artwork will appear when the provider returns an art URL.

**Affected pages:** `/` (Homepage hero), all pages with sticky player

---

### 5. AMP Studio Player Bar (Header)

**Component:** `templates/amp_studio/components/header.html` — stream status widget
**Alpine component:** `ampPlayer()` → `fetchNowPlaying()` in `static/js/amp-studio/amp-studio.js`

| | Before | After |
|---|---|---|
| **Now-playing fetch URL** | `/radio/api/status/` | `/api/v1/radio/live/` |
| **Song title field** | `data.song_title` | `data.title` |
| **Program field** | `data.current_program` | `data.program` |
| **Listener count field** | `data.current_listeners` | `data.listeners` |
| **Stream URL fallback** | Only from `fetchConfig()` → `/radio/api/player-config/` | Also from `data.stream_url` in live response |

**Visual result:** "Now Playing" display in the AMP Studio header now sources from the live stream. If `stream_url` is returned by the live API, the player has a stream URL even without a DB-configured provider.

**Affected pages:** All AMP Studio pages (header is global)

---

### Screenshots
_Screenshots require a superuser account (Task #2) and network access to the live stream. To be captured before the July 21 demo presentation._
