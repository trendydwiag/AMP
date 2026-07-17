import logging
from typing import Optional
from django.core.cache import cache
from .models import PartnerTheme, ThemePreset

logger = logging.getLogger('platform')

CACHE_TTL = 600  # 10 minutes
CACHE_PREFIX = 'partner_theme:'


class ThemeService:
    """Service for managing partner themes."""

    def get_theme(self, partner) -> Optional[PartnerTheme]:
        """Get theme for a partner, using cache."""
        if not partner:
            return None

        cache_key = f"{CACHE_PREFIX}{partner.pk}"
        cached = cache.get(cache_key)
        if cached:
            return cached

        try:
            theme = PartnerTheme.objects.get(partner=partner)
            cache.set(cache_key, theme, CACHE_TTL)
            return theme
        except PartnerTheme.DoesNotExist:
            return None

    def get_or_create_theme(self, partner) -> PartnerTheme:
        """Get or create theme for a partner."""
        theme, created = PartnerTheme.objects.get_or_create(
            partner=partner,
            defaults={
                'primary_color': partner.primary_color or '#4E2F1F',
                'secondary_color': partner.secondary_color or '#FAF7F3',
            }
        )
        return theme

    def update_theme(self, partner, **kwargs) -> Optional[PartnerTheme]:
        """Update partner theme fields."""
        theme = self.get_or_create_theme(partner)
        for key, value in kwargs.items():
            if hasattr(theme, key):
                setattr(theme, key, value)
        theme.save()
        cache.delete(f"{CACHE_PREFIX}{partner.pk}")
        return theme

    def generate_css(self, partner) -> str:
        """Generate full CSS for a partner's theme."""
        theme = self.get_theme(partner)
        if not theme:
            return ''

        css = f':root[data-theme="{partner.slug}"] {{\n'
        css += theme.to_css_variables()
        css += '\n}\n'

        if theme.custom_css:
            css += f'\n/* Custom CSS for {partner.name} */\n'
            css += theme.custom_css

        return css

    def get_presets(self):
        """Get all active theme presets."""
        return ThemePreset.objects.filter(is_active=True)

    def apply_preset(self, partner, preset_slug: str) -> Optional[PartnerTheme]:
        """Apply a preset theme to a partner."""
        try:
            preset = ThemePreset.objects.get(slug=preset_slug, is_active=True)
            theme = preset.apply_to_partner(partner)
            cache.delete(f"{CACHE_PREFIX}{partner.pk}")
            return theme
        except ThemePreset.DoesNotExist:
            logger.warning(f"Preset '{preset_slug}' not found")
            return None

    def clear_cache(self, partner=None):
        """Clear theme cache."""
        if partner:
            cache.delete(f"{CACHE_PREFIX}{partner.pk}")
        else:
            cache.delete_pattern(f"{CACHE_PREFIX}*")
