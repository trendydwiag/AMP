# 0017. Use Poppins + Inter Typography

**Status:** Accepted
**Date:** 2024-07-15

## Context

The CMS requires a typography system that:

- Provides clear visual hierarchy between headings and body text
- Renders well on screen at various sizes (14px to 48px+)
- Is available for free via Google Fonts
- Complements the warm coffee color palette (ADR-0016)

A single font family creates visual monotony. Two complementary fonts — one for display, one for reading — create natural hierarchy.

## Decision

We use **Poppins** for headings and **Inter** for body text.

Configuration in `tailwind.config.js`:

```javascript
fontFamily: {
  heading: ['Poppins', 'sans-serif'],
  body: ['Inter', 'sans-serif'],
},
```

### Font Roles

| Role | Font | Weight Range | Usage |
|------|------|-------------|-------|
| `font-heading` | Poppins | 500-700 | H1-H6, navigation, card titles |
| `font-body` | Inter | 400-500 | Paragraphs, form labels, table data |

### Google Fonts Loading

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Poppins:wght@500;600;700&display=swap" rel="stylesheet">
```

### Usage in Templates

```html
<h1 class="font-heading text-coffee-800 text-3xl font-bold">Judul Halaman</h1>
<p class="font-body text-coffee-600 text-base leading-relaxed">Isi konten utama...</p>
<button class="font-heading font-semibold">Simpan</button>
```

## Consequences

**Positive:**

- Poppins (geometric sans-serif) provides modern, bold headings.
- Inter (humanist sans-serif) is optimized for screen readability at body text sizes.
- Both fonts have excellent Latin + extended character support for Indonesian diacritics.
- Google Fonts CDN handles caching and global availability.
- Free, open-source fonts with no licensing concerns.

**Negative:**

- Google Fonts CDN dependency — external request for font files.
- Two font families increase page weight (~40KB total).
- Fallback `sans-serif` is system-dependent, causing minor cross-platform differences.

**Mitigations:**

- `font-display=swap` in the Google Fonts URL ensures text is visible while fonts load.
- Font files are cached aggressively by browsers and CDNs.
- System font fallbacks (`sans-serif`) are readable on all platforms.
- AppearanceSettings model allows admin to change font family in the future.
