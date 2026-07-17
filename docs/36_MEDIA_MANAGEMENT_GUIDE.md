# 36. Media Management Guide

## Overview

This guide covers the media management system in Kabulhaden CMS, including file uploads, storage, organization, compression, and thumbnail generation.

---

## Media Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                   Media Management System                     │
│                                                              │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐   │
│  │  Upload Form  │───▶│  Processing  │───▶│   Storage    │   │
│  │  (views.py)   │    │  (services)  │    │  (local/S3)  │   │
│  └──────────────┘    └──────────────┘    └──────────────┘   │
│         │                   │                   │            │
│         ▼                   ▼                   ▼            │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐   │
│  │   Validate    │    │  Compress    │    │   Organize   │   │
│  │   - Size      │    │  - Audio     │    │   - Folders  │   │
│  │   - Type      │    │  - Image     │    │   - Metadata │   │
│  │   - Duration  │    │  - Video     │    │   - Search   │   │
│  └──────────────┘    └──────────────┘    └──────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

---

## Supported File Types

### Audio

| Extension | MIME Type | Max Size | Notes |
|-----------|-----------|----------|-------|
| `.mp3` | audio/mpeg | 500 MB | Primary format |
| `.wav` | audio/wav | 1 GB | Uncompressed |
| `.ogg` | audio/ogg | 500 MB | Open format |
| `.flac` | audio/flac | 1 GB | Lossless |
| `.m4a` | audio/mp4 | 500 MB | AAC format |

### Images

| Extension | MIME Type | Max Size | Notes |
|-----------|-----------|----------|-------|
| `.jpg` | image/jpeg | 10 MB | Primary format |
| `.png` | image/png | 10 MB | Transparent |
| `.gif` | image/gif | 10 MB | Animated |
| `.webp` | image/webp | 10 MB | Modern format |
| `.svg` | image/svg+xml | 1 MB | Vector |

### Video (Future)

| Extension | MIME Type | Max Size | Notes |
|-----------|-----------|----------|-------|
| `.mp4` | video/mp4 | 2 GB | Primary format |
| `.webm` | video/webm | 1 GB | Web format |

---

## Media Models

```python
# apps/media_manager/models.py
class MediaFolder(UUIDPrimaryKeyMixin, TimeStampMixin):
    name = models.CharField(max_length=200)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    
    class Meta:
        verbose_name_plural = 'Media folders'
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    @property
    def full_path(self):
        if self.parent:
            return f"{self.parent.full_path}/{self.name}"
        return self.name


class Media(UUIDPrimaryKeyMixin, TimeStampMixin):
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='media/%Y/%m/')
    file_type = models.CharField(max_length=20, choices=MediaType.choices)
    mime_type = models.CharField(max_length=100)
    file_size = models.BigIntegerField()  # bytes
    duration = models.FloatField(null=True, blank=True)  # seconds, for audio/video
    folder = models.ForeignKey(MediaFolder, null=True, blank=True, on_delete=models.SET_NULL)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    thumbnail = models.ImageField(upload_to='thumbnails/', null=True, blank=True)
    metadata = models.JSONField(default=dict)
    
    class Meta:
        verbose_name_plural = 'Media'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    @property
    def file_size_display(self):
        """Human-readable file size."""
        size = self.file_size
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024:
                return f"{size:.1f} {unit}"
            size /= 1024
        return f"{size:.1f} TB"
    
    @property
    def duration_display(self):
        """Human-readable duration."""
        if not self.duration:
            return '--:--'
        minutes = int(self.duration // 60)
        seconds = int(self.duration % 60)
        return f"{minutes:02d}:{seconds:02d}"
```

---

## Upload Flow

```
┌─────────────────────────────────────────────────────────────┐
│                    Upload Process                             │
│                                                              │
│  1. User drops file or clicks upload                         │
│     ───────────────────────────────────────▶                  │
│                                                              │
│  2. Frontend validation                                      │
│     - File type check                                        │
│     - File size check                                        │
│     ───────────────────────────────────────▶                  │
│                                                              │
│  3. Server-side validation                                   │
│     - MIME type verification                                 │
│     - Size limit check                                       │
│     - Duplicate detection                                    │
│     ───────────────────────────────────────▶                  │
│                                                              │
│  4. File storage                                             │
│     - Save to media/%Y/%m/                                   │
│     - Generate unique filename if needed                     │
│     ───────────────────────────────────────▶                  │
│                                                              │
│  5. Post-processing                                          │
│     - Extract metadata (duration, bitrate)                   │
│     - Generate thumbnail (images)                            │
│     - Optional compression                                   │
│     ───────────────────────────────────────▶                  │
│                                                              │
│  6. Database record creation                                 │
│     - Create Media instance                                  │
│     - Link to folder                                         │
│     - Return response                                        │
└─────────────────────────────────────────────────────────────┘
```

