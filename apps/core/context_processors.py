from django.conf import settings
from django.http import HttpRequest
import datetime


def global_settings(request: HttpRequest) -> dict:
    """Exposes global site parameters and config values to the global template context."""
    try:
        from apps.settings.models import SiteSettings
        site = SiteSettings.load()
        site_name        = site.site_name or 'Kabulhaden CMS'
        site_description = site.site_description or 'Platform multi-media siar digital berbasis teknologi internet.'
        site_logo_url    = site.site_logo.url    if site.site_logo    else ''
        site_favicon_url = site.site_favicon.url if site.site_favicon else ''
        maintenance_mode    = site.maintenance_mode
        maintenance_message = site.maintenance_message
    except Exception:
        site_name           = 'Kabulhaden CMS'
        site_description    = 'Platform multi-media siar digital.'
        site_logo_url       = ''
        site_favicon_url    = ''
        maintenance_mode    = False
        maintenance_message = ''

    return {
        'SITE_NAME':            site_name,
        'SITE_DESCRIPTION':     site_description,
        'SITE_LOGO_URL':        site_logo_url,
        'SITE_FAVICON_URL':     site_favicon_url,
        'MAINTENANCE_MODE':     maintenance_mode,
        'MAINTENANCE_MESSAGE':  maintenance_message,
        'CURRENT_YEAR':         datetime.datetime.now().year,
        'IS_DEBUG':             settings.DEBUG,
    }
