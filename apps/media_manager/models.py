import os
from django.db import models
from django.conf import settings
from utils.mixins import TimeStampedModel, UUIDPrimaryKeyMixin
from utils.storage import generate_uuid_filename


class Folder(UUIDPrimaryKeyMixin, TimeStampedModel):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True,
        related_name='children', verbose_name='Folder Induk'
    )
    description = models.TextField(blank=True, default='')
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, related_name='created_folders'
    )
    partner = models.ForeignKey(
        'platform.Partner', on_delete=models.CASCADE,
        null=True, blank=True, related_name='media_folders',
        help_text="Partner yang memiliki folder ini."
    )

    class Meta:
        verbose_name = 'Folder'
        verbose_name_plural = 'Folder'
        ordering = ['name']
        unique_together = ['name', 'parent']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            base = slugify(self.name)
            slug = base
            counter = 1
            while Folder.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f'{base}-{counter}'
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    @property
    def full_path(self):
        parts = [self.name]
        parent = self.parent
        while parent:
            parts.insert(0, parent.name)
            parent = parent.parent
        return ' / '.join(parts)

    @property
    def file_count(self):
        return self.files.count()

    @property
    def total_size(self):
        return self.files.aggregate(total=models.Sum('file_size'))['total'] or 0


class Tag(UUIDPrimaryKeyMixin, TimeStampedModel):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    color = models.CharField(max_length=7, default='#3B82F6')

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tag'
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class MediaFile(UUIDPrimaryKeyMixin, TimeStampedModel):
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to=generate_uuid_filename)
    original_filename = models.CharField(max_length=500)
    file_type = models.CharField(max_length=20, choices=[
        ('IMAGE', 'Gambar'), ('VIDEO', 'Video'), ('DOCUMENT', 'Dokumen'),
        ('AUDIO', 'Audio'), ('OTHER', 'Lainnya')
    ])
    mime_type = models.CharField(max_length=100, blank=True, default='')
    file_size = models.PositiveBigIntegerField(default=0)
    width = models.PositiveIntegerField(null=True, blank=True)
    height = models.PositiveIntegerField(null=True, blank=True)
    alt_text = models.CharField(max_length=255, blank=True, default='')
    caption = models.TextField(blank=True, default='')
    folder = models.ForeignKey(
        Folder, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='files', verbose_name='Folder'
    )
    tags = models.ManyToManyField(Tag, blank=True, related_name='files')
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, related_name='uploaded_media'
    )
    partner = models.ForeignKey(
        'platform.Partner', on_delete=models.CASCADE,
        null=True, blank=True, related_name='media_files',
        help_text="Partner yang memiliki file ini."
    )
    thumbnail = models.FileField(upload_to='thumbnails/', blank=True, null=True)
    is_public = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'File Media'
        verbose_name_plural = 'File Media'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    @property
    def file_extension(self):
        return os.path.splitext(self.original_filename)[1].lower()

    @property
    def is_image(self):
        return self.file_type == 'IMAGE'

    @property
    def is_video(self):
        return self.file_type == 'VIDEO'

    @property
    def is_document(self):
        return self.file_type == 'DOCUMENT'

    @property
    def is_audio(self):
        return self.file_type == 'AUDIO'

    @property
    def formatted_size(self):
        size = self.file_size
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} TB"

    @property
    def type_badge_color(self):
        colors = {
            'IMAGE': 'bg-green-100 text-green-800',
            'VIDEO': 'bg-blue-100 text-blue-800',
            'DOCUMENT': 'bg-yellow-100 text-yellow-800',
            'AUDIO': 'bg-purple-100 text-purple-800',
            'OTHER': 'bg-gray-100 text-gray-800',
        }
        return colors.get(self.file_type, 'bg-gray-100 text-gray-800')
