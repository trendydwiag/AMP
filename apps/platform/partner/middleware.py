import logging
from django.http import HttpRequest, HttpResponse
from django.conf import settings
from .resolver import PartnerResolver
from .context import PartnerContext

logger = logging.getLogger('platform')


class PartnerMiddleware:
    """Middleware that resolves the active partner from the request and attaches PartnerContext.

    Resolution order:
    1. Domain (primary_domain or PartnerDomain table)
    2. Subdomain
    3. HTTP Header (X-Partner-ID / X-Partner-Slug)
    4. Session (partner switcher)
    5. Default (configured default partner slug)

    After resolution, request.partner_context is set with the resolved partner.
    For admin users, the session can override the domain-resolved partner.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        self.resolver = PartnerResolver()

    def __call__(self, request: HttpRequest) -> HttpResponse:
        ctx = PartnerContext()

        try:
            partner = self._resolve_partner(request)
            if partner:
                ctx.partner = partner
                ctx.is_default = False
                ctx.resolved_domain = request.get_host().split(':')[0]

                # Load partner config for downstream use
                from .service import PartnerService
                service = PartnerService()
                ctx.config = service.load_partner_config(partner)

                logger.debug(f"Partner resolved: {partner.name} ({ctx.resolved_domain})")
        except Exception as e:
            logger.error(f"Partner resolution error: {e}")
            ctx.partner = None
            ctx.is_default = True

        request.partner_context = ctx

        response = self.get_response(request)
        return response

    def _resolve_partner(self, request: HttpRequest):
        """Resolve partner with admin session override support.

        For SUPERUSER/ADMINISTRATOR users, session-based partner takes precedence
        over domain resolution (allows partner switching in AMP Studio).
        """
        user = getattr(request, 'user', None)

        # Check if admin user has a session-switched partner
        if user and user.is_authenticated and hasattr(user, 'role'):
            if user.role in ('SUPERUSER', 'ADMINISTRATOR'):
                session_partner_id = request.session.get(PartnerResolver.SESSION_KEY)
                if session_partner_id:
                    from .models import Partner
                    try:
                        partner = Partner.objects.filter(
                            pk=session_partner_id,
                            status='ACTIVE',
                            is_deleted=False,
                        ).first()
                        if partner:
                            return partner
                    except Exception:
                        pass

        # Standard resolution flow
        return self.resolver.resolve(request)
