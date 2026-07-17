# Next Sprint Recommendations
**Based on:** Sprint 3.4D completion + demo gap analysis
**Demo date:** July 21, 2026
**Prepared:** July 17, 2026

---

## Context

Sprint 3.4D delivered the live streaming integration layer. The architecture is sound. What remains before the July 21 demo is finishing the last 28 points of demo score — primarily visible gaps that the Kabulhaden team will immediately notice.

The next sprint should be **laser-focused on demo readiness**, not new features.

---

## Recommended Sprint: 3.5A — Demo Hardening

**Goal:** Close all visible demo gaps before July 21. No new features. No architectural work.

---

## Priority 1 — Business Value: HIGH | Technical Risk: LOW | Demo Importance: CRITICAL

### 1.1 — Create a superuser account and verify studio login
**Task ref:** Task #2 (existing proposed task)
**Effort:** 30 minutes
**Why now:** Without a login, the entire AMP Studio cannot be shown. This is the single highest-leverage action.
**Done when:** A demo user can log in at `/akun/masuk/` and reach `/studio/` dashboard.

### 1.2 — Verify live stream is reachable from demo machine
**Effort:** 1 hour (testing + documentation)
**Why now:** The architecture is complete but untested end-to-end. If `a7.siar.us` is unreachable on demo day, the live player shows "Offline" — which looks broken, not like a network issue.
**Done when:**
- `curl https://a7.siar.us/api/nowplaying/kabulhaden` returns valid JSON from the demo machine
- `/api/v1/radio/live/` returns `"status": "live"` (not `"offline"`) on the demo machine
- Dashboard listener count and track title show real data

---

## Priority 2 — Business Value: HIGH | Technical Risk: LOW | Demo Importance: HIGH

### 2.1 — Wire program name into the live API
**Task ref:** Task #7
**Effort:** 2–4 hours
**Why now:** "Tidak ada program" on the dashboard is the most visible gap. The Kabulhaden team will immediately ask "why doesn't it show the program name?"
**Done when:** `LiveRadioAPIView` queries the active broadcast schedule slot and returns the correct program name in the `program` field.

### 2.2 — Add a stream URL fallback setting
**Task ref:** Task #8
**Effort:** 1–2 hours
**Why now:** If the demo machine's stream response omits `station.listen_url`, the play button is silent. This is a silent failure that would embarrass the demo.
**Done when:** `STREAM_URL` env var is read as fallback; player has a URL even if provider omits it.

---

## Priority 3 — Business Value: MEDIUM | Technical Risk: MEDIUM | Demo Importance: MEDIUM

### 3.1 — Apply pending platform migrations
**Effort:** 30 minutes
**Why now:** Low-effort risk elimination. Unapplied migrations are a latent hazard during the demo if any platform feature is shown.
**Done when:** `python manage.py migrate` completes with no errors.

### 3.2 — Run and verify demo seed data
**Effort:** 30 minutes
**Why now:** The `demo_seed` command populates realistic Kabulhaden content. Without it, the dashboard shows mostly zeros.
**Done when:** `python manage.py demo_seed` completes; dashboard shows real article counts, schedule entries, and program data.

---

## Priority 4 — Business Value: LOW | Technical Risk: LOW | Demo Importance: LOW

### 4.1 — Add automated tests for LiveRadioAPIView
**Task ref:** Task #9
**Effort:** 2–3 hours
**Why now:** Not blocking the demo, but reduces risk of silent regressions if any last-minute changes are made before July 21.
**Done when:** `python manage.py test apps.radio` passes with coverage of the happy path and offline fallback.

---

## What to Defer (Post-Demo)

These are valuable but should not be started before July 21:

| Item | Reason to defer |
|------|----------------|
| WebSocket/SSE push for real-time updates | Requires Django Channels — multi-day effort |
| Full AMP Streaming Connector architecture | Planned post-demo replacement for Broadcastindo adapter |
| Dark mode | Design exists; implementation is multi-day |
| Mobile app | Future scope |
| Analytics deep-dive | Non-blocking for demo |
| Listener history charts with real data | DB records not yet populated from live stream |

---

## Sprint 3.5A Scope Summary

| Task | Priority | Effort | Demo Impact |
|------|----------|--------|-------------|
| Create superuser + verify login | P0 | 30 min | 🚨 Critical |
| Verify live stream on demo machine | P0 | 1 hr | 🚨 Critical |
| Wire program name (Task #7) | P1 | 3 hr | ⚠️ High |
| Stream URL fallback (Task #8) | P1 | 1 hr | ⚠️ High |
| Apply platform migrations | P2 | 30 min | ℹ️ Medium |
| Run demo_seed | P2 | 30 min | ℹ️ Medium |
| Live API tests (Task #9) | P3 | 2 hr | ℹ️ Low |
| **Total** | | **~8.5 hr** | |

**Recommended sprint duration:** 1 day (July 18) to leave July 19–20 as buffer before the July 21 demo.
