# 38. Broadcast Module Deep Dive

## Overview

This guide provides an in-depth look at the Broadcast module in Kabulhaden CMS, covering encoders, streams, playlists, recordings, and live broadcast management.

---

## Broadcast Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         Broadcast System                                      │
│                                                                              │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐  │
│  │   Encoder    │───▶│   Stream    │───▶│  Listener   │───▶│   Player    │  │
│  │  (Icecast)   │    │  (Output)   │    │  (Client)   │    │  (Web/Radio)│  │
│  └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘  │
│         │                                                            │       │
│         ▼                                                            ▼       │
│  ┌─────────────┐                                           ┌─────────────┐  │
│  │  Playlist    │                                           │  Recording  │  │
│  │  (Scheduled) │                                           │  (Archive)  │  │
│  └─────────────┘                                           └─────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Data Models

### Encoder

```python
# apps/broadcast/models.py
class Encoder(UUIDPrimaryKeyMixin, TimeStampMixin):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    encoder_type = models.CharField(max_length=20, choices=EncoderType.choices)
    host = models.CharField(max_length=200)
    port = models.IntegerField()
    mount_point = models.CharField(max_length=100)
    password = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    is_connected = models.BooleanField(default=False)
    bitrate = models.IntegerField(default=128)  # kbps
    sample_rate = models.IntegerField(default=44100)
    channels = models.IntegerField(default=2)
    last_health_check = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    @property
    def stream_url(self):
        return f"http://{self.host}:{self.port}{self.mount_point}"
    
    @property
    def status(self):
        if not self.is_active:
            return 'inactive'
        if self.is_connected:
            return 'connected'
        return 'disconnected'


class EncoderType(models.TextChoices):
    ICECAST = 'icecast', 'Icecast'
    SHOUTCAST = 'shoutcast', 'Shoutcast'
    CUSTOM = 'custom', 'Custom'
```

### Stream

```python
class Stream(UUIDPrimaryKeyMixin, TimeStampMixin):
    station = models.ForeignKey('radio.Station', on_delete=models.CASCADE, related_name='streams')
    encoder = models.ForeignKey(Encoder, on_delete=models.CASCADE, related_name='streams')
    name = models.CharField(max_length=200)
    is_live = models.BooleanField(default=False)
    started_at = models.DateTimeField(null=True, blank=True)
    listener_count = models.IntegerField(default=0)
    peak_listeners = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['-started_at']
    
    def __str__(self):
        return f"{self.station.name} - {self.name}"
    
    @property
    def duration(self):
        if self.started_at:
            return timezone.now() - self.started_at
        return None
```

### Playlist

```python
class Playlist(UUIDPrimaryKeyMixin, TimeStampMixin):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    is_active = models.BooleanField(default=True)
    total_duration = models.FloatField(default=0)  # seconds
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def recalculate_duration(self):
        self.total_duration = sum(
            track.episode.duration for track in self.tracks.all()
        )
        self.save()


class PlaylistTrack(UUIDPrimaryKeyMixin):
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE, related_name='tracks')
    episode = models.ForeignKey('radio.Episode', on_delete=models.CASCADE)
    position = models.IntegerField(default=0)
    added_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['position']
        unique_together = ['playlist', 'episode']
```

### Recording

```python
class Recording(UUIDPrimaryKeyMixin, TimeStampMixin):
    stream = models.ForeignKey(Stream, on_delete=models.CASCADE, related_name='recordings')
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='broadcast/recordings/')
    file_size = models.BigIntegerField()
    duration = models.FloatField()  # seconds
    recorded_at = models.DateTimeField()
    format = models.CharField(max_length=10)  # mp3, wav, etc
    
    class Meta:
        ordering = ['-recorded_at']
    
    def __str__(self):
        return self.title
    
    @property
    def file_size_display(self):
        size = self.file_size
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024:
                return f"{size:.1f} {unit}"
            size /= 1024
        return f"{size:.1f} TB"
```

---

## Broadcast Flow

### Starting a Broadcast

```
┌─────────────────────────────────────────────────────────────┐
│  1. Admin Opens Broadcast Dashboard                         │
│     GET /broadcast/                                         │
└──────────────┬──────────────────────────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────────────────────────┐
│  2. Select Encoder & Start                                  │
│     POST /broadcast/encoder/<uuid>/start/                   │
└──────────────┬──────────────────────────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────────────────────────┐
│  3. System Connects to Encoder                              │
│     - Verify encoder credentials                            │
│     - Check stream mount point                              │
│     - Start audio feed                                      │
└──────────────┬──────────────────────────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────────────────────────┐
│  4. Stream Status Updated                                   │
│     - is_connected = True                                   │
│     - is_live = True                                        │
│     - started_at = now                                      │
└──────────────┬──────────────────────────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────────────────────────┐
│  5. Notification Sent                                       │
│     - Admin notified: "Broadcast started"                   │
│     - Listeners can now tune in                             │
└─────────────────────────────────────────────────────────────┘
```

### Stopping a Broadcast

