from django.db import models
from django.conf import settings
from django.utils.text import slugify
from utils.mixins import UUIDPrimaryKeyMixin, TimeStampedModel


class ContentCategory(UUIDPrimaryKeyMixin, TimeStampedModel):
    CONTENT_TYPE_CHOICES = [
        ('ARTICLE', 'Artikel'),
        ('PODCAST', 'Podcast'),
        ('PROGRAM', 'Program'),
        ('EPISODE', 'Episode'),
        ('BROADCAST', 'Siaran'),
    ]
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=250, unique=True)
    description = models.TextField(blank=True, default='')
    content_type = models.CharField(max_length=20, choices=CONTENT_TYPE_CHOICES)
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE,
        null=True, blank=True, related_name='children'
    )
    icon = models.CharField(max_length=100, blank=True, default='')
    color = models.CharField(max_length=7, blank=True, default='#6B4226')
    active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = 'Content Category'
        verbose_name_plural = 'Content Categories'
        ordering = ['display_order', 'name']
        unique_together = ['name', 'content_type']

    def __str__(self):
        return f"[{self.get_content_type_display()}] {self.name}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class ContentTag(UUIDPrimaryKeyMixin, TimeStampedModel):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=150, unique=True)
    color = models.CharField(max_length=7, default='#6B4226')
    usage_count = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = 'Content Tag'
        verbose_name_plural = 'Content Tags'
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Author(UUIDPrimaryKeyMixin, TimeStampedModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='author_profile'
    )
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=250, unique=True)
    bio = models.TextField(blank=True, default='')
    avatar = models.ImageField(upload_to='content/authors/avatars/', blank=True)
    email = models.EmailField(blank=True, default='')
    website = models.URLField(max_length=500, blank=True, default='')
    social_links = models.JSONField(default=dict, blank=True)
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Author'
        verbose_name_plural = 'Authors'
        ordering = ['name']

    def __str__(self):
        return self.name

    @property
    def article_count(self):
        return self.content_author.filter(content_type='ARTICLE').count()

    @property
    def podcast_count(self):
        return self.content_author.filter(content_type='PODCAST').count()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class SEOModel(UUIDPrimaryKeyMixin, TimeStampedModel):
    content_type = models.ForeignKey(
        'contenttypes.ContentType', on_delete=models.CASCADE
    )
    object_id = models.UUIDField()
    title = models.CharField(max_length=200, blank=True, default='')
    description = models.TextField(max_length=500, blank=True, default='')
    keywords = models.CharField(max_length=500, blank=True, default='')
    og_title = models.CharField(max_length=200, blank=True, default='')
    og_description = models.TextField(max_length=500, blank=True, default='')
    og_image = models.ImageField(upload_to='content/seo/og/', blank=True)
    og_type = models.CharField(max_length=50, default='article')
    twitter_card = models.CharField(max_length=20, default='summary_large_image')
    twitter_title = models.CharField(max_length=200, blank=True, default='')
    twitter_description = models.TextField(max_length=500, blank=True, default='')
    twitter_image = models.ImageField(upload_to='content/seo/twitter/', blank=True)
    canonical_url = models.URLField(max_length=500, blank=True, default='')
    robots = models.CharField(max_length=30, default='index,follow')
    schema_markup = models.JSONField(default=dict, blank=True)

    class Meta:
        verbose_name = 'SEO Metadata'
        verbose_name_plural = 'SEO Metadata'
        unique_together = ['content_type', 'object_id']
        ordering = ['-created_at']

    def __str__(self):
        return f"SEO for {self.content_type.model} #{self.object_id}"

    @property
    def effective_title(self):
        return self.title or ''

    @property
    def effective_description(self):
        return self.description or self.og_description or ''

    @property
    def seo_score(self):
        score = 0
        if self.title:
            score += 20
        if 30 <= len(self.title) <= 60:
            score += 10
        if self.description:
            score += 20
        if 120 <= len(self.description) <= 160:
            score += 10
        if self.og_title:
            score += 10
        if self.og_description:
            score += 10
        if self.og_image:
            score += 10
        if self.keywords:
            score += 10
        return min(score, 100)

    @property
    def seo_grade(self):
        score = self.seo_score
        if score >= 90:
            return 'A'
        elif score >= 70:
            return 'B'
        elif score >= 50:
            return 'C'
        elif score >= 30:
            return 'D'
        return 'F'


