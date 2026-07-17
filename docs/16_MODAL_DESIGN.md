# 16 — Modal Design

Modals in Kabulhaden CMS are used for confirmations, forms, and search. They use Alpine.js for visibility control and follow consistent patterns for focus management and dismissal.

---

## Confirmation Modal (Delete)

The simplest modal pattern — a JavaScript `confirm()` dialog for destructive actions.

```html
<form method="post" action="{% url 'broadcast:episode_delete' ep.pk %}"
      onsubmit="return confirm('Hapus episode ini?')">
  {% csrf_token %}
  <button type="submit" class="text-red-600 hover:text-red-700 dark:text-red-400 text-sm">
    Hapus
  </button>
</form>
```

**Reference:** `templates/broadcast/episode_list.html:69-72`

### Bulk Delete Confirmation

```html
<button type="submit" onclick="return confirm('Hapus file terpilih?')"
        class="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 text-sm">
  Hapus Terpilih
</button>
```

**Reference:** `templates/media_manager/list.html:52-53`

---

## Search Modal (Alpine.js)

Full overlay modal for global search.

**Template:** `templates/website/components/search_modal.html`

```html
<div id="search-modal"
     class="hidden fixed inset-0 z-[90] search-backdrop bg-black/50"
     role="dialog" aria-modal="true" aria-label="Cari">
  <div class="flex items-start justify-center min-h-screen pt-[15vh] px-4"
       @click.self="toggleSearch()">
    <div class="w-full max-w-2xl bg-white dark:bg-slate-800 rounded-2xl shadow-2xl
                border border-slate-200 dark:border-slate-700 overflow-hidden animate-scale-in"
         @click.stop>
      <!-- Search Input -->
      <div class="flex items-center gap-3 px-6 py-4 border-b border-slate-200 dark:border-slate-700">
        <svg class="w-5 h-5 text-slate-400 dark:text-slate-500 flex-shrink-0"><!-- search icon --></svg>
        <input type="search"
               placeholder="Cari program, podcast, berita..."
               class="flex-1 bg-transparent text-lg text-slate-900 dark:text-white
                      placeholder-slate-400 dark:placeholder-slate-500 focus:outline-none"
               oninput="handleSearch(this.value)"
               autofocus>
        <kbd class="hidden sm:inline-flex items-center px-2 py-0.5 rounded text-xs font-mono
                    text-slate-400 dark:text-slate-500 bg-slate-100 dark:bg-slate-700
                    border border-slate-200 dark:border-slate-600">ESC</kbd>
      </div>
      <!-- Results -->
      <div id="search-results" class="max-h-[50vh] overflow-y-auto p-4">
        <p class="text-center text-slate-400 dark:text-slate-500 text-sm py-8">
          Ketik untuk mulai mencari...
        </p>
      </div>
    </div>
  </div>
</div>
```

**Reference:** `templates/website/components/search_modal.html:1-25`

### Search Modal Properties

| Property | Value |
|---|---|
| Z-index | 90 |
| Backdrop | `bg-black/50` |
| Position | `fixed inset-0` |
| Content max-width | `max-w-2xl` |
| Content padding-top | `pt-[15vh]` |
| Content max-height | `max-h-[50vh]` (results area) |
| Border radius | `rounded-2xl` |
| Animation | `animate-scale-in` |
| Dismiss | Click backdrop (`@click.self`) or press ESC |
| Focus | Auto-focus on search input |

---

## Dropdown Menu (Alpine.js)

Used for user menu, filter dropdowns, and action menus.

