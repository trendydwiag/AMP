---
name: Platform Template Dark Mode
description: Platform templates (feature_list, partner_form/detail, theme_list/edit) used hardcoded bg-white; correct pattern for amp_studio-extending templates uses CSS vars.
---

## Rule
Any template that `{% extends "amp_studio/base.html" %}` must use AMP Studio CSS variables for backgrounds, borders, and text — NOT Tailwind utility classes with hardcoded colors.

**Why:** The AMP Studio dark mode works by switching CSS variable values when the `.dark` class is toggled on `<html>`. Hardcoded `bg-white` / `text-coffee-800` classes don't adapt — they stay white in dark mode.

## Correct pattern
```html
<!-- backgrounds -->
bg-[var(--amp-surface-primary)]       ← replaces bg-white
bg-[var(--amp-surface-secondary)]     ← replaces bg-coffee-50 / bg-slate-50

<!-- text -->
text-[var(--amp-text-primary)]        ← replaces text-coffee-800 / text-slate-900
text-[var(--amp-text-secondary)]      ← replaces text-coffee-600 / text-slate-600
text-[var(--amp-text-tertiary)]       ← replaces text-coffee-500 / text-slate-400

<!-- borders -->
border-[var(--amp-border-default)]    ← replaces border-coffee-200
border-[var(--amp-border-light)]      ← replaces border-coffee-100
```

## Exception
Broadcast module templates (`templates/broadcast/`) use Tailwind `dark:` utilities (dark:text-white, dark:bg-slate-800). These work because `.dark` is also on `<html>`, but they are not on the CSS var system. Tracked as TD-008. Do NOT change them unless doing a full broadcast template refactor.

## Inline `<style>` blocks
If a template has a `<style>` block with hardcoded colors (e.g. `background-color: white`), replace with CSS variable equivalents:
- `background-color: white` → `background-color: var(--amp-surface-secondary)`
- `color: #1A0F0B` → `color: var(--amp-text-primary)`
- `border-color: #d6ccc0` → `border-color: var(--amp-border-default)`
