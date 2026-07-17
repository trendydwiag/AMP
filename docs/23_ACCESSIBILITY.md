# 23 — Accessibility

Kabulhaden CMS follows WCAG 2.1 guidelines where applicable. This document covers focus states, ARIA labels, color contrast, keyboard navigation, and screen reader support.

---

## Focus States

### Standard Focus Ring

All interactive elements use a visible focus ring for keyboard users.

```html
<!-- Button focus -->
<button class="focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-brand-500">
  Masuk
</button>

<!-- Input focus -->
<input class="focus:ring-2 focus:ring-blue-500 focus:border-blue-500">

<!-- Link focus (via Tailwind) -->
<a class="focus:outline-none focus:ring-2 focus:ring-coffee-400 focus:ring-offset-2 rounded-xl">
```

**Reference:** `apps/users/templates/users/login.html:55`

### Focus Ring Colors

| Context | Focus Ring Color | Tailwind Class |
|---|---|---|
| Brand buttons | brand-500 (blue) | `focus:ring-brand-500` |
| Form inputs | blue-500 | `focus:ring-blue-500` |
| Coffee elements | coffee-400 | `focus:ring-coffee-400` |
| Error states | red-500 | `focus:ring-red-500` |

### Focus Offset

All focus rings use `focus:ring-offset-2` to create space between the element and the ring, improving visibility.

---

## ARIA Labels

### Landmark Roles

```html
<!-- Banner (navbar) -->
<header role="banner">

<!-- Main content -->
<main>

<!-- Navigation -->
<nav aria-label="Navigasi utama">
<nav aria-label="Breadcrumb">
```

**Reference:** `templates/website/components/navbar.html:2`, `templates/dashboard_base.html:125`

### Button ARIA Labels

```html
<!-- Search button -->
<button aria-label="Cari">

<!-- Mobile menu toggle -->
<button aria-label="Toggle menu navigasi"
        :aria-expanded="mobileMenuOpen">

<!-- Sidebar toggle (dashboard) -->
<button aria-label="Toggle sidebar">

<!-- Dark mode toggle -->
<button title="Ubah Tema">
```

**Reference:** `templates/website/components/navbar.html:89`, `templates/dashboard_base.html:26`

### Modal ARIA

```html
<div role="dialog" aria-modal="true" aria-label="Cari">
```

**Reference:** `templates/website/components/search_modal.html:2`

### Form Labels

```html
<!-- Explicit label with for attribute -->
<label for="id_username" class="block text-sm font-medium text-slate-700 mb-1">
  Username
</label>
<input type="text" id="id_username" name="username">

<!-- Implicit label (wrapping) -->
<label class="flex items-center gap-2">
  {{ form.remember_me }}
  <span class="text-sm text-slate-600">Ingat saya</span>
</label>
```

**Reference:** `apps/users/templates/users/login.html:30`, `apps/users/templates/users/login.html:46`

### Form Field Errors (aria-describedby pattern)

```html
<div>
  <label for="id_password" class="block text-sm font-medium text-slate-700 mb-1">
    Password
  </label>
  {{ form.password }}
  {% if form.password.errors %}
  <p class="mt-1 text-xs text-red-600" role="alert">{{ form.password.errors.0 }}</p>
  {% endif %}
</div>
```

### Icon-Only Buttons (screen reader text)

```html
<!-- Search icon button -->
<button aria-label="Cari">
  <svg class="w-5 h-5"><!-- search icon --></svg>
</button>

<!-- Mobile hamburger -->
<button aria-label="Toggle menu navigasi">
  <svg class="w-6 h-6"><!-- hamburger icon --></svg>
</button>
```

**Reference:** `templates/website/components/navbar.html:89`, `templates/website/components/navbar.html:101`

---

## Color Contrast

### Text on Backgrounds

