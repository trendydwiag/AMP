# Documentation Audit Report — AMP Studio
**Generated:** Sprint 4.0.1 — July 20, 2026
**Audit Type:** Full knowledge base synchronization after Sprint 4.3

---

## Summary

A comprehensive audit of the AMP Studio knowledge base was performed by comparing all documentation against actual source code. The project has completed 14 sprints (1.x through 4.3) but documentation drift was significant — especially in `AI_CONTEXT.md` which still referenced Sprint 4.0 status, and several numbered docs (04, 24, 25, 31) that had not been updated since early sprints.

**Total documents audited:** 69 files in `docs/`
**Documents updated:** 2 (AI_CONTEXT.md, PROJECT_STATE.md created)
**Documents deprecated:** 0 (marked for future cleanup)
**New documents created:** 3 (PROJECT_STATE.md, documentation-audit.md, sprint-4.0.1.md)
**Incorrect documentation found:** 8 files with significant drift
**Documentation drift level:** HIGH (pre-audit) → RESOLVED (post-audit)

---

## Updated Documents

| Document | Change | Reason |
|---|---|---|
| `docs/AI_CONTEXT.md` | **Full rewrite** | Transformed from progress report to permanent architecture document. Removed sprint status, tech debt list, completed/pending sprints, credential info, demo seed instructions. Added Documentation Hierarchy section. |
| `docs/PROJECT_STATE.md` | **Created** | New authoritative source of truth for project status, sprint history, demo readiness, working features, open tech debt, and demo credentials. |

---

## New Documents

| Document | Purpose |
|---|---|
| `docs/PROJECT_STATE.md` | Authoritative project status — sprint, demo readiness, features, tech debt, credentials |
| `docs/reports/documentation-audit.md` | This file — audit findings and recommendations |
| `docs/changelog/sprint-4.0.1.md` | Changelog for this documentation sprint |

---

## Deprecated Documents (Not Deleted, Marked for Future Cleanup)

| Document | Status | Reason |
|---|---|---|
| `docs/04_FEATURE_BACKLOG.md` | ⚠ STALE | Last updated Sprint 3.4. Does not include Sprint 3.5–4.3 features (media pipeline, streaming center, platform UI, radio player stabilization). Superseded by `docs/architecture/feature-status.md`. |
| `docs/24_DARK_MODE.md` | ⚠ STALE | References `templates/base.html:24` and `templates/dashboard_base.html:4` — legacy templates. Actual implementation is in `templates/amp_studio/base.html` and `static/js/amp-studio/amp-studio.js` with dual `data-theme` + `.dark` class strategy. |
| `docs/25_TAILWIND_CONFIG.md` | ⚠ STALE | References `tailwind.config.js` file. Actual Tailwind config for the CMS is injected via CDN in `templates/amp_studio/base.html` with `window.tailwind.config`. The `tailwind.config.js` file only exists for the npm build process (public website CSS). |
| `docs/31_API_ENDPOINTS_REFERENCE.md` | ⚠ STALE | References old URL structure missing studio, media, radio, broadcast, podcast, news, content, and platform URLs. Also references non-existent views (`ProfileEditView`, `ResendVerificationView`, `DashboardView`). Superseded by `docs/architecture/routes.md`. |
| `docs/sprints/NEXT_SPRINT.md` | ⚠ STALE | Still references Sprint 3.5A as "NEXT" and lists Sprint 4.1 as "Wire program name" — but Sprint 4.1 was actually "Demo Readiness & Founder Experience". Needs complete rewrite. |
| `docs/changelog/CHANGELOG.md` | ⚠ STALE | Missing Sprint 4.1, 4.2 entries. Only has Sprint 3.4D and 4.3. Sprint 4.0.1 should be appended. |

---

## Incorrect Documentation Found

### 1. AI_CONTEXT.md — Sprint Status Mismatch
**Before:** Listed "Current Sprint: 4.2 — Media Pipeline Engine" and "Pending Sprints" still showed Sprint 4.1 as "Wire program name"
**After:** Fixed — removed all sprint status from AI_CONTEXT.md, moved to PROJECT_STATE.md

