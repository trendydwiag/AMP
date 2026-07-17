# 22 — Animation Guide

Kabulhaden CMS uses CSS transitions, Alpine.js transitions, and HTMX animations for smooth user experiences. The default transition duration is 250ms.

---

## CSS Transition System

### Default Duration

```javascript
// tailwind.config.js
transitionDuration: {
  '250': '250ms',
}
```

### Standard Transition Classes

| Element | Transition | Tailwind Class |
|---|---|---|
| Color transitions | 250ms ease | `transition-colors duration-250` |
| Sidebar slide | 200ms ease-in-out | `transition-transform duration-200 ease-in-out` |
| Dropdown menus | 200ms ease-out (in) | `transition ease-out duration-200` |
| Card hover | 250ms default | `transition-all` |
| Button press | — | `active:scale-[.98]` |
| Shadow hover | 250ms | `transition-shadow` |
| Opacity | 300ms | `transition-opacity duration-300` |

**Reference:** `templates/dashboard_base.html`, `tailwind.config.js:51-53`

---

## Hover Effects

### Card Hover

Cards use shadow transitions on hover.

```html
<div class="bg-white rounded-card shadow-card p-6
            hover:shadow-card-hover transition-shadow duration-250">
```

**Shadow progression:**
- Default: `shadow-card` → `0 10px 30px rgba(0,0,0,.08)`
- Hover: `shadow-card-hover` → `0 20px 40px rgba(0,0,0,.12)`

### Image Scale Hover

Program and article cards scale images on hover.

```html
<div class="aspect-[4/3] overflow-hidden">
  <img src="{{ program.cover_image.url }}"
       class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500">
</div>
```

### Button Active Press

Buttons scale down slightly on press for tactile feedback.

```html
<a class="bg-coffee-400 text-white active:scale-[.98] transition-all">
  DENGARKAN LIVE
</a>
```

**Reference:** `templates/website/components/navbar.html:96`

### Link Hover States

```html
<!-- Nav link hover -->
<a class="text-[#666666] hover:text-coffee-600 hover:bg-coffee-50 transition-colors">

<!-- Dropdown item hover -->
<a class="text-coffee-700 group-hover:text-coffee-600 transition-colors">
<div class="bg-coffee-100 group-hover:bg-coffee-200 transition-colors">

<!-- Ghost button hover -->
<button class="text-[#666666] hover:text-coffee-600 hover:bg-coffee-50 transition-colors">
```

### Focus Ring

```html
<button class="focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-brand-500">
```

---

## Page Transitions

### Body Background Transition

```html
<body class="bg-[#FAF7F3] text-[#2D2D2D] font-body flex flex-col transition-colors duration-250">
```

**Reference:** `templates/base.html:76`

### Content Card Transition

```html
<div class="bg-white dark:bg-slate-800 transition-colors duration-200">
```

**Reference:** `templates/dashboard_base.html:155`

---

## Alpine.js x-transition

### Dropdown Enter/Leave

```html
<div x-show="open"
     x-transition:enter="transition ease-out duration-200"
     x-transition:enter-start="opacity-0 translate-y-1"
     x-transition:enter-end="opacity-100 translate-y-0"
     x-transition:leave="transition ease-in duration-150"
     x-transition:leave-start="opacity-100 translate-y-0"
     x-transition:leave-end="opacity-0 translate-y-1">
```

**Reference:** `templates/website/components/navbar.html:29`

### Mobile Menu Enter/Leave

```html
<div x-show="mobileMenuOpen"
     x-transition:enter="transition ease-out duration-200"
     x-transition:enter-start="opacity-0 -translate-y-2"
     x-transition:enter-end="opacity-100 translate-y-0"
     x-transition:leave="transition ease-in duration-150"
     x-transition:leave-start="opacity-100 translate-y-0"
     x-transition:leave-end="opacity-0 -translate-y-2">
```

**Reference:** `templates/website/components/navbar.html:113`

### Toast Message Fade

```html
<div x-data="{ show: true }"
     x-show="show"
     class="transition-opacity duration-300">
  <!-- message content -->
  <button @click="show = false" class="hover:opacity-70 p-1">×</button>
</div>
```

**Reference:** `templates/dashboard_base.html:140`

### Simple Fade

```html
<div x-show="isVisible"
     x-transition:enter="transition ease-out duration-300"
     x-transition:enter-start="opacity-0"
     x-transition:enter-end="opacity-100"
     x-transition:leave="transition ease-in duration-200"
     x-transition:leave-start="opacity-100"
     x-transition:leave-end="opacity-0">
```

---

## HTMX Animations

### Content Swap with Fade

```html
<div hx-get="{% url 'endpoint' %}"
     hx-trigger="revealed"
     hx-swap="innerHTML fade:300ms">
</div>
```

### HTMX Indicator Show/Hide

```css
.htmx-indicator {
  display: none;
}

.htmx-request .htmx-indicator {
  display: inline-block;
}

.htmx-request.htmx-indicator {
  display: inline-block;
}
```

### HTMX Boosted Pages

```html
<body hx-boost="true">
  <!-- All internal links will use HTMX for page transitions -->
</body>
```

---

## Loading Animations

### Pulse (Live indicator)

```html
<span class="w-2 h-2 bg-white rounded-full animate-pulse"></span>
```

**Reference:** `templates/website/components/navbar.html:97`

### Spin (Loading spinner)

```html
<svg class="animate-spin h-4 w-4 text-white" fill="none" viewBox="0 0 24 24">
  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
  <path class="opacity-75" fill="currentColor"
        d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z">
  </path>
</svg>
```

### Pulse (Skeleton loading)

```html
<div class="animate-pulse">
  <div class="h-4 bg-slate-200 rounded w-3/4"></div>
</div>
```

### Scale-in (Search modal)

```html
<div class="animate-scale-in">
  <!-- Modal content scales in from 95% -->
</div>
```

---

## CSS Keyframes (Custom)

### Wave Animation (Radio)

```css
@keyframes wave {
  0%, 100% { height: 20%; }
  50% { height: 100%; }
}
```

Used in `templates/radio/components/wave_animation.html`.

### Slide (Progress bar)

```css
@keyframes slide {
  0% { transform: translateX(-100%); }
  100% { transform: translateX(250%); }
}
```

### Scale-in (Modal)

```css
@keyframes scale-in {
  from { transform: scale(0.95); opacity: 0; }
  to { transform: scale(1); opacity: 1; }
}
```

---

## Animation Timing Reference

| Animation | Duration | Easing | Trigger |
|---|---|---|---|
| Color transitions | 250ms | ease | Hover/focus |
| Sidebar slide | 200ms | ease-in-out | Toggle button |
| Dropdown enter | 200ms | ease-out | Mouse hover/click |
| Dropdown leave | 150ms | ease-in | Mouse leave |
| Mobile menu | 200ms | ease-out | Hamburger toggle |
| Toast fade | 300ms | ease | Auto/manual dismiss |
| Card shadow | 250ms | default | Hover |
| Image scale | 500ms | default | Card hover |
| Button press | instant | — | Active state |
| Skeleton pulse | 2s | ease-in-out | CSS animation |
| Spinner rotate | 1s | linear | CSS animation |
| Live pulse | 2s | ease-in-out | CSS animation |

---

## Reduced Motion

For users with `prefers-reduced-motion`, disable animations:

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

This should be added to the global CSS to respect user system preferences.
