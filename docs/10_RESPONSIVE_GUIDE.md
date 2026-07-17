# 10 — Responsive Design Guide

Kabulhaden CMS follows a mobile-first responsive design strategy. All pages adapt seamlessly from smartphone (< 640px) to desktop (> 1024px) using Tailwind CSS breakpoint utilities.

---

## Breakpoint Definitions

| Breakpoint | Range | Tailwind Prefix | Target Device |
|---|---|---|---|
| **Mobile** | 0 – 639px | (default, no prefix) | Smartphones, small screens |
| **Tablet** | 640px – 1023px | `sm:` | Tablets, large phones in landscape |
| **Desktop** | 1024px+ | `lg:` | Laptops, desktop monitors |
| **Wide** | 1280px+ | `xl:` | Large monitors (optional enhancement) |

### Tailwind Breakpoint Config

```javascript
// Default Tailwind breakpoints (no custom override needed)
screens: {
  'sm': '640px',
  'md': '768px',    // Used in some components
  'lg': '1024px',
  'xl': '1280px',
}
```

---

## Responsive Behavior by Component

### 1. Navbar (`templates/website/components/navbar.html`)

| Breakpoint | Behavior |
|---|---|
| **Mobile (< 640px)** | Logo icon only (no text), hamburger menu, "DENGARKAN LIVE" hidden |
| **Tablet (640–1023px)** | Logo + "Kabulhaden" text, "DENGARKAN LIVE" visible, hamburger still present |
| **Desktop (1024px+)** | Full horizontal nav links, Program dropdown, ⌘K search hint, hamburger hidden |

```html
<!-- Logo text hidden on mobile -->
<span class="text-xl font-heading font-bold text-coffee-700 hidden sm:block">
  Kabulhaden
</span>

<!-- Desktop navigation hidden below lg -->
<div class="hidden lg:flex items-center gap-1 absolute left-1/2 -translate-x-1/2">
  <!-- Nav links -->
</div>

<!-- Mobile hamburger visible below lg -->
<button @click="mobileMenuOpen = !mobileMenuOpen"
        class="lg:hidden p-2.5 rounded-xl">
  <!-- Hamburger/X icon -->
</button>

<!-- Mobile menu slides in below lg -->
<div x-show="mobileMenuOpen" class="lg:hidden border-t py-3 space-y-1">
  <!-- Stacked nav links -->
</div>
```

**Key classes**: `hidden lg:flex`, `lg:hidden`, `sm:block`

---

### 2. Hero Section (`templates/website/components/home/hero_radio.html`)

| Breakpoint | Behavior |
|---|---|
| **Mobile** | Full-width card, stacked layout, smaller artwork, condensed text |
| **Tablet** | Side-by-side artwork + info, medium text sizes |
| **Desktop** | Max-width 1280px centered, generous padding, large artwork |

```html
<div class="max-w-[1280px] mx-auto px-4 sm:px-6 lg:px-8">
  <!-- Hero card -->
  <div class="bg-coffee-800 rounded-card-lg p-6 md:p-10 lg:p-14">
    <!-- Text scales responsively -->
    <h1 class="text-3xl sm:text-4xl lg:text-5xl font-heading font-bold text-white">
      Siaran Langsung
    </h1>
  </div>
</div>
```

---

### 3. Sidebar (Dashboard) (`templates/dashboard_base.html`)

| Breakpoint | Behavior |
|---|---|
| **Mobile (< 768px)** | Hidden off-screen (`-translate-x-full`), toggled via hamburger button |
| **Tablet (768px+)** | Visible, fixed position, 264px wide |
| **Desktop (1024px+)** | Visible, relative position, scrollable nav |

```html
<aside :class="sidebarOpen ? 'translate-x-0' : '-translate-x-full'"
       class="w-64 fixed inset-y-0 left-0
              md:relative md:translate-x-0
              z-40 transform transition-transform duration-200
              pt-16 md:pt-0">

  <!-- Mobile toggle button -->
  <button @click="sidebarOpen = !sidebarOpen"
          class="md:hidden text-slate-500 p-2 rounded-lg">
    <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
            d="M4 6h16M4 12h16M4 18h16" />
    </svg>
  </button>
```

---

### 4. Content Cards Grid

| Breakpoint | Behavior |
|---|---|
| **Mobile** | Single column (`grid-cols-1`), full-width cards |
| **Tablet** | 2 columns (`sm:grid-cols-2`) |
| **Desktop** | 3 columns (`lg:grid-cols-3`) or 4 columns for featured items |

```html
<!-- Programs grid -->
<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
  {% for program in programs %}
  <div class="bg-white rounded-card shadow-card hover:shadow-card-hover transition-shadow">
    <!-- Card content -->
  </div>
  {% endfor %}
</div>

<!-- Featured podcasts (4 columns on desktop) -->
<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
  <!-- Podcast cards -->
</div>
```

---

### 5. Data Tables

| Breakpoint | Behavior |
|---|---|
| **Mobile** | Horizontal scroll container, condensed columns |
| **Tablet** | Full table with some columns hidden |
| **Desktop** | Full table, all columns visible |

```html
<div class="overflow-x-auto">
  <table class="w-full text-sm">
    <thead>
      <tr>
        <th class="hidden sm:table-cell">Kolom Opsional</th>
        <!-- Always-visible columns -->
      </tr>
    </thead>
    <tbody>
      <tr>
        <td class="hidden sm:table-cell">Data</td>
        <!-- Always-visible data -->
      </tr>
    </tbody>
  </table>
</div>
```

---

### 6. Sticky Radio Player

