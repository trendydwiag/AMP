# Sprint 3.6 — Platform UI Consistency & Navigation Hardening

**Tanggal:** 17 Juli 2026  
**Tipe:** Quality Assurance — tidak ada perubahan business logic

---

## Halaman yang Diaudit

| Route | Template | Status |
|---|---|---|
| `/studio/` | `amp_studio/dashboard.html` | ✅ Konsisten |
| `/studio/streaming/` | `amp_studio/streaming_center.html` | ✅ Konsisten |
| `/studio/setup/` | `amp_studio/setup_wizard.html` | ✅ Konsisten |
| `/studio/kalender/` | `amp_studio/calendar.html` | ✅ Konsisten |
| `/studio/media/` | `amp_studio/media_explorer.html` | ✅ Konsisten |
| `/studio/analytics/` | `amp_studio/analytics.html` | ✅ Konsisten |
| `/studio/preview/<type>/<pk>/` | `amp_studio/preview.html` | ✅ Konsisten |
| `/studio/komunitas/` | `amp_studio/community.html` | ✅ **Baru dibuat** |
| `/studio/iklan/` | `amp_studio/iklan.html` | ✅ **Baru dibuat** |

---

## Task 1 & 2 — Audit Layout & Base Layout Tunggal

**Hasil:** Semua halaman Studio sudah menggunakan `amp_studio/base.html` sebagai satu-satunya base layout.  
Tidak ditemukan penggunaan `dashboard.html` (sebagai layout), `legacy_admin.html`, atau `old_layout.html`.  
Tidak ada perubahan diperlukan.

---

## Task 3 — Konsistensi Sidebar

**Diperbaiki:**
- Submenu **Siaran** kini otomatis terbuka ketika user berada di halaman `broadcast` app.
- Submenu **Konten** otomatis terbuka di halaman `news` atau `content` app.
- Submenu **Podcast** otomatis terbuka di halaman `podcast` app.
- Submenu **Media** otomatis terbuka di halaman `media_manager` app.
- Submenu **Pengaturan** otomatis terbuka di halaman `settings` app.
- Semua item submenu mendapat class `active` berdasarkan `request.resolver_match.url_name`.

---

## Task 4 — Tombol Beranda

**Hasil:** "Beranda" di sidebar sudah mengarah ke `/studio/` — tidak ada perubahan diperlukan.

---

## Task 5 — Header Konsisten

**Hasil:** Semua halaman menggunakan satu komponen header via `{% include 'amp_studio/components/header.html' %}` — tidak ada perubahan diperlukan.

---

## Task 6 — Breadcrumb

**Ditambahkan** ke `amp_studio/base.html`: block `{% block breadcrumb %}` di antara header dan main content.

**Breadcrumb ditambahkan ke semua halaman:**
- `dashboard.html` → Studio / Beranda
- `streaming_center.html` → Studio / Streaming Center
- `analytics.html` → Studio / Analytics
- `calendar.html` → Studio / Kalender Siaran
- `media_explorer.html` → Studio / Media Explorer
- `setup_wizard.html` → Studio / Setup Wizard
- `preview.html` → Studio / Pratinjau Konten
- `community.html` → Studio / Komunitas
- `iklan.html` → Studio / Iklan

**CSS breadcrumb** ditambahkan ke `static/css/amp-studio/amp-studio.css`.

---

## Task 7 — Audit Semua Menu

**Route mati yang diperbaiki:**

| Menu | Sebelum | Sesudah |
|---|---|---|
| Komunitas | `href="#"` (dead link) | `{% url 'studio:community' %}` |
| Iklan | `href="#"` (dead link) | `{% url 'studio:iklan' %}` |

**Route baru ditambahkan:**
- `path('komunitas/', CommunityView, name='community')` → `apps/studio/urls.py`
- `path('iklan/', IklanView, name='iklan')` → `apps/studio/urls.py`

**View baru ditambahkan:**
- `CommunityView` — menampilkan data diskusi dari `apps.community.models`
- `IklanView` — menampilkan data sponsor dari `apps.sponsor.models`

**Semua URL lain tervalidasi:** 32 URL di sidebar dan header dikonfirmasi resolve dengan `reverse()`.

---

## Task 8 — Komentar Developer

**Hasil:** Seluruh komentar template menggunakan sintaks Django `{# #}` yang **tidak dirender** ke HTML browser. Tidak ada komentar internal yang bocor ke UI pengguna. Tidak ada perubahan diperlukan.

---

## Task 9 — Asset Pipeline

