# 0008. Use HTMX for Dynamic Content

**Status:** Accepted
**Date:** 2024-07-01

## Context

Modern web applications require dynamic content updates without full page reloads:

- Live radio player with now-playing updates
- AJAX form submissions with partial page updates
- Infinite scroll or load-more patterns
- Real-time search results

Building this with vanilla JavaScript or a SPA framework adds significant frontend complexity that conflicts with the Django-template rendering model.

## Decision

We use **HTMX** to enable dynamic content via HTML attributes, keeping the UI logic server-driven.

HTMX extends HTML with attributes like `hx-get`, `hx-post`, `hx-trigger`, `hx-target`, and `hx-swap`:

```html
<!-- Live now-playing update -->
<div hx-get="/radio/api/now-playing/"
     hx-trigger="every 15s"
     hx-target="#now-playing"
     hx-swap="innerHTML">
  <div id="now-playing">Loading...</div>
</div>

<!-- AJAX form submission -->
<form hx-post="/broadcast/program/"
      hx-target="#form-container"
      hx-swap="outerHTML">
  {% csrf_token %}
  {{ form.as_p }}
  <button type="submit">Save</button>
</form>

<!-- Load more button -->
<div hx-get="/articles/?page=2"
     hx-trigger="click"
     hx-target="#article-list"
     hx-swap="beforeend">
  Load More
</div>
```

## Consequences

**Positive:**

- No JavaScript framework required — pure HTML attributes.
- Server renders HTML fragments, keeping Django's template system as the single source of truth.
- Progressive enhancement: pages work without JavaScript, HTMX adds dynamism.
- Pairs with Alpine.js — Alpine handles client state, HTMX handles server communication.
- Django views return `HttpResponse` fragments or full pages with minimal adaptation.

**Negative:**

- Learning curve for the HTMX attribute model.
- Debugging network requests requires browser dev tools.
- Complex client-side state is not HTMX's strength (use Alpine.js instead).
- HTMX adds ~14KB gzipped to the page.

**Mitigations:**

- HTMX patterns are simple and documentable.
- Django's `{% include %}` and `{% block %}` work naturally for fragment rendering.
- Alpine.js handles the few cases needing client-side state.
