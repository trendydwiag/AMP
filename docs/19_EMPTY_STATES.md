# 19 — Empty States

Empty states display a friendly placeholder when no data is available. Each empty state follows the pattern: illustration/icon + message + optional CTA button.

---

## Pattern Structure

```html
<div class="flex flex-col items-center justify-center py-12 text-center">
  <!-- Icon / Illustration -->
  <div class="w-16 h-16 rounded-full bg-coffee-50 flex items-center justify-center mb-4">
    <svg class="w-8 h-8 text-coffee-300" fill="none" viewBox="0 0 24 24" stroke="currentColor"
         stroke-width="1.5">
      <!-- Context-specific icon -->
    </svg>
  </div>

  <!-- Title -->
  <h3 class="text-lg font-heading font-semibold text-slate-700 dark:text-slate-300">
    No Data Title
  </h3>

  <!-- Description -->
  <p class="text-sm text-slate-500 dark:text-slate-400 mt-1 max-w-sm">
    Description of what this empty state means and what the user can do.
  </p>

  <!-- CTA Button (optional) -->
  <a href="{% url 'some:create' %}"
     class="mt-4 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 text-sm font-medium">
    + Create New
  </a>
</div>
```

---

## No Media Files

```html
<!-- templates/media_manager/list.html (via {% empty %}) -->
<div class="col-span-full flex flex-col items-center justify-center py-12 text-center">
  <div class="w-16 h-16 rounded-full bg-coffee-50 flex items-center justify-center mb-4">
    <svg class="w-8 h-8 text-coffee-300" fill="none" viewBox="0 0 24 24" stroke="currentColor"
         stroke-width="1.5">
      <path stroke-linecap="round" stroke-linejoin="round"
            d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
    </svg>
  </div>
  <h3 class="text-lg font-heading font-semibold text-slate-700">Tidak ada file ditemukan</h3>
  <p class="text-sm text-slate-500 mt-1">Upload file media pertama Anda untuk memulai.</p>
  <a href="{% url 'media_manager:upload' %}"
     class="mt-4 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 text-sm font-medium">
    Upload File
  </a>
</div>
```

### Simple Text Empty State (existing pattern)

```html
<!-- Inline empty state within grid -->
<p class="col-span-full text-gray-500 text-sm">Tidak ada file ditemukan.</p>
```

**Reference:** `templates/media_manager/list.html:47`

---

## No Broadcasts / Episodes

```html
<div class="flex flex-col items-center justify-center py-12 text-center">
  <div class="w-16 h-16 rounded-full bg-coffee-50 flex items-center justify-center mb-4">
    <svg class="w-8 h-8 text-coffee-300" fill="none" viewBox="0 0 24 24" stroke="currentColor"
         stroke-width="1.5">
      <path stroke-linecap="round" stroke-linejoin="round"
            d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z" />
    </svg>
  </div>
  <h3 class="text-lg font-heading font-semibold text-slate-700 dark:text-slate-300">
    Belum ada episode
  </h3>
  <p class="text-sm text-slate-500 dark:text-slate-400 mt-1 max-w-sm">
    Buat episode pertama untuk memulai siaran Anda.
  </p>
  <a href="{% url 'broadcast:episode_create' %}"
     class="mt-4 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 text-sm font-medium">
    + Tambah Episode
  </a>
</div>
```

### Table Empty Row (existing pattern)

```html
{% empty %}
<tr>
  <td colspan="5" class="px-4 py-8 text-center text-slate-500 dark:text-slate-400">
    Belum ada episode
  </td>
</tr>
{% endfor %}
```

**Reference:** `templates/broadcast/episode_list.html:75-78`

---

## No Radio Stations

```html
<div class="flex flex-col items-center justify-center py-12 text-center">
  <div class="w-16 h-16 rounded-full bg-coffee-50 flex items-center justify-center mb-4">
    <svg class="w-8 h-8 text-coffee-300" fill="none" viewBox="0 0 24 24" stroke="currentColor"
         stroke-width="1.5">
      <path stroke-linecap="round" stroke-linejoin="round"
            d="M5.636 18.364a9 9 0 010-12.728m12.728 0a9 9 0 010 12.728m-9.9-2.829a5 5 0 010-7.07m7.072 0a5 5 0 010 7.07M13 12a1 1 0 11-2 0 1 1 0 012 0z" />
    </svg>
  </div>
  <h3 class="text-lg font-heading font-semibold text-slate-700 dark:text-slate-300">
    Belum ada station
  </h3>
  <p class="text-sm text-slate-500 dark:text-slate-400 mt-1 max-w-sm">
    Tambahkan stasiun radio pertama untuk memulai streaming.
  </p>
  <a href="{% url 'radio:station_create' %}"
     class="mt-4 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 text-sm font-medium">
    + Tambah Station
  </a>
</div>
```

