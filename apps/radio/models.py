import uuid
from django.db import models
from django.conf import settings
from utils.mixins import UUIDPrimaryKeyMixin, TimeStampedModel
from utils.choices import (
    RadioProviderType, StreamStatus, StreamHealthStatus, MetadataFormat
)


class RadioStation(UUIDPrimaryKeyMixin, TimeStampedModel):
    station_name = models.CharField(max_length=200)
    station_description = models.TextField(blank=True, default='')
    logo = models.ImageField(upload_to='radio/station/', blank=True, null=True)
    banner = models.ImageField(upload_to='radio/station/', blank=True, null=True)
    partner = models.ForeignKey(
        'platform.Partner', on_delete=models.CASCADE,
        null=True, blank=True, related_name='radio_stations',
        help_text="Partner yang memiliki stasiun radio ini."
    )
    timezone = models.CharField(max_length=50, default='Asia/Jakarta')
    country = models.CharField(max_length=100, blank=True, default='Indonesia')
    language = models.CharField(max_length=10, default='id')
    genre = models.CharField(max_length=100, blank=True, default='')
    website = models.URLField(max_length=500, blank=True, default='')
    default_volume = models.PositiveIntegerField(default=80, help_text='Volume default player (0-100).')
    autoplay = models.BooleanField(default=False)
    sticky_player = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Radio Station'
        verbose_name_plural = 'Radio Stations'
        ordering = ['station_name']

    def __str__(self) -> str:
        return self.station_name

    @property
    def primary_provider(self):
        return self.providers.filter(active=True).first()


class RadioProvider(UUIDPrimaryKeyMixin, TimeStampedModel):
    station = models.ForeignKey(
        RadioStation, on_delete=models.CASCADE,
        related_name='providers'
    )
    provider_name = models.CharField(max_length=200)
    provider_type = models.CharField(
        max_length=20, choices=RadioProviderType.choices,
        default=RadioProviderType.ICECAST
    )
    api_url = models.URLField(max_length=500, blank=True, default='')
    stream_url = models.URLField(max_length=500)
    backup_stream_url = models.URLField(max_length=500, blank=True, default='')
    metadata_url = models.URLField(max_length=500, blank=True, default='')
    listener_url = models.URLField(max_length=500, blank=True, default='')
    healthcheck_url = models.URLField(max_length=500, blank=True, default='')
    username = models.CharField(max_length=200, blank=True, default='')
    password = models.CharField(max_length=500, blank=True, default='')
    timeout = models.PositiveIntegerField(default=10, help_text='Request timeout in seconds.')
    active = models.BooleanField(default=True)
    metadata_format = models.CharField(
        max_length=10, choices=MetadataFormat.choices,
        default=MetadataFormat.JSON
    )

    class Meta:
        verbose_name = 'Radio Provider'
        verbose_name_plural = 'Radio Providers'
        ordering = ['provider_name']

    def __str__(self) -> str:
        return f"{self.provider_name} ({self.get_provider_type_display()})"

    @property
    def masked_password(self) -> str:
        if self.password:
            return '*' * 8
        return ''

    def get_connection_url(self) -> str:
        if self.username and self.password:
            scheme = 'http://'
            url = self.stream_url.replace('http://', '').replace('https://', '')
            return f"{scheme}{self.username}:{self.password}@{url}"
        return self.stream_url


class NowPlayingCache(UUIDPrimaryKeyMixin, TimeStampedModel):
    station = models.OneToOneField(
        RadioStation, on_delete=models.CASCADE,
        related_name='now_playing'
    )
    provider = models.ForeignKey(
        RadioProvider, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='now_playing'
    )
    song_title = models.CharField(max_length=500, blank=True, default='')
    artist = models.CharField(max_length=500, blank=True, default='')
    album = models.CharField(max_length=500, blank=True, default='')
    artwork = models.URLField(max_length=1000, blank=True, default='')
    duration = models.PositiveIntegerField(default=0, help_text='Duration in seconds.')
    elapsed = models.PositiveIntegerField(default=0, help_text='Elapsed time in seconds.')
    started_at = models.DateTimeField(null=True, blank=True)
    ends_at = models.DateTimeField(null=True, blank=True)
    raw_response = models.JSONField(default=dict, blank=True)
    stream_status = models.CharField(
        max_length=20, choices=StreamStatus.choices,
        default=StreamStatus.UNKNOWN
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Now Playing Cache'
        verbose_name_plural = 'Now Playing Cache'

    def __str__(self) -> str:
        if self.artist and self.song_title:
            return f"{self.artist} - {self.song_title}"
        return f"{self.station.station_name} - No Track"

    @property
    def is_online(self) -> bool:
        return self.stream_status == StreamStatus.ONLINE

    @property
    def progress_percent(self) -> int:
        if self.duration and self.duration > 0:
            return min(int((self.elapsed / self.duration) * 100), 100)
        return 0


class ListenerStatistic(UUIDPrimaryKeyMixin, TimeStampedModel):
    station = models.ForeignKey(
        RadioStation, on_delete=models.CASCADE,
        related_name='listener_stats'
    )
    provider = models.ForeignKey(
        RadioProvider, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='listener_stats'
    )
    current_listeners = models.PositiveIntegerField(default=0)
    peak_listeners = models.PositiveIntegerField(default=0)
    recorded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Listener Statistic'
        verbose_name_plural = 'Listener Statistics'
        ordering = ['-recorded_at']

    def __str__(self) -> str:
        return f"{self.station.station_name} - {self.current_listeners} listeners @ {self.recorded_at}"


class StreamHealth(UUIDPrimaryKeyMixin, TimeStampedModel):
    station = models.ForeignKey(
        RadioStation, on_delete=models.CASCADE,
        related_name='health_checks'
    )
    provider = models.ForeignKey(
        RadioProvider, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='health_checks'
    )
    response_time = models.FloatField(default=0, help_text='Response time in milliseconds.')
    http_status = models.PositiveIntegerField(default=0)
    provider_status = models.CharField(
        max_length=20, choices=StreamHealthStatus.choices,
        default=StreamHealthStatus.DOWN
    )
    stream_bitrate = models.PositiveIntegerField(default=0, help_text='Bitrate in kbps.')
    stream_format = models.CharField(max_length=50, blank=True, default='')
    error_message = models.TextField(blank=True, default='')
    last_checked = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Stream Health'
        verbose_name_plural = 'Stream Health Checks'
        ordering = ['-last_checked']

    def __str__(self) -> str:
        return f"{self.station.station_name} - {self.get_provider_status_display()} @ {self.last_checked}"


class LiveSession(UUIDPrimaryKeyMixin, TimeStampedModel):
    station = models.ForeignKey(
        RadioStation, on_delete=models.CASCADE,
        related_name='live_sessions'
    )
    program = models.CharField(max_length=200, blank=True, default='')
    host = models.CharField(max_length=200, blank=True, default='')
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    listener_peak = models.PositiveIntegerField(default=0)
    average_listeners = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = 'Live Session'
        verbose_name_plural = 'Live Sessions'
        ordering = ['-started_at']

    def __str__(self) -> str:
        return f"{self.program} ({self.host}) @ {self.started_at}"

    @property
    def is_active(self) -> bool:
        return self.ended_at is None

    @property
    def duration_display(self) -> str:
        from django.utils import timezone
        end = self.ended_at or timezone.now()
        delta = end - self.started_at
        hours, remainder = divmod(int(delta.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        if hours:
            return f"{hours}j {minutes}m"
        return f"{minutes}m {seconds}s"
