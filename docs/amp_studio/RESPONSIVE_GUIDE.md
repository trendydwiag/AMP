# AMP Studio — Responsive Guide

## Breakpoints

| Breakpoint | Width | Layout |
|-----------|-------|--------|
| Mobile | < 640px | Single column, stacked layout |
| Tablet | 640–1024px | Two column where possible |
| Desktop | > 1024px | Full sidebar, multi-column grid |
| Large | > 1280px | Max-width content area |

## Behavior by Breakpoint

### Desktop (> 1024px)
- Sidebar visible by default (260px)
- Collapsible to 72px (icon-only)
- Full grid layouts (2, 3, 4 columns)
- Player bar spans full width below sidebar
- Header has all elements visible

### Tablet (640–1024px)
- Sidebar hidden off-canvas (hamburger toggle)
- Grid collapses: 4 → 2 columns, 3 → 2 columns
- Player bar spans full width
- Stream status widget hidden in header
- Search input shows icon only (no text label)

### Mobile (< 640px)
- Sidebar is overlay with backdrop
- All grids collapse to single column
- Page padding reduced (`--amp-space-4`)
- Player bar simplified (no volume slider, no stream info)
- Header simplified (fewer visible controls)
- Command palette is full-screen
- Notifications panel is full-width

## CSS Implementation

```css
/* Tablet */
@media (max-width: 1024px) {
  .amp-sidebar { transform: translateX(-100%); }
  .amp-sidebar.open { transform: translateX(0); }
  .amp-main { margin-left: 0; }
  .amp-player-bar { left: 0; }
  .amp-grid-3, .amp-grid-4 { grid-template-columns: repeat(2, 1fr); }
}

/* Mobile */
@media (max-width: 640px) {
  .amp-grid-2, .amp-grid-3, .amp-grid-4 {
    grid-template-columns: 1fr;
  }
  .amp-content { padding: var(--amp-space-4); }
}
```

## Touch Considerations
- All interactive elements minimum 44×44px touch target
- Swipe gestures on mobile for sidebar open/close (planned)
- Long-press for context menus (planned)
- Pull-to-refresh on list views (planned)

## Player Bar Responsive
- **Desktop**: Full player with all controls
- **Tablet**: Full player, hidden bitrate/listeners
- **Mobile**: Minimal player (play/pause + now playing only)