**Hasil:** Semua asset (Tailwind CDN, Alpine.js core + Collapse plugin, HTMX, AMP Studio CSS + JS) di-load melalui `amp_studio/base.html` secara konsisten. Tidak ada halaman yang load asset berbeda.

---

## Task 10 — Komponen Konsisten

**Hasil:** Semua halaman menggunakan class `.amp-card`, `.amp-btn`, `.amp-page-title`, `.amp-page-subtitle`, `.amp-badge`, `.amp-nav-item` dari design system yang sama.

---

## Task 11 — Responsive Audit

**Hasil:** Sidebar collapse dikontrol oleh `sidebarCollapsed` Alpine state. Mobile toggle dikontrol oleh `sidebarMobileOpen`. Semua halaman mewarisi behavior ini dari base layout.

---

## Task 12 — Route Validation

**Semua route divalidasi:**

| App | URL Prefix | Status |
|---|---|---|
| `studio` | `/studio/` | ✅ 9 routes aktif |
| `broadcast` | `/broadcast/` | ✅ Semua submenu resolve |
| `news` | `/berita/` | ✅ Resolve |
| `content` | `/konten/` | ✅ Resolve |
| `podcast` | `/podcast/` | ✅ Resolve |
| `media_manager` | `/media/` | ✅ Resolve |
| `radio` | `/radio/` | ✅ Resolve |
| `platform` | `/platform/` | ✅ Resolve |
| `settings` | `/pengaturan/` | ✅ Resolve |
| `users` | `/akun/` | ✅ Resolve |

---

## Task 13 — Functional Validation

- Semua halaman dilindungi `@login_required` via `method_decorator`.
- Partner switcher dibatasi untuk role `SUPERUSER` dan `ADMINISTRATOR`.
- Menu Partner di sidebar hanya muncul untuk role tersebut.

---

## Task 14 — Dummy Data Validation

- **community.html**: Menampilkan data riil dari `Discussion` dan `Reply` model (atau empty state yang informatif).
- **iklan.html**: Menampilkan data riil dari `Sponsor` dan `Advertisement` model.
- Semua halaman lain menampilkan data dari demo seed.

---

## Task 15 — Changelog

File ini: `docs/changelog/sprint-3.6.md`

---

## Bug yang Ditemukan & Diperbaiki

| Bug | Lokasi | Perbaikan |
|---|---|---|
| Komunitas link mati (`href="#"`) | `sidebar.html` | Route baru `studio:community` |
| Iklan link mati (`href="#"`) | `sidebar.html` | Route baru `studio:iklan` |
| Submenu tidak auto-open pada halaman aktif | `sidebar.html` | Alpine `open` state di-init dari `request.resolver_match.app_name` |
| Tidak ada breadcrumb di manapun | Semua template | Block `breadcrumb` ditambahkan ke `base.html` dan semua template |

---

## File yang Diubah

- `apps/studio/urls.py` — +2 routes
- `apps/studio/views.py` — +2 views (`CommunityView`, `IklanView`)
- `templates/amp_studio/base.html` — tambah `{% block breadcrumb %}`
- `templates/amp_studio/components/sidebar.html` — auto-open submenus, active states, fix dead links
- `templates/amp_studio/dashboard.html` — tambah breadcrumb
- `templates/amp_studio/streaming_center.html` — tambah breadcrumb
- `templates/amp_studio/analytics.html` — tambah breadcrumb
- `templates/amp_studio/calendar.html` — tambah breadcrumb
- `templates/amp_studio/media_explorer.html` — tambah breadcrumb
- `templates/amp_studio/setup_wizard.html` — tambah breadcrumb
- `templates/amp_studio/preview.html` — tambah breadcrumb
- `templates/amp_studio/community.html` — **file baru**
- `templates/amp_studio/iklan.html` — **file baru**
- `static/css/amp-studio/amp-studio.css` — tambah `.amp-breadcrumb` styles
- `docs/changelog/sprint-3.6.md` — **file baru** (ini)

---

## Definition of Done — Checklist

- [x] Tidak ada halaman dengan layout berbeda — semua extend `amp_studio/base.html`
- [x] Tidak ada menu yang mati — Komunitas dan Iklan sudah punya route
- [x] Tidak ada komentar developer tampil di UI — semua `{# #}` tidak dirender
- [x] Semua halaman memakai base layout yang sama
- [x] Semua menu mengarah ke tujuan yang benar — 32 URL tervalidasi
- [x] Seluruh dashboard terasa seperti satu produk profesional
- [x] Tidak ada perubahan business logic — hanya UI/UX, konsistensi, stabilitas