### Table Empty Row

```html
{% empty %}
<tr>
  <td colspan="5" class="px-4 py-8 text-center text-slate-500 dark:text-slate-400">
    Belum ada station
  </td>
</tr>
{% endfor %}
```

**Reference:** `templates/radio/station_list.html:72-76`

---

## No News Articles

```html
<div class="flex flex-col items-center justify-center py-12 text-center">
  <div class="w-16 h-16 rounded-full bg-coffee-50 flex items-center justify-center mb-4">
    <svg class="w-8 h-8 text-coffee-300" fill="none" viewBox="0 0 24 24" stroke="currentColor"
         stroke-width="1.5">
      <path stroke-linecap="round" stroke-linejoin="round"
            d="M19 20H5a2 2 0 01-2-2V6a2 2 0 012-2h10a2 2 0 012 2v1m2 13a2 2 0 01-2-2V7m2 13a2 2 0 002-2V9a2 2 0 00-2-2h-2m-4-3H9M7 16h6M7 8h6v4H7V8z" />
    </svg>
  </div>
  <h3 class="text-lg font-heading font-semibold text-slate-700 dark:text-slate-300">
    Belum ada berita
  </h3>
  <p class="text-sm text-slate-500 dark:text-slate-400 mt-1 max-w-sm">
    Publikasikan artikel berita pertama untuk informasi pendengar.
  </p>
  <a href="#"
     class="mt-4 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 text-sm font-medium">
    + Tulis Berita
  </a>
</div>
```

---

## No Search Results

```html
<!-- Search modal empty state -->
<div class="flex flex-col items-center justify-center py-8 text-center">
  <svg class="w-12 h-12 text-slate-300 dark:text-slate-600 mb-3" fill="none" viewBox="0 0 24 24"
       stroke="currentColor" stroke-width="1.5">
    <path stroke-linecap="round" stroke-linejoin="round"
          d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
  </svg>
  <p class="text-sm text-slate-500 dark:text-slate-400">
    Tidak ada hasil untuk "{{ query }}"
  </p>
  <p class="text-xs text-slate-400 dark:text-slate-500 mt-1">
    Coba kata kunci lain atau periksa ejaan.
  </p>
</div>
```

**Reference:** `templates/website/components/search_modal.html:20-22`

---

## Empty State for Public Pages

The search modal has a "Ketik untuk mulai mencari..." placeholder.

```html
<div id="search-results" class="max-h-[50vh] overflow-y-auto p-4">
  <p class="text-center text-slate-400 dark:text-slate-500 text-sm py-8">
    Ketik untuk mulai mencari...
  </p>
</div>
```

**Reference:** `templates/website/components/search_modal.html:20-22`

---

## Empty State Styling Summary

| Property | Value |
|---|---|
| Container | `flex flex-col items-center justify-center py-12 text-center` |
| Icon circle | `w-16 h-16 rounded-full bg-coffee-50 flex items-center justify-center mb-4` |
| Icon size | `w-8 h-8 text-coffee-300` |
| Title | `text-lg font-heading font-semibold text-slate-700 dark:text-slate-300` |
| Description | `text-sm text-slate-500 dark:text-slate-400 mt-1 max-w-sm` |
| CTA button | `mt-4 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 text-sm font-medium` |
| Table empty | `px-4 py-8 text-center text-slate-500 dark:text-slate-400` with `colspan` |

---

## Icon Selection Guide

| Context | Icon | SVG Path |
|---|---|---|
| Media files | Image/photo | `M4 16l4.586-4.586a2 2 0 012.828 0...` |
| Episodes | Broadcast | `M19 11a7 7 0 01-7 7...` |
| Radio stations | Radio | `M5.636 18.364a9 9 0 010-12.728...` |
| News | Newspaper | `M19 20H5a2 2 0 01-2-2V6...` |
| Users | People | `M12 4.354a4 4 0 110 5.292...` |
| Search | Magnifying glass | `M21 21l-6-6m2-5a7 7 0 11-14 0...` |