```
┌─────────────────────────────────────────────────────────────┐
│  1. Admin Clicks Stop                                       │
│     POST /broadcast/encoder/<uuid>/stop/                    │
└──────────────┬──────────────────────────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────────────────────────┐
│  2. System Stops Encoder                                    │
│     - Gracefully close connection                           │
│     - Save recording (if enabled)                           │
└──────────────┬──────────────────────────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────────────────────────┐
│  3. Status Updated                                          │
│     - is_connected = False                                  │
│     - is_live = False                                       │
│     - Record stream duration                                │
└─────────────────────────────────────────────────────────────┘
```

---

## Encoder Status View

```
┌──────────────────────────────────────────────────────────────┐
│  Encoder Status - Studio Utama                                │
│                                                               │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │  Status: 🟢 CONNECTED                                    │  │
│  │  Encoder: Icecast 2.4                                    │  │
│  │  Host: radio.kabulhaden.id:8000                          │  │
│  │  Mount: /live                                            │  │
│  │                                                          │  │
│  │  ┌──────────────┬──────────────┬──────────────┐         │  │
│  │  │ Bitrate      │ Sample Rate  │ Channels     │         │  │
│  │  │ 128 kbps     │ 44.1 kHz     │ Stereo       │         │  │
│  │  └──────────────┴──────────────┴──────────────┘         │  │
│  │                                                          │  │
│  │  ┌──────────────┬──────────────┬──────────────┐         │  │
│  │  │ Listeners    │ Peak         │ Duration     │         │  │
│  │  │ 234          │ 567          │ 02:34:15     │         │  │
│  │  └──────────────┴──────────────┴──────────────┘         │  │
│  └─────────────────────────────────────────────────────────┘  │
│                                                               │
│  [⏹ Stop Broadcast]  [🔄 Restart]  [📊 View Logs]           │
└──────────────────────────────────────────────────────────────┘
```

---

## Broadcast Services

```python
# apps/broadcast/services.py
class BroadcastService:
    def __init__(self, repository):
        self.repository = repository
    
    def start_broadcast(self, encoder_id):
        """Start broadcasting on encoder."""
        encoder = self.repository.get(encoder_id)
        
        # Connect to encoder
        connection = self._connect_to_encoder(encoder)
        
        if connection:
            encoder.is_connected = True
            encoder.save()
            
            # Create stream record
            stream = Stream.objects.create(
                station=encoder.station,
                encoder=encoder,
                name=f"Live - {timezone.now().strftime('%Y-%m-%d %H:%M')}",
                is_live=True,
                started_at=timezone.now(),
            )
            
            # Notify admins
            NotificationService.notify_stream_start(encoder.station)
            
            return stream
        
        raise ConnectionError(f"Gagal terhubung ke encoder {encoder.name}")
    
    def stop_broadcast(self, encoder_id):
        """Stop broadcasting on encoder."""
        encoder = self.repository.get(encoder_id)
        
        # Stop encoder
        self._stop_encoder(encoder)
        
        # Update status
        encoder.is_connected = False
        encoder.save()
        
        # Update stream
        stream = Stream.objects.filter(
            encoder=encoder,
            is_live=True
        ).first()
        
        if stream:
            stream.is_live = False
            stream.save()
            
            # Auto-record if enabled
            if encoder.auto_record:
                self._save_recording(stream)
        
        return stream
    
    def get_stream_status(self, encoder_id):
        """Get current stream status."""
        encoder = self.repository.get(encoder_id)
        
        return {
            'encoder': encoder.name,
            'status': encoder.status,
            'stream_url': encoder.stream_url,
            'bitrate': encoder.bitrate,
            'is_live': encoder.is_connected,
            'listeners': self._get_listener_count(encoder),
            'duration': self._get_stream_duration(encoder),
        }
```

---

## Playlist Management

### Playlist View

```
┌──────────────────────────────────────────────────────────────┐
│  Playlist Manager                                             │
│                                                               │
│  [+ Buat Playlist Baru]                                       │
│                                                               │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │ 🎵 Playlist Siang (1:45:30)                             │  │
│  │    12 tracks • Dibuat: 15 Jul 2026                      │  │
│  │    [Edit] [Hapus] [Putar]                               │  │
│  └─────────────────────────────────────────────────────────┘  │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │ 🎵 Playlist Malam (2:15:00)                             │  │
│  │    15 tracks • Dibuat: 14 Jul 2026                      │  │
│  │    [Edit] [Hapus] [Putar]                               │  │
│  └─────────────────────────────────────────────────────────┘  │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │ 🎵 Berita & Informasi (0:45:00)                         │  │
│  │    8 tracks • Dibuat: 13 Jul 2026                       │  │
│  │    [Edit] [Hapus] [Putar]                               │  │
│  └─────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────┘
```

### Add Track to Playlist

