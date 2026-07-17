from django.contrib import admin
from .models import (
    RadioStation, RadioProvider, NowPlayingCache,
    ListenerStatistic, StreamHealth, LiveSession
)


@admin.register(RadioStation)
class RadioStationAdmin(admin.ModelAdmin):
    list_display = ('station_name', 'genre', 'is_active', 'default_volume', 'created_at')
    list_filter = ('is_active', 'genre')
    search_fields = ('station_name',)


@admin.register(RadioProvider)
class RadioProviderAdmin(admin.ModelAdmin):
    list_display = ('provider_name', 'station', 'provider_type', 'active', 'timeout')
    list_filter = ('provider_type', 'active')
    search_fields = ('provider_name',)
    readonly_fields = ('password',)


@admin.register(NowPlayingCache)
class NowPlayingCacheAdmin(admin.ModelAdmin):
    list_display = ('station', 'song_title', 'artist', 'stream_status', 'updated_at')
    list_filter = ('stream_status',)


@admin.register(ListenerStatistic)
class ListenerStatisticAdmin(admin.ModelAdmin):
    list_display = ('station', 'current_listeners', 'peak_listeners', 'recorded_at')
    list_filter = ('station',)


@admin.register(StreamHealth)
class StreamHealthAdmin(admin.ModelAdmin):
    list_display = ('station', 'provider_status', 'response_time', 'http_status', 'last_checked')
    list_filter = ('provider_status',)


@admin.register(LiveSession)
class LiveSessionAdmin(admin.ModelAdmin):
    list_display = ('station', 'program', 'host', 'started_at', 'ended_at', 'listener_peak')
    list_filter = ('station',)
