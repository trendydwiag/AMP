# 25 — Tailwind Configuration

Kabulhaden CMS customizes Tailwind CSS with project-specific colors, fonts, spacing, and utility classes. The configuration lives in `tailwind.config.js` and is also injected via CDN in development.

---

## Configuration File

**Path:** `tailwind.config.js`

```javascript
/** @type {import('tailwindcss').Config} */
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
          50: '#FAF7F3',
          100: '#F5F0EA',
          200: '#E7DDD3',
          300: '#C89B6D',
          400: '#8C5A3C',
          500: '#6B4226',
          600: '#4E2F1F',
          700: '#3A2318',
          800: '#2B1A13',
          900: '#1A0F0B',
        },
        live: '#E53935',
        success: '#2F9E44',
      },
      fontFamily: {
        heading: ['Poppins', 'sans-serif'],
        body: ['Inter', 'sans-serif'],
      },
      maxWidth: {
        'site': '1440px',
        'content': '1280px',
      },
      spacing: {
        'section': '96px',
        'section-md': '64px',
        'section-sm': '48px',
      },
      borderRadius: {
        'card': '20px',
        'card-lg': '24px',
      },
      boxShadow: {
        'card': '0 10px 30px rgba(0,0,0,.08)',
        'card-hover': '0 20px 40px rgba(0,0,0,.12)',
        'hero-card': '0 30px 60px rgba(0,0,0,.20)',
        'header': '0 1px 3px rgba(0,0,0,.06)',
        'player': '0 -4px 20px rgba(0,0,0,.08)',
      },
      transitionDuration: {
        '250': '250ms',
      }
    },
  },
  plugins: [],
}
```

**Reference:** `tailwind.config.js:1-57`

---

## Color System

### Coffee Palette

| Token | Hex | Tailwind Class | Usage |
|---|---|---|---|
| coffee-50 | `#FAF7F3` | `bg-coffee-50` | Page background, hover bg |
| coffee-100 | `#F5F0EA` | `bg-coffee-100` | Light backgrounds, icon bg |
| coffee-200 | `#E7DDD3` | `border-coffee-200` | Borders, dividers |
| coffee-300 | `#C89B6D` | `text-coffee-300` | Muted headings, labels |
| coffee-400 | `#8C5A3C` | `bg-coffee-400` | Primary CTA, active states |
| coffee-500 | `#6B4226` | `bg-coffee-500` | CTA hover, emphasis |
| coffee-600 | `#4E2F1F` | `bg-coffee-600` | Logo bg, active nav |
| coffee-700 | `#3A2318` | `text-coffee-700` | Headings, logo text |
| coffee-800 | `#2B1A13` | `text-coffee-800` | Dark text |
| coffee-900 | `#1A0F0B` | `text-coffee-900` | Darkest text |

### Accent Colors

| Token | Hex | Tailwind Class | Usage |
|---|---|---|---|
| live | `#E53935` | `text-live` / `bg-live` | Live indicator, red accents |
| success | `#2F9E44` | `text-success` | Success states |

### Brand Colors (CDN fallback)

| Token | Hex | Tailwind Class | Usage |
|---|---|---|---|
| brand-50 | `#f5f7fa` | `bg-brand-50` | Light blue bg |
| brand-100 | `#e4ebf2` | `bg-brand-100` | Lighter blue bg |
| brand-500 | `#1e3a8a` | `bg-brand-500` | Auth buttons, brand |
| brand-600 | `#172554` | `bg-brand-600` | Auth button hover |

---

## Typography

### Font Families

| Token | Font | Tailwind Class | Usage |
|---|---|---|---|
| heading | Poppins | `font-heading` | Headings, titles, CTAs |
| body | Inter | `font-body` | Body text, UI elements |

### Font Loading

```html
<!-- Google Fonts loaded in base.html -->
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Poppins:wght@400;500;600;700;800&display=swap" rel="stylesheet">
```

**Reference:** `templates/base.html:13`

### Usage

```html
<h1 class="font-heading font-bold text-coffee-700">Heading</h1>
<p class="font-body text-sm text-[#666666]">Body text</p>
<button class="font-heading font-semibold text-sm">CTA Button</button>
```

---

## Spacing

### Section Spacing

| Token | Value | Tailwind Class | Usage |
|---|---|---|---|
| section | 96px | `py-section` | Major page sections |
| section-md | 64px | `py-section-md` | Secondary sections |
| section-sm | 48px | `py-section-sm` | Compact sections |

### Responsive Horizontal Padding

| Breakpoint | Padding | Tailwind Class |
|---|---|---|
| Mobile | 16px | `px-4` |
| Tablet | 24px | `sm:px-6` |
| Desktop | 32px | `lg:px-8` |

---

## Border Radius

| Token | Value | Tailwind Class | Usage |
|---|---|---|---|
| card | 20px | `rounded-card` | Standard cards |
| card-lg | 24px | `rounded-card-lg` | Hero cards, featured |
| (default) | 8px | `rounded-lg` | Buttons, inputs |
| (default) | 12px | `rounded-xl` | Dashboard cards, dropdowns |
| (default) | 16px | `rounded-2xl` | Mega dropdown, search modal |
| full | 9999px | `rounded-full` | Avatars, badges, dots |

---

## Shadows

| Token | Value | Tailwind Class | Usage |
|---|---|---|---|
| header | `0 1px 3px rgba(0,0,0,.06)` | `shadow-header` | Sticky navbar |
| card | `0 10px 30px rgba(0,0,0,.08)` | `shadow-card` | Default card |
| card-hover | `0 20px 40px rgba(0,0,0,.12)` | `shadow-card-hover` | Card hover |
| hero-card | `0 30px 60px rgba(0,0,0,.20)` | `shadow-hero-card` | Hero sections |
| player | `0 -4px 20px rgba(0,0,0,.08)` | `shadow-player` | Sticky bottom player |

---

## Max Width

| Token | Value | Tailwind Class | Usage |
|---|---|---|---|
| site | 1440px | `max-w-site` | Outermost site container |
| content | 1280px | `max-w-content` | Content areas |

---

## Dark Mode

```javascript
darkMode: 'class',
```

Activated by adding `class="dark"` to `<html>` element. See [24_DARK_MODE.md](24_DARK_MODE.md).

---

## Build Commands

### Production Build

```bash
# Compile Tailwind CSS
npx tailwindcss -i ./static/css/input.css -o ./static/css/styles.css --minify

# Or via npm script (if defined in package.json)
npm run build
```

### Development Watch

```bash
# Watch mode
npx tailwindcss -i ./static/css/input.css -o ./static/css/styles.css --watch

# Or via npm script
npm run dev
```

### CDN Fallback (Development)

In development (`IS_DEBUG=True`), the Tailwind CDN is loaded with the config inline:

```html
<script src="https://cdn.tailwindcss.com"></script>
<script>
  tailwind.config = { /* ... */ }
</script>
```

**Reference:** `templates/base.html:21-69`

---

## Content Paths

Tailwind scans these paths for class usage:

```javascript
content: [
  "./templates/**/*.html",          // All Django templates
  "./apps/**/templates/**/*.html",  // App-specific templates
  "./static/**/*.js",               // JavaScript files
  "./utils/**/*.py"                 // Python utilities
]
```

---

## Custom Utility Classes

The project does not define custom `@layer` utilities. All styling uses Tailwind's built-in utilities plus the extended theme tokens.

---

## Plugin Usage

No Tailwind plugins are currently installed.

```javascript
plugins: [],
```
