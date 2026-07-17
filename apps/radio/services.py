import logging
from typing import Optional, Dict, Any
from django.conf import settings
from django.core.cache import cache
from django.utils import timezone
from utils.services import BaseService
from .adapters import get_adapter
from .adapters.base import NowPlayingData, ListenerData, HealthCheckData
from .repositories import (
    RadioStationRepository, RadioProviderRepository, NowPlayingCacheRepository,
    ListenerStatisticRepository, StreamHealthRepository, LiveSessionRepository,
)
from .models import (
    RadioStation, RadioProvider, NowPlayingCache,
    ListenerStatistic, StreamHealth, LiveSession
)
from utils.choices import StreamStatus, StreamHealthStatus

logger = logging.getLogger('radio')

CACHE_TTL_NOW_PLAYING = getattr(settings, 'RADIO_CACHE_TTL_NOW_PLAYING', 15)
CACHE_TTL_LISTENER = getattr(settings, 'RADIO_CACHE_TTL_LISTENER', 30)
CACHE_TTL_HEALTH = getattr(settings, 'RADIO_CACHE_TTL_HEALTH', 60)


class RadioStationService(BaseService[RadioStationRepository]):
    def __init__(self):
        super().__init__(RadioStationRepository())

    def get_active_stations(self):
        return self.repository.get_active_stations()

    def get_primary_station(self):
        return self.repository.get_primary_station()

    def create_station(self, **kwargs):
        return self.repository.create(**kwargs)

    def update_station(self, station_id, **kwargs):
        station = self.repository.get_by_id(station_id)
        if station:
            return self.repository.update(station, **kwargs)
        return None

    def toggle_active(self, station_id):
        station = self.repository.get_by_id(station_id)
        if station:
            station.is_active = not station.is_active
            station.save(update_fields=['is_active'])
            return station
        return None


class RadioProviderService(BaseService[RadioProviderRepository]):
    def __init__(self):
        super().__init__(RadioProviderRepository())

    def get_for_station(self, station_id):
        return self.repository.get_for_station(station_id)

    def get_primary_provider(self, station_id):
        return self.repository.get_primary_provider(station_id)

    def create_provider(self, **kwargs):
        return self.repository.create(**kwargs)

    def update_provider(self, provider_id, **kwargs):
        provider = self.repository.get_by_id(provider_id)
        if provider:
            return self.repository.update(provider, **kwargs)
        return None

    def get_adapter_instance(self, provider: RadioProvider):
        adapter_class = get_adapter(provider.provider_type)
        return adapter_class(
            api_url=provider.api_url,
            stream_url=provider.stream_url,
            metadata_url=provider.metadata_url,
            listener_url=provider.listener_url,
            healthcheck_url=provider.healthcheck_url,
            username=provider.username,
            password=provider.password,
            timeout=provider.timeout,
        )

    def toggle_active(self, provider_id):
        provider = self.repository.get_by_id(provider_id)
        if provider:
            provider.active = not provider.active
            provider.save(update_fields=['active'])
            return provider
        return None


