from .base import (
    BaseProvider, StreamingProvider, StorageProvider, EmailProvider,
    AIProvider, NotificationProvider, AnalyticsProvider, PaymentProvider,
    ProviderResult,
)
from .registry import (
    register_provider, get_provider_class, list_providers,
    get_provider_for_partner,
)

# Auto-register default providers
from .local_storage import LocalStorageProvider
from .django_email import DjangoEmailProvider

register_provider('STORAGE', 'local', LocalStorageProvider)
register_provider('EMAIL', 'django', DjangoEmailProvider)

__all__ = [
    'BaseProvider', 'StreamingProvider', 'StorageProvider', 'EmailProvider',
    'AIProvider', 'NotificationProvider', 'AnalyticsProvider', 'PaymentProvider',
    'ProviderResult',
    'register_provider', 'get_provider_class', 'list_providers',
    'get_provider_for_partner',
]
