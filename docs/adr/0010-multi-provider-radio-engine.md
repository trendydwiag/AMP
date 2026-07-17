# 0010. Use Adapter Pattern for Radio Providers

**Status:** Accepted
**Date:** 2024-07-15

## Context

The radio module must integrate with multiple streaming server providers:

- **AzuraCast** — REST API for now-playing, listeners, status
- **Icecast** — JSON status API and mount point data
- **Shoutcast** — ICY metadata protocol and admin interface scraping
- **RadioBOSS** — HTTP API for stats and current track

Each provider has different API formats, authentication methods, and data structures. The CMS should not be tightly coupled to any single provider, and adding new providers should not require changing service-layer code.

## Decision

We use the **Adapter pattern** with an abstract base class and concrete adapter implementations.

### Abstract Base Adapter

```python
# apps/radio/adapters/base.py
class RadioProviderAdapter(ABC):
    def __init__(self, api_url, stream_url, metadata_url, listener_url,
                 healthcheck_url, username, password, timeout, **kwargs): ...

    @abstractmethod
    def get_now_playing(self) -> NowPlayingData: ...

    @abstractmethod
    def get_listener_count(self) -> ListenerData: ...

    @abstractmethod
    def check_health(self) -> HealthCheckData: ...
```

### Data Classes

```python
@dataclass
class NowPlayingData:
    song_title: str = ''
    artist: str = ''
    album: str = ''
    artwork: str = ''
    duration: int = 0
    elapsed: int = 0
    stream_status: str = 'UNKNOWN'
    raw_response: Dict[str, Any] = field(default_factory=dict)
```

### Concrete Adapters

| Adapter | File | Provider |
|---------|------|----------|
| `AzuraCastAdapter` | `adapters/azuracast.py` | AzuraCast REST API |
| `IcecastAdapter` | `adapters/icecast.py` | Icecast JSON status |
| `ShoutcastAdapter` | `adapters/shoutcast.py` | ICY metadata protocol |
| `RadioBossAdapter` | `adapters/radioboss.py` | RadioBOSS HTTP API |

### Adapter Selection

The `get_adapter()` factory function in `adapters/__init__.py` selects the appropriate adapter based on `RadioProvider.provider_type`:

```python
from utils.choices import RadioProviderType

ADAPTER_MAP = {
    RadioProviderType.AZURACAST: AzuraCastAdapter,
    RadioProviderType.ICECAST: IcecastAdapter,
    RadioProviderType.SHOUTCAST: ShoutcastAdapter,
    RadioProviderType.RADIOBOSS: RadioBossAdapter,
}
```

## Consequences

**Positive:**

- Adding a new provider requires only a new adapter class — no service layer changes.
- All adapters return the same data classes (`NowPlayingData`, `ListenerData`, `HealthCheckData`).
- The base adapter provides shared HTTP request handling with timeout and error management.
- Adapters are independently testable with mock HTTP responses.
- Provider-specific quirks (ICY metadata parsing, mount point selection) are isolated.

**Negative:**

- Each new provider requires understanding its API and writing ~80-100 lines of adapter code.
- The adapter layer adds indirection when debugging API issues.
- Raw responses are preserved in `raw_response` for debugging, adding storage overhead.

**Mitigations:**

- Base adapter's `_make_request()` handles common HTTP patterns (auth, timeout, error catching).
- Four adapters are already implemented, providing templates for future additions.
- `raw_response` JSONField is stored in `NowPlayingCache` for post-mortem analysis.
