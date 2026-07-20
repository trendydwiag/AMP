# Production Audit Report — Sprint 4.4.1B

**Tanggal Audit:** 20 Juli 2026
**Auditor:** QA Agent (Replit)
**Aplikasi:** AMP Studio / Radio Kabulhaden CMS
**Metode:** Template static analysis + live HTTP status checks + screenshot + browser console log review

---

## Executive Summary

| Metrik | Sebelum Fix | Sesudah Fix |
|---|---|---|
| Total URL diaudit | 67 | 67 |
| PASS | 59 | 64 |
| WARNING | 3 | 3 |
| FAIL | 5 | 0 |
| Dead code dihapus | 2 file | — |
| **Production Readiness** | **88.1%** | **95.5%** |

> Formula: `PASS / (PASS + WARNING + FAIL) × 100`

---

## Inventory Lengkap

### A. Public Website

| # | URL | Template | View | Permission | Sidebar | Breadcrumb | Dark Mode | Empty State | Responsive | Console Error | Status |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | `/` | website/home.html | HomeView | Public | N/A | N/A | ✓ | ✓ | ✓ | CDN⚠ | **PASS** |
| 2 | `/tentang/` | website/about.html | AboutView | Public | N/A | N/A | ✓ | N/A | ✓ | CDN⚠ | **PASS** |
| 3 | `/program/` | website/program_list.html | ProgramListView | Public | N/A | ✓ | ✓ | ✓ | ✓ | ~~Alpine Error~~ | **PASS** *(fixed)* |
| 4 | `/program/<slug>/` | website/program_detail.html | ProgramDetailView | Public | N/A | N/A | ✓ | N/A | ✓ | CDN⚠ | **PASS** |
| 5 | `/jadwal/` | website/schedule.html | ScheduleView | Public | N/A | N/A | ✓ | ✓ | ✓ | CDN⚠ | **PASS** |
| 6 | `/podcast/` | website/podcast_list.html | PodcastListView | Public | N/A | ✓ | ✓ | ✓ | ✓ | CDN⚠ | **PASS** |
| 7 | `/podcast/<slug>/` | website/podcast_detail.html | PodcastDetailView | Public | N/A | N/A | ✓ | N/A | ✓ | CDN⚠ | **PASS** |
| 8 | `/podcast/episode/<uuid>/` | website/podcast_episode.html | PodcastEpisodeView | Public | N/A | N/A | ✓ | N/A | ✓ | CDN⚠ | **PASS** |
| 9 | `/berita/` | website/news_list.html | NewsListView | Public | N/A | ✓ | ✓ | ✓ | ✓ | CDN⚠ | **PASS** |
| 10 | `/berita/<slug>/` | website/article_detail.html | ArticleDetailView | Public | N/A | ✓ | ✓ | N/A | ✓ | CDN⚠ | **PASS** |
| 11 | `/komunitas/` | website/community.html | CommunityView | Public | N/A | N/A | ✓ | ✓ | ✓ | CDN⚠ | **PASS** |
| 12 | `/komunitas/<slug>/` | website/community_discussion.html | DiscussionView | Public | N/A | N/A | ✓ | N/A | ✓ | CDN⚠ | **PASS** |
| 13 | `/mitra/` | website/partner_list.html | PartnerListView | Public | N/A | N/A | ✓ | ✓ | ✓ | CDN⚠ | **PASS** |
| 14 | `/sponsor/` | website/sponsor_list.html | SponsorListView | Public | N/A | N/A | ✓ | ✓ | ✓ | CDN⚠ | **PASS** |
| 15 | `/kontak/` | website/contact.html | ContactView | Public | N/A | N/A | ✓ | N/A | ✓ | CDN⚠ | **PASS** |
| 16 | `/kebijakan-privasi/` | website/privacy.html | PrivacyView | Public | N/A | N/A | ✓ | N/A | ✓ | CDN⚠ | **PASS** |
| 17 | `/syarat-ketentuan/` | website/terms.html | TermsView | Public | N/A | N/A | ✓ | N/A | ✓ | CDN⚠ | **PASS** |
| 18 | `/pencarian/` | website/search.html | SearchView | Public | N/A | N/A | ✓ | ✓ | ✓ | CDN⚠ | **PASS** |
| 19 | `/pemeliharaan/` | website/maintenance.html | MaintenanceView | Public | N/A | N/A | ✓ | N/A | ✓ | CDN⚠ | **PASS** |
| 20 | `/radio-live/` | website/radio_live.html | RadioLiveView | Public | N/A | N/A | ✓ | N/A | ✓ | CDN⚠ | **PASS** |

