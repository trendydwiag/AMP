# 07 — Color Palette

Kabulhaden CMS uses a **coffee-inspired** color palette that evokes warmth, professionalism, and the communal atmosphere of a radio station.

---

## Primary Palette: Coffee Scale

The coffee scale is the dominant color system used across the entire UI — from the public website to the admin dashboard.

| Token | Hex | RGB | Tailwind Class | Usage |
|---|---|---|---|---|
| **Coffee 50** | `#FAF7F3` | 250, 247, 243 | `coffee-50` | Page background (body `bg-[#FAF7F3]`) |
| **Coffee 100** | `#F5F0EA` | 245, 240, 234 | `coffee-100` | Card hover states, subtle backgrounds |
| **Coffee 200** | `#E7DDD3` | 231, 221, 211 | `coffee-200` | Borders, dividers, `border-coffee-200` |
| **Coffee 300** | `#C89B6D` | 200, 155, 109 | `coffee-300` | Accent text, audio bars, secondary labels |
| **Coffee 400** | `#8C5A3C` | 140, 90, 60 | `coffee-400` | Primary buttons, CTA, "DENGARKAN LIVE" button |
| **Coffee 500** | `#6B4226` | 107, 66, 38 | `coffee-500` | Button hover states, icon fills |
| **Coffee 600** | `#4E2F1F` | 78, 47, 31 | `coffee-600` | Dark CTA sections, hero cards, logo background |
| **Coffee 700** | `#3A2318` | 58, 35, 24 | `coffee-700` | Headings, logo text (`text-coffee-700`) |
| **Coffee 800** | `#2B1A13` | 43, 26, 19 | `coffee-800` | Hero section backgrounds |
| **Coffee 900** | `#1A0F0B` | 26, 15, 11 | `coffee-900` | Deepest darks, overlays |

### Coffee Scale Visual Reference

```
Darkest ────────────────────────────────────── Lightest

#1A0F0B  #2B1A13  #3A2318  #4E2F1F  #6B4226  #8C5A3C  #C89B6D  #E7DDD3  #F5F0EA  #FAF7F3
  900      800      700      600      500      400      300      200      100       50
```

---

## Semantic Colors

These colors are used for specific functional purposes beyond the coffee palette.

| Token | Hex | RGB | Tailwind Class | Usage |
|---|---|---|---|---|
| **Live Red** | `#E53935` | 229, 57, 53 | `live` | Live indicator dot, "LIVE" badges, on-air status |
| **Success Green** | `#2F9E44` | 47, 158, 68 | `success` | Success messages, active status, online indicator |
| **Dark Text** | `#2D2D2D` | 45, 45, 45 | `text-[#2D2D2D]` | Primary body text on light backgrounds |
| **Secondary Text** | `#666666` | 102, 102, 102 | `text-[#666666]` | Secondary/muted text, navigation links |
| **Hero BG** | `#2B1A13` | 43, 26, 19 | `bg-coffee-800` | Hero section backgrounds |
| **Border** | `#E7DDD3` | 231, 221, 211 | `border-[#E7DDD3]` | Default border color for cards and containers |
| **White** | `#FFFFFF` | 255, 255, 255 | `white` | Card backgrounds, text on dark surfaces |

---

## Admin Dashboard Colors (Dark Mode)

The admin dashboard (`dashboard_base.html`) uses a Slate-based dark mode system separate from the coffee palette.

