from django.contrib import admin
from .models import Podcast, PodcastEpisode


@admin.register(Podcast)
class PodcastAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'active', 'featured']
    list_filter = ['active', 'featured', 'category']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}


@admin.register(PodcastEpisode)
class PodcastEpisodeAdmin(admin.ModelAdmin):
    list_display = ['title', 'podcast', 'episode_number', 'published', 'publish_date']
    list_filter = ['published', 'podcast']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}
