# 11 — Reusable UI Components

Kabulhaden CMS uses a consistent set of reusable UI components built with Tailwind CSS utility classes and the project's custom design tokens (coffee palette, rounded-card, shadow-card). All components live in Django templates under `templates/website/components/` (public) or are inlined in dashboard templates.

---

## Buttons

### Primary Button (coffee-400)

The main CTA button used across the public site. Uses the coffee-400 brand color.

```html
<!-- Standard primary -->
<button class="px-5 py-2.5 rounded-xl bg-coffee-400 text-white font-heading font-semibold text-sm
               hover:bg-coffee-500 transition-all shadow-md hover:shadow-lg active:scale-[.98]">
  DENGARKAN LIVE
</button>

<!-- With icon -->
<a href="{% url 'website:radio_live' %}"
   class="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-coffee-400 text-white
          font-heading font-semibold text-sm hover:bg-coffee-500 transition-all
          shadow-md hover:shadow-lg active:scale-[.98]">
  <span class="w-2 h-2 bg-white rounded-full animate-pulse"></span>
  DENGARKAN LIVE
</a>
```

**Reference:** `templates/website/components/navbar.html:96`

### Secondary Button

Used for less prominent actions in the dashboard.

```html
<a href="{% url 'broadcast:episode_list' %}"
   class="px-6 py-2 border border-slate-300 dark:border-slate-600 text-slate-700
          dark:text-slate-300 rounded-lg hover:bg-slate-50 dark:hover:bg-slate-700 font-medium">
  Batal
</a>
```

**Reference:** `templates/broadcast/episode_form.html:42`

### Danger Button (red)

Used for destructive actions (delete, remove).

```html
<button type="submit"
        class="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 text-sm">
  Hapus Terpilih
</button>

<!-- Text variant (inline delete link) -->
<form method="post" action="{% url 'broadcast:episode_delete' ep.pk %}"
      onsubmit="return confirm('Hapus episode ini?')">
  {% csrf_token %}
  <button type="submit" class="text-red-600 hover:text-red-700 dark:text-red-400 text-sm">
    Hapus
  </button>
</form>
```

**Reference:** `templates/media_manager/list.html:52`, `templates/broadcast/episode_list.html:70`

### Ghost Button

Minimal button for secondary actions in header/toolbar areas.

```html
<button class="p-2.5 rounded-xl text-[#666666] hover:text-coffee-600 hover:bg-coffee-50 transition-colors"
        aria-label="Cari">
  <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
    <path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
  </svg>
</button>
```

**Reference:** `templates/website/components/navbar.html:89`

### Dashboard Action Button (blue-600)

Standard "create/add" button in admin dashboards.

```html
<a href="{% url 'broadcast:episode_create' %}"
   class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 text-sm font-medium">
  + Tambah Episode
</a>
```

**Reference:** `templates/broadcast/episode_list.html:20`

### Auth Submit Button (brand-500)

Full-width submit button for auth forms.

```html
<button type="submit"
        class="w-full flex justify-center py-2.5 px-4 border border-transparent rounded-lg
               shadow-sm text-sm font-semibold text-white bg-brand-500 hover:bg-brand-600
               focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-brand-500 transition">
  Masuk
</button>
```

**Reference:** `apps/users/templates/users/login.html:55`

### Button Sizes

| Size | Classes | Usage |
|---|---|---|
| Small | `px-4 py-2 text-sm` | Table actions, inline buttons |
| Medium | `px-5 py-2.5 text-sm` | Standard buttons, nav CTAs |
| Large | `px-6 py-2 text-base` | Form submit, primary actions |
| Icon | `p-2.5 rounded-xl` | Icon-only buttons (search, menu) |

---

## Cards

### Standard Card (shadow-card, rounded-card)

```html
<div class="bg-white rounded-card shadow-card p-6
            hover:shadow-card-hover transition-shadow duration-250">
  <h3 class="font-heading font-bold text-coffee-700">Card Title</h3>
  <p class="text-sm text-[#666666] mt-2">Card description text.</p>
</div>
```

### Dashboard Content Card

White background card used as the main content wrapper in the admin panel.

```html
<div class="flex-1 bg-white dark:bg-slate-800 rounded-xl shadow-sm
            border border-slate-200 dark:border-slate-700 p-6 transition-colors duration-200">
  {% block content %}{% endblock %}
</div>
```

**Reference:** `templates/dashboard_base.html:155`

### Form Container Card

Bordered card used to group form fields.

```html
<div class="bg-white dark:bg-slate-800 rounded-xl shadow-sm border border-slate-200
            dark:border-slate-700 p-6 space-y-4">
  <!-- Form fields here -->
</div>
```

