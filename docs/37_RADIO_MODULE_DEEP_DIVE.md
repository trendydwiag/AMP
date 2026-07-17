# 37. Radio Module Deep Dive

## Overview

This guide provides an in-depth look at the Radio module in Kabulhaden CMS, covering stations, programs, schedules, episodes, play queue, and stream management.

---

## Radio Module Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Radio Module                              │
│                                                              │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │  Station     │  │  Program    │  │  Schedule   │         │
│  │  (stasiun)   │──│  (program)  │──│  (jadwal)   │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
│         │                │                │                   │
│         ▼                ▼                ▼                   │
│  ┌─────────────────────────────────────────────────────────┐│
│  │                    Episode                               ││
│  │  (linked to Program, appears in Schedule)                ││
│  └─────────────────────────────────────────────────────────┘│
│         │                                                    │
│         ▼                                                    │
│  ┌─────────────────────────────────────────────────────────┐│
│  │                    Play Queue                            ││
│  │  (ordered list of tracks/episodes to play)              ││
│  └─────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────┘
```

---

## Data Models

### Station

```python
# apps/radio/models.py
class Station(UUIDPrimaryKeyMixin, TimeStampMixin):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    stream_url = models.URLField(help_text='URL streaming audio')
    is_active = models.BooleanField(default=True)
    logo = models.ImageField(upload_to='radio/stations/', blank=True, null=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    @property
    def current_program(self):
        now = timezone.now()
        current_time = now.time()
        day_of_week = now.weekday()
        
        schedule = Schedule.objects.filter(
            station=self,
            day_of_week=day_of_week,
            start_time__lte=current_time,
            end_time__gt=current_time,
        ).first()
        
        return schedule.program if schedule else None
```

### Program

```python
class Program(UUIDPrimaryKeyMixin, TimeStampMixin):
    station = models.ForeignKey(Station, on_delete=models.CASCADE, related_name='programs')
    title = models.CharField(max_length=200)
    slug = models.SlugField()
    description = models.TextField(blank=True)
    genre = models.CharField(max_length=50, choices=Genre.choices, blank=True)
    host = models.CharField(max_length=100, blank=True)
    duration_minutes = models.IntegerField(default=60)
    is_active = models.BooleanField(default=True)
    image = models.ImageField(upload_to='radio/programs/', blank=True, null=True)
    
    class Meta:
        ordering = ['title']
        unique_together = ['station', 'slug']
    
    def __str__(self):
        return f"{self.station.name} - {self.title}"
```

### Schedule

```python
class Schedule(UUIDPrimaryKeyMixin, TimeStampMixin):
    station = models.ForeignKey(Station, on_delete=models.CASCADE, related_name='schedules')
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='schedules')
    day_of_week = models.IntegerField(choices=DayOfWeek.choices)
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['day_of_week', 'start_time']
    
    def __str__(self):
        return f"{self.program.title} - {self.get_day_of_week_display()} {self.start_time}"
    
    @property
    def duration_minutes(self):
        start = datetime.combine(datetime.today(), self.start_time)
        end = datetime.combine(datetime.today(), self.end_time)
        return int((end - start).total_seconds() / 60)
    
    @property
    def is_current(self):
        now = timezone.now()
        return (
            now.weekday() == self.day_of_week and
            self.start_time <= now.time() < self.end_time
        )
