import os
import logging
from typing import Any, Dict
from django.conf import settings
from django.core.files.storage import default_storage
from .base import StorageProvider, ProviderResult

logger = logging.getLogger('platform')


class LocalStorageProvider(StorageProvider):
    """Default local filesystem storage provider."""

    name = 'local'
    description = 'Penyimpanan lokal di server (default)'

    def __init__(self):
        self.media_root = ''
        self.max_file_size = 10 * 1024 * 1024  # 10MB default

    def configure(self, config: Dict[str, Any]) -> None:
        self.media_root = config.get('media_root', getattr(settings, 'MEDIA_ROOT', ''))
        self.max_file_size = config.get('max_file_size_mb', 10) * 1024 * 1024

    def upload(self, file_obj: Any, path: str, **kwargs) -> ProviderResult:
        try:
            saved_path = default_storage.save(path, file_obj)
            return ProviderResult(
                success=True,
                data={'path': saved_path, 'url': default_storage.url(saved_path)},
                provider_name=self.name
            )
        except Exception as e:
            logger.error(f"Local storage upload error: {e}")
            return ProviderResult(success=False, error=str(e), provider_name=self.name)

    def delete(self, path: str) -> ProviderResult:
        try:
            if default_storage.exists(path):
                default_storage.delete(path)
                return ProviderResult(success=True, provider_name=self.name)
            return ProviderResult(success=False, error='File not found', provider_name=self.name)
        except Exception as e:
            logger.error(f"Local storage delete error: {e}")
            return ProviderResult(success=False, error=str(e), provider_name=self.name)

    def get_url(self, path: str, **kwargs) -> ProviderResult:
        try:
            url = default_storage.url(path)
            return ProviderResult(success=True, data=url, provider_name=self.name)
        except Exception as e:
            return ProviderResult(success=False, error=str(e), provider_name=self.name)

    def get_usage(self) -> ProviderResult:
        try:
            total_size = 0
            file_count = 0
            for root, dirs, files in os.walk(self.media_root):
                for f in files:
                    fp = os.path.join(root, f)
                    if os.path.isfile(fp):
                        total_size += os.path.getsize(fp)
                        file_count += 1
            return ProviderResult(
                success=True,
                data={
                    'total_bytes': total_size,
                    'total_mb': round(total_size / (1024 * 1024), 2),
                    'file_count': file_count,
                },
                provider_name=self.name
            )
        except Exception as e:
            return ProviderResult(success=False, error=str(e), provider_name=self.name)

    def health_check(self) -> ProviderResult:
        try:
            accessible = os.access(self.media_root, os.W_OK) if self.media_root else False
            return ProviderResult(
                success=accessible,
                data={'writable': accessible},
                provider_name=self.name
            )
        except Exception as e:
            return ProviderResult(success=False, error=str(e), provider_name=self.name)
