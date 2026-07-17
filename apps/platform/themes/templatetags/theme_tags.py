from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def partner_css_variables(context):
    """Render CSS custom properties for the current partner's theme.

    Usage:
        {% partner_css_variables %}
    """
    from .service import ThemeService
    request = context.get('request')
    partner_ctx = getattr(request, 'partner_context', None)

    if not partner_ctx or not partner_ctx.partner:
        return ''

    svc = ThemeService()
    css = svc.generate_css(partner_ctx.partner)
    return css


@register.simple_tag(takes_context=True)
def partner_theme_class(context):
    """Output the data-theme attribute for the current partner.

    Usage:
        <div {% partner_theme_class %}>
    """
    request = context.get('request')
    partner_ctx = getattr(request, 'partner_context', None)

    if partner_ctx and partner_ctx.partner:
        return f'data-theme="{partner_ctx.partner.slug}"'
    return 'data-theme="default"'


@register.simple_tag(takes_context=True)
def partner_logo(context):
    """Get partner logo URL or fallback to default.

    Usage:
        {% partner_logo as logo %}
        <img src="{{ logo }}" />
    """
    request = context.get('request')
    partner_ctx = getattr(request, 'partner_context', None)

    if partner_ctx and partner_ctx.partner:
        theme = getattr(partner_ctx.partner, 'theme', None)
        if theme and theme.logo_url:
            return theme.logo_url
        if partner_ctx.partner.logo:
            return partner_ctx.partner.logo.url

    return '/static/images/default-logo.png'
