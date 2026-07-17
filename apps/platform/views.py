import json
from django.views.generic import ListView, CreateView, DetailView, UpdateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from utils.permissions import RoleRequiredMixin

from .partner.models import Partner, PartnerMembership, PartnerDomain
from .providers import list_providers
from .feature_flags.models import FeatureFlag
from .themes.models import PartnerTheme


class PlatformDashboardView(LoginRequiredMixin, RoleRequiredMixin, TemplateView):
    template_name = 'platform/dashboard.html'
    allowed_roles = ['SUPERUSER', 'ADMINISTRATOR']

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['total_partners'] = Partner.objects.count()
        ctx['active_partners'] = Partner.objects.filter(status='ACTIVE').count()
        ctx['total_users'] = PartnerMembership.objects.filter(is_active=True).count()
        ctx['feature_flags'] = FeatureFlag.objects.all()[:10]
        ctx['providers'] = list_providers()
        return ctx


class PartnerListView(LoginRequiredMixin, RoleRequiredMixin, ListView):
    model = Partner
    template_name = 'platform/partner_list.html'
    context_object_name = 'partners'
    paginate_by = 20
    allowed_roles = ['SUPERUSER', 'ADMINISTRATOR']


class PartnerCreateView(LoginRequiredMixin, RoleRequiredMixin, CreateView):
    model = Partner
    template_name = 'platform/partner_form.html'
    fields = ['name', 'slug', 'tier', 'primary_domain', 'primary_color', 'secondary_color',
              'description', 'tagline', 'contact_email', 'max_users', 'max_storage_mb']
    success_url = reverse_lazy('platform:partner_list')
    allowed_roles = ['SUPERUSER', 'ADMINISTRATOR']


class PartnerDetailView(LoginRequiredMixin, RoleRequiredMixin, DetailView):
    model = Partner
    template_name = 'platform/partner_detail.html'
    context_object_name = 'partner'
    allowed_roles = ['SUPERUSER', 'ADMINISTRATOR']

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        partner = self.object
        ctx['memberships'] = PartnerMembership.objects.filter(partner=partner).select_related('user')
        ctx['domains'] = PartnerDomain.objects.filter(partner=partner)
        ctx['theme'] = PartnerTheme.objects.filter(partner=partner).first()
        ctx['feature_overrides'] = partner.feature_overrides or {}
        return ctx


class PartnerUpdateView(LoginRequiredMixin, RoleRequiredMixin, UpdateView):
    model = Partner
    template_name = 'platform/partner_form.html'
    fields = ['name', 'slug', 'tier', 'status', 'primary_domain', 'primary_color', 'secondary_color',
              'description', 'tagline', 'contact_email', 'max_users', 'max_storage_mb',
              'feature_overrides', 'provider_overrides']
    success_url = reverse_lazy('platform:partner_list')
    allowed_roles = ['SUPERUSER', 'ADMINISTRATOR']


class ProviderListView(LoginRequiredMixin, RoleRequiredMixin, TemplateView):
    template_name = 'platform/provider_list.html'
    allowed_roles = ['SUPERUSER', 'ADMINISTRATOR']

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['providers'] = list_providers()
        return ctx


class FeatureFlagListView(LoginRequiredMixin, RoleRequiredMixin, ListView):
    model = FeatureFlag
    template_name = 'platform/feature_list.html'
    context_object_name = 'flags'
    paginate_by = 50
    allowed_roles = ['SUPERUSER', 'ADMINISTRATOR']


class ThemeListView(LoginRequiredMixin, RoleRequiredMixin, ListView):
    model = PartnerTheme
    template_name = 'platform/theme_list.html'
    context_object_name = 'themes'
    allowed_roles = ['SUPERUSER', 'ADMINISTRATOR']

    def get_queryset(self):
        return PartnerTheme.objects.select_related('partner').all()


class ThemeEditView(LoginRequiredMixin, RoleRequiredMixin, UpdateView):
    model = PartnerTheme
    template_name = 'platform/theme_edit.html'
    fields = ['base_theme', 'primary_color', 'secondary_color', 'accent_color',
              'background_color', 'surface_color', 'text_primary_color', 'text_secondary_color',
              'border_color', 'font_family_heading', 'font_family_body',
              'custom_css', 'logo_url', 'favicon_url']
    success_url = reverse_lazy('platform:theme_list')
    allowed_roles = ['SUPERUSER', 'ADMINISTRATOR']

    def get_object(self, queryset=None):
        from django.shortcuts import get_object_or_404
        partner_pk = self.kwargs.get('partner_pk')
        theme, _ = PartnerTheme.objects.get_or_create(
            partner_id=partner_pk,
            defaults={'base_theme': 'coffee'}
        )
        return theme
