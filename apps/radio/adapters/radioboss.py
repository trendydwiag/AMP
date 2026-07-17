import json
import logging
from typing import Dict, Any
from .base import RadioProviderAdapter, NowPlayingData, ListenerData, HealthCheckData

logger = logging.getLogger('radio')


class RadioBossAdapter(RadioProviderAdapter):
    """Adapter for RadioBoss Advance server via its HTTP API."""

    def _get_json(self, url: str) -> Dict[str, Any]:
        result = self._make_request(url)
        if result.get('error'):
            return {}
        json_data = result.get('json')
        if json_data is not None:
            return json_data
        try:
            return json.loads(result.get('data', '{}'))
        except (json.JSONDecodeError, TypeError):
            return {}

    def get_now_playing(self) -> NowPlayingData:
        url = self.metadata_url or f"{self.api_url}/api/stats"
        data = self._get_json(url)
        if not data:
            return NowPlayingData(stream_status='OFFLINE', raw_response={})

        status = 'OFFLINE'
        if data.get('onair') or data.get('status') == 'playing':
            status = 'ONLINE'

        current = data.get('current', data)
        return NowPlayingData(
            song_title=current.get('title', current.get('song', '')),
            artist=current.get('artist', ''),
            album=current.get('album', ''),
            artwork=current.get('artwork', current.get('cover', '')),
            duration=int(current.get('duration', 0)),
            elapsed=int(current.get('elapsed', 0)),
            stream_status=status,
            raw_response=data,
        )

    def get_listener_count(self) -> ListenerData:
        url = self.listener_url or f"{self.api_url}/api/listeners"
        data = self._get_json(url)
        if not data:
            return ListenerData()
        return ListenerData(
            current_listeners=int(data.get('listeners', data.get('current', 0))),
            peak_listeners=int(data.get('peak', data.get('max', 0))),
            raw_response=data,
        )

    def check_health(self) -> HealthCheckData:
        url = self.healthcheck_url or f"{self.api_url}/api/stats"
        result = self._make_request(url)
        if result.get('error'):
            return HealthCheckData(
                response_time=result.get('response_time', 0),
                http_status=result.get('status_code', 0),
                provider_status='DOWN',
                error_message=result['error'],
            )
        return HealthCheckData(
            response_time=result.get('response_time', 0),
            http_status=result.get('status_code', 0),
            provider_status='HEALTHY',
            stream_format='mp3',
            raw_response={'status_code': result.get('status_code')},
        )
