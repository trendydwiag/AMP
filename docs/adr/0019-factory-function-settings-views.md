# 0019. Use _settings_view Factory for Settings Views

**Status:** Accepted
**Date:** 2024-07-15

## Context

The CMS has 10 settings models, each requiring a settings view that:

- Displays a form with the current singleton settings
- Handles form submission and validation
- Shows success messages on save
- Requires admin authentication
- Shares the same sidebar navigation

Without DRY abstraction, each settings view would repeat 20-30 lines of identical boilerplate, totaling 200-300 lines of duplicated view code.

## Decision

We use a **factory function** `_settings_view()` in `apps/settings/views.py` that generates settings views from configuration:

```python
def _settings_view(form_class, service_class, model_class, tpl, title):
    """Factory function to create settings views."""
    @method_decorator(login_required, name='dispatch')
    @method_decorator(admin_required, name='dispatch')
    class View(TemplateView):
        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['title'] = title
            context['form'] = form_class(instance=model_class.load())
            context['settings_groups'] = SettingsBaseView().get_context_data()['settings_groups']
            return context

        def post(self, request, *args, **kwargs):
            instance = model_class.load()
            form = form_class(request.POST, request.FILES, instance=instance)
            if form.is_valid():
                form.save()
                messages.success(request, f'{title} berhasil diperbarui.')
                return redirect(request.path)
            context = self.get_context_data(**kwargs)
            context['form'] = form
            return self.render_to_response(context)

    View.template_name = tpl
    View.__name__ = f'{title.replace(" ", "")}View'
    return View
```

Usage — one line per settings view:

```python
SiteSettingsView = _settings_view(
    SiteSettingsForm, SiteSettingsService, SiteSettings,
    'settings/site.html', 'Pengaturan Situs'
)
SEOSettingsView = _settings_view(
    SEOSettingsForm, SEOSettingsService, SEOSettings,
    'settings/seo.html', 'Pengaturan SEO'
)
# ... 8 more settings views
```

## Consequences

**Positive:**

- 10 settings views are defined in 10 lines instead of 300+ lines.
- All settings views share identical GET/POST behavior and authentication.
- Adding a new settings view requires only one `_settings_view()` call.
- Consistent `messages.success()` feedback across all settings pages.
- `settings_groups` sidebar navigation is generated once and shared.

**Negative:**

- Factory-generated classes have dynamic `__name__`, which can confuse debuggers and stack traces.
- The pattern is non-standard Django — new developers must understand the factory.
- Custom per-view behavior (e.g., file upload handling) requires extending the factory or adding special cases.

**Mitigations:**

- `View.__name__` is set to a descriptive name (`PengaturanSitusView`) for stack trace readability.
- The factory is documented with a clear docstring and usage examples.
- File upload is handled generically via `request.FILES` in the POST handler.
- If a settings view needs custom logic, it can be defined as a standalone CBV without the factory.
