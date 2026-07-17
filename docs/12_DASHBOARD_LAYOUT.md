# 12 — Dashboard Layout

The admin dashboard uses a sidebar-based layout with a sticky top header, implemented through Django template inheritance and Tailwind CSS utilities. All admin modules share this layout for consistency.

---

## Template Inheritance

```
base.html
└── dashboard_base.html
    ├── broadcast/dashboard.html
    ├── broadcast/episode_list.html
    ├── broadcast/episode_form.html
    ├── radio/station_list.html
    ├── radio/station_form.html
    ├── media_manager/base.html
    │   ├── media_manager/list.html
    │   ├── media_manager/upload.html
    │   └── media_manager/dashboard.html
    ├── settings/base.html
    │   ├── settings/site.html
    │   ├── settings/security.html
    │   └── ...
    └── users/admin/user_list.html
```

**Key files:**
- `templates/base.html` — Root: fonts, scripts, CSRF config
- `templates/dashboard_base.html` — Dashboard shell: header + sidebar + content
- Child templates extend `dashboard_base.html` and override `{% block content %}` and `{% block breadcrumbs %}`

---

## Dashboard Structure

```
┌──────────────────────────────────────────────────┐
│ Top Header (h-16, sticky)                        │
│ [☰ mobile] Kabulhaden CMS    [🌙 dark] [👤 user] │
├──────────┬───────────────────────────────────────┤
│          │ Breadcrumbs: Home / Module / Page      │
│ Sidebar  ├───────────────────────────────────────┤
│ (w-64)   │ Flash Messages                        │
│          ├───────────────────────────────────────┤
│ ┌──────┐ │ ┌───────────────────────────────────┐ │
│ │ Home │ │ │ Content Card (white bg, rounded)  │ │
│ ├──────┤ │ │                                   │ │
│ │ CMS  │ │ │   {% block content %}             │ │
│ │ Radio│ │ │                                   │ │
│ │ Bcast│ │ │                                   │ │
│ ├──────┤ │ │                                   │ │
│ │ Admin│ │ └───────────────────────────────────┘ │
│ │ Users│ │ Footer                               │
│ │ Django│                                       │
│ └──────┘ │                                       │
│ ──────── │                                       │
│ Role: .. │                                       │
└──────────┴───────────────────────────────────────┘
```

---

## Top Header Bar

**Height:** 64px (`h-16`)  
**Position:** Sticky top (`sticky top-0 z-30`)  
**Background:** White / dark:slate-800  
**Border:** Bottom (`border-b border-slate-200`)

```html
<header class="bg-white dark:bg-slate-800 border-b border-slate-200 dark:border-slate-700
               h-16 flex items-center justify-between px-4 sm:px-6 lg:px-8
               z-30 sticky top-0 shadow-sm transition-colors duration-200">
```

**Reference:** `templates/dashboard_base.html:7`

### Left Section
- Mobile sidebar toggle (hamburger icon, visible `md:hidden`)
- Kabulhaden CMS logo/text link to `core:home`

### Right Section
- Dark mode toggle button (moon/sun icon swap via Alpine.js)
- User menu dropdown (avatar initial + full name)
  - "Profil Saya" → `users:profile`
  - "Admin Panel" → `admin:index` (staff only)
  - "Keluar" (logout) → form POST to `users:logout`

**Reference:** `templates/dashboard_base.html:22-60`

---

## Sidebar Navigation

**Width:** 256px (`w-64`)  
**Position:** Fixed on mobile, relative on desktop  
**Z-index:** 40  
**Background:** White / dark:slate-800  
**Transition:** `transform 200ms ease-in-out`

```html
<aside :class="sidebarOpen ? 'translate-x-0' : '-translate-x-full'"
       class="bg-white dark:bg-slate-800 border-r border-slate-200 dark:border-slate-700
              w-64 fixed inset-y-0 left-0 md:relative md:translate-x-0 z-40
              transform transition-transform duration-200 ease-in-out
              md:flex md:flex-col shadow-sm pt-16 md:pt-0">
```

