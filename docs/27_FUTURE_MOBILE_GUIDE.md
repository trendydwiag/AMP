# 27 — Future Mobile Guide

This document outlines considerations for a future Kabulhaden mobile app, PWA implementation, and responsive design improvements. The current codebase is a server-rendered Django application with Tailwind CSS responsive utilities.

---

## PWA Strategy

### Service Worker

```javascript
// static/js/sw.js
const CACHE_NAME = 'kabulhaden-v1';
const STATIC_ASSETS = [
  '/',
  '/static/css/styles.css',
  '/static/js/app.js',
  '/offline/',
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => cache.addAll(STATIC_ASSETS))
  );
});

self.addEventListener('fetch', (event) => {
  event.respondWith(
    caches.match(event.request).then((response) => {
      return response || fetch(event.request).catch(() => {
        return caches.match('/offline/');
      });
    })
  );
});
```

### Web App Manifest

```json
{
  "name": "Kabulhaden Radio",
  "short_name": "Kabulhaden",
  "description": "Dengarkan Kabulhaden Radio live",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#FAF7F3",
  "theme_color": "#8C5A3C",
  "icons": [
    {
      "src": "/static/img/icons/icon-192.png",
      "sizes": "192x192",
      "type": "image/png"
    },
    {
      "src": "/static/img/icons/icon-512.png",
      "sizes": "512x512",
      "type": "image/png"
    }
  ]
}
```

### PWA Meta Tags (in base.html)

```html
<link rel="manifest" href="{% static 'manifest.json' %}">
<meta name="theme-color" content="#8C5A3C">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
```

---

## Responsive Breakpoints

### Current Tailwind Breakpoints

| Prefix | Min Width | Target |
|---|---|---|
| (none) | 0px | Mobile phones |
| `sm:` | 640px | Large phones / small tablets |
| `md:` | 768px | Tablets |
| `lg:` | 1024px | Small laptops |
| `xl:` | 1280px | Desktops |

### Key Responsive Patterns

#### Navbar

```html
<!-- Desktop: center nav links visible -->
<div class="hidden lg:flex items-center gap-1 absolute left-1/2 -translate-x-1/2">
  <!-- Nav links -->
</div>

<!-- Mobile: hamburger toggle visible -->
<button @click="mobileMenuOpen = !mobileMenuOpen" class="lg:hidden ...">
```

**Reference:** `templates/website/components/navbar.html:19`, `templates/website/components/navbar.html:101`

#### Dashboard Sidebar

```html
<!-- Desktop: sidebar always visible -->
<aside class="w-64 fixed inset-y-0 left-0 md:relative md:translate-x-0 ...">

<!-- Mobile: sidebar hidden, toggled via hamburger -->
<button @click="sidebarOpen = !sidebarOpen" class="md:hidden ...">
```

**Reference:** `templates/dashboard_base.html:66`

#### Content Padding

```html
<main class="flex-1 min-w-0 flex flex-col p-4 sm:p-6 lg:p-8">
```

| Breakpoint | Padding |
|---|---|
| Mobile | `p-4` (16px) |
| Tablet | `sm:p-6` (24px) |
| Desktop | `lg:p-8` (32px) |

#### Grid Layouts

```html
<!-- 2-column responsive -->
<div class="grid grid-cols-1 sm:grid-cols-2 gap-6">

<!-- 3-column responsive -->
<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">

<!-- 4-column responsive -->
<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">

<!-- Media manager grid -->
<div class="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-4">
```

---

## Touch Targets

### Minimum Touch Target Size

WCAG 2.1 recommends minimum 44x44px touch targets.

```html
<!-- Good: 44x44px minimum -->
<button class="p-2.5 rounded-xl min-w-[44px] min-h-[44px] ...">
  <!-- icon -->
</button>

<!-- Nav links with sufficient padding -->
<a class="px-4 py-2.5 rounded-xl text-sm ...">
```

### Touch Target Audit

| Element | Current Size | Meets 44px? | Notes |
|---|---|---|---|
| Nav links | `px-4 py-2` | Yes (32px height + padding) | Adequate |
| Ghost buttons | `p-2.5` | ~40px | Close enough |
| Search button | `p-2.5` | ~40px | Close enough |
| Hamburger | `p-2.5` | ~40px | Close enough |
| Table actions | `text-sm` | No (text only) | Needs padding |

### Touch-Friendly Table Actions

```html
<!-- Current (needs improvement) -->
<a href="#" class="text-blue-600 text-sm">Edit</a>

<!-- Improved for touch -->
<a href="#" class="inline-flex items-center px-3 py-1.5 text-sm text-blue-600
                  hover:bg-blue-50 rounded-lg min-h-[44px]">Edit</a>
```

---

## Mobile Navigation Patterns

### Current Mobile Menu

The public site uses a collapsible menu below the navbar.

```html
<div x-show="mobileMenuOpen" class="lg:hidden border-t border-coffee-200 py-3 space-y-1">
  <a href="{% url 'website:home' %}"
     class="block px-4 py-2.5 rounded-xl text-sm font-medium text-coffee-700
            hover:bg-coffee-50 transition-colors">
    Beranda
  </a>
  <!-- ... other links ... -->
  <div class="pt-2 px-4">
    <a href="{% url 'website:radio_live' %}"
       class="flex items-center justify-center gap-2 w-full py-3 rounded-xl
              bg-coffee-400 text-white font-heading font-semibold text-sm">
      DENGARKAN LIVE
    </a>
  </div>
</div>
```

**Reference:** `templates/website/components/navbar.html:112-126`

### Dashboard Mobile Sidebar

The admin sidebar slides in from the left on mobile.