| Breakpoint | Behavior |
|---|---|
| **Mobile (< 768px)** | Bottom bar with expand-to-fullscreen overlay |
| **Desktop (768px+)** | Fixed bottom bar, always visible, compact layout |

```html
<!-- templates/website/components/sticky_player.html -->
<footer class="fixed bottom-0 left-0 right-0 z-50 bg-coffee-700 shadow-player">
  <div class="max-w-[1440px] mx-auto px-4 sm:px-6 lg:px-8">
    <div class="flex items-center justify-between h-16 md:h-20">
      <!-- Compact player info -->
    </div>
  </div>
</footer>

<!-- Mobile fullscreen player (hidden on desktop) -->
<div id="mobile-player-fullscreen"
     class="fixed inset-0 z-[100] hidden flex-col md:hidden">
  <!-- Full-screen player overlay -->
</div>
```

---

### 7. Section Spacing

| Breakpoint | Behavior |
|---|---|
| **Mobile** | Reduced padding: `py-12` (48px) or `py-16` (64px) |
| **Tablet** | Standard padding: `py-16` (64px) |
| **Desktop** | Full padding: `py-24` (96px) |

```html
<section class="py-12 md:py-16 lg:py-24">
  <!-- Or using the section tokens -->
<section class="max-w-[1280px] mx-auto px-4 sm:px-6 lg:px-8"
          style="padding-top: 96px; padding-bottom: 96px;">
```

---

### 8. Announcement Bar

| Breakpoint | Behavior |
|---|---|
| **Mobile** | Title only, content truncated |
| **Tablet+** | Title + truncated content visible |

```html
<span class="font-heading font-medium">{{ announcement.title }}</span>
<span class="hidden sm:inline">- {{ announcement.content|truncatewords:10 }}</span>
```

---

### 9. Footer (`templates/website/components/footer.html`)

| Breakpoint | Behavior |
|---|---|
| **Mobile** | Stacked columns, centered text |
| **Tablet** | 2-column layout |
| **Desktop** | 4-column layout with social links |

---

### 10. Search Modal

| Breakpoint | Behavior |
|---|---|
| **Mobile** | Full-screen overlay |
| **Desktop** | Centered modal with max-width |

```html
<div class="fixed inset-0 z-[200] bg-black/50 flex items-start justify-center pt-[15vh] px-4">
  <div class="w-full max-w-2xl bg-white rounded-card shadow-hero-card">
    <!-- Search input + results -->
  </div>
</div>
```

---

## Mobile-First CSS Patterns

### Common Responsive Combinations

```html
<!-- Hide on mobile, show on tablet+ -->
<div class="hidden sm:block">...</div>

<!-- Show on mobile, hide on desktop -->
<div class="lg:hidden">...</div>

<!-- Always visible, but adjusts spacing -->
<div class="px-4 sm:px-6 lg:px-8">...</div>

<!-- Text size scaling -->
<h1 class="text-3xl sm:text-4xl lg:text-5xl">...</h1>

<!-- Grid column scaling -->
<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-6">

<!-- Flex direction: column on mobile, row on desktop -->
<div class="flex flex-col sm:flex-row gap-6">

<!-- Centering: block on mobile, inline on desktop -->
<span class="hidden sm:inline-flex items-center gap-2">...</span>
```

---

## Touch Targets

All interactive elements on mobile meet the minimum 44x44px touch target:

```html
<!-- Navigation links: large padding on mobile -->
<a class="block px-4 py-2.5 rounded-xl text-sm font-medium">
  Beranda
</a>

<!-- Buttons: generous padding -->
<button class="px-5 py-2.5 rounded-xl text-sm font-heading font-semibold">
  DENGARKAN LIVE
</button>

<!-- Icon buttons: adequate size -->
<button class="p-2.5 rounded-xl">
  <svg class="w-5 h-5">...</svg>
</button>
```

---

## Responsive Testing Checklist

| Viewport | Width | Key Checks |
|---|---|---|
| iPhone SE | 375px | Mobile layout, hamburger menu, single column grids, player fullscreen |
| iPhone 14 | 390px | Standard mobile, touch targets, text readability |
| iPad Mini | 768px | Tablet layout, 2-column grids, sidebar visible (dashboard) |
| iPad Pro | 1024px | Transition to desktop layout, full navigation visible |
| Laptop | 1280px | Full desktop layout, 3-column grids, max-width constraints |
| Desktop | 1440px | Full-width experience, all features visible |
| Ultra-wide | 1920px+ | Content remains centered within 1440px max-width |

---

## Key Responsive Rules

1. **Mobile-first**: Write base styles for mobile, add `sm:`, `md:`, `lg:` prefixes for larger screens.
2. **Never hide critical content on mobile** — reflow it, stack it, or make it scrollable.
3. **Touch targets minimum 44x44px** — use `p-2.5` or `p-3` on icon buttons.
4. **Text never smaller than `text-xs` (12px)** — even badges and metadata stay readable.
5. **Images are always responsive** — use `object-cover` with aspect-ratio containers.
6. **Tables always have `overflow-x-auto`** — prevents horizontal page scroll on mobile.
7. **The sidebar is always hidden on mobile** — toggled with AlpineJS `sidebarOpen` state.
8. **The sticky player adapts** — compact bar on mobile, expanded bar on desktop, fullscreen overlay as optional on mobile.
9. **Horizontal padding scales**: `px-4` → `sm:px-6` → `lg:px-8` — maintains comfortable margins.
10. **Max-width is enforced at every level** — `1440px` for site, `1280px` for content — no exceptions.
