from unittest.mock import patch, MagicMock
from django.test import TestCase, RequestFactory, override_settings
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta

from .models import RadioStation, RadioProvider, NowPlayingCache, ListenerStatistic, StreamHealth, LiveSession
from .repositories import (
    RadioStationRepository, RadioProviderRepository, NowPlayingCacheRepository,
    ListenerStatisticRepository, StreamHealthRepository, LiveSessionRepository
)
from .services import (
    NowPlayingService, ListenerService, StreamHealthService,
    LiveSessionService, RadioStationService, RadioProviderService,
    MetadataService, ArtworkService, FallbackService,
    PlayerService, BroadcastIntegrationService
)
from .adapters.base import NowPlayingData, ListenerData, HealthCheckData

User = get_user_model()


class RadioStationRepositoryTest(TestCase):
    def setUp(self):
        self.repo = RadioStationRepository()
        self.station = RadioStation.objects.create(station_name='Test FM', is_active=True)

    def test_get_active_stations(self):
        RadioStation.objects.create(station_name='Inactive', is_active=False)
        active = self.repo.get_active_stations()
        self.assertEqual(active.count(), 1)
        self.assertEqual(active.first().station_name, 'Test FM')

    def test_get_primary_station(self):
        primary = self.repo.get_primary_station()
        self.assertEqual(primary.station_name, 'Test FM')

    def test_get_primary_station_none(self):
        RadioStation.objects.all().delete()
        primary = self.repo.get_primary_station()
        self.assertIsNone(primary)


class RadioProviderRepositoryTest(TestCase):
    def setUp(self):
        self.repo = RadioProviderRepository()
        self.station = RadioStation.objects.create(station_name='Test FM')
        self.provider = RadioProvider.objects.create(
            station=self.station,
            provider_name='Test Provider',
            provider_type='RADIOBOSS',
            active=True
        )

    def test_get_active_providers(self):
        RadioProvider.objects.create(
            station=self.station,
            provider_name='Inactive',
            active=False
        )
        active = self.repo.get_active_providers()
        self.assertEqual(active.count(), 1)

    def test_get_for_station(self):
        providers = self.repo.get_for_station(self.station.pk)
        self.assertEqual(providers.count(), 1)

    def test_get_primary_provider(self):
        provider = self.repo.get_primary_provider(self.station.pk)
        self.assertEqual(provider.provider_name, 'Test Provider')


class NowPlayingCacheRepositoryTest(TestCase):
    def setUp(self):
        self.repo = NowPlayingCacheRepository()
        self.station = RadioStation.objects.create(station_name='Test FM')

    def test_get_for_station(self):
        NowPlayingCache.objects.create(station=self.station, song_title='Song 1', stream_status='ONLINE')
        cache = self.repo.get_for_station(self.station.pk)
        self.assertEqual(cache.song_title, 'Song 1')

    def test_get_for_station_none(self):
        cache = self.repo.get_for_station(self.station.pk)
        self.assertIsNone(cache)

    def test_get_or_none(self):
        cache = self.repo.get_or_none(self.station.pk)
        self.assertIsNone(cache)


class ListenerStatisticRepositoryTest(TestCase):
    def setUp(self):
        self.repo = ListenerStatisticRepository()
        self.station = RadioStation.objects.create(station_name='Test FM')

    def test_get_for_station(self):
        ListenerStatistic.objects.create(
            station=self.station,
            current_listeners=10,
            peak_listeners=15
        )
        stats = self.repo.get_for_station(self.station.pk)
        self.assertEqual(len(stats), 1)

    def test_get_recent(self):
        ListenerStatistic.objects.create(
            station=self.station,
            current_listeners=10,
            peak_listeners=15
        )
        stats = self.repo.get_recent(self.station.pk, hours=24)
        self.assertEqual(len(stats), 1)

    def test_get_latest(self):
        ListenerStatistic.objects.create(
            station=self.station,
            current_listeners=10,
            peak_listeners=15
        )
        latest = self.repo.get_latest(self.station.pk)
        self.assertEqual(latest.current_listeners, 10)


