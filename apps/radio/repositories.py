from typing import Optional, List
from utils.repositories import BaseRepository
from .models import (
    RadioStation, RadioProvider, NowPlayingCache,
    ListenerStatistic, StreamHealth, LiveSession
)


class RadioStationRepository(BaseRepository):
    model = RadioStation

    def get_active_stations(self):
        return self.model.objects.filter(is_active=True)

    def get_primary_station(self):
        return self.model.objects.filter(is_active=True).first()


class RadioProviderRepository(BaseRepository):
    model = RadioProvider

    def get_active_providers(self):
        return self.model.objects.filter(active=True)

    def get_for_station(self, station_id):
        return self.model.objects.filter(station_id=station_id, active=True)

    def get_primary_provider(self, station_id):
        return self.model.objects.filter(station_id=station_id, active=True).first()


class NowPlayingCacheRepository(BaseRepository):
    model = NowPlayingCache

    def get_for_station(self, station_id) -> Optional[NowPlayingCache]:
        try:
            return self.model.objects.get(station_id=station_id)
        except self.model.DoesNotExist:
            return None

    def get_or_none(self, station_id) -> Optional[NowPlayingCache]:
        return self.get_for_station(station_id)


class ListenerStatisticRepository(BaseRepository):
    model = ListenerStatistic

    def get_for_station(self, station_id, limit: int = 100):
        return list(self.model.objects.filter(station_id=station_id)[:limit])

    def get_recent(self, station_id, hours: int = 24):
        from django.utils import timezone
        from datetime import timedelta
        cutoff = timezone.now() - timedelta(hours=hours)
        return list(self.model.objects.filter(
            station_id=station_id, recorded_at__gte=cutoff
        ).order_by('-recorded_at'))

    def get_latest(self, station_id):
        return self.model.objects.filter(station_id=station_id).order_by('-recorded_at').first()


class StreamHealthRepository(BaseRepository):
    model = StreamHealth

    def get_for_station(self, station_id, limit: int = 50):
        return list(self.model.objects.filter(station_id=station_id)[:limit])

    def get_latest(self, station_id):
        return self.model.objects.filter(station_id=station_id).order_by('-last_checked').first()

    def get_failures(self, station_id, limit: int = 10):
        from .models import StreamHealthStatus
        return list(self.model.objects.filter(
            station_id=station_id,
            provider_status__in=[StreamHealthStatus.DOWN, StreamHealthStatus.TIMEOUT]
        ).order_by('-last_checked')[:limit])


class LiveSessionRepository(BaseRepository):
    model = LiveSession

    def get_active(self, station_id):
        return self.model.objects.filter(station_id=station_id, ended_at__isnull=True).first()

    def get_for_station(self, station_id, limit: int = 20):
        return list(self.model.objects.filter(station_id=station_id)[:limit])

    def close_session(self, session_id):
        from django.utils import timezone
        try:
            session = self.model.objects.get(pk=session_id)
            session.ended_at = timezone.now()
            session.save(update_fields=['ended_at'])
            return session
        except self.model.DoesNotExist:
            return None
