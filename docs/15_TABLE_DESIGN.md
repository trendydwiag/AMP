# 15 — Table Design

Data tables in the admin dashboard use a consistent pattern with Tailwind CSS. Tables appear in broadcast, radio, media, and user management modules.

---

## Base Table Structure

```html
<div class="overflow-x-auto">
  <table class="min-w-full divide-y divide-slate-200 dark:divide-slate-700">
    <thead class="bg-slate-50 dark:bg-slate-700/50">
      <tr>
        <th class="px-4 py-3 text-left text-xs font-medium text-slate-500 dark:text-slate-400 uppercase">
          Column Header
        </th>
      </tr>
    </thead>
    <tbody class="divide-y divide-slate-200 dark:divide-slate-700">
      {% for item in items %}
      <tr class="hover:bg-slate-50 dark:hover:bg-slate-700/30">
        <td class="px-4 py-3">Content</td>
      </tr>
      {% empty %}
      <tr>
        <td colspan="5" class="px-4 py-8 text-center text-slate-500 dark:text-slate-400">
          No data message
        </td>
      </tr>
      {% endfor %}
    </tbody>
  </table>
</div>
```

---

## Table Header

```html
<thead class="bg-slate-50 dark:bg-slate-700/50">
  <tr>
    <th class="px-4 py-3 text-left text-xs font-medium text-slate-500 dark:text-slate-400 uppercase">
      Episode
    </th>
    <th class="px-4 py-3 text-left text-xs font-medium text-slate-500 dark:text-slate-400 uppercase">
      Program
    </th>
    <th class="px-4 py-3 text-left text-xs font-medium text-slate-500 dark:text-slate-400 uppercase">
      Status
    </th>
    <th class="px-4 py-3 text-left text-xs font-medium text-slate-500 dark:text-slate-400 uppercase">
      Tanggal
    </th>
    <th class="px-4 py-3 text-left text-xs font-medium text-slate-500 dark:text-slate-400 uppercase">
      Aksi
    </th>
  </tr>
</thead>
```

**Header classes:**
- `px-4 py-3` — Cell padding
- `text-left` — Left-aligned
- `text-xs font-medium` — Small, medium weight
- `text-slate-500 dark:text-slate-400` — Muted color
- `uppercase` — All caps

**Reference:** `templates/broadcast/episode_list.html:38-45`, `templates/radio/station_list.html:28-34`

---

## Striped / Hover Rows

Tables use hover states rather than zebra striping.

```html
<!-- Hover row -->
<tr class="hover:bg-slate-50 dark:hover:bg-slate-700/30">

<!-- Row divider -->
<tbody class="divide-y divide-slate-200 dark:divide-slate-700">
```

---

## Table Cell Patterns

### Text Cell

```html
<td class="px-4 py-3 text-sm text-slate-600 dark:text-slate-400">
  {{ ep.program.title }}
</td>
```

### Primary Content Cell (title + subtitle)

```html
<td class="px-4 py-3">
  <div>
    <p class="font-medium text-slate-900 dark:text-white">
      E{{ ep.episode_number }}: {{ ep.title }}
    </p>
    {% if ep.description %}
    <p class="text-sm text-slate-500 dark:text-slate-400 line-clamp-1">
      {{ ep.description|truncatewords:10 }}
    </p>
    {% endif %}
  </div>
</td>
```

**Reference:** `templates/broadcast/episode_list.html:50-56`

### Cell with Icon + Text

```html
<td class="px-4 py-3">
  <div class="flex items-center gap-3">
    {% if s.logo %}
    <img src="{{ s.logo.url }}" class="w-10 h-10 rounded-lg object-cover">
    {% else %}
    <div class="w-10 h-10 rounded-lg bg-slate-200 dark:bg-slate-600 flex items-center justify-center">
      <svg class="w-5 h-5 text-slate-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <!-- default icon -->
      </svg>
    </div>
    {% endif %}
    <div>
      <p class="font-medium text-slate-900 dark:text-white">{{ s.station_name }}</p>
      <p class="text-sm text-slate-500 dark:text-slate-400">{{ s.timezone }}</p>
    </div>
  </div>
</td>
```

**Reference:** `templates/radio/station_list.html:39-55`

### Date Cell

```html
<td class="px-4 py-3 text-sm text-slate-500 dark:text-slate-400">
  {{ ep.publish_date|date:"d M Y"|default:"-" }}
</td>
```

**Reference:** `templates/broadcast/episode_list.html:66`

### Status Badge Cell

```html
<td class="px-4 py-3">
  {% if ep.published %}
  <span class="px-2 py-1 text-xs rounded-full bg-green-100 text-green-700
               dark:bg-green-900 dark:text-green-300">
    Published
  </span>
  {% else %}
  <span class="px-2 py-1 text-xs rounded-full bg-slate-100 text-slate-700
               dark:bg-slate-700 dark:text-slate-300">
    Draft
  </span>
  {% endif %}
</td>
```

