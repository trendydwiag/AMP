# Sprint 4.0 — Knowledge Base Refresh & Project Reindex

**Tanggal:** 17 Juli 2026
**Tipe:** Documentation Sprint — tidak ada perubahan business logic
**Tujuan:** Sinkronisasi pemahaman AI terhadap kondisi project terkini

---

## Ringkasan

Sprint ini adalah sprint dokumentasi murni. Seluruh codebase di-scan, didokumentasikan, dan divalidasi terhadap dokumen yang sudah ada. Tidak ada perubahan kode, tidak ada refactor, tidak ada fitur baru.

---

## Dokumen Baru yang Dibuat

### Step 5 — Architecture Inventory
**File:** `docs/architecture/current-project-map.md`
- Project tree lengkap
- App inventory (14 apps) dengan namespace dan mount point
- Dependencies (Python + Frontend CDN)
- Service Layer, Repository Layer, Broadcast Layer, Content Layer, Podcast Layer, Analytics Layer, Authentication Layer, Partner Layer
- Public API dan Internal API inventory
- Data flow diagram
- Routing summary
- Background jobs (management commands — tidak ada Celery)
- Storage, media, caching, external integrations

### Step 6 — Feature Status Inventory
**File:** `docs/architecture/feature-status.md`
- Status lengkap per modul: ✅ Complete | 🟡 Partial | ⚪ Planned
- 13 modul: Users, Core, Settings, Media Manager, Radio Engine, Broadcast, Podcast, News, Sponsor, Community, Platform, AMP Studio, Public Website
- Mencakup perubahan Sprint 3.5, 3.6, 3.7, 4.0

### Step 7 — Route Inventory
**File:** `docs/architecture/routes.md`
- Semua URL di seluruh project
- Termasuk: path, view class, url name, auth requirement
- Auth legend: 🔓 Public | 🔒 Login Required | 👑 SUPERUSER/ADMIN only
- Grouped by namespace/app

### Step 8 — Data Model Inventory
**File:** `docs/architecture/models.md`
- Semua model dengan field lengkap (type + relationship)
- Relationships summary diagram
- Known model issues: naming conflicts (sponsor.Partner vs platform.Partner, news.Tag vs media_manager.Tag vs content.ContentTag)

### Step 9 — Service & Repository Inventory
**File:** `docs/architecture/services.md`
- BaseRepository dan BaseService dari `utils/`
- Semua service + repository per app
- Radio provider adapters (Broadcastindo active, AzuraCast partial, rest stub)
- Technical debt note: AMPStudioDashboardView inline queries

### Step 15 — AI Context
**File:** `docs/AI_CONTEXT.md` ← **DOKUMEN WAJIB DIBACA**
- Visi project
- Arsitektur lengkap
- Coding rules
- Design system (coffee palette, dark mode, Tailwind config)
- Naming convention
- Folder convention
- Layer architecture
- Business rules (RBAC, Partner, Settings singleton, Live Radio API, StreamHealth fields)
- Broadcast concept, Podcast concept, Analytics concept
- Sprint history (completed + pending)
- Known issues
- Technical debt
- DO NOT list
- Best practices

---

## Temuan: Dokumen Usang

Dokumen berikut masih ada tapi perlu diperhatikan statusnya:

| Dokumen | Status | Catatan |
|---|---|---|
| `docs/sprints/NEXT_SPRINT.md` | ⚠ STALE | Ditulis untuk Sprint 3.5A — sebagian besar sudah selesai di Sprint 3.5–3.7 |
| `docs/adr/0020-caching-strategy.md` | ⚠ STALE | Redis masih "Planned" — dev saat ini pakai Django default cache |
| `docs/04_FEATURE_BACKLOG.md` | ⚠ STALE | Terakhir diupdate Sprint 3.4; belum mencerminkan Sprint 3.5–4.0 |
| `docs/25_TAILWIND_CONFIG.md` | ⚠ STALE | Config Tailwind CDN sudah berubah (coffee palette + darkMode:'class' ditambahkan Sprint 3.7/4.0) |
| `docs/24_DARK_MODE.md` | ⚠ STALE | Implementasi dark mode berubah (butuh .dark class + data-theme, dijelaskan di AI_CONTEXT.md) |
| `docs/content/*.md` (VERSIONING, PUBLISHING) | ⚠ STALE | Boilerplate template, belum ada implementasi spesifik |

Semua dokumen di atas **tidak dihapus** sesuai instruksi sprint. Status STALE ditambahkan di sini.

---

## Temuan: Duplikasi

Step 10 — dilaporkan, tidak diperbaiki:

