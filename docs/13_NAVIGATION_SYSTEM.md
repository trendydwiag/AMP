# 13 — Navigation System

Kabulhaden CMS has three distinct navigation systems: the public navbar, the admin sidebar, and breadcrumb trails. Each serves a specific context and follows the project's design tokens.

---

## 1. Public Navbar

**Template:** `templates/website/components/navbar.html`  
**Height:** 80px  
**Position:** Sticky top (`sticky top-0 z-50`)  
**Background:** White (`bg-white`)  
**Shadow:** `shadow-header`  
**Max width:** 1440px (`max-w-[1440px] mx-auto`)

### Layout Structure

```
┌────────────────────────────────────────────────────────────┐
│ max-w-[1440px] mx-auto px-4 sm:px-6 lg:px-8               │
│ ┌──────────┬─────────────────────┬────────────────────┐    │
│ │ Logo     │  Nav links (center) │  Actions (right)   │    │
│ │ Kabulhaden│  Beranda Program.. │  🔍 ⌘K [LIVE] ☰   │    │
│ └──────────┴─────────────────────┴────────────────────┘    │
├────────────────────────────────────────────────────────────┤
│ Mobile Menu (x-show, hidden on lg:)                        │
│ Beranda / Program / Jadwal / Podcast / Berita / Komunitas  │
│ [DENGARKAN LIVE button]                                     │
└────────────────────────────────────────────────────────────┘
```

### Logo

```html
<div class="flex-shrink-0">
  <a href="{% url 'website:home' %}" class="flex items-center gap-2.5 group"
     aria-label="{{ SITE_NAME }} - Beranda">
    <div class="w-10 h-10 rounded-xl bg-coffee-600 flex items-center justify-center
                shadow-md group-hover:shadow-lg transition-shadow">
      <svg class="w-5 h-5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor"
           stroke-width="2">
        <!-- Music note icon -->
      </svg>
    </div>
    <span class="text-xl font-heading font-bold text-coffee-700 hidden sm:block">
      Kabulhaden
    </span>
  </a>
</div>
```

**Reference:** `templates/website/components/navbar.html:7-16`

### Desktop Navigation (center-aligned)

Links are absolutely centered within the navbar using `absolute left-1/2 -translate-x-1/2`.

```html
<div class="hidden lg:flex items-center gap-1 absolute left-1/2 -translate-x-1/2">
  <a href="{% url 'website:home' %}"
     class="px-4 py-2 rounded-xl text-sm font-body font-medium text-[#666666]
            hover:text-coffee-600 hover:bg-coffee-50 transition-colors">
    Beranda
  </a>
  <!-- Program dropdown, Jadwal, Podcast, Berita, Komunitas -->
</div>
```

**Reference:** `templates/website/components/navbar.html:19`

### Dropdown Navigation (Programs)

Mega-dropdown with Alpine.js hover activation.

```html
<div class="relative" x-data="{ open: false }"
     @mouseenter="open = true" @mouseleave="open = false">
  <a href="{% url 'website:program_list' %}" @click="open = !open"
     class="flex items-center gap-1 px-4 py-2 rounded-xl text-sm font-body font-medium
            text-[#666666] hover:text-coffee-600 hover:bg-coffee-50 transition-colors">
    Program
    <svg class="w-4 h-4 transition-transform" :class="open && 'rotate-180'"
         fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
      <path stroke-linecap="round" stroke-linejoin="round" d="M19 9l-7 7-7-7" />
    </svg>
  </a>
  <div x-show="open"
       x-transition:enter="transition ease-out duration-200"
       x-transition:enter-start="opacity-0 translate-y-1"
       x-transition:enter-end="opacity-100 translate-y-0"
       x-transition:leave="transition ease-in duration-150"
       x-transition:leave-start="opacity-100 translate-y-0"
       x-transition:leave-end="opacity-0 translate-y-1"
       class="absolute left-0 mt-1 w-[560px] bg-white rounded-2xl shadow-card-hover
              border border-coffee-200 p-6 z-50"
       style="display: none;"
       @click.away="open = false">
    <div class="grid grid-cols-2 gap-4">
      <!-- Column 1: Program Unggulan -->
      <!-- Column 2: Jadwal & Siaran -->
    </div>
  </div>
</div>
```

**Reference:** `templates/website/components/navbar.html:22-79`

