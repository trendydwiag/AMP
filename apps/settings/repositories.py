from utils.repositories import BaseRepository
from .models import (
    SiteSettings, SEOSettings, EmailSettings, SecuritySettings,
    AppearanceSettings, NotificationSettings, SocialMediaSettings,
    ContentSettings, LanguageSettings, MediaSettings
)


class SiteSettingsRepository(BaseRepository[SiteSettings]):
    def __init__(self):
        super().__init__(SiteSettings)


class SEOSettingsRepository(BaseRepository[SEOSettings]):
    def __init__(self):
        super().__init__(SEOSettings)


class EmailSettingsRepository(BaseRepository[EmailSettings]):
    def __init__(self):
        super().__init__(EmailSettings)


class SecuritySettingsRepository(BaseRepository[SecuritySettings]):
    def __init__(self):
        super().__init__(SecuritySettings)


class AppearanceSettingsRepository(BaseRepository[AppearanceSettings]):
    def __init__(self):
        super().__init__(AppearanceSettings)


class NotificationSettingsRepository(BaseRepository[NotificationSettings]):
    def __init__(self):
        super().__init__(NotificationSettings)


class SocialMediaSettingsRepository(BaseRepository[SocialMediaSettings]):
    def __init__(self):
        super().__init__(SocialMediaSettings)


class ContentSettingsRepository(BaseRepository[ContentSettings]):
    def __init__(self):
        super().__init__(ContentSettings)


class LanguageSettingsRepository(BaseRepository[LanguageSettings]):
    def __init__(self):
        super().__init__(LanguageSettings)


class MediaSettingsRepository(BaseRepository[MediaSettings]):
    def __init__(self):
        super().__init__(MediaSettings)
