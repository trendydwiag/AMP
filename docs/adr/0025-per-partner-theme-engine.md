# ADR-0025: Per-Partner Theme Engine

## Status
Accepted

## Date
2026-07-17

## Context
Each partner on the platform needs distinct branding (colors, fonts, logos) while sharing the same base templates and CSS architecture. The existing AMP Studio theme system supports light/dark/coffee modes but is not per-partner.

## Decision
We implement a **Per-Partner Theme Engine** that generates CSS custom properties from partner-specific configurations and applies them via `data-theme` attribute.

### Architecture:
- **PartnerTheme model**: One-to-one with Partner, stores all visual overrides as model fields
- **ThemePreset model**: Pre-defined theme templates partners can start from
- **ThemeService**: Business logic for theme resolution, CSS generation, preset application
- **Template tags**: `{% partner_css_variables %}`, `{% partner_theme_class %}`, `{% partner_logo %}`

### CSS Variable Override:
PartnerTheme generates CSS custom properties that override the base design tokens:
```css
:root[data-theme="kabulhaden-online"] {
  --color-primary: #4E2F1F;
  --color-secondary: #FAF7F3;
  --font-family-heading: Poppins;
  --sidebar-width: 260px;
  /* ... */
}
```

### Resolution Order:
1. Check PartnerTheme for the current partner
2. Fall back to base theme (light/dark/coffee)
3. Apply design token defaults
4. Apply partner-specific CSS variables
5. Apply partner custom CSS (last)

### Available Overrides:
- **Colors**: primary, secondary, accent, background, surface, text, border, error, success, warning, info
- **Typography**: heading font, body font, base size, line height
- **Border Radius**: sm, md, lg, xl
- **Layout**: sidebar width, collapsed width, header height
- **Assets**: logo URL, favicon URL
- **Custom CSS**: Free-form CSS for advanced customization

## Consequences
- Theme CSS is cached per-partner (10-min TTL)
- All templates inherit partner theming via `{% partner_css_variables %}`
- ThemePreset enables quick onboarding with pre-made themes
- Custom CSS field allows unlimited branding flexibility
- Backward compatible: existing templates work unchanged

## References
- `apps/platform/themes/models.py` - PartnerTheme, ThemePreset
- `apps/platform/themes/service.py` - ThemeService
- `apps/platform/themes/templatetags/theme_tags.py` - Template tags