class NowPlayingService(BaseService[NowPlayingCacheRepository]):
    def __init__(self):
        super().__init__(NowPlayingCacheRepository())

    def get_now_playing(self, station_id) -> Optional[NowPlayingCache]:
        cache_key = f"radio:now_playing:{station_id}"
        cached = cache.get(cache_key)
        if cached:
            return cached
        np_cache = self.repository.get_for_station(station_id)
        if np_cache:
            cache.set(cache_key, np_cache, CACHE_TTL_NOW_PLAYING)
        return np_cache

    def refresh_from_provider(self, station_id) -> Optional[NowPlayingCache]:
        provider_svc = RadioProviderService()
        provider = provider_svc.get_primary_provider(station_id)
        if not provider:
            return self._set_offline(station_id, None)

        try:
            adapter = provider_svc.get_adapter_instance(provider)
            data = adapter.get_now_playing()
            return self._update_cache(station_id, provider, data)
        except Exception as e:
            logger.error(f"Error refreshing now playing for station {station_id}: {e}")
            return self._set_offline(station_id, provider)

    def refresh_all(self):
        station_svc = RadioStationService()
        for station in station_svc.get_active_stations():
            self.refresh_from_provider(station.pk)

    def _update_cache(self, station_id, provider, data: NowPlayingData) -> NowPlayingCache:
        np_cache, _ = NowPlayingCache.objects.update_or_create(
            station_id=station_id,
            defaults={
                'provider': provider,
                'song_title': data.song_title,
                'artist': data.artist,
                'album': data.album,
                'artwork': data.artwork,
                'duration': data.duration,
                'elapsed': data.elapsed,
                'started_at': data.started_at,
                'ends_at': data.ends_at,
                'raw_response': data.raw_response,
                'stream_status': data.stream_status,
            }
        )
        cache_key = f"radio:now_playing:{station_id}"
        cache.set(cache_key, np_cache, CACHE_TTL_NOW_PLAYING)
        return np_cache

    def _set_offline(self, station_id, provider) -> NowPlayingCache:
        np_cache, _ = NowPlayingCache.objects.update_or_create(
            station_id=station_id,
            defaults={
                'provider': provider,
                'song_title': '',
                'artist': '',
                'album': '',
                'artwork': '',
                'duration': 0,
                'elapsed': 0,
                'stream_status': StreamStatus.OFFLINE,
                'raw_response': {},
            }
        )
        cache_key = f"radio:now_playing:{station_id}"
        cache.delete(cache_key)
        return np_cache


class ListenerService(BaseService[ListenerStatisticRepository]):
    def __init__(self):
        super().__init__(ListenerStatisticRepository())

    def get_current(self, station_id) -> Optional[ListenerStatistic]:
        cache_key = f"radio:listeners:{station_id}"
        cached = cache.get(cache_key)
        if cached:
            return cached
        stat = self.repository.get_latest(station_id)
        if stat:
            cache.set(cache_key, stat, CACHE_TTL_LISTENER)
        return stat

    def refresh_from_provider(self, station_id) -> Optional[ListenerStatistic]:
        provider_svc = RadioProviderService()
        provider = provider_svc.get_primary_provider(station_id)
        if not provider:
            return None

        try:
            adapter = provider_svc.get_adapter_instance(provider)
            data = adapter.get_listener_count()
            stat = ListenerStatistic.objects.create(
                station_id=station_id,
                provider=provider,
                current_listeners=data.current_listeners,
                peak_listeners=data.peak_listeners,
            )
            cache_key = f"radio:listeners:{station_id}"
            cache.set(cache_key, stat, CACHE_TTL_LISTENER)
            return stat
        except Exception as e:
            logger.error(f"Error refreshing listeners for station {station_id}: {e}")
            return None

    def refresh_all(self):
        station_svc = RadioStationService()
        for station in station_svc.get_active_stations():
            self.refresh_from_provider(station.pk)

    def get_hourly_stats(self, station_id, hours=24):
        from django.utils import timezone
        from datetime import timedelta
        from django.db.models import Avg, Max
        cutoff = timezone.now() - timedelta(hours=hours)
        return ListenerStatistic.objects.filter(
            station_id=station_id, recorded_at__gte=cutoff
        ).aggregate(
            avg_listeners=Avg('current_listeners'),
            peak=Max('peak_listeners'),
        )

    def export_csv(self, station_id, hours=168):
        import csv
        import io
        from django.utils import timezone
        from datetime import timedelta
        cutoff = timezone.now() - timedelta(hours=hours)
        stats = ListenerStatistic.objects.filter(
            station_id=station_id, recorded_at__gte=cutoff
        ).order_by('recorded_at')

        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['Waktu', 'Current Listeners', 'Peak Listeners'])
        for stat in stats:
            writer.writerow([
                stat.recorded_at.strftime('%Y-%m-%d %H:%M:%S'),
                stat.current_listeners,
                stat.peak_listeners,
            ])
        return output.getvalue()

    def export_excel(self, station_id, hours=168):
        from django.utils import timezone
        from datetime import timedelta
        try:
            import openpyxl
        except ImportError:
            return None

        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = 'Listener Statistics'
        ws.append(['Waktu', 'Current Listeners', 'Peak Listeners'])

        cutoff = timezone.now() - timedelta(hours=hours)
        stats = ListenerStatistic.objects.filter(
            station_id=station_id, recorded_at__gte=cutoff
        ).order_by('recorded_at')

        for stat in stats:
            ws.append([
                stat.recorded_at.strftime('%Y-%m-%d %H:%M:%S'),
                stat.current_listeners,
                stat.peak_listeners,
            ])

        import io
        output = io.BytesIO()
        wb.save(output)
        output.seek(0)
        return output.getvalue()


