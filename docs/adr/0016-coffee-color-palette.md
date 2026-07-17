# 0016. Use Coffee Color Palette

**Status:** Accepted
**Date:** 2024-07-15

## Context

The CMS serves radio stations, which typically have warm, inviting brand aesthetics. The color palette should:

- Reflect the warmth of radio broadcasting (coffee shop, lounge atmosphere)
- Provide sufficient contrast for readability (WCAG AA)
- Work across admin panel and public website
- Support dark and light themes

Generic blue/gray palettes are overused and do not differentiate the brand.

## Decision

We define a **coffee-themed color palette** in `tailwind.config.js`:

```javascript
colors: {
  coffee: {
    50:  '#FAF7F3',  // Near white — backgrounds
    100: '#F5F0EA',  // Light cream — hover backgrounds
    200: '#E7DDD3',  // Warm gray — borders
    300: '#C89B6D',  // Latte — secondary accents
    400: '#8C5A3C',  // Medium roast — links
    500: '#6B4226',  // Dark roast — primary
    600: '#4E2F1F',  // Espresso — hover states
    700: '#3A2318',  // Deep espresso — text
    800: '#2B1A13',  // Near black — headings
    900: '#1A0F0B',  // Darkest — high contrast text
  },
  live: '#E53935',   // Red — live indicator
  success: '#2F9E44', // Green — success states
}
```

### Usage Guidelines

| Element | Color Token | Hex |
|---------|-------------|-----|
| Primary buttons | `bg-coffee-500` | #6B4226 |
| Button hover | `bg-coffee-600` | #4E2F1F |
| Page background | `bg-coffee-50` | #FAF7F3 |
| Card background | `bg-white` | #FFFFFF |
| Card border | `border-coffee-200` | #E7DDD3 |
| Body text | `text-coffee-800` | #2B1A13 |
| Secondary text | `text-coffee-400` | #8C5A3C |
| Links | `text-coffee-500` | #6B4226 |
| Link hover | `text-coffee-700` | #3A2318 |
| Live badge | `bg-live` | #E53935 |

## Consequences

**Positive:**

- Warm, distinctive aesthetic that differentiates from generic Bootstrap/Tailwind defaults.
- 10-shade palette provides sufficient range for all UI elements.
- Coffee-500 (`#6B4226`) as primary provides strong contrast on white backgrounds (ratio > 7:1).
- `live` and `success` semantic colors handle broadcast status and feedback.
- Palette scales naturally across light themes and can be adapted for dark mode.

**Negative:**

- Brown palette may feel dated if not balanced with whitespace and modern layout patterns.
- Limited high-saturation accent colors (relying on `live` red for highlights).
- Custom palette is a commitment — changing it later requires updating all templates.

**Mitigations:**

- Modern typography (Poppins + Inter, see ADR-0017) and generous spacing keep the design fresh.
- The `live` red and `success` green provide necessary color accents.
- Tailwind's utility classes make palette-wide changes a single config edit.