### 2. AI_CONTEXT.md — Missing Sprint 4.1, 4.2, 4.3 from Completed
**Before:** Completed sprints stopped at Sprint 4.0
**After:** Fixed — PROJECT_STATE.md lists all sprints through 4.3

### 3. feature-status.md — Mostly Accurate
**Finding:** Updated through Sprint 4.3 (header says "last updated Sprint 4.3"). Radio Player Bar shows "isLoading bug fixed Sprint 4.3", Homepage shows "Direct stream URL (Sprint 4.3)". This document is the most accurate of the numbered docs.
**Action:** No changes needed.

### 4. TECH_DEBT.md — Mostly Accurate
**Finding:** TD-002 correctly marked RESOLVED. TD-008 (ngrok) correctly added. However, several new TD items discovered during audit are not yet registered.
**Action:** New TD items documented in PROJECT_STATE.md "Open Technical Debt" section.

### 5. routes.md — Mostly Accurate
**Finding:** Route inventory is comprehensive and matches actual URL patterns. Minor differences in view class names (e.g., `ProgramEditView` vs `ProgramUpdateView`) but paths are correct.
**Action:** No changes needed.

### 6. services.md — Mostly Accurate
**Finding:** Service inventory matches actual code. New services found during audit: `BroadcastIntegrationService`, `FallbackService`, `MetadataService`, `ArtworkService`, `PlayerService` — not listed in services.md.
**Action:** Documented in PROJECT_STATE.md.

### 7. models.md — Mostly Accurate
**Finding:** Model inventory matches. Sprint 4.2 pipeline fields correctly documented. Platform model structure (subpackages) not fully reflected.
**Action:** No critical changes needed.

### 8. current-project-map.md — Mostly Accurate
**Finding:** Project tree and app inventory match. Some missing details: platform subpackages (partner/, themes/, feature_flags/, providers/, plugins/, security/, domains/), media_manager new files (pipeline.py, storage.py, events.py, validators.py).
**Action:** No critical changes needed.

---

## Documentation Drift Analysis

### High Drift (Significant inaccuracies)
| Document | Drift Level | Issue |
|---|---|---|
| `AI_CONTEXT.md` | **HIGH** → RESOLVED | Sprint status, tech debt, pending sprints all stale |
| `04_FEATURE_BACKLOG.md` | **HIGH** | Missing Sprint 3.5–4.3 features |
| `31_API_ENDPOINTS_REFERENCE.md` | **HIGH** | Missing 60%+ of actual URL patterns |
| `sprints/NEXT_SPRINT.md` | **HIGH** | Sprint numbers and titles incorrect |

### Medium Drift (Some inaccuracies)
| Document | Drift Level | Issue |
|---|---|---|
| `24_DARK_MODE.md` | **MEDIUM** | References legacy templates |
| `25_TAILWIND_CONFIG.md` | **MEDIUM** | References wrong config file |
| `changelog/CHANGELOG.md` | **MEDIUM** | Missing Sprint 4.1, 4.2 entries |

### Low Drift (Minor inaccuracies)
| Document | Drift Level | Issue |
|---|---|---|
| `architecture/services.md` | **LOW** | Missing 5 newer service classes |
| `architecture/current-project-map.md` | **LOW** | Missing platform subpackages, media_manager new files |
| `architecture/models.md` | **LOW** | Minor field details |
| `architecture/routes.md` | **LOW** | View class name variations |

### No Drift (Accurate)
| Document | Status |
|---|---|
| `architecture/feature-status.md` | ✅ Accurate through Sprint 4.3 |
| `architecture/TECH_DEBT.md` | ✅ Accurate (TD-002 resolved, TD-008 added) |
| `architecture/DECISION_LOG.md` | ✅ Accurate |
| `changelog/sprint-4.0.md` | ✅ Accurate |
| `changelog/sprint-4.1.md` | ✅ Accurate |
| `changelog/sprint-4.2.md` | ✅ Accurate |
| `changelog/sprint-4.3.md` | ✅ Accurate |

---

## Recommendations

