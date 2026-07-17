from django.db import models
from django.utils.text import slugify
from utils.mixins import UUIDPrimaryKeyMixin, TimeStampedModel
from utils.choices import PodcastCategory, ContentStatus, ContentPriority, ContentFormat


class Podcast(UUIDPrimaryKeyMixin, TimeStampedModel):
    title = models.CharField(max_length=300)
    slug = models.SlugField(max_length=350, unique=True, blank=True)
    description = models.TextField(blank=True, default='')
    short_description = models.CharField(max_length=500, blank=True, default='')
    thumbnail = models.ImageField(upload_to='podcast/thumbnails/', blank=True)
    banner = models.ImageField(upload_to='podcast/banners/', blank=True)
    author_name = models.CharField(max_length=200, default='Redaksi')
    category = models.CharField(
        max_length=20,
        choices=PodcastCategory.choices,
        default=PodcastCategory.OTHER
    )
    partner = models.ForeignKey(
        'platform.Partner', on_delete=models.CASCADE,
        null=True, blank=True, related_name='podcasts',
        help_text="Partner yang memiliki podcast ini."
    )
    language = models.CharField(max_length=10, default='id')
    episode_count = models.PositiveIntegerField(default=0)
    itunes_url = models.URLField(blank=True, default='')
    spotify_url = models.URLField(blank=True, default='')
    google_url = models.URLField(blank=True, default='')
    active = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    seo_title = models.CharField(max_length=200, blank=True, default='')
    seo_description = models.CharField(max_length=500, blank=True, default='')

    status = models.CharField(
        max_length=15,
        choices=ContentStatus.choices,
        default=ContentStatus.DRAFT
    )
    priority = models.CharField(
        max_length=10,
        choices=ContentPriority.choices,
        default=ContentPriority.NORMAL
    )
    version = models.PositiveIntegerField(default=1)
    last_published_at = models.DateTimeField(null=True, blank=True)
    author = models.ForeignKey(
        'content.Author',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='podcast_author'
    )
    tags_content = models.ManyToManyField(
        'content.ContentTag',
        blank=True,
        related_name='podcasts_content'
    )
    og_title = models.CharField(max_length=200, blank=True)
    og_description = models.CharField(max_length=500, blank=True)
    og_image = models.ImageField(upload_to='podcast/og/', blank=True)
    twitter_card = models.CharField(max_length=20, default='summary_large_image')
    canonical_url = models.URLField(max_length=500, blank=True)
    robots = models.CharField(max_length=30, default='index,follow')
    schema_markup = models.JSONField(default=dict, blank=True)
    content_format = models.CharField(
        max_length=15,
        choices=ContentFormat.choices,
        default=ContentFormat.RICH_TEXT
    )

    class Meta:
        verbose_name = 'Podcast'
        verbose_name_plural = 'Podcasts'
        ordering = ['title']

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class PodcastEpisode(UUIDPrimaryKeyMixin, TimeStampedModel):
    podcast = models.ForeignKey(
        Podcast, on_delete=models.CASCADE,
        related_name='episodes'
    )
    title = models.CharField(max_length=300)
    slug = models.SlugField(max_length=350, blank=True)
    description = models.TextField(blank=True, default='')
    audio_file = models.FileField(upload_to='podcast/episodes/audio/')
    audio_url = models.URLField(blank=True, default='')
    cover_image = models.ImageField(upload_to='podcast/episodes/covers/', blank=True)
    duration = models.PositiveIntegerField(
        default=0,
        help_text='Duration in seconds'
    )
    episode_number = models.PositiveIntegerField(default=1)
    season_number = models.PositiveIntegerField(default=1)
    published = models.BooleanField(default=False)
    publish_date = models.DateTimeField(null=True, blank=True)
    download_count = models.PositiveIntegerField(default=0)
    partner = models.ForeignKey(
        'platform.Partner', on_delete=models.CASCADE,
        null=True, blank=True, related_name='podcast_episodes',
        help_text="Partner yang memiliki episode ini."
    )

    status = models.CharField(
        max_length=15,
        choices=ContentStatus.choices,
        default=ContentStatus.DRAFT
    )
    content_format = models.CharField(
        max_length=15,
        choices=ContentFormat.choices,
        default=ContentFormat.RICH_TEXT
    )
    transcript = models.TextField(blank=True, default='')
    version = models.PositiveIntegerField(default=1)
    last_published_at = models.DateTimeField(null=True, blank=True)
    scheduled_at = models.DateTimeField(null=True, blank=True)
    og_title = models.CharField(max_length=200, blank=True)
    og_description = models.CharField(max_length=500, blank=True)
    og_image = models.ImageField(upload_to='podcast/episodes/og/', blank=True)
    twitter_card = models.CharField(max_length=20, default='summary_large_image')
    canonical_url = models.URLField(max_length=500, blank=True)
    robots = models.CharField(max_length=30, default='index,follow')

    class Meta:
        verbose_name = 'Podcast Episode'
        verbose_name_plural = 'Podcast Episodes'
        ordering = ['-publish_date']

    def __str__(self) -> str:
        return f"{self.podcast.title} - E{self.episode_number}: {self.title}"

    @property
    def is_published(self) -> bool:
        return self.status == ContentStatus.PUBLISHED and self.publish_date is not None

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
