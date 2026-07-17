---
name: Sprint 4.1 Findings
description: Audit results and patterns from the Sprint 4.1 demo-readiness polish pass.
---

# Sprint 4.1 — Demo Readiness Findings

## "Coming Soon" Pattern
Both `community.html` and `iklan.html` had "Segera Hadir" badges + Coming Soon banners. Fix: remove badge entirely, replace banner with "Fitur yang Sedang Dikembangkan" grid card (4 items, no Coming Soon language). This is the approved pattern for features-in-development.

## Old Card Style (media_manager)
`media_manager/` child templates used `bg-white dark:bg-coffee-800 shadow rounded-lg` — the pre-AMP-Studio card style. Sprint 4.1 upgraded all 7 child templates to `amp-card`.

## Platform Templates
`platform/dashboard.html`, `partner_list.html`, `provider_list.html` were missing:
- `{% block breadcrumb %}` overrides
- Dark mode classes on text/border elements
All three were fully rewritten.

## Empty State Standard
Approved pattern (icon + title + description + CTA button):
```html
<div class="w-12 h-12 rounded-full bg-coffee-100 dark:bg-coffee-700 flex items-center justify-center mx-auto mb-3">
  <svg .../>
</div>
<p class="text-sm font-medium ...">Belum ada X</p>
<p class="text-xs text-coffee-400 ...">Deskripsi singkat.</p>
<a href="{% url '...' %}" class="inline-flex items-center gap-2 mt-4 px-4 py-2 bg-coffee-600 text-white text-sm rounded-xl hover:bg-coffee-700 transition-colors">
  <svg ... plus icon/>
  Tambah X Pertama
</a>
```

## Known Tech Debt (skipped in 4.1)
- `core/home.html` + `dashboard/home.html` still extend `dashboard_base.html` (separate migration needed)
- `settings/` templates use their own `settings/base.html` — intentional architecture
- `platform/partner_detail.html`, `partner_form.html`, `theme_edit.html`, `feature_list.html` — not fully audited

**Why:** Sprint 4.1 rules: no schema/logic changes, UI polish only. Above items risk wider breakage.
