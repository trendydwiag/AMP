# AMP Studio — UI Guidelines

## Design Philosophy

AMP Studio follows a **clean, spacious, purposeful** design inspired by Notion, Spotify Studio, YouTube Studio, Linear, Vercel, and Stripe.

### Core Principles
1. **Clarity over cleverness** — Every element has a clear purpose
2. **Progressive disclosure** — Show only what's needed, when needed
3. **Consistent patterns** — Same interaction = same appearance
4. **Coffee warmth** — Warm palette that feels inviting, not clinical

## Visual Language

### Color Hierarchy
| Token | Usage |
|-------|-------|
| `--amp-coffee-600` | Primary actions, active states, links |
| `--amp-surface-primary` | Card backgrounds, sidebar |
| `--amp-surface-secondary` | Page background |
| `--amp-surface-tertiary` | Hover states, subtle backgrounds |
| `--amp-text-primary` | Headings, important text |
| `--amp-text-secondary` | Body text, descriptions |
| `--amp-text-tertiary` | Timestamps, labels, hints |

### Spacing System
Use the 4px base grid via CSS tokens:
- `--amp-space-1` = 4px (tight spacing)
- `--amp-space-2` = 8px (default gap)
- `--amp-space-3` = 12px (comfortable gap)
- `--amp-space-4` = 16px (section gap)
- `--amp-space-6` = 24px (page padding)
- `--amp-space-8` = 32px (large sections)

### Border Radius
- `--amp-radius-sm` = 6px (badges, small elements)
- `--amp-radius-md` = 8px (buttons, inputs)
- `--amp-radius-lg` = 12px (cards)
- `--amp-radius-xl` = 16px (modals, drawers)
- `--amp-radius-2xl` = 20px (command palette)
- `--amp-radius-full` = 9999px (avatars, status dots)

## Typography

### Font Stack
- **Headings**: Poppins (500, 600, 700)
- **Body**: Inter (400, 500, 600)

### Type Scale
| Token | Size | Usage |
|-------|------|-------|
| `--amp-text-xs` | 12px | Timestamps, badges |
| `--amp-text-sm` | 14px | Body text, descriptions |
| `--amp-text-base` | 16px | Default text |
| `--amp-text-lg` | 18px | Section headings |
| `--amp-text-xl` | 20px | Card headings |
| `--amp-text-2xl` | 24px | Page titles |

## Component Patterns

### Cards
```html
<div class="amp-card amp-card-elevated p-6">
  <!-- Content -->
</div>
```
- Use `amp-card-elevated` for primary content areas
- Use plain `amp-card` for nested elements
- Padding: `p-5` for metric cards, `p-6` for content cards

### Buttons
```html
<button class="amp-btn amp-btn-primary">Primary Action</button>
<button class="amp-btn amp-btn-secondary">Secondary</button>
<button class="amp-btn amp-btn-ghost">Ghost</button>
<button class="amp-btn amp-btn-danger">Destructive</button>
```
- Primary: filled coffee-600 background
- Secondary: bordered, transparent background
- Ghost: no border, no background
- Danger: red for destructive actions

### Badges
```html
<span class="amp-badge amp-badge-success">Published</span>
<span class="amp-badge amp-badge-warning">Pending</span>
<span class="amp-badge amp-badge-danger">Error</span>
```

### Inputs
```html
<input class="amp-input" placeholder="Search...">
<select class="amp-input">...</select>
```

## Empty States
Every list/table should have an empty state:
```html
<div class="amp-empty">
  <div class="amp-empty-icon"><!-- SVG --></div>
  <p class="amp-empty-title">No items yet</p>
  <p class="amp-empty-description">Create your first item to get started.</p>
  <button class="amp-btn amp-btn-primary">Create</button>
</div>
```

## Icons
- Use inline SVGs only (no icon font)
- Size: 16px for inline, 20px for navigation, 24px for feature icons
- Stroke width: 1.5px for decorative, 2px for interactive
