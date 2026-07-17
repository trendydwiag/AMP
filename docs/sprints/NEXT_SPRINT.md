# Next Sprint Recommendations
**Based on:** Sprint 4.0 completion (Knowledge Base Refresh)
**Demo date:** July 21, 2026
**Prepared:** July 17, 2026

> ⚠️ **NOTE:** File ini diperbarui di Sprint 4.0. Versi sebelumnya merujuk ke Sprint 3.5A.
> Sprint 3.5, 3.6, 3.7, dan 4.0 sudah **SELESAI**.

---

## Status Sprint Terkini

| Sprint | Judul | Status |
|---|---|---|
| 3.5 | Founder Experience | ✅ DONE |
| 3.6 | Platform UI Consistency | ✅ DONE |
| 3.7 | UX/Visual Regression Fixes | ✅ DONE |
| 4.0 | Knowledge Base Refresh | ✅ DONE |

---

## Sprint Berikutnya yang Direkomendasikan

### 🚨 PRIORITY 0 — Task #2 (CRITICAL untuk demo)

**Sprint 4.1 — Superuser Setup & Demo Verification**

**Task:** Buat superuser account dan verifikasi studio login
- Jalankan: `python manage.py create_superadmin`
- Atau: `python manage.py reset_admin`
- Verifikasi login di `/akun/masuk/` → redirect ke `/studio/`
- Verifikasi dark mode toggle berfungsi
- Verifikasi radio player bar berfungsi
- Jalankan demo seed: `python manage.py demo_seed --reset`

**Effort:** 30 menit
**Blocker:** Tanpa ini, AMP Studio tidak bisa di-demo

---

### 🔴 PRIORITY 1 — Technical Debt Kritis

**Sprint 4.2 — Live API Program Name (TD-001)**

**Task:** Wire program name ke `GET /api/v1/radio/live/`
- Di `LiveRadioAPIView.get()`, query `apps/broadcast` untuk jadwal slot aktif berdasarkan hari/jam sekarang
- Populate field `program` dengan nama program yang sedang on-air
- Cache bersama dengan data upstream (20s TTL)
- Saat ini field `program` selalu return null → terlihat sebagai bug di demo

**Effort:** 2–4 jam
**Files:** `apps/radio/views.py` (LiveRadioAPIView), `apps/broadcast/repositories.py` (ScheduleRepository)

**Sprint 4.3 — Stream URL Fallback (TD-002)**

**Task:** Tambah fallback stream URL
- Tambah `STREAM_URL` ke `config/settings/base.py` (env-var readable)
- Di `LiveRadioAPIView`, gunakan `station.listen_url` jika ada; fallback ke `settings.STREAM_URL`
- Di `radio-player.js`, tampilkan visible error state jika `streamUrl` kosong

**Effort:** 1–2 jam

---

### 🟡 PRIORITY 2 — Task #4 (Real Radio Stream)

**Sprint 4.4 — Connect Real Radio Stream**

**Task:** Pastikan live player tampil data now-playing dari stream nyata
- Verifikasi `a7.siar.us` reachable dari dev/production environment
- Jika tidak reachable: configure AzuraCast adapter sebagai primary
- Pastikan `/api/v1/radio/live/` return `"status": "live"` (bukan `"offline"`)
- Verifikasi track title dan listener count muncul di dashboard

**Note:** Architecture sudah ada (BroadcastindoAdapter active). Problem utama adalah network access dari Replit ke upstream provider.

---

### 🟡 PRIORITY 3 — Medium Priority

**Sprint 4.5 — Analytics Dashboard (Real Data)**
- Agregasi `ListenerStatistic` records ke dashboard analytics
- Chart listener over time
- Status: view + template sudah ada, data belum diagregasi

**Sprint 4.6 — Automated Tests**
- `apps/radio/tests/test_live_api.py`
- Test happy path + offline fallback + cache behavior

**Sprint 4.7 — Platform Migrations**
- Verifikasi dan apply unapplied migrations di `apps/platform`
- `python manage.py showmigrations` → `python manage.py migrate`

---

## Post-Demo Scope (Jangan Dimulai Sebelum 21 Juli)

| Item | Alasan defer |
|---|---|
| WebSocket/SSE real-time updates | Butuh Django Channels — multi-day effort |
| Full AMP Streaming Connector architecture | Post-demo replacement untuk Broadcastindo adapter |
| Mobile app | Future scope |
| Listener history charts dengan real data | DB records belum ter-populate dari live stream |
| Service extraction (StudioService) | Low priority, tidak blocking |
| Merge duplicate tag/category models | Breaking change, needs careful migration |
