# 21 — Icons and Illustrations

Kabulhaden CMS uses inline SVG icons throughout the interface. Icons are rendered directly in templates without an external icon library, using consistent sizing and alignment patterns.

---

## Inline SVG Icons

All icons are inline SVGs with `fill="none"`, `viewBox="0 0 24 24"`, and `stroke="currentColor"`.

### Base Pattern

```html
<svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
  <path stroke-linecap="round" stroke-linejoin="round"
        d="ICON_PATH_DATA" />
</svg>
```

---

## Icon Sizes

| Size | Classes | Pixels | Usage |
|---|---|---|---|
| XS | `w-4 h-4` | 16px | Inline breadcrumbs, close buttons |
| SM | `w-5 h-5` | 20px | Nav links, sidebar items, buttons |
| MD | `w-6 h-6` | 24px | Mobile hamburger, header actions |
| LG | `w-8 h-8` | 32px | Empty state icons, large CTAs |
| XL | `h-12 w-12` | 48px | Upload zone illustration |

### Stroke Width

| Context | `stroke-width` |
|---|---|
| Standard icons | `2` |
| Thin/decorative | `1.5` |
| Bold/emphasis | `2` |

---

## Icon + Text Alignment

### Horizontal (inline)

```html
<!-- Button with icon -->
<a href="{% url 'website:radio_live' %}"
   class="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-coffee-400 text-white
          font-heading font-semibold text-sm">
  <span class="w-2 h-2 bg-white rounded-full animate-pulse"></span>
  DENGARKAN LIVE
</a>

<!-- Nav link with icon -->
<a href="{% url 'radio:dashboard' %}"
   class="flex items-center gap-3 px-3 py-2 rounded-lg ...">
  <svg class="h-5 w-5"><!-- icon --></svg>
  Radio Engine
</a>
```

**Reference:** `templates/website/components/navbar.html:96`, `templates/dashboard_base.html:80`

### Vertical (stacked)

```.html
<!-- Empty state -->
<div class="flex flex-col items-center justify-center">
  <svg class="w-8 h-8 text-coffee-300"><!-- icon --></svg>
  <h3 class="text-lg font-heading font-semibold mt-4">Title</h3>
  <p class="text-sm text-slate-500 mt-1">Description</p>
</div>
```

### Icon in Dropdown Item

```html
<a href="#" class="flex items-start gap-3 p-2.5 rounded-xl hover:bg-coffee-50 transition-colors group">
  <div class="w-10 h-10 rounded-xl bg-coffee-100 flex items-center justify-center flex-shrink-0
              group-hover:bg-coffee-200 transition-colors">
    <svg class="w-5 h-5 text-coffee-500"><!-- icon --></svg>
  </div>
  <div>
    <p class="text-sm font-medium text-coffee-700 group-hover:text-coffee-600 transition-colors">
      Link Title
    </p>
    <p class="text-xs text-[#666666]">Description text</p>
  </div>
</a>
```

**Reference:** `templates/website/components/navbar.html:34-42`

---

## Common Icons Reference

### Navigation

| Icon | Purpose | SVG Path |
|---|---|---|
| Home | Dashboard/Home link | `M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6` |
| Search | Global search | `M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z` |
| Hamburger | Mobile menu | `M4 6h16M4 12h16M4 18h16` |
| Close (X) | Close modal/menu | `M6 18L18 6M6 6l12 12` |
| Chevron Down | Dropdown toggle | `M19 9l-7 7-7-7` |
| Chevron Right | Breadcrumb separator | `M9 5l7 7-7 7` |

### Media & Broadcasting

| Icon | Purpose | SVG Path |
|---|---|---|
| Radio/Broadcast | Radio stations, programs | `M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z` |
| Live | Live indicator | `M5.636 18.364a9 9 0 010-12.728m12.728 0a9 9 0 010 12.728m-9.9-2.829a5 5 0 010-7.07m7.072 0a5 5 0 010 7.07M13 12a1 1 0 11-2 0 1 1 0 012 0z` |
| Music Note | Logo, audio content | `M9 19V6l12-3v13M9 19c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zm12-3c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zM9 10l12-3` |
| Upload | File upload | `M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12` |
| Image | Media files, photos | `M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z` |

### Users & Admin

| Icon | Purpose | SVG Path |
|---|---|---|
| Users | User management | `M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z` |
| Settings (gear) | Django Admin | `M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.066 2.573c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.573 1.066c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.066-2.573c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z M15 12a3 3 0 11-6 0 3 3 0 016 0z` |

### Theme

| Icon | Purpose | SVG Path |
|---|---|---|
| Moon | Dark mode toggle | `M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z` |
| Sun | Light mode toggle | `M12 3v1m0 16v1m9-9h-1M4 12H3m15.364-6.364l-.707.707M6.343 17.657l-.707.707m0-12.728l.707.707m12.728 12.728l.707.707M12 8a4 4 0 100 8 4 4 0 000-8z` |

### Calendar & Time

| Icon | Purpose | SVG Path |
|---|---|---|
| Calendar | Schedule | `M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z` |

### Content

| Icon | Purpose | SVG Path |
|---|---|---|
| Newspaper | News articles | `M19 20H5a2 2 0 01-2-2V6a2 2 0 012-2h10a2 2 0 012 2v1m2 13a2 2 0 01-2-2V7m2 13a2 2 0 002-2V9a2 2 0 00-2-2h-2m-4-3H9M7 16h6M7 8h6v4H7V8z` |

---

## Icon Color Context

| Context | Color | Tailwind Class |
|---|---|---|
| Default | Slate | `text-slate-400` / `text-slate-500` |
| Active link | Coffee | `text-coffee-500` / `text-coffee-400` |
| Brand link | Blue | `text-brand-500` / `text-blue-400` |
| Live indicator | Red | `text-live` / `text-red-500` |
| Success | Green | `text-green-500` |
| Error | Red | `text-red-500` |
| Muted placeholder | Light slate | `text-gray-400` |

---

## Illustration Style (Empty States)

Empty states use a circular icon container as a minimal illustration.

```html
<!-- Circle container -->
<div class="w-16 h-16 rounded-full bg-coffee-50 flex items-center justify-center mb-4">
  <svg class="w-8 h-8 text-coffee-300" fill="none" viewBox="0 0 24 24"
       stroke="currentColor" stroke-width="1.5">
    <!-- Context icon -->
  </svg>
</div>
```

| Property | Value |
|---|---|
| Circle size | `w-16 h-16` (64px) |
| Circle bg | `bg-coffee-50` |
| Circle shape | `rounded-full` |
| Icon size | `w-8 h-8` (32px) |
| Icon color | `text-coffee-300` |
| Stroke width | `1.5` (lighter for illustration feel) |

---

## Logo Icon

The Kabulhaden logo icon uses a music note in a coffee-colored rounded square.

```html
<div class="w-10 h-10 rounded-xl bg-coffee-600 flex items-center justify-center shadow-md
            group-hover:shadow-lg transition-shadow">
  <svg class="w-5 h-5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor"
       stroke-width="2">
    <path stroke-linecap="round" stroke-linejoin="round"
          d="M9 19V6l12-3v13M9 19c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zm12-3c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zM9 10l12-3" />
  </svg>
</div>
```

**Reference:** `templates/website/components/navbar.html:9-12`