class StreamHealthService(BaseService[StreamHealthRepository]):
    def __init__(self):
        super().__init__(StreamHealthRepository())

    def get_latest(self, station_id):
        return self.repository.get_latest(station_id)

    def refresh_from_provider(self, station_id) -> Optional[StreamHealth]:
        provider_svc = RadioProviderService()
        provider = provider_svc.get_primary_provider(station_id)
        if not provider:
            return None

        try:
            adapter = provider_svc.get_adapter_instance(provider)
            data = adapter.check_health()
            health = StreamHealth.objects.create(
                station_id=station_id,
                provider=provider,
                response_time=data.response_time,
                http_status=data.http_status,
                provider_status=data.provider_status,
                stream_bitrate=data.stream_bitrate,
                stream_format=data.stream_format,
                error_message=data.error_message,
            )
            cache_key = f"radio:health:{station_id}"
            cache.set(cache_key, health, CACHE_TTL_HEALTH)
            return health
        except Exception as e:
            logger.error(f"Error checking health for station {station_id}: {e}")
            return None

    def refresh_all(self):
        station_svc = RadioStationService()
        for station in station_svc.get_active_stations():
            self.refresh_from_provider(station.pk)

    def get_failures(self, station_id):
        return self.repository.get_failures(station_id)

    def get_health_history(self, station_id, limit=50):
        return self.repository.get_for_station(station_id, limit)


class LiveSessionService(BaseService[LiveSessionRepository]):
    def __init__(self):
        super().__init__(LiveSessionRepository())

    def get_active(self, station_id):
        return self.repository.get_active(station_id)

    def get_history(self, station_id, limit=20):
        return self.repository.get_for_station(station_id, limit)

    def start_session(self, station_id, program='', host=''):
        existing = self.get_active(station_id)
        if existing:
            self.end_session(existing.pk)
        return self.repository.create(
            station_id=station_id, program=program, host=host
        )

    def end_session(self, session_id):
        return self.repository.close_session(session_id)


class FallbackService:
    """Handles fallback stream logic when primary provider fails."""

    def __init__(self):
        self.provider_svc = RadioProviderService()

    def get_fallback_stream(self, station_id) -> Optional[str]:
        providers = self.provider_svc.get_for_station(station_id)
        for provider in providers:
            if provider.backup_stream_url:
                return provider.backup_stream_url
        return None

    def get_available_stream(self, station_id) -> Optional[str]:
        providers = self.provider_svc.get_for_station(station_id)
        for provider in providers:
            adapter = self.provider_svc.get_adapter_instance(provider)
            health = adapter.check_health()
            if health.provider_status in ['HEALTHY', 'DEGRADED']:
                return provider.stream_url
        fallback = self.get_fallback_stream(station_id)
        return fallback


class MetadataService:
    """Unified metadata retrieval across all providers."""

    def __init__(self):
        self.np_svc = NowPlayingService()

    def get_track_info(self, station_id) -> Dict[str, Any]:
        np_cache = self.np_svc.get_now_playing(station_id)
        if not np_cache:
            return {'song_title': '', 'artist': '', 'album': '', 'artwork': ''}
        return {
            'song_title': np_cache.song_title,
            'artist': np_cache.artist,
            'album': np_cache.album,
            'artwork': np_cache.artwork,
            'duration': np_cache.duration,
            'elapsed': np_cache.elapsed,
            'stream_status': np_cache.stream_status,
            'progress_percent': np_cache.progress_percent,
        }


class ArtworkService:
    """Artwork retrieval and caching."""

    def get_artwork(self, station_id) -> str:
        np_cache = NowPlayingCache.objects.filter(station_id=station_id).first()
        if np_cache and np_cache.artwork:
            return np_cache.artwork
        return ''