class StreamHealthRepositoryTest(TestCase):
    def setUp(self):
        self.repo = StreamHealthRepository()
        self.station = RadioStation.objects.create(station_name='Test FM')

    def test_get_for_station(self):
        StreamHealth.objects.create(
            station=self.station,
            provider_status='HEALTHY',
            response_time=100,
            http_status=200,
            stream_bitrate=128
        )
        health = self.repo.get_for_station(self.station.pk)
        self.assertEqual(len(health), 1)

    def test_get_latest(self):
        StreamHealth.objects.create(
            station=self.station,
            provider_status='HEALTHY',
            response_time=100,
            http_status=200,
            stream_bitrate=128
        )
        latest = self.repo.get_latest(self.station.pk)
        self.assertEqual(latest.provider_status, 'HEALTHY')


class LiveSessionRepositoryTest(TestCase):
    def setUp(self):
        self.repo = LiveSessionRepository()
        self.station = RadioStation.objects.create(station_name='Test FM')

    def test_get_active(self):
        session = LiveSession.objects.create(
            station=self.station,
            program='Morning Show',
            host='DJ John',
            started_at=timezone.now()
        )
        active = self.repo.get_active(self.station.pk)
        self.assertEqual(active.program, 'Morning Show')

    def test_get_active_none(self):
        active = self.repo.get_active(self.station.pk)
        self.assertIsNone(active)

    def test_get_for_station(self):
        LiveSession.objects.create(
            station=self.station,
            program='Show',
            host='DJ',
            started_at=timezone.now()
        )
        sessions = self.repo.get_for_station(self.station.pk)
        self.assertEqual(len(sessions), 1)


class NowPlayingServiceTest(TestCase):
    def setUp(self):
        self.station = RadioStation.objects.create(station_name='Test FM', is_active=True)
        self.provider = RadioProvider.objects.create(
            station=self.station,
            provider_name='Test',
            provider_type='RADIOBOSS',
            active=True,
            api_url='http://example.com/api',
            stream_url='http://stream.example.com'
        )
        self.service = NowPlayingService()

    @patch('apps.radio.adapters.radioboss.RadioBossAdapter.get_now_playing')
    def test_refresh_from_provider(self, mock_get):
        mock_get.return_value = NowPlayingData(
            stream_status='ONLINE',
            song_title='Test Song',
            artist='Test Artist',
            album='Test Album',
            artwork='',
            duration=240,
            elapsed=120,
        )
        np = self.service.refresh_from_provider(str(self.station.pk))
        self.assertIsNotNone(np)
        self.assertEqual(np.song_title, 'Test Song')
        self.assertEqual(np.artist, 'Test Artist')
        self.assertEqual(np.stream_status, 'ONLINE')

    def test_get_now_playing(self):
        NowPlayingCache.objects.create(
            station=self.station,
            song_title='Cached Song',
            stream_status='ONLINE'
        )
        np = self.service.get_now_playing(str(self.station.pk))
        self.assertEqual(np.song_title, 'Cached Song')

    def test_get_now_playing_none(self):
        np = self.service.get_now_playing(str(self.station.pk))
        self.assertIsNone(np)

    @patch('apps.radio.adapters.radioboss.RadioBossAdapter.get_now_playing')
    def test_refresh_all(self, mock_get):
        mock_get.return_value = NowPlayingData(
            stream_status='ONLINE',
            song_title='Song',
            artist='Artist',
            album='Album',
            artwork='',
            duration=0,
            elapsed=0,
        )
        self.service.refresh_all()
        self.assertEqual(NowPlayingCache.objects.count(), 1)