### Upload View

```python
# apps/media_manager/views.py
class MediaUploadView(LoginRequiredMixin, CreateView):
    model = Media
    form_class = MediaUploadForm
    template_name = 'media_manager/media_upload.html'
    success_url = reverse_lazy('media:list')
    
    def form_valid(self, form):
        form.instance.uploaded_by = self.request.user
        form.instance.file_size = form.instance.file.size
        form.instance.mime_type = form.instance.file.content_type
        
        # Extract metadata
        if form.instance.file_type in ('audio', 'video'):
            duration = extract_duration(form.instance.file.path)
            form.instance.duration = duration
        
        # Generate thumbnail for images
        if form.instance.file_type == 'image':
            thumbnail = generate_thumbnail(form.instance.file.path)
            form.instance.thumbnail = thumbnail
        
        messages.success(self.request, 'Media berhasil diunggah.')
        return super().form_valid(form)
```

---

## Media Services

```python
# apps/media_manager/services.py
import os
from mutagen import File as MutagenFile
from PIL import Image


class MediaService:
    def __init__(self, repository):
        self.repository = repository
    
    def upload(self, file, user, folder=None):
        """Process and store uploaded media."""
        media = Media(
            title=os.path.splitext(file.name)[0],
            file=file,
            file_type=self._get_file_type(file),
            mime_type=file.content_type,
            file_size=file.size,
            folder=folder,
            uploaded_by=user,
        )
        
        # Extract audio metadata
        if media.file_type == 'audio':
            metadata = self._extract_audio_metadata(file)
            media.duration = metadata.get('duration')
            media.metadata = metadata
        
        # Generate thumbnail for images
        if media.file_type == 'image':
            media.thumbnail = self._generate_thumbnail(file)
        
        media.save()
        return media
    
    def _get_file_type(self, file):
        ext = os.path.splitext(file.name)[1].lower()
        type_map = {
            '.mp3': 'audio', '.wav': 'audio', '.ogg': 'audio',
            '.flac': 'audio', '.m4a': 'audio',
            '.jpg': 'image', '.jpeg': 'image', '.png': 'image',
            '.gif': 'image', '.webp': 'image',
            '.mp4': 'video', '.webm': 'video',
        }
        return type_map.get(ext, 'other')
    
    def _extract_audio_metadata(self, file):
        try:
            audio = MutagenFile(file)
            return {
                'duration': audio.info.length if audio.info else None,
                'bitrate': audio.info.bitrate if audio.info else None,
                'sample_rate': audio.info.sample_rate if audio.info else None,
            }
        except Exception:
            return {}
    
    def _generate_thumbnail(self, file, size=(200, 200)):
        try:
            img = Image.open(file)
            img.thumbnail(size)
            
            thumb_name = f"thumb_{file.name}"
            thumb_path = os.path.join('thumbnails', thumb_name)
            img.save(thumb_path)
            return thumb_path
        except Exception:
            return None
    
    def compress_media(self, media_id, quality=0.8):
        """Compress media file."""
        media = self.repository.get(media_id)
        # Compression logic here
        return media
    
    def cleanup_orphaned(self):
        """Remove files not linked to any Media record."""
        from django.conf import settings
        media_root = settings.MEDIA_ROOT
        
        db_files = set(
            Media.objects.values_list('file', flat=True)
        )
        
        removed = 0
        for root, dirs, files in os.walk(media_root):
            for file in files:
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, media_root)
                if rel_path not in db_files:
                    os.remove(file_path)
                    removed += 1
        
        return removed
```

---

## Folder Organization

### Folder Tree

```
Media/
├── Audio/
│   ├── Program/
│   │   ├── Berita/
│   │   ├── Musik/
│   │   └── Bicara/
│   ├── Episode/
│   └── Jingle/
├── Images/
│   ├── Logo/
│   ├── Banner/
│   └── Thumbnail/
├── Video/ (future)
└── Archive/
```

