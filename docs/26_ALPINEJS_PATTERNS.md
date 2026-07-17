# 26 — Alpine.js Patterns

Kabulhaden CMS uses Alpine.js for interactive UI components: dropdowns, modals, tabs, accordions, form validation, and file upload previews. Alpine.js is loaded via CDN with `defer`.

---

## Setup

```html
<!-- In base.html -->
<script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.14.0/dist/cdn.min.js"
        integrity="sha384-9r4u6+P6g9XnF7LwO0oH+L9r4u6+P6g9XnF7LwO0oH+"
        crossorigin="anonymous"></script>
```

**Reference:** `templates/base.html:74`

---

## Core Directives

| Directive | Purpose | Example |
|---|---|---|
| `x-data` | Component state | `x-data="{ open: false }"` |
| `x-show` | Show/hide element | `x-show="open"` |
| `x-on` | Event listener | `@click="open = !open"` |
| `x-bind` | Attribute binding | `:class="{ 'active': isOpen }"` |
| `x-text` | Text content | `x-text="loading ? 'Saving...' : 'Save'"` |
| `x-html` | HTML content | `x-html="content"` |
| `x-ref` | Reference element | `x-ref="fileInput"` |
| `x-init` | Initialization | `x-init="loadData()"` |
| `x-transition` | Transitions | `x-transition:enter="..."` |
| `x-trap` | Focus trap | `x-trap.noscroll="isOpen"` |
| `@click.away` | Click outside | `@click.away="open = false"` |
| `@keydown.escape` | ESC key | `@keydown.escape.window="close()"` |

---

## Dropdown Pattern

### Simple Dropdown

```html
<div class="relative" x-data="{ open: false }">
  <button @click="open = !open" class="...">
    Toggle Menu
  </button>
  <div x-show="open"
       @click.away="open = false"
       x-transition:enter="transition ease-out duration-200"
       x-transition:enter-start="opacity-0 translate-y-1"
       x-transition:enter-end="opacity-100 translate-y-0"
       x-transition:leave="transition ease-in duration-150"
       x-transition:leave-start="opacity-100 translate-y-0"
       x-transition:leave-end="opacity-0 translate-y-1"
       class="absolute right-0 mt-2 w-48 bg-white rounded-lg shadow-lg py-1 z-50"
       style="display: none;">
    <a href="#" class="block px-4 py-2 text-sm hover:bg-slate-100">Item 1</a>
    <a href="#" class="block px-4 py-2 text-sm hover:bg-slate-100">Item 2</a>
  </div>
</div>
```

**Reference:** `templates/dashboard_base.html:39-57`

### Hover Dropdown (Mega Menu)

```html
<div class="relative" x-data="{ open: false }"
     @mouseenter="open = true" @mouseleave="open = false">
  <a href="#" @click="open = !open" class="flex items-center gap-1 ...">
    Program
    <svg class="w-4 h-4 transition-transform" :class="open && 'rotate-180'"><!-- chevron --></svg>
  </a>
  <div x-show="open"
       class="absolute left-0 mt-1 w-[560px] bg-white rounded-2xl shadow-card-hover p-6 z-50"
       style="display: none;"
       @click.away="open = false">
    <!-- Dropdown content -->
  </div>
</div>
```

**Reference:** `templates/website/components/navbar.html:22-79`

---

## Modal Pattern

### Search Modal

```html
<div x-data="{ searchOpen: false }">
  <!-- Trigger -->
  <button @click="searchOpen = true">Open Search</button>

  <!-- Modal -->
  <div x-show="searchOpen"
       x-transition:enter="transition ease-out duration-200"
       x-transition:enter-start="opacity-0"
       x-transition:enter-end="opacity-100"
       x-transition:leave="transition ease-in duration-150"
       x-transition:leave-start="opacity-100"
       x-transition:leave-end="opacity-0"
       class="fixed inset-0 z-50 bg-black/50"
       @keydown.escape.window="searchOpen = false"
       style="display: none;">
    <div @click.self="searchOpen = false"
         class="flex items-center justify-center min-h-screen">
      <div class="bg-white rounded-2xl shadow-2xl max-w-2xl w-full mx-4" @click.stop>
        <!-- Modal content -->
      </div>
    </div>
  </div>
</div>
```

---

## Tab Pattern

