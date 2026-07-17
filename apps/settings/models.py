from django.db import models
from utils.mixins import TimeStampedModel


class SiteSettings(TimeStampedModel):
    site_name = models.CharField(max_length=200, default='Kabulhaden CMS')
    site_tagline = models.CharField(max_length=300, blank=True, default='')
    site_description = models.TextField(blank=True, default='')
    site_url = models.URLField(max_length=500, blank=True, default='')
    site_logo = models.ImageField(upload_to='settings/site/', blank=True, null=True)
    site_favicon = models.ImageField(upload_to='settings/site/', blank=True, null=True)
    maintenance_mode = models.BooleanField(default=False)
    maintenance_message = models.TextField(blank=True, default='Situs sedang dalam pemeliharaan.')

    class Meta:
        verbose_name = 'Pengaturan Situs'
        verbose_name_plural = 'Pengaturan Situs'

    def __str__(self):
        return self.site_name

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class SEOSettings(TimeStampedModel):
    meta_title = models.CharField(max_length=200, default='Kabulhaden CMS')
    meta_description = models.TextField(blank=True, default='')
    meta_keywords = models.CharField(max_length=500, blank=True, default='')
    og_title = models.CharField(max_length=200, blank=True, default='')
    og_description = models.TextField(blank=True, default='')
    og_image = models.ImageField(upload_to='settings/seo/', blank=True, null=True)
    twitter_card = models.CharField(
        max_length=30,
        choices=[('summary', 'Summary'), ('summary_large_image', 'Summary Large Image')],
        default='summary_large_image'
    )
    twitter_site = models.CharField(max_length=100, blank=True, default='')
    twitter_creator = models.CharField(max_length=100, blank=True, default='')
    robots_meta = models.CharField(
        max_length=50,
        choices=[('index,follow', 'Index & Follow'), ('noindex,follow', 'No Index, Follow'),
                 ('index,nofollow', 'Index, No Follow'), ('noindex,nofollow', 'No Index, No Follow')],
        default='index,follow'
    )
    google_analytics_id = models.CharField(max_length=50, blank=True, default='')
    google_tag_manager_id = models.CharField(max_length=50, blank=True, default='')
    custom_head_scripts = models.TextField(blank=True, default='')
    custom_footer_scripts = models.TextField(blank=True, default='')

    class Meta:
        verbose_name = 'Pengaturan SEO'
        verbose_name_plural = 'Pengaturan SEO'

    def __str__(self):
        return f'SEO: {self.meta_title}'

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class EmailSettings(TimeStampedModel):
    email_backend = models.CharField(
        max_length=200,
        default='django.core.mail.backends.smtp.EmailBackend'
    )
    email_host = models.CharField(max_length=200, default='smtp.gmail.com')
    email_port = models.PositiveIntegerField(default=587)
    email_use_tls = models.BooleanField(default=True)
    email_use_ssl = models.BooleanField(default=False)
    email_host_user = models.EmailField(blank=True, default='')
    email_host_password = models.CharField(max_length=500, blank=True, default='')
    default_from_name = models.CharField(max_length=200, blank=True, default='Kabulhaden CMS')
    default_from_email = models.EmailField(blank=True, default='noreply@kabulhaden.com')

    class Meta:
        verbose_name = 'Pengaturan Email'
        verbose_name_plural = 'Pengaturan Email'

    def __str__(self):
        return f'Email: {self.email_host}'

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class SecuritySettings(TimeStampedModel):
    session_timeout_minutes = models.PositiveIntegerField(default=60)
    max_login_attempts = models.PositiveIntegerField(default=5)
    lockout_duration_minutes = models.PositiveIntegerField(default=15)
    password_min_length = models.PositiveIntegerField(default=12)
    require_uppercase = models.BooleanField(default=True)
    require_lowercase = models.BooleanField(default=True)
    require_numbers = models.BooleanField(default=True)
    require_special_chars = models.BooleanField(default=True)
    password_expiry_days = models.PositiveIntegerField(default=90)
    enable_2fa = models.BooleanField(default=False)
    force_2fa_admin = models.BooleanField(default=False)
    allowed_ip_ranges = models.TextField(
        blank=True, default='',
        help_text='Satu IP atau CIDR per baris. Kosongkan untuk izinkan semua.'
    )
    csrf_trusted_origins = models.TextField(blank=True, default='')

    class Meta:
        verbose_name = 'Pengaturan Keamanan'
        verbose_name_plural = 'Pengaturan Keamanan'

    def __str__(self):
        return 'Pengaturan Keamanan'

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class AppearanceSettings(TimeStampedModel):
    primary_color = models.CharField(max_length=7, default='#3B82F6')
    secondary_color = models.CharField(max_length=7, default='#10B981')
    accent_color = models.CharField(max_length=7, default='#F59E0B')
    dark_mode = models.BooleanField(default=False)
    sidebar_collapsed = models.BooleanField(default=False)
    sidebar_theme = models.CharField(
        max_length=20,
        choices=[('light', 'Terang'), ('dark', 'Gelap')],
        default='dark'
    )
    font_family = models.CharField(
        max_length=50,
        choices=[('inter', 'Inter'), ('poppins', 'Poppins'), ('opensans', 'Open Sans'), ('roboto', 'Roboto')],
        default='inter'
    )
    font_size = models.CharField(
        max_length=10,
        choices=[('small', 'Kecil'), ('medium', 'Sedang'), ('large', 'Besar')],
        default='medium'
    )
    border_radius = models.CharField(
        max_length=10,
        choices=[('none', 'Tidak Ada'), ('small', 'Kecil'), ('medium', 'Sedang'), ('large', 'Besar')],
        default='medium'
    )
    compact_mode = models.BooleanField(default=False)
    show_breadcrumbs = models.BooleanField(default=True)
    show_welcome_message = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Pengaturan Tampilan'
        verbose_name_plural = 'Pengaturan Tampilan'

    def __str__(self):
        return 'Pengaturan Tampilan'

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class NotificationSettings(TimeStampedModel):
    email_on_user_register = models.BooleanField(default=True)
    email_on_user_login = models.BooleanField(default=False)
    email_on_password_change = models.BooleanField(default=True)
    email_on_role_change = models.BooleanField(default=True)
    email_on_account_lock = models.BooleanField(default=True)
    email_on_system_error = models.BooleanField(default=True)
    email_on_maintenance = models.BooleanField(default=True)
    notify_admins_on_error = models.BooleanField(default=True)
    notify_superusers_on_critical = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Pengaturan Notifikasi'
        verbose_name_plural = 'Pengaturan Notifikasi'

    def __str__(self):
        return 'Pengaturan Notifikasi'

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class SocialMediaSettings(TimeStampedModel):
    facebook_url = models.URLField(blank=True, default='')
    twitter_url = models.URLField(blank=True, default='')
    instagram_url = models.URLField(blank=True, default='')
    youtube_url = models.URLField(blank=True, default='')
    tiktok_url = models.URLField(blank=True, default='')
    linkedin_url = models.URLField(blank=True, default='')
    github_url = models.URLField(blank=True, default='')
    whatsapp_number = models.CharField(max_length=30, blank=True, default='')
    telegram_username = models.CharField(max_length=100, blank=True, default='')

    class Meta:
        verbose_name = 'Pengaturan Media Sosial'
        verbose_name_plural = 'Pengaturan Media Sosial'

    def __str__(self):
        return 'Pengaturan Media Sosial'

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class ContentSettings(TimeStampedModel):
    posts_per_page = models.PositiveIntegerField(default=10)
    excerpt_length = models.PositiveIntegerField(default=150)
    enable_comments = models.BooleanField(default=True)
    moderate_comments = models.BooleanField(default=True)
    allow_guest_comments = models.BooleanField(default=False)
    default_post_status = models.CharField(
        max_length=20,
        choices=[('draft', 'Draft'), ('published', 'Terbitkan')],
        default='draft'
    )
    enable_revision_history = models.BooleanField(default=True)
    max_upload_size_mb = models.PositiveIntegerField(default=10)
    allowed_upload_types = models.CharField(
        max_length=500, blank=True, default='',
        help_text='Dipisah koma. Kosongkan untuk izinkan semua.'
    )

    class Meta:
        verbose_name = 'Pengaturan Konten'
        verbose_name_plural = 'Pengaturan Konten'

    def __str__(self):
        return 'Pengaturan Konten'

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class LanguageSettings(TimeStampedModel):
    site_language = models.CharField(
        max_length=10,
        choices=[('id', 'Bahasa Indonesia'), ('en', 'English')],
        default='id'
    )
    date_format = models.CharField(
        max_length=30,
        choices=[('d/m/Y', 'DD/MM/YYYY'), ('Y-m-d', 'YYYY-MM-DD'), ('m/d/Y', 'MM/DD/YYYY')],
        default='d/m/Y'
    )
    time_format = models.CharField(
        max_length=10,
        choices=[('H:i', '24 Jam'), ('h:i A', '12 Jam')],
        default='H:i'
    )
    timezone = models.CharField(max_length=50, default='Asia/Jakarta')

    class Meta:
        verbose_name = 'Pengaturan Bahasa & Lokal'
        verbose_name_plural = 'Pengaturan Bahasa & Lokal'

    def __str__(self):
        return f'Language: {self.site_language}'

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class MediaSettings(TimeStampedModel):
    storage_backend = models.CharField(
        max_length=30,
        choices=[('local', 'Lokal'), ('s3', 'Amazon S3'), ('gcs', 'Google Cloud Storage')],
        default='local'
    )
    max_file_size_mb = models.PositiveIntegerField(default=10)
    image_max_width = models.PositiveIntegerField(default=1920)
    image_max_height = models.PositiveIntegerField(default=1080)
    image_compression_quality = models.CharField(
        max_length=20,
        choices=[('lossless', 'Lossless'), ('high', 'Tinggi (85%)'),
                 ('medium', 'Sedang (70%)'), ('low', 'Rendah (50%)')],
        default='high'
    )
    auto_generate_thumbnails = models.BooleanField(default=True)
    thumbnail_width = models.PositiveIntegerField(default=300)
    thumbnail_height = models.PositiveIntegerField(default=200)
    allowed_extensions = models.CharField(
        max_length=500, blank=True, default='',
        help_text='Dipisah koma. Contoh: jpg,png,gif,webp,pdf,docx'
    )
    enable_image_optimization = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Pengaturan Media'
        verbose_name_plural = 'Pengaturan Media'

    def __str__(self):
        return f'Media: {self.storage_backend}'

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj
