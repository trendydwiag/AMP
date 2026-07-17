---
name: AMP Studio Architecture
description: Design tokens, CSS class conventions, Alpine.js patterns, and component structure for AMP Studio templates.
---

## CSS
- All custom CSS in `static/css/amp-studio/`: `amp-studio.css` → imports `design-tokens.css`, `components.css`, `layout.css`
- Design tokens use `--amp-*` CSS variables (coffee palette: `--amp-coffee-50` to `--amp-coffee-900`)
- Component classes: `amp-card`, `amp-card-elevated`, `amp-btn`, `amp-btn-primary`, `amp-btn-secondary`, `amp-btn-ghost`, `amp-btn-icon`, `amp-badge`, `amp-nav-item`, `amp-empty`, `amp-empty-icon`, `amp-empty-title`, `amp-empty-description`, `amp-metric-value`, `amp-metric-label`, `amp-page-title`, `amp-page-subtitle`, `amp-separator`, `amp-dropdown`, `amp-dropdown-item`, `amp-avatar`, `amp-status-dot`
- No inline `style=` for brand colors — use CSS variables

## Base Template (`amp_studio/base.html`)
- Extends nothing; includes sidebar, header, player_bar, command_palette, notifications
- Alpine.js loaded via CDN: `https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js`
- Main JS: `static/js/amp-studio/amp-studio.js` (defines `ampStudio()`, `streamStatus()`, etc.)
- Body: `x-data="ampStudio()" x-init="init()"`
- Toast container: `#toast-container` at `z-[1100]`
- Z-index scale: base=0, dropdown=1000, sidebar=1030, header=1040, player=1050, modal-backdrop=1060, modal=1070, command-palette=1080, notification=1090, toast=1100

## Alpine.js Conventions
- Global app state in `ampStudio()` function in `amp-studio.js`
- `streamStatus()` component available globally for stream status polling (polls `/radio/api/status/`)
- `partnerSwitcher()` in sidebar for partner switching
- Guided tour: `guidedTour()` data defined in `guided_tour.html` inline script
- Setup wizard: `setupWizard(initialStep)` data defined in `setup_wizard.html` inline script
- Streaming center: `streamingCenter()` data defined in `streaming_center.html` inline script

## Views Pattern
- All views `@method_decorator(login_required, name='dispatch')` + `TemplateView`
- All radio/sponsor/news service calls wrapped in try/except (resilient to missing data)
- Context: `SITE_NAME`, `SITE_LOGO` added in `AMPStudioDashboardView.get_context_data()`

## Known Issues
- Alpine.js blocked by browser CSP (SRI hash mismatch for `@3.x.x` → resolves to 3.14.0)
- `sponsor` app has no CMS URL namespace (no `app_name` in urls.py)
