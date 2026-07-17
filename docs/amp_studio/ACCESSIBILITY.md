# AMP Studio — Accessibility

## Standards Target
- **WCAG 2.1 Level AA** compliance
- **Section 508** compliance
- Keyboard navigable throughout

## Keyboard Navigation

### Tab Order
1. Skip to main content link (hidden, appears on focus)
2. Sidebar navigation items
3. Header controls (search, notifications, theme, user menu)
4. Page content
5. Player bar controls

### Focus Indicators
All interactive elements have visible focus indicators:
```css
:focus-visible {
  outline: 2px solid var(--amp-coffee-600);
  outline-offset: 2px;
}
```

### Keyboard Shortcuts
| Key | Action |
|-----|--------|
| `Tab` | Move to next focusable element |
| `Shift+Tab` | Move to previous focusable element |
| `Enter` / `Space` | Activate button/link |
| `Escape` | Close modal/overlay/dropdown |
| `Arrow keys` | Navigate within menus/lists |
| `⌘K` / `Ctrl+K` | Open command palette |

## ARIA Patterns

### Landmarks
```html
<body>
  <aside role="navigation" aria-label="Main Navigation">...</aside>
  <main role="main" aria-label="Page Content">...</main>
  <div role="complementary" aria-label="Player">...</div>
</body>
```

### Buttons
```html
<!-- Icon-only buttons must have labels -->
<button aria-label="Toggle Sidebar">...</button>
<button aria-label="Close">...</button>

<!-- Toggle buttons use aria-pressed -->
<button aria-pressed="false">...</button>
```

### Modals/Overlays
```html
<div role="dialog" aria-modal="true" aria-labelledby="dialog-title">
  <h2 id="dialog-title">Dialog Title</h2>
  <!-- Focus trap inside dialog -->
</div>
```

### Live Regions
```html
<!-- For dynamic updates (stream status, toasts) -->
<div aria-live="polite" aria-atomic="true">
  <!-- Updated content -->
</div>
```

### Navigation
```html
<nav aria-label="Main Navigation">
  <ul role="menubar">
    <li role="menuitem">
      <a href="..." aria-current="page">Active Page</a>
    </li>
  </ul>
</nav>
```

## Color Contrast

| Element | Foreground | Background | Ratio | Pass? |
|---------|-----------|------------|-------|-------|
| Primary text | #1A0F0B | #FFFFFF | 16.5:1 | ✅ |
| Secondary text | #4E2F1F | #FFFFFF | 9.2:1 | ✅ |
| Tertiary text | #8C5A3C | #FFFFFF | 4.6:1 | ✅ AA |
| Primary button | #FFFFFF | #4E2F1F | 9.2:1 | ✅ |
| Links | #4E2F1F | #FFFFFF | 9.2:1 | ✅ |

## Screen Reader Support
- All images have meaningful `alt` text
- Form inputs have associated labels
- Error messages linked via `aria-describedby`
- Tables have proper `<th>` and `scope` attributes
- Dynamic content updates announced via `aria-live`

## Reduced Motion
```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

## Testing Checklist
- [ ] All pages navigable via keyboard alone
- [ ] No keyboard traps
- [ ] Focus visible on all interactive elements
- [ ] Color contrast meets AA standards
- [ ] Screen reader tested (VoiceOver/NVDA)
- [ ] `prefers-reduced-motion` respected
- [ ] Form errors announced to screen readers
- [ ] Skip navigation link present