```python
class TrackAddView(LoginRequiredMixin, AdminRequiredMixin, View):
    def post(self, request, playlist_id):
        playlist = Playlist.objects.get(pk=playlist_id)
        episode_id = request.POST.get('episode_id')
        episode = Episode.objects.get(pk=episode_id)
        
        # Check if already in playlist
        if PlaylistTrack.objects.filter(playlist=playlist, episode=episode).exists():
            messages.warning(request, 'Episode sudah ada dalam playlist.')
            return redirect('broadcast:playlist_detail', pk=playlist_id)
        
        # Add to end
        last_position = playlist.tracks.count()
        PlaylistTrack.objects.create(
            playlist=playlist,
            episode=episode,
            position=last_position,
        )
        
        # Recalculate duration
        playlist.recalculate_duration()
        
        messages.success(request, f'"{episode.title}" berhasil ditambahkan ke playlist.')
        return redirect('broadcast:playlist_detail', pk=playlist_id)
```

### Reorder Tracks

```python
class TrackReorderView(LoginRequiredMixin, AdminRequiredMixin, View):
    def post(self, request, playlist_id):
        playlist = Playlist.objects.get(pk=playlist_id)
        track_ids = request.POST.getlist('track_order')
        
        for position, track_id in enumerate(track_ids):
            PlaylistTrack.objects.filter(
                playlist=playlist,
                pk=track_id
            ).update(position=position)
        
        return JsonResponse({'status': 'ok'})
```

---

## Recording Management

### Recordings List

```
┌──────────────────────────────────────────────────────────────┐
│  Rekaman                                                      │
│                                                               │
│  🔍 Search... | Filter: [All Streams ▼]                      │
│                                                               │
│  ┌───────────┬─────────────┬───────────┬─────────┬────────┐  │
│  │ Judul     │ Stream      │ Durasi    │ Size    │ Tanggal│  │
│  ├───────────┼─────────────┼───────────┼─────────┼────────┤  │
│  │ Live 07/15│ Studio A    │ 02:34:15  │ 45.2 MB │ 15 Jul │  │
│  │ Live 07/14│ Studio A    │ 01:45:22  │ 32.1 MB │ 14 Jul │  │
│  │ Live 07/13│ Studio B    │ 03:12:45  │ 58.3 MB │ 13 Jul │  │
│  └───────────┴─────────────┴───────────┴─────────┴────────┘  │
│                                                               │
│  [📥 Download] [🗑️ Hapus] [📊 Detail]                        │
└──────────────────────────────────────────────────────────────┘
```

### Recording Service

```python
class RecordingService:
    def save_recording(self, stream):
        """Save completed stream as recording."""
        recording = Recording(
            stream=stream,
            title=f"Recording - {stream.name}",
            file=stream.recording_file,
            file_size=stream.recording_file.size,
            duration=stream.duration.total_seconds(),
            recorded_at=stream.started_at,
            format='mp3',
        )
        recording.save()
        return recording
    
    def download_recording(self, recording_id):
        """Get recording file for download."""
        recording = Recording.objects.get(pk=recording_id)
        return FileResponse(
            recording.file.open('rb'),
            as_attachment=True,
            filename=f"{recording.title}.{recording.format}"
        )
```

---

## Health Check

```python
# apps/broadcast/views.py
class HealthCheckView(View):
    def get(self, request, *args, **kwargs):
        encoders = Encoder.objects.filter(is_active=True)
        healthy = all(self._check_encoder(e) for e in encoders)
        
        status = {
            'status': 'healthy' if healthy else 'degraded',
            'encoders': [
                {
                    'name': e.name,
                    'status': e.status,
                    'last_check': e.last_health_check.isoformat(),
                }
                for e in encoders
            ],
            'timestamp': timezone.now().isoformat(),
        }
        
        return JsonResponse(status, status=200 if healthy else 503)
```

---

## Broadcast Statistics

### Stats View

```
┌──────────────────────────────────────────────────────────────┐
│  Statistik Broadcast                                          │
│                                                               │
│  Minggu Ini:                                                  │
│  ┌────────────┬────────────┬────────────┬────────────┐       │
│  │ Total Jam  │ Pendengar  │ Peak       │ Recording  │       │
│  │ 120 jam    │ 12,450     │ 567        │ 45 file    │       │
│  └────────────┴────────────┴────────────┴────────────┘       │
│                                                               │
│  Grafik Pendengar (24 jam terakhir):                         │
│  600│        ╭──╮                                             │
│  500│    ╭──╯  │                                             │
│  400│   ╭╯     ╰──╮                                          │
│  300│  ╭╯         ╰──╮                                       │
│  200│──╯              ╰─────────────────────────              │
│  100│                                                          │
│     └───────────────────────────────────────────────          │
│       00  04  08  12  16  20  24                              │
└──────────────────────────────────────────────────────────────┘
```

---

## Related Documentation

- `erd.md` - Broadcast entity relationships
- `37_RADIO_MODULE_DEEP_DIVE.md` - Radio module (related)
- `31_API_ENDPOINTS_REFERENCE.md` - Broadcast API endpoints
- `15_TABLE_DESIGN.md` - Table patterns
- `16_MODAL_DESIGN.md` - Confirmation modals

---

*Last updated: 2026-07-15*