### B. Auth

| # | URL | Template | View | Permission | Sidebar | Breadcrumb | Dark Mode | Empty State | Responsive | Console Error | Status |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 21 | `/akun/masuk/` | users/login.html | LoginView | Public | N/A | N/A | N/A | N/A | ✓ | CDN⚠ | **PASS** |
| 22 | `/akun/daftar/` | users/register.html | RegisterView | Public | N/A | N/A | N/A | N/A | ✓ | CDN⚠ | **PASS** |

### C. AMP Studio

| # | URL | Template | View | Permission | Sidebar | Breadcrumb | Dark Mode | Empty State | Responsive | Console Error | Status |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 23 | `/studio/` | amp_studio/dashboard.html | StudioDashboardView | Login | ✓ | ✓ | PARTIAL | ✓ | ✓ | CDN⚠ | **PASS** |
| 24 | `/studio/kalender/` | amp_studio/calendar.html | CalendarView | Login | ✓ | ✓ | PARTIAL | ✗ | ✓ | CDN⚠ | **WARNING** |
| 25 | `/studio/media/` | amp_studio/media_explorer.html | MediaExplorerView | Login | ✓ | ✓ | PARTIAL | ✗ | ✓ | CDN⚠ | **WARNING** |
| 26 | `/studio/analytics/` | amp_studio/analytics.html | AnalyticsView | Login | ✓ | ✓ | PARTIAL | ✗ | ✓ | CDN⚠ | **WARNING** |
| 27 | `/studio/streaming/` | amp_studio/streaming_center.html | StreamingCenterView | Login | ✓ | ✓ | PARTIAL | ✓ | ✓ | CDN⚠ | **PASS** |
| 28 | `/studio/setup/` | amp_studio/setup_wizard.html | SetupWizardView | Login | ✓ | ✓ | PARTIAL | ✓ | ✓ | CDN⚠ | **PASS** |
| 29 | `/studio/komunitas/` | amp_studio/community.html | CommunityView | Login | ✓ | ✓ | PARTIAL | ✓ | ✓ | ~~500 FieldError~~ | **PASS** *(fixed)* |
| 30 | `/studio/iklan/` | amp_studio/iklan.html | IklanView | Login | ✓ | ✓ | PARTIAL | ✓ | ✓ | CDN⚠ | **PASS** |

### D. Radio

| # | URL | Template | View | Permission | Sidebar | Breadcrumb | Dark Mode | Empty State | Responsive | Console Error | Status |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 31 | `/radio/` | radio/dashboard.html | RadioDashboardView | Admin | ✓ | ✓ | ✓ | ✓ | ✓ | CDN⚠ | **PASS** |
| 32 | `/radio/station/` | radio/station_list.html | RadioStationListView | Admin | ~~✗~~ ✓ | ✓ | ✓ | ✓ | ✓ | CDN⚠ | **PASS** *(fixed)* |
| 33 | `/radio/station/buat/` | radio/station_form.html | RadioStationCreateView | Admin | ~~✗~~ ✓ | ✓ | ✓ | N/A | ✓ | CDN⚠ | **PASS** *(fixed)* |
| 34 | `/radio/provider/` | radio/provider_list.html | RadioProviderListView | Admin | ~~✗~~ ✓ | ✓ | ✓ | ✓ | ✓ | CDN⚠ | **PASS** *(fixed)* |
| 35 | `/radio/analytics/` | radio/analytics.html | RadioAnalyticsView | Admin | ✓ | ✓ | ✓ | ✓ | ✓ | CDN⚠ | **PASS** |

### E. Broadcast

