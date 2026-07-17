import logging
from typing import Optional
from django.http import HttpRequest
from django.conf import settings
from .models import Partner, PartnerDomain

logger = logging.getLogger('platform')


class PartnerResolver:
    """Resolves the active partner from an HTTP request.

    Resolution order:
    1. Domain matching (primary_domain or custom_domains)
    2. Subdomain matching
    3. HTTP header (X-Partner-ID or X-Partner-Slug)
    4. Session-based (stored partner_id in session)
    5. Default partner (first active partner or fallback)
    """

    HEADER_PARTNER_ID = 'HTTP_X_PARTNER_ID'
    HEADER_PARTNER_SLUG = 'HTTP_X_PARTNER_SLUG'
    SESSION_KEY = '_current_partner_id'

    def resolve(self, request: HttpRequest) -> Optional[Partner]:
        """Attempt to resolve partner from request. Returns Partner or None."""
        partner = None
        method = ''

        # 1. Domain matching
        partner, method = self._resolve_by_domain(request)
        if partner:
            return partner

        # 2. Subdomain matching
        partner, method = self._resolve_by_subdomain(request)
        if partner:
            return partner

        # 3. Header matching
        partner, method = self._resolve_by_header(request)
        if partner:
            return partner

        # 4. Session matching
        partner, method = self._resolve_by_session(request)
        if partner:
            return partner

        # 5. Default partner
        partner = self._get_default_partner()
        if partner:
            logger.debug(f"Resolved default partner: {partner.name}")
            return partner

        return None

    def _resolve_by_domain(self, request: HttpRequest) -> tuple[Optional[Partner], str]:
        host = request.get_host().split(':')[0].lower()

        # Check primary_domain
        try:
            partner = Partner.objects.filter(
                status='ACTIVE',
                primary_domain=host,
                is_deleted=False,
            ).first()
            if partner:
                return partner, 'domain_primary'
        except Exception:
            pass

        # Check PartnerDomain table
        try:
            pd = PartnerDomain.objects.select_related('partner').filter(
                domain=host,
                is_verified=True,
                partner__status='ACTIVE',
                partner__is_deleted=False,
            ).first()
            if pd:
                return pd.partner, 'domain_custom'
        except Exception:
            pass

        return None, ''

    def _resolve_by_subdomain(self, request: HttpRequest) -> tuple[Optional[Partner], str]:
        host = request.get_host().split(':')[0].lower()
        base_domain = getattr(settings, 'PLATFORM_BASE_DOMAIN', '')

        if base_domain and host.endswith(f'.{base_domain}'):
            subdomain = host.replace(f'.{base_domain}', '')
            if subdomain:
                try:
                    partner = Partner.objects.filter(
                        slug=subdomain,
                        status='ACTIVE',
                        is_deleted=False,
                    ).first()
                    if partner:
                        return partner, 'subdomain'
                except Exception:
                    pass

        return None, ''

    def _resolve_by_header(self, request: HttpRequest) -> tuple[Optional[Partner], str]:
        partner_id = request.META.get(self.HEADER_PARTNER_ID)
        if partner_id:
            try:
                partner = Partner.objects.filter(pk=partner_id, status='ACTIVE', is_deleted=False).first()
                if partner:
                    return partner, 'header_id'
            except Exception:
                pass

        partner_slug = request.META.get(self.HEADER_PARTNER_SLUG)
        if partner_slug:
            try:
                partner = Partner.objects.filter(slug=partner_slug, status='ACTIVE', is_deleted=False).first()
                if partner:
                    return partner, 'header_slug'
            except Exception:
                pass

        return None, ''

    def _resolve_by_session(self, request: HttpRequest) -> tuple[Optional[Partner], str]:
        if not hasattr(request, 'session'):
            return None, ''

        partner_id = request.session.get(self.SESSION_KEY)
        if partner_id:
            try:
                partner = Partner.objects.filter(pk=partner_id, status='ACTIVE', is_deleted=False).first()
                if partner:
                    return partner, 'session'
            except Exception:
                pass

        return None, ''

    def _get_default_partner(self) -> Optional[Partner]:
        try:
            default_slug = getattr(settings, 'PLATFORM_DEFAULT_PARTNER_SLUG', '')
            if default_slug:
                partner = Partner.objects.filter(
                    slug=default_slug, status='ACTIVE', is_deleted=False
                ).first()
                if partner:
                    return partner
            return Partner.objects.filter(status='ACTIVE', is_deleted=False).order_by('created_at').first()
        except Exception:
            return None

    def resolve_from_domain(self, domain: str) -> Optional[Partner]:
        """Resolve partner from a raw domain string (non-request context)."""
        try:
            partner = Partner.objects.filter(
                status='ACTIVE',
                primary_domain=domain,
                is_deleted=False,
            ).first()
            if partner:
                return partner

            pd = PartnerDomain.objects.select_related('partner').filter(
                domain=domain,
                is_verified=True,
                partner__status='ACTIVE',
                partner__is_deleted=False,
            ).first()
            if pd:
                return pd.partner
        except Exception:
            pass
        return None

    def resolve_from_slug(self, slug: str) -> Optional[Partner]:
        """Resolve partner from slug string."""
        try:
            return Partner.objects.filter(slug=slug, status='ACTIVE', is_deleted=False).first()
        except Exception:
            return None
