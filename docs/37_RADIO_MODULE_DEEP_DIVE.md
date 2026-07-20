# 37. Radio Module Deep Dive

## Overview

Radio module (`apps/radio`) mengelola streaming live radio di Kabulhaden CMS: konfigurasi provider, metadata now-playing, listener statistics, stream health monitoring, dan live session tracking. Module ini terpisah dari `apps/broadcast` yang mengelola konten siaran (program, jadwal, rekaman).

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         Radio Module                                 │
│                                                                      │
│  ┌──────────────┐   ┌──────────────┐   ┌──────────────┐            │
│  │ RadioStation │──▶│ RadioProvider│   │ NowPlaying   │            │
│  │ (stasiun)    │   │ (Icecast/AZ) │   │ Cache        │            │
│  └──────────────┘   └──────────────┘   └──────────────┘            │
│         │                  │                   │                     │
│         │            ┌─────▼─────────────┐    │                     │
│         │            │   Adapter Layer    │    │                     │
│         │            │  IcecastAdapter    │    │                     │
│         │            │  AzuraCastAdapter  │    │                     │
│         │            │  BroadcastindoAdptr│    │                     │
│         │            └─────────────────────┘    │                    │
│         │                                       │                    │
│  ┌──────▼──────────────────────────────────────▼──────────────────┐│
│  │                    LiveRadioAPIView                              ││
│  │  GET /api/v1/radio/live/  (20s cache, offline-safe)             ││
│  └─────────────────────────────────────────────────────────────────┘│
│                               │                                      │
│              ┌────────────────▼─────────────────┐                   │
│              │         Browser                   │                   │
│              │   Alpine.store('radio')           │                   │
│              │   audio.src = stream_url (direct) │                   │
│              └───────────────────────────────────┘                  │
└─────────────────────────────────────────────────────────────────────┘
```

**Key Design Decision:** Browser connect langsung ke URL stream (Icecast/ngrok), bukan melalui Django proxy. Ini karena Replit's reverse proxy mem-buffer streaming responses. Lihat `docs/adr/0010-multi-provider-radio-engine.md`.

---

## Data Models

### RadioStation

Stasiun radio. Satu instalasi bisa punya beberapa stasiun (multi-partner).

```python
class RadioStation(models.Model):
    id              = UUIDField (PK)
    station_name    = CharField(max_length=200)
    is_active       = BooleanField(default=True)
    logo            = ImageField(upload_to='radio/stations/')
    default_volume  = IntegerField(default=75)   # 0-100
    autoplay        = BooleanField(default=False)
    sticky_player   = BooleanField(default=True)

    @property
    def primary_provider(self):
        return self.providers.filter(active=True).first()
```

### RadioProvider

Konfigurasi koneksi ke streaming provider (Icecast, AzuraCast, dll).

```python
class RadioProvider(models.Model):
    id            = UUIDField (PK)
    station       = ForeignKey(RadioStation)
    provider_name = CharField(max_length=200)
    provider_type = CharField(choices=['ICECAST','AZURACAST','BROADCASTINDO','SIAR'])
    api_url       = URLField()     # Endpoint metadata: .../status-json.xsl (Icecast)
    stream_url    = URLField()     # URL audio yang dimainkan browser
    username      = CharField()    # Opsional untuk provider yang butuh auth
    password      = CharField()
    timeout       = IntegerField(default=8)
    active        = BooleanField(default=True)
    backup_stream_url = URLField(blank=True)
```

### NowPlayingCache

Cache metadata lagu yang sedang diputar. Diupdate setiap kali `LiveRadioAPIView` query provider.

```python
class NowPlayingCache(models.Model):
    station        = OneToOneField(RadioStation)
    song_title     = CharField()
    artist         = CharField()
    album          = CharField()
    artwork        = URLField()
    stream_status  = CharField()   # 'LIVE' | 'OFFLINE'
    duration       = FloatField()  # detik
    elapsed        = FloatField()
    progress_percent = FloatField()
    raw_response   = JSONField()   # Raw response dari provider API
```

### ListenerStatistic

Statistik jumlah pendengar saat ini dan peak.

```python
class ListenerStatistic(models.Model):
    station          = ForeignKey(RadioStation)
    current_listeners = IntegerField(default=0)
    peak_listeners   = IntegerField(default=0)
    recorded_at      = DateTimeField(auto_now=True)
```

### StreamHealth

Hasil health check stream terakhir.

```python
class StreamHealth(models.Model):
    station        = ForeignKey(RadioStation)
    provider_status = CharField()  # 'HEALTHY' | 'DEGRADED' | 'DOWN'
    http_status    = IntegerField()
    response_time  = FloatField()  # ms
    stream_bitrate = IntegerField()
    last_checked   = DateTimeField(auto_now=True)
```

### LiveSession

Sesi siaran langsung yang aktif.

```python
class LiveSession(models.Model):
    station    = ForeignKey(RadioStation)
    program    = CharField()
    host       = CharField()
    started_at = DateTimeField()
    ended_at   = DateTimeField(null=True)
