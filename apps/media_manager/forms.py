from django import forms
from django.core.exceptions import ValidationError
import os

ALLOWED_TYPES = {
    'image': ['jpg', 'jpeg', 'png', 'gif', 'webp', 'svg', 'bmp', 'ico'],
    'video': ['mp4', 'webm', 'ogg', 'avi', 'mov', 'mkv'],
    'document': ['pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'txt', 'csv', 'rtf'],
    'audio': ['mp3', 'wav', 'ogg', 'flac', 'aac', 'm4a'],
}


def validate_file_upload(file_obj, max_size_mb=10):
    ext = os.path.splitext(file_obj.name)[1].lower().lstrip('.')
    all_types = []
    for types in ALLOWED_TYPES.values():
        all_types.extend(types)
    if ext not in all_types:
        raise ValidationError(f'Tipe file tidak didukung: .{ext}')
    if file_obj.size > max_size_mb * 1024 * 1024:
        raise ValidationError(f'Ukuran file melebihi batas maksimum ({max_size_mb} MB).')
    return True


class FolderForm(forms.ModelForm):
    class Meta:
        from .models import Folder
        model = Folder
        fields = ['name', 'parent', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Nama folder'}),
            'parent': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-input', 'rows': 2}),
        }


class TagForm(forms.ModelForm):
    class Meta:
        from .models import Tag
        model = Tag
        fields = ['name', 'color']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Nama tag'}),
            'color': forms.TextInput(attrs={'class': 'form-input', 'type': 'color'}),
        }


class MediaFileUploadForm(forms.Form):
    folder = forms.UUIDField(required=False, widget=forms.HiddenInput())
    is_public = forms.BooleanField(initial=True, required=False, widget=forms.CheckboxInput(attrs={'class': 'form-checkbox'}))


class MediaFileEditForm(forms.ModelForm):
    class Meta:
        from .models import MediaFile
        model = MediaFile
        fields = ['title', 'alt_text', 'caption', 'folder', 'is_public']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'alt_text': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Deskripsi gambar untuk aksesibilitas'}),
            'caption': forms.Textarea(attrs={'class': 'form-input', 'rows': 2}),
            'folder': forms.Select(attrs={'class': 'form-select'}),
            'is_public': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
        }


class MediaSearchForm(forms.Form):
    q = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Cari file media...',
            'hx-get': '/media/api/search/',
            'hx-trigger': 'keyup changed delay:300ms',
            'hx-target': '#media-grid',
        })
    )
    file_type = forms.ChoiceField(
        required=False,
        choices=[('', 'Semua Tipe')] + [
            ('IMAGE', 'Gambar'), ('VIDEO', 'Video'),
            ('DOCUMENT', 'Dokumen'), ('AUDIO', 'Audio'), ('OTHER', 'Lainnya')
        ],
        widget=forms.Select(attrs={'class': 'form-select', 'hx-get': '/media/api/search/', 'hx-trigger': 'change', 'hx-target': '#media-grid'})
    )
    folder = forms.UUIDField(required=False, widget=forms.HiddenInput())
