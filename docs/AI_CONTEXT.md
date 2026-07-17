# AI_CONTEXT.md — Kabulhaden CMS / AMP Studio
**Wajib dibaca sebelum mengerjakan sprint apapun.**
**Last updated:** Sprint 4.0 — July 17, 2026

---

## Visi Project

**Kabulhaden CMS** (codename: **AMP Studio** — Aradhana Media Platform) adalah sistem manajemen konten berbasis Django yang dibangun khusus untuk stasiun radio. Tujuannya: menggantikan patchwork tool yang dipakai stasiun radio (sistem streaming terpisah, spreadsheet jadwal, website statis) dengan satu platform terpadu.

**Satu platform untuk:** live radio stream → jadwal siaran → episode → podcast → berita → komunitas → sponsor → website publik.

Klien pertama: **Radio Kabulhaden** (demo target: 21 Juli 2026).

---

## Arsitektur

### Stack
- **Backend:** Django 5.0.14 | Python 3.13 | PostgreSQL (psycopg3)
- **Frontend:** Alpine.js 3 (lokal) | Tailwind CSS CDN (Play mode) | HTMX 1.9.10
- **Static:** WhiteNoise + brotli
- **Dev server:** Gunicorn di Replit (port 5000)

### Layer Architecture
```
Request → Django URL routing
        → View (LoginRequiredMixin + AuditLogMixin)
        → Service (business logic, transactions)
        → Repository (ORM queries)
        → Model (Django ORM)
        → PostgreSQL
```

Semua business logic ada di `apps/*/services.py`.
Semua ORM query ada di `apps/*/repositories.py`.
View hanya mengorchestrasi — tidak boleh ada query ORM langsung di view.

**Pengecualian yang diketahui (Technical Debt):** `AMPStudioDashboardView` di `apps/studio/views.py` masih punya inline model queries. Ini TD yang harus diperbaiki di sprint berikutnya.

### Multi-Tenant Architecture
Setiap content item (Program, Article, Podcast, MediaFile) punya `FK → platform.Partner`. Middleware resolve partner aktif dari request. Superuser bisa switch partner via dropdown sidebar. Setiap partner bisa punya custom theme, feature flags, dan usage limits.

### Folder Convention
```
apps/<nama_app>/
    models.py        # Data models
    services.py      # Business logic (no direct ORM)
    repositories.py  # ORM queries only
    views.py         # Orchestration only
    urls.py          # URL patterns + namespace
    forms.py         # Django forms
    templatetags/    # Custom template tags

templates/
    amp_studio/      # Semua template CMS Studio
        base.html    # BASE TEMPLATE TUNGGAL untuk semua halaman CMS
        components/  # Header, sidebar, player_bar, etc.
    broadcast/       # Broadcast CMS templates
    settings/        # Settings templates (base.html sendiri)
    website/         # Public website templates
    users/           # Auth + user admin templates

static/
    css/amp-studio/  # AMP Studio CSS system (design-tokens, components, layout)
    js/amp-studio/   # amp-studio.js (Alpine components + theme engine)
```

---

## Design System

### Warna — Coffee Palette
| Token | Hex | Penggunaan |
|---|---|---|
| coffee-50 | #FAF7F3 | Background page (light) |
| coffee-100 | #F5F0EA | Surface cards (light) |
| coffee-200 | #E7DDD3 | Borders (light) |
| coffee-300 | #C89B6D | Accent light |
| coffee-400 | #8C5A3C | Primary action |
| coffee-500 | #6B4226 | Primary dark |
| coffee-600 | #4E2F1F | **Brand primary** |
| coffee-700 | #3A2318 | Header background |
| coffee-800 | #2B1A13 | Surface (dark mode) |
| coffee-900 | #1A0F0B | Background (dark mode) |

CSS variables: `var(--amp-coffee-600)` etc. Didefinisikan di `static/css/amp-studio/design-tokens.css`.

### Typography
- **Heading:** Poppins (CDN Google Fonts)
- **Body:** Inter (CDN Google Fonts)