### Folder Views

```python
# apps/media_manager/views.py
class FolderListView(LoginRequiredMixin, ListView):
    model = MediaFolder
    template_name = 'media_manager/folder_list.html'
    
    def get_queryset(self):
        return MediaFolder.objects.filter(parent=None)


class FolderDetailView(LoginRequiredMixin, DetailView):
    model = MediaFolder
    template_name = 'media_manager/folder_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['media_list'] = Media.objects.filter(folder=self.object)
        context['subfolders'] = MediaFolder.objects.filter(parent=self.object)
        return context
```

---

## Management Commands

### Cleanup Orphaned Media

```python
# apps/media_manager/management/commands/cleanup_media.py
from django.core.management.base import BaseCommand
from apps.media_manager.services import MediaService


class Command(BaseCommand):
    help = 'Remove media files not linked to database records'
    
    def handle(self, *args, **options):
        service = MediaService()
        removed = service.cleanup_orphaned()
        self.stdout.write(
            self.style.SUCCESS(f'Successfully removed {removed} orphaned files')
        )
```

### Generate Thumbnails

```python
# apps/media_manager/management/commands/generate_thumbnails.py
from django.core.management.base import BaseCommand
from apps.media_manager.models import Media


class Command(BaseCommand):
    help = 'Generate thumbnails for all images'
    
    def handle(self, *args, **options):
        images = Media.objects.filter(file_type='image', thumbnail__isnull=True)
        generated = 0
        
        for image in images:
            thumbnail = generate_thumbnail(image.file.path)
            if thumbnail:
                image.thumbnail = thumbnail
                image.save()
                generated += 1
        
        self.stdout.write(
            self.style.SUCCESS(f'Generated {generated} thumbnails')
        )
```

### Compress Media

```python
# apps/media_manager/management/commands/compress_media.py
from django.core.management.base import BaseCommand
from apps.media_manager.models import Media


class Command(BaseCommand):
    help = 'Compress media files'
    
    def add_arguments(self, parser):
        parser.add_argument('--quality', type=float, default=0.8)
        parser.add_argument('--type', type=str, choices=['audio', 'image'])
    
    def handle(self, *args, **options):
        quality = options['quality']
        media_type = options.get('type')
        
        queryset = Media.objects.all()
        if media_type:
            queryset = queryset.filter(file_type=media_type)
        
        compressed = 0
        for media in queryset:
            if compress_file(media.file.path, quality):
                compressed += 1
        
        self.stdout.write(
            self.style.SUCCESS(f'Compressed {compressed} files')
        )
```

---

## Media Statistics

### Usage Dashboard

```
┌──────────────────────────────────────────────────────────────┐
│  Statistik Media                                              │
│                                                               │
│  Total: 1,234 files (45.6 GB)                                │
│                                                               │
│  ┌────────────┬────────────┬────────────┬────────────┐       │
│  │   Audio    │   Images   │   Video    │   Other    │       │
│  │   856      │   312      │   45       │   21       │       │
│  │   (38.2GB) │ (2.1GB)    │ (5.0GB)   │ (0.3GB)    │       │
│  └────────────┴────────────┴────────────┴────────────┘       │
│                                                               │
│  Storage Usage:                                               │
│  ████████████████░░░░░░░░░░░░░  45.6 GB / 100 GB (45.6%)   │
│                                                               │
│  Recent Uploads:                                              │
│  - news_2026_07_15.mp3 (4.2 MB) - 2 jam lalu               │
│  - banner_ramadan.png (1.1 MB) - 5 jam lalu                 │
│  - podcast_ep42.mp3 (15.3 MB) - 1 hari lalu                │
└──────────────────────────────────────────────────────────────┘
```

---

## Storage Configuration

### Local Storage

```python
# config/settings/base.py
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

### S3 Storage (Production)

```python
# config/settings/production.py
AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = env('AWS_STORAGE_BUCKET_NAME')
AWS_S3_REGION_NAME = env('AWS_S3_REGION_NAME', default='ap-southeast-1')
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = 'private'
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
```

---

## Related Documentation

- `erd.md` - Media entity relationships
- `31_API_ENDPOINTS_REFERENCE.md` - Media API endpoints
- `25_TAILWIND_CONFIG.md` - Media card styles
- `15_TABLE_DESIGN.md` - Media list table

---

*Last updated: 2026-07-15*
