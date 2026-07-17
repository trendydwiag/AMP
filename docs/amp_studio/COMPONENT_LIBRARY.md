# AMP Studio — Component Library

## Layout Components

### App Shell (`amp-app`)
```html
<div class="amp-app" :class="{ 'sidebar-collapsed': sidebarCollapsed }">
  <aside class="amp-sidebar">...</aside>
  <div class="amp-main" :class="{ 'expanded': sidebarCollapsed }">
    <header class="amp-header">...</header>
    <main class="amp-content">...</main>
    <div class="amp-player-bar">...</div>
  </div>
</div>
```

### Sidebar (`amp-sidebar`)
- Fixed left, full height
- Collapsed width: 72px, Expanded: 260px
- Contains: Logo, Navigation, User Footer

### Header (`amp-header`)
- Sticky top, 64px height
- Blur backdrop effect
- Contains: Sidebar toggle, Stream status, Search, Notifications, Theme toggle, User menu

### Player Bar (`amp-player-bar`)
- Fixed bottom, 64px height
- Contains: Now playing info, Playback controls, Volume, Stream info

---

## Card Components

### Basic Card
```html
<div class="amp-card p-6">Content</div>
```

### Elevated Card
```html
<div class="amp-card amp-card-elevated p-6">Content</div>
```

### Interactive Card
```html
<div class="amp-card amp-card-interactive p-4 cursor-pointer">Clickable content</div>
```

---

## Button Components

### Button Variants
```html
<button class="amp-btn amp-btn-primary">Primary</button>
<button class="amp-btn amp-btn-secondary">Secondary</button>
<button class="amp-btn amp-btn-ghost">Ghost</button>
<button class="amp-btn amp-btn-danger">Danger</button>
```

### Button Sizes
```html
<button class="amp-btn amp-btn-sm">Small</button>
<button class="amp-btn">Default</button>
<button class="amp-btn amp-btn-lg">Large</button>
```

### Icon Button
```html
<button class="amp-btn amp-btn-ghost amp-btn-icon">
  <svg>...</svg>
</button>
```

### Button with Icon
```html
<button class="amp-btn amp-btn-primary gap-2">
  <svg>...</svg>
  Label
</button>
```

---

## Badge Components

```html
<span class="amp-badge amp-badge-default">Default</span>
<span class="amp-badge amp-badge-secondary">Secondary</span>
<span class="amp-badge amp-badge-success">Success</span>
<span class="amp-badge amp-badge-warning">Warning</span>
<span class="amp-badge amp-badge-danger">Danger</span>
<span class="amp-badge amp-badge-info">Info</span>
<span class="amp-badge amp-badge-coffee">Coffee</span>
```

### Badge Sizes
```html
<span class="amp-badge amp-badge-sm">Small</span>
<span class="amp-badge">Default</span>
```

---

## Form Components

### Input
```html
<input class="amp-input" placeholder="Placeholder text">
```

### Input with Icon
```html
<div class="relative">
  <svg class="absolute left-3 top-1/2 -translate-y-1/2">...</svg>
  <input class="amp-input pl-10">
</div>
```

### Select
```html
<select class="amp-input">
  <option>Option 1</option>
</select>
```

---

## Feedback Components

### Status Dot
```html
<span class="amp-status-dot"></span>         <!-- Default -->
<span class="amp-status-dot live"></span>    <!-- Live (red pulse) -->
<span class="amp-status-dot offline"></span> <!-- Offline -->
```

### Toast (JavaScript)
```javascript
ampToast('Message', 'success', 4000);
// Types: 'success', 'error', 'warning', 'info'
```

### Empty State
```html
<div class="amp-empty">
  <div class="amp-empty-icon"><svg>...</svg></div>
  <p class="amp-empty-title">Title</p>
  <p class="amp-empty-description">Description</p>
  <button class="amp-btn amp-btn-primary">Action</button>
</div>
```

### Skeleton Loading
```html
<div class="amp-skeleton-rect w-full h-4"></div>
<div class="amp-skeleton-circle w-10 h-10"></div>
```

---

## Navigation Components

### Nav Item
```html
<a href="..." class="amp-nav-item">
  <svg>...</svg>
  <span>Label</span>
</a>
```

### Nav Section (Collapsible)
```html
<div class="amp-nav-section" x-data="{ open: false }">
  <button @click="open = !open" class="amp-nav-item w-full">
    <svg>...</svg>
    <span>Section</span>
    <svg class="ml-auto w-4 h-4 transition-transform" :class="{ 'rotate-180': open }">...</svg>
  </button>
  <div x-show="open && !sidebarCollapsed" x-collapse class="mt-1 ml-9 space-y-0.5">
    <a href="..." class="amp-nav-item">Child 1</a>
  </div>
</div>
```

### Dropdown
```html
<div class="relative" x-data="{ open: false }">
  <button @click="open = !open">Trigger</button>
  <div x-show="open" @click.outside="open = false" class="amp-dropdown right-0 mt-2 w-56">
    <a class="amp-dropdown-item">Item</a>
    <div class="amp-dropdown-divider"></div>
  </div>
</div>
```

---

## Data Display

### Metric
```html
<p class="amp-metric-value">1,234</p>
<p class="amp-metric-label">Label</p>
```

### Avatar
```html
<div class="amp-avatar amp-avatar-sm">AB</div>
<div class="amp-avatar">AB</div>
<div class="amp-avatar amp-avatar-lg">AB</div>
```

### Progress Bar
```html
<div class="w-full h-2 bg-[var(--amp-surface-tertiary)] rounded-full overflow-hidden">
  <div class="h-full bg-[var(--amp-coffee-500)] rounded-full" style="width: 60%"></div>
</div>
```

### Separator
```html
<div class="amp-separator my-3"></div>
```

---

## Overlay Components

### Modal
```html
<div x-show="open" class="fixed inset-0 z-[1070] flex items-center justify-center">
  <div class="absolute inset-0 bg-black/50"></div>
  <div class="relative amp-card p-6 max-w-lg w-full mx-4">Content</div>
</div>
```

### Drawer
```html
<div x-show="open" class="fixed inset-0 z-[1070]">
  <div class="absolute inset-0 bg-black/50"></div>
  <div class="absolute right-0 top-0 bottom-0 w-96 bg-[var(--amp-surface-primary)] p-6">Content</div>
</div>
```

### Command Palette
See `templates/amp_studio/components/command_palette.html` for full implementation.

### Notification Panel
See `templates/amp_studio/components/notifications.html` for full implementation.

---

## Tooltip
```html
<div data-amp-tooltip="Tooltip text">Element</div>
```

## Tabs
```html
<div class="amp-tabs">
  <button class="amp-tab active">Tab 1</button>
  <button class="amp-tab">Tab 2</button>
</div>
```