| # | URL | Template | View | Permission | Sidebar | Breadcrumb | Dark Mode | Empty State | Responsive | Console Error | Status |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 36 | `/broadcast/` | broadcast/dashboard.html | BroadcastDashboardView | Admin | ✓ | ✓ | ✓ | ✓ | ✓ | CDN⚠ | **PASS** |
| 37 | `/broadcast/program/` | broadcast/program_list.html | ProgramListView | Admin | ✓ | ✓ | ✓ | ✓ | ✓ | CDN⚠ | **PASS** |
| 38 | `/broadcast/host/` | broadcast/host_list.html | HostListView | Admin | ✓ | ✓ | ✓ | ✓ | ✓ | CDN⚠ | **PASS** |
| 39 | `/broadcast/jadwal/` | broadcast/schedule_list.html | ScheduleListView | Admin | ✓ | ✓ | ✓ | ✓ | ✓ | CDN⚠ | **PASS** |
| 40 | `/broadcast/sesi/` | broadcast/session_list.html | SessionListView | Admin | ✓ | ✓ | ✓ | ✓ | ✓ | CDN⚠ | **PASS** |
| 41 | `/broadcast/episode/` | broadcast/episode_list.html | EpisodeListView | Admin | ✓ | ✓ | ✓ | ✓ | ✓ | CDN⚠ | **PASS** |
| 42 | `/broadcast/pengumuman/` | broadcast/announcement_list.html | AnnouncementListView | Admin | ✓ | ✓ | ✓ | ✓ | ✓ | CDN⚠ | **PASS** |
| 43 | `/broadcast/kalender/` | broadcast/calendar.html | CalendarView | Admin | ✓ | ✓ | ✓ | ✓ | ✓ | CDN⚠ | **PASS** |
| 44 | `/broadcast/cms/program/` | broadcast/cms/program_list.html | CMSProgramListView | Admin | ✓ | ✓ | ✓ | ✓ | ✓ | CDN⚠ | **PASS** |
| 45 | `/broadcast/cms/episode/` | broadcast/cms/episode_list.html | CMSEpisodeListView | Admin | ✓ | ✓ | ✓ | ✓ | ✓ | CDN⚠ | **PASS** |

### F. Media Manager

| # | URL | Template | View | Permission | Sidebar | Breadcrumb | Dark Mode | Empty State | Responsive | Console Error | Status |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 46 | `/media/` | media_manager/dashboard.html | MediaDashboardView | Admin | ✓ | ✓ | ✓ | ✓ | ✓ | CDN⚠ | **PASS** |
| 47 | `/media/file/` | media_manager/list.html | MediaListView | Admin | ✓ | ✓ | ✓ | ✓ | ✓ | CDN⚠ | **PASS** |
| 48 | `/media/folder/` | media_manager/folders.html | FoldersView | Admin | ✓ | ✓ | ✓ | ✓ | ✓ | CDN⚠ | **PASS** |
| 49 | `/media/tag/` | media_manager/tags.html | TagsView | Admin | ✓ | ✓ | ✓ | ✓ | ✓ | CDN⚠ | **PASS** |
| 50 | `/media/inspector/` | media_manager/inspector.html | InspectorView | Admin | ✓ | ✓ | ✓ | N/A | ✓ | CDN⚠ | **PASS** |

### G. Pengaturan

> **Catatan URL:** `settings:site` → `/pengaturan/` (bukan `/pengaturan/site/`); `settings:appearance` → `/pengaturan/tampilan/` (bukan `/pengaturan/appearance/`). Kedua URL yang benar mengembalikan HTTP 200.

| # | URL | Template | View | Permission | Sidebar | Breadcrumb | Dark Mode | Empty State | Responsive | Console Error | Status |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 51 | `/pengaturan/` | settings/site.html | SiteSettingsView | Admin | ✓ | ✓ | ✓ | N/A | ✓ | CDN⚠ | **PASS** |
| 52 | `/pengaturan/seo/` | settings/seo.html | SeoSettingsView | Admin | ✓ | ✓ | ✓ | N/A | ✓ | CDN⚠ | **PASS** |
| 53 | `/pengaturan/tampilan/` | settings/appearance.html | AppearanceSettingsView | Admin | ✓ | ✓ | ✓ | N/A | ✓ | CDN⚠ | **PASS** |
| 54 | `/pengaturan/email/` | settings/email.html | EmailSettingsView | Admin | ✓ | ✓ | ✓ | N/A | ✓ | CDN⚠ | **PASS** |
| 55 | `/pengaturan/keamanan/` | settings/security.html | SecuritySettingsView | Admin | ✓ | ✓ | ✓ | N/A | ✓ | CDN⚠ | **PASS** |

### H. Platform

| # | URL | Template | View | Permission | Sidebar | Breadcrumb | Dark Mode | Empty State | Responsive | Console Error | Status |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 56 | `/platform/` | platform/dashboard.html | PlatformDashboardView | Admin | ✓ | ✓ | ✓ | ✓ | ✓ | CDN⚠ | **PASS** |
| 57 | `/platform/partners/` | platform/partner_list.html | PartnerListView | Admin | ✓ | ✓ | ✓ | ✓ | ✓ | CDN⚠ | **PASS** |
| 58 | `/platform/providers/` | platform/provider_list.html | ProviderListView | Admin | ✓ | ✓ | ✓ | ✓ | ✓ | CDN⚠ | **PASS** |

### I. Manajemen Konten