### Dark Mode
- AMP Studio CSS menggunakan selector `[data-theme="dark"]`
- Tailwind `dark:` variants membutuhkan class `.dark` di `<html>`
- **KEDUANYA harus diset bersamaan** di `amp-studio.js`: `data-theme` attribute + `.dark` class
- Tailwind CDN config: `darkMode: 'class'` + coffee palette → di `templates/amp_studio/base.html`

### Tailwind Config (amp_studio/base.html)
```js
window.tailwind = {
  config: {
    darkMode: 'class',
    corePlugins: { preflight: false },
    theme: {
      extend: {
        colors: {
          coffee: { 50:'#FAF7F3', 100:'#F5F0EA', 200:'#E7DDD3', 300:'#C89B6D',
                    400:'#8C5A3C', 500:'#6B4226', 600:'#4E2F1F', 700:'#3A2318',
                    800:'#2B1A13', 900:'#1A0F0B' }
        }
      }
    }
  }
};
```

---

## Coding Rules

### WAJIB
1. **Semua query ORM di repository** — tidak ada `Model.objects.filter()` langsung di view
2. **Semua business logic di service** — view hanya orchestrate
3. **UUID primary keys** — via `UUIDPrimaryKeyMixin`
4. **TimeStampedModel** — semua model punya `created_at`, `updated_at`
5. **Bahasa Indonesia di UI** — semua label, breadcrumb, navigasi dalam Bahasa Indonesia
6. **AMP Studio base template** — semua halaman CMS extend `amp_studio/base.html`
7. **AuditLogMixin** — semua view CMS yang write harus include audit logging
8. **LoginRequiredMixin** — semua view CMS harus protected

### DILARANG
1. Jangan query ORM langsung di view atau template
2. Jangan hardcode warna hex di template — gunakan CSS variables `var(--amp-coffee-*)`
3. Jangan hardcode localhost di kode aplikasi — gunakan relative URL
4. Jangan buat base template baru — gunakan `amp_studio/base.html` yang sudah ada
5. Jangan refactor tanpa task yang di-approve user
6. Jangan hapus dokumentasi — tandai `DEPRECATED` jika sudah tidak relevan
7. Jangan commit kredensial atau secret ke git

### Alpine.js
- Gunakan `Alpine.store('radio')` — bukan `x-data="radioPlayer()"`
- Global store `ampStudio` sudah ada di `amp-studio.js` — jangan duplicate
- Untuk toggle dark mode: set `data-theme` attribute DAN `.dark` class di `<html>` **bersamaan**

---

## Naming Convention

| Element | Convention | Contoh |
|---|---|---|
| URL name (Indonesia) | snake_case Indonesia | `program_list`, `jadwal_buat` |
| Template file | lowercase_underscore | `program_list.html` |
| View class | PascalCase + suffix | `ProgramListView`, `ProgramCreateView` |
| Service class | PascalCase + Service | `ProgramService` |
| Repository class | PascalCase + Repository | `ProgramRepository` |
| Model field | snake_case | `start_time`, `is_active` |
| CSS class (AMP) | `amp-` prefix | `amp-badge`, `amp-card` |
| URL namespace | lowercase app name | `broadcast`, `radio`, `podcast` |

---

## Business Rules

### RBAC Roles
| Role | Level | Akses |
|---|---|---|
| SUPERUSER | 4 | Semua — termasuk platform management, partner switch |
| ADMINISTRATOR | 3 | CMS semua modul, user management |
| EDITOR | 2 | Buat/edit konten, tidak bisa delete user |
| VIEWER | 1 | Read-only di semua modul |

### Partner Concept
- Setiap stasiun radio adalah satu `Partner`
- Partner pertama = Kabulhaden (seeded via `init_settings` + `seed_platform`)
- User bisa punya membership di multiple partners
- SUPERUSER bisa switch partner tanpa membership

### Settings Singleton
- Semua settings (`SiteSettings`, `SocialMediaSettings`, dll) punya pk=1
- Akses via `.load()` class method
- Jangan gunakan `SiteSettings.objects.first()` — gunakan `SiteSettings.load()`
- Context processor sudah expose semua settings ke semua template secara otomatis

