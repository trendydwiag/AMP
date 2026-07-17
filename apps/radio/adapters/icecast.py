import json
import re
import logging
from typing import Dict, Any
from .base import RadioProviderAdapter, NowPlayingData, ListenerData, HealthCheckData

logger = logging.getLogger('radio')


class IcecastAdapter(RadioProviderAdapter):
    """Adapter for Icecast streaming server via its JSON status API."""

    def _get_status(self) -> Dict[str, Any]:
        url = self.api_url or self.metadata_url
        if not url:
            return {}
        result = self._make_request(url)
        if result.get('error'):
            return {}
        try:
            return json.loads(result.get('data', '{}'))
        except (json.JSONDecodeError, TypeError):
            return {}

    def _find_mount(self, data: Dict[str, Any]) -> Dict[str, Any]:
        mounts = data.get('icestats', {}).get('mount', [])
        if isinstance(mounts, dict):
            mounts = [mounts]
        stream_path = ''
        if self.stream_url:
            parts = self.stream_url.rstrip('/').split('/')
            stream_path = '/' + parts[-1] if parts else ''
        for mount in mounts:
            mnt = mount.get('mount', '')
            if stream_path and mnt == stream_path:
                return mount
        if mounts:
            return mounts[0]
        return {}

    def get_now_playing(self) -> NowPlayingData:
        data = self._get_status()
        if not data:
            return NowPlayingData(stream_status='OFFLINE', raw_response={})

        ice = data.get('icestats', {})
        mount = self._find_mount(data)

        title = mount.get('title', mount.get('song', ''))
        artist = ''
        if ' - ' in title:
            parts = title.split(' - ', 1)
            artist = parts[0].strip()
            title = parts[1].strip()

        server_stats = ice.get('server_stats', {})
        status = 'ONLINE' if mount else 'OFFLINE'

        return NowPlayingData(
            song_title=title,
            artist=artist,
            album=mount.get('genre', ''),
            artwork=mount.get('artwork', ''),
            duration=0,
            elapsed=0,
            stream_status=status,
            raw_response=data,
        )

    def get_listener_count(self) -> ListenerData:
        data = self._get_status()
        if not data:
            return ListenerData()
        mount = self._find_mount(data)
        listeners = mount.get('listeners', ice.get('listener_peak', 0))
        ice = data.get('icestats', {})
        return ListenerData(
            current_listeners=int(mount.get('listeners', 0)),
            peak_listeners=int(ice.get('listener_peak', 0)),
            raw_response=data,
        )

    def check_health(self) -> HealthCheckData:
        url = self.api_url or self.metadata_url
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
            raw_response={'status_code': result.get('status_code')},
        )
