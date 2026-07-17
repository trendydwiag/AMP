from django.core.management.base import BaseCommand
from apps.settings.models import (
    SiteSettings, SEOSettings, EmailSettings, SecuritySettings,
    AppearanceSettings, NotificationSettings, SocialMediaSettings,
    ContentSettings, LanguageSettings, MediaSettings
)


class Command(BaseCommand):
    help = 'Inisialisasi semua pengaturan default (singleton)'

    def handle(self, *args, **options):
        models = [
            SiteSettings, SEOSettings, EmailSettings, SecuritySettings,
            AppearanceSettings, NotificationSettings, SocialMediaSettings,
            ContentSettings, LanguageSettings, MediaSettings
        ]
        for model in models:
            obj, created = model.objects.get_or_create(pk=1)
            status = 'DIBUAT' if created else 'ADA'
            self.stdout.write(f'  {model._meta.verbose_name}: {status}')
        self.stdout.write(self.style.SUCCESS('Semua pengaturan berhasil diinisialisasi.'))