| # | URL | Template | View | Permission | Sidebar | Breadcrumb | Dark Mode | Empty State | Responsive | Console Error | Status |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 59 | `/konten/` | content/dashboard.html | ContentDashboardView | Admin | ✓ | ✓ | ✓ | ✓ | ✓ | CDN⚠ | **PASS** |
| 60 | `/konten/categories/` | content/category_list.html | CategoryListView | Admin | ✓ | ✓ | ✓ | ✓ | ✓ | CDN⚠ | **PASS** |
| 61 | `/konten/tags/` | content/tag_list.html | TagListView | Admin | ✓ | ✓ | ✓ | ✓ | ✓ | CDN⚠ | **PASS** |
| 62 | `/konten/authors/` | content/author_list.html | AuthorListView | Admin | ✓ | ✓ | ✓ | ✓ | ✓ | CDN⚠ | **PASS** |

### J. Podcast CMS

| # | URL | Template | View | Permission | Sidebar | Breadcrumb | Dark Mode | Empty State | Responsive | Console Error | Status |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 63 | `/podcast/cms/podcast/` | podcast/cms/podcast_list.html | PodcastCMSListView | Admin | ✓ | ✓ | ✓ | ✓ | ✓ | CDN⚠ | **PASS** |
| 64 | `/podcast/cms/episode/` | podcast/cms/episode_list.html | EpisodeCMSListView | Admin | ✓ | ✓ | ✓ | ✓ | ✓ | CDN⚠ | **PASS** |

### K. Berita CMS

| # | URL | Template | View | Permission | Sidebar | Breadcrumb | Dark Mode | Empty State | Responsive | Console Error | Status |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 65 | `/berita/cms/artikel/` | news/cms/article_list.html | ArticleCMSListView | Admin | ✓ | ✓ | ✓ | ✓ | ✓ | CDN⚠ | **PASS** |

### L. Akun / Pengguna

| # | URL | Template | View | Permission | Sidebar | Breadcrumb | Dark Mode | Empty State | Responsive | Console Error | Status |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 66 | `/akun/admin/pengguna/` | users/admin/user_list.html | AdminUserListView | Admin | ✓ | ✓ | ✓ | N/A | ✓ | CDN⚠ | **PASS** |
| 67 | `/akun/profil/` | users/profile.html | ProfileView | Login | ✓ | ✓ | ✓ | N/A | ✓ | CDN⚠ | **PASS** |

---

## Bug yang Diperbaiki (5 FAIL → 0)

### BUG-001 — `/studio/komunitas/` HTTP 500
- **Severity:** CRITICAL
- **Root Cause:** `CommunityView.get_context_data()` memanggil `Discussion.objects.select_related('author')`. Model `Discussion` tidak memiliki FK `author` — hanya `author_name` dan `author_email` (CharField). Queryset bersifat lazy; exception (`FieldError`) tidak dilempar saat `select_related()` dipanggil, melainkan saat Django mengevaluasi queryset di template — di luar blok `try/except`.
- **Fix:** Hapus `select_related('author')` dan wrap queryset dengan `list()` untuk memaksa evaluasi di dalam `try` block.
- **File:** `apps/studio/views.py` (CommunityView.get_context_data)

### BUG-002 — `/program/` Alpine.js Expression Error
- **Severity:** MEDIUM
- **Root Cause:** `x-effect` attribute di `program_list.html` line 78-80 berisi JS expression dengan escaped double-quotes di dalam HTML attribute value: `document.querySelectorAll('[x-show*=\"activeCategory\"]')`. Alpine.js tidak bisa parse escaped quotes di dalam attribute string → `Invalid or unexpected token` di console. Div ini juga merupakan dead code (count dihitung tapi tidak digunakan).
- **Fix:** Hapus div dead code tersebut seluruhnya.
- **File:** `templates/website/program_list.html`

### BUG-003 — Radio Sidebar Active State Tidak Berfungsi di Sub-pages
- **Severity:** LOW
- **Root Cause:** Sidebar Radio link menggunakan kondisi `app_name == 'radio' AND url_name == 'dashboard'`. Saat user navigasi ke `/radio/station/`, `/radio/station/buat/`, atau `/radio/provider/`, tidak ada item sidebar yang di-highlight, membuat user kehilangan navigasi context.
- **Fix:** Ganti kondisi menjadi `app_name == 'radio'` (tanpa syarat `url_name`).
- **File:** `templates/amp_studio/components/sidebar.html`