**Reference:** `templates/dashboard_base.html:66`

### Sidebar Sections

#### 1. Home Link
```html
<a href="{% url 'core:home' %}"
   class="flex items-center gap-3 px-3 py-2 rounded-lg bg-slate-100 dark:bg-slate-700
          text-brand-500 dark:text-blue-400 font-medium text-sm">
  <svg class="h-5 w-5"><!-- home icon --></svg>
  Dashboard
</a>
```

#### 2. CMS Modules
```html
<span class="px-3 text-xs font-semibold text-slate-400 uppercase tracking-wider block mb-2">
  CMS Modules
</span>

<!-- Radio Engine -->
<a href="{% url 'radio:dashboard' %}"
   class="flex items-center gap-3 px-3 py-2 rounded-lg hover:bg-slate-100
          dark:hover:bg-slate-700 text-slate-600 dark:text-slate-400 text-sm">
  <svg class="h-5 w-5"><!-- radio icon --></svg>
  Radio Engine
</a>

<!-- Broadcast Management -->
<a href="{% url 'broadcast:dashboard' %}"
   class="flex items-center gap-3 px-3 py-2 rounded-lg hover:bg-slate-100
          dark:hover:bg-slate-700 text-slate-600 dark:text-slate-400 text-sm">
  <svg class="h-5 w-5"><!-- broadcast icon --></svg>
  Broadcast Management
</a>
```

**Reference:** `templates/dashboard_base.html:77-93`

#### 3. Admin Section (staff only)
```html
{% if user.is_staff %}
<span class="px-3 text-xs font-semibold text-slate-400 uppercase tracking-wider block mb-2">
  Admin
</span>

<!-- Kelola Pengguna -->
<a href="{% url 'users:admin_user_list' %}"
   class="flex items-center gap-3 px-3 py-2 rounded-lg hover:bg-slate-100
          dark:hover:bg-slate-700 text-slate-600 dark:text-slate-400 text-sm">
  <svg class="h-5 w-5"><!-- users icon --></svg>
  Kelola Pengguna
</a>

<!-- Django Admin -->
<a href="{% url 'admin:index' %}"
   class="flex items-center gap-3 px-3 py-2 rounded-lg hover:bg-slate-100
          dark:hover:bg-slate-700 text-slate-600 dark:text-slate-400 text-sm">
  <svg class="h-5 w-5"><!-- settings icon --></svg>
  Django Admin
</a>
{% endif %}
```

**Reference:** `templates/dashboard_base.html:95-114`

#### 4. Sidebar Footer
Displays the current user's role.

```html
<div class="p-4 border-t border-slate-200 dark:border-slate-700 text-xs text-slate-500">
  Sistem Peran:
  <span class="font-semibold text-slate-700 dark:text-slate-300">
    {{ user.get_role_display|default:"Tamu" }}
  </span>
</div>
```

**Reference:** `templates/dashboard_base.html:117-119`

### Sidebar Item States

| State | Classes |
|---|---|
| Default | `text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-700` |
| Active (home) | `bg-slate-100 dark:bg-slate-700 text-brand-500 dark:text-blue-400 font-medium` |
| Separator | `border-t border-slate-200 dark:border-slate-700 pt-4` |

---

## Content Area

**Padding:** Responsive — `p-4 sm:p-6 lg:p-8`  
**Background:** Transparent (inherits page background)

```html
<main class="flex-1 min-w-0 flex flex-col p-4 sm:p-6 lg:p-8">
```

**Reference:** `templates/dashboard_base.html:123`

### Content Structure

