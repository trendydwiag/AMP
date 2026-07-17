import uuid
import secrets
from django.db import models
from django.utils.text import slugify
from utils.mixins import UUIDPrimaryKeyMixin, TimeStampedModel
from apps.platform.choices import PartnerStatus, PartnerTier, PartnerResolutionMethod


class PartnerManager(models.Manager):
    """Manager that excludes soft-deleted partners by default."""

    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)

    def with_deleted(self):
        """Include soft-deleted partners."""
        return super().get_queryset()

    def only_deleted(self):
        """Only soft-deleted partners."""
        return super().get_queryset().filter(is_deleted=True)


class Partner(UUIDPrimaryKeyMixin, TimeStampedModel):
    """Represents an independent media partner tenant on the platform.

    Internally called 'Tenant' but exposed as 'Partner' in UI.
    Each partner has isolated settings, themes, storage, and domain configuration.
    """

    name = models.CharField(
        max_length=200,
        help_text="Nama partner/media station."
    )
    slug = models.SlugField(
        max_length=250,
        unique=True,
        help_text="Unique slug untuk URL dan identifikasi."
    )
    api_key = models.CharField(
        max_length=64,
        unique=True,
        default='',
        blank=True,
        help_text="API key untuk autentikasi external."
    )
    status = models.CharField(
        max_length=20,
        choices=PartnerStatus.choices,
        default=PartnerStatus.PENDING
    )
    tier = models.CharField(
        max_length=20,
        choices=PartnerTier.choices,
        default=PartnerTier.COMMUNITY
    )
    owner = models.ForeignKey(
        'users.User',
        on_delete=models.PROTECT,
        related_name='owned_partners',
        null=True,
        blank=True,
        help_text="User pemilik partner ini."
    )

    # Company
    company_name = models.CharField(
        max_length=300,
        blank=True,
        default='',
        help_text="Nama perusahaan/organisasi partner."
    )

    # Branding
    logo = models.ImageField(
        upload_to='platform/partners/logos/',
        blank=True,
        null=True
    )
    favicon = models.ImageField(
        upload_to='platform/partners/favicons/',
        blank=True,
        null=True
    )
    primary_color = models.CharField(
        max_length=7,
        default='#4E2F1F',
        help_text="Warna utama partner (hex)."
    )
    secondary_color = models.CharField(
        max_length=7,
        default='#FAF7F3',
        help_text="Warna sekunder partner (hex)."
    )
    accent_color = models.CharField(
        max_length=7,
        default='#8B5E3C',
        help_text="Warna aksen partner (hex)."
    )
    tagline = models.CharField(
        max_length=300,
        blank=True,
        default=''
    )
    description = models.TextField(
        blank=True,
        default=''
    )

    # Domain resolution
    resolution_method = models.CharField(
        max_length=20,
        choices=PartnerResolutionMethod.choices,
        default=PartnerResolutionMethod.DOMAIN
    )
    primary_domain = models.CharField(
        max_length=255,
        blank=True,
        default='',
        help_text="Domain utama partner (contoh: radio.kabulhaden.com)."
    )
    custom_domains = models.JSONField(
        default=list,
        blank=True,
        help_text="Daftar domain kustom partner."
    )

    # Contact
    contact_email = models.EmailField(blank=True, default='')
    contact_phone = models.CharField(max_length=50, blank=True, default='')
    contact_website = models.URLField(max_length=500, blank=True, default='')

    # Limits (per tier)
    max_users = models.PositiveIntegerField(
        default=5,
        help_text="Jumlah maksimum user yang diizinkan."
    )
    max_storage_mb = models.PositiveIntegerField(
        default=1024,
        help_text="Kapasitas penyimpanan dalam MB."
    )
    max_articles = models.PositiveIntegerField(
        default=100,
        help_text="Jumlah maksimum artikel."
    )
    max_podcasts = models.PositiveIntegerField(
        default=10,
        help_text="Jumlah maksimum podcast."
    )
    max_episodes = models.PositiveIntegerField(
        default=50,
        help_text="Jumlah maksimum episode per podcast."
    )

    # Feature overrides (JSON: feature_key -> bool/value)
    feature_overrides = models.JSONField(
        default=dict,
        blank=True,
        help_text="Override fitur per partner. Format: {\"feature_key\": true/false/value}."
    )

    # Provider overrides (JSON: category -> provider_slug)
    provider_overrides = models.JSONField(
        default=dict,
        blank=True,
        help_text="Override provider per partner. Format: {\"STREAMING\": \"radioboss\"}."
    )

    # Provider defaults
    storage_provider = models.CharField(
        max_length=50,
        blank=True,
        default='',
        help_text="Default storage provider slug."
    )
    streaming_provider = models.CharField(
        max_length=50,
        blank=True,
        default='',
        help_text="Default streaming provider slug."
    )
    smtp_provider = models.CharField(
        max_length=50,
        blank=True,
        default='',
        help_text="Default email/SMTP provider slug."
    )

    # Soft delete
    is_deleted = models.BooleanField(
        default=False,
        help_text="Soft delete flag."
    )
    deleted_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Waktu soft delete."
    )

    # Metadata
    timezone = models.CharField(max_length=50, default='Asia/Jakarta')
    language = models.CharField(max_length=10, default='id')
    locale = models.CharField(max_length=10, default='id_ID')

    objects = PartnerManager()
    all_objects = models.Manager()

    class Meta:
        verbose_name = 'Partner'
        verbose_name_plural = 'Partners'
        ordering = ['name']

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        if not self.api_key:
            self.api_key = secrets.token_hex(32)
        if not self.slug:
            self.slug = slugify(self.name)
            # Ensure uniqueness
            original_slug = self.slug
            counter = 1
            while Partner.all_objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1
        super().save(*args, **kwargs)

    @property
    def is_active(self) -> bool:
        return self.status == PartnerStatus.ACTIVE and not self.is_deleted

    def soft_delete(self):
        """Soft delete this partner."""
        from django.utils import timezone as tz
        self.is_deleted = True
        self.deleted_at = tz.now()
        self.status = PartnerStatus.INACTIVE
        self.save(update_fields=['is_deleted', 'deleted_at', 'status', 'updated_at'])

    def restore(self):
        """Restore a soft-deleted partner."""
        self.is_deleted = False
        self.deleted_at = None
        self.status = PartnerStatus.ACTIVE
        self.save(update_fields=['is_deleted', 'deleted_at', 'status', 'updated_at'])

    @property
    def storage_used_mb(self) -> int:
        from apps.media_manager.models import MediaFile
        total = MediaFile.objects.filter(
            partner=self
        ).aggregate(total=models.Sum('file_size'))['total'] or 0
        return int(total / (1024 * 1024))

    @property
    def storage_usage_percent(self) -> float:
        if self.max_storage_mb <= 0:
            return 0
        return min((self.storage_used_mb / self.max_storage_mb) * 100, 100)

    def has_feature(self, feature_key: str, default: bool = False) -> bool:
        """Check if a feature is enabled for this partner.

        Checks feature_overrides first, then falls back to global defaults.
        """
        if feature_key in self.feature_overrides:
            return bool(self.feature_overrides[feature_key])
        return default

    def get_provider(self, category: str) -> str | None:
        """Get the provider slug for a given category, checking overrides first."""
        if category in self.provider_overrides:
            return self.provider_overrides[category]
        return None

    def get_all_domains(self) -> list[str]:
        """Return all domains associated with this partner."""
        domains = []
        if self.primary_domain:
            domains.append(self.primary_domain)
        if isinstance(self.custom_domains, list):
            domains.extend(self.custom_domains)
        return domains

    def get_domain_for_resolution(self) -> str:
        """Return the primary domain used for partner resolution."""
        return self.primary_domain


