# ADR 0030: Founder Experience & Onboarding (Sprint 3.5)

**Date:** 2025-07-17
**Status:** Accepted
**Decider:** Kabulhaden Engineering

---

## Context

AMP Studio was built for technical operators. Non-technical radio owners (founders) found the interface difficult to navigate without documentation. Sprint 3.5 was commissioned to solve this by adding guided onboarding, contextual help, and a dedicated streaming management page — without touching backend architecture.

---

## Decision 1: Tour completion tracked in localStorage (not DB)

**Chosen:** `localStorage.setItem('amp_tour_completed_v1', '1')`

**Alternatives considered:**
1. Add `onboarding_completed` field to `User` model (requires migration)
2. Use Django session (server-side, resets on logout)
3. Use `localStorage` (client-side, persists per browser)

**Why localStorage:**
- Sprint constraint: "DO NOT change database schema unless absolutely required"
- The guided tour is a per-device UX feature (different devices should each show the tour)
- No migration risk
- Instant read/write — no server round-trip

**Trade-off:** Tour resets if user clears browser storage or switches browser. Acceptable for a first-login UX element.

**Future:** If persistent cross-device tour tracking becomes required, add `onboarding_completed_at` to `UserProfile` with a migration.

---

## Decision 2: Setup Wizard completion tracked in Django session

**Chosen:** `request.session['setup_wizard_done'] = True`

**Why session (not localStorage):**
- The wizard result (completed/not) affects server-rendered UI (the Setup Wizard CTA button in the dashboard header)
- Sessions are user-scoped and server-authoritative
- No migration required (sessions table already exists)

**Trade-off:** Resets when session expires or user logs out from all devices. For a one-time setup flow this is acceptable.

---

## Decision 3: Streaming Center as a separate page, not a modal

**Chosen:** Dedicated page at `/studio/streaming/`

**Alternatives considered:**
1. Embed streaming data in the existing Radio Dashboard
2. Add a modal/drawer to the main dashboard
3. Separate dedicated page (chosen)

**Why a separate page:**
- The sprint explicitly calls it the "single source of truth for streaming configuration"
- Founders need a bookmark-able URL to return to
- Enough content (URL copy, health history table, provider list) to warrant a full page
- Clean separation of concerns — the radio dashboard is operator-focused, the streaming center is founder-focused

---

## Decision 4: Setup Wizard delegates to existing settings pages (no new forms)

**Chosen:** Each wizard step shows an explanation and links to the relevant existing settings page (opens in same tab).

**Alternatives considered:**
1. Inline forms in the wizard (duplicate of existing settings forms)
2. HTMX-embedded settings forms inside the wizard card
3. Link-based wizard (chosen)

**Why link-based:**
- Sprint constraint: "DO NOT refactor existing services" / "Do not duplicate CSS"
- Avoids duplicating form validation logic that already exists in settings views
- Less code to maintain
- The wizard's job is to guide, not to be the form itself

**Trade-off:** User leaves the wizard page when they go to configure settings. The wizard tracks per-step completion via Django model queries (e.g. `SiteSettings.site_logo` is truthy), so when they return, the wizard shows the checkmark.

---

## Decision 5: Action Cards shown/hidden by server-side context flags

**Chosen:** Django view injects boolean flags (`has_radio_station`, `has_schedule`, etc.) into template context. The `{% if not has_radio_station %}` template tags control visibility.

**Why server-side:**
- No JavaScript dependency for a content-status feature
- Consistent with the project's existing server-rendered approach
- Zero additional API calls

**Trade-off:** Requires a page refresh to see that an action card has been dismissed. Acceptable UX for a "getting started" banner.

---

## Constraints Observed

| Constraint | How Met |
|-----------|---------|
| No backend architecture changes | All new code is additive (new views/urls, no service changes) |
| No service refactoring | Used existing radio, sponsor, news, podcast services as-is |
| No Partner Engine changes | Did not touch `platform/` or `PartnerMiddleware` |
| No schema changes | Session + localStorage used instead of new model fields |
| Coffee Theme only | All CSS uses `--amp-coffee-*` and `amp-*` component classes |
| No duplicate CSS | No new CSS written; all components reuse existing `amp-*` classes |
| No breaking changes | All existing views, URLs, and templates left intact |
| Responsive + mobile friendly | Cards use responsive grid; FAB positioned correctly on mobile |
| Maintain accessibility | All interactive elements have `aria-label`; semantic HTML used |
