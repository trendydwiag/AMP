import os
import mimetypes
from django.core.exceptions import ValidationError


ALLOWED_EXTENSIONS = {
    'image': {'jpg', 'jpeg', 'png', 'gif', 'webp', 'svg', 'bmp', 'ico'},
    'video': {'mp4', 'webm', 'ogg', 'avi', 'mov', 'mkv'},
    'document': {'pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'txt', 'csv', 'rtf'},
    'audio': {'mp3', 'wav', 'ogg', 'flac', 'aac', 'm4a'},
}


def validate_media_file(file_obj, max_size_mb=10):
    ext = os.path.splitext(file_obj.name)[1].lower().lstrip('.')
    all_extensions = set()
    for exts in ALLOWED_EXTENSIONS.values():
        all_extensions.update(exts)
    if ext not in all_extensions:
        raise ValidationError(f'Tipe file tidak didukung: .{ext}. Tipe yang diizinkan: {", ".join(sorted(all_extensions))}')
    if file_obj.size > max_size_mb * 1024 * 1024:
        raise ValidationError(f'Ukuran file ({file_obj.size / (1024*1024):.1f} MB) melebihi batas maksimum ({max_size_mb} MB).')
    return True


def validate_image_file(file_obj, max_size_mb=10):
    ext = os.path.splitext(file_obj.name)[1].lower().lstrip('.')
    if ext not in ALLOWED_EXTENSIONS['image']:
        raise ValidationError(f'File bukan gambar yang valid: .{ext}')
    if file_obj.size > max_size_mb * 1024 * 1024:
        raise ValidationError(f'Ukuran gambar melebihi batas ({max_size_mb} MB).')
    return True


def get_file_type_from_mime(mime_type):
    if not mime_type:
        return 'OTHER'
    if mime_type.startswith('image/'):
        return 'IMAGE'
    if mime_type.startswith('video/'):
        return 'VIDEO'
    if mime_type.startswith('audio/'):
        return 'AUDIO'
    if any(t in mime_type for t in ['pdf', 'document', 'text', 'spreadsheet', 'presentation']):
        return 'DOCUMENT'
    return 'OTHER'


def get_file_type_from_extension(filename):
    ext = os.path.splitext(filename)[1].lower().lstrip('.')
    if ext in ALLOWED_EXTENSIONS['image']:
        return 'IMAGE'
    if ext in ALLOWED_EXTENSIONS['video']:
        return 'VIDEO'
    if ext in ALLOWED_EXTENSIONS['audio']:
        return 'AUDIO'
    if ext in ALLOWED_EXTENSIONS['document']:
        return 'DOCUMENT'
    return 'OTHER'