### Live Radio API
- Endpoint: `GET /api/v1/radio/live/`
- Response di-cache 20 detik (env: `STREAM_CACHE_TTL`)
- Provider aktif: Broadcastindo (`a7.siar.us`) — via `BroadcastindoAdapter`
- Field `program` selalu null (**TD-001** — belum ada integrasi ke broadcast schedule)
- Polling dari frontend: 25 detik (sesuai cache TTL)

### StreamHealth Field Names
| BENAR | SALAH (jangan pakai) |
|---|---|
| `provider_status` | `status` |
| `last_checked` | `checked_at` |
| `stream_bitrate` | `bitrate` |
| `stream_format` | `codec` |
| `response_time` | `listener_count` |
| `get_provider_status_display` | `get_status_display` |
| Status values: HEALTHY/DEGRADED/DOWN/TIMEOUT | healthy/degraded/down |

### Demo Seed
- Jalankan: `python manage.py demo_seed [--reset]`
- Mengisi ~340 records data REAL Kabulhaden (dari pitch deck)
- Harus dijalankan setelah `python manage.py migrate`

---

## Broadcast Concept

```
Program (acara radio)
  └── Schedule (jadwal siaran: hari + jam)
      └── BroadcastSession (instance siaran: scheduled → live → finished)
          └── Episode (rekaman dari session)
              └── EpisodeGuest (bintang tamu)
  └── HostMember (host tetap program)
  └── Playlist → PlaylistItem (lagu-lagu yang diputar)
```

Pengumuman (`Announcement`) adalah independent dari program — bersifat global.

## Podcast Concept

```
Podcast (serial/show)
  └── PodcastEpisode (episode: season/episode number, audio file)
```

Distribution links (Spotify, iTunes, Google) ada di level Podcast, bukan Episode.

## Analytics Concept

Analytics saat ini **stub** — view dan template ada tapi data belum real. Data listener dari `ListenerStatistic` tersedia tapi belum diagregasi ke dashboard analytics. Sprint mendatang perlu mengisi ini.

---

## Current Sprint

**Sprint 4.2 — Media Pipeline Engine**
- Jenis: Backend architecture — tidak ada perubahan UI
- Deliverables: pipeline.py, storage.py, events.py, migration 0003, Media Inspector view, changelog/sprint-4.2.md
- Status: Selesai (17 Juli 2026)

---

## Completed Sprints

| Sprint | Judul | Status | Tanggal |
|---|---|---|---|
| 1.x | Project Setup & Foundation | ✅ DONE | — |
| 2.x | Core modules (users, settings, media) | ✅ DONE | — |
| 3.0–3.3 | Broadcast, Radio, Podcast, News, Content | ✅ DONE | — |
| 3.4 | Live Radio Engine (multi-provider, now-playing API) | ✅ DONE | Juli 2026 |
| 3.4D | Streaming integration + now-playing cache | ✅ DONE | Juli 2026 |
| 3.5 | Founder Experience (wizard, tour, dark mode, health widget) | ✅ DONE | Juli 17, 2026 |
| 3.6 | Platform UI Consistency (amp_studio/base migration, breadcrumbs, komunitas/iklan pages) | ✅ DONE | Juli 17, 2026 |
| 3.6+ | Logo/footer dari DB, contact fields, social media icons di footer | ✅ DONE | Juli 17, 2026 |
| 3.7 | UX/visual regressions (dark mode .dark class, streaming 500, settings dark mode) | ✅ DONE | Juli 17, 2026 |
| 4.0 | Knowledge Base Refresh & Project Reindex | ✅ DONE | Juli 17, 2026 |

---

## Pending Sprints (Post-Demo)