```

---

## Adapter Layer

Semua adapter mewarisi `BaseRadioAdapter` dari `apps/radio/adapters/base.py`.

### BaseRadioAdapter

```python
class BaseRadioAdapter:
    def __init__(self, api_url, stream_url, username='', password='', timeout=8):
        ...

    def _make_request(self, url, **kwargs):
        """Semua HTTP request keluar melalui method ini.
        Menambahkan header ngrok-skip-browser-warning: true secara otomatis."""
        headers = {
            'ngrok-skip-browser-warning': 'true',
            'User-Agent': 'AMP-Studio/1.0',
        }
        response = requests.get(url, headers=headers, timeout=self.timeout, **kwargs)
        return response

    def get_now_playing(self) -> NowPlayingResult:
        raise NotImplementedError

    def get_listener_count(self) -> ListenerResult:
        raise NotImplementedError
```

### IcecastAdapter (`adapters/icecast.py`)

Mendukung Icecast 2.x via `/status-json.xsl`.

**`_find_mount(data, mount_name)`** — helper kritis:
- Icecast mengembalikan `icestats.source` (bukan `icestats.mount`)
- Satu source → dict; lebih dari satu source → list
- Cocokkan berdasarkan `listenurl` yang mengandung `mount_name`

```python
def _find_mount(self, data, mount_name):
    icestats = data.get('icestats', {})
    sources = icestats.get('source', icestats.get('mount'))
    if not sources:
        return None
    if isinstance(sources, dict):
        sources = [sources]   # normalize ke list
    for s in sources:
        if mount_name in s.get('listenurl', ''):
            return s
    return sources[0] if sources else None
```

**`get_now_playing()`** — mengambil `title`, `artist` dari `source.title` (format "Artist - Title"):
```python
raw_title = source.get('title', '')
if ' - ' in raw_title:
    artist, title = raw_title.split(' - ', 1)
```

**`get_listener_count()`** — membaca `source.listeners` (bukan `icestats.listeners`).

### AzuraCastAdapter (`adapters/azuracast.py`)

Mendukung AzuraCast via `/api/nowplaying/<station_id>` (JSON).

### BroadcastindoAdapter (`adapters/broadcastindo.py`)

Mendukung Broadcastindo/Siar.us via endpoint mereka sendiri.

### Registrasi Adapter

```python
# apps/radio/adapters/__init__.py
ADAPTER_MAP = {
    'ICECAST':       IcecastAdapter,
    'AZURACAST':     AzuraCastAdapter,
    'BROADCASTINDO': BroadcastindoAdapter,
    'SIAR':          BroadcastindoAdapter,  # alias
}

def get_adapter(provider_type: str) -> type[BaseRadioAdapter]:
    return ADAPTER_MAP[provider_type.upper()]
```

---

## LiveRadioAPIView

`GET /api/v1/radio/live/` — endpoint utama yang dikonsumsi semua UI component.

### Karakteristik
- **No authentication required** — publik, bisa dicall dari browser tanpa login
- **20 detik cache** (`STREAM_CACHE_TTL` setting, default 20)
- **Offline-safe** — tidak pernah return HTTP error; selalu return HTTP 200 dengan `status: "offline"` jika upstream gagal
- **DB-first provider** — selalu pakai provider yang disimpan di DB; settings sebagai fallback

### Flow

```
GET /api/v1/radio/live/
  │
  ├─ Cache hit? → return cached JSON
  │
  ├─ Resolve provider (DB-first):
  │    station = RadioStationService.get_primary_station()
  │    db_provider = station.primary_provider  (active=True)
  │    listen_url_fallback = db_provider.stream_url
  │
  ├─ try:
  │    adapter = get_adapter(db_provider.provider_type)(...)
  │    np = adapter.get_now_playing()
  │    listener_data = adapter.get_listener_count()
  │    stream_url = np.raw_response.get('listen_url') or listen_url_fallback
  │    → build data dict
  │
  ├─ except Exception:
  │    → build fallback data (stream_url = listen_url_fallback)
  │
  ├─ cache.set('amp_v1_live_radio', data, cache_ttl)
  └─ return JsonResponse(data)
```

### Response Schema

```json
{
  "status":     "live" | "offline",
  "station":    "Kabulhaden Online",
  "program":    null,
  "title":      "Song Title",
  "artist":     "Artist Name",
  "cover":      "",
  "listeners":  3,
  "started_at": null,
  "stream_url": "https://<ngrok-subdomain>.ngrok-free.app/kabulhaden.mp3",
  "is_live":    true,
  "provider":   "icecast"
}
```

> **Note:** `program` selalu `null` (TD-001 — integrasi broadcast schedule belum dilakukan).

---

## RadioStreamProxyView

`GET /radio/stream/` — same-origin proxy yang merelay byte audio dari Icecast ke browser.

**Kapan digunakan:**
- Production deployment di belakang Nginx (Nginx mendukung streaming response dengan benar)
- Debugging server-side audio tanpa CORS consideration

**Kapan TIDAK digunakan (default):**
- Replit development — Replit's reverse proxy mem-buffer streaming response, sehingga browser tidak pernah menerima data audio (spinner terus berputar). Lihat `docs/deployment/TROUBLESHOOTING.md#radio-streaming-issues-replit`.

