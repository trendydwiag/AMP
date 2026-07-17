from django.contrib import admin
from .models import (
    SiteSettings, SEOSettings, EmailSettings, SecuritySettings,
    AppearanceSettings, NotificationSettings, SocialMediaSettings,
    ContentSettings, LanguageSettings, MediaSettings
)


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ('site_name', 'maintenance_mode')


@admin.register(SEOSettings)
class SEOSettingsAdmin(admin.ModelAdmin):
    list_display = ('meta_title', 'robots_meta')


@admin.register(EmailSettings)
class EmailSettingsAdmin(admin.ModelAdmin):
    list_display = ('email_host', 'email_port', 'email_use_tls')


@admin.register(SecuritySettings)
class SecuritySettingsAdmin(admin.ModelAdmin):
    list_display = ('session_timeout_minutes', 'max_login_attempts', 'enable_2fa')


@admin.register(AppearanceSettings)
class AppearanceSettingsAdmin(admin.ModelAdmin):
    list_display = ('primary_color', 'dark_mode', 'font_family')


@admin.register(NotificationSettings)
class NotificationSettingsAdmin(admin.ModelAdmin):
    list_display = ('email_on_user_register', 'notify_admins_on_error')


@admin.register(SocialMediaSettings)
class SocialMediaSettingsAdmin(admin.ModelAdmin):
    list_display = ('facebook_url', 'twitter_url', 'instagram_url')


@admin.register(ContentSettings)
class ContentSettingsAdmin(admin.ModelAdmin):
    list_display = ('posts_per_page', 'enable_comments', 'max_upload_size_mb')


@admin.register(LanguageSettings)
class LanguageSettingsAdmin(admin.ModelAdmin):
    list_display = ('site_language', 'date_format', 'timezone')


@admin.register(MediaSettings)
class MediaSettingsAdmin(admin.ModelAdmin):
    list_display = ('storage_backend', 'max_file_size_mb', 'auto_generate_thumbnails')
