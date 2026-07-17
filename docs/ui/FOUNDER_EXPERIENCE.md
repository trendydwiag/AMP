# Founder Experience & Onboarding
**Sprint 3.5 — Kabulhaden CMS**

## Overview

Sprint 3.5 transforms AMP Studio into a CMS that non-technical radio owners can use without reading documentation. Every UX decision prioritizes Kabulhaden Online (Partner #001) while remaining reusable for future AMP partners.

---

## Features Implemented

### 1. Welcome Dashboard (`templates/amp_studio/dashboard.html`)

The dashboard now shows:
- **Partner logo** — site logo from `SiteSettings` displayed in the welcome banner. Falls back to a branded coffee-colored radio icon.
- **Time-aware greeting** — pagi/siang/sore/malam depending on the server's current hour.
- **Setup Wizard shortcut** — CTA button in the header if the wizard hasn't been completed.
- **Dashboard Action Cards** — contextual suggestions for missing content (see section 5).

### 2. Streaming Center (`/studio/streaming/`)

A dedicated page that is the **single source of truth** for streaming configuration.

**URL:** `{% url 'studio:streaming_center' %}`
**Template:** `templates/amp_studio/streaming_center.html`
**View:** `StreamingCenterView` in `apps/studio/views.py`

**Contents:**
| Element | Description |
|---------|-------------|
| Live Status Banner | Real-time on-air / offline status with auto-refresh every 30s |
| Stream URL | Primary and backup stream URLs with one-click copy |
| API Endpoint | RadioBOSS/AzuraCast API URL with copy button |
| Test Stream Button | Opens stream in new tab for quick audio check |
| Connection Status | Live/offline indicator |
| Listener Count | Real-time via `/radio/api/status/` |
| Bitrate & Codec | From latest `StreamHealth` record |
| Last Heartbeat | Timestamp of most recent health check |
| Provider List | All active providers with edit links |
| Health History | Last 20 health records in a table |
| Now Playing | Current track from API |

**Empty State:** When no station exists, shows a clear CTA to create one or use the Setup Wizard.

### 3. Quick Setup Wizard (`/studio/setup/`)

A guided 5-step onboarding flow for first-time founders.

**URL:** `{% url 'studio:setup_wizard' %}`
**Template:** `templates/amp_studio/setup_wizard.html`
**View:** `SetupWizardView` in `apps/studio/views.py`

**Steps:**

| Step | Title | Action |
|------|-------|--------|
| 1 | Radio Identity | Links to `settings:site` |
| 2 | Upload Logo | Links to `settings:site` logo section |
| 3 | Streaming URL | Links to `radio:station_create` + `radio:provider_create` |
| 4 | Social Media | Links to `settings:social_media` |
| 5 | Finish | POST to mark completion in session |

**Features:**
- Visual progress indicator with colored step dots and connecting line
- Completion status per step (green checkmark if done)
- `Skip` link to exit wizard at any time
- Step navigation via `?step=N` URL params
- Completion tracked via Django session (`setup_wizard_done` key, no schema change)

### 4. Improved Empty States

All empty states in the dashboard follow the pattern:
- **Icon** — relevant SVG illustration
- **Explanation** — clear message in Indonesian
- **Primary CTA** — direct link to the correct action

Applied to: Today's Schedule, Recent Articles, Providers list, Streaming Center.

### 5. Dashboard Action Cards

Shown when content is missing. Dismissed automatically once the item is created.

| Card | Trigger Condition | Links To |
|------|-------------------|----------|
| Tambah Streaming | No active `RadioStation` | `studio:streaming_center` |
| Buat Jadwal | No schedule for today | `broadcast:schedule_list` |
| Tambah Sponsor | `active_sponsors == 0` | `sponsor:partner_list` |
| Upload Podcast | No `PodcastEpisode` exists | `podcast:cms_episode_create` |
| Tulis Berita | No published `Article` | `news:cms_article_create` |

The action cards banner is hidden when all items are complete.

### 6. Floating Help Button

A persistent floating action button (FAB) in the bottom-right corner on all AMP Studio pages.

**Template:** `templates/amp_studio/components/help_button.html`
**Included in:** `templates/amp_studio/base.html`

**Menu items:**
| Item | Action |
|------|--------|
| Dokumentasi | Opens `docs.kabulhaden.online` in new tab |
| FAQ | Opens FAQ page in new tab |
| Tutorial Video | Opens video tutorial page |
| Mulai Tur Panduan | Triggers the guided tour |
| Hubungi Administrator | Opens email to `admin@kabulhaden.online` |

### 7. First Login Guided Tour

An interactive onboarding tour that highlights key sections of AMP Studio.

**Template:** `templates/amp_studio/components/guided_tour.html`
**Included in:** `templates/amp_studio/base.html`
**Completion tracking:** `localStorage` key `amp_tour_completed_v1` (no DB schema change)

**Tour stops:**

| Stop | Element | Description |
|------|---------|-------------|
| 1 | Dashboard | Overview of the control center |
| 2 | Streaming Center | Live status and stream URLs |
| 3 | Program & Siaran | Schedule and program management |
| 4 | Konten & Berita | Article and content creation |
| 5 | Pengaturan | Settings and configuration |
| 6 | Help Button | How to access help anytime |

**Behavior:**
- Automatically starts on first visit (1.2s delay after page load)
- Highlights target element with coffee-colored ring
- Card positions near the highlighted element, adjusting to viewport boundaries
- **Skip** link exits the tour and marks it complete
- Can be restarted from the Help Button menu via `startGuidedTour()`

---

## Design Principles

| Principle | Implementation |
|-----------|---------------|
| Coffee Theme only | All components use `--amp-coffee-*` CSS variables |
| No duplicate CSS | All styles reuse existing `amp-*` classes |
| Mobile friendly | Responsive grid, touch-friendly tap targets |
| Accessible | Semantic HTML, `aria-label` on interactive elements |
| No breaking changes | All features additive; no existing views modified |
| No schema changes | Wizard completion tracked in session, tour in localStorage |

---

## Files Modified

| File | Change |
|------|--------|
| `apps/studio/views.py` | Added `StreamingCenterView`, `SetupWizardView`, enhanced dashboard context |
| `apps/studio/urls.py` | Added `/streaming/` and `/setup/` routes |
| `templates/amp_studio/dashboard.html` | Partner logo, time greeting, Setup Wizard CTA, Action Cards |
| `templates/amp_studio/base.html` | Included help button and guided tour |
| `templates/amp_studio/components/sidebar.html` | Added Streaming Center and Setup Wizard nav items |

## Files Created

| File | Purpose |
|------|---------|
| `templates/amp_studio/streaming_center.html` | Streaming Center page |
| `templates/amp_studio/setup_wizard.html` | 5-step setup wizard |
| `templates/amp_studio/components/help_button.html` | Floating help FAB |
| `templates/amp_studio/components/guided_tour.html` | Interactive onboarding tour |
| `docs/ui/FOUNDER_EXPERIENCE.md` | This document |
| `docs/adr/0030-founder-experience.md` | Architecture Decision Record |