class PlayerService:
    """Manages player configuration and stream resolution."""

    def __init__(self):
        self.station_svc = RadioStationService()
        self.fallback_svc = FallbackService()

    def get_player_config(self) -> Dict[str, Any]:
        station = self.station_svc.get_primary_station()
        if not station:
            return {
                'station_name': '',
                'stream_url': '',
                'backup_stream_url': '',
                'default_volume': 80,
                'autoplay': False,
                'sticky_player': False,
                'logo': '',
                'is_active': False,
            }
        provider = station.primary_provider
        stream_url = self.fallback_svc.get_available_stream(station.pk) or (
            provider.stream_url if provider else ''
        )
        return {
            'station_name': station.station_name,
            'stream_url': stream_url,
            'backup_stream_url': provider.backup_stream_url if provider else '',
            'default_volume': station.default_volume,
            'autoplay': station.autoplay,
            'sticky_player': station.sticky_player,
            'logo': station.logo.url if station.logo else '',
            'is_active': station.is_active,
        }

    def update_volume(self, station_id, volume: int) -> Optional[RadioStation]:
        if volume < 0 or volume > 100:
            return None
        return self.station_svc.update_station(station_id, default_volume=volume)

    def update_autoplay(self, station_id, autoplay: bool) -> Optional[RadioStation]:
        return self.station_svc.update_station(station_id, autoplay=autoplay)

    def update_sticky(self, station_id, sticky: bool) -> Optional[RadioStation]:
        return self.station_svc.update_station(station_id, sticky_player=sticky)


class BroadcastIntegrationService:
    """Integrates broadcast module data into radio module for display on radio dashboard."""

    def __init__(self):
        self.live_svc = LiveSessionService()

    def get_current_program(self, station_id) -> Dict[str, Any]:
        from django.utils import timezone as tz
        session = self.live_svc.get_active(station_id)
        if session:
            return {
                'program': session.program,
                'host': session.host,
                'started_at': session.started_at,
                'duration': session.duration_display,
            }
        return self._get_scheduled_program()

    def _get_scheduled_program(self) -> Dict[str, Any]:
        try:
            from apps.broadcast.models import Schedule, BroadcastSession
            from apps.broadcast.services import BroadcastService, ScheduleService
            from datetime import time as time_type
            from django.utils import timezone as tz

            now = tz.now()
            current_time = now.time()
            day_map = {
                0: 'MON', 1: 'TUE', 2: 'WED',
                3: 'THU', 4: 'FRI', 5: 'SAT', 6: 'SUN',
            }
            current_day = day_map[now.weekday()]

            schedule_svc = ScheduleService()
            today_schedules = schedule_svc.get_for_day(current_day)
            for sched in today_schedules:
                if sched.start_time <= current_time <= sched.end_time:
                    host_member = sched.program.host_members.filter(is_lead=True).select_related('host').first()
                    host_name = host_member.host.display_name if host_member else ''
                    return {
                        'program': sched.program.title,
                        'host': host_name,
                        'started_at': None,
                        'duration': f"{sched.start_time.strftime('%H:%M')}-{sched.end_time.strftime('%H:%M')}",
                    }
        except Exception:
            pass
        return {'program': '', 'host': '', 'started_at': None, 'duration': ''}

    def get_program_info_for_station(self, station_id) -> Dict[str, Any]:
        session = self.live_svc.get_active(station_id)
        if session:
            return {
                'has_session': True,
                'program': session.program,
                'host': session.host,
                'started_at': session.started_at.isoformat() if session.started_at else None,
                'duration': session.duration_display,
            }
        scheduled = self._get_scheduled_program()
        if scheduled['program']:
            return {
                'has_session': False,
                'program': scheduled['program'],
                'host': scheduled['host'],
                'started_at': None,
                'duration': scheduled['duration'],
            }
        return {
            'has_session': False,
            'program': '',
            'host': '',
            'started_at': None,
            'duration': '',
        }

    def sync_live_session(self, station_id, program: str = '', host: str = ''):
        return self.live_svc.start_session(station_id, program=program, host=host)