**Reference:** `templates/broadcast/episode_form.html:27`

### Program Card

Card used for displaying radio programs on the public site.

```html
<!-- templates/website/components/program_card.html -->
<a href="{{ program.get_absolute_url }}"
   class="block bg-white rounded-card shadow-card overflow-hidden
          hover:shadow-card-hover transition-all duration-250 group">
  <div class="aspect-[4/3] overflow-hidden">
    <img src="{{ program.cover_image.url }}" alt="{{ program.title }}"
         class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500">
  </div>
  <div class="p-5">
    <h3 class="font-heading font-bold text-coffee-700 group-hover:text-coffee-500 transition-colors">
      {{ program.title }}
    </h3>
    <p class="text-sm text-[#666666] mt-1 line-clamp-2">{{ program.description }}</p>
  </div>
</a>
```

### Article / Podcast Card

Similar pattern for news articles and podcast episodes. See `templates/website/components/article_card.html` and `templates/website/components/podcast_card.html`.

---

## Badges

### Status Badge (Published / Active)

```html
<!-- Published / Active -->
<span class="px-2 py-1 text-xs rounded-full bg-green-100 text-green-700
             dark:bg-green-900 dark:text-green-300">
  Published
</span>

<!-- Active -->
<span class="px-2 py-1 text-xs rounded-full bg-green-100 text-green-700
             dark:bg-green-900 dark:text-green-300">
  Active
</span>
```

**Reference:** `templates/broadcast/episode_list.html:61`, `templates/radio/station_list.html:59`

### Status Badge (Draft / Inactive)

```html
<!-- Draft -->
<span class="px-2 py-1 text-xs rounded-full bg-slate-100 text-slate-700
             dark:bg-slate-700 dark:text-slate-300">
  Draft
</span>

<!-- Inactive -->
<span class="px-2 py-1 text-xs rounded-full bg-red-100 text-red-700
             dark:bg-red-900 dark:text-red-300">
  Inactive
</span>
```

**Reference:** `templates/broadcast/episode_list.html:63`, `templates/radio/station_list.html:59`

### Live Badge (pulsing)

```html
<span class="w-2 h-2 bg-white rounded-full animate-pulse"></span>
<span class="px-2 py-1 text-xs rounded-full bg-red-600 text-white font-semibold">
  LIVE
</span>
```

### Role Badge

```html
<span class="text-xs text-slate-500">
  Sistem Peran:
  <span class="font-semibold text-slate-700 dark:text-slate-300">
    {{ user.get_role_display|default:"Tamu" }}
  </span>
</span>
```

**Reference:** `templates/dashboard_base.html:118`

---

## Tags

Tags are used for media file types, categories, and labels.

```html
<!-- Media type tag -->
<span class="px-2 py-1 text-xs font-medium rounded-md bg-coffee-100 text-coffee-600">
  IMAGE
</span>

<!-- Category tag -->
<span class="px-2 py-1 text-xs font-medium rounded-md bg-blue-100 text-blue-700">
  Berita
</span>

<!-- Keyword tag -->
<span class="px-2 py-1 text-xs font-medium rounded-md bg-yellow-100 text-yellow-700">
  Trending
</span>
```

---

## Avatars

### Initial Avatar (dashboard user menu)

```html
<div class="w-8 h-8 rounded-full bg-brand-500 text-white flex items-center justify-center font-bold">
  {{ user.username|slice:":1"|upper }}
</div>
```

**Reference:** `templates/dashboard_base.html:41`

### Avatar Sizes

| Size | Classes | Usage |
|---|---|---|
| XS | `w-6 h-6 text-xs` | Inline mentions |
| SM | `w-8 h-8 text-sm` | User menu, comments |
| MD | `w-10 h-10 text-base` | Table rows, list items |
| LG | `w-12 h-12 text-lg` | Profile page |

### Placeholder Avatar (no image)

```html
<div class="w-10 h-10 rounded-lg bg-slate-200 dark:bg-slate-600
            flex items-center justify-center">
  <svg class="w-5 h-5 text-slate-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
          d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
  </svg>
</div>
```

---

## Form Inputs

### Standard Text Input

```html
<input type="text"
       name="q"
       value="{{ search_form.q.value|default:'' }}"
       placeholder="Cari file..."
       class="flex-1 px-4 py-2 border border-gray-300 rounded-lg
              focus:ring-2 focus:ring-blue-500">
```

**Reference:** `templates/media_manager/list.html:13`

### Dashboard Input (dark mode aware)