**Reference:** `templates/broadcast/episode_list.html:59-65`

### Active/Inactive Badge Cell

```html
<td class="px-4 py-3">
  <span class="px-2 py-1 text-xs rounded-full
               {% if s.is_active %}
                 bg-green-100 text-green-700 dark:bg-green-900 dark:text-green-300
               {% else %}
                 bg-red-100 text-red-700 dark:bg-red-900 dark:text-red-300
               {% endif %}">
    {% if s.is_active %}Active{% else %}Inactive{% endif %}
  </span>
</td>
```

**Reference:** `templates/radio/station_list.html:58-62`

### Actions Cell

```html
<td class="px-4 py-3 flex gap-2">
  <a href="{% url 'broadcast:episode_edit' ep.pk %}"
     class="text-blue-600 hover:text-blue-700 dark:text-blue-400 text-sm">
    Edit
  </a>
  <form method="post" action="{% url 'broadcast:episode_delete' ep.pk %}"
        onsubmit="return confirm('Hapus episode ini?')">
    {% csrf_token %}
    <button type="submit" class="text-red-600 hover:text-red-700 dark:text-red-400 text-sm">
      Hapus
    </button>
  </form>
</td>
```

**Reference:** `templates/broadcast/episode_list.html:67-72`

### Toggle Action Cell (activate/deactivate)

```html
<td class="px-4 py-3">
  <div class="flex items-center gap-3">
    <a href="{% url 'radio:station_edit' s.pk %}"
       class="text-blue-600 hover:text-blue-700 dark:text-blue-400 text-sm">Edit</a>
    <a href="{% url 'radio:station_delete' s.pk %}"
       class="{% if s.is_active %}
                 text-yellow-600 hover:text-yellow-700 dark:text-yellow-400
               {% else %}
                 text-green-600 hover:text-green-700 dark:text-green-400
               {% endif %} text-sm">
      {% if s.is_active %}Nonaktifkan{% else %}Aktifkan{% endif %}
    </a>
  </div>
</td>
```

**Reference:** `templates/radio/station_list.html:63-68`

---

## Bulk Actions

Media manager implements bulk delete with checkboxes.

```html
<form method="post" action="{% url 'media_manager:bulk_delete' %}">
  {% csrf_token %}
  <div id="media-grid" class="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-4">
    {% for file in files %}
    <div class="bg-white shadow rounded-lg overflow-hidden hover:shadow-md
                transition-shadow relative group">
      <input type="checkbox" name="file_ids" value="{{ file.pk }}"
             class="absolute top-2 left-2 z-10 opacity-0 group-hover:opacity-100
                    transition-opacity">
      <!-- file card content -->
    </div>
    {% endfor %}
  </div>
  {% if files %}
  <div class="mt-4 flex justify-end">
    <button type="submit" onclick="return confirm('Hapus file terpilih?')"
            class="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 text-sm">
      Hapus Terpilih
    </button>
  </div>
  {% endif %}
</form>
```

**Reference:** `templates/media_manager/list.html:24-57`

---

## Pagination

### Basic Pagination

```html
{% if is_paginated %}
<div class="flex justify-center gap-2">
  {% if page_obj.has_previous %}
  <a href="?page={{ page_obj.previous_page_number }}"
     class="px-3 py-1 bg-gray-100 rounded">Sebelumnya</a>
  {% endif %}
  <span class="px-3 py-1">
    Halaman {{ page_obj.number }} dari {{ page_obj.paginator.num_pages }}
  </span>
  {% if page_obj.has_next %}
  <a href="?page={{ page_obj.next_page_number }}"
     class="px-3 py-1 bg-gray-100 rounded">Selanjutnya</a>
  {% endif %}
</div>
{% endif %}
```

**Reference:** `templates/media_manager/list.html:60-70`

---

## Empty State (within table)

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

The `colspan` value must match the number of columns in the table.

---

## Dashboard Table Examples

| Module | Template | Columns |
|---|---|---|
| Broadcast Episodes | `templates/broadcast/episode_list.html` | Episode, Program, Status, Tanggal, Aksi |
| Radio Stations | `templates/radio/station_list.html` | Station, Genre, Volume, Status, Aksi |
| Media Files | `templates/media_manager/list.html` | Grid layout (not table) with bulk checkboxes |
| User Management | `templates/users/admin/user_list.html` | User details, role, actions |

---

## Responsive Tables

Tables use `overflow-x-auto` on the wrapper for horizontal scrolling on small screens.

```html
<div class="overflow-x-auto">
  <table class="min-w-full ...">
```

---

## Table Container

Tables sit inside the dashboard content card, which is the white container with rounded corners.

```html
<div class="flex-1 bg-white dark:bg-slate-800 rounded-xl shadow-sm
            border border-slate-200 dark:border-slate-700 p-6 transition-colors duration-200">
  <div class="space-y-6">
    <!-- Page header with title + create button -->
    <!-- Search/filter form -->
    <!-- Table -->
  </div>
</div>
```