### BUG-004 & BUG-005 — Orphaned Template Files dengan Alpine Pattern Lama
- **Severity:** LOW
- **Root Cause:** `templates/radio/sticky_player.html` dan `templates/radio/player.html` menggunakan `x-data="stickyRadioPlayer()"` dan `x-data="radioPlayer()"` — pola lama yang bertentangan dengan `Alpine.store('radio')`. Kedua file tidak pernah di-include oleh template mana pun (dead code). Player aktif yang sebenarnya ada di `templates/website/components/sticky_player.html` yang sudah menggunakan `Alpine.store('radio')` dengan benar.
- **Fix:** Hapus kedua file.
- **Files dihapus:** `templates/radio/sticky_player.html`, `templates/radio/player.html`

---

## Bug yang Belum Diperbaiki (WARNING)

### WARN-001 — Missing Empty State: Studio Calendar, Media Explorer, Analytics
- **Halaman:** `/studio/kalender/`, `/studio/media/`, `/studio/analytics/`
- **Detail:** Template tidak memiliki fallback UI ketika data kosong (tidak ada event di kalender, tidak ada media di explorer, tidak ada data analytics). Halaman tampak kosong atau menampilkan section header tanpa konten.
- **Severity:** LOW (visual/UX issue, tidak crash)
- **Rekomendasi:** Tambahkan empty state component mengikuti pola yang sudah ada di template lain (`amp-empty` class atau `{% empty %}` block).

### WARN-002 — Tailwind CSS CDN di Production
- **Detail:** Semua halaman menggunakan CDN Tailwind (`cdn.tailwindcss.com`) yang menampilkan warning di browser console pada setiap page load. CDN Tailwind tidak boleh digunakan di production.
- **Severity:** LOW (tidak crash, tapi CDN lambat dan tidak optimal untuk production)
- **Rekomendasi:** Setup Tailwind build pipeline (PostCSS/CLI). Ini adalah perubahan infrastruktur yang lebih besar.
- **Tech Debt:** TD-010

### WARN-003 — AMP Studio Dark Mode Partial
- **Detail:** Semua template AMP Studio menggunakan CSS variables yang mendukung theming, tapi `amp_studio/base.html` memiliki `data-theme="light"` hardcoded tanpa mechanism toggle yang persistent. Dark mode tidak disimpan ke localStorage/cookie.
- **Severity:** LOW (dark mode toggle ada tapi tidak persistent antar session)
- **Tech Debt:** sudah terdokumentasi di `docs/architecture/TECH_DEBT.md`

---

## Technical Debt Baru Ditemukan

| ID | Deskripsi | Severity | File |
|---|---|---|---|
| TD-009 | `broadcast/services.py:454` — `now.replace(tzinfo=None)` tidak perlu; strip timezone info lalu arithmetika dengan naive datetime lain, berfungsi tapi semantically confusing | LOW | `apps/broadcast/services.py` |
| TD-010 | Tailwind CSS CDN digunakan di semua template — harus diganti dengan proper build pipeline untuk production | MEDIUM | `templates/*/base.html` |

---

## Statistik Final

```
Total URL diaudit:     67
PASS (setelah fix):    64  (95.5%)
WARNING (unfixed):      3  ( 4.5%)
FAIL (setelah fix):     0  ( 0.0%)

Dead code dihapus:      2 file (templates/radio/sticky_player.html, templates/radio/player.html)

Bug diperbaiki:         5
  - BUG-001: /studio/komunitas/ HTTP 500 FieldError
  - BUG-002: /program/ Alpine expression error
  - BUG-003: Radio sidebar active state
  - BUG-004: templates/radio/sticky_player.html (deleted)
  - BUG-005: templates/radio/player.html (deleted)

Bug belum diperbaiki:   3 (semua WARNING, tidak FAIL)
  - WARN-001: Missing empty state di 3 Studio pages
  - WARN-002: Tailwind CDN (infrastructure change diperlukan)
  - WARN-003: Dark mode tidak persistent

Production Readiness:  95.5%
```

---

## Catatan Metodologi

- **HTTP status codes** diverifikasi via curl dengan session cookie (login sebagai `superadmin`)
- **Template analysis** dilakukan via static code analysis (grep + subagent exploration)
- **Console errors** diverifikasi via Replit browser console log capture
- **Sidebar active state** diverifikasi via review `sidebar.html` Django conditional expressions
- **Breadcrumb** diverifikasi via grep `{% block breadcrumb %}` di semua template
- **Dark mode** diverifikasi via grep `dark:` Tailwind classes di template
- **Empty state** diverifikasi via grep `{% empty %}`, `amp-empty`, `belum ada` di template

---

*Dihasilkan: Sprint 4.4.1B — 20 Juli 2026*
