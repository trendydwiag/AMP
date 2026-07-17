# 0007. Use Alpine.js for Interactivity

**Status:** Accepted
**Date:** 2024-07-01

## Context

Django templates are server-rendered and lack built-in client-side interactivity. Common UI patterns need JavaScript:

- Dropdown menus and modal dialogs
- Form validation feedback
- Tab switching
- Toggle visibility (show/hide elements)
- Countdown timers and live counters

A full JavaScript framework (React, Vue) is overkill for a Django-rendered CMS where most state lives on the server.

## Decision

We use **Alpine.js** (~15KB gzipped) for declarative, inline interactivity directly in HTML templates.

Example patterns:

```html
<!-- Dropdown -->
<div x-data="{ open: false }">
  <button @click="open = !open">Menu</button>
  <div x-show="open" @click.away="open = false">
    <a href="/link">Item</a>
  </div>
</div>

<!-- Modal -->
<div x-data="{ showModal: false }">
  <button @click="showModal = true">Open</button>
  <div x-show="showModal" x-transition>
    <div class="modal-content">...</div>
    <button @click="showModal = false">Close</button>
  </div>
</div>

<!-- Form validation -->
<form x-data="{ valid: false }">
  <input x-model="valid" required>
  <button :disabled="!valid">Submit</button>
</form>
```

Alpine.js is included via CDN or static file, no build step required.

## Consequences

**Positive:**

- Zero build step — just add `<script defer src="alpine.js">` to base template.
- Declarative `x-data`, `x-show`, `x-on` attributes work directly in Django templates.
- No JavaScript framework knowledge required for backend developers.
- Pairs naturally with HTMX (see ADR-0008) — Alpine handles micro-interactions, HTMX handles server communication.
- 15KB gzipped vs. 40KB+ for React/Vue runtime.

**Negative:**

- Complex state management (multi-step forms, optimistic UI) is limited.
- Debugging inline JavaScript in templates is harder than in `.js` files.
- No TypeScript support or type safety.

**Mitigations:**

- Complex interactions are handled server-side via HTMX instead.
- Alpine component patterns are documented in `docs/26_ALPINEJS_PATTERNS.md`.
- Alpine DevTools browser extension provides debugging support.
