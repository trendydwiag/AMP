# Sprint 4.1 — Demo Readiness & Founder Experience

**Tanggal:** 17 Juli 2026  
**Target demo:** Radio Kabulhaden, 21 Juli 2026  
**Fokus:** UI/UX polish — audit seluruh halaman CMS, hapus placeholder/Coming Soon, perbaiki empty states, konsistensi AMP Studio design system.

---

## Ruang Lingkup

Tidak ada perubahan business logic, schema database, migrasi, atau refaktor arsitektur. Semua perubahan bersifat presentasi (HTML/CSS/template).

---

## Halaman yang Diaudit

| Halaman | Template | Status Sebelum | Tindakan |
|---|---|---|---|
| Komunitas | `amp_studio/community.html` | "Segera Hadir" badge di header + Coming Soon banner | ✅ Diperbaiki |
| Iklan | `amp_studio/iklan.html` | "Segera Hadir" badge di header + Coming Soon banner | ✅ Diperbaiki |
| Platform Dashboard | `platform/dashboard.html` | Tanpa dark mode, tanpa breadcrumb, `bg-white` lama | ✅ Diperbaiki |
| Partner List | `platform/partner_list.html` | Tanpa dark mode, tanpa breadcrumb, empty state minimal | ✅ Diperbaiki |
| Provider List | `platform/provider_list.html` | Tanpa dark mode, tanpa breadcrumb, tanpa empty state | ✅ Diperbaiki |
| Media Dashboard | `media_manager/dashboard.html` | Card style lama (`bg-white shadow rounded-lg`) | ✅ Diperbaiki |
| Media List | `media_manager/list.html` | Card style lama, empty state minimal | ✅ Diperbaiki |
| Media Upload | `media_manager/upload.html` | Card style lama | ✅ Diperbaiki |
| Media Detail | `media_manager/detail.html` | Card style lama | ✅ Diperbaiki |
| Media Folders | `media_manager/folders.html` | Card style lama, empty state minimal | ✅ Diperbaiki |
| Media Tags | `media_manager/tags.html` | Card style lama, empty state minimal | ✅ Diperbaiki |
| Media Delete Confirm | `media_manager/delete_confirm.html` | Card style lama | ✅ Diperbaiki |
| Program Siaran List | `broadcast/cms/program_list.html` | Empty state tanpa CTA button | ✅ Diperbaiki |
| Episode Siaran List | `broadcast/cms/episode_list.html` | Empty state satu baris teks saja | ✅ Diperbaiki |
| Podcast List | `podcast/cms/podcast_list.html` | Empty state tanpa CTA button | ✅ Diperbaiki |
| Podcast Episode List | `podcast/cms/episode_list.html` | Empty state satu baris teks saja | ✅ Diperbaiki |
| Artikel List | `news/cms/article_list.html` | Empty state tanpa CTA button | ✅ Diperbaiki |
| Content Dashboard | `content/dashboard.html` | Sudah baik — tanpa perubahan | ✔ OK |
| Broadcast Program Form | `broadcast/cms/program_form.html` | Sudah baik | ✔ OK |
| Broadcast Program List | `broadcast/cms/program_list.html` | Breadcrumb & dark mode OK | ✔ OK |
| News Article Detail | `news/cms/article_detail.html` | Breadcrumb & dark mode OK | ✔ OK |
| Podcast Form | `podcast/cms/podcast_form.html` | Sudah baik | ✔ OK |
| Media Inspector | `media_manager/inspector.html` | Dibuat Sprint 4.2, sudah amp-card | ✔ OK |

---

## Perubahan per Kategori

### 1. Hapus "Segera Hadir" / Coming Soon

**`templates/amp_studio/community.html`**
- Dihapus: badge `Segera Hadir` di header
- Diganti: tombol aksi "Undang Pendengar" yang bersih
- Dihapus: banner "Modul Komunitas — Segera Hadir" di bawah
- Diganti: card "Fitur yang Sedang Dikembangkan" dengan grid 4 item roadmap (Forum Diskusi, Komentar Episode, Request Lagu, Voting & Poll) — tanpa label Coming Soon, tanpa badge

