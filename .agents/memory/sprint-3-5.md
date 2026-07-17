---
name: Sprint 3.5 Founder Experience
description: 7 UX features added to AMP Studio for non-technical radio founders. Constraints and gotchas.
---

## Features Added
1. Welcome Dashboard — partner logo, time-aware greeting, action cards, wizard CTA
2. Streaming Center — `/studio/streaming/` via `studio:streaming_center`
3. Setup Wizard — `/studio/setup/` via `studio:setup_wizard`, 5 steps
4. Improved Empty States — icon + explanation + CTA pattern
5. Dashboard Action Cards — `has_radio_station`, `has_schedule`, `has_sponsor`, `has_podcast`, `has_news` context flags
6. Floating Help Button — `amp_studio/components/help_button.html`, included in base.html
7. Guided Tour — `amp_studio/components/guided_tour.html`, localStorage key `amp_tour_completed_v1`
8. P3 Radio Health Widget — `amp_studio/components/health_widget.html`, `_get_system_health()` method on dashboard view

## Key Decisions
- Wizard completion: Django session `setup_wizard_done` key (no migration)
- Tour completion: localStorage `amp_tour_completed_v1` (no migration, per-device)
- Setup Wizard delegates to existing settings pages (no duplicate forms)
- `{% now "H" as h %}` returns zero-padded string ("07", "14") — string comparison in `{% if %}` works correctly for 24h time
- Health widget: 6 services (Streaming/Website/DB/Storage/SSL/Backup), all try/except safe, `_get_system_health()` on view
- `sponsor` app has NO CMS URL namespace; action card falls back to `/admin/sponsor/`
- amp-status-dot modifier classes: `.live` (green pulse), `.online` (green), `.offline` (gray), `.warning` (yellow)

## Gotchas
- Alpine.js blocked by browser CSP (Task #3 still open) — guided tour degrades gracefully
- `StreamingCenterView` wraps all radio service calls in try/except — no crash if no station
- `SetupWizardView.get()` builds `steps` context (NOT `get_context_data()`) — must call via `get()`
- Dashboard context: `SITE_NAME`, `SITE_LOGO`, `system_health` added in `AMPStudioDashboardView.get_context_data()`
- `User.get_full_name` is a **property** (string), not a method — do NOT call it with `()`

**Why:**
Sprint constraint was "DO NOT change DB schema / backend architecture" — session + localStorage solve persistence needs without migrations.