```html
<div x-data="{ activeTab: 'tab1' }">
  <!-- Tab Headers -->
  <div class="flex border-b border-slate-200">
    <button @click="activeTab = 'tab1'"
            :class="activeTab === 'tab1'
              ? 'border-coffee-400 text-coffee-600'
              : 'border-transparent text-slate-500 hover:text-slate-700'"
            class="px-4 py-2 border-b-2 font-medium text-sm transition-colors">
      Tab 1
    </button>
    <button @click="activeTab = 'tab2'"
            :class="activeTab === 'tab2'
              ? 'border-coffee-400 text-coffee-600'
              : 'border-transparent text-slate-500 hover:text-slate-700'"
            class="px-4 py-2 border-b-2 font-medium text-sm transition-colors">
      Tab 2
    </button>
  </div>

  <!-- Tab Content -->
  <div class="py-4">
    <div x-show="activeTab === 'tab1'">
      Content for Tab 1
    </div>
    <div x-show="activeTab === 'tab2'" style="display: none;">
      Content for Tab 2
    </div>
  </div>
</div>
```

---

## Accordion Pattern

```html
<div x-data="{ openItem: null }">
  <div class="border border-slate-200 rounded-lg">
    <!-- Item 1 -->
    <div class="border-b border-slate-200 last:border-b-0">
      <button @click="openItem = openItem === 1 ? null : 1"
              class="w-full flex items-center justify-between px-4 py-3 text-sm font-medium">
        <span>Accordion Title 1</span>
        <svg class="w-5 h-5 text-slate-400 transition-transform duration-200"
             :class="openItem === 1 && 'rotate-180'"
             fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M19 9l-7 7-7-7" />
        </svg>
      </button>
      <div x-show="openItem === 1"
           x-transition:enter="transition ease-out duration-200"
           x-transition:enter-start="opacity-0 -translate-y-1"
           x-transition:enter-end="opacity-100 translate-y-0"
           x-transition:leave="transition ease-in duration-150"
           x-transition:leave-start="opacity-100 translate-y-0"
           x-transition:leave-end="opacity-0 -translate-y-1"
           class="px-4 pb-3 text-sm text-slate-600"
           style="display: none;">
        Accordion content for item 1.
      </div>
    </div>

    <!-- Item 2 -->
    <div class="border-b border-slate-200 last:border-b-0">
      <button @click="openItem = openItem === 2 ? null : 2" class="...">
        <span>Accordion Title 2</span>
      </button>
      <div x-show="openItem === 2" style="display: none;" class="px-4 pb-3 text-sm text-slate-600">
        Accordion content for item 2.
      </div>
    </div>
  </div>
</div>
```

---

## Form Validation Pattern

### Inline Validation

```html
<div x-data="{ email: '', emailError: '' }">
  <label class="block text-sm font-medium text-slate-700 mb-1">Email</label>
  <input type="email" x-model="email"
         @input="emailError = email && !email.includes('@') ? 'Email tidak valid' : ''"
         :class="emailError ? 'border-red-300 focus:ring-red-500' : 'border-slate-300'"
         class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500">
  <p x-show="emailError" x-text="emailError"
     class="mt-1 text-sm text-red-600" style="display: none;"></p>
</div>
```

### Password Visibility Toggle

```html
<div x-data="{ showPassword: false }">
  <label class="block text-sm font-medium text-slate-700 mb-1">Password</label>
  <div class="relative">
    <input :type="showPassword ? 'text' : 'password'" name="password"
           class="w-full px-4 py-2 pr-10 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500">
    <button type="button" @click="showPassword = !showPassword"
            class="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600">
      <svg x-show="!showPassword" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M15 12a3 3 0 11-6 0 3 3 0 016 0z M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
      </svg>
      <svg x-show="showPassword" class="w-5 h-5" style="display: none;" fill="none" viewBox="0 0 24 24"
           stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21" />
      </svg>
    </button>
  </div>
</div>
```

---

## File Upload Preview

### Drag-and-Drop with Preview