class PartnerMembership(UUIDPrimaryKeyMixin, TimeStampedModel):
    """Links a User to a Partner with a specific role within that partner.

    A user can belong to multiple partners with different roles.
    """

    PARTNER_ROLE_CHOICES = [
        ('OWNER', 'Pemilik'),
        ('ADMINISTRATOR', 'Administrator'),
        ('EDITOR', 'Editor'),
        ('PRESENTER', 'Presenter'),
        ('VIEWER', 'Viewer'),
    ]

    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='partner_memberships'
    )
    partner = models.ForeignKey(
        Partner,
        on_delete=models.CASCADE,
        related_name='memberships'
    )
    role = models.CharField(
        max_length=30,
        choices=PARTNER_ROLE_CHOICES,
        default='VIEWER'
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Keanggotaan Partner'
        verbose_name_plural = 'Keanggotaan Partner'
        unique_together = ['user', 'partner']
        ordering = ['-created_at']

    def __str__(self) -> str:
        return f"{self.user.username} -> {self.partner.name} ({self.get_role_display()})"

    @property
    def is_owner(self) -> bool:
        return self.role == 'OWNER'

    @property
    def is_admin(self) -> bool:
        return self.role in ('OWNER', 'ADMINISTRATOR')


class PartnerDomain(UUIDPrimaryKeyMixin, TimeStampedModel):
    """Custom domain mapping for partners.

    Supports CNAME-based custom domains and subdomain routing.
    """

    partner = models.ForeignKey(
        Partner,
        on_delete=models.CASCADE,
        related_name='domains'
    )
    domain = models.CharField(
        max_length=255,
        unique=True,
        help_text="Domain yang mengarah ke partner ini."
    )
    is_primary = models.BooleanField(
        default=False,
        help_text="Apakah ini domain utama partner."
    )
    is_verified = models.BooleanField(
        default=False,
        help_text="Apakah domain sudah terverifikasi (CNAME/dns pointed)."
    )
    ssl_enabled = models.BooleanField(
        default=True,
        help_text="Apakah SSL aktif untuk domain ini."
    )

    class Meta:
        verbose_name = 'Domain Partner'
        verbose_name_plural = 'Domain Partner'
        ordering = ['-is_primary', 'domain']

    def __str__(self) -> str:
        return f"{self.domain} -> {self.partner.name}"

    def save(self, *args, **kwargs):
        if self.is_primary:
            PartnerDomain.objects.filter(
                partner=self.partner, is_primary=True
            ).exclude(pk=self.pk).update(is_primary=False)
        super().save(*args, **kwargs)


class PartnerInvitation(UUIDPrimaryKeyMixin, TimeStampedModel):
    """Pending invitations for users to join a partner."""

    INVITATION_STATUS_CHOICES = [
        ('PENDING', 'Menunggu'),
        ('ACCEPTED', 'Diterima'),
        ('EXPIRED', 'Kedaluwarsa'),
        ('REVOKED', 'Dicabut'),
    ]

    partner = models.ForeignKey(
        Partner,
        on_delete=models.CASCADE,
        related_name='invitations'
    )
    email = models.EmailField()
    role = models.CharField(
        max_length=30,
        choices=PartnerMembership.PARTNER_ROLE_CHOICES,
        default='VIEWER'
    )
    token = models.CharField(
        max_length=64,
        unique=True,
        default='',
        blank=True
    )
    status = models.CharField(
        max_length=20,
        choices=INVITATION_STATUS_CHOICES,
        default='PENDING'
    )
    invited_by = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        related_name='sent_invitations'
    )
    expires_at = models.DateTimeField()
    accepted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = 'Undangan Partner'
        verbose_name_plural = 'Undangan Partner'
        ordering = ['-created_at']

    def __str__(self) -> str:
        return f"Undangan: {self.email} -> {self.partner.name}"

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = secrets.token_hex(32)
        super().save(*args, **kwargs)

    @property
    def is_expired(self) -> bool:
        from django.utils import timezone
        return timezone.now() > self.expires_at

    @property
    def is_valid(self) -> bool:
        return self.status == 'PENDING' and not self.is_expired
