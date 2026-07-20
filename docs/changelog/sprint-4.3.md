# Sprint 4.3 — Radio Live Player Stabilization

**Tanggal:** 20 Juli 2026
**Tipe:** Bug Fix + Architecture Fix
**Objective:** Buat live radio player benar-benar bisa play audio di browser. Sebelumnya player menampilkan metadata dengan benar tapi tombol play tidak menghasilkan suara.

---

## Root Cause Analysis

Terdapat 6 bug yang ditemukan dan diperbaiki secara berurutan:

### Bug 1 — `LiveRadioAPIView` Mengabaikan Database
`views.py` membaca `settings.STREAM_PROVIDER` dan `settings.STREAM_API_URL` secara hardcoded, sehingga provider apapun yang disimpan lewat UI diabaikan.

**Fix:** DB-first lookup via `RadioStationService` → `station.primary_provider`. Settings hanya dipakai sebagai fallback ketika tidak ada provider aktif di DB.

### Bug 2 — `icecast.py` NameError
`get_listener_count()` mereferensikan variabel `ice` sebelum di-assign.

**Fix:** Perbaiki urutan assignment variabel.

### Bug 3 — ngrok Bypass Header Hilang (Server-Side)
`base.py` `_make_request()` tidak mengirim header `ngrok-skip-browser-warning: true` ke upstream, sehingga ngrok mengembalikan HTML interstitial alih-alih data JSON/audio.

**Fix:** Header ditambahkan ke semua upstream request di `BaseAdapter._make_request()`.

### Bug 4 — `_find_mount()` Menggunakan Key yang Salah
Icecast mengembalikan `icestats.source` (bukan `icestats.mount`). Ketika hanya satu source yang terhubung, nilainya berupa dict; beberapa source berupa list.

**Fix:** `_find_mount()` dicek `source` dulu, `mount` sebagai fallback, handle keduanya.

### Bug 5 — `isLoading` Tersangkut True
Di `scheduleReconnect()`, ketika reconnect `audio.play()` gagal, `.catch(() => {})` tidak melakukan apapun — `isLoading` tetap `true`. Klik pengguna berikutnya mengenai `if (this.isLoading) return;` dan keluar diam-diam.

**Fix:** Catch block di reconnect timer sekarang reset `isLoading = false`. `togglePlay()` dirombak agar selalu menghormati klik pengguna dengan membatalkan reconnect timer yang pending dan reset `isLoading` sebelum mencoba play. Error logging ditambahkan ke semua catch block.

### Bug 6 — Replit Reverse Proxy Mem-buffer Streaming Response
Django proxy (`/radio/stream/`) dikembalikan sebagai `stream_url`. Browser mengirim request ke Replit dev domain, tapi reverse proxy Replit mem-buffer seluruh response body sebelum diteruskan ke browser — yang tidak pernah selesai untuk live stream. Browser spinner terus tanpa menerima data.

**Fix:** `LiveRadioAPIView` mengembalikan URL stream langsung dari provider (ngrok/Icecast URL). Browser connect langsung ke Icecast, bypass semua proxy. Icecast sudah mengirim `Access-Control-Allow-Origin: *` sehingga CORS bukan masalah.

> **Note:** Django proxy endpoint `/radio/stream/` tetap tersedia di `RadioStreamProxyView` sebagai fallback untuk deployment production non-Replit.

---

## Perubahan File

### Backend

| File | Perubahan |
|---|---|
| `apps/radio/views.py` | `LiveRadioAPIView`: DB-first provider; mengembalikan `stream_url` langsung (bukan proxy); perbaiki except block. Tambah `RadioStreamProxyView`. |
| `apps/radio/urls.py` | Tambah `path('stream/', RadioStreamProxyView, name='stream_proxy')` |
| `apps/radio/adapters/icecast.py` | Perbaiki `_find_mount()` gunakan key `source` (bukan `mount`); handle dict & list; perbaiki `ice` NameError di `get_listener_count()` |
| `apps/radio/adapters/base.py` | Tambah header `ngrok-skip-browser-warning: true` di `_make_request()` |

### Frontend

| File | Perubahan |
|---|---|
| `static/js/radio-player.js` | Fix `isLoading` stuck bug di `scheduleReconnect()` catch; refactor `togglePlay()` agar selalu honouri klik; tambah `console.warn` di semua error path; hapus `crossOrigin='anonymous'` |
| `templates/website/main.html` | Hapus stale comment tentang pola lama `x-data="radioPlayer()"`; tambah cache bust `?v=2` |
| `templates/website/components/home/hero_radio.html` | Kompakkan layout: `min-h` 90vh→72vh, `py-28`→`py-16`, tombol play 120px→80px, card 500px→360px, album art fixed 160px |

### Config

| File | Perubahan |
|---|---|
| `config/settings/development.py` | Tambah `CSP_MEDIA_SRC = ("'self'",)`; perluas `CSP_CONNECT_SRC` dengan `wss:` dan `https:` |

---

## Tech Debt Diselesaikan

- **TD-002** (No Fallback Stream URL) — RESOLVED. `listen_url_fallback = db_provider.stream_url` di-set sebelum try block, digunakan di except block. `stream_url` di try block mengambil dari API response dulu, fallback ke `listen_url_fallback`.

---

## Catatan Operasional

**ngrok URL harus diupdate di DB setiap kali tunnel di-restart.** ngrok free-tier men-generate URL baru setiap restart. Update via: AMP Studio → Radio → Provider → Edit.

Field yang perlu diupdate:
- `api_url` → `https://<ngrok-subdomain>.ngrok-free.app/status-json.xsl`
- `stream_url` → `https://<ngrok-subdomain>.ngrok-free.app/kabulhaden.mp3`

---

## Cara Verifikasi

```bash
# 1. Pastikan Icecast sedang live (ada broadcaster terhubung)
curl -s https://<ngrok-url>/status-json.xsl | python3 -m json.tool

# 2. Cek API mengembalikan data benar
curl -s http://localhost:5000/api/v1/radio/live/ | python3 -m json.tool
# Harus: stream_url berisi URL ngrok langsung, is_live: true

# 3. Cek stream URL bisa diakses
curl -si <stream_url> | head -5
# Harus: HTTP/2 200, Content-Type: audio/mpeg
```

---

## Known Limitations

- **Stream offline saat tidak ada broadcaster** → `NotSupportedError` di browser adalah perilaku benar. Player akan reconnect otomatis saat stream kembali online.
- **ngrok URL berubah saat restart** → Perlu update manual di DB (lihat Catatan Operasional di atas).
- `program` field masih `null` (TD-001, belum diselesaikan — menunggu integrasi broadcast schedule).
