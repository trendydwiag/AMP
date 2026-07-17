from django.conf import settings
from django.http import HttpRequest
import datetime

def global_settings(request: HttpRequest) -> dict:
    """Exposes global site parameters and config values to the global template context."""
    return {
        'SITE_NAME': 'Kabulhaden CMS',
        'SITE_DESCRIPTION': 'Content Management System production-grade modern.',
        'CURRENT_YEAR': datetime.datetime.now().year,
        'IS_DEBUG': settings.DEBUG,
    }
