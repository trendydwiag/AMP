from functools import wraps
from typing import Callable, Optional
from django.http import HttpRequest


def require_partner(fn: Callable = None, *, active_only: bool = True):
    """Decorator for views that require an active partner context.

    Usage:
        @require_partner
        def my_view(request):
            partner = request.partner_context.partner
            ...

        @require_partner(active_only=False)
        def my_view(request):
            partner = request.partner_context.partner
            ...
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped(request: HttpRequest, *args, **kwargs):
            ctx = getattr(request, 'partner_context', None)
            if ctx is None or ctx.partner is None:
                from django.http import JsonResponse
                return JsonResponse(
                    {'error': 'Partner tidak ditemukan.'},
                    status=404
                )
            if active_only and not ctx.is_active:
                from django.http import JsonResponse
                return JsonResponse(
                    {'error': 'Partner tidak aktif.'},
                    status=403
                )
            return view_func(request, *args, **kwargs)
        return _wrapped

    if fn is not None:
        return decorator(fn)
    return decorator


def get_partner_from_request(request: HttpRequest):
    """Shortcut to extract partner from request."""
    ctx = getattr(request, 'partner_context', None)
    if ctx:
        return ctx.partner
    return None


def get_partner_id_from_request(request: HttpRequest) -> Optional[str]:
    """Shortcut to extract partner ID as string from request."""
    partner = get_partner_from_request(request)
    return str(partner.pk) if partner else None


def partner_required_json(view_func):
    """Decorator that returns JSON error responses for missing partner."""
    @wraps(view_func)
    def _wrapped(request: HttpRequest, *args, **kwargs):
        ctx = getattr(request, 'partner_context', None)
        if ctx is None or ctx.partner is None:
            from django.http import JsonResponse
            return JsonResponse(
                {'error': 'Partner tidak ditemukan.'},
                status=404
            )
        if not ctx.is_active:
            from django.http import JsonResponse
            return JsonResponse(
                {'error': 'Partner tidak aktif.'},
                status=403
            )
        return view_func(request, *args, **kwargs)
    return _wrapped