```html
<input type="text" name="q" value="{{ search }}" placeholder="Cari episode..."
       class="flex-1 px-4 py-2 border border-slate-300 dark:border-slate-600 rounded-lg
              text-sm bg-white dark:bg-slate-800 text-slate-900 dark:text-white">
```

**Reference:** `templates/broadcast/episode_list.html:26`

### Search Modal Input (borderless)

```html
<input type="search"
       placeholder="Cari program, podcast, berita..."
       class="flex-1 bg-transparent text-lg text-slate-900 dark:text-white
              placeholder-slate-400 dark:placeholder-slate-500 focus:outline-none"
       autofocus>
```

**Reference:** `templates/website/components/search_modal.html:10`

### Select Dropdown

```html
<select name="type"
        class="px-4 py-2 border border-gray-300 rounded-lg">
  <option value="">Semua Tipe</option>
  <option value="IMAGE" {% if current_type == 'IMAGE' %}selected{% endif %}>Gambar</option>
  <option value="VIDEO" {% if current_type == 'VIDEO' %}selected{% endif %}>Video</option>
</select>
```

**Reference:** `templates/media_manager/list.html:14`

### Checkbox

```html
<label class="flex items-center gap-2">
  <input type="checkbox" name="is_public" checked
         class="form-checkbox h-4 w-4 text-blue-600">
  <span class="text-sm text-gray-700">Publik (bisa diakses semua orang)</span>
</label>
```

**Reference:** `templates/media_manager/upload.html:38`

---

## Dropdowns (Alpine.js)

```html
<div class="relative" x-data="{ open: false }">
  <button @click="open = !open" class="flex items-center gap-2 ...">
    Dropdown Label
  </button>
  <div x-show="open"
       @click.away="open = false"
       x-transition:enter="transition ease-out duration-200"
       x-transition:enter-start="opacity-0 translate-y-1"
       x-transition:enter-end="opacity-100 translate-y-0"
       x-transition:leave="transition ease-in duration-150"
       x-transition:leave-start="opacity-100 translate-y-0"
       x-transition:leave-end="opacity-0 translate-y-1"
       class="absolute right-0 mt-2 w-48 bg-white dark:bg-slate-800
              border border-slate-200 dark:border-slate-700 rounded-lg
              shadow-lg py-1 z-50 transition-all"
       style="display: none;">
    <a href="#" class="block px-4 py-2 text-sm text-slate-700 dark:text-slate-300
                      hover:bg-slate-100 dark:hover:bg-slate-700">Item</a>
  </div>
</div>
```

**Reference:** `templates/dashboard_base.html:39`, `templates/website/components/navbar.html:22`

---

## Tooltips

Tooltips are implemented via the `title` attribute for simple cases, and via Alpine.js for rich tooltips.

```html
<!-- Simple tooltip -->
<button title="Ubah Tema" class="...">
  <!-- icon -->
</button>

<!-- Alpine.js rich tooltip -->
<div class="relative" x-data="{ showTooltip: false }">
  <button @mouseenter="showTooltip = true" @mouseleave="showTooltip = false">
    <!-- trigger -->
  </button>
  <div x-show="showTooltip" x-transition
       class="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 px-3 py-1.5
              text-xs text-white bg-coffee-600 rounded-lg whitespace-nowrap z-50">
    Tooltip text
  </div>
</div>
```

---

## Keyboard Shortcut Indicators

Used in the navbar search trigger.

```html
<kbd class="hidden lg:inline-flex items-center px-1.5 py-0.5 text-[10px] font-mono
            text-coffee-300 bg-coffee-50 border border-coffee-200 rounded">
  ⌘K
</kbd>
```

**Reference:** `templates/website/components/navbar.html:94`

---

## Component Token Reference

| Token | Value | Usage |
|---|---|---|
| `coffee-400` | `#8C5A3C` | Primary CTA, active states |
| `coffee-500` | `#6B4226` | CTA hover, emphasis |
| `coffee-600` | `#4E2F1F` | Sidebar dark background |
| `coffee-700` | `#3A2318` | Heading text, logo |
| `coffee-200` | `#E7DDD3` | Borders, dividers |
| `coffee-50` | `#FAF7F3` | Hover backgrounds |
| `live` | `#E53935` | Live indicator, red accents |
| `success` | `#2F9E44` | Success states |
| `rounded-card` | `20px` | Card border radius |
| `shadow-card` | `0 10px 30px rgba(0,0,0,.08)` | Default card shadow |
| `shadow-card-hover` | `0 20px 40px rgba(0,0,0,.12)` | Card hover shadow |
