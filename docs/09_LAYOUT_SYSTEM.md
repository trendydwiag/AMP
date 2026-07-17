# 09 — Layout System

Kabulhaden CMS uses a consistent layout system across all pages — public website, admin dashboard, and authentication screens — defined through Tailwind CSS utility classes and a few key base templates.

---

## Layout Hierarchy

```
base.html                    ← Root template (fonts, scripts, body)
├── website/main.html        ← Public website layout (navbar + footer)
│   └── website/home.html    ← Individual public pages
├── dashboard_base.html      ← Admin dashboard layout (sidebar + header)
│   └── broadcast/*.html     ← Individual CMS module pages
└── auth_base.html           ← Auth pages layout (centered card)
    └── users/login.html     ← Login, register, password reset
```

---

## Max Width Constraints

| Token | Value | Tailwind Class | Usage |
|---|---|---|---|
| **Site Max** | 1440px | `max-w-site` or `max-w-[1440px]` | Outermost container for the entire site |
| **Content Max** | 1280px | `max-w-content` or `max-w-[1280px]` | Content areas, section inner wrappers |

### Configuration

```javascript
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      maxWidth: {
        'site': '1440px',
        'content': '1280px',
      },
    },
  },
}
```

### Application

```html
<!-- Navbar: spans full 1440px -->
<nav class="max-w-[1440px] mx-auto px-4 sm:px-6 lg:px-8">

<!-- Page content: constrained to 1280px -->
<div class="max-w-[1280px] mx-auto px-4 sm:px-6 lg:px-8">
  <!-- Section content here -->
</div>
```

---

## Section Spacing

Vertical spacing between major page sections uses predefined tokens:

| Token | Value | Tailwind Class | Usage |
|---|---|---|---|
| **Section (Large)** | 96px | `py-section` or `style="padding-top:96px; padding-bottom:96px"` | Major page sections (hero, featured content) |
| **Section (Medium)** | 64px | `py-section-md` | Secondary sections |
| **Section (Small)** | 48px | `py-section-sm` | Compact sections, card groups |

### Configuration

```javascript
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      spacing: {
        'section': '96px',
        'section-md': '64px',
        'section-sm': '48px',
      },
    },
  },
}
```

### Usage Pattern in Homepage

```html
<!-- templates/website/home.html -->

{# SECTION 1: Hero — No extra padding (hero handles its own) #}
{% include 'website/components/home/hero_radio.html' %}

{# SECTION 2: Today's Programs — Large section spacing #}
{% include 'website/components/home/today_programs.html' %}

{# SECTION 3: Weekly Schedule — Medium section spacing #}
{% include 'website/components/home/weekly_schedule.html' %}

{# SECTION 9: Newsletter — Explicit large spacing #}
<section class="max-w-[1280px] mx-auto px-4 sm:px-6 lg:px-8"
         style="padding-top: 96px; padding-bottom: 96px;">
  <!-- Content -->
</section>
```

---

## Border Radius System

| Token | Value | Tailwind Class | Usage |
|---|---|---|---|
| **Card** | 20px | `rounded-card` | Standard cards, form containers |
| **Card Large** | 24px | `rounded-card-lg` | Hero cards, featured sections |
| **Default** | 8px | `rounded-lg` | Buttons, inputs, small containers |
| **Full** | 9999px | `rounded-full` | Avatars, status dots, pills |

---

## Shadow System

| Token | Tailwind Class | Usage |
|---|---|---|
| **Header** | `shadow-header` | Sticky navbar: `0 1px 3px rgba(0,0,0,.06)` |
| **Card** | `shadow-card` | Default card shadow: `0 10px 30px rgba(0,0,0,.08)` |
| **Card Hover** | `shadow-card-hover` | Card hover state: `0 20px 40px rgba(0,0,0,.12)` |
| **Hero Card** | `shadow-hero-card` | Hero sections: `0 30px 60px rgba(0,0,0,.20)` |
| **Player** | `shadow-player` | Sticky bottom player: `0 -4px 20px rgba(0,0,0,.08)` |

---

## Grid System

Kabulhaden uses Tailwind's utility-first grid system rather than a custom grid framework.

### Common Grid Patterns

```html
<!-- 2-column grid (programs, podcasts) -->
<div class="grid grid-cols-1 sm:grid-cols-2 gap-6">

<!-- 3-column grid (news articles, sponsors) -->
<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">

<!-- 4-column grid (featured podcasts) -->
<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">

<!-- Auto-fill responsive grid -->
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">

<!-- Schedule timeline (single column with day tabs) -->
<div class="grid grid-cols-1 lg:grid-cols-7 gap-4">
```

### Navbar Grid

```html
<!-- templates/website/components/navbar.html -->
<div class="flex items-center justify-between h-20">
  <!-- Left: Logo -->
  <div class="flex-shrink-0">...</div>

  <!-- Center: Navigation (absolutely centered) -->
  <div class="hidden lg:flex items-center gap-1 absolute left-1/2 -translate-x-1/2">
    ...
  </div>

  <!-- Right: Actions -->
  <div class="flex items-center gap-3">...</div>
</div>
```

---

## Public Website Layout

### Page Container Structure

