from django.db import models


class UserRole(models.TextChoices):
    """System role choices for Role-Based Access Control (RBAC)."""
    SUPERUSER = 'SUPERUSER', 'Super User'
    ADMINISTRATOR = 'ADMINISTRATOR', 'Administrator'
    EDITOR = 'EDITOR', 'Editor/Penulis'
    VIEWER = 'VIEWER', 'Viewer/Pembaca'


class AuditLevel(models.TextChoices):
    """Security audit levels for log classification."""
    INFO = 'INFO', 'Informasi'
    WARNING = 'WARNING', 'Peringatan'
    CRITICAL = 'CRITICAL', 'Kritis'


class StatusActive(models.TextChoices):
    """Standard Active/Inactive flag choices."""
    ACTIVE = 'ACTIVE', 'Aktif'
    INACTIVE = 'INACTIVE', 'Tidak Aktif'


class LoginStatus(models.TextChoices):
    """Login attempt outcome classification."""
    SUCCESS = 'SUCCESS', 'Berhasil'
    FAILED = 'FAILED', 'Gagal'


class AuditAction(models.TextChoices):
    """Audit log action classifications for tracking system events."""
    LOGIN = 'LOGIN', 'Login'
    LOGOUT = 'LOGOUT', 'Logout'
    LOGIN_FAILED = 'LOGIN_FAILED', 'Login Gagal'
    PASSWORD_CHANGE = 'PASSWORD_CHANGE', 'Ubah Password'
    PASSWORD_RESET = 'PASSWORD_RESET', 'Reset Password'
    PROFILE_UPDATE = 'PROFILE_UPDATE', 'Ubah Profil'
    ROLE_ASSIGN = 'ROLE_ASSIGN', 'Tugaskan Peran'
    PERMISSION_ASSIGN = 'PERMISSION_ASSIGN', 'Tugaskan Izin'
    USER_CREATE = 'USER_CREATE', 'Buat User'
    USER_ACTIVATE = 'USER_ACTIVATE', 'Aktifkan User'
    USER_DEACTIVATE = 'USER_DEACTIVATE', 'Nonaktifkan User'
    USER_SUSPEND = 'USER_SUSPEND', 'Tangguhkan User'
    ACCOUNT_LOCK = 'ACCOUNT_LOCK', 'Kunci Akun'
    ACCOUNT_UNLOCK = 'ACCOUNT_UNLOCK', 'Buka Kunci Akun'
    EMAIL_VERIFY = 'EMAIL_VERIFY', 'Verifikasi Email'
    TWO_FACTOR_ENABLE = 'TWO_FACTOR_ENABLE', 'Aktifkan 2FA'
    TWO_FACTOR_DISABLE = 'TWO_FACTOR_DISABLE', 'Nonaktifkan 2FA'


class AccountStatus(models.TextChoices):
    """Account operational status for lifecycle management."""
    ACTIVE = 'ACTIVE', 'Aktif'
    INACTIVE = 'INACTIVE', 'Tidak Aktif'
    SUSPENDED = 'SUSPENDED', 'Ditangguhkan'
    LOCKED = 'LOCKED', 'Dikunci'


class FileType(models.TextChoices):
    """Media file type classification."""
    IMAGE = 'IMAGE', 'Gambar'
    VIDEO = 'VIDEO', 'Video'
    DOCUMENT = 'DOCUMENT', 'Dokumen'
    AUDIO = 'AUDIO', 'Audio'
    OTHER = 'OTHER', 'Lainnya'


class ImageCompression(models.TextChoices):
    """Image compression quality presets."""
    LOSSLESS = 'LOSSLESS', 'Lossless'
    HIGH = 'HIGH', 'Tinggi (85%)'
    MEDIUM = 'MEDIUM', 'Sedang (70%)'
    LOW = 'LOW', 'Rendah (50%)'


class TwitterCard(models.TextChoices):
    """Twitter Card type options."""
    SUMMARY = 'summary', 'Summary'
    SUMMARY_LARGE_IMAGE = 'summary_large_image', 'Summary Large Image'


