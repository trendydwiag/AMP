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
        ice = data.get('icestats', {})

        # Icecast uses 'source' key (not 'mount') for active stream sources.
        # When one source is connected it's a dict; when multiple, a list.
        # Some older/patched builds may use 'mount' — check both.
        raw = ice.get('source') or ice.get('mount')
        if raw is None:
            return {}
        mounts = [raw] if isinstance(raw, dict) else list(raw)

        # Try to match by mount path extracted from stream_url
        stream_path = ''
        if self.stream_url:
            parts = self.stream_url.rstrip('/').split('/')
            stream_path = '/' + parts[-1] if parts else ''

        for mount in mounts:
            # Icecast 'source' entries use 'listenurl' or 'mount' for identification
            listen = mount.get('listenurl', '')
            mnt = mount.get('mount', '')
            if stream_path:
                if listen.endswith(stream_path) or mnt == stream_path:
                    return mount
        # No exact match — return first available source
        return mounts[0] if mounts else {}

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
        ice = data.get('icestats', {})
        mount = self._find_mount(data)
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
