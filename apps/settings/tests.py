from django.test import TestCase, Client, override_settings
from django.urls import reverse
from apps.settings.models import (
    SiteSettings, SEOSettings, EmailSettings, SecuritySettings,
    AppearanceSettings, NotificationSettings, SocialMediaSettings,
    ContentSettings, LanguageSettings, MediaSettings
)
from apps.users.models import User


class SettingsModelsTest(TestCase):
    def test_site_settings_singleton(self):
        s = SiteSettings.load()
        self.assertEqual(s.pk, 1)
        s2 = SiteSettings.load()
        self.assertEqual(s.pk, s2.pk)

    def test_seo_settings_singleton(self):
        s = SEOSettings.load()
        self.assertEqual(s.pk, 1)

    def test_email_settings_singleton(self):
        s = EmailSettings.load()
        self.assertEqual(s.pk, 1)

    def test_security_settings_singleton(self):
        s = SecuritySettings.load()
        self.assertEqual(s.pk, 1)
        self.assertEqual(s.session_timeout_minutes, 60)
        self.assertEqual(s.max_login_attempts, 5)

    def test_appearance_settings_singleton(self):
        s = AppearanceSettings.load()
        self.assertEqual(s.pk, 1)
        self.assertEqual(s.primary_color, '#3B82F6')

    def test_notification_settings_singleton(self):
        s = NotificationSettings.load()
        self.assertEqual(s.pk, 1)
        self.assertTrue(s.email_on_user_register)

    def test_social_media_settings_singleton(self):
        s = SocialMediaSettings.load()
        self.assertEqual(s.pk, 1)

    def test_content_settings_singleton(self):
        s = ContentSettings.load()
        self.assertEqual(s.pk, 1)
        self.assertEqual(s.posts_per_page, 10)

    def test_language_settings_singleton(self):
        s = LanguageSettings.load()
        self.assertEqual(s.pk, 1)
        self.assertEqual(s.site_language, 'id')

    def test_media_settings_singleton(self):
        s = MediaSettings.load()
        self.assertEqual(s.pk, 1)
        self.assertEqual(s.storage_backend, 'local')

    def test_str_repr(self):
        self.assertEqual(str(SiteSettings.load()), 'Kabulhaden CMS')
        self.assertEqual(str(SecuritySettings.load()), 'Pengaturan Keamanan')


class SettingsViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = User.objects.create_superuser(
            username='admin', email='admin@test.com', password='TestPass123!'
        )
        self.user = User.objects.create_user(
            username='user1', email='user1@test.com', password='TestPass123!'
        )

    @override_settings(AUTHENTICATION_BACKENDS=['django.contrib.auth.backends.ModelBackend'])
    def test_admin_can_access_site_settings(self):
        self.client.login(username='admin', password='TestPass123!')
        resp = self.client.get(reverse('settings:site'))
        self.assertEqual(resp.status_code, 200)

    @override_settings(AUTHENTICATION_BACKENDS=['django.contrib.auth.backends.ModelBackend'])
    def test_non_admin_redirected(self):
        self.client.login(username='user1', password='TestPass123!')
        resp = self.client.get(reverse('settings:site'))
        self.assertIn(resp.status_code, [302, 403])

    def test_unauthenticated_redirected(self):
        resp = self.client.get(reverse('settings:site'))
        self.assertEqual(resp.status_code, 302)

    @override_settings(AUTHENTICATION_BACKENDS=['django.contrib.auth.backends.ModelBackend'])
    def test_update_site_settings(self):
        self.client.login(username='admin', password='TestPass123!')
        resp = self.client.post(reverse('settings:site'), {
            'site_name': 'New Name',
            'site_tagline': 'New Tagline',
            'maintenance_mode': True,
        })
        self.assertEqual(resp.status_code, 302)
        s = SiteSettings.load()
        self.assertEqual(s.site_name, 'New Name')

    @override_settings(AUTHENTICATION_BACKENDS=['django.contrib.auth.backends.ModelBackend'])
    def test_all_settings_urls(self):
        self.client.login(username='admin', password='TestPass123!')
        urls = ['site', 'seo', 'email', 'security', 'appearance',
                'notification', 'social_media', 'content', 'language', 'media']
        for name in urls:
            resp = self.client.get(reverse(f'settings:{name}'))
            self.assertEqual(resp.status_code, 200, f'Failed for {name}')

    @override_settings(AUTHENTICATION_BACKENDS=['django.contrib.auth.backends.ModelBackend'])
    def test_update_security_settings(self):
        self.client.login(username='admin', password='TestPass123!')
        resp = self.client.post(reverse('settings:security'), {
            'session_timeout_minutes': 30,
            'max_login_attempts': 3,
            'lockout_duration_minutes': 10,
            'password_min_length': 14,
            'require_uppercase': True,
            'require_lowercase': True,
            'require_numbers': True,
            'require_special_chars': True,
            'password_expiry_days': 60,
            'enable_2fa': False,
            'force_2fa_admin': False,
        })
        self.assertEqual(resp.status_code, 302)
        s = SecuritySettings.load()
        self.assertEqual(s.session_timeout_minutes, 30)