**Default saat ini:** `LiveRadioAPIView` mengembalikan `stream_url` langsung (URL Icecast/ngrok), bukan `/radio/stream/`.

---

## Frontend — Alpine.store('radio')

Radio player menggunakan Alpine.js global store, bukan komponen `x-data`. Ini memungkinkan template mana pun membaca dan mengontrol state player yang sama.

### State Properties

| Property | Type | Description |
|---|---|---|
| `isPlaying` | boolean | Audio sedang diputar |
| `isLoading` | boolean | Buffer loading (spinner ditampilkan) |
| `isLive` | boolean | Stream sedang live |
| `isMuted` | boolean | Audio di-mute |
| `volume` | number | Volume 0–100 (persisted ke localStorage) |
| `streamUrl` | string | URL stream dari `/api/v1/radio/live/` |
| `currentTrack` | object | `{ title, artist, artwork }` |
| `listeners` | number | Jumlah pendengar saat ini |

### Key Methods

| Method | Description |
|---|---|
| `init()` | Setup audio element, event listeners, mulai polling. Dipanggil manual. |
| `togglePlay()` | Play/pause. Selalu menghormati klik pengguna (tidak ada isLoading guard). |
| `fetchStatus()` | Fetch `/api/v1/radio/live/`, update state. Poll setiap 25 detik. |
| `scheduleReconnect()` | Exponential backoff (1s, 2s, 4s… max 30s). Reset `isLoading` di catch. |
| `setVolume(event)` | Set volume dari click position pada progress bar. |

### Penggunaan di Template

```html
<!-- Harus berada dalam x-data (bisa empty) -->
<div x-data>
  <button @click="$store.radio.togglePlay()">
    <template x-if="$store.radio.isLoading">
      <svg class="animate-spin">...</svg>
    </template>
    <template x-if="$store.radio.isPlaying && !$store.radio.isLoading">
      <!-- pause icon -->
    </template>
    <template x-if="!$store.radio.isPlaying && !$store.radio.isLoading">
      <!-- play icon -->
    </template>
  </button>
  <span x-text="$store.radio.currentTrack.title"></span>
  <span x-text="$store.radio.currentTrack.artist"></span>
  <span x-text="$store.radio.listeners + ' pendengar'"></span>
</div>
```

**Reference:** `static/js/radio-player.js`, `templates/website/components/sticky_player.html`, `templates/website/components/home/hero_radio.html`

---

## Hero Radio Layout

`templates/website/components/home/hero_radio.html` — komponen player di homepage.

| Property | Sebelum Sprint 4.3 | Sesudah Sprint 4.3 |
|---|---|---|
| min-height | 90vh | 72vh |
| Vertical padding | py-28 | py-16 |
| Tombol play | 120px | 80px |
| Card width | 500px | 360px |
| Album art | aspect-square (full) | fixed 160px height |

---

## Services

| Service | Tanggung Jawab |
|---|---|
| `RadioStationService` | CRUD station, get_primary_station() |
| `RadioProviderService` | CRUD provider, toggle_active() |
| `NowPlayingService` | get_now_playing(station_id) |
| `ListenerService` | get_current(station_id), export_csv/excel |
| `StreamHealthService` | get_latest(station_id), get_health_history() |
| `LiveSessionService` | get_active(station_id) |
| `PlayerService` | get_player_config() → volume, autoplay, stream_url |
| `FallbackService` | get_available_stream(station_id) → URL dengan fallback |
| `MetadataService` | Metadata manipulation helpers |
| `BroadcastIntegrationService` | get_current_program() — integrasi ke apps.broadcast |

---

## Catatan Operasional (ngrok)

Saat testing dengan ngrok free-tier, URL berubah setiap restart tunnel. Update manual diperlukan:

```bash
# Update via Django shell
python3 manage.py shell -c "
from apps.radio.models import RadioProvider
p = RadioProvider.objects.filter(active=True).first()
p.api_url = 'https://NEW-SUBDOMAIN.ngrok-free.app/status-json.xsl'
p.stream_url = 'https://NEW-SUBDOMAIN.ngrok-free.app/kabulhaden.mp3'
p.save()
from django.core.cache import cache
cache.delete('amp_v1_live_radio')
print('Updated and cache cleared.')
"
```

Atau lewat: **AMP Studio → Radio → Provider → Edit**.

---

## Related Documentation

- `docs/adr/0010-multi-provider-radio-engine.md` — ADR untuk multi-provider architecture
- `docs/31_API_ENDPOINTS_REFERENCE.md` — semua radio API endpoints
- `docs/26_ALPINEJS_PATTERNS.md` — Alpine.store('radio') pattern detail
- `docs/changelog/sprint-4.3.md` — bug fixes Sprint 4.3
- `docs/architecture/TECH_DEBT.md` — TD-001 (program null), TD-008 (ngrok URL)
- `docs/deployment/TROUBLESHOOTING.md#radio-streaming-issues-replit` — troubleshooting audio

---

*Last updated: Sprint 4.3 — 20 Juli 2026*
