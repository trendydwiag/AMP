import os
import uuid
from django.utils.text import slugify


def generate_uuid_filename(instance, filename):
    """Generate UUID-based filename to prevent collisions and path traversal."""
    ext = os.path.splitext(filename)[1].lower()
    safe_name = slugify(os.path.splitext(filename)[0])[:50]
    return f"uploads/{safe_name}-{uuid.uuid4().hex[:12]}{ext}"


def generate_thumbnail_path(instance, filename):
    """Generate path for thumbnail files."""
    ext = os.path.splitext(filename)[1].lower()
    return f"thumbnails/{uuid.uuid4().hex[:12]}{ext}"


def get_upload_path(subfolder):
    """Return a callable upload path generator for a given subfolder."""
    def uploader(instance, filename):
        ext = os.path.splitext(filename)[1].lower()
        safe_name = slugify(os.path.splitext(filename)[0])[:50]
        return f"{subfolder}/{safe_name}-{uuid.uuid4().hex[:12]}{ext}"
    return uploader
