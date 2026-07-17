"""
Media Pipeline — Storage Abstraction
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Provides a backend-agnostic interface for storing media files.
Swap backends without changing the pipeline or model layer.

Supported backends (current and planned):
    local       — Django FileSystemStorage (default, active)
    s3          — Amazon S3 (stub — implement when needed)
    r2          — Cloudflare R2 (stub)
    minio       — MinIO (stub)

Configuration:
    Backend is resolved via MediaSettings.storage_backend (DB) with
    MEDIA_STORAGE_BACKEND env-var as fallback, defaulting to 'local'.
"""
from __future__ import annotations

import logging
from abc import ABC, abstractmethod

from django.core.files.storage import default_storage
from django.core.files.base import File

logger = logging.getLogger(__name__)


# ── Base interface ───────────────────────────────────────────────────────────
class BaseStorageBackend(ABC):
    """
    Abstract base for all storage backends.
    Each backend must implement save(), delete(), url(), and exists().
    """

    @property
    @abstractmethod
    def backend_name(self) -> str:
        """Short identifier used in MediaFile.storage_backend field."""

    @abstractmethod
    def save(self, name: str, content: File) -> str:
        """
        Persist `content` under `name` and return the stored path.
        The returned path is what gets saved to MediaFile.file.name.
        """

    @abstractmethod
    def delete(self, name: str) -> None:
        """Delete the file at `name`. Silent if not found."""

    @abstractmethod
    def url(self, name: str) -> str:
        """Return a publicly accessible URL for `name`."""

    @abstractmethod
    def exists(self, name: str) -> bool:
        """Return True if a file exists at `name`."""

    def __repr__(self) -> str:
        return f"<StorageBackend:{self.backend_name}>"


# ── Local (FileSystem) ───────────────────────────────────────────────────────
class LocalStorageBackend(BaseStorageBackend):
    """
    Wraps Django's default_storage (FileSystemStorage in dev/prod without S3).
    All MEDIA_ROOT configuration stays in Django settings — this class adds no new config.
    """

    @property
    def backend_name(self) -> str:
        return 'local'

    def save(self, name: str, content: File) -> str:
        return default_storage.save(name, content)

    def delete(self, name: str) -> None:
        try:
            if default_storage.exists(name):
                default_storage.delete(name)
        except Exception as exc:
            logger.warning("LocalStorageBackend.delete(%r) failed: %s", name, exc)

    def url(self, name: str) -> str:
        return default_storage.url(name)

    def exists(self, name: str) -> bool:
        return default_storage.exists(name)


# ── S3 (stub) ────────────────────────────────────────────────────────────────
class S3StorageBackend(BaseStorageBackend):
    """
    Amazon S3 backend — STUB.
    Implement when django-storages is installed and AWS credentials are configured.

    Required packages: boto3, django-storages
    Required env vars: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_S3_BUCKET_NAME
    """

    @property
    def backend_name(self) -> str:
        return 's3'

    def save(self, name: str, content: File) -> str:
        raise NotImplementedError(
            "S3StorageBackend is not yet implemented. "
            "Install django-storages and configure AWS credentials."
        )

    def delete(self, name: str) -> None:
        raise NotImplementedError("S3StorageBackend.delete() not implemented.")

    def url(self, name: str) -> str:
        raise NotImplementedError("S3StorageBackend.url() not implemented.")

    def exists(self, name: str) -> bool:
        raise NotImplementedError("S3StorageBackend.exists() not implemented.")


# ── Cloudflare R2 (stub) ──────────────────────────────────────────────────────
class CloudflareR2Backend(BaseStorageBackend):
    """
    Cloudflare R2 backend — STUB.
    R2 is S3-compatible; implement by pointing S3StorageBackend at R2 endpoint.

    Required env vars: R2_ACCOUNT_ID, R2_ACCESS_KEY_ID, R2_SECRET_ACCESS_KEY, R2_BUCKET_NAME
    """

    @property
    def backend_name(self) -> str:
        return 'r2'

    def save(self, name: str, content: File) -> str:
        raise NotImplementedError("CloudflareR2Backend is not yet implemented.")

    def delete(self, name: str) -> None:
        raise NotImplementedError("CloudflareR2Backend.delete() not implemented.")

    def url(self, name: str) -> str:
        raise NotImplementedError("CloudflareR2Backend.url() not implemented.")

    def exists(self, name: str) -> bool:
        raise NotImplementedError("CloudflareR2Backend.exists() not implemented.")


# ── MinIO (stub) ──────────────────────────────────────────────────────────────
class MinIOBackend(BaseStorageBackend):
    """
    MinIO backend — STUB.
    MinIO is S3-compatible; can reuse the S3 backend with a custom endpoint.

    Required env vars: MINIO_ENDPOINT, MINIO_ACCESS_KEY, MINIO_SECRET_KEY, MINIO_BUCKET
    """

    @property
    def backend_name(self) -> str:
        return 'minio'

    def save(self, name: str, content: File) -> str:
        raise NotImplementedError("MinIOBackend is not yet implemented.")

    def delete(self, name: str) -> None:
        raise NotImplementedError("MinIOBackend.delete() not implemented.")

    def url(self, name: str) -> str:
        raise NotImplementedError("MinIOBackend.url() not implemented.")

    def exists(self, name: str) -> bool:
        raise NotImplementedError("MinIOBackend.exists() not implemented.")


# ── Factory ───────────────────────────────────────────────────────────────────
_BACKEND_REGISTRY: dict[str, type[BaseStorageBackend]] = {
    'local': LocalStorageBackend,
    's3': S3StorageBackend,
    'r2': CloudflareR2Backend,
    'minio': MinIOBackend,
}


def get_storage_backend(backend_name: str | None = None) -> BaseStorageBackend:
    """
    Resolve and instantiate the correct storage backend.

    Resolution order:
        1. Explicit `backend_name` argument
        2. MediaSettings.storage_backend from the database
        3. 'local' as the final default

    Args:
        backend_name: Optional explicit backend identifier.

    Returns:
        An instance of the resolved BaseStorageBackend.
    """
    if not backend_name:
        try:
            from apps.settings.models import MediaSettings
            settings = MediaSettings.load()
            backend_name = getattr(settings, 'storage_backend', 'local') or 'local'
        except Exception:
            backend_name = 'local'

    cls = _BACKEND_REGISTRY.get(backend_name)
    if cls is None:
        logger.warning(
            "Unknown storage backend %r — falling back to LocalStorageBackend.", backend_name
        )
        cls = LocalStorageBackend

    return cls()


def register_storage_backend(name: str, cls: type[BaseStorageBackend]) -> None:
    """
    Register a custom storage backend.
    Call this in your app's AppConfig.ready() if adding a new backend.
    """
    _BACKEND_REGISTRY[name] = cls
    logger.info("Registered custom storage backend: %r → %s", name, cls.__name__)