class RobotsMeta(models.TextChoices):
    """Search engine robots meta directives."""
    INDEX_FOLLOW = 'index,follow', 'Index & Follow'
    NOINDEX_FOLLOW = 'noindex,follow', 'No Index, Follow'
    INDEX_NOFOLLOW = 'index,nofollow', 'Index, No Follow'
    NOINDEX_NOFOLLOW = 'noindex,nofollow', 'No Index, No Follow'


class LanguageCode(models.TextChoices):
    """Site language options."""
    ID = 'id', 'Bahasa Indonesia'
    EN = 'en', 'English'


class RadioProviderType(models.TextChoices):
    """Radio server provider type classifications."""
    RADIOBOSS = 'RADIOBOSS', 'RadioBoss Advance'
    ICECAST = 'ICECAST', 'Icecast'
    SHOUTCAST = 'SHOUTCAST', 'Shoutcast'
    AZURACAST = 'AZURACAST', 'AzuraCast'


class StreamStatus(models.TextChoices):
    """Current stream operational status."""
    ONLINE = 'ONLINE', 'Online'
    OFFLINE = 'OFFLINE', 'Offline'
    AUTO_DJ = 'AUTO_DJ', 'Auto DJ'
    LIVE_DJ = 'LIVE_DJ', 'Live DJ'
    UNKNOWN = 'UNKNOWN', 'Unknown'


class StreamHealthStatus(models.TextChoices):
    """Health check result classification."""
    HEALTHY = 'HEALTHY', 'Sehat'
    DEGRADED = 'DEGRADED', 'Menurun'
    DOWN = 'DOWN', 'Mati'
    TIMEOUT = 'TIMEOUT', 'Timeout'


class MetadataFormat(models.TextChoices):
    """Supported metadata retrieval formats."""
    JSON = 'JSON', 'JSON API'
    XML = 'XML', 'XML API'
    ICY = 'ICY', 'ICY Metadata'
    HTTP = 'HTTP', 'HTTP Metadata'


class DayOfWeek(models.TextChoices):
    """Day of week choices for scheduling."""
    MONDAY = 'MON', 'Senin'
    TUESDAY = 'TUE', 'Selasa'
    WEDNESDAY = 'WED', 'Rabu'
    THURSDAY = 'THU', 'Kamis'
    FRIDAY = 'FRI', 'Jumat'
    SATURDAY = 'SAT', 'Sabtu'
    SUNDAY = 'SUN', 'Minggu'


class BroadcastStatus(models.TextChoices):
    """Broadcast session status lifecycle."""
    SCHEDULED = 'SCHEDULED', 'Terjadwal'
    LIVE = 'LIVE', 'Sedang Tayang'
    FINISHED = 'FINISHED', 'Selesai'
    CANCELLED = 'CANCELLED', 'Dibatalkan'
    DELAYED = 'DELAYED', 'Ditunda'


class ContentRating(models.TextChoices):
    """Content rating for programs."""
    GENERAL = 'G', 'Umum'
    PARENTAL = 'PG', 'Parental Guidance'
    TEEN = 'T', 'Remaja'
    MATURE = 'M', 'Dewasa'


class AnnouncementStatus(models.TextChoices):
    """Announcement display status."""
    ACTIVE = 'ACTIVE', 'Aktif'
    INACTIVE = 'INACTIVE', 'Tidak Aktif'
    EXPIRED = 'EXPIRED', 'Kedaluwarsa'


