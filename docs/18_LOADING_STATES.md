# 18 — Loading States

Kabulhaden CMS uses several loading patterns to provide feedback during asynchronous operations: skeleton screens, spinners, progress bars, and HTMX loading indicators.

---

## Skeleton Screens

Skeleton screens show placeholder content while data loads. They use animated gradient backgrounds.

### Card Skeleton

```html
<div class="animate-pulse">
  <div class="aspect-[4/3] bg-coffee-100 rounded-card"></div>
  <div class="p-5 space-y-3">
    <div class="h-4 bg-coffee-100 rounded w-3/4"></div>
    <div class="h-3 bg-coffee-100 rounded w-full"></div>
    <div class="h-3 bg-coffee-100 rounded w-2/3"></div>
  </div>
</div>
```

### Table Row Skeleton

```html
<tr class="animate-pulse">
  <td class="px-4 py-3">
    <div class="h-4 bg-slate-200 rounded w-3/4"></div>
  </td>
  <td class="px-4 py-3">
    <div class="h-4 bg-slate-200 rounded w-1/2"></div>
  </td>
  <td class="px-4 py-3">
    <div class="h-4 bg-slate-200 rounded w-1/4"></div>
  </td>
</tr>
```

### List Item Skeleton

```html
<div class="flex items-center gap-4 p-4 animate-pulse">
  <div class="w-12 h-12 rounded-lg bg-slate-200"></div>
  <div class="flex-1 space-y-2">
    <div class="h-4 bg-slate-200 rounded w-1/3"></div>
    <div class="h-3 bg-slate-200 rounded w-2/3"></div>
  </div>
</div>
```

---

## Spinners

### Standard Spinner

```html
<div class="flex items-center justify-center py-12">
  <svg class="animate-spin h-8 w-8 text-coffee-400" fill="none" viewBox="0 0 24 24">
    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
    <path class="opacity-75" fill="currentColor"
          d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z">
    </path>
  </svg>
</div>
```

### Small Spinner (inline)

```html
<svg class="animate-spin h-4 w-4 text-white" fill="none" viewBox="0 0 24 24">
  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
  <path class="opacity-75" fill="currentColor"
        d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z">
  </path>
</svg>
```

---

## Progress Bars

### Upload Progress Bar

```html
<div class="w-full bg-slate-200 rounded-full h-2">
  <div class="bg-coffee-400 h-2 rounded-full transition-all duration-300"
       style="width: 45%">
  </div>
</div>
```

### Indeterminate Progress Bar

```html
<div class="w-full bg-slate-200 rounded-full h-1 overflow-hidden">
  <div class="h-full bg-coffee-400 rounded-full animate-[slide_1.5s_ease-in-out_infinite]"
       style="width: 40%">
  </div>
</div>
```

---

## Button Loading States

### Button with Spinner

```html
<button type="submit" disabled
        class="px-6 py-2 bg-blue-600 text-white rounded-lg font-medium
               flex items-center gap-2 opacity-75 cursor-not-allowed">
  <svg class="animate-spin h-4 w-4" fill="none" viewBox="0 0 24 24">
    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
    <path class="opacity-75" fill="currentColor"
          d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z">
    </path>
  </svg>
  Menyimpan...
</button>
```

### Alpine.js Button Loading

```html
<button x-data="{ loading: false }"
        @click="loading = true"
        :disabled="loading"
        class="px-6 py-2 bg-blue-600 text-white rounded-lg font-medium
               flex items-center gap-2 disabled:opacity-75 disabled:cursor-not-allowed">
  <svg x-show="loading" class="animate-spin h-4 w-4" fill="none" viewBox="0 0 24 24">
    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
    <path class="opacity-75" fill="currentColor"
          d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z">
    </path>
  </svg>
  <span x-text="loading ? 'Menyimpan...' : 'Simpan'">Simpan</span>
</button>
```

---

## HTMX Loading Indicators

### HTMX Indicator Classes

HTMX provides built-in loading indicator classes.

```html
<!-- Show spinner during HTMX request -->
<button hx-post="{% url 'broadcast:episode_delete' ep.pk %}"
        hx-confirm="Hapus episode ini?"
        hx-indicator=".htmx-spinner">
  Hapus
  <svg class="htmx-indicator animate-spin h-4 w-4" fill="none" viewBox="0 0 24 24">
    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
    <path class="opacity-75" fill="currentColor"
          d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z">
    </path>
  </svg>
</button>
```

### HTMX Loading State CSS

```css
.htmx-indicator {
  display: none;
}

.htmx-request .htmx-indicator {
  display: inline-block;
}

.htmx-request.htmx-indicator {
  display: inline-block;
}
```

### HTMX Target Swap Animation

```html
<!-- Fade in content after swap -->
<div hx-get="{% url 'broadcast:episode_list' %}"
     hx-trigger="revealed"
     hx-swap="innerHTML fade:300ms">
</div>
```

---

## Pulse Animation (Live Indicator)

Used for the live radio indicator.

```html
<span class="w-2 h-2 bg-white rounded-full animate-pulse"></span>
```

**Reference:** `templates/website/components/navbar.html:97`

---

## Wave Animation (Radio)

The radio module has a custom wave animation component.

**Template:** `templates/radio/components/wave_animation.html`

```html
<!-- Wave bars animation -->
<div class="flex items-end gap-1 h-4">
  <div class="w-1 bg-coffee-400 rounded-full animate-[wave_1s_ease-in-out_infinite]"
       style="height: 60%; animation-delay: 0s;"></div>
  <div class="w-1 bg-coffee-400 rounded-full animate-[wave_1s_ease-in-out_infinite]"
       style="height: 100%; animation-delay: 0.15s;"></div>
  <div class="w-1 bg-coffee-400 rounded-full animate-[wave_1s_ease-in-out_infinite]"
       style="height: 40%; animation-delay: 0.3s;"></div>
  <div class="w-1 bg-coffee-400 rounded-full animate-[wave_1s_ease-in-out_infinite]"
       style="height: 80%; animation-delay: 0.45s;"></div>
</div>
```

---

## Page Load Transitions

### Alpine.js Page Transition

```html
<div x-data="{ loaded: false }" x-init="loaded = true"
     x-transition:enter="transition ease-out duration-300"
     x-transition:enter-start="opacity-0"
     x-transition:enter-end="opacity-100">
  <!-- Page content fades in -->
</div>
```

### HTMX Page Transition

```html
<body hx-boost="true"
      hx-indicator="#page-loader">
  <!-- Global page loader -->
  <div id="page-loader" class="htmx-indicator fixed inset-0 z-50 flex items-center justify-center bg-white/80">
    <svg class="animate-spin h-8 w-8 text-coffee-400" fill="none" viewBox="0 0 24 24">
      <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
      <path class="opacity-75" fill="currentColor"
            d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z">
      </path>
    </svg>
  </div>
</body>
```

---

## Loading State Patterns Summary

| Pattern | Usage | Animation |
|---|---|---|
| Skeleton | Content placeholders | `animate-pulse` |
| Spinner | Inline/block loading | `animate-spin` |
| Progress bar | Upload/processing | Width transition |
| Pulse dot | Live indicator | `animate-pulse` |
| Wave bars | Radio playing | Custom `wave` keyframe |
| HTMX indicator | Request loading | `.htmx-indicator` |
| Button spinner | Form submission | `animate-spin` |
