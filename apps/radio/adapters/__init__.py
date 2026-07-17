from .base import RadioProviderAdapter, NowPlayingData, ListenerData, HealthCheckData
from .radioboss import RadioBossAdapter
from .icecast import IcecastAdapter
from .shoutcast import ShoutcastAdapter
from .azuracast import AzuraCastAdapter
from .broadcastindo import BroadcastindoAdapter

ADAPTER_MAP = {
    'RADIOBOSS': RadioBossAdapter,
    'ICECAST': IcecastAdapter,
    'SHOUTCAST': ShoutcastAdapter,
    'AZURACAST': AzuraCastAdapter,
    # Temporary adapter — see broadcastindo.py for replacement instructions
    'BROADCASTINDO': BroadcastindoAdapter,
}


def get_adapter(provider_type: str) -> type:
    adapter_class = ADAPTER_MAP.get(provider_type)
    if not adapter_class:
        raise ValueError(f"Unknown provider type: {provider_type}")
    return adapter_class
