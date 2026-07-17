# CMS Templates

> Template hierarchy, component library, and frontend patterns.

## Template Inheritance Hierarchy

```
base.html
└── dashboard_base.html
    ├── content/dashboard.html
    ├── content/category_list.html / category_form.html / category_confirm_delete.html
    ├── content/tag_list.html / tag_form.html / tag_confirm_delete.html
    ├── content/author_list.html / author_form.html / author_detail.html
    ├── content/seo_list.html / seo_form.html
    ├── content/version_list.html / version_detail.html
    ├── content/publishing_queue.html / publishing_queue_form.html
    ├── content/highlight_list.html / highlight_form.html
    ├── content/search_results.html / audit_log.html
    ├── news/cms/article_list.html / article_form.html / article_detail.html
    ├── podcast/cms/podcast_list.html / podcast_form.html / podcast_detail.html
    ├── podcast/cms/episode_list.html / episode_form.html / episode_detail.html
    ├── broadcast/cms/program_list.html / program_form.html / program_detail.html
    └── broadcast/cms/episode_list.html / episode_form.html / episode_detail.html
```

## Base Templates

### base.html

Root template providing HTML5 structure, Tailwind CSS, Alpine.js, HTMX, and global CSS/JS blocks.

### dashboard_base.html

CMS layout with top navigation, sidebar (full/collapsed/mobile drawer), mobile bottom nav, keyboard shortcuts modal, breadcrumbs, and flash messages.

**Blocks:** `title`, `dashboard_title`, `extra_css`, `content`, `extra_js`, `breadcrumb_current`

## Component Library

### Sidebar Menu

**File:** `dashboard/components/sidebar_menu.html`

Collapsible navigation sections: Beranda, Konten (articles/podcasts/episodes/categories/tags/authors/seo/schedule/versions/highlights/search/audit), Radio, Siaran (programs/hosts/schedules/episodes/announcements), Media, Sistem (users/settings).

### Quick Actions

**File:** `dashboard/components/quick_actions.html`

Mobile FAB panel with new article, podcast, episode, upload media, schedule, and search actions.

## Coffee Color Palette

| Token | Hex | Usage |
|-------|-----|-------|
| `coffee-50` | `#FDF8F4` | Page background (light) |
| `coffee-100` | `#F5E6D3` | Card backgrounds, borders |
| `coffee-200` | `#E8D0B3` | Borders, dividers |
| `coffee-300` | `#D4B896` | Disabled text, icons |
| `coffee-400` | `#B8956F` | Secondary text, placeholders |
| `coffee-500` | `#8B6914` | Body text, icons |
| `coffee-600` | `#6B4226` | Primary buttons, links |
| `coffee-700` | `#5A3621` | Headings, emphasis |
| `coffee-800` | `#3D2517` | Dark mode backgrounds |
| `coffee-900` | `#2A1A10` | Dark mode deep background |

**Status colors:** `bg-live` (active broadcast), `bg-success` (online), `bg-yellow-*` (warning), `bg-red-*` (error)

## Dark Mode Implementation

Uses Tailwind `dark:` class variant with manual toggle via Alpine.js `dashboardApp()`:

```javascript
toggleTheme() {
    this.darkMode = !this.darkMode;
    localStorage.setItem('theme', this.darkMode ? 'dark' : 'light');
    document.documentElement.classList.toggle('dark', this.darkMode);
}
```

**Toggle locations:** Header button, user menu, `Cmd+D` shortcut. Persisted in `localStorage`.

**Pattern:** `<div class="bg-white dark:bg-coffee-800">` for all elements.

## HTMX Integration Patterns

### Instant Search

```html
<input hx-get="/konten/search/" hx-trigger="input changed delay:300ms"
       hx-target="#search-results" hx-indicator="#search-spinner">
```

### Delete Confirmation

```html
<form hx-delete="{% url '...' pk %}" hx-confirm="Yakin?"
      hx-target="closest tr" hx-swap="outerHTML">
```

### Load More

```html
<div hx-get="/konten/categories/?page=2" hx-trigger="revealed"
     hx-swap="beforeend" hx-target="#list">
```

### HTMX Attributes

`hx-get`, `hx-post`, `hx-put`, `hx-delete`, `hx-trigger`, `hx-target`, `hx-swap`, `hx-indicator`, `hx-confirm`, `hx-headers`

## Alpine.js Patterns

### Collapsible Sidebar

```html
<div x-data="{ open: false }">
  <button @click="open = !open">Toggle</button>
  <div x-show="open" x-collapse>...</div>
</div>
```

### Dropdown

```html
<div x-data="{ dropdownOpen: false }">
  <div x-show="dropdownOpen" @click.away="dropdownOpen = false" x-transition>
```

### Modal

```html
<div x-data="{ modalOpen: false }">
  <div x-show="modalOpen" x-transition class="fixed inset-0 z-50">
    <div @click.away="modalOpen = false">
```

### Tab Navigation

```html
<div x-data="{ activeTab: 'tab1' }">
  <button @click="activeTab = 'tab1'" :class="{ 'active': activeTab === 'tab1' }">
  <div x-show="activeTab === 'tab1'">
```

## Form Patterns

### Standard Layout

```html
<form method="post" class="space-y-6">
  {% csrf_token %}
  <div class="bg-white dark:bg-coffee-800 rounded-xl shadow-sm border p-6">
    {% for field in form %}
    <label>{{ field.label }}</label>
    {{ field }}
    {% if field.errors %}<p class="text-red-500">{{ field.errors.0 }}</p>{% endif %}
    {% endfor %}
  </div>
  <div class="flex justify-end gap-3">
    <a href="..." class="text-coffee-600">Batal</a>
    <button type="submit" class="bg-coffee-600 text-white">Simpan</button>
  </div>
</form>
```

### Form Input Classes

`.form-input` and `.form-select` are defined with Tailwind directives for consistent styling.

## Responsive Design

| Breakpoint | Width | Layout |
|-----------|-------|--------|
| Mobile | < 640px | Bottom nav, drawer sidebar, stacked grid |
| Tablet | 640–1024px | Bottom nav, collapsed sidebar |
| Desktop | > 1024px | Full sidebar, top nav |

## CSS Architecture

**Static files:** `static/css/homepage.css`, `static/css/dashboard.css`

**Animations:** `.animate-fade-in`, `.animate-scale-in`

**Tailwind config:** `tailwind.config.js` with custom coffee palette, `darkMode: 'class'`, custom fonts, and box shadows.
