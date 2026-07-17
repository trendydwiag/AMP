import json
import logging
from typing import Dict, Any
from .base import RadioProviderAdapter, NowPlayingData, ListenerData, HealthCheckData

logger = logging.getLogger('radio')


class AzuraCastAdapter(RadioProviderAdapter):
    """Adapter for AzuraCast radio server via its REST API."""

    def _get_api_json(self, endpoint: str) -> Dict[str, Any]:
        url = f"{self.api_url.rstrip('/')}/{endpoint.lstrip('/')}"
        result = self._make_request(url)
        if result.get('error'):
            return {}
        try:
            return json.loads(result.get('data', '{}'))
        except (json.JSONDecodeError, TypeError):
            return {}

    def _get_station_shortcode(self) -> str:
        if self.extra_config.get('station_shortcode'):
            return self.extra_config['station_shortcode']
        if self.api_url:
            parts = self.api_url.rstrip('/').split('/')
            for i, part in enumerate(parts):
                if part == 'api' and i + 3 < len(parts):
                    return parts[i + 2]
        return 'default'

    def get_now_playing(self) -> NowPlayingData:
        sc = self._get_station_shortcode()
        data = self._get_api_json(f"station/{sc}/nowplaying")
        if not data:
            return NowPlayingData(stream_status='OFFLINE', raw_response={})

        np = data.get('now_playing', data)
        song = np.get('song', {})
        live = np.get('live', {})
        is_live = live.get('is_live', False)

        status = 'LIVE_DJ' if is_live else 'AUTO_DJ'
        if np.get('is_edit'):
            status = 'ONLINE'

        duration = int(np.get('duration', 0))
        elapsed = int(np.get('elapsed', 0))

        return NowPlayingData(
            song_title=song.get('title', ''),
            artist=song.get('artist', ''),
            album=song.get('album', ''),
            artwork=song.get('art', ''),
            duration=duration,
            elapsed=elapsed,
            stream_status=status,
            raw_response=data,
        )

    def get_listener_count(self) -> ListenerData:
        sc = self._get_station_shortcode()
        data = self._get_api_json(f"station/{sc}/listeners")
        listeners = data if isinstance(data, list) else data.get('listeners', [])
        return ListenerData(
            current_listeners=len(listeners),
            peak_listeners=0,
            raw_response=data,
        )

    def check_health(self) -> HealthCheckData:
        sc = self._get_station_shortcode()
        result = self._make_request(f"{self.api_url.rstrip('/')}/station/{sc}/status")
        if result.get('error'):
            return HealthCheckData(
                response_time=result.get('response_time', 0),
                http_status=result.get('status_code', 0),
                provider_status='DOWN',
                error_message=result['error'],
            )
        try:
            data = json.loads(result.get('data', '{}'))
            is_running = data.get('is_running', False)
            return HealthCheckData(
                response_time=result.get('response_time', 0),
                http_status=result.get('status_code', 0),
                provider_status='HEALTHY' if is_running else 'DOWN',
                raw_response=data,
            )
        except (json.JSONDecodeError, TypeError):
            return HealthCheckData(
                response_time=result.get('response_time', 0),
                http_status=result.get('status_code', 0),
                provider_status='DEGRADED',
            )