| Text Color | Background | Contrast Ratio | WCAG AA |
|---|---|---|---|
| `#2D2D2D` | `#FAF7F3` | ~10:1 | Pass (AAA) |
| `#666666` | `#FAF7F3` | ~5.5:1 | Pass (AA) |
| `coffee-700` (#3A2318) | white | ~8:1 | Pass (AAA) |
| `coffee-400` (#8C5A3C) | white | ~4.5:1 | Pass (AA) |
| `slate-500` | white | ~4.6:1 | Pass (AA) |
| `white` | `coffee-400` (#8C5A3C) | ~4.5:1 | Pass (AA) |

### Interactive Elements

| Element | Color Combination | Notes |
|---|---|---|
| Primary CTA | white on coffee-400 | 4.5:1 ratio, meets AA |
| Nav links | `#666666` on white | 5.5:1, meets AA |
| Hover states | coffee-600 on coffee-50 | Dark on light, good contrast |
| Error text | red-600 on white | 5:1, meets AA |
| Success text | green-700 on white | 4.5:1, meets AA |

---

## Keyboard Navigation

### Tab Order

Interactive elements follow DOM order:
1. Logo → home link
2. Navigation links (left to right)
3. Search button
4. CTA button (DENGARKAN LIVE)
5. Mobile menu toggle
6. Content links and forms

### Keyboard Shortcuts

```html
<!-- ⌘K for search -->
<kbd class="hidden lg:inline-flex items-center px-1.5 py-0.5 text-[10px] font-mono
            text-coffee-300 bg-coffee-50 border border-coffee-200 rounded">
  ⌘K
</kbd>
```

**Reference:** `templates/website/components/navbar.html:94`

### Escape Key (Modal Dismiss)

```html
<!-- Search modal closes on ESC -->
<div @keydown.escape.window="toggleSearch()">
```

### Focus Trap (Modals)

For accessible modals, focus should be trapped within the modal.

```html
<div x-show="isOpen"
     x-trap.noscroll="isOpen"
     @keydown.escape.window="isOpen = false">
```

Requires `@alpinejs/trap` plugin.

---

## Screen Reader Support

### Skip to Content

Add a skip link at the top of `base.html`:

```html
<a href="#main-content"
   class="sr-only focus:not-sr-only focus:absolute focus:top-4 focus:left-4
          focus:z-50 focus:px-4 focus:py-2 focus:bg-coffee-400 focus:text-white
          focus:rounded-lg focus:text-sm focus:font-semibold">
  Lewati ke konten utama
</a>

<!-- In main content area -->
<main id="main-content">
```

### Visually Hidden Text

```html
<span class="sr-only">Toggle menu navigasi</span>
```

### Meaningful SVG Icons

```html
<!-- Decorative icon (hidden from screen readers) -->
<svg class="w-5 h-5" aria-hidden="true" fill="none" viewBox="0 0 24 24" stroke="currentColor">
  <!-- icon path -->
</svg>

<!-- Meaningful icon with adjacent text -->
<a href="#" aria-label="Cari">
  <svg class="w-5 h-5" aria-hidden="true"><!-- search icon --></svg>
</a>
```

---

## Semantic HTML

### Document Structure

```html
<!DOCTYPE html>
<html lang="id">  <!-- Indonesian language -->
<head>...</head>
<body>
  <header role="banner">...</header>
  <nav aria-label="...">...</nav>
  <main>...</main>
  <footer>...</footer>
</body>
</html>
```

**Reference:** `templates/base.html:3-4`

### Heading Hierarchy

Each page follows a logical heading order:

```html
<h1>Page Title</h1>          <!-- One per page -->
  <h2>Section Title</h2>     <!-- Major sections -->
    <h3>Subsection</h3>      <!-- Sub-sections -->
```

### Lists

Navigation items use `<nav>` with `<ol>` or `<ul>`:

```html
<nav aria-label="Breadcrumb">
  <ol class="inline-flex items-center space-x-1 md:space-x-3">
    <li>...</li>
    <li>...</li>
  </ol>
</nav>
```

**Reference:** `templates/dashboard_base.html:126`

### Tables

Data tables use proper `<thead>` and `<tbody>`:

```html
<table class="min-w-full divide-y divide-slate-200">
  <thead class="bg-slate-50">
    <tr>
      <th scope="col" class="px-4 py-3 text-left text-xs font-medium uppercase">
        Column Header
      </th>
    </tr>
  </thead>
  <tbody class="divide-y divide-slate-200">
    <tr>...</tr>
  </tbody>
</table>
```

---

## Form Accessibility

### Required Fields

```html
<label for="id_email">
  Email
  <span class="text-red-500" aria-hidden="true">*</span>
</label>
<input type="email" id="id_email" required aria-required="true">
```

### Error Association

```html
<input type="email" id="id_email" aria-describedby="email-error" aria-invalid="true">
<p id="email-error" class="text-sm text-red-600" role="alert">
  Masukkan alamat email yang valid.
</p>
```

---

## Accessibility Checklist

- [ ] All images have meaningful `alt` text
- [ ] All form inputs have associated `<label>` elements
- [ ] All interactive elements are keyboard accessible
- [ ] Focus is visible on all focusable elements
- [ ] Color is not the only way to convey information
- [ ] ARIA landmarks are used (`nav`, `main`, `header`)
- [ ] Heading hierarchy is logical (h1 → h2 → h3)
- [ ] Modal dialogs trap focus
- [ ] Error messages are associated with form fields
- [ ] `lang="id"` is set on `<html>` element