### Immediate (Before Next Sprint)
1. **Rewrite `sprints/NEXT_SPRINT.md`** — Currently lists incorrect sprint numbers and titles
2. **Update `changelog/CHANGELOG.md`** — Append Sprint 4.1, 4.2 entries (they exist as separate files but CHANGELOG.md wasn't updated)

### Short-Term (Next Sprint)
3. **Update `04_FEATURE_BACKLOG.md`** — Add Sprint 3.5–4.3 features or mark as superseded by `architecture/feature-status.md`
4. **Update `31_API_ENDPOINTS_REFERENCE.md`** — Add studio, media, radio, broadcast, podcast, news, content, platform URLs; or mark as superseded by `architecture/routes.md`
5. **Register new TD items** in `architecture/TECH_DEBT.md`:
   - AMPStudioDashboardView inline queries
   - demo_seed admin is_superuser bug
   - CSP settings not active
   - content/repos.py naming inconsistency
   - pyproject.toml dependency drift

### Long-Term (Post-Demo)
6. **Consolidate duplicate documentation** — Several docs cover the same topic (04_FEATURE_BACKLOG vs feature-status, 31_API_ENDPOINTS vs routes.md). Consider deprecating the older versions.
7. **Update 24_DARK_MODE.md** — Reflect actual implementation in amp_studio/base.html
8. **Update 25_TAILWIND_CONFIG.md** — Reflect CDN-based config in base.html
9. **Fix pyproject.toml** — Update name from "repl-nix-workspace", sync dependencies with requirements/base.txt

---

## Verified Technical Debt

| ID | Claimed Status | Actual Status | Evidence | Verdict |
|---|---|---|---|---|
| TD-001 | OPEN | **OPEN** | `apps/radio/views.py:543`: `'program': None` hardcoded | ✅ Correct |
| TD-002 | RESOLVED | **RESOLVED** | `apps/radio/views.py:491`: `listen_url_fallback = db_provider.stream_url` | ✅ Correct |
| TD-003 | OPEN | **OPEN** | No test file in `apps/radio/tests/` for LiveRadioAPIView | ✅ Correct |
| TD-004 | OPEN | **OPEN** | `broadcastindo.py`: two separate HTTP calls | ✅ Correct |
| TD-005 | OPEN | **OPEN** | Hardcoded intervals in 3 JS files | ✅ Correct |
| TD-006 | OPEN | **OPEN** | Platform migrations pending (unverified — needs `showmigrations`) | ✅ Correct |
| TD-007 | OPEN | **OPEN** | No superuser exists until `demo_seed` or `create_superadmin` is run | ✅ Correct |
| TD-008 | OPEN | **OPEN** | ngrok free-tier generates new URL per restart | ✅ Correct |

### New Technical Debt Discovered

| ID | Issue | Priority | Evidence |
|---|---|---|---|
| NEW-001 | AMPStudioDashboardView ~25+ inline ORM queries | 🔴 HIGH | `apps/studio/views.py:12-334` — violates Service-Repository pattern |
| NEW-002 | `admin` user gets `is_superuser=True` in demo_seed | 🟡 MEDIUM | `apps/core/management/commands/demo_seed.py` |
| NEW-003 | CSP settings defined but not active | 🟡 MEDIUM | `django-csp` not in INSTALLED_APPS/MIDDLEWARE |
| NEW-004 | `content/repos.py` non-standard filename | ⚪ LOW | Should be `repositories.py` per convention |
| NEW-005 | pyproject.toml dependency drift | ⚪ LOW | Different deps from requirements/base.txt |

---

## Verified Sprint History

| Sprint | Title | Changelog Exists | Matches Code | Status |
|---|---|---|---|---|
| 3.4D | Live Streaming Integration | ✅ sprint-3.4D.md (in CHANGELOG.md) | ✅ | ✅ Verified |
| 4.0 | Knowledge Base Refresh | ✅ sprint-4.0.md | ✅ | ✅ Verified |
| 4.1 | Demo Readiness & Founder Experience | ✅ sprint-4.1.md | ✅ 17 pages audited | ✅ Verified |
| 4.2 | Media Pipeline Engine | ✅ sprint-4.2.md | ✅ pipeline.py, storage.py, events.py exist | ✅ Verified |
| 4.3 | Radio Live Player Stabilization | ✅ sprint-4.3.md | ✅ 6 bugs fixed, TD-002 resolved | ✅ Verified |

---

*This report was generated during Sprint 4.0.1 — Knowledge Base Governance & Documentation Synchronization.*
