# Management Commands

## Settings App

### `init_settings`
Inisialisasi semua pengaturan default (singleton) ke database.

```bash
python manage.py init_settings
```

**Output:**
```
  pengaturan situs: DIBUAT
  pengaturan seo: DIBUAT
  pengaturan email: DIBUAT
  pengaturan keamanan: DIBUAT
  pengaturan tampilan: DIBUAT
  pengaturan notifikasi: DIBUAT
  pengaturan media sosial: DIBUAT
  pengaturan konten: DIBUAT
  bahasa & lokal: DIBUAT
  pengaturan media: DIBUAT
Semua pengaturan berhasil diinisialisasi.
```

---

## Media Manager App

### `cleanup_media`
Bersihkan file media orphans dan cache thumbnails lama.

```bash
python manage.py cleanup_media --days 30 --dry-run
python manage.py cleanup_media --days 30
```

**Options:**
- `--days N` — Hapus file lebih tua dari N hari (default: 30)
- `--dry-run` — Tampilkan file yang akan dihapus tanpa menghapus

### `generate_thumbnails`
Generate ulang thumbnails untuk semua file gambar.

```bash
python manage.py generate_thumbnails
python manage.py generate_thumbnails --force
```

**Options:**
- `--force` — Generate ulang semua thumbnails termasuk yang sudah ada

### `compress_media`
Kompresi gambar untuk menghemat storage.

```bash
python manage.py compress_media --quality 85 --max-width 1920
python manage.py compress_media --dry-run
```

**Options:**
- `--quality N` — Kualitas kompresi JPEG 1-100 (default: 85)
- `--max-width N` — Lebar maksimum dalam px (default: 1920)
- `--dry-run` — Tampilkan tanpa mengubah

---

## Radio App

### `refresh_now_playing`
Refresh now playing data dari provider untuk semua/satu station.

```bash
python manage.py refresh_now_playing
python manage.py refresh_now_playing --station <uuid>
```

### `refresh_listener`
Refresh listener statistics dari provider.

```bash
python manage.py refresh_listener
python manage.py refresh_listener --station <uuid>
```

### `check_stream_health`
Check stream health untuk semua/satu station.

```bash
python manage.py check_stream_health
python manage.py check_stream_health --station <uuid>
```

### `cleanup_cache`
Bersihkan data cache listener statistics dan health checks lama.

```bash
python manage.py cleanup_cache --days 30 --dry-run
python manage.py cleanup_cache --days 30
```

**Options:**
- `--days N` — Hapus data lebih tua dari N hari (default: 30)
- `--dry-run` — Tampilkan tanpa menghapus

### `refresh_radio_all`
Refresh semua radio data (now playing + listeners + health) sekaligus.

```bash
python manage.py refresh_radio_all
```
