from django.contrib import admin
from .models import Discussion, Reply


class ReplyInline(admin.TabularInline):
    model = Reply
    extra = 0
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Discussion)
class DiscussionAdmin(admin.ModelAdmin):
    list_display = ('title', 'author_name', 'category', 'is_pinned', 'is_locked', 'view_count', 'reply_count', 'created_at')
    list_filter = ('is_pinned', 'is_locked', 'category')
    search_fields = ('title', 'content', 'author_name', 'author_email')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ReplyInline]
    date_hierarchy = 'created_at'


@admin.register(Reply)
class ReplyAdmin(admin.ModelAdmin):
    list_display = ('discussion', 'author_name', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('content', 'author_name', 'author_email')
    date_hierarchy = 'created_at'