```

### Episode

```python
class Episode(UUIDPrimaryKeyMixin, TimeStampMixin):
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='episodes')
    title = models.CharField(max_length=200)
    slug = models.SlugField()
    description = models.TextField(blank=True)
    audio_file = models.FileField(upload_to='radio/episodes/')
    duration = models.FloatField(help_text='Duration in seconds')
    episode_number = models.IntegerField(null=True, blank=True)
    season_number = models.IntegerField(default=1)
    air_date = models.DateField(null=True, blank=True)
    is_published = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-season_number', '-episode_number']
        unique_together = ['program', 'season_number', 'episode_number']
    
    def __str__(self):
        return f"{self.program.title} - S{self.season_number}E{self.episode_number}: {self.title}"
    
    @property
    def duration_display(self):
        minutes = int(self.duration // 60)
        seconds = int(self.duration % 60)
        return f"{minutes:02d}:{seconds:02d}"
```

### Play Queue

```python
class PlayQueue(UUIDPrimaryKeyMixin, TimeStampMixin):
    station = models.OneToOneField(Station, on_delete=models.CASCADE, related_name='play_queue')
    
    class Meta:
        verbose_name_plural = 'Play queues'
    
    @property
    def current_track(self):
        return self.tracks.filter(is_playing=True).first()
    
    @property
    def next_track(self):
        current = self.current_track
        if current:
            return self.tracks.filter(position__gt=current.position).first()
        return self.tracks.filter(is_playing=False).first()


class QueueTrack(UUIDPrimaryKeyMixin):
    queue = models.ForeignKey(PlayQueue, on_delete=models.CASCADE, related_name='tracks')
    episode = models.ForeignKey(Episode, on_delete=models.CASCADE)
    position = models.IntegerField(default=0)
    is_playing = models.BooleanField(default=False)
    added_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['position']
```

---

## Schedule View (Weekly Grid)

### Weekly Schedule Display

```
┌──────────────────────────────────────────────────────────────────────────────┐
│  Jadwal Radio - Studio Utama                                                 │
│                                                                              │
│       │ Senin    │ Selasa   │ Rabu    │ Kamis    │ Jumat    │ Sabtu  │ Minggu│
│  ─────┼──────────┼──────────┼─────────┼──────────┼──────────┼────────┼───────│
│  06:00│ Berita   │ Berita   │ Berita  │ Berita   │ Berita   │ Musik  │ Libur │
│  08:00│ Musik    │ Musik    │ Musik   │ Musik    │ Musik    │ Musik  │ Libur │
│  10:00│ Bicara   │ Bicara   │ Bicara  │ Bicara   │ Bicara   │ Anak   │ Libur │
│  12:00│ Berita   │ Berita   │ Berita  │ Berita   │ Berita   │ Anak   │ Libur │
│  14:00│ Musik    │ Musik    │ Musik   │ Musik    │ Musik    │ Musik  │ Libur │
│  16:00│ Olahraga │ Budaya   │ Pendid. │ Keseh.  │ Agama    │ Musik  │ Libur │
│  18:00│ Berita   │ Berita   │ Berita  │ Berita   │ Berita   │ Musik  │ Libur │
│  20:00│ Malam    │ Malam    │ Malam   │ Malam    │ Malam    │ Musik  │ Libur │
│  22:00│ Musik    │ Musik    │ Musik   │ Musik    │ Musik    │ Musik  │ Musik │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## Radio Services

```python
# apps/radio/services.py
class RadioService:
    def __init__(self, repository):
        self.repository = repository
    
    def get_current_schedule(self, station):
        """Get currently airing program."""
        now = timezone.now()
        return Schedule.objects.filter(
            station=station,
            day_of_week=now.weekday(),
            start_time__lte=now.time(),
            end_time__gt=now.time(),
        ).first()
    
    def get_next_program(self, station):
        """Get next scheduled program."""
        now = timezone.now()
        current_time = now.time()
        day_of_week = now.weekday()
        
        # Try to find next program today
        next_today = Schedule.objects.filter(
            station=station,
            day_of_week=day_of_week,
            start_time__gt=current_time,
        ).order_by('start_time').first()
        
        if next_today:
            return next_today
        
        # Otherwise, first program tomorrow
        tomorrow = (day_of_week + 1) % 7
        return Schedule.objects.filter(
            station=station,
            day_of_week=tomorrow,
        ).order_by('start_time').first()
    
    def add_to_queue(self, station, episode):
        """Add episode to play queue."""
        queue, _ = PlayQueue.objects.get_or_create(station=station)
        last_position = queue.tracks.count()
        
        QueueTrack.objects.create(
            queue=queue,
            episode=episode,
            position=last_position,
        )
    
    def reorder_queue(self, station, track_ids):
        """Reorder tracks in queue."""
        queue = PlayQueue.objects.get(station=station)
        for position, track_id in enumerate(track_ids):
            queue.tracks.filter(pk=track_id).update(position=position)
    
    def play_next(self, station):
        """Skip to next track in queue."""
        queue = PlayQueue.objects.get(station=station)
        current = queue.current_track
        
        if current:
            current.is_playing = False
            current.save()
        
        next_track = queue.next_track
        if next_track:
            next_track.is_playing = True
            next_track.save()
        
        return next_track
```

---

## Radio Dashboard

### Dashboard View

```
┌──────────────────────────────────────────────────────────────┐
│  Radio Dashboard                                              │
│                                                               │
│  ┌─────────────────────┐  ┌─────────────────────┐           │
│  │ Sedang Tayang        │  │ Selanjutnya          │           │
│  │ 🎵 Musik Pagi        │  │ 📰 Berita Siang      │           │
│  │ 08:00 - 10:00        │  │ 12:00 - 14:00        │           │
│  │ Status: 🔴 LIVE      │  │ Tersisa: 2j 15m      │           │
│  └─────────────────────┘  └─────────────────────┘           │
│                                                               │
│  ┌─────────────────────┐  ┌─────────────────────┐           │
│  │ Antrian Play         │  │ Status Stream        │           │
│  │ 1. Episode 42 ✅     │  │ Encoder: Connected   │           │
│  │ 2. Episode 43 ⏳     │  │ Bitrate: 128 kbps    │           │
│  │ 3. Episode 44 ⏳     │  │ Listeners: 234       │           │
│  └─────────────────────┘  └─────────────────────┘           │
│                                                               │
│  Statistik Minggu Ini:                                        │
│  Total Pendengar: 12,450                                      │
│  Rata-rata per Jam: 245                                       │
│  Peak: 567 (Senin 18:00)                                     │
└──────────────────────────────────────────────────────────────┘
```

---

## Management Commands

### Refresh All Radio Data

```python
# apps/radio/management/commands/refresh_radio_all.py
class Command(BaseCommand):
    help = 'Refresh all radio data (schedules, now playing, listeners)'
    
    def handle(self, *args, **options):
        # Update now playing
        self.stdout.write('Updating now playing...')
        update_now_playing()
        
        # Update listener counts
        self.stdout.write('Updating listener counts...')
        update_listener_counts()
        
        # Check stream health
        self.stdout.write('Checking stream health...')
        check_stream_health()
        
        self.stdout.write(self.style.SUCCESS('Radio data refreshed'))
```

### Check Stream Health

```python
# apps/radio/management/commands/check_stream_health.py
class Command(BaseCommand):
    help = 'Check health of all streams'
    
    def handle(self, *args, **options):
        stations = Station.objects.filter(is_active=True)
        
        for station in stations:
            is_healthy = self._check_stream(station.stream_url)
            status = '✓ Healthy' if is_healthy else '✗ Unhealthy'
            self.stdout.write(f'{station.name}: {status}')
            
            if not is_healthy:
                # Send notification to admins
                NotificationService.notify_stream_error(
                    station,
                    f'Stream {station.name} tidak merespons'
                )
```

---

## Stream Status API

```python
# apps/radio/views.py
class StreamStatusAPI(View):
    """JSON API for stream status (used by players)."""
    
    def get(self, request, *args, **kwargs):
        stations = Station.objects.filter(is_active=True)
        data = []
        
        for station in stations:
            current = station.current_program
            data.append({
                'id': str(station.pk),
                'name': station.name,
                'stream_url': station.stream_url,
                'is_live': self._is_streaming(station),
                'current_program': {
                    'title': current.program.title if current else None,
                    'host': current.program.host if current else None,
                    'start_time': current.start_time.strftime('%H:%M') if current else None,
                    'end_time': current.end_time.strftime('%H:%M') if current else None,
                } if current else None,
                'listeners': self._get_listener_count(station),
            })
        
        return JsonResponse({'stations': data})
```

---

## Related Documentation

- `erd.md` - Radio entity relationships
- `31_API_ENDPOINTS_REFERENCE.md` - Radio API endpoints
- `22_ANIMATION_GUIDE.md` - Now-playing animations
- `06_USER_FLOWS.md` - Radio management flows

---

*Last updated: 2026-07-15*
