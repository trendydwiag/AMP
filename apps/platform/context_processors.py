from django.http import HttpRequest
from typing import Dict, Any


def partner_context(request: HttpRequest) -> Dict[str, Any]:
    """Context processor that adds partner information to all templates.

    Available in templates as:
        {{ partner_context.partner }}
        {{ partner_context.partner_name }}
        {{ partner_context.tier }}
        {{ partner_context.is_default }}
        {{ partner_name }}
        {{ partner_primary_color }}
        {{ partner_logo_url }}
    """
    ctx = getattr(request, 'partner_context', None)

    if ctx and ctx.partner:
        branding = ctx.config.get('branding', {}) if ctx.config else {}
        return {
            'partner_context': ctx,
            'current_partner': ctx.partner,
            'partner_name': ctx.partner_name,
            'partner_tier': ctx.tier,
            'partner_primary_color': branding.get('primary_color', ctx.partner.primary_color),
            'partner_secondary_color': branding.get('secondary_color', ctx.partner.secondary_color),
            'partner_accent_color': branding.get('accent_color', ctx.partner.accent_color),
            'partner_logo_url': branding.get('logo_url', ''),
            'partner_tagline': branding.get('tagline', ctx.partner.tagline),
            'partner_features': ctx.config.get('features', {}) if ctx.config else {},
        }

    return {
        'partner_context': None,
        'current_partner': None,
        'partner_name': '',
        'partner_tier': '',
        'partner_primary_color': '',
        'partner_secondary_color': '',
        'partner_accent_color': '',
        'partner_logo_url': '',
        'partner_tagline': '',
        'partner_features': {},
    }


def platform_settings(request: HttpRequest) -> Dict[str, Any]:
    """Context processor for platform-level settings available to all templates."""
    return {
        'platform_name': 'Aradhana Media Platform',
        'platform_version': '1.0.0',
    }