class ListenerServiceTest(TestCase):
    def setUp(self):
        self.station = RadioStation.objects.create(station_name='Test FM', is_active=True)
        self.provider = RadioProvider.objects.create(
            station=self.station,
            provider_name='Test',
            provider_type='RADIOBOSS',
            active=True,
            api_url='http://example.com/api'
        )
        self.service = ListenerService()

    @patch('apps.radio.adapters.radioboss.RadioBossAdapter.get_listener_count')
    def test_refresh_from_provider(self, mock_get):
        mock_get.return_value = ListenerData(
            current_listeners=25,
            peak_listeners=30,
        )
        stat = self.service.refresh_from_provider(str(self.station.pk))
        self.assertIsNotNone(stat)
        self.assertEqual(stat.current_listeners, 25)

    def test_get_current(self):
        ListenerStatistic.objects.create(
            station=self.station,
            current_listeners=10,
            peak_listeners=15
        )
        stat = self.service.get_current(str(self.station.pk))
        self.assertEqual(stat.current_listeners, 10)

    def test_get_hourly_stats(self):
        ListenerStatistic.objects.create(
            station=self.station,
            current_listeners=10,
            peak_listeners=15,
            recorded_at=timezone.now() - timedelta(hours=1)
        )
        stats = self.service.get_hourly_stats(str(self.station.pk), hours=24)
        self.assertIn('avg_listeners', stats)

    def test_export_csv(self):
        ListenerStatistic.objects.create(
            station=self.station,
            current_listeners=10,
            peak_listeners=15,
        )
        csv_data = self.service.export_csv(str(self.station.pk), hours=24)
        self.assertIn('Current Listeners', csv_data)


class StreamHealthServiceTest(TestCase):
    def setUp(self):
        self.station = RadioStation.objects.create(station_name='Test FM', is_active=True)
        self.provider = RadioProvider.objects.create(
            station=self.station,
            provider_name='Test',
            provider_type='RADIOBOSS',
            active=True,
            api_url='http://example.com/api'
        )
        self.service = StreamHealthService()

    @patch('apps.radio.adapters.radioboss.RadioBossAdapter.check_health')
    def test_refresh_from_provider(self, mock_get):
        mock_get.return_value = HealthCheckData(
            response_time=150.0,
            http_status=200,
            provider_status='HEALTHY',
            stream_bitrate=128,
            stream_format='MP3',
            error_message='',
        )
        health = self.service.refresh_from_provider(str(self.station.pk))
        self.assertIsNotNone(health)
        self.assertEqual(health.provider_status, 'HEALTHY')

    def test_get_latest(self):
        StreamHealth.objects.create(
            station=self.station,
            provider_status='HEALTHY',
            response_time=100,
            http_status=200,
            stream_bitrate=128
        )
        health = self.service.get_latest(str(self.station.pk))
        self.assertEqual(health.provider_status, 'HEALTHY')


class LiveSessionServiceTest(TestCase):
    def setUp(self):
        self.station = RadioStation.objects.create(station_name='Test FM')
        self.service = LiveSessionService()

    def test_get_active(self):
        session = LiveSession.objects.create(
            station=self.station,
            program='Morning Show',
            host='DJ John',
            started_at=timezone.now()
        )
        active = self.service.get_active(str(self.station.pk))
        self.assertEqual(active.program, 'Morning Show')

    def test_get_active_none(self):
        active = self.service.get_active(str(self.station.pk))
        self.assertIsNone(active)

    def test_start_session(self):
        session = self.service.start_session(str(self.station.pk), program='Test', host='DJ')
        self.assertEqual(session.program, 'Test')
        self.assertEqual(session.host, 'DJ')

    def test_end_session(self):
        session = LiveSession.objects.create(
            station=self.station,
            program='Show',
            host='DJ',
            started_at=timezone.now()
        )
        ended = self.service.end_session(session.pk)
        self.assertIsNotNone(ended.ended_at)


class MetadataServiceTest(TestCase):
    def setUp(self):
        self.station = RadioStation.objects.create(station_name='Test FM')
        self.service = MetadataService()

    def test_get_track_info(self):
        NowPlayingCache.objects.create(
            station=self.station,
            song_title='Test',
            artist='Artist',
            stream_status='ONLINE'
        )
        meta = self.service.get_track_info(str(self.station.pk))
        self.assertEqual(meta['song_title'], 'Test')

    def test_get_track_info_none(self):
        meta = self.service.get_track_info(str(self.station.pk))
        self.assertEqual(meta['song_title'], '')


class ArtworkServiceTest(TestCase):
    def setUp(self):
        self.station = RadioStation.objects.create(station_name='Test FM')
        self.service = ArtworkService()

    def test_get_artwork(self):
        NowPlayingCache.objects.create(
            station=self.station,
            artwork='http://example.com/art.jpg',
            stream_status='ONLINE'
        )
        artwork = self.service.get_artwork(str(self.station.pk))
        self.assertEqual(artwork, 'http://example.com/art.jpg')

    def test_get_artwork_empty(self):
        artwork = self.service.get_artwork(str(self.station.pk))
        self.assertEqual(artwork, '')