1. **Breadcrumbs** — `mb-4`, see [13_NAVIGATION_SYSTEM.md](13_NAVIGATION_SYSTEM.md)
2. **Flash Messages** — `mb-6 space-y-2`, see [17_TOAST_NOTIFICATION.md](17_TOAST_NOTIFICATION.md)
3. **Content Card** — White bg, rounded-xl, shadow-sm, border, p-6
4. **Footer** — `mt-8 text-center text-xs text-slate-400`

```html
<!-- Content Card -->
<div class="flex-1 bg-white dark:bg-slate-800 rounded-xl shadow-sm
            border border-slate-200 dark:border-slate-700 p-6 transition-colors duration-200">
  {% block content %}{% endblock %}
</div>
```

**Reference:** `templates/dashboard_base.html:155`

---

## Sub-Module Navigation (Secondary Sidebar)

Some modules (Settings, Media Manager) have a secondary sidebar within the content area.

### Settings Sidebar
```html
<!-- templates/settings/base.html -->
<aside class="w-64 bg-gray-50 border-r border-gray-200 p-4">
  <h2 class="text-lg font-semibold text-gray-900 mb-4">Pengaturan</h2>
  <nav class="space-y-1">
    {% for group in settings_groups %}
    <a href="{{ group.url }}"
       class="block px-3 py-2 rounded-lg text-sm font-medium
              {% if request.path == group.url %}
                bg-blue-50 text-blue-700
              {% else %}
                text-gray-700 hover:bg-gray-100
              {% endif %}">
      {{ group.name }}
    </a>
    {% endfor %}
  </nav>
</aside>
```

**Reference:** `templates/settings/base.html:5-15`

### Media Manager Sidebar
```html
<!-- templates/media_manager/base.html -->
<aside class="w-64 bg-gray-50 border-r border-gray-200 p-4">
  <h2 class="text-lg font-semibold text-gray-900 mb-4">Media</h2>
  <nav class="space-y-1">
    <a href="{% url 'media_manager:dashboard' %}"
       class="block px-3 py-2 rounded-lg text-sm font-medium
              {% if request.resolver_match.url_name == 'dashboard' %}
                bg-blue-50 text-blue-700
              {% else %}
                text-gray-700 hover:bg-gray-100
              {% endif %}">
      Dashboard
    </a>
    <!-- Semua File, Upload, Folder, Tag links -->
  </nav>
</aside>
```

**Reference:** `templates/media_manager/base.html:5-28`

---

## Mobile Sidebar Behavior

| Property | Value |
|---|---|
| Default state | Hidden (`-translate-x-full`) |
| Toggled state | Visible (`translate-x-0`) |
| Trigger | Hamburger button in header |
| Overlay | None (pushes content) |
| Close mechanism | Click any sidebar link or toggle button |
| Alpine.js state | `sidebarOpen` |

```html
<!-- Mobile toggle button -->
<button @click="sidebarOpen = !sidebarOpen"
        class="text-slate-500 hover:text-slate-600 dark:text-slate-400
               dark:hover:text-slate-300 md:hidden p-2 rounded-lg
               hover:bg-slate-100 dark:hover:bg-slate-700">
  <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
          d="M4 6h16M4 12h16M4 18h16" />
  </svg>
</button>
```

**Reference:** `templates/dashboard_base.html:10-14`

---

## Page Title Pattern

Each dashboard page sets its title via `{% block title %}`.

```html
{% block title %}Episodes - Broadcast Management{% endblock %}
{% block title %}Radio Stations - Kabulhaden CMS{% endblock %}
{% block title %}Edit Episode - Broadcast Management{% endblock %}
```

---

## Content Width

The dashboard content area has no max-width constraint (uses `flex-1 min-w-0`). Tables use `overflow-x-auto` for horizontal scrolling on smaller screens.

---

## Z-Index Layering

| Element | Z-index | Tailwind Class |
|---|---|---|
| Header | 30 | `z-30` |
| Sidebar | 40 | `z-40` |
| User menu dropdown | 50 | `z-50` |
| Search modal | 90 | `z-[90]` |
| Flash messages | 30 (in flow) | Default |