class PodcastCategory(models.TextChoices):
    """Podcast program category classification."""
    NEWS = 'NEWS', 'Berita'
    ENTERTAINMENT = 'ENTERTAINMENT', 'Hiburan'
    EDUCATION = 'EDUCATION', 'Pendidikan'
    TECHNOLOGY = 'TECHNOLOGY', 'Teknologi'
    MUSIC = 'MUSIC', 'Musik'
    RELIGION = 'RELIGION', 'Agama'
    TALK_SHOW = 'TALK_SHOW', 'Talk Show'
    SPORTS = 'SPORTS', 'Olahraga'
    BUSINESS = 'BUSINESS', 'Bisnis'
    CULTURE = 'CULTURE', 'Budaya'
    HEALTH = 'HEALTH', 'Kesehatan'
    OTHER = 'OTHER', 'Lainnya'


class ContentStatus(models.TextChoices):
    """Content publishing workflow status."""
    DRAFT = 'DRAFT', 'Draft'
    PENDING_REVIEW = 'PENDING_REVIEW', 'Menunggu Review'
    APPROVED = 'APPROVED', 'Disetujui'
    SCHEDULED = 'SCHEDULED', 'Terjadwal'
    PUBLISHED = 'PUBLISHED', 'Diterbitkan'
    ARCHIVED = 'ARCHIVED', 'Diarsipkan'
    REJECTED = 'REJECTED', 'Ditolak'


class ContentPriority(models.TextChoices):
    """Content priority level for scheduling and editorial."""
    LOW = 'LOW', 'Rendah'
    NORMAL = 'NORMAL', 'Normal'
    HIGH = 'HIGH', 'Tinggi'
    URGENT = 'URGENT', 'Mendesak'


class ContentFormat(models.TextChoices):
    """Content format type."""
    RICH_TEXT = 'RICH_TEXT', 'Rich Text'
    MARKDOWN = 'MARKDOWN', 'Markdown'
    HTML = 'HTML', 'HTML'


class WorkflowAction(models.TextChoices):
    """Workflow transition actions."""
    SUBMIT_REVIEW = 'SUBMIT_REVIEW', 'Kirim ke Review'
    APPROVE = 'APPROVE', 'Setujui'
    REJECT = 'REJECT', 'Tolak'
    PUBLISH = 'PUBLISH', 'Terbitkan'
    UNPUBLISH = 'UNPUBLISH', 'Cabut Publikasi'
    ARCHIVE = 'ARCHIVE', 'Arsipkan'
    RESTORE = 'RESTORE', 'Pulihkan'
    SCHEDULE = 'SCHEDULE', 'Jadwalkan'


class PartnerStatus(models.TextChoices):
    """Partner lifecycle status."""
    ACTIVE = 'ACTIVE', 'Aktif'
    INACTIVE = 'INACTIVE', 'Tidak Aktif'
    SUSPENDED = 'SUSPENDED', 'Ditangguhkan'
    PENDING = 'PENDING', 'Menunggu Persetujuan'


class PartnerTier(models.TextChoices):
    """Partner subscription tier."""
    ENTERPRISE = 'ENTERPRISE', 'Enterprise'
    PROFESSIONAL = 'PROFESSIONAL', 'Professional'
    STARTER = 'STARTER', 'Starter'
    COMMUNITY = 'COMMUNITY', 'Community'


class ProviderCategory(models.TextChoices):
    """Platform service provider categories."""
    STREAMING = 'STREAMING', 'Streaming'
    STORAGE = 'STORAGE', 'Penyimpanan'
    EMAIL = 'EMAIL', 'Email'
    AI = 'AI', 'Artificial Intelligence'
    NOTIFICATION = 'NOTIFICATION', 'Notifikasi'
    ANALYTICS = 'ANALYTICS', 'Analytics'
    PAYMENT = 'PAYMENT', 'Pembayaran'


class FeatureFlagScope(models.TextChoices):
    """Feature flag scope."""
    GLOBAL = 'GLOBAL', 'Global (Semua Partner)'
    PARTNER = 'PARTNER', 'Partner Tertentu'


class ThemeMode(models.TextChoices):
    """Available theme modes."""
    LIGHT = 'light', 'Terang'
    DARK = 'dark', 'Gelap'
    COFFEE = 'coffee', 'Coffee'
    CUSTOM = 'custom', 'Kustom'
