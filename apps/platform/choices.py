from django.db import models


class PartnerStatus(models.TextChoices):
    ACTIVE = 'ACTIVE', 'Aktif'
    INACTIVE = 'INACTIVE', 'Tidak Aktif'
    SUSPENDED = 'SUSPENDED', 'Ditangguhkan'
    PENDING = 'PENDING', 'Menunggu Persetujuan'


class PartnerTier(models.TextChoices):
    ENTERPRISE = 'ENTERPRISE', 'Enterprise'
    PROFESSIONAL = 'PROFESSIONAL', 'Professional'
    STARTER = 'STARTER', 'Starter'
    COMMUNITY = 'COMMUNITY', 'Community'


class ProviderCategory(models.TextChoices):
    STREAMING = 'STREAMING', 'Streaming'
    STORAGE = 'STORAGE', 'Penyimpanan'
    EMAIL = 'EMAIL', 'Email'
    AI = 'AI', 'Artificial Intelligence'
    NOTIFICATION = 'NOTIFICATION', 'Notifikasi'
    ANALYTICS = 'ANALYTICS', 'Analytics'
    PAYMENT = 'PAYMENT', 'Pembayaran'


class ProviderStatus(models.TextChoices):
    ACTIVE = 'ACTIVE', 'Aktif'
    INACTIVE = 'INACTIVE', 'Tidak Aktif'
    ERROR = 'ERROR', 'Error'


class FeatureFlagScope(models.TextChoices):
    GLOBAL = 'GLOBAL', 'Global (Semua Partner)'
    PARTNER = 'PARTNER', 'Partner Tertentu'


class PluginStatus(models.TextChoices):
    ENABLED = 'ENABLED', 'Aktif'
    DISABLED = 'DISABLED', 'Nonaktif'
    ERROR = 'ERROR', 'Error'


class ThemeMode(models.TextChoices):
    LIGHT = 'light', 'Terang'
    DARK = 'dark', 'Gelap'
    COFFEE = 'coffee', 'Coffee'
    CUSTOM = 'custom', 'Kustom'


class PartnerResolutionMethod(models.TextChoices):
    DOMAIN = 'DOMAIN', 'Domain'
    HEADER = 'HEADER', 'HTTP Header'
    SESSION = 'SESSION', 'Sesi'
    SUBDOMAIN = 'SUBDOMAIN', 'Subdomain'
    PATH = 'PATH', 'URL Path'
