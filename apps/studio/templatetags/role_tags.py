from django import template
from django.contrib.auth import get_user_model

register = template.Library()
User = get_user_model()


@register.simple_tag(takes_context=True)
def has_role(context, *roles):
    """Check if the current user has one of the specified roles.

    Usage:
        {% has_role 'SUPERUSER' 'ADMINISTRATOR' as is_admin %}
        {% if is_admin %}...{% endif %}
    """
    request = context.get('request')
    if not request or not hasattr(request, 'user'):
        return False
    user = request.user
    if not user.is_authenticated:
        return False
    if hasattr(user, 'role'):
        return user.role in roles
    return False


@register.simple_tag(takes_context=True)
def is_superadmin(context):
    """Check if the current user is a SUPERUSER or ADMINISTRATOR."""
    request = context.get('request')
    if not request or not hasattr(request, 'user'):
        return False
    user = request.user
    if not user.is_authenticated:
        return False
    return hasattr(user, 'role') and user.role in ('SUPERUSER', 'ADMINISTRATOR')


@register.simple_tag(takes_context=True)
def get_current_partner(context):
    """Get the current partner from request context."""
    request = context.get('request')
    if not request:
        return None
    ctx = getattr(request, 'partner_context', None)
    if ctx and ctx.partner:
        return ctx.partner
    return None