class ContentVersion(UUIDPrimaryKeyMixin, TimeStampedModel):
    CONTENT_TYPE_CHOICES = [
        ('ARTICLE', 'Artikel'),
        ('PODCAST', 'Podcast'),
        ('PODCAST_EPISODE', 'Episode Podcast'),
        ('PROGRAM', 'Program'),
        ('EPISODE', 'Episode Siaran'),
        ('ANNOUNCEMENT', 'Pengumuman'),
        ('DISCUSSION', 'Diskusi'),
    ]
    content_type = models.CharField(max_length=25, choices=CONTENT_TYPE_CHOICES)
    content_id = models.UUIDField()
    version_number = models.PositiveIntegerField(default=1)
    title = models.CharField(max_length=300, blank=True, default='')
    data_snapshot = models.JSONField(default=dict)
    change_summary = models.CharField(max_length=500, blank=True, default='')
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='content_versions'
    )
    is_current = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Content Version'
        verbose_name_plural = 'Content Versions'
        ordering = ['-version_number']
        unique_together = ['content_type', 'content_id', 'version_number']

    def __str__(self):
        return f"{self.get_content_type_display()} #{self.content_id} v{self.version_number}"

    @property
    def content_label(self):
        return f"{self.get_content_type_display()} - {self.title}"

    @classmethod
    def create_version(cls, content_type, content_id, data, author=None, summary=''):
        last = cls.objects.filter(
            content_type=content_type, content_id=content_id
        ).order_by('-version_number').first()
        version_number = (last.version_number + 1) if last else 1

        if last:
            last.is_current = False
            last.save(update_fields=['is_current'])

        return cls.objects.create(
            content_type=content_type,
            content_id=content_id,
            version_number=version_number,
            data_snapshot=data,
            change_summary=summary,
            author=author,
            is_current=True,
        )

    @classmethod
    def get_current(cls, content_type, content_id):
        return cls.objects.filter(
            content_type=content_type,
            content_id=content_id,
            is_current=True,
        ).first()

    @classmethod
    def get_history(cls, content_type, content_id, limit=20):
        return cls.objects.filter(
            content_type=content_type,
            content_id=content_id,
        ).order_by('-version_number')[:limit]


class PublishingQueue(UUIDPrimaryKeyMixin, TimeStampedModel):
    CONTENT_TYPE_CHOICES = [
        ('ARTICLE', 'Artikel'),
        ('PODCAST', 'Podcast'),
        ('PODCAST_EPISODE', 'Episode Podcast'),
        ('PROGRAM', 'Program'),
        ('EPISODE', 'Episode Siaran'),
        ('ANNOUNCEMENT', 'Pengumuman'),
    ]
    content_type = models.CharField(max_length=25, choices=CONTENT_TYPE_CHOICES)
    content_id = models.UUIDField()
    scheduled_at = models.DateTimeField()
    published_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, default='PENDING')
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='publishing_queue'
    )
    error_message = models.TextField(blank=True, default='')
    retry_count = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = 'Publishing Queue'
        verbose_name_plural = 'Publishing Queue'
        ordering = ['scheduled_at']

    def __str__(self):
        return f"{self.get_content_type_display()} #{self.content_id} @ {self.scheduled_at}"


class ContentHighlight(UUIDPrimaryKeyMixin, TimeStampedModel):
    HIGHLIGHT_TYPE_CHOICES = [
        ('HERO', 'Hero Section'),
        ('FEATURED', 'Unggulan'),
        ('TRENDING', 'Trending'),
        ('LATEST', 'Terbaru'),
        ('EDITORS_PICK', 'Pilihan Editor'),
    ]
    CONTENT_TYPE_CHOICES = [
        ('ARTICLE', 'Artikel'),
        ('PODCAST', 'Podcast'),
        ('PODCAST_EPISODE', 'Episode Podcast'),
        ('PROGRAM', 'Program'),
        ('EPISODE', 'Episode Siaran'),
    ]
    highlight_type = models.CharField(max_length=20, choices=HIGHLIGHT_TYPE_CHOICES)
    content_type = models.CharField(max_length=25, choices=CONTENT_TYPE_CHOICES)
    content_id = models.UUIDField()
    title_override = models.CharField(max_length=300, blank=True, default='')
    description_override = models.TextField(blank=True, default='')
    image_override = models.ImageField(upload_to='content/highlights/', blank=True)
    display_order = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=True)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = 'Content Highlight'
        verbose_name_plural = 'Content Highlights'
        ordering = ['highlight_type', 'display_order']

    def __str__(self):
        return f"[{self.get_highlight_type_display()}] {self.get_content_type_display()} #{self.content_id}"

    @property
    def is_active_now(self):
        from django.utils import timezone
        now = timezone.now()
        if not self.active:
            return False
        if self.start_date and now < self.start_date:
            return False
        if self.end_date and now > self.end_date:
            return False
        return True
