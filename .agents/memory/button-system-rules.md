---
name: Button System Rules
description: Aturan wajib untuk semua tombol di AMP Studio — mencegah tombol putih di atas putih (invisible button).
---

## Masalah yang pernah terjadi
Tombol yang menggunakan Tailwind CDN custom color class (`bg-coffee-500`, `bg-coffee-600`, `bg-slate-100`, dll.)
dapat merender **putih di atas putih (invisible)** karena Tailwind CDN JIT compilation untuk custom colors
dapat gagal atau terlambat — sehingga background-color tidak diterapkan, tapi `text-white` tetap aktif.
Hasil: teks putih di atas latar belakang putih = tidak terlihat.

## Aturan wajib: selalu gunakan kelas `amp-btn`

CSS variables di `static/css/amp-studio/design-tokens.css` selalu di-load via stylesheet statis
dan selalu reliable. Gunakan kelas `amp-btn` yang bergantung pada CSS vars, BUKAN raw Tailwind colors.

### Kelas yang tersedia

| Kelas | Tampilan | Gunakan untuk |
|---|---|---|
| `amp-btn amp-btn-primary` | Coffee-600 bg, teks putih | Aksi utama: Simpan, Buat, Submit |
| `amp-btn amp-btn-secondary` | Border abu, bg transparan | Aksi sekunder: Batal, Kembali |
| `amp-btn amp-btn-ghost` | Tanpa border/bg | Navigasi, Filter, Reset |
| `amp-btn amp-btn-danger` | Merah bg, teks putih | Hapus, Nonaktifkan permanen |
| `amp-btn amp-btn-success` | Hijau bg, teks putih | Aktifkan, Approve |
| `amp-btn amp-btn-warning` | Oranye bg, teks putih | Tangguhkan, Peringatan |

### Modifier ukuran (opsional)
- `amp-btn-sm` — kecil (untuk inline table actions)
- `amp-btn-xs` — sangat kecil

### Contoh benar ✅

```html
<!-- Primary / Submit -->
<button type="submit" class="amp-btn amp-btn-primary">Simpan Perubahan</button>

<!-- Cancel / Batal -->
<a href="{% url 'broadcast:list' %}" class="amp-btn amp-btn-secondary">Batal</a>

<!-- Filter -->
<button type="submit" class="amp-btn amp-btn-ghost">Filter</button>

<!-- Danger / Delete -->
<button type="submit" class="amp-btn amp-btn-danger">Hapus</button>

<!-- Warning / Suspend -->
<button type="submit" class="amp-btn amp-btn-warning">Tangguhkan</button>

<!-- Dengan icon -->
<a href="..." class="amp-btn amp-btn-primary flex items-center gap-2">
  <svg>...</svg>
  Tambah Data
</a>
```

### Contoh SALAH ❌ — JANGAN PERNAH pakai ini di /studio templates

```html
<!-- SALAH: Tailwind custom color — bisa invisible -->
<button class="bg-coffee-600 text-white rounded-lg ...">Simpan</button>
<button class="bg-coffee-500 text-white rounded-lg ...">Buat</button>
<button class="bg-slate-100 text-slate-700 dark:bg-slate-700 dark:text-slate-300 ...">Filter</button>
<a class="px-6 py-2 border border-slate-300 text-slate-700 ...">Batal</a>

<!-- SALAH: amp-btn tanpa variant = tidak ada background/text color -->
<button class="amp-btn">Aksi</button>
```

## Scope berlaku

Semua template yang di-extend dari `amp_studio/base.html`:
- `templates/broadcast/**`
- `templates/radio/**`
- `templates/platform/**`
- `templates/settings/**`
- `apps/users/templates/users/admin/**`
- `templates/media_manager/**`

**PENGECUALIAN:** Template website publik (`templates/website/**`) dan player radio components
boleh tetap menggunakan `bg-coffee-500 text-white` karena tidak bergantung pada design token
yang sama dan memiliki konteks rendering berbeda.

## Catatan settings templates

Settings templates (`templates/settings/`) secara sengaja menggunakan coffee palette untuk sidebar
dan elemen dekoratif. Tapi tombol submit/aksi di form tetap harus menggunakan `amp-btn amp-btn-primary`.

**Why:** CSS vars selalu reliable; Tailwind CDN custom colors tidak.
**How to apply:** Setiap kali menulis `<button>` atau link yang berfungsi sebagai tombol di /studio,
wajib gunakan `amp-btn` + salah satu variant class di atas.