class FallbackServiceTest(TestCase):
    def setUp(self):
        self.station = RadioStation.objects.create(station_name='Test FM', is_active=True)
        self.provider = RadioProvider.objects.create(
            station=self.station,
            provider_name='Primary',
            provider_type='RADIOBOSS',
            stream_url='http://primary.stream',
            backup_stream_url='http://backup.stream',
            active=True,
            api_url='http://example.com/api'
        )
        self.service = FallbackService()

    def test_get_fallback_stream(self):
        url = self.service.get_fallback_stream(str(self.station.pk))
        self.assertEqual(url, 'http://backup.stream')

    def test_get_fallback_stream_none(self):
        self.provider.backup_stream_url = ''
        self.provider.save()
        url = self.service.get_fallback_stream(str(self.station.pk))
        self.assertIsNone(url)


class RadioStationServiceTest(TestCase):
    def setUp(self):
        self.service = RadioStationService()

    def test_get_primary_station(self):
        station = RadioStation.objects.create(station_name='Primary', is_active=True)
        RadioStation.objects.create(station_name='Secondary', is_active=True)
        primary = self.service.get_primary_station()
        self.assertEqual(primary.station_name, 'Primary')

    def test_get_primary_station_none(self):
        primary = self.service.get_primary_station()
        self.assertIsNone(primary)

    def test_get_active_stations(self):
        RadioStation.objects.create(station_name='Active', is_active=True)
        RadioStation.objects.create(station_name='Inactive', is_active=False)
        stations = self.service.get_active_stations()
        self.assertEqual(stations.count(), 1)

    def test_create_station(self):
        station = self.service.create_station(station_name='New FM', is_active=True)
        self.assertEqual(station.station_name, 'New FM')

    def test_toggle_active(self):
        station = RadioStation.objects.create(station_name='Toggle FM', is_active=True)
        toggled = self.service.toggle_active(station.pk)
        self.assertFalse(toggled.is_active)


class RadioProviderServiceTest(TestCase):
    def setUp(self):
        self.service = RadioProviderService()
        self.station = RadioStation.objects.create(station_name='Test FM')

    def test_get_for_station(self):
        RadioProvider.objects.create(
            station=self.station,
            provider_name='Test',
            provider_type='RADIOBOSS',
            active=True
        )
        providers = self.service.get_for_station(self.station.pk)
        self.assertEqual(providers.count(), 1)

    def test_get_primary_provider(self):
        RadioProvider.objects.create(
            station=self.station,
            provider_name='Test',
            provider_type='RADIOBOSS',
            active=True
        )
        provider = self.service.get_primary_provider(self.station.pk)
        self.assertEqual(provider.provider_name, 'Test')

    def test_create_provider(self):
        provider = self.service.create_provider(
            station=self.station,
            provider_name='New',
            provider_type='ICECAST',
            stream_url='http://stream.example.com',
            active=True
        )
        self.assertEqual(provider.provider_name, 'New')

    def test_toggle_active(self):
        provider = RadioProvider.objects.create(
            station=self.station,
            provider_name='Toggle',
            provider_type='RADIOBOSS',
            active=True
        )
        toggled = self.service.toggle_active(provider.pk)
        self.assertFalse(toggled.active)