| Duplikasi | Lokasi | Catatan |
|---|---|---|
| CRUD view pattern | broadcast, podcast, news, content | ListView + CreateView + LoginRequiredMixin + AuditLogMixin hampir identik |
| List + filter template | `program_list.html`, `episode_list.html`, `article_list.html` | HTML structure + Alpine.js filter logic hampir sama |
| Tag model | `news.Tag`, `media_manager.Tag`, `content.ContentTag` | Tiga model tag berbeda di tiga app |
| Category model | `news.Category`, `content.ContentCategory` | Dua model kategori berpotensi overlap |
| Partner model | `sponsor.Partner`, `platform.Partner` | Nama sama tapi tujuan berbeda — berpotensi membingungkan import |

---

## Temuan: Dead Code

Step 11 — dilaporkan, tidak dihapus:

| Item | Lokasi | Catatan |
|---|---|---|
| `static/broadcast/` | `static/broadcast/` | Direktori kosong |
| `static/radio/` | `static/radio/` | Direktori kosong |
| `dashboard_base.html` extend | `templates/dashboard/home.html`, `templates/core/home.html` | Masih pakai layout lama, belum dimigrasikan |

---

## Temuan: TODO / FIXME / Placeholder

Step 12 — tidak ada TODO/FIXME explicit di `.py` atau `.html` files.
Semua placeholder yang ditemukan adalah UI `placeholder` attribute di form fields — bukan code debt.

---

## Temuan: Legacy Components

Step 13 — dilaporkan:

| File | Legacy Element | Catatan |
|---|---|---|
| `templates/dashboard/home.html` | Extends `dashboard_base.html` | Layout lama — belum dimigrasikan ke `amp_studio/base.html` |
| `templates/core/home.html` | Extends `dashboard_base.html` | Layout lama — belum dimigrasikan |
| `static/css/dashboard.css` | Legacy dashboard CSS | Masih diload oleh `dashboard_base.html` |
| `static/css/homepage.css` | Legacy homepage CSS | Diload oleh public website — bukan legacy tapi perlu verifikasi relevance |

---

## Roadmap Update

Step 14 — sprint status update:

| Sprint | Judul | Status Lama | Status Baru |
|---|---|---|---|
| 3.5 | Founder Experience | NEXT | ✅ DONE |
| 3.6 | Platform UI Consistency | NEXT | ✅ DONE |
| 3.6+ | Logo/footer DB integration | — | ✅ DONE |
| 3.7 | UX/Visual Regression Fixes | — | ✅ DONE |
| 4.0 | Knowledge Base Refresh | NEXT | ✅ DONE |

Sprint berikutnya yang direkomendasikan: **Sprint 4.1** — Wire program name ke live API (TD-001), atau **Sprint 4.3** — Create superuser account (Task #2, CRITICAL untuk demo).

---

## Sprint 4.0 Juga Mencakup Fixes (dari Sprint 3.7 yang selesai di sesi yang sama)

Sebelum dokumentasi dimulai, beberapa bug kritis diperbaiki dalam sesi yang sama:

### Fix 1 — Streaming Center 500 Error
- **File:** `templates/amp_studio/streaming_center.html`
- **Problem:** Template mengakses field StreamHealth yang salah (h.status, h.checked_at, h.listener_count, h.bitrate, h.codec)
- **Fix:** Ganti ke field yang benar (h.provider_status, h.last_checked, h.response_time, h.stream_bitrate, h.stream_format)
- **Status badge:** `{% if h.provider_status == 'HEALTHY' %}` dengan choices HEALTHY/DEGRADED/DOWN/TIMEOUT

### Fix 2 — Tailwind Coffee Palette + Dark Mode Class Strategy
- **File:** `templates/amp_studio/base.html`
- **Problem:** Coffee-* utility classes tidak berfungsi; dark: variants tidak aktif
- **Fix:** Tambah `darkMode: 'class'` + coffee color palette ke Tailwind CDN config
- **Commit:** bb5d447

### Fix 3 — Settings Dark Mode Override (dari Sprint 3.7)
- **File:** `templates/settings/base.html`
- **Problem:** `style="color-scheme: light"` hardcoded di `<main>` block dark mode di halaman pengaturan
- **Fix:** Dihapus

---

## Commit Reference

| Sprint | Commit | Tanggal |
|---|---|---|
| Sprint 3.7 fixes | f426857 | Juli 17, 2026 |
| Sprint 4.0 (streaming + Tailwind) | bb5d447 | Juli 17, 2026 |
| Sprint 4.0 dokumentasi | (sprint ini) | Juli 17, 2026 |