| Sprint | Judul | Priority |
|---|---|---|
| 4.1 | Wire program name ke live API (TD-001) | 🔴 HIGH |
| 4.2 | Stream URL fallback (TD-002) | 🔴 HIGH |
| 4.3 | Superuser creation + verify login (Task #2) | 🔴 CRITICAL |
| 4.4 | Real radio stream integration (Task #4) | 🟡 HIGH |
| 4.5 | Analytics dashboard (real data) | 🟡 MEDIUM |
| 4.6 | Automated tests for LiveRadioAPIView (TD-003) | 🟡 MEDIUM |
| 4.7 | Apply pending platform migrations (TD-006) | 🟡 MEDIUM |
| 4.8 | Studio service extraction (inline queries di dashboard view) | ⚪ LOW |
| 4.9 | WebSocket/SSE for real-time updates | ⚪ LOW (post-demo) |

---

## Known Issues

| ID | Issue | Impact | Sprint |
|---|---|---|---|
| TD-001 | `program` field selalu null di live API | HIGH — terlihat di demo | 4.1 |
| TD-002 | Tidak ada fallback stream URL | HIGH — silent play failure | 4.2 |
| TD-003 | Tidak ada automated tests untuk LiveRadioAPIView | MEDIUM | 4.6 |
| TD-004 | BroadcastindoAdapter buat 2 HTTP call per cache miss | LOW | — |
| TD-006 | Unapplied migrations di apps/platform | MEDIUM | 4.7 |
| TD-007 | Belum ada superuser account di dev | CRITICAL (Task #2) | 4.3 |
| — | `templates/dashboard/home.html` masih extend dashboard_base.html | LOW | — |
| — | `templates/core/home.html` masih extend dashboard_base.html | LOW | — |
| — | `AMPStudioDashboardView` punya inline ORM queries | LOW | 4.8 |
| — | `sponsor.Partner` vs `platform.Partner` — nama model sama di 2 app | MEDIUM | — |
| — | `news.Tag` vs `media_manager.Tag` vs `content.ContentTag` — 3 tag models | MEDIUM | — |

---

## Technical Debt

Semua TD terdokumentasi di `docs/architecture/TECH_DEBT.md`.

**Prinsip:** Jangan sembunyikan masalah — dokumentasikan agar bisa direncanakan.

---

## DO NOT

1. **Jangan edit business logic** tanpa task yang di-approve
2. **Jangan refactor** tanpa explicit instruction
3. **Jangan buat fitur baru** tanpa sprint planning
4. **Jangan hardcode** warna, URL, atau credential
5. **Jangan duplicate** base template — satu base, `amp_studio/base.html`
6. **Jangan hapus** dokumentasi — tandai DEPRECATED
7. **Jangan commit** secret/credential ke repository
8. **Jangan gunakan** field names yang salah di `StreamHealth` — lihat tabel di atas
9. **Jangan polling** lebih cepat dari cache TTL (20s) — waste upstream bandwidth
10. **Jangan assume** — cek dokumentasi dulu sebelum implement

---

## Best Practices

1. **Baca dulu:** AI_CONTEXT.md → roadmap → changelog sprint terakhir
2. **Cek tech debt register** sebelum mulai sprint
3. **Demo seed dulu** sebelum screenshot atau test live
4. **Test di authenticated session** — hampir semua view butuh login
5. **Restart workflow** setelah code change, cek logs sebelum screenshot
6. **Commit ke GitHub** setelah setiap sprint selesai (GitHub PAT tersedia via secret)
7. **Management commands** untuk init: `init_settings` → `seed_platform` → `demo_seed`
8. **Login demo:** `admin` / `admin1234` (jika sudah dibuat via `create_superadmin`)

---

## Template Warisan (Legacy)

File-file berikut masih menggunakan layout lama dan **belum dimigrasikan**:
- `templates/dashboard/home.html` — extend `dashboard_base.html`
- `templates/core/home.html` — extend `dashboard_base.html`

Semua file lain sudah dimigrasikan ke `amp_studio/base.html`.

---

## Credential Dev (non-secret)

- **Login dev:** username `admin`, password `admin1234` (via `create_superadmin` atau `reset_admin`)
- **Demo seed:** `python manage.py demo_seed --reset`
- **Port dev:** 5000

---

*Dokumen ini diperbarui setiap sprint. Source of truth adalah kode aktual.*
*Jika ada konflik antara dokumen ini dan kode, percayai kode.*
