from django.contrib import admin
from django.utils.html import format_html
from .models import Folder, Tag, MediaFile


@admin.register(Folder)
class FolderAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'file_count', 'created_by', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'color')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(MediaFile)
class MediaFileAdmin(admin.ModelAdmin):
    list_display = ('title', 'file_type', 'formatted_size', 'folder', 'uploaded_by', 'is_public', 'created_at')
    list_filter = ('file_type', 'is_public', 'folder')
    search_fields = ('title', 'original_filename', 'alt_text')
    readonly_fields = ('original_filename', 'mime_type', 'file_size', 'width', 'height')