```html
<aside :class="sidebarOpen ? 'translate-x-0' : '-translate-x-full'"
       class="w-64 fixed inset-y-0 left-0 md:relative md:translate-x-0
              transform transition-transform duration-200 ease-in-out z-40">
```

**Reference:** `templates/dashboard_base.html:66`

### Bottom Tab Navigation (Future)

For a mobile app or enhanced PWA, consider a bottom tab bar:

```html
<!-- Mobile bottom nav (future) -->
<nav class="fixed bottom-0 inset-x-0 bg-white border-t border-slate-200 z-50 lg:hidden">
  <div class="flex items-center justify-around h-16">
    <a href="/" class="flex flex-col items-center gap-1 text-coffee-400">
      <svg class="w-6 h-6"><!-- home icon --></svg>
      <span class="text-[10px] font-medium">Beranda</span>
    </a>
    <a href="/jadwal/" class="flex flex-col items-center gap-1 text-slate-400">
      <svg class="w-6 h-6"><!-- schedule icon --></svg>
      <span class="text-[10px] font-medium">Jadwal</span>
    </a>
    <a href="/radio/" class="flex flex-col items-center gap-1 text-slate-400
                             relative -mt-4">
      <div class="w-14 h-14 rounded-full bg-coffee-400 flex items-center justify-center shadow-lg">
        <svg class="w-7 h-7 text-white"><!-- play icon --></svg>
      </div>
    </a>
    <a href="/podcast/" class="flex flex-col items-center gap-1 text-slate-400">
      <svg class="w-6 h-6"><!-- podcast icon --></svg>
      <span class="text-[10px] font-medium">Podcast</span>
    </a>
    <a href="/komunitas/" class="flex flex-col items-center gap-1 text-slate-400">
      <svg class="w-6 h-6"><!-- community icon --></svg>
      <span class="text-[10px] font-medium">Komunitas</span>
    </a>
  </div>
</nav>
```

---

## Offline Support

### Offline Page

```html
<!-- templates/offline.html -->
{% extends 'base.html' %}
{% block title %}Offline | {{ SITE_NAME }}{% endblock %}
{% block layout %}
<div class="min-h-screen flex items-center justify-center px-4">
  <div class="text-center space-y-4">
    <svg class="w-16 h-16 mx-auto text-coffee-300" fill="none" viewBox="0 0 24 24"
         stroke="currentColor" stroke-width="1.5">
      <path stroke-linecap="round" stroke-linejoin="round"
            d="M18.364 5.636a9 9 0 010 12.728m-2.829-2.829a5 5 0 000-7.07m-4.243 2.122a1.5 1.5 0 112.121 2.121 1.5 1.5 0 01-2.121-2.121z" />
    </svg>
    <h1 class="text-2xl font-heading font-bold text-coffee-700">Anda Offline</h1>
    <p class="text-[#666666]">
      Koneksi internet tidak tersedia. Silakan periksa koneksi Anda.
    </p>
    <button onclick="location.reload()"
            class="px-6 py-3 bg-coffee-400 text-white rounded-xl font-heading font-semibold text-sm
                   hover:bg-coffee-500 transition-all">
      Coba Lagi
    </button>
  </div>
</div>
{% endblock %}
```

### Cached Content Strategy

| Content | Cache Strategy | Priority |
|---|---|---|
| HTML pages | Network-first, fallback to cache | High |
| CSS/JS | Cache-first | High |
| Images | Cache-first | Medium |
| API responses | Network-first | Medium |
| Radio stream | Network only (cannot cache) | N/A |

---

## Mobile-Specific UI Concerns

### Viewport Meta

```html
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0">
```

### Responsive Typography

| Element | Mobile | Tablet | Desktop |
|---|---|---|---|
| Page title | `text-2xl` | `text-3xl` | `text-4xl` |
| Section heading | `text-xl` | `text-2xl` | `text-3xl` |
| Body text | `text-sm` | `text-base` | `text-base` |
| Nav links | `text-sm` | `text-sm` | `text-sm` |

### Horizontal Overflow Prevention

```html
<!-- Prevent table overflow on mobile -->
<div class="overflow-x-auto">
  <table class="min-w-full ...">
```

### Sticky Player on Mobile

The sticky audio player needs special handling for small screens.

```html
<!-- Desktop player -->
<div class="hidden lg:block fixed bottom-0 inset-x-0 z-50 shadow-player">
  <!-- Full player UI -->
</div>

<!-- Mobile player (compact) -->
<div class="lg:hidden fixed bottom-0 inset-x-0 z-[100] shadow-player">
  <!-- Simplified player UI -->
</div>
```

---

## Future Mobile App Considerations

### Framework Options

| Approach | Pros | Cons |
|---|---|---|
| PWA (current) | No app store needed, shares codebase | Limited offline, no push notifications on iOS |
| React Native | Native performance, shared logic | Separate codebase, maintenance overhead |
| Flutter | Cross-platform, fast rendering | Dart learning curve, larger app size |
| Capacitor/Cordova | Wrap existing PWA, native APIs | WebView performance, plugin dependency |

### Recommended Path

1. **Phase 1:** Implement PWA with service worker and offline support
2. **Phase 2:** Add push notifications via Web Push API
3. **Phase 3:** Evaluate Capacitor for native app wrapping if needed
4. **Phase 4:** Consider React Native only if native features are required

### Key Features for Mobile

| Feature | PWA | Native App |
|---|---|---|
| Live radio streaming | Yes | Yes |
| Podcast playback | Yes | Yes |
| Push notifications | Limited (iOS) | Full support |
| Offline podcast download | Yes (service worker) | Yes |
| Background audio | Limited | Yes |
| Share to social | Yes | Yes |
| Camera (user avatar) | Yes | Yes |
| Geolocation (schedule) | Yes | Yes |
