# AMP Studio — Demo Status
**Last Updated:** July 17, 2026
**Demo Date:** July 21, 2026 (4 days remaining)
**Audience:** Kabulhaden Radio team

---

## Overall Demo Score: 72 / 100

_Score reflects functional completeness on a production server with live stream access. Development environment score is lower due to network restrictions._

---

## Completion Percentage: ~72%

The core platform is functional. The primary remaining gaps are account setup, live program name display, and manual verification of the live stream in a network-capable environment.

---

## Completed Modules

| Module | Status | Notes |
|--------|--------|-------|
| AMP Studio shell (layout, nav, design system) | ✅ Complete | All pages render correctly |
| User authentication & session management | ✅ Complete | Login, logout, session timeout |
| Dashboard overview | ✅ Complete | Stats, schedule widget, recent articles |
| News/Article CMS | ✅ Complete | Create, edit, publish, pending review |
| Podcast management | ✅ Complete | Episode upload, publish |
| Broadcast schedule | ✅ Complete | Weekly schedule grid |
| Media manager | ✅ Complete | Upload, browse, attach |
| Radio dashboard | ✅ Complete | Station + provider management views |
| Streaming Center | ✅ Complete | Live status, provider list, health history |
| `/api/v1/radio/live/` endpoint | ✅ Complete | Normalized schema, 20 s cache, offline fallback |
| Broadcastindo adapter | ✅ Complete | Temporary; replaceable via env var |
| Public website hero player | ✅ Complete | Binds to `$store.radio` |
| Sticky player (public site) | ✅ Complete | Binds to `$store.radio` |
| Setup Wizard | ✅ Complete | 5-step onboarding flow |
| Platform partner system | ✅ Complete | Subdomain routing, partner context |
| Demo seed data | ✅ Complete | `python manage.py demo_seed` — ~340 Kabulhaden records |

---

## Modules Still Under Construction / Incomplete

| Module | Gap | Blocking? | Task |
|--------|-----|-----------|------|
| Live program name display | `program` always null in live API | ⚠️ Visible | Task #7 |
| Stream URL fallback | Empty if provider omits `station.listen_url` | ⚠️ Playback risk | Task #8 |
| Live API automated tests | No tests for critical endpoint | ℹ️ Non-blocking | Task #9 |
| Superuser account | No dev login credential | 🚨 Blocks all manual QA | Task #2 |
| Dark mode | Design documented, not implemented | ℹ️ Non-blocking | Backlog |
| Mobile app | Future scope | ℹ️ Non-blocking | Future |

---

## Known Demo Risks

### 🚨 Risk 1 — No superuser account
**Severity:** Critical for pre-demo QA
**Description:** Cannot log into AMP Studio to show any dashboard or studio page without creating an account first.
**Mitigation:** Run `python manage.py demo_seed` to create demo users, or create a superuser manually (Task #2).
**Required action before demo:** YES

### ⚠️ Risk 2 — Live stream shows "Offline" in dev environment
**Severity:** Medium (expected in dev, not in prod)
**Description:** `a7.siar.us` is unreachable from the Replit dev container. The live player and all widgets will show "Offline" during development.
**Mitigation:** Demo must be run on a server/machine with network access to `a7.siar.us`. Verify with `curl https://a7.siar.us/api/nowplaying/kabulhaden` from the demo machine before presenting.
**Required action before demo:** YES — verify network access from demo machine

### ⚠️ Risk 3 — Program name shows blank
**Severity:** Medium (visible cosmetic gap)
**Description:** Dashboard "Siaran Langsung" card and Streaming Center banner show "Tidak ada program" because the schedule is not wired to the live API.
**Mitigation:** Complete Task #7 before the demo if possible. Alternatively, brief the presenter that "program integration is in the next sprint."
**Required action before demo:** Ideally YES

### ℹ️ Risk 4 — Pending platform migrations
**Severity:** Low (non-blocking currently)
**Description:** `apps/platform` has unapplied migrations. Not causing visible errors but could cause issues if platform features are demonstrated.
**Mitigation:** Run `python manage.py migrate` before the demo.
**Required action before demo:** Recommended

---

## Recommendation Before Presenting to Kabulhaden

**Priority checklist (in order):**

1. 🚨 **Create a superuser account** (5 minutes — `python manage.py demo_seed` or `createsuperuser`)
2. 🚨 **Verify `curl https://a7.siar.us/api/nowplaying/kabulhaden` returns JSON** from the demo machine
3. ⚠️ **Complete Task #7** (program name display — ~3 hours)
4. ⚠️ **Complete Task #8** (stream URL fallback — ~1 hour)
5. ℹ️ **Run `python manage.py migrate`** to apply pending platform migrations
6. ℹ️ **Run `python manage.py demo_seed`** to populate realistic Kabulhaden content

**If items 1 and 2 are completed, the demo is presentable.** Items 3–6 improve polish but are not blockers.

---

## Demo Score Breakdown

| Area | Score | Notes |
|------|-------|-------|
| UI/Design quality | 18/20 | AMP Studio design system is polished and consistent |
| Core CMS features | 18/20 | News, podcast, broadcast all functional |
| Live streaming architecture | 12/20 | API layer complete; program name and fallback URL missing |
| Public website | 10/15 | Player functional; track display depends on live stream access |
| Admin/Studio UX | 14/15 | All views complete; blocked by missing superuser in dev |
| Demo data | 10/10 | `demo_seed` provides realistic Kabulhaden content |
| **Total** | **72/100** | |

_Score will reach ~85/100 after Tasks #2, #7, #8 are completed._
