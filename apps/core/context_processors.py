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
        site_address        = site.address or ''
        site_contact_email  = site.contact_email or ''
        site_contact_phone  = site.contact_phone or ''
    except Exception:
        site_name           = 'Kabulhaden CMS'
        site_description    = 'Platform multi-media siar digital.'
        site_logo_url       = ''
        site_favicon_url    = ''
        maintenance_mode    = False
        maintenance_message = ''
        site_address        = ''
        site_contact_email  = ''
        site_contact_phone  = ''

    try:
        from apps.settings.models import SocialMediaSettings
        social = SocialMediaSettings.load()
        social_facebook   = social.facebook_url or ''
        social_instagram  = social.instagram_url or ''
        social_twitter    = social.twitter_url or ''
        social_youtube    = social.youtube_url or ''
        social_tiktok     = social.tiktok_url or ''
        social_linkedin   = social.linkedin_url or ''
        social_whatsapp   = social.whatsapp_number or ''
        social_telegram   = social.telegram_username or ''
    except Exception:
        social_facebook = social_instagram = social_twitter = social_youtube = ''
        social_tiktok = social_linkedin = social_whatsapp = social_telegram = ''

    return {
        'SITE_NAME':            site_name,
        'SITE_DESCRIPTION':     site_description,
        'SITE_LOGO_URL':        site_logo_url,
        'SITE_FAVICON_URL':     site_favicon_url,
        'MAINTENANCE_MODE':     maintenance_mode,
        'MAINTENANCE_MESSAGE':  maintenance_message,
        'SITE_ADDRESS':         site_address,
        'SITE_CONTACT_EMAIL':   site_contact_email,
        'SITE_CONTACT_PHONE':   site_contact_phone,
        'SOCIAL_FACEBOOK':      social_facebook,
        'SOCIAL_INSTAGRAM':     social_instagram,
        'SOCIAL_TWITTER':       social_twitter,
        'SOCIAL_YOUTUBE':       social_youtube,
        'SOCIAL_TIKTOK':        social_tiktok,
        'SOCIAL_LINKEDIN':      social_linkedin,
        'SOCIAL_WHATSAPP':      social_whatsapp,
        'SOCIAL_TELEGRAM':      social_telegram,
        'CURRENT_YEAR':         datetime.datetime.now().year,
        'IS_DEBUG':             settings.DEBUG,
    }
