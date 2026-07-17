from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag(takes_context=True)
def feature_enabled(context, key, *args, **kwargs):
    """Check if a feature flag is enabled.

    Usage:
        {% feature_enabled 'podcast' %} -> True/False
        {% feature_enabled 'podcast' as enabled %}
            {% if enabled %}...{% endif %}
    """
    from .service import FeatureFlagService
    request = context.get('request')
    partner = getattr(request, 'partner_context', None)
    partner_obj = partner.partner if partner else None

    svc = FeatureFlagService()
    return svc.is_enabled(key, partner_obj)


@register.simple_tag(takes_context=True)
def feature_config(context, key):
    """Get feature configuration dict.

    Usage:
        {% feature_config 'podcast' as config %}
            {{ config.max_episodes }}
    """
    from .service import FeatureFlagService
    request = context.get('request')
    partner = getattr(request, 'partner_context', None)
    partner_obj = partner.partner if partner else None

    svc = FeatureFlagService()
    return svc.get_config(key, partner_obj)


@register.inclusion_tag('platform/tags/feature_gate.html', takes_context=True)
def feature_gate(context, key):
    """Conditionally render content if feature is enabled.

    Usage:
        {% feature_gate 'podcast' %}
            <div>Podcast feature content</div>
        {% endfeature_gate %}
    """
    from .service import FeatureFlagService
    request = context.get('request')
    partner = getattr(request, 'partner_context', None)
    partner_obj = partner.partner if partner else None

    svc = FeatureFlagService()
    return {
        'enabled': svc.is_enabled(key, partner_obj),
        'key': key,
    }