**`templates/amp_studio/iklan.html`**
- Sama dengan pola di atas: badge dihapus, banner diganti grid roadmap (Slot Iklan, Jadwal Otomatis, Laporan Performa, Integrasi Pembayaran)

### 2. Platform Templates — Dark Mode + Breadcrumb + AMP Studio Style

**`templates/platform/dashboard.html`**
- Tambah: `{% block breadcrumb %}` dengan jalur Studio › Platform
- Ganti: `bg-white rounded-xl border border-coffee-200` → `amp-card`
- Tambah: dark mode classes di semua elemen teks
- Tambah: stat cards (Total Partner, Partner Aktif, Total Pengguna, Feature Flags)

**`templates/platform/partner_list.html`**
- Tambah: `{% block breadcrumb %}` dengan jalur Studio › Platform › Partner
- Ganti ke: tabel `amp-card` dengan dark mode lengkap
- Tambah: avatar/initial letter untuk partner tanpa logo
- Upgrade: empty state dengan icon + deskripsi + CTA "Tambah Partner Pertama"
- Tambah: paginasi

**`templates/platform/provider_list.html`**
- Tambah: `{% block breadcrumb %}` dengan jalur Studio › Platform › Provider
- Ganti: card style ke `amp-card`
- Tambah: outer empty state (icon + deskripsi) saat tidak ada provider sama sekali

### 3. Media Manager Templates — AMP Studio Card Style

Semua 7 template child `media_manager/` diupgrade dari `bg-white dark:bg-coffee-800 shadow rounded-lg` ke `amp-card`:

- **`dashboard.html`** — Redesign lengkap: stat cards 4-kolom, grid file terbaru, quick links ke semua sub-halaman
- **`list.html`** — Grid file dengan hover, filter aktif, empty state berbeda untuk "kosong" vs "pencarian tidak ditemukan"
- **`upload.html`** — Drop zone dipertahankan, card container diupgrade, file input distilkan
- **`detail.html`** — Layout 3+2 kolom, info pipeline status tampil, metadata audio (artist/album/bitrate) tampil jika ada
- **`folders.html`** — Icon folder per baris, delete button muncul saat hover (group), empty state dengan icon
- **`tags.html`** — Color swatch per tag, delete on hover, empty state dengan icon
- **`delete_confirm.html`** — Card terpusat dengan icon destructive, nama file ditampilkan, tombol "Ya, Hapus Permanen"

### 4. Empty States — Icon + Deskripsi + CTA

Semua halaman list yang sebelumnya hanya menampilkan teks sederhana kini mengikuti pola standar:

```
[Icon dalam lingkaran]
Judul empty state
Deskripsi singkat
[CTA Button → halaman buat baru]
```

Halaman yang diupgrade: Program Siaran, Episode Siaran, Podcast, Episode Podcast, Artikel, Media Library.

---

## Technical Debt yang Diketahui (Tidak Diperbaiki Sprint Ini)

| Item | Keterangan |
|---|---|
| `core/home.html` + `dashboard/home.html` | Masih extend `dashboard_base.html` lama — perlu migrasi terpisah |
| `settings/` templates | Extend `settings/base.html` sendiri (bukan `amp_studio/base.html`) — arsitektur disengaja, bukan bug |
| `platform/partner_detail.html` | Belum diaudit detail — perlu pass terpisah |
| `platform/partner_form.html` | Belum diaudit detail |
| `platform/theme_edit.html` + `feature_list.html` | Belum diaudit detail |
| Radio stream live now-playing | Timeout ke `a7.siar.us` — ditangani Sprint 4.4 (Task #4) |

---

## Ringkasan

- **17 halaman** diaudit dan diperbaiki
- **2 halaman** "Segera Hadir" dibersihkan
- **3 halaman** platform mendapat dark mode + breadcrumb
- **7 template** media_manager diupgrade ke AMP Studio design system
- **6 halaman** mendapat empty state standar dengan CTA
- Tidak ada migrasi database, tidak ada perubahan model, tidak ada instalasi package baru
