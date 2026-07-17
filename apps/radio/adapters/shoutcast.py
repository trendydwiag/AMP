import re
import logging
from typing import Dict, Any
from .base import RadioProviderAdapter, NowPlayingData, ListenerData, HealthCheckData

logger = logging.getLogger('radio')


class ShoutcastAdapter(RadioProviderAdapter):
    """Adapter for Shoutcast server via ICY metadata and admin interface."""

    def _parse_icy_metadata(self, raw: str) -> Dict[str, str]:
        result = {}
        match = re.search(r"StreamTitle='([^']*)'", raw)
        if match:
            title_str = match.group(1)
            if ' - ' in title_str:
                parts = title_str.split(' - ', 1)
                result['artist'] = parts[0].strip()
                result['title'] = parts[1].strip()
            else:
                result['title'] = title_str
                result['artist'] = ''
        match_len = re.search(r'StreamLength=(\d+)', raw)
        if match_len:
            result['duration'] = match_len.group(1)
        return result

    def _get_icy_data(self) -> Dict[str, Any]:
        import requests
        url = self.stream_url
        if not url:
            return {}
        auth = None
        if self.username:
            from requests.auth import HTTPBasicAuth
            auth = HTTPBasicAuth(self.username, self.password)
        try:
            response = requests.get(
                url, timeout=self.timeout, stream=True, auth=auth,
                headers={'Icy-MetaData': '1', 'User-Agent': 'Kabulhaden-RadioEngine/1.0'}
            )
            icy_headers = {k: v for k, v in response.headers.items() if k.lower().startswith('icy-')}
            content_type = response.headers.get('Content-Type', '')
            meta_int = int(icy_headers.get('icy-metaint', 0))
            raw_meta = b''
            if meta_int > 0:
                chunk = response.raw.read(meta_int)
                length = int.from_bytes(response.raw.read(1), 'big') * 16
                raw_meta = response.raw.read(length)
            else:
                raw_meta = response.raw.read(4096)
            response.close()
            return {
                'icy_headers': icy_headers,
                'content_type': content_type,
                'raw_meta': raw_meta.decode('utf-8', errors='ignore'),
                'bitrate': int(icy_headers.get('icy-br', 0)),
            }
        except Exception as e:
            logger.warning(f"Shoutcast ICY error: {e}")
            return {}

    def get_now_playing(self) -> NowPlayingData:
        icy = self._get_icy_data()
        if not icy or not icy.get('raw_meta'):
            return NowPlayingData(stream_status='OFFLINE', raw_response=icy or {})

        parsed = self._parse_icy_metadata(icy['raw_meta'])
        status = 'ONLINE' if parsed.get('title') else 'OFFLINE'

        return NowPlayingData(
            song_title=parsed.get('title', ''),
            artist=parsed.get('artist', ''),
            album='',
            artwork='',
            duration=int(parsed.get('duration', 0)),
            elapsed=0,
            stream_status=status,
            raw_response=icy,
        )

    def get_listener_count(self) -> ListenerData:
        if not self.listener_url:
            return ListenerData()
        result = self._make_request(self.listener_url)
        if result.get('error'):
            return ListenerData()
        text = result.get('data', '')
        current = 0
        peak = 0
        match = re.search(r'Current Listeners:\s*(\d+)', text)
        if match:
            current = int(match.group(1))
        match = re.search(r'Peak Listeners:\s*(\d+)', text)
        if match:
            peak = int(match.group(1))
        return ListenerData(current_listeners=current, peak_listeners=peak)

    def check_health(self) -> HealthCheckData:
        result = self._make_request(self.stream_url)
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
