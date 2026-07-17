from utils.services import BaseService
from .repositories import (
    SiteSettingsRepository, SEOSettingsRepository, EmailSettingsRepository,
    SecuritySettingsRepository, AppearanceSettingsRepository, NotificationSettingsRepository,
    SocialMediaSettingsRepository, ContentSettingsRepository, LanguageSettingsRepository,
    MediaSettingsRepository
)
from .models import (
    SiteSettings, SEOSettings, EmailSettings, SecuritySettings,
    AppearanceSettings, NotificationSettings, SocialMediaSettings,
    ContentSettings, LanguageSettings, MediaSettings
)


class SiteSettingsService(BaseService[SiteSettingsRepository]):
    def __init__(self):
        repo = SiteSettingsRepository()
        super().__init__(repo)

    def get_settings(self):
        return SiteSettings.load()

    def update(self, **kwargs):
        settings = SiteSettings.load()
        for key, value in kwargs.items():
            setattr(settings, key, value)
        settings.save()
        return settings


class SEOSettingsService(BaseService[SEOSettingsRepository]):
    def __init__(self):
        repo = SEOSettingsRepository()
        super().__init__(repo)

    def get_settings(self):
        return SEOSettings.load()

    def update(self, **kwargs):
        settings = SEOSettings.load()
        for key, value in kwargs.items():
            setattr(settings, key, value)
        settings.save()
        return settings


class EmailSettingsService(BaseService[EmailSettingsRepository]):
    def __init__(self):
        repo = EmailSettingsRepository()
        super().__init__(repo)

    def get_settings(self):
        return EmailSettings.load()

    def update(self, **kwargs):
        settings = EmailSettings.load()
        for key, value in kwargs.items():
            setattr(settings, key, value)
        settings.save()
        return settings


class SecuritySettingsService(BaseService[SecuritySettingsRepository]):
    def __init__(self):
        repo = SecuritySettingsRepository()
        super().__init__(repo)

    def get_settings(self):
        return SecuritySettings.load()

    def update(self, **kwargs):
        settings = SecuritySettings.load()
        for key, value in kwargs.items():
            setattr(settings, key, value)
        settings.save()
        return settings


class AppearanceSettingsService(BaseService[AppearanceSettingsRepository]):
    def __init__(self):
        repo = AppearanceSettingsRepository()
        super().__init__(repo)

    def get_settings(self):
        return AppearanceSettings.load()

    def update(self, **kwargs):
        settings = AppearanceSettings.load()
        for key, value in kwargs.items():
            setattr(settings, key, value)
        settings.save()
        return settings


class NotificationSettingsService(BaseService[NotificationSettingsRepository]):
    def __init__(self):
        repo = NotificationSettingsRepository()
        super().__init__(repo)

    def get_settings(self):
        return NotificationSettings.load()

    def update(self, **kwargs):
        settings = NotificationSettings.load()
        for key, value in kwargs.items():
            setattr(settings, key, value)
        settings.save()
        return settings


class SocialMediaSettingsService(BaseService[SocialMediaSettingsRepository]):
    def __init__(self):
        repo = SocialMediaSettingsRepository()
        super().__init__(repo)

    def get_settings(self):
        return SocialMediaSettings.load()

    def update(self, **kwargs):
        settings = SocialMediaSettings.load()
        for key, value in kwargs.items():
            setattr(settings, key, value)
        settings.save()
        return settings


class ContentSettingsService(BaseService[ContentSettingsRepository]):
    def __init__(self):
        repo = ContentSettingsRepository()
        super().__init__(repo)

    def get_settings(self):
        return ContentSettings.load()

    def update(self, **kwargs):
        settings = ContentSettings.load()
        for key, value in kwargs.items():
            setattr(settings, key, value)
        settings.save()
        return settings


class LanguageSettingsService(BaseService[LanguageSettingsRepository]):
    def __init__(self):
        repo = LanguageSettingsRepository()
        super().__init__(repo)

    def get_settings(self):
        return LanguageSettings.load()

    def update(self, **kwargs):
        settings = LanguageSettings.load()
        for key, value in kwargs.items():
            setattr(settings, key, value)
        settings.save()
        return settings


class MediaSettingsService(BaseService[MediaSettingsRepository]):
    def __init__(self):
        repo = MediaSettingsRepository()
        super().__init__(repo)

    def get_settings(self):
        return MediaSettings.load()

    def update(self, **kwargs):
        settings = MediaSettings.load()
        for key, value in kwargs.items():
            setattr(settings, key, value)
        settings.save()
        return settings
