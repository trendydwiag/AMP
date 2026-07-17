from dataclasses import dataclass, field
from typing import Optional, Dict, Any
from .models import Partner


@dataclass
class PartnerContext:
    """Thread-local context holding the current partner for a request.

    Access via `request.partner_context` after PartnerMiddleware runs.
    """

    partner: Optional[Partner] = None
    resolution_method: str = ''
    resolved_domain: str = ''
    is_default: bool = True
    config: Dict[str, Any] = field(default_factory=dict)

    @property
    def partner_id(self) -> Optional[str]:
        return str(self.partner.pk) if self.partner else None

    @property
    def partner_name(self) -> str:
        return self.partner.name if self.partner else ''

    @property
    def is_active(self) -> bool:
        return self.partner.is_active if self.partner else False

    @property
    def tier(self) -> str:
        return self.partner.tier if self.partner else ''

    def has_feature(self, feature_key: str, default: bool = False) -> bool:
        if self.partner:
            return self.partner.has_feature(feature_key, default)
        return default

    def get_provider(self, category: str) -> Optional[str]:
        if self.partner:
            return self.partner.get_provider(category)
        return None

    def get_config_value(self, key: str, default=None):
        """Get a value from the loaded partner config."""
        return self.config.get(key, default)

    def get_branding(self, key: str, default=None):
        """Get a branding value from the loaded partner config."""
        branding = self.config.get('branding', {})
        return branding.get(key, default)

    def to_dict(self) -> dict:
        return {
            'partner_id': self.partner_id,
            'partner_name': self.partner_name,
            'resolution_method': self.resolution_method,
            'resolved_domain': self.resolved_domain,
            'is_default': self.is_default,
            'tier': self.tier,
        }


def get_partner_from_context(request) -> Optional[Partner]:
    """Extract partner from request's PartnerContext."""
    ctx = getattr(request, 'partner_context', None)
    if ctx and isinstance(ctx, PartnerContext):
        return ctx.partner
    return None