class PlayerServiceTest(TestCase):
    def setUp(self):
        self.service = PlayerService()
        self.station = RadioStation.objects.create(
            station_name='Test FM', is_active=True,
            default_volume=80, autoplay=True, sticky_player=True
        )
        self.provider = RadioProvider.objects.create(
            station=self.station,
            provider_name='Primary',
            provider_type='RADIOBOSS',
            stream_url='http://stream.example.com',
            backup_stream_url='http://backup.example.com',
            active=True,
            api_url='http://example.com/api'
        )

    @patch('apps.radio.adapters.radioboss.RadioBossAdapter.check_health')
    def test_get_player_config(self, mock_health):
        from .adapters.base import HealthCheckData
        mock_health.return_value = HealthCheckData(
            response_time=100.0, http_status=200,
            provider_status='HEALTHY', stream_bitrate=128,
            stream_format='MP3', error_message='',
        )
        config = self.service.get_player_config()
        self.assertEqual(config['station_name'], 'Test FM')
        self.assertEqual(config['stream_url'], 'http://stream.example.com')
        self.assertEqual(config['backup_stream_url'], 'http://backup.example.com')
        self.assertEqual(config['default_volume'], 80)
        self.assertTrue(config['autoplay'])
        self.assertTrue(config['sticky_player'])
        self.assertTrue(config['is_active'])

    def test_get_player_config_no_station(self):
        RadioStation.objects.all().delete()
        config = self.service.get_player_config()
        self.assertEqual(config['station_name'], '')
        self.assertFalse(config['is_active'])

    def test_update_volume(self):
        updated = self.service.update_volume(str(self.station.pk), 50)
        self.assertIsNotNone(updated)
        self.assertEqual(updated.default_volume, 50)

    def test_update_volume_invalid(self):
        updated = self.service.update_volume(str(self.station.pk), 150)
        self.assertIsNone(updated)

    def test_update_autoplay(self):
        updated = self.service.update_autoplay(str(self.station.pk), False)
        self.assertIsNotNone(updated)
        self.assertFalse(updated.autoplay)

    def test_update_sticky(self):
        updated = self.service.update_sticky(str(self.station.pk), False)
        self.assertIsNotNone(updated)
        self.assertFalse(updated.sticky_player)


class BroadcastIntegrationServiceTest(TestCase):
    def setUp(self):
        self.service = BroadcastIntegrationService()
        self.station = RadioStation.objects.create(
            station_name='Test FM', is_active=True
        )

    def test_get_current_program_no_session_no_schedule(self):
        info = self.service.get_current_program(str(self.station.pk))
        self.assertEqual(info['program'], '')
        self.assertEqual(info['host'], '')

    def test_get_program_info_for_station_no_data(self):
        info = self.service.get_program_info_for_station(str(self.station.pk))
        self.assertFalse(info['has_session'])
        self.assertEqual(info['program'], '')

    def test_sync_live_session(self):
        session = self.service.sync_live_session(
            str(self.station.pk), program='Test Show', host='DJ Test'
        )
        self.assertEqual(session.program, 'Test Show')
        self.assertEqual(session.host, 'DJ Test')

    def test_get_current_program_with_session(self):
        from django.utils import timezone
        LiveSession.objects.create(
            station=self.station,
            program='Live Show',
            host='DJ Live',
            started_at=timezone.now()
        )
        info = self.service.get_current_program(str(self.station.pk))
        self.assertEqual(info['program'], 'Live Show')
        self.assertEqual(info['host'], 'DJ Live')

    def test_get_program_info_with_session(self):
        from django.utils import timezone
        LiveSession.objects.create(
            station=self.station,
            program='Live Show',
            host='DJ Live',
            started_at=timezone.now()
        )
        info = self.service.get_program_info_for_station(str(self.station.pk))
        self.assertTrue(info['has_session'])
        self.assertEqual(info['program'], 'Live Show')


@override_settings(AUTHENTICATION_BACKENDS=['django.contrib.auth.backends.ModelBackend'])
class RadioStationDeleteViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testadmin', email='admin@test.com', password='testpass123', is_staff=True, is_superuser=True
        )
        self.client.login(username='testadmin', password='testpass123')
        self.station = RadioStation.objects.create(
            station_name='Test FM', is_active=True
        )

    def test_get_confirm_page(self):
        response = self.client.get(f'/radio/station/{self.station.pk}/hapus/')
        self.assertEqual(response.status_code, 200)

    def test_post_toggle_inactive(self):
        response = self.client.post(f'/radio/station/{self.station.pk}/hapus/')
        self.assertEqual(response.status_code, 302)
        self.station.refresh_from_db()
        self.assertFalse(self.station.is_active)

    def test_post_toggle_active(self):
        self.station.is_active = False
        self.station.save()
        response = self.client.post(f'/radio/station/{self.station.pk}/hapus/')
        self.assertEqual(response.status_code, 302)
        self.station.refresh_from_db()
        self.assertTrue(self.station.is_active)


