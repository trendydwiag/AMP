import re

from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from utils.choices import ContentFormat, ContentPriority, ContentStatus
from utils.mixins import UUIDPrimaryKeyMixin, TimeStampedModel


class Category(UUIDPrimaryKeyMixin, TimeStampedModel):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=250, unique=True)
    description = models.TextField(blank=True, default='')
    active = models.BooleanField(default=True)
    partner = models.ForeignKey(
        'platform.Partner', on_delete=models.CASCADE,
        null=True, blank=True, related_name='news_categories',
        help_text="Partner yang memiliki kategori ini."
    )

    class Meta:
        verbose_name = 'News Category'
        verbose_name_plural = 'News Categories'
        ordering = ['name']

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Tag(UUIDPrimaryKeyMixin, TimeStampedModel):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=150, unique=True)
    partner = models.ForeignKey(
        'platform.Partner', on_delete=models.CASCADE,
        null=True, blank=True, related_name='news_tags',
        help_text="Partner yang memiliki tag ini."
    )

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'
        ordering = ['name']

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Article(UUIDPrimaryKeyMixin, TimeStampedModel):
    title = models.CharField(max_length=300)
    slug = models.SlugField(max_length=350, unique=True, blank=True)
    excerpt = models.CharField(max_length=500, blank=True, default='')
    content = models.TextField()
    featured_image = models.ImageField(upload_to='news/articles/', blank=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='articles'
    )
    tags = models.ManyToManyField(Tag, blank=True, related_name='articles')
    author_name = models.CharField(max_length=200, default='Redaksi')
    partner = models.ForeignKey(
        'platform.Partner', on_delete=models.CASCADE,
        null=True, blank=True, related_name='articles',
        help_text="Partner yang memiliki artikel ini."
    )

    content_format = models.CharField(
        max_length=15, choices=ContentFormat.choices, default=ContentFormat.RICH_TEXT
    )
    status = models.CharField(
        max_length=18, choices=ContentStatus.choices, default=ContentStatus.DRAFT
    )
    priority = models.CharField(
        max_length=10, choices=ContentPriority.choices, default=ContentPriority.NORMAL
    )
    featured = models.BooleanField(default=False)
    allow_comments = models.BooleanField(default=True)
    word_count = models.PositiveIntegerField(default=0)
    reading_time_minutes = models.PositiveIntegerField(default=0)

    version = models.PositiveIntegerField(default=1)
    last_published_at = models.DateTimeField(null=True, blank=True)

    publish_date = models.DateTimeField(null=True, blank=True)
    scheduled_at = models.DateTimeField(null=True, blank=True)
    publish_end_date = models.DateTimeField(null=True, blank=True)

    view_count = models.PositiveIntegerField(default=0)

    seo_title = models.CharField(max_length=200, blank=True, default='')
    seo_description = models.CharField(max_length=500, blank=True, default='')
    og_title = models.CharField(max_length=200, blank=True)
    og_description = models.CharField(max_length=500, blank=True)
    og_image = models.ImageField(upload_to='news/articles/og/', blank=True)
    twitter_card = models.CharField(max_length=20, default='summary_large_image')
    canonical_url = models.URLField(max_length=500, blank=True)
    robots = models.CharField(max_length=30, default='index,follow')
    schema_markup = models.JSONField(default=dict, blank=True)

    related_articles = models.ManyToManyField('self', blank=True, symmetrical=False)
    author = models.ForeignKey(
        'content.Author', on_delete=models.SET_NULL,
        null=True, blank=True, related_name='content_author'
    )
    tags_content = models.ManyToManyField(
        'content.ContentTag', blank=True, related_name='articles_content'
    )

    class Meta:
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'
        ordering = ['-publish_date']

    def __str__(self) -> str:
        return self.title

    @property
    def is_published(self) -> bool:
        return self.status == ContentStatus.PUBLISHED and self.last_published_at is not None

    def _calculate_word_count(self):
        text = re.sub(r'<[^>]+>', ' ', self.content or '')
        words = text.split()
        return len(words)

    def _calculate_reading_time(self):
        words = self._calculate_word_count()
        minutes = max(1, words // 200)
        return minutes

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        self.word_count = self._calculate_word_count()
        self.reading_time_minutes = self._calculate_reading_time()
        super().save(*args, **kwargs)
