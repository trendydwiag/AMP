from django.contrib import admin
from .models import (
    Program, Host, HostMember, Schedule, BroadcastSession,
    Episode, GuestStar, EpisodeGuest, Playlist, PlaylistItem, Announcement
)


class HostMemberInline(admin.TabularInline):
    model = HostMember
    extra = 0


class ScheduleInline(admin.TabularInline):
    model = Schedule
    extra = 0


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'genre', 'content_rating', 'featured', 'active', 'created_at')
    list_filter = ('active', 'featured', 'content_rating', 'category')
    search_fields = ('title', 'short_description', 'category', 'genre')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [HostMemberInline, ScheduleInline]


@admin.register(Host)
class HostAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'stage_name', 'email', 'active', 'created_at')
    list_filter = ('active',)
    search_fields = ('full_name', 'stage_name', 'email')


@admin.register(HostMember)
class HostMemberAdmin(admin.ModelAdmin):
    list_display = ('host', 'program', 'is_lead', 'joined_date')
    list_filter = ('is_lead',)
    search_fields = ('host__full_name', 'program__title')


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('program', 'day_of_week', 'start_time', 'end_time', 'repeat_weekly', 'active')
    list_filter = ('day_of_week', 'active')
    search_fields = ('program__title',)


@admin.register(BroadcastSession)
class BroadcastSessionAdmin(admin.ModelAdmin):
    list_display = ('program', 'status', 'start_datetime', 'end_datetime', 'created_at')
    list_filter = ('status',)
    search_fields = ('program__title',)
    date_hierarchy = 'start_datetime'


@admin.register(Episode)
class EpisodeAdmin(admin.ModelAdmin):
    list_display = ('title', 'program', 'episode_number', 'published', 'publish_date')
    list_filter = ('published', 'program')
    search_fields = ('title', 'description')
    date_hierarchy = 'publish_date'


@admin.register(GuestStar)
class GuestStarAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'organization', 'created_at')
    search_fields = ('full_name', 'organization')


@admin.register(EpisodeGuest)
class EpisodeGuestAdmin(admin.ModelAdmin):
    list_display = ('episode', 'guest', 'role')
    search_fields = ('episode__title', 'guest__full_name')


@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    list_display = ('title', 'program', 'active', 'created_at')
    list_filter = ('active',)
    search_fields = ('title', 'program__title')


@admin.register(PlaylistItem)
class PlaylistItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist', 'album', 'duration', 'sequence', 'playlist')
    list_filter = ('playlist',)
    search_fields = ('title', 'artist')


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'publish_start', 'publish_end', 'active')
    list_filter = ('active',)
    search_fields = ('title', 'content')
    date_hierarchy = 'publish_start'