@override_settings(AUTHENTICATION_BACKENDS=['django.contrib.auth.backends.ModelBackend'])
class RadioProviderDeleteViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testadmin', email='admin@test.com', password='testpass123', is_staff=True, is_superuser=True
        )
        self.client.login(username='testadmin', password='testpass123')
        self.station = RadioStation.objects.create(station_name='Test FM')
        self.provider = RadioProvider.objects.create(
            station=self.station,
            provider_name='Test Provider',
            provider_type='RADIOBOSS',
            stream_url='http://stream.example.com',
            active=True
        )

    def test_get_confirm_page(self):
        response = self.client.get(f'/radio/provider/{self.provider.pk}/hapus/')
        self.assertEqual(response.status_code, 200)

    def test_post_toggle_inactive(self):
        response = self.client.post(f'/radio/provider/{self.provider.pk}/hapus/')
        self.assertEqual(response.status_code, 302)
        self.provider.refresh_from_db()
        self.assertFalse(self.provider.active)


@override_settings(AUTHENTICATION_BACKENDS=['django.contrib.auth.backends.ModelBackend'])
class RadioCurrentHostAPIViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testadmin', email='admin@test.com', password='testpass123', is_staff=True, is_superuser=True
        )
        self.client.login(username='testadmin', password='testpass123')
        self.station = RadioStation.objects.create(
            station_name='Test FM', is_active=True
        )

    def test_no_station(self):
        RadioStation.objects.all().delete()
        response = self.client.get('/radio/api/current-host/')
        self.assertEqual(response.status_code, 404)

    def test_no_session(self):
        response = self.client.get('/radio/api/current-host/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['program'], '')

    def test_with_session(self):
        from django.utils import timezone
        LiveSession.objects.create(
            station=self.station,
            program='Morning Show',
            host='DJ John',
            started_at=timezone.now()
        )
        response = self.client.get('/radio/api/current-host/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['program'], 'Morning Show')
        self.assertEqual(data['host'], 'DJ John')


@override_settings(AUTHENTICATION_BACKENDS=['django.contrib.auth.backends.ModelBackend'])
class RadioProvidersAPIViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testadmin', email='admin@test.com', password='testpass123', is_staff=True, is_superuser=True
        )
        self.client.login(username='testadmin', password='testpass123')
        self.station = RadioStation.objects.create(
            station_name='Test FM', is_active=True
        )

    def test_no_station(self):
        RadioStation.objects.all().delete()
        response = self.client.get('/radio/api/providers/')
        self.assertEqual(response.status_code, 404)

    def test_with_providers(self):
        RadioProvider.objects.create(
            station=self.station,
            provider_name='Provider 1',
            provider_type='RADIOBOSS',
            stream_url='http://stream1.example.com',
            active=True
        )
        RadioProvider.objects.create(
            station=self.station,
            provider_name='Provider 2',
            provider_type='ICECAST',
            stream_url='http://stream2.example.com',
            active=False
        )
        response = self.client.get('/radio/api/providers/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['station'], 'Test FM')
        self.assertEqual(len(data['providers']), 1)
        self.assertEqual(data['providers'][0]['provider_name'], 'Provider 1')


@override_settings(AUTHENTICATION_BACKENDS=['django.contrib.auth.backends.ModelBackend'])
class RadioPlayerConfigAPIViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testadmin', email='admin@test.com', password='testpass123', is_staff=True, is_superuser=True
        )
        self.client.login(username='testadmin', password='testpass123')
        self.station = RadioStation.objects.create(
            station_name='Test FM', is_active=True,
            default_volume=75, autoplay=True, sticky_player=True
        )
        self.provider = RadioProvider.objects.create(
            station=self.station,
            provider_name='Primary',
            provider_type='RADIOBOSS',
            stream_url='http://stream.example.com',
            active=True,
            api_url='http://example.com/api'
        )

    def test_get_player_config(self):
        response = self.client.get('/radio/api/player-config/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['station_name'], 'Test FM')
        self.assertEqual(data['default_volume'], 75)
        self.assertTrue(data['autoplay'])

    def test_get_player_config_no_station(self):
        RadioStation.objects.all().delete()
        response = self.client.get('/radio/api/player-config/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['station_name'], '')
