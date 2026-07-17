# 0006. Use Tailwind CSS

**Status:** Accepted
**Date:** 2024-07-01

## Context

The CMS frontend requires:

- Consistent styling across admin panel and public website
- Responsive design for desktop, tablet, and mobile
- Custom coffee-themed color palette
- Fast iteration speed for UI development
- Small production CSS bundle (no heavy framework)

Custom CSS or Bootstrap would require extensive overrides. A utility-first approach allows rapid prototyping with full design control.

## Decision

We use **Tailwind CSS 3.4.x** with the following configuration:

```javascript
// tailwind.config.js
module.exports = {
  content: [
    "./templates/**/*.html",
    "./apps/**/templates/**/*.html",
    "./static/**/*.js",
    "./utils/**/*.py"
  ],
  theme: {
    extend: {
      colors: {
        coffee: {
          50: '#FAF7F3', 100: '#F5F0EA', 200: '#E7DDD3',
          300: '#C89B6D', 400: '#8C5A3C', 500: '#6B4226',
          600: '#4E2F1F', 700: '#3A2318', 800: '#2B1A13', 900: '#1A0F0B',
        },
        live: '#E53935', success: '#2F9E44',
      },
      fontFamily: {
        heading: ['Poppins', 'sans-serif'],
        body: ['Inter', 'sans-serif'],
      },
    },
  },
}
```

Build scripts in `package.json`:

```bash
npm run build       # Minified production CSS
npm run build:dev   # Development CSS (unminified)
npm run watch       # Watch mode for live development
```

WhiteNoise serves the compiled CSS with Brotli compression.

## Consequences

**Positive:**

- Utility classes in templates eliminate most custom CSS files.
- PurgeCSS removes unused classes, keeping the production bundle small (~15-25KB).
- Coffee palette defined in config is available as `bg-coffee-500`, `text-coffee-300`, etc.
- Custom `font-heading` and `font-body` utilities apply Poppins/Inter consistently.
- `box-shadow-card`, `shadow-card-hover` utilities standardize elevation.

**Negative:**

- Templates become verbose with many utility classes.
- Requires Node.js for building (dev dependency only).
- Learning curve for developers unfamiliar with utility-first CSS.

**Mitigations:**

- Component patterns documented in `docs/11_COMPONENT_LIBRARY.md`.
- `@apply` directives can extract repeated patterns into named classes.
- Node.js is only needed at build time; production serves pre-compiled CSS.
