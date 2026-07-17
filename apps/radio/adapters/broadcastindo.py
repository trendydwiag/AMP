"""
Broadcastindo Adapter — Temporary live-streaming integration for AMP Studio.

This adapter fetches now-playing data from Broadcastindo (hosted on Siar.us),
which exposes an AzuraCast-compatible /api/nowplaying/<station> endpoint.

Architecture note
-----------------
This is a TEMPORARY adapter replaced later by the official AMP Streaming
Connector (BroadcastindoConnector). It is deliberately thin: provider-specific
field names never escape this file. All callers consume the normalized
NowPlayingData / ListenerData types.

To swap providers:
  1. Create apps/radio/adapters/<provider>.py implementing RadioProviderAdapter
  2. Set STREAM_PROVIDER env var (or settings key) to the new key
  3. Register the key in ADAPTER_MAP in __init__.py
  4. No UI, template, or JS changes required.
"""

import json
import logging
from .base import RadioProviderAdapter, NowPlayingData, ListenerData, HealthCheckData

logger = logging.getLogger('radio')


class BroadcastindoAdapter(RadioProviderAdapter):
    """
    Adapter for Broadcastindo radio hosting via Siar.us (AzuraCast-compatible API).

    api_url must be the full nowplaying endpoint URL, e.g.
        https://a7.siar.us/api/nowplaying/kabulhaden

    A single GET to that URL returns both track metadata and listener counts,
    so get_now_playing() and get_listener_count() share the same payload.
    """

    def _fetch_nowplaying_data(self) -> dict:
        """Fetch and parse the nowplaying JSON from the provider endpoint."""
        if not self.api_url:
            logger.warning("BroadcastindoAdapter: api_url is not configured")
            return {}

        result = self._make_request(self.api_url)
        if result.get('error'):
            logger.warning(
                "BroadcastindoAdapter: upstream error fetching %s — %s",
                self.api_url, result['error'],
            )
            return {}

        try:
            return json.loads(result.get('data', '{}'))
        except (json.JSONDecodeError, TypeError) as exc:
            logger.error("BroadcastindoAdapter: JSON parse error — %s", exc)
            return {}

    def get_now_playing(self) -> NowPlayingData:
        """Return normalized now-playing track metadata."""
        data = self._fetch_nowplaying_data()
        if not data:
            return NowPlayingData(stream_status='OFFLINE', raw_response={})

        # AzuraCast /api/nowplaying/<station> response shape
        now_playing = data.get('now_playing', {})
        song = now_playing.get('song', {})
        live = data.get('live', {})
        is_live_dj = live.get('is_live', False)

        stream_status = 'LIVE_DJ' if is_live_dj else 'AUTO_DJ'
        duration = int(now_playing.get('duration', 0))
        elapsed = int(now_playing.get('elapsed', 0))

        return NowPlayingData(
            song_title=song.get('title', ''),
            artist=song.get('artist', ''),
            album=song.get('album', ''),
            artwork=song.get('art', ''),
            duration=duration,
            elapsed=elapsed,
            stream_status=stream_status,
            raw_response=data,
        )

    def get_listener_count(self) -> ListenerData:
        """Return listener count from the same nowplaying payload."""
        data = self._fetch_nowplaying_data()
        if not data:
            return ListenerData(current_listeners=0, peak_listeners=0, raw_response={})

        listeners = data.get('listeners', {})
        if isinstance(listeners, dict):
            current = int(listeners.get('current', 0))
            # Siar.us exposes 'unique' not 'peak'
            peak = int(listeners.get('unique', current))
        else:
            current = 0
            peak = 0

        return ListenerData(
            current_listeners=current,
            peak_listeners=peak,
            raw_response=data,
        )

    def check_health(self) -> HealthCheckData:
        """Quick health check — reuses the nowplaying endpoint."""
        if not self.api_url:
            return HealthCheckData(provider_status='DOWN', error_message='api_url not configured')

        result = self._make_request(self.api_url)
        if result.get('error'):
            return HealthCheckData(
                response_time=result.get('response_time', 0),
                http_status=result.get('status_code', 0),
                provider_status='DOWN',
                error_message=result['error'],
            )

        return HealthCheckData(
            response_time=result.get('response_time', 0),
            http_status=result.get('status_code', 200),
            provider_status='HEALTHY',
        )