```html
<div x-data="{ dragover: false, files: [] }"
     @dragover.prevent="dragover = true"
     @dragleave.prevent="dragover = false"
     @drop.prevent="dragover = false; handleFiles($event.dataTransfer.files)"
     :class="{ 'border-blue-400 bg-blue-50': dragover }"
     class="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center cursor-pointer">
  <input type="file" multiple @change="handleFiles($event.target.files)" class="hidden" x-ref="fileInput">
  <div @click="$refs.fileInput.click()">
    <!-- Upload zone content -->
  </div>

  <!-- File preview list -->
  <div class="mt-4 space-y-2">
    <template x-for="file in files" :key="file.name">
      <div class="flex items-center gap-3 p-2 bg-slate-50 rounded-lg">
        <span class="text-sm font-medium" x-text="file.name"></span>
        <span class="text-xs text-slate-500" x-text="formatSize(file.size)"></span>
      </div>
    </template>
  </div>
</div>
```

**Reference:** `templates/media_manager/upload.html:10-25`

---

## User Menu Toggle

```html
<div class="relative" x-data="{ userMenuOpen: false }">
  <button @click="userMenuOpen = !userMenuOpen"
          class="flex items-center gap-2 text-sm font-medium focus:outline-none">
    <!-- Avatar + name -->
  </button>
  <div x-show="userMenuOpen"
       @click.away="userMenuOpen = false"
       class="absolute right-0 mt-2 w-48 bg-white border rounded-lg shadow-lg py-1 z-50"
       style="display: none;">
    <!-- Menu items -->
  </div>
</div>
```

**Reference:** `templates/dashboard_base.html:39-57`

---

## Mobile Menu Toggle

```html
<div x-data="{ mobileMenuOpen: false }">
  <button @click="mobileMenuOpen = !mobileMenuOpen"
          :aria-expanded="mobileMenuOpen"
          aria-label="Toggle menu navigasi">
    <svg x-show="!mobileMenuOpen"><!-- hamburger icon --></svg>
    <svg x-show="mobileMenuOpen" style="display: none;"><!-- close icon --></svg>
  </button>

  <div x-show="mobileMenuOpen"
       x-transition:enter="transition ease-out duration-200"
       x-transition:enter-start="opacity-0 -translate-y-2"
       x-transition:enter-end="opacity-100 translate-y-0"
       x-transition:leave="transition ease-in duration-150"
       x-transition:leave-start="opacity-100 translate-y-0"
       x-transition:leave-end="opacity-0 -translate-y-2"
       class="lg:hidden border-t border-coffee-200 py-3 space-y-1"
       style="display: none;">
    <!-- Mobile nav links -->
  </div>
</div>
```

**Reference:** `templates/website/components/navbar.html:101-126`

---

## Dark Mode Toggle

```html
<div x-data="{ darkMode: localStorage.getItem('theme') === 'dark' }">
  <button @click="
    darkMode = !darkMode;
    localStorage.setItem('theme', darkMode ? 'dark' : 'light');
    if (darkMode) { document.documentElement.classList.add('dark'); }
    else { document.documentElement.classList.remove('dark'); }
  ">
    <svg x-show="!darkMode"><!-- moon icon --></svg>
    <svg x-show="darkMode" style="display: none;"><!-- sun icon --></svg>
  </button>
</div>
```

**Reference:** `templates/dashboard_base.html:22-35`

---

## Toast Auto-dismiss

```html
<div x-data="{ show: true }" x-show="show"
     x-init="setTimeout(() => show = false, 5000)"
     x-transition:enter="transition ease-out duration-300"
     x-transition:enter-start="opacity-0"
     x-transition:enter-end="opacity-100"
     x-transition:leave="transition ease-in duration-200"
     x-transition:leave-start="opacity-100"
     x-transition:leave-end="opacity-0"
     class="p-4 rounded-lg flex items-center justify-between">
  <span>{{ message }}</span>
  <button @click="show = false" class="hover:opacity-70">×</button>
</div>
```

---

## FOUC Prevention

All `x-show` elements include `style="display: none;"` to prevent Flash of Unstyled Content before Alpine.js initializes.

```html
<div x-show="isOpen" style="display: none;">
  <!-- Content -->
</div>
```

---

## Common State Patterns

| Pattern | State | Example |
|---|---|---|
| Toggle | `x-data="{ open: false }"` | `@click="open = !open"` |
| Accordion | `x-data="{ openItem: null }"` | `openItem === 1 ? null : 1` |
| Tabs | `x-data="{ activeTab: 'tab1' }"` | `@click="activeTab = 'tab2'"` |
| Form | `x-data="{ field: '', error: '' }"` | `x-model="field"` |
| Loading | `x-data="{ loading: false }"` | `:disabled="loading"` |
| Theme | `x-data="{ darkMode: false }"` | `localStorage` persistence |
