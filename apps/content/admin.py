from django.contrib import admin
from .models import (
    ContentCategory, ContentTag, Author, SEOModel,
    ContentVersion, PublishingQueue, ContentHighlight
)


@admin.register(ContentCategory)
class ContentCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'content_type', 'parent', 'active', 'display_order']
    list_filter = ['content_type', 'active']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(ContentTag)
class ContentTagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'color', 'usage_count']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'active']
    list_filter = ['active']
    search_fields = ['name', 'email']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(SEOModel)
class SEOModelAdmin(admin.ModelAdmin):
    list_display = ['content_type', 'object_id', 'title', 'seo_score', 'seo_grade']
    search_fields = ['title', 'description']
    list_filter = ['robots']


@admin.register(ContentVersion)
class ContentVersionAdmin(admin.ModelAdmin):
    list_display = ['content_type', 'content_id', 'version_number', 'title', 'author', 'is_current']
    list_filter = ['content_type', 'is_current']
    search_fields = ['title', 'change_summary']


@admin.register(PublishingQueue)
class PublishingQueueAdmin(admin.ModelAdmin):
    list_display = ['content_type', 'content_id', 'scheduled_at', 'status', 'created_by']
    list_filter = ['content_type', 'status']
    search_fields = ['error_message']


@admin.register(ContentHighlight)
class ContentHighlightAdmin(admin.ModelAdmin):
    list_display = ['highlight_type', 'content_type', 'content_id', 'display_order', 'active']
    list_filter = ['highlight_type', 'content_type', 'active']
