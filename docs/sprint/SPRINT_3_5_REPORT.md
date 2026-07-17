# Sprint 3.5 — Founder Experience & Onboarding
**Report Date:** 2025-07-17
**Sprint Type:** Pure UX Sprint (no backend/schema changes)
**Status:** ✅ Completed

---

## Summary

Sprint 3.5 delivers 7 founder-focused UX improvements to AMP Studio, making the CMS accessible to non-technical radio owners without any database migrations or backend architectural changes.

---

## Features Delivered

### ✅ Feature 1: Welcome Dashboard
- **Partner logo** displayed in the welcome banner using `SiteSettings.site_logo`
- **Time-aware greeting** (pagi / siang / sore / malam) using Django's `{% now %}` template tag
- **Setup Wizard CTA** button shown in header until wizard is marked complete
- **Fallback logo** — branded coffee-gradient radio icon when no logo is configured

### ✅ Feature 2: Streaming Center (`/studio/streaming/`)
New dedicated page at `studio:streaming_center`:
- Live status banner (ON AIR / OFFLINE) with auto-refresh every 30 seconds
- Primary and backup stream URLs with one-click copy to clipboard
- RadioBOSS/AzuraCast API endpoint with copy button
- Test Stream button (opens stream URL in new tab)
- Connection status, listener count, bitrate, codec from `StreamHealth`
- Last heartbeat timestamp
- All active providers listed with edit links
- Stream health history table (last 20 records)
- Now Playing display with audio visualizer bars
- Empty state when no station exists (links to wizard)

### ✅ Feature 3: Quick Setup Wizard (`/studio/setup/`)
5-step guided onboarding at `studio:setup_wizard`:
1. **Radio Identity** — links to `settings:site`
2. **Upload Logo** — links to `settings:site` logo section
3. **Streaming URL** — links to `radio:station_create` + `radio:provider_create`
4. **Social Media** — links to `settings:social_media`
5. **Finish** — POSTs to mark completion; redirects to dashboard

Features:
- Visual progress indicator with step dots and connecting line
- Per-step completion checkmarks (queries existing models, no new schema)
- Alpine.js step navigation with URL param `?step=N`
- Skip link on every step
- Completion tracked in Django session (no migration needed)

### ✅ Feature 4: Improved Empty States
Applied richer empty states throughout:
- **Today's Schedule** — icon + explanation + Atur Jadwal CTA
- **Recent Articles** — icon + Buat Artikel CTA
- **Streaming Center no-station** — illustration + dual CTAs (create station / use wizard)
- **Providers empty** — full explanation of supported providers + CTA

### ✅ Feature 5: Dashboard Action Cards
Contextual suggestion banner shown when setup is incomplete. Each card:
- Appears only when the relevant content is missing
- Has a colored icon, title, and description
- Links directly to the correct creation/setup page
- Entire banner hides when all content is present

| Card | Trigger |
|------|---------|
| Tambah Streaming | No active `RadioStation` |
| Buat Jadwal | No schedule for today |
| Tambah Sponsor | `active_sponsors == 0` |
| Upload Podcast | No `PodcastEpisode` exists |
| Tulis Berita | No published `Article` |

### ✅ Feature 6: Floating Help Button
Persistent FAB in bottom-right corner on all AMP Studio pages:
- Animated open/close with rotation
- Dropdown menu: Dokumentasi, FAQ, Tutorial Video, Mulai Tur Panduan, Hubungi Administrator
- Z-index `1090` — above all content, below modals

### ✅ Feature 7: First Login Guided Tour
Interactive onboarding using Alpine.js + vanilla JS:
- Automatically starts on first visit (1.2s delay)
- 6 tour stops: Dashboard, Streaming, Siaran, Konten, Pengaturan, Help Button
- Coffee-colored spotlight ring highlights each target element
- Card positions near target, adjusts to viewport boundaries
- Skip button exits and marks complete
- Restartable from Help Button menu via `startGuidedTour()`
- Completion stored in `localStorage` key `amp_tour_completed_v1`

---

## Files Created / Modified

| File | Type | Change |
|------|------|--------|
| `apps/studio/views.py` | Modified | Added `StreamingCenterView`, `SetupWizardView`, enhanced dashboard context |
| `apps/studio/urls.py` | Modified | Added `/streaming/` and `/setup/` routes |
| `templates/amp_studio/dashboard.html` | Modified | Partner logo, time greeting, action cards, wizard CTA |
| `templates/amp_studio/base.html` | Modified | Help button + guided tour includes; toast container repositioned |
| `templates/amp_studio/components/sidebar.html` | Modified | Streaming + Setup Wizard nav items; tour target IDs |
| `templates/amp_studio/streaming_center.html` | **Created** | Full Streaming Center page |
| `templates/amp_studio/setup_wizard.html` | **Created** | 5-step setup wizard |
| `templates/amp_studio/components/help_button.html` | **Created** | Floating help FAB |
| `templates/amp_studio/components/guided_tour.html` | **Created** | Interactive onboarding tour |
| `docs/ui/FOUNDER_EXPERIENCE.md` | **Created** | Feature documentation |
| `docs/adr/0030-founder-experience.md` | **Created** | Architecture Decision Record |
| `docs/sprint/SPRINT_3_5_REPORT.md` | **Created** | This document |

---

## Constraints Respected

| Constraint | Status |
|-----------|--------|
| Coffee theme only | ✅ All components use `--amp-coffee-*` variables |
| No duplicate CSS | ✅ All styles reuse existing `amp-*` classes |
| No backend architecture changes | ✅ Only new views/URLs added; services untouched |
| No schema changes | ✅ Session (wizard) + localStorage (tour) used |
| Responsive + mobile friendly | ✅ Responsive grids, mobile-safe tap targets |
| Maintain accessibility | ✅ `aria-label` on all interactive elements |
| No breaking changes | ✅ All existing views and templates intact |
| Reusable components | ✅ Help button + guided tour are `{% include %}`-able |

---

## Technical Notes

1. **Alpine.js CDN** — The `amp_studio/base.html` CDN tag uses `@3.x.x` (no SRI hash). The browser CSP is blocking it (Task #3). The guided tour degrades gracefully when Alpine.js is unavailable — the backdrop and card don't show but no JS errors are thrown (all DOM manipulation is in plain JS, not Alpine).

2. **Django `{% now %}` tag** — Used for time-aware greeting. The tag outputs a string (e.g. `"14"`), compared against string literals in `{% if %}` blocks using Django's template string comparison.

3. **Sponsor URL** — The `sponsor` app has no CMS URL namespace. The "Tambah Sponsor" action card links to `/admin/sponsor/` as a temporary fallback until a CMS sponsor view is created.

4. **Empty state for Streaming Center** — When `RadioStation.objects.filter(is_active=True).exists()` returns `False`, the streaming center shows a full-page empty state instead of the normal content. This avoids broken template rendering when no station exists.

---

## Open Issues (Not In Scope)

- **Task #2**: No superuser exists yet for the admin dashboard (a test admin was created during this sprint for verification purposes).
- **Task #3**: AlpineJS blocked by browser CSP/SRI — affects interactive features including the guided tour.
- **Task #4**: No real radio stream connected yet — streaming center will show "Tidak ada yang diputar".
- **Sponsor CMS**: No dedicated CMS sponsor management page exists; action card uses Django admin fallback.
