# 08 — Typography

Kabulhaden CMS uses a dual-font system: **Poppins** for headings and UI accents, **Inter** for body text and general content.

---

## Font Families

| Family | Weight(s) | Tailwind Class | Usage |
|---|---|---|---|
| **Poppins** | 400, 500, 600, 700, 800 | `font-heading` | Headings, buttons, labels, badges, navigation brand |
| **Inter** | 400, 500, 600, 700 | `font-body` | Body text, paragraphs, form inputs, descriptions |

### Why This Pairing

- **Poppins** is a geometric sans-serif with personality — it gives headings a warm, approachable feel that matches the coffee palette.
- **Inter** is optimized for screen readability at small sizes — ideal for body text, form fields, and data-dense admin interfaces.
- Both fonts share similar x-heights and proportions, creating visual harmony when used together.

---

## Google Fonts Loading

Fonts are loaded via Google Fonts CDN in `templates/base.html`:

```html
<!-- Google Fonts: Poppins + Inter -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Poppins:wght@400;500;600;700;800&display=swap" rel="stylesheet">
```

### Loading Strategy

- `preconnect` hints establish early connections to Google's CDN
- `display=swap` ensures text remains visible during font loading (FOUT, not FOIT)
- Both `font-heading` and `font-body` are available immediately via the `<link>` tag

---

## Tailwind Configuration

```javascript
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      fontFamily: {
        heading: ['Poppins', 'sans-serif'],
        body: ['Inter', 'sans-serif'],
      },
    },
  },
}
```

### Application in Templates

```html
<!-- Body uses Inter by default (set in base.html) -->
<body class="font-body">

<!-- Headings use Poppins -->
<h1 class="font-heading font-bold text-4xl">Beranda</h1>
<h2 class="font-heading font-semibold text-2xl">Program Unggulan</h2>

<!-- Buttons use Poppins -->
<button class="font-heading font-semibold text-sm">
  DENGARKAN LIVE
</button>

<!-- Body text explicitly uses Inter -->
<p class="font-body text-base leading-relaxed">
  Deskripsi program di sini.
</p>
```

---

## Font Size Scale

### Headings (Poppins)

| Element | Tailwind Class | Font Size | Line Height | Letter Spacing | Usage |
|---|---|---|---|---|---|
| **H1** | `text-4xl lg:text-5xl` | 2.25rem → 3rem | 1.2 | -0.025em | Page titles, hero headings |
| **H2** | `text-2xl md:text-3xl lg:text-4xl` | 1.5rem → 2.25rem | 1.3 | -0.02em | Section headings |
| **H3** | `text-xl md:text-2xl` | 1.25rem → 1.5rem | 1.4 | -0.015em | Subsection headings |
| **H4** | `text-lg md:text-xl` | 1.125rem → 1.25rem | 1.4 | -0.01em | Card titles |
| **H5** | `text-base md:text-lg` | 1rem → 1.125rem | 1.5 | 0 | Small headings |
| **Overline** | `text-xs font-heading font-semibold uppercase tracking-wider` | 0.75rem | 1.5 | 0.1em | Category labels, section labels |

### Body Text (Inter)

| Element | Tailwind Class | Font Size | Line Height | Usage |
|---|---|---|---|---|
| **Large** | `text-lg` | 1.125rem | 1.6 | Hero descriptions, intros |
| **Base** | `text-base` | 1rem | 1.6 | Default body text |
| **Small** | `text-sm` | 0.875rem | 1.5 | Navigation links, form labels |
| **Extra Small** | `text-xs` | 0.75rem | 1.5 | Timestamps, metadata, badges |

### UI Elements