```html
<div class="relative" x-data="{ userMenuOpen: false }">
  <button @click="userMenuOpen = !userMenuOpen"
          class="flex items-center gap-2 text-sm font-medium text-slate-700
                 dark:text-slate-300 hover:text-slate-900 dark:hover:text-white
                 focus:outline-none">
    <div class="w-8 h-8 rounded-full bg-brand-500 text-white flex items-center justify-center font-bold">
      {{ user.username|slice:":1"|upper }}
    </div>
    <span class="hidden md:inline">{{ user.get_full_name }}</span>
  </button>
  <div x-show="userMenuOpen"
       @click.away="userMenuOpen = false"
       class="absolute right-0 mt-2 w-48 bg-white dark:bg-slate-800
              border border-slate-200 dark:border-slate-700 rounded-lg shadow-lg py-1
              z-50 transition-all"
       style="display: none;">
    <a href="{% url 'users:profile' %}"
       class="block px-4 py-2 text-sm text-slate-700 dark:text-slate-300
              hover:bg-slate-100 dark:hover:bg-slate-700">
      Profil Saya
    </a>
    {% if user.is_staff %}
    <a href="{% url 'admin:index' %}"
       class="block px-4 py-2 text-sm text-slate-700 dark:text-slate-300
              hover:bg-slate-100 dark:hover:bg-slate-700">
      Admin Panel
    </a>
    {% endif %}
    <hr class="border-slate-200 dark:border-slate-700 my-1">
    <form action="{% url 'users:logout' %}" method="post" class="w-full">
      {% csrf_token %}
      <button type="submit"
              class="block w-full text-left px-4 py-2 text-sm text-red-600
                     dark:text-red-400 hover:bg-slate-100 dark:hover:bg-slate-700">
        Keluar
      </button>
    </form>
  </div>
</div>
```

**Reference:** `templates/dashboard_base.html:39-57`

### Dropdown Properties

| Property | Value |
|---|---|
| Position | `absolute right-0 mt-2` |
| Width | `w-48` |
| Z-index | 50 |
| Border radius | `rounded-lg` |
| Shadow | `shadow-lg` |
| Dismiss | `@click.away` |
| Transition | `transition-all` |

---

## Mega Dropdown (Navigation)

Large dropdown for the Program menu in the public navbar.

```html
<div class="relative" x-data="{ open: false }"
     @mouseenter="open = true" @mouseleave="open = false">
  <a href="{% url 'website:program_list' %}" @click="open = !open" class="...">
    Program
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
      <!-- Two column grid with grouped links -->
    </div>
  </div>
</div>
```

**Reference:** `templates/website/components/navbar.html:22-79`

---

## Alpine.js x-show Pattern

All Alpine.js modals use `x-show` with `style="display: none;"` for initial state to prevent FOUC (Flash of Unstyled Content).

```html
<!-- Standard pattern -->
<div x-show="isOpen"
     style="display: none;">
  <!-- Modal content -->
</div>

<!-- With transitions -->
<div x-show="isOpen"
     x-transition:enter="transition ease-out duration-200"
     x-transition:enter-start="opacity-0"
     x-transition:enter-end="opacity-100"
     x-transition:leave="transition ease-in duration-150"
     x-transition:leave-start="opacity-100"
     x-transition:leave-end="opacity-0"
     style="display: none;">
  <!-- Modal content -->
</div>
```

---

## Focus Trap

For accessible modals, focus should be trapped within the modal when open.

```html
<div x-show="isOpen"
     @keydown.escape.window="isOpen = false"
     x-trap.noscroll="isOpen"
     class="fixed inset-0 z-50 ...">
  <!-- Modal content -->
</div>
```

Requires the Alpine.js Focus plugin (`@alpinejs/trap`).

---

## Dismissal Patterns

| Pattern | Mechanism | Example |
|---|---|---|
| Click outside | `@click.away="open = false"` | Dropdown menus |
| Click backdrop | `@click.self="toggleSearch()"` | Search modal |
| Escape key | `@keydown.escape.window` | Global escape handler |
| Close button | `@click="show = false"` | Toast notifications |
| Confirm dialog | `onsubmit="return confirm('...')"` | Delete confirmations |

---

## Modal Backdrop

| Modal Type | Backdrop | Reference |
|---|---|---|
| Search | `bg-black/50` | `search_modal.html` |
| Dropdown | None (positioned below trigger) | `dashboard_base.html` |
| Confirm | Native browser `confirm()` | `episode_list.html` |

---

## Z-Index Stack

| Layer | Z-index |
|---|---|
| Page content | 0 (default) |
| Sticky header | 30 |
| Sidebar | 40 |
| Dropdown menus | 50 |
| Search modal | 90 |
| Mobile player | 100 |
