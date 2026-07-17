import logging
from typing import Dict, Optional, Type
from .base import (
    BaseProvider, StreamingProvider, StorageProvider, EmailProvider,
    AIProvider, NotificationProvider, AnalyticsProvider, PaymentProvider,
)

logger = logging.getLogger('platform')

# Global provider registry
_PROVIDER_REGISTRY: Dict[str, Dict[str, Type[BaseProvider]]] = {
    'STREAMING': {},
    'STORAGE': {},
    'EMAIL': {},
    'AI': {},
    'NOTIFICATION': {},
    'ANALYTICS': {},
    'PAYMENT': {},
}


def register_provider(category: str, slug: str, provider_class: Type[BaseProvider]):
    """Register a provider implementation in the global registry."""
    if category not in _PROVIDER_REGISTRY:
        _PROVIDER_REGISTRY[category] = {}
    _PROVIDER_REGISTRY[category][slug] = provider_class
    logger.debug(f"Registered provider: {category}/{slug}")


def get_provider_class(category: str, slug: str) -> Optional[Type[BaseProvider]]:
    """Get a provider class by category and slug."""
    return _PROVIDER_REGISTRY.get(category, {}).get(slug)


def list_providers(category: Optional[str] = None) -> Dict[str, list]:
    """List all registered providers, optionally filtered by category."""
    if category:
        providers = _PROVIDER_REGISTRY.get(category, {})
        return {category: list(providers.keys())}
    return {cat: list(provs.keys()) for cat, provs in _PROVIDER_REGISTRY.items()}


def get_provider_for_partner(partner, category: str) -> Optional[BaseProvider]:
    """Get a configured provider instance for a partner.

    Resolution order:
    1. Partner provider_overrides for this category
    2. Global default (first registered provider)
    """
    # 1. Check partner overrides
    provider_slug = partner.get_provider(category) if hasattr(partner, 'get_provider') else None
    if provider_slug:
        provider_class = get_provider_class(category, provider_slug)
        if provider_class:
            return _instantiate_provider(provider_class, partner, category)

    # 2. Fall back to global default
    providers = _PROVIDER_REGISTRY.get(category, {})
    if providers:
        first_slug = next(iter(providers))
        return _instantiate_provider(providers[first_slug], partner, category)

    return None


def _instantiate_provider(provider_class: Type[BaseProvider], partner, category: str) -> BaseProvider:
    """Create and configure a provider instance for a partner."""
    instance = provider_class()
    config = _get_partner_provider_config(partner, category)
    try:
        instance.configure(config)
    except Exception as e:
        logger.error(f"Failed to configure provider {instance.name}: {e}")
    return instance


def _get_partner_provider_config(partner, category: str) -> Dict:
    """Extract provider configuration from partner's settings."""
    if hasattr(partner, 'provider_overrides') and isinstance(partner.provider_overrides, dict):
        return partner.provider_overrides.get(category, {})
    return {}