| Element | Font | Weight | Size | Tailwind Classes |
|---|---|---|---|---|
| **Brand Logo** | Poppins | 700 | 1.25rem | `text-xl font-heading font-bold` |
| **Nav Links** | Inter | 500 | 0.875rem | `text-sm font-body font-medium` |
| **Button Primary** | Poppins | 600 | 0.875rem | `text-sm font-heading font-semibold` |
| **Button Small** | Poppins | 600 | 0.75rem | `text-xs font-heading font-semibold` |
| **Card Title** | Poppins | 600 | 1.125rem | `text-lg font-heading font-semibold` |
| **Badge** | Poppins | 600 | 0.75rem | `text-xs font-heading font-semibold uppercase tracking-wider` |
| **Form Input** | Inter | 400 | 0.875rem | `text-sm font-body` |
| **Form Error** | Inter | 400 | 0.75rem | `text-xs text-red-600` |
| **Footer Text** | Inter | 400 | 0.75rem | `text-xs font-body` |

---

## Font Weight Map

| Weight | Poppins Usage | Inter Usage |
|---|---|---|
| **400** | — | Body text, paragraphs, form inputs |
| **500** | — | Navigation links, medium emphasis text |
| **600** | Buttons, card titles, badges, labels | — |
| **700** | H1–H3 headings, logo, bold emphasis | Bold body text (sparingly) |
| **800** | Hero headings (display), extra bold | — |

---

## Typography in Key Components

### Public Website Navbar

```html
<!-- templates/website/components/navbar.html -->
<a class="text-xl font-heading font-bold text-coffee-700">
  Kabulhaden
</a>
<a class="text-sm font-body font-medium text-[#666666] hover:text-coffee-600">
  Beranda
</a>
```

### Hero Section

```html
<!-- templates/website/components/home/hero_radio.html -->
<h1 class="text-4xl md:text-5xl lg:text-6xl font-heading font-bold text-white">
  Dengarkan Siaran Langsung
</h1>
<p class="text-lg font-body text-white/80">
  Temukan program favorit Anda
</p>
```

### Card Titles

```html
<h3 class="font-heading font-semibold text-lg text-coffee-700">
  Program Unggulan
</h3>
<p class="font-body text-sm text-[#666666]">
  Deskripsi singkat program
</p>
```

### Dashboard Sidebar

```html
<!-- templates/dashboard_base.html -->
<span class="font-bold text-xl text-brand-500">Kabulhaden CMS</span>
<span class="text-xs font-semibold text-slate-400 uppercase tracking-wider">CMS Modules</span>
<a class="text-sm font-medium text-slate-600">Radio Engine</a>
```

### Badges & Labels

```html
<!-- Overline / Section Label -->
<span class="text-xs font-heading font-semibold text-coffee-300 uppercase tracking-wider">
  Program Unggulan
</span>

<!-- Status Badge -->
<span class="text-xs font-heading font-semibold px-2 py-1 rounded-full bg-green-100 text-green-800">
  Online
</span>
```

---

## Responsive Typography

Font sizes scale across breakpoints using Tailwind's responsive prefixes:

```html
<!-- Typical heading scaling -->
<h1 class="text-3xl sm:text-4xl lg:text-5xl font-heading font-bold">
  Judul Halaman
</h1>

<h2 class="text-2xl md:text-3xl lg:text-4xl font-heading font-bold">
  Section Title
</h2>

<!-- Body text stays consistent, only adjusts spacing -->
<p class="text-base md:text-lg font-body leading-relaxed">
  Deskripsi konten
</p>
```

### Mobile Adjustments

- Headings reduce by 1 step on mobile (e.g., `text-4xl` becomes `text-3xl`)
- Body text size remains consistent across breakpoints (readability priority)
- Line height increases slightly on mobile for better readability on small screens
- Letter spacing on overline labels stays constant (0.1em)

---

## Typography Rules

1. **Never mix font families within the same visual element** — headings are Poppins, body is Inter, never both in one line.
2. **Use `font-heading` for all interactive elements** — buttons, nav links, badges use Poppins for consistency.
3. **Body text must be at least `text-sm` (0.875rem)** — no smaller for readable content.
4. **Overline/label text uses `uppercase tracking-wider`** — provides clear visual hierarchy for category labels.
5. **Maintain the weight hierarchy** — 700 for headings, 600 for buttons/labels, 500 for nav, 400 for body.
6. **Line height for body text is always 1.6** — ensures comfortable reading at all sizes.
