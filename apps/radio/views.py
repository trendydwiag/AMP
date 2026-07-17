import csv
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse, HttpRequest
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import TemplateView
from apps.users.decorators import admin_required
from .models import RadioStation, RadioProvider, NowPlayingCache, ListenerStatistic, StreamHealth, LiveSession
from .services import (
    NowPlayingService, ListenerService, StreamHealthService,
    LiveSessionService, RadioStationService, RadioProviderService,
    MetadataService, ArtworkService, FallbackService,
    PlayerService, BroadcastIntegrationService
)
from .forms import RadioStationForm, RadioProviderForm


def _json_response(data, status=200):
    import json
    from django.http import JsonResponse
    return JsonResponse(data, status=status, safe=False)


@method_decorator(login_required, name='dispatch')
@method_decorator(admin_required, name='dispatch')
class RadioDashboardView(TemplateView):
    template_name = 'radio/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        station_svc = RadioStationService()
        station = station_svc.get_primary_station()
        if station:
            np_svc = NowPlayingService()
            listener_svc = ListenerService()
            health_svc = StreamHealthService()
            live_svc = LiveSessionService()
            context['station'] = station
            context['now_playing'] = np_svc.get_now_playing(station.pk)
            context['listener_stat'] = listener_svc.get_current(station.pk)
            context['health'] = health_svc.get_latest(station.pk)
            context['active_session'] = live_svc.get_active(station.pk)
            context['providers'] = station.providers.all()
            context['health_history'] = health_svc.get_health_history(station.pk, limit=10)
            context['stations'] = station_svc.get_active_stations()
        else:
            context['station'] = None
            context['stations'] = station_svc.get_active_stations()
        return context


@method_decorator(login_required, name='dispatch')
@method_decorator(admin_required, name='dispatch')
class RadioStationListView(TemplateView):
    template_name = 'radio/station_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['stations'] = RadioStation.objects.all()
        return context


@method_decorator(login_required, name='dispatch')
@method_decorator(admin_required, name='dispatch')
class RadioStationCreateView(TemplateView):
    template_name = 'radio/station_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = RadioStationForm()
        context['is_edit'] = False
        return context

    def post(self, request, *args, **kwargs):
        form = RadioStationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            from django.contrib import messages
            from django.shortcuts import redirect
            messages.success(request, 'Station berhasil dibuat.')
            return redirect('radio:station_list')
        context = self.get_context_data(**kwargs)
        context['form'] = form
        return self.render_to_response(context)


@method_decorator(login_required, name='dispatch')
@method_decorator(admin_required, name='dispatch')
class RadioStationEditView(TemplateView):
    template_name = 'radio/station_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        station = RadioStation.objects.get(pk=kwargs['pk'])
        context['form'] = RadioStationForm(instance=station)
        context['is_edit'] = True
        context['station'] = station
        return context

    def post(self, request, *args, **kwargs):
        station = RadioStation.objects.get(pk=kwargs['pk'])
        form = RadioStationForm(request.POST, request.FILES, instance=station)
        if form.is_valid():
            form.save()
            from django.contrib import messages
            from django.shortcuts import redirect
            messages.success(request, 'Station berhasil diperbarui.')
            return redirect('radio:station_list')
        context = self.get_context_data(**kwargs)
        context['form'] = form
        return self.render_to_response(context)


@method_decorator(login_required, name='dispatch')
@method_decorator(admin_required, name='dispatch')
class RadioProviderListView(TemplateView):
    template_name = 'radio/provider_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['providers'] = RadioProvider.objects.select_related('station').all()
        return context


@method_decorator(login_required, name='dispatch')
@method_decorator(admin_required, name='dispatch')
class RadioProviderCreateView(TemplateView):
    template_name = 'radio/provider_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = RadioProviderForm()
        context['is_edit'] = False
        return context

    def post(self, request, *args, **kwargs):
        form = RadioProviderForm(request.POST)
        if form.is_valid():
            form.save()
            from django.contrib import messages
            from django.shortcuts import redirect
            messages.success(request, 'Provider berhasil dibuat.')
            return redirect('radio:provider_list')
        context = self.get_context_data(**kwargs)
        context['form'] = form
        return self.render_to_response(context)