### Actions Section (right-aligned)

```html
<div class="flex items-center gap-3">
  <!-- Search button -->
  <button onclick="toggleSearch()" class="p-2.5 rounded-xl text-[#666666]
          hover:text-coffee-600 hover:bg-coffee-50 transition-colors" aria-label="Cari">
    <!-- search icon -->
  </button>

  <!-- Keyboard shortcut indicator -->
  <kbd class="hidden lg:inline-flex items-center px-1.5 py-0.5 text-[10px] font-mono
              text-coffee-300 bg-coffee-50 border border-coffee-200 rounded">⌘K</kbd>

  <!-- DENGARKAN LIVE CTA -->
  <a href="{% url 'website:radio_live' %}"
     class="hidden sm:inline-flex items-center gap-2 px-5 py-2.5 rounded-xl
            bg-coffee-400 text-white font-heading font-semibold text-sm
            hover:bg-coffee-500 transition-all shadow-md hover:shadow-lg active:scale-[.98]">
    <span class="w-2 h-2 bg-white rounded-full animate-pulse"></span>
    DENGARKAN LIVE
  </a>

  <!-- Mobile hamburger -->
  <button @click="mobileMenuOpen = !mobileMenuOpen"
          class="lg:hidden p-2.5 rounded-xl text-[#666666] hover:text-coffee-600
                 hover:bg-coffee-50 transition-colors"
          :aria-expanded="mobileMenuOpen" aria-label="Toggle menu navigasi">
    <!-- hamburger / close icons swap -->
  </button>
</div>
```

**Reference:** `templates/website/components/navbar.html:88-108`

### Mobile Menu

Collapsible menu visible on screens below `lg` breakpoint.

```html
<div x-show="mobileMenuOpen"
     x-transition:enter="transition ease-out duration-200"
     x-transition:enter-start="opacity-0 -translate-y-2"
     x-transition:enter-end="opacity-100 translate-y-0"
     x-transition:leave="transition ease-in duration-150"
     x-transition:leave-start="opacity-100 translate-y-0"
     x-transition:leave-end="opacity-0 -translate-y-2"
     class="lg:hidden border-t border-coffee-200 py-3 space-y-1"
     style="display: none;">
  <a href="{% url 'website:home' %}"
     class="block px-4 py-2.5 rounded-xl text-sm font-medium text-coffee-700
            hover:bg-coffee-50 hover:text-coffee-600 transition-colors">Beranda</a>
  <!-- ... other links ... -->
  <div class="pt-2 px-4">
    <a href="{% url 'website:radio_live' %}"
       class="flex items-center justify-center gap-2 w-full py-3 rounded-xl
              bg-coffee-400 text-white font-heading font-semibold text-sm
              hover:bg-coffee-500 transition-colors">
      <span class="w-2 h-2 bg-white rounded-full animate-pulse"></span>
      DENGARKAN LIVE
    </a>
  </div>
</div>
```

**Reference:** `templates/website/components/navbar.html:112-126`

---

## 2. Admin Sidebar

**Template:** `templates/dashboard_base.html:66-120`  
**Width:** 256px (`w-64`)  
**Sections:** Dashboard, CMS Modules, Admin (staff-only)

See [12_DASHBOARD_LAYOUT.md](12_DASHBOARD_LAYOUT.md) for the full sidebar specification.

### Sidebar Navigation Items

| Section | Items | URL Pattern |
|---|---|---|
| Home | Dashboard | `core:home` |
| CMS Modules | Radio Engine | `radio:dashboard` |
| CMS Modules | Broadcast Management | `broadcast:dashboard` |
| Admin | Kelola Pengguna | `users:admin_user_list` |
| Admin | Django Admin | `admin:index` |

### Active State Detection

Dashboard sidebar items are currently static (no active state detection for module links). Sub-module sidebars (Settings, Media) use `request.path` or `request.resolver_match.url_name` for active state:

```html
{% if request.resolver_match.url_name == 'dashboard' %}
  bg-blue-50 text-blue-700
{% else %}
  text-gray-700 hover:bg-gray-100
{% endif %}
```

**Reference:** `templates/media_manager/base.html:9`

---

## 3. Breadcrumbs

### Public Breadcrumbs

**Template:** `templates/website/components/breadcrumb.html`