```html
<!-- templates/website/main.html (extends base.html) -->
<body class="h-full bg-[#FAF7F3] text-[#2D2D2D] font-body flex flex-col">

  <!-- Sticky Header -->
  {% include 'website/components/navbar.html' %}

  <!-- Main Content -->
  <main class="flex-1">
    {% block content %}{% endblock %}
  </main>

  <!-- Sticky Player Bar (positioned at bottom) -->
  {% include 'website/components/sticky_player.html' %}

  <!-- Footer -->
  {% include 'website/components/footer.html' %}

</body>
```

### Standard Section Pattern

```html
<section class="max-w-[1280px] mx-auto px-4 sm:px-6 lg:px-8 py-section">
  <!-- Section Header -->
  <div class="text-center mb-12">
    <span class="text-xs font-heading font-semibold text-coffee-300 uppercase tracking-wider">
      Section Label
    </span>
    <h2 class="text-3xl md:text-4xl font-heading font-bold text-coffee-700 mt-3">
      Section Title
    </h2>
  </div>

  <!-- Section Content (grid) -->
  <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
    <!-- Cards -->
  </div>
</section>
```

---

## Admin Dashboard Layout

### Sidebar + Main Content Structure

```html
<!-- templates/dashboard_base.html -->
<div class="min-h-screen flex flex-col">

  <!-- Top Header Bar -->
  <header class="bg-white dark:bg-slate-800 border-b h-16 sticky top-0 z-30">
    <!-- Mobile toggle | Logo | Dark mode | User menu -->
  </header>

  <div class="flex-1 flex flex-row">

    <!-- Sidebar (264px fixed width) -->
    <aside class="w-64 fixed inset-y-0 left-0 md:relative
                  pt-16 md:pt-0
                  -translate-x-full md:translate-x-0
                  transition-transform duration-200">
      <div class="p-4 space-y-4">
        <!-- Navigation links -->
      </div>
    </aside>

    <!-- Main Content Area -->
    <main class="flex-1 min-w-0 p-4 sm:p-6 lg:p-8">
      <!-- Breadcrumbs -->
      <nav class="mb-4">...</nav>

      <!-- Flash Messages -->
      <div class="mb-6 space-y-2">...</div>

      <!-- Content Card -->
      <div class="bg-white dark:bg-slate-800 rounded-xl shadow-sm
                  border p-6">
        {% block content %}{% endblock %}
      </div>

      <!-- Footer -->
      <footer class="mt-8 text-center text-xs text-slate-400">...</footer>
    </main>

  </div>
</div>
```

### Sidebar Dimensions

| Property | Value |
|---|---|
| Width | 264px (`w-64`) |
| Position | Fixed (mobile), Relative (desktop) |
| Z-index | 40 |
| Top offset | 64px (`pt-16`) to clear header |
| Transition | `transform 200ms ease-in-out` |
| Overflow | `overflow-y-auto` for scrollable nav |

---

## Auth Pages Layout

```html
<!-- templates/auth_base.html -->
<div class="min-h-screen flex flex-col justify-center py-12 sm:px-6 lg:px-8
            bg-slate-100 dark:bg-slate-900">

  <!-- Brand -->
  <div class="sm:mx-auto sm:w-full sm:max-w-md text-center">
    <a class="text-3xl font-extrabold text-brand-500">Kabulhaden CMS</a>
    <h2 class="mt-6 text-2xl font-bold tracking-tight">
      {% block auth_title %}{% endblock %}
    </h2>
  </div>

  <!-- Form Card -->
  <div class="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
    <div class="bg-white dark:bg-slate-800 py-8 px-4 shadow sm:rounded-xl sm:px-10">
      {% block auth_content %}{% endblock %}
    </div>
  </div>

</div>
```

### Auth Card Dimensions

| Property | Value |
|---|---|
| Max width | 448px (`sm:max-w-md`) |
| Border radius | 12px (`sm:rounded-xl`) |
| Padding | 32px (`py-8 px-4 sm:px-10`) |
| Shadow | Default shadow |
| Background | White / dark:slate-800 |

---

## Transition System

| Element | Duration | Easing | Tailwind Class |
|---|---|---|---|
| Color transitions | 250ms | ease | `transition-colors duration-250` |
| Sidebar slide | 200ms | ease-in-out | `transition-transform duration-200 ease-in-out` |
| Dropdown menus | 200ms | ease-out (in) / ease-in (out) | `transition ease-out duration-200` |
| Card hover | 250ms | default | `transition-all` |
| Button press | — | — | `active:scale-[.98]` |

---

## Layout Rules

1. **1440px is the maximum site width** — nothing should extend beyond this on any screen size.
2. **1280px is the content width** — all section content is constrained within this.
3. **Horizontal padding scales**: `px-4` (mobile) → `px-6` (tablet) → `px-8` (desktop).
4. **Sidebar is hidden on mobile** — toggled via hamburger button with `translate-x` animation.
5. **The sticky player sits above the footer but below the sidebar** — `z-index` layering: header (30) < sidebar (40) < player (50) < mobile player (100).
6. **All content sections use the same max-width + mx-auto pattern** — ensures consistent alignment.
7. **Cards use `rounded-card` (20px) consistently** — never mix card border radii within the same module.
