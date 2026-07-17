import json
from django.db import models
from utils.mixins import UUIDPrimaryKeyMixin, TimeStampedModel
from apps.platform.choices import ThemeMode


class PartnerTheme(UUIDPrimaryKeyMixin, TimeStampedModel):
    """Per-partner theme configuration.

    Stores CSS variable overrides and theme settings that are applied
    on top of the base theme (light/dark/coffee).
    """

    partner = models.OneToOneField(
        'platform.Partner',
        on_delete=models.CASCADE,
        related_name='theme'
    )
    base_theme = models.CharField(
        max_length=20,
        choices=ThemeMode.choices,
        default=ThemeMode.COFFEE,
        help_text="Base theme to extend."
    )
    custom_css = models.TextField(
        blank=True,
        default='',
        help_text="Custom CSS (applied after design tokens)."
    )

    # Color overrides (CSS variables)
    primary_color = models.CharField(max_length=7, default='#4E2F1F')
    secondary_color = models.CharField(max_length=7, default='#FAF7F3')
    accent_color = models.CharField(max_length=7, default='#8B6914')
    background_color = models.CharField(max_length=7, default='#FAF7F3')
    surface_color = models.CharField(max_length=7, default='#FFFFFF')
    text_primary_color = models.CharField(max_length=7, default='#1A0F0B')
    text_secondary_color = models.CharField(max_length=7, default='#6B5B4F')
    border_color = models.CharField(max_length=7, default='#E5DDD5')
    error_color = models.CharField(max_length=7, default='#DC2626')
    success_color = models.CharField(max_length=7, default='#16A34A')
    warning_color = models.CharField(max_length=7, default='#F59E0B')
    info_color = models.CharField(max_length=7, default='#3B82F6')

    # Typography overrides
    font_family_heading = models.CharField(max_length=100, default='Poppins')
    font_family_body = models.CharField(max_length=100, default='Inter')
    font_size_base = models.CharField(max_length=10, default='16px')
    line_height_base = models.CharField(max_length=10, default='1.6')

    # Border radius overrides
    radius_sm = models.CharField(max_length=10, default='6px')
    radius_md = models.CharField(max_length=10, default='8px')
    radius_lg = models.CharField(max_length=10, default='12px')
    radius_xl = models.CharField(max_length=10, default='16px')

    # Logo overrides
    logo_url = models.URLField(max_length=500, blank=True, default='')
    favicon_url = models.URLField(max_length=500, blank=True, default='')

    # Spacing overrides
    sidebar_width = models.CharField(max_length=10, default='260px')
    sidebar_collapsed_width = models.CharField(max_length=10, default='72px')
    header_height = models.CharField(max_length=10, default='64px')

    class Meta:
        verbose_name = 'Tema Partner'
        verbose_name_plural = 'Tema Partner'

    def __str__(self) -> str:
        return f"Tema: {self.partner.name} ({self.get_base_theme_display()})"

    def to_css_variables(self) -> str:
        """Generate CSS custom properties from theme configuration."""
        vars_dict = {
            '--color-primary': self.primary_color,
            '--color-secondary': self.secondary_color,
            '--color-accent': self.accent_color,
            '--color-background': self.background_color,
            '--color-surface': self.surface_color,
            '--color-text-primary': self.text_primary_color,
            '--color-text-secondary': self.text_secondary_color,
            '--color-border': self.border_color,
            '--color-error': self.error_color,
            '--color-success': self.success_color,
            '--color-warning': self.warning_color,
            '--color-info': self.info_color,
            '--font-family-heading': self.font_family_heading,
            '--font-family-body': self.font_family_body,
            '--font-size-base': self.font_size_base,
            '--line-height-base': self.line_height_base,
            '--radius-sm': self.radius_sm,
            '--radius-md': self.radius_md,
            '--radius-lg': self.radius_lg,
            '--radius-xl': self.radius_xl,
            '--sidebar-width': self.sidebar_width,
            '--sidebar-collapsed-width': self.sidebar_collapsed_width,
            '--header-height': self.header_height,
        }
        return '\n'.join(f"  {k}: {v};" for k, v in vars_dict.items())

    def to_dict(self) -> dict:
        """Export theme as dictionary."""
        return {
            'base_theme': self.base_theme,
            'colors': {
                'primary': self.primary_color,
                'secondary': self.secondary_color,
                'accent': self.accent_color,
                'background': self.background_color,
                'surface': self.surface_color,
                'text_primary': self.text_primary_color,
                'text_secondary': self.text_secondary_color,
                'border': self.border_color,
                'error': self.error_color,
                'success': self.success_color,
                'warning': self.warning_color,
                'info': self.info_color,
            },
            'typography': {
                'font_family_heading': self.font_family_heading,
                'font_family_body': self.font_family_body,
                'font_size_base': self.font_size_base,
                'line_height_base': self.line_height_base,
            },
            'radius': {
                'sm': self.radius_sm,
                'md': self.radius_md,
                'lg': self.radius_lg,
                'xl': self.radius_xl,
            },
            'layout': {
                'sidebar_width': self.sidebar_width,
                'sidebar_collapsed_width': self.sidebar_collapsed_width,
                'header_height': self.header_height,
            },
            'custom_css': self.custom_css,
            'logo_url': self.logo_url,
            'favicon_url': self.favicon_url,
        }


class ThemePreset(UUIDPrimaryKeyMixin, TimeStampedModel):
    """Pre-defined theme presets that partners can start from."""

    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True, default='')
    is_active = models.BooleanField(default=True)
    config = models.JSONField(
        default=dict,
        help_text="Theme configuration JSON matching PartnerTheme structure."
    )

    class Meta:
        verbose_name = 'Preset Tema'
        verbose_name_plural = 'Preset Tema'
        ordering = ['name']

    def __str__(self) -> str:
        return self.name

    def apply_to_partner(self, partner):
        """Apply this preset to a partner's theme."""
        from .models import PartnerTheme
        theme, created = PartnerTheme.objects.get_or_create(partner=partner)

        config = self.config
        for field_name, value in config.items():
            if hasattr(theme, field_name):
                setattr(theme, field_name, value)

        theme.save()
        return theme