| Token | Light Mode | Dark Mode | Tailwind Classes |
|---|---|---|---|
| **Page BG** | `slate-100` | `dark:slate-900` | `bg-slate-100 dark:bg-slate-900` |
| **Card BG** | `white` | `dark:slate-800` | `bg-white dark:bg-slate-800` |
| **Border** | `slate-200` | `dark:slate-700` | `border-slate-200 dark:border-slate-700` |
| **Text Primary** | `slate-900` | `dark:white` | `text-slate-900 dark:text-white` |
| **Text Secondary** | `slate-500` | `dark:slate-400` | `text-slate-500 dark:text-slate-400` |
| **Brand Accent** | `brand-500` (#1e3a8a) | `dark:blue-400` | `text-brand-500 dark:text-blue-400` |
| **Hover BG** | `slate-100` | `dark:slate-700` | `hover:bg-slate-100 dark:hover:bg-slate-700` |

### Admin Status Colors

| Status | Background | Text | Classes |
|---|---|---|---|
| **Success** | `green-50` / `dark:green-950` | `green-800` / `dark:green-300` | `bg-green-50 text-green-800 dark:bg-green-950 dark:text-green-300` |
| **Error** | `red-50` / `dark:red-950` | `red-800` / `dark:red-300` | `bg-red-50 text-red-800 dark:bg-red-950 dark:text-red-300` |
| **Warning** | `yellow-50` / `dark:yellow-950` | `yellow-800` / `dark:yellow-300` | `bg-yellow-50 text-yellow-800 dark:bg-yellow-950 dark:text-yellow-300` |
| **Info** | `blue-50` / `dark:blue-950` | `blue-800` / `dark:blue-300` | `bg-blue-50 text-blue-800 dark:bg-blue-950 dark:text-blue-300` |

---

## Media Type Badge Colors

Used in the media manager to indicate file types (`apps/media_manager/models.py:144`).

| File Type | Background | Text | Classes |
|---|---|---|---|
| **IMAGE** | `green-100` | `green-800` | `bg-green-100 text-green-800` |
| **VIDEO** | `blue-100` | `blue-800` | `bg-blue-100 text-blue-800` |
| **DOCUMENT** | `yellow-100` | `yellow-800` | `bg-yellow-100 text-yellow-800` |
| **AUDIO** | `purple-100` | `purple-800` | `bg-purple-100 text-purple-800` |
| **OTHER** | `gray-100` | `gray-800` | `bg-gray-100 text-gray-800` |

---

## Tailwind Configuration Reference

The coffee palette is defined in `tailwind.config.js` under `theme.extend.colors`:

```javascript
// tailwind.config.js
module.exports = {
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
    },
  },
}
```

### Usage Examples in Templates

```html
<!-- Primary button -->
<button class="bg-coffee-400 text-white hover:bg-coffee-500">
  DENGARKAN LIVE
</button>

<!-- Page background -->
<body class="bg-[#FAF7F3]">

<!-- Card with coffee border -->
<div class="border border-coffee-200 rounded-card">

<!-- Live indicator -->
<span class="w-2 h-2 bg-live rounded-full animate-pulse"></span>

<!-- Success message -->
<div class="bg-green-50 text-green-800 dark:bg-green-950 dark:text-green-300">
  Program berhasil disimpan!
</div>

<!-- Body text -->
<p class="text-[#2D2D2D]">Primary content text</p>
<p class="text-[#666666]">Secondary description text</p>
```

---

## Color Accessibility

| Combination | Contrast Ratio | WCAG AA | WCAG AAA |
|---|---|---|---|
| Coffee 700 on Coffee 50 | ~8.5:1 | ✅ Pass | ✅ Pass |
| Coffee 600 on White | ~7.2:1 | ✅ Pass | ✅ Pass |
| Coffee 400 on White | ~4.6:1 | ✅ Pass (large) | ❌ Fail |
| Secondary Text (#666) on Coffee 50 | ~5.8:1 | ✅ Pass | ❌ Fail |
| Live Red on White | ~4.1:1 | ✅ Pass (large) | ❌ Fail |
| White on Coffee 600 | ~7.2:1 | ✅ Pass | ✅ Pass |

---

## Color Usage Rules

1. **Coffee 50 (`#FAF7F3`)** — Use as the default page background. Never use pure white (`#FFFFFF`) for page backgrounds on the public website.
2. **Coffee 400–500** — Primary action colors. Use `coffee-400` for default state, `coffee-500` for hover.
3. **Coffee 600–700** — Reserved for headings, dark sections, and emphasis areas.
4. **Coffee 200** — Use for borders and dividers. Never use `border-gray-*` on the public website.
5. **`#2D2D2D`** — Use for all primary body text. Do not use pure black (`#000000`).
6. **`#666666`** — Use for secondary text, descriptions, and muted content.
7. **Live Red (`#E53935`)** — Use exclusively for live/on-air indicators. Do not use for general errors.
8. **Success Green (`#2F9E44`)** — Use for positive confirmations and online status indicators.
