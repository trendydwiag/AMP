from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from apps.users.decorators import admin_required
from .forms import (
    SiteSettingsForm, SEOSettingsForm, EmailSettingsForm, SecuritySettingsForm,
    AppearanceSettingsForm, NotificationSettingsForm, SocialMediaSettingsForm,
    ContentSettingsForm, LanguageSettingsForm, MediaSettingsForm
)
from .services import (
    SiteSettingsService, SEOSettingsService, EmailSettingsService,
    SecuritySettingsService, AppearanceSettingsService, NotificationSettingsService,
    SocialMediaSettingsService, ContentSettingsService, LanguageSettingsService,
    MediaSettingsService
)
from .models import (
    SiteSettings, SEOSettings, EmailSettings, SecuritySettings,
    AppearanceSettings, NotificationSettings, SocialMediaSettings,
    ContentSettings, LanguageSettings, MediaSettings
)


class SettingsBaseView(TemplateView):
    template_name = 'settings/base.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['settings_groups'] = [
            {'name': 'Pengaturan Situs', 'url': reverse('settings:site'), 'icon': 'globe'},
            {'name': 'Pengaturan SEO', 'url': reverse('settings:seo'), 'icon': 'search'},
            {'name': 'Pengaturan Email', 'url': reverse('settings:email'), 'icon': 'mail'},
            {'name': 'Pengaturan Keamanan', 'url': reverse('settings:security'), 'icon': 'shield'},
            {'name': 'Pengaturan Tampilan', 'url': reverse('settings:appearance'), 'icon': 'palette'},
            {'name': 'Pengaturan Notifikasi', 'url': reverse('settings:notification'), 'icon': 'bell'},
            {'name': 'Media Sosial', 'url': reverse('settings:social_media'), 'icon': 'share'},
            {'name': 'Pengaturan Konten', 'url': reverse('settings:content'), 'icon': 'document'},
            {'name': 'Bahasa & Lokal', 'url': reverse('settings:language'), 'icon': 'translate'},
            {'name': 'Pengaturan Media', 'url': reverse('settings:media'), 'icon': 'image'},
        ]
        return context


def _settings_view(form_class, service_class, model_class, tpl, title):
    """Factory function to create settings views."""
    @method_decorator(login_required, name='dispatch')
    @method_decorator(admin_required, name='dispatch')
    class View(TemplateView):
        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['title'] = title
            context['form'] = form_class(instance=model_class.load())
            context['settings_groups'] = SettingsBaseView().get_context_data()['settings_groups']
            return context

        def post(self, request, *args, **kwargs):
            instance = model_class.load()
            form = form_class(request.POST, request.FILES, instance=instance)
            if form.is_valid():
                form.save()
                messages.success(request, f'{title} berhasil diperbarui.')
                return redirect(request.path)
            context = self.get_context_data(**kwargs)
            context['form'] = form
            return self.render_to_response(context)

    View.template_name = tpl
    View.__name__ = f'{title.replace(" ", "")}View'
    return View


SiteSettingsView = _settings_view(
    SiteSettingsForm, SiteSettingsService, SiteSettings,
    'settings/site.html', 'Pengaturan Situs'
)
SEOSettingsView = _settings_view(
    SEOSettingsForm, SEOSettingsService, SEOSettings,
    'settings/seo.html', 'Pengaturan SEO'
)
EmailSettingsView = _settings_view(
    EmailSettingsForm, EmailSettingsService, EmailSettings,
    'settings/email.html', 'Pengaturan Email'
)
SecuritySettingsView = _settings_view(
    SecuritySettingsForm, SecuritySettingsService, SecuritySettings,
    'settings/security.html', 'Pengaturan Keamanan'
)
AppearanceSettingsView = _settings_view(
    AppearanceSettingsForm, AppearanceSettingsService, AppearanceSettings,
    'settings/appearance.html', 'Pengaturan Tampilan'
)
NotificationSettingsView = _settings_view(
    NotificationSettingsForm, NotificationSettingsService, NotificationSettings,
    'settings/notification.html', 'Pengaturan Notifikasi'
)
SocialMediaSettingsView = _settings_view(
    SocialMediaSettingsForm, SocialMediaSettingsService, SocialMediaSettings,
    'settings/social_media.html', 'Media Sosial'
)
ContentSettingsView = _settings_view(
    ContentSettingsForm, ContentSettingsService, ContentSettings,
    'settings/content.html', 'Pengaturan Konten'
)
LanguageSettingsView = _settings_view(
    LanguageSettingsForm, LanguageSettingsService, LanguageSettings,
    'settings/language.html', 'Bahasa & Lokal'
)
MediaSettingsView = _settings_view(
    MediaSettingsForm, MediaSettingsService, MediaSettings,
    'settings/media.html', 'Pengaturan Media'
)
