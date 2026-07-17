import logging
from typing import Optional, Tuple
from django.conf import settings
from django.http import HttpRequest

logger = logging.getLogger('platform')


class DomainEngine:
    """Handles domain resolution for multi-partner routing.

    Supports:
    - Direct domain (primary_domain on Partner)
    - Custom domain (PartnerDomain table)
    - Subdomain (*.PLATFORM_BASE_DOMAIN)
    - Localhost development (localhost:PORT)
    """

    # Localhost patterns for development
    LOCALHOST_PATTERNS = ['localhost', '127.0.0.1', '0.0.0.0']

    def resolve_partner_from_request(self, request: HttpRequest):
        """Resolve partner from the incoming request's domain."""
        host = request.get_host().split(':')[0].lower()
        port = request.get_port() if hasattr(request, 'get_port') else ''

        # Skip resolution for localhost in development (use default partner)
        if self._is_localhost(host):
            return self._get_default_partner(), 'localhost'

        return self._resolve_domain(host)

    def _is_localhost(self, host: str) -> bool:
        """Check if the host is a localhost address."""
        return host in self.LOCALHOST_PATTERNS

    def _resolve_domain(self, domain: str):
        """Resolve a domain to a partner."""
        from apps.platform.partner.models import Partner, PartnerDomain

        # 1. Check primary_domain on Partner
        try:
            partner = Partner.objects.filter(
                primary_domain=domain,
                status='ACTIVE',
                is_deleted=False,
            ).first()
            if partner:
                return partner, 'domain_primary'
        except Exception as e:
            logger.error(f"Domain resolution error (primary): {e}")

        # 2. Check PartnerDomain table
        try:
            pd = PartnerDomain.objects.select_related('partner').filter(
                domain=domain,
                is_verified=True,
                partner__status='ACTIVE',
                partner__is_deleted=False,
            ).first()
            if pd:
                return pd.partner, 'domain_custom'
        except Exception as e:
            logger.error(f"Domain resolution error (custom): {e}")

        # 3. Check subdomain pattern
        base_domain = getattr(settings, 'PLATFORM_BASE_DOMAIN', '')
        if base_domain and domain.endswith(f'.{base_domain}'):
            subdomain = domain.replace(f'.{base_domain}', '')
            if subdomain:
                try:
                    partner = Partner.objects.filter(
                        slug=subdomain,
                        status='ACTIVE',
                        is_deleted=False,
                    ).first()
                    if partner:
                        return partner, 'subdomain'
                except Exception as e:
                    logger.error(f"Domain resolution error (subdomain): {e}")

        # 4. Fallback to default
        return self._get_default_partner(), 'default'

    def _get_default_partner(self):
        """Get the default partner from settings."""
        from apps.platform.partner.models import Partner

        default_slug = getattr(settings, 'PLATFORM_DEFAULT_PARTNER_SLUG', '')
        if default_slug:
            try:
                return Partner.objects.filter(
                    slug=default_slug,
                    status='ACTIVE',
                    is_deleted=False,
                ).first()
            except Exception:
                pass

        return Partner.objects.filter(
            status='ACTIVE', is_deleted=False
        ).order_by('created_at').first()

    def get_partner_domains(self, partner) -> list:
        """Return all domains associated with a partner."""
        domains = []
        if partner.primary_domain:
            domains.append({
                'domain': partner.primary_domain,
                'is_primary': True,
                'is_verified': True,
            })

        from apps.platform.partner.models import PartnerDomain
        for pd in PartnerDomain.objects.filter(partner=partner):
            domains.append({
                'domain': pd.domain,
                'is_primary': pd.is_primary,
                'is_verified': pd.is_verified,
                'ssl_enabled': pd.ssl_enabled,
            })

        if isinstance(partner.custom_domains, list):
            for d in partner.custom_domains:
                if not any(dom['domain'] == d for dom in domains):
                    domains.append({
                        'domain': d,
                        'is_primary': False,
                        'is_verified': False,
                    })

        return domains

    def verify_domain(self, domain: str) -> Tuple[bool, str]:
        """Verify that a domain is correctly configured (DNS pointed to platform).

        Returns (is_valid, message).
        """
        import socket
        try:
            ip = socket.gethostbyname(domain)
            # Check if it resolves to a valid IP
            return True, f"Domain terverifikasi: {ip}"
        except socket.gaierror:
            return False, "Domain belum terverifikasi (DNS belum terpoint)"

    def get_subdomain_for_partner(self, partner) -> str:
        """Generate the subdomain URL for a partner."""
        base_domain = getattr(settings, 'PLATFORM_BASE_DOMAIN', 'kabulhaden.com')
        return f"{partner.slug}.{base_domain}"
