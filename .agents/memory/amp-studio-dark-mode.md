---
name: AMP Studio Dark Mode
description: Dark mode requires both data-theme attribute AND .dark class on <html>; Tailwind CDN config needed for coffee palette and class-based dark mode.
---

## The Rule
Always toggle BOTH `data-theme="dark"` AND `.dark` class on `<html>` when switching themes.

**Why:** AMP Studio CSS (`amp-studio.css` and `design-tokens.css`) uses `[data-theme="dark"]` selector for its own variables. But all migrated templates use Tailwind `dark:` utility variants, which require the `.dark` class on `<html>` (class-based dark mode). Without `.dark`, dark: variants never activate → white-on-white bug.

## How to Apply
In `static/js/amp-studio/amp-studio.js`, every place that sets `data-theme` must also call:
```js
document.documentElement.classList.toggle('dark', this.theme === 'dark');
```

Three locations: `applyTheme()` in themeEngine, `init()` in ampStudio, `toggleTheme()` in ampStudio.

Also add an early-sync IIFE in the ampStudio data object to sync before Alpine hydrates.

## Tailwind CDN Config (amp_studio/base.html)
```js
window.tailwind = {
  config: {
    darkMode: 'class',          // Required for dark: variants
    corePlugins: { preflight: false },
    theme: {
      extend: {
        colors: {
          coffee: {
            50: '#FAF7F3', 100: '#F5F0EA', 200: '#E7DDD3',
            300: '#C89B6D', 400: '#8C5A3C', 500: '#6B4226',
            600: '#4E2F1F', 700: '#3A2318', 800: '#2B1A13', 900: '#1A0F0B'
          }
        }
      }
    }
  }
};
```

**Why coffee palette in config:** All migrated templates (broadcast, radio, podcast, content, news, users) use `text-coffee-*`, `bg-coffee-*`, `border-coffee-*` Tailwind classes. Without registering the palette in CDN Tailwind config, these classes generate no CSS.