```html
<nav class="flex items-center text-sm text-slate-500 dark:text-slate-400 mb-6"
     aria-label="Breadcrumb">
  <ol class="flex items-center flex-wrap gap-1">
    <li>
      <a href="{% url 'website:home' %}"
         class="flex items-center gap-1 hover:text-brand-500 dark:hover:text-blue-400 transition-colors">
        <svg class="w-4 h-4"><!-- home icon --></svg>
        Beranda
      </a>
    </li>
    {% for crumb in breadcrumbs %}
    <li class="flex items-center gap-1">
      <svg class="w-4 h-4 text-slate-300 dark:text-slate-600 flex-shrink-0"
           fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
        <path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7" />
      </svg>
      {% if crumb.url %}
        <a href="{{ crumb.url }}"
           class="hover:text-brand-500 dark:hover:text-blue-400 transition-colors">
          {{ crumb.label }}
        </a>
      {% else %}
        <span class="text-slate-700 dark:text-slate-300 font-medium">{{ crumb.label }}</span>
      {% endif %}
    </li>
    {% endfor %}
  </ol>
</nav>
```

**Separator:** Chevron-right icon (`M9 5l7 7-7 7`)  
**Last item:** Non-link, bold text (`font-medium text-slate-700`)

### Dashboard Breadcrumbs

Defined inline in each child template via `{% block breadcrumbs %}`.

```html
<!-- templates/broadcast/episode_form.html -->
{% block breadcrumbs %}
<li class="inline-flex items-center">
    <span class="mx-2">/</span>
    <a href="{% url 'broadcast:dashboard' %}" class="hover:text-blue-600">Broadcast</a>
</li>
<li class="inline-flex items-center">
    <span class="mx-2">/</span>
    <a href="{% url 'broadcast:episode_list' %}" class="hover:text-blue-600">Episodes</a>
</li>
<li class="inline-flex items-center">
    <span class="mx-2">/</span>
    <span class="text-slate-700 dark:text-slate-300">
      {% if is_edit %}Edit{% else %}Tambah{% endif %}
    </span>
</li>
{% endblock %}
```

**Reference:** `templates/broadcast/episode_form.html:5-18`

**Separator:** Forward slash (`/`) with `mx-2` spacing  
**Last item:** Non-link, `text-slate-700 dark:text-slate-300`

### Breadcrumb Rendering (dashboard_base.html)

```html
<nav class="flex text-sm text-slate-500 dark:text-slate-400 mb-4" aria-label="Breadcrumb">
  <ol class="inline-flex items-center space-x-1 md:space-x-3">
    <li class="inline-flex items-center">
      <a href="{% url 'core:home' %}" class="inline-flex items-center hover:text-brand-500">
        Home
      </a>
    </li>
    {% block breadcrumbs %}{% endblock %}
  </ol>
</nav>
```

**Reference:** `templates/dashboard_base.html:125-134`

---

## 4. Search Modal

**Template:** `templates/website/components/search_modal.html`  
**Trigger:** Search icon button in navbar (calls `toggleSearch()`) or `⌘K` shortcut  
**Z-index:** 90

```html
<div id="search-modal" class="hidden fixed inset-0 z-[90] search-backdrop bg-black/50"
     role="dialog" aria-modal="true" aria-label="Cari">
  <div class="flex items-start justify-center min-h-screen pt-[15vh] px-4"
       @click.self="toggleSearch()">
    <div class="w-full max-w-2xl bg-white dark:bg-slate-800 rounded-2xl shadow-2xl
                border border-slate-200 dark:border-slate-700 overflow-hidden animate-scale-in"
         @click.stop>
      <!-- Search input + results -->
    </div>
  </div>
</div>
```

**Reference:** `templates/website/components/search_modal.html:1-4`

---

## Navigation Component Locations

| Component | Template Path |
|---|---|
| Public navbar | `templates/website/components/navbar.html` |
| Public breadcrumb | `templates/website/components/breadcrumb.html` |
| Search modal | `templates/website/components/search_modal.html` |
| Dashboard header + sidebar | `templates/dashboard_base.html` |
| Dashboard breadcrumbs | Inline `{% block breadcrumbs %}` in child templates |
| Settings sub-nav | `templates/settings/base.html` (sidebar `<aside>`) |
| Media Manager sub-nav | `templates/media_manager/base.html` (sidebar `<aside>`) |
| Public footer | `templates/website/components/footer.html` |
