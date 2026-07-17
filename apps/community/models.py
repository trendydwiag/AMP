from django.db import models
from django.utils.text import slugify
from utils.mixins import UUIDPrimaryKeyMixin, TimeStampedModel


class Discussion(UUIDPrimaryKeyMixin, TimeStampedModel):
    title = models.CharField(max_length=300)
    slug = models.SlugField(max_length=350, unique=True, blank=True)
    content = models.TextField()
    author_name = models.CharField(max_length=200)
    author_email = models.EmailField(blank=True)
    category = models.CharField(max_length=100, blank=True)
    is_pinned = models.BooleanField(default=False)
    is_locked = models.BooleanField(default=False)
    view_count = models.PositiveIntegerField(default=0)
    reply_count = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-is_pinned', '-created_at']
        verbose_name = 'Discussion'
        verbose_name_plural = 'Discussions'

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Reply(UUIDPrimaryKeyMixin, TimeStampedModel):
    discussion = models.ForeignKey(
        Discussion,
        on_delete=models.CASCADE,
        related_name='replies'
    )
    content = models.TextField()
    author_name = models.CharField(max_length=200)
    author_email = models.EmailField(blank=True)

    class Meta:
        ordering = ['created_at']
        verbose_name = 'Reply'
        verbose_name_plural = 'Replies'

    def __str__(self) -> str:
        return f"Reply by {self.author_name} on {self.discussion.title}"
