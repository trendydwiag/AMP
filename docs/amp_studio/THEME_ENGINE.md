# AMP Studio — Theme Engine

## Overview

AMP Studio supports three themes: **Light** (default), **Dark**, and **Coffee**. The theme is applied via the `data-theme` attribute on `<html>` and persisted in `localStorage`.

## Implementation

### Theme Application
```javascript
// Set theme
document.documentElement.setAttribute('data-theme', 'dark');
localStorage.setItem('amp-theme', 'dark');

// Read theme
const theme = localStorage.getItem('amp-theme') || 'light';
```

### CSS Activation
```css
/* Light theme (default) — no attribute needed */
:root {
  --amp-surface-primary: #FFFFFF;
  --amp-surface-secondary: #FAF7F3;
  /* ... */
}

/* Dark theme */
[data-theme="dark"] {
  --amp-surface-primary: #111111;
  --amp-surface-secondary: #1A1A1A;
  --amp-surface-tertiary: #222222;
  --amp-text-primary: #F5F0EA;
  --amp-text-secondary: #C89B6D;
  --amp-text-tertiary: #8C5A3C;
  --amp-border-light: #333333;
  --amp-border-medium: #555555;
}

/* Coffee theme */
[data-theme="coffee"] {
  --amp-surface-primary: #FAF7F3;
  --amp-surface-secondary: #F5F0EA;
  --amp-surface-tertiary: #E7DDD3;
  /* Coffee tones intensified */
}
```

### Theme Toggle (Header Button)
```html
<button @click="toggleTheme()" class="amp-btn amp-btn-ghost amp-btn-icon">
  <svg x-show="theme === 'light'" ...><!-- Moon icon --></svg>
  <svg x-show="theme === 'dark'" ...><!-- Sun icon --></svg>
</button>
```

## Alpine.js Integration

The `ampStudio()` data object manages theme state:

```javascript
function ampStudio() {
  return {
    theme: localStorage.getItem('amp-theme') || 'light',

    init() {
      document.documentElement.setAttribute('data-theme', this.theme);
    },

    toggleTheme() {
      this.theme = this.theme === 'light' ? 'dark' : 'light';
      document.documentElement.setAttribute('data-theme', this.theme);
      localStorage.setItem('amp-theme', this.theme);
    }
  };
}
```

## System Preference Detection

On first visit (no localStorage), the theme follows system preference:

```javascript
if (!localStorage.getItem('amp-theme')) {
  const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
  this.theme = prefersDark ? 'dark' : 'light';
}
```

## Dark Mode Specifics

### Header
```css
[data-theme="dark"] .amp-header {
  background: rgba(17, 17, 17, 0.85);
}
```

### Sidebar
```css
[data-theme="dark"] .amp-sidebar {
  background: #111111;
  border-right-color: #333333;
}
```

### Cards
```css
[data-theme="dark"] .amp-card {
  background: #1A1A1A;
  border-color: #333333;
}
```

### Forms
```css
[data-theme="dark"] .amp-input {
  background: #222222;
  border-color: #444444;
  color: #F5F0EA;
}
```

## Future: Coffee Theme

The Coffee theme will intensify the warm coffee palette across all surfaces, creating a sepia-toned experience. Implementation is deferred to Phase 10.
