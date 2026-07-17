import logging
from functools import wraps
from django.http import HttpRequest, JsonResponse, HttpResponseForbidden
from django.contrib.contenttypes.models import ContentType
from apps.platform.partner.context import get_partner_from_context

logger = logging.getLogger('platform')


class TenantIsolation:
    """Enforces tenant isolation across all queries.

    Provides querysets scoped to the current partner, and decorators
    to enforce partner ownership on views.
    """

    @staticmethod
    def get_partner_queryset(model, partner):
        """Return a queryset filtered to the given partner.

        Works for any model that has a `partner` FK field.
        """
        if not partner:
            return model.objects.none()
        return model.objects.filter(partner=partner)

    @staticmethod
    def get_current_partner_queryset(model, request):
        """Return a queryset filtered to the current request's partner."""
        from apps.platform.partner.context import get_partner_from_context
        partner = get_partner_from_context(request)
        return TenantIsolation.get_partner_queryset(model, partner)

    @staticmethod
    def check_object_access(obj, request) -> bool:
        """Check if the current user can access an object based on partner membership.

        Returns True if the user has access.
        """
        user = request.user
        if not user.is_authenticated:
            return False

        # Superuser can access everything
        if hasattr(user, 'role') and user.role == 'SUPERUSER':
            return True

        # Get the object's partner
        obj_partner = getattr(obj, 'partner', None)
        if obj_partner is None:
            return True  # No partner FK = global object

        # Get current request partner
        current_partner = get_partner_from_context(request)

        if current_partner is None:
            return False

        # Same partner = access allowed
        return str(obj_partner.pk) == str(current_partner.pk)

    @staticmethod
    def ensure_partner_ownership(obj, request):
        """Raise PermissionDenied if the user doesn't own this object's partner."""
        if not TenantIsolation.check_object_access(obj, request):
            logger.warning(
                f"Cross-partner access denied: user={request.user.username}, "
                f"object_partner={getattr(obj, 'partner', None)}"
            )
            raise PermissionDenied("Akses ditolak: objek bukan milik partner Anda.")


class AuditLogger:
    """Logs security-relevant actions for partner data."""

    @staticmethod
    def log_action(action: str, user, partner=None, object_repr: str = '', details: dict = None):
        """Log a security action."""
        from apps.platform.feature_flags.models import FeatureFlagLog
        from apps.platform.feature_flags.models import FeatureFlag

        # Find or create an audit flag for this action type
        flag, _ = FeatureFlag.objects.get_or_create(
            key=f'audit_{action}',
            defaults={
                'name': f'Audit: {action}',
                'description': f'Audit log for {action} actions',
                'is_enabled': True,
                'category': 'audit',
            }
        )

        log_data = {
            'action': action,
            'user': str(user) if user else 'anonymous',
            'partner': str(partner) if partner else 'none',
            'object': object_repr,
        }
        if details:
            log_data.update(details)

        FeatureFlagLog.objects.create(
            flag=flag,
            action=action,
            old_value={},
            new_value=log_data,
            changed_by=user if user and user.is_authenticated else None,
        )

        logger.info(f"AUDIT: {action} by {user} on {partner} - {object_repr}")


class PermissionDenied(Exception):
    """Raised when a user attempts to access a resource they don't own."""
    pass


def require_partner_access(view_func):
    """Decorator that enforces partner access control on views.

    Ensures the current user can only access objects from their partner.
    """
    @wraps(view_func)
    def _wrapped(request: HttpRequest, *args, **kwargs):
        ctx = getattr(request, 'partner_context', None)
        if ctx is None or ctx.partner is None:
            return JsonResponse(
                {'error': 'Partner tidak ditemukan.'},
                status=404
            )
        if not ctx.is_active:
            return JsonResponse(
                {'error': 'Partner tidak aktif.'},
                status=403
            )
        return view_func(request, *args, **kwargs)
    return _wrapped


def require_superuser(view_func):
    """Decorator that requires SUPERUSER role."""
    @wraps(view_func)
    def _wrapped(request: HttpRequest, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            return JsonResponse({'error': 'Login required.'}, status=401)
        if not hasattr(user, 'role') or user.role != 'SUPERUSER':
            return JsonResponse({'error': 'Akses ditolak: Superuser required.'}, status=403)
        return view_func(request, *args, **kwargs)
    return _wrapped
