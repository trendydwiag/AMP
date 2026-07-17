import logging
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Optional, Dict, Any
from django.utils import timezone

logger = logging.getLogger('radio')


@dataclass
class NowPlayingData:
    song_title: str = ''
    artist: str = ''
    album: str = ''
    artwork: str = ''
    duration: int = 0
    elapsed: int = 0
    started_at: Optional[timezone.datetime] = None
    ends_at: Optional[timezone.datetime] = None
    stream_status: str = 'UNKNOWN'
    raw_response: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ListenerData:
    current_listeners: int = 0
    peak_listeners: int = 0
    raw_response: Dict[str, Any] = field(default_factory=dict)


@dataclass
class HealthCheckData:
    response_time: float = 0.0
    http_status: int = 0
    provider_status: str = 'DOWN'
    stream_bitrate: int = 0
    stream_format: str = ''
    error_message: str = ''
    raw_response: Dict[str, Any] = field(default_factory=dict)


class RadioProviderAdapter(ABC):
    """Abstract base adapter defining the contract for all radio provider integrations."""

    def __init__(self, api_url: str = '', stream_url: str = '', metadata_url: str = '',
                 listener_url: str = '', healthcheck_url: str = '', username: str = '',
                 password: str = '', timeout: int = 10, **kwargs) -> None:
        self.api_url = api_url
        self.stream_url = stream_url
        self.metadata_url = metadata_url
        self.listener_url = listener_url
        self.healthcheck_url = healthcheck_url
        self.username = username
        self.password = password
        self.timeout = timeout
        self.extra_config = kwargs

    @abstractmethod
    def get_now_playing(self) -> NowPlayingData:
        """Fetch current track information from the provider."""
        ...

    @abstractmethod
    def get_listener_count(self) -> ListenerData:
        """Fetch current and peak listener counts."""
        ...

    @abstractmethod
    def check_health(self) -> HealthCheckData:
        """Perform a health check on the stream."""
        ...

    def _make_request(self, url: str, timeout: Optional[int] = None) -> Dict[str, Any]:
        """Perform an HTTP GET request with timeout handling."""
        import requests
        from requests.auth import HTTPBasicAuth

        timeout = timeout or self.timeout
        auth = HTTPBasicAuth(self.username, self.password) if self.username else None

        try:
            start = time.monotonic()
            response = requests.get(
                url, timeout=timeout, auth=auth,
                headers={'User-Agent': 'Kabulhaden-RadioEngine/1.0'}
            )
            elapsed_ms = (time.monotonic() - start) * 1000
            response.raise_for_status()
            return {
                'data': response.text,
                'status_code': response.status_code,
                'response_time': elapsed_ms,
                'headers': dict(response.headers),
                'json': response.json() if response.headers.get('content-type', '').startswith('application/json') else None,
            }
        except requests.exceptions.Timeout:
            logger.warning(f"Timeout requesting {url}")
            return {'data': '', 'status_code': 0, 'response_time': timeout * 1000, 'error': 'timeout'}
        except requests.exceptions.ConnectionError as e:
            logger.warning(f"Connection error requesting {url}: {e}")
            return {'data': '', 'status_code': 0, 'response_time': 0, 'error': 'connection_error'}
        except Exception as e:
            logger.error(f"Request error for {url}: {e}")
            return {'data': '', 'status_code': 0, 'response_time': 0, 'error': str(e)}