@method_decorator(login_required, name='dispatch')
@method_decorator(admin_required, name='dispatch')
class RadioProviderEditView(TemplateView):
    template_name = 'radio/provider_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        provider = RadioProvider.objects.get(pk=kwargs['pk'])
        context['form'] = RadioProviderForm(instance=provider)
        context['is_edit'] = True
        context['provider'] = provider
        return context

    def post(self, request, *args, **kwargs):
        provider = RadioProvider.objects.get(pk=kwargs['pk'])
        form = RadioProviderForm(request.POST, instance=provider)
        if form.is_valid():
            form.save()
            from django.contrib import messages
            from django.shortcuts import redirect
            messages.success(request, 'Provider berhasil diperbarui.')
            return redirect('radio:provider_list')
        context = self.get_context_data(**kwargs)
        context['form'] = form
        return self.render_to_response(context)


@method_decorator(login_required, name='dispatch')
@method_decorator(admin_required, name='dispatch')
class RadioAnalyticsView(TemplateView):
    template_name = 'radio/analytics.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        station_svc = RadioStationService()
        station = station_svc.get_primary_station()
        if station:
            listener_svc = ListenerService()
            context['station'] = station
            context['hourly_stats'] = listener_svc.get_hourly_stats(station.pk, hours=24)
            context['daily_stats'] = listener_svc.get_hourly_stats(station.pk, hours=168)
        return context


