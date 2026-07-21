# DEMO FREEZE — July 21, 2026

**Status:** 🔒 FROZEN FOR DEMO  
**Freeze Time:** July 21, 2026  
**Target Demo:** Radio Kabulhaden client demo, 18:00 WIB  
**Frozen By:** Sprint 4.5 — Demo Readiness Verification & End-to-End Acceptance  

---

## Frozen Git Commit

```
Commit : 34e4db68f9e582471d9abdfb3e0547d8fcade4cf
Branch : main
Date   : 2026-07-21 05:05:20 UTC  (12:05:20 WIB)
Message: Sprint 4.5: Demo Readiness Verification & End-to-End Acceptance
```

---

## Project Version at Freeze

**AMP Studio v0.4.6** — after Sprint 4.5

---

## Demo Readiness Score at Freeze

**98 / 100**

- Critical blockers: **NONE**
- Routes verified OK: **32+**
- CRUD flows verified: **Program, Schedule, Playlist, News, Podcast, Media**
- Auth roles verified: **superadmin, admin, editor, viewer**
- Public website verified: **Homepage, Program, Podcast, News, Article Detail**
- Live Radio API: **All required fields present**

Full report: `docs/reports/sprint-4.5-demo-readiness.md`

---

## What Is Frozen

All code in the `main` branch at commit `34e4db6` is frozen for demo.

This includes:
- All Django apps (`apps/`)
- All templates (`templates/`)
- All static files (`static/`)
- All configuration (`config/`)
- All documentation (`docs/`)
- All management commands
- All migrations (applied)
- All dependencies (`requirements/`)

---

## Demo Credentials

| Username | Password | Role |
|---|---|---|
| superadmin | DemoAdmin2024! | SUPERUSER |
| admin | DemoAdmin2024! | ADMINISTRATOR |
| editor | DemoEditor2024! | EDITOR |
| viewer | DemoViewer2024! | VIEWER |

---

## Known Limitations at Freeze (Non-Blocking)

| Issue | Notes |
|---|---|
| `current_program` null at non-scheduled hours | Resolver works correctly — no schedule at 12:00 WIB TUE. At 18:00 WIB, CadasPersada (TUE 18:00–19:00) will be active. |
| `stream.kabulhaden.online` DNS not resolving from Replit dev container | External dependency. Stream audio works on production servers with internet access. |
| Playlist: 0 entries | demo_seed does not seed playlist items. Empty state displayed correctly. CRUD works. |
| MediaFile: 0 | demo_seed does not upload files. Empty state displayed. Upload form works. |
| Tailwind CDN browser console warning | Known TD-010. Not visible to client. |
| `admin` user has unintended `is_superuser=True` | Known TD, not visible in CMS demo flow. |

---

## DEMO LOCK RULES (Active)

From this point, the following actions are **PROHIBITED** without explicit owner approval:

- Creating new features
- Redesigning UI
- Changing the design system
- Changing the database schema
- Running new migrations
- Running `demo_seed --reset`
- Refactoring architecture
- Changing the streaming provider
- Changing stream URLs
- Changing RBAC
- Changing business logic
- Deleting demo data
- Deleting documentation

Only permitted actions post-freeze:

- Emergency bug fix for a live demo blocker
- Updating stream provider URL in DB if ngrok restarts (operational, not code)
- Reading logs

---

## Rollback Instructions

To restore this exact state at any time:

```bash
git checkout 34e4db68f9e582471d9abdfb3e0547d8fcade4cf
```

Or via Replit checkpoint saved at this commit.