class ExportCSVView(View):
    def get(self, request, station_id):
        listener_svc = ListenerService()
        hours = int(request.GET.get('hours', 168))
        csv_data = listener_svc.export_csv(station_id, hours)
        response = HttpResponse(csv_data, content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="listener_stats_{station_id}.csv"'
        return response


class ExportExcelView(View):
    def get(self, request, station_id):
        listener_svc = ListenerService()
        hours = int(request.GET.get('hours', 168))
        excel_data = listener_svc.export_excel(station_id, hours)
        if not excel_data:
            return HttpResponse('openpyxl not installed', status=500)
        response = HttpResponse(excel_data, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename="listener_stats_{station_id}.xlsx"'
        return response


class RadioNowPlayingAPIView(View):
    def get(self, request):
        station_svc = RadioStationService()
        station = station_svc.get_primary_station()
        if not station:
            return JsonResponse({'error': 'No active station'}, status=404)
        np_svc = NowPlayingService()
        np_cache = np_svc.get_now_playing(station.pk)
        if not np_cache:
            return JsonResponse({
                'station': station.station_name,
                'stream_status': 'OFFLINE',
                'song_title': '',
                'artist': '',
                'album': '',
                'artwork': '',
                'duration': 0,
                'elapsed': 0,
                'progress_percent': 0,
            })
        return JsonResponse({
            'station': station.station_name,
            'stream_url': station.primary_provider.stream_url if station.primary_provider else '',
            'stream_status': np_cache.stream_status,
            'song_title': np_cache.song_title,
            'artist': np_cache.artist,
            'album': np_cache.album,
            'artwork': np_cache.artwork,
            'duration': np_cache.duration,
            'elapsed': np_cache.elapsed,
            'progress_percent': np_cache.progress_percent,
        })


class RadioStatusAPIView(View):
    def get(self, request):
        station_svc = RadioStationService()
        station = station_svc.get_primary_station()
        if not station:
            return JsonResponse({'error': 'No active station'}, status=404)
        np_svc = NowPlayingService()
        listener_svc = ListenerService()
        health_svc = StreamHealthService()
        live_svc = LiveSessionService()
        np_cache = np_svc.get_now_playing(station.pk)
        listener_stat = listener_svc.get_current(station.pk)
        health = health_svc.get_latest(station.pk)
        active_session = live_svc.get_active(station.pk)
        provider = station.primary_provider
        return JsonResponse({
            'station': station.station_name,
            'is_active': station.is_active,
            'stream_url': provider.stream_url if provider else '',
            'backup_stream_url': provider.backup_stream_url if provider else '',
            'stream_status': np_cache.stream_status if np_cache else 'UNKNOWN',
            'song_title': np_cache.song_title if np_cache else '',
            'artist': np_cache.artist if np_cache else '',
            'album': np_cache.album if np_cache else '',
            'artwork': np_cache.artwork if np_cache else '',
            'duration': np_cache.duration if np_cache else 0,
            'elapsed': np_cache.elapsed if np_cache else 0,
            'progress_percent': np_cache.progress_percent if np_cache else 0,
            'current_listeners': listener_stat.current_listeners if listener_stat else 0,
            'peak_listeners': listener_stat.peak_listeners if listener_stat else 0,
            'health_status': health.provider_status if health else 'UNKNOWN',
            'response_time': health.response_time if health else 0,
            'last_health_check': health.last_checked.isoformat() if health else None,
            'current_program': active_session.program if active_session else '',
            'current_host': active_session.host if active_session else '',
        })


class RadioPlayerAPIView(View):
    def get(self, request):
        station_svc = RadioStationService()
        station = station_svc.get_primary_station()
        if not station:
            return JsonResponse({'error': 'No active station'}, status=404)
        provider = station.primary_provider
        fallback_svc = FallbackService()
        stream_url = fallback_svc.get_available_stream(station.pk) or (provider.stream_url if provider else '')
        return JsonResponse({
            'station': station.station_name,
            'stream_url': stream_url,
            'backup_stream_url': provider.backup_stream_url if provider else '',
            'default_volume': station.default_volume,
            'autoplay': station.autoplay,
            'sticky_player': station.sticky_player,
            'logo': station.logo.url if station.logo else '',
        })


class RadioListenerAPIView(View):
    def get(self, request):
        station_svc = RadioStationService()
        station = station_svc.get_primary_station()
        if not station:
            return JsonResponse({'error': 'No active station'}, status=404)
        listener_svc = ListenerService()
        stat = listener_svc.get_current(station.pk)
        return JsonResponse({
            'current_listeners': stat.current_listeners if stat else 0,
            'peak_listeners': stat.peak_listeners if stat else 0,
        })


class RadioHealthAPIView(View):
    def get(self, request):
        station_svc = RadioStationService()
        station = station_svc.get_primary_station()
        if not station:
            return JsonResponse({'error': 'No active station'}, status=404)
        health_svc = StreamHealthService()
        health = health_svc.get_latest(station.pk)
        return JsonResponse({
            'status': health.provider_status if health else 'UNKNOWN',
            'response_time': health.response_time if health else 0,
            'http_status': health.http_status if health else 0,
            'stream_bitrate': health.stream_bitrate if health else 0,
            'last_checked': health.last_checked.isoformat() if health else None,
        })


class RadioCurrentProgramAPIView(View):
    def get(self, request):
        station_svc = RadioStationService()
        station = station_svc.get_primary_station()
        if not station:
            return JsonResponse({'error': 'No active station'}, status=404)
        live_svc = LiveSessionService()
        session = live_svc.get_active(station.pk)
        return JsonResponse({
            'program': session.program if session else '',
            'host': session.host if session else '',
            'started_at': session.started_at.isoformat() if session else None,
            'duration': session.duration_display if session else '',
        })


@method_decorator(login_required, name='dispatch')
@method_decorator(admin_required, name='dispatch')
class RadioStationDeleteView(TemplateView):
    template_name = 'radio/station_confirm_delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['station'] = RadioStation.objects.get(pk=kwargs['pk'])
        return context

    def post(self, request, *args, **kwargs):
        station_svc = RadioStationService()
        toggled = station_svc.toggle_active(kwargs['pk'])
        from django.contrib import messages
        from django.shortcuts import redirect
        if toggled:
            status = 'diaktifkan' if toggled.is_active else 'dinonaktifkan'
            messages.success(request, f'Station berhasil {status}.')
        else:
            messages.error(request, 'Station tidak ditemukan.')
        return redirect('radio:station_list')


@method_decorator(login_required, name='dispatch')
@method_decorator(admin_required, name='dispatch')
class RadioProviderDeleteView(TemplateView):
    template_name = 'radio/provider_confirm_delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['provider'] = RadioProvider.objects.get(pk=kwargs['pk'])
        return context

    def post(self, request, *args, **kwargs):
        provider_svc = RadioProviderService()
        toggled = provider_svc.toggle_active(kwargs['pk'])
        from django.contrib import messages
        from django.shortcuts import redirect
        if toggled:
            status = 'diaktifkan' if toggled.active else 'dinonaktifkan'
            messages.success(request, f'Provider berhasil {status}.')
        else:
            messages.error(request, 'Provider tidak ditemukan.')
        return redirect('radio:provider_list')


class RadioCurrentHostAPIView(View):
    def get(self, request):
        station_svc = RadioStationService()
        station = station_svc.get_primary_station()
        if not station:
            return JsonResponse({'error': 'No active station'}, status=404)
        integration_svc = BroadcastIntegrationService()
        info = integration_svc.get_current_program(station.pk)
        return JsonResponse({
            'program': info['program'],
            'host': info['host'],
            'started_at': info['started_at'].isoformat() if info['started_at'] else None,
            'duration': info['duration'],
        })


class RadioProvidersAPIView(View):
    def get(self, request):
        station_svc = RadioStationService()
        station = station_svc.get_primary_station()
        if not station:
            return JsonResponse({'error': 'No active station'}, status=404)
        providers = station.providers.filter(active=True).values(
            'pk', 'provider_name', 'provider_type', 'stream_url', 'active'
        )
        return JsonResponse({
            'station': station.station_name,
            'providers': list(providers),
        })


class RadioPlayerConfigAPIView(View):
    def get(self, request):
        player_svc = PlayerService()
        return JsonResponse(player_svc.get_player_config())


class LiveRadioAPIView(View):
    """
    GET /api/v1/radio/live/

    Normalized, provider-agnostic live radio data consumed by all UI components.
    The provider URL lives only in Django settings — never in templates or JS.

    Response is cached for STREAM_CACHE_TTL seconds (default: 20s).
    On any upstream failure: returns status=offline with HTTP 200 — never crashes.

    Schema:
        status      "live" | "offline"
        station     Station name from settings
        program     Current program name or null
        title       Now-playing song title
        artist      Now-playing artist
        cover       Artwork URL
        listeners   Current listener count (int)
        started_at  ISO datetime or null
        stream_url  Audio stream URL from provider
        is_live     Boolean shorthand for status == "live"
        provider    Provider key (lowercase, e.g. "broadcastindo")
    """
    CACHE_KEY = 'amp_v1_live_radio'

    def get(self, request):
        import logging
        from django.core.cache import cache
        from django.conf import settings
        from .adapters import get_adapter

        logger = logging.getLogger('radio')

        cached = cache.get(self.CACHE_KEY)
        if cached is not None:
            return JsonResponse(cached)

        provider_key = getattr(settings, 'STREAM_PROVIDER', 'broadcastindo').upper()
        api_url = getattr(settings, 'STREAM_API_URL', '')
        station_name = getattr(settings, 'STREAM_STATION_NAME', 'Kabulhaden')
        cache_ttl = getattr(settings, 'STREAM_CACHE_TTL', 20)

        try:
            adapter_class = get_adapter(provider_key)
            adapter = adapter_class(api_url=api_url, timeout=8)

            np = adapter.get_now_playing()
            listener_data = adapter.get_listener_count()

            # Extract the audio stream URL from the provider's raw response.
            # AzuraCast / Siar.us includes station.listen_url in the nowplaying payload.
            stream_url = ''
            raw = np.raw_response
            if isinstance(raw, dict):
                station_block = raw.get('station', {})
                stream_url = station_block.get('listen_url', '')

            is_offline = np.stream_status == 'OFFLINE'
            status = 'offline' if is_offline else 'live'

            data = {
                'status': status,
                'station': station_name,
                'program': None,  # Live schedule wire-up planned for a future sprint
                'title': np.song_title or 'Kabulhaden Radio',
                'artist': np.artist or 'Siaran Langsung',
                'cover': np.artwork or '',
                'listeners': listener_data.current_listeners,
                'started_at': np.started_at.isoformat() if np.started_at else None,
                'stream_url': stream_url,
                'is_live': not is_offline,
                'provider': provider_key.lower(),
            }

        except Exception as exc:
            logger.error('LiveRadioAPIView: failed to fetch live data — %s', exc)
            data = {
                'status': 'offline',
                'station': station_name,
                'program': None,
                'title': 'Kabulhaden Radio',
                'artist': 'Siaran Langsung',
                'cover': '',
                'listeners': 0,
                'started_at': None,
                'stream_url': '',
                'is_live': False,
                'provider': provider_key.lower(),
                'error': 'Unable to retrieve live data',
            }

        cache.set(self.CACHE_KEY, data, cache_ttl)
        return JsonResponse(data)
