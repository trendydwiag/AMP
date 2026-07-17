# 24 — Dark Mode

Kabulhaden CMS has a dark mode toggle in the admin dashboard, implemented via Alpine.js and Tailwind's `dark:` prefix with `class` strategy. The public site does not currently support dark mode.

---

## Implementation Strategy

### Tailwind Configuration

```javascript
// tailwind.config.js (CDN fallback in base.html)
tailwind.config = {
  darkMode: 'class',
  // ...
}
```

**Reference:** `templates/base.html:24`

### Alpine.js State Management

```html
<div x-data="{ sidebarOpen: false, darkMode: localStorage.getItem('theme') === 'dark' }">
```

**Reference:** `templates/dashboard_base.html:4`

### Toggle Mechanism

```html
<button @click="
    darkMode = !darkMode;
    localStorage.setItem('theme', darkMode ? 'dark' : 'light');
    if (darkMode) {
        document.documentElement.classList.add('dark');
    } else {
        document.documentElement.classList.remove('dark');
    }
" class="text-slate-500 hover:text-slate-600 dark:text-slate-400 dark:hover:text-slate-300
         p-2 rounded-lg hover:bg-slate-100 dark:hover:bg-slate-700" title="Ubah Tema">
  <!-- Moon icon (when light) -->
  <svg x-show="!darkMode" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
          d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
  </svg>
  <!-- Sun icon (when dark) -->
  <svg x-show="darkMode" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"
       style="display: none;">
    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
          d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364-6.364l-.707.707M6.343 17.657l-.707.707m0-12.728l.707.707m12.728 12.728l.707.707M12 8a4 4 0 100 8 4 4 0 000-8z" />
  </svg>
</button>
```

**Reference:** `templates/dashboard_base.html:22-35`

---

## Color Mappings

### Background Colors

| Element | Light Mode | Dark Mode | Tailwind Classes |
|---|---|---|---|
| Page body | `#FAF7F3` | `slate-900` | `bg-[#FAF7F3] dark:bg-slate-900` |
| Sidebar | white | `slate-800` | `bg-white dark:bg-slate-800` |
| Content card | white | `slate-800` | `bg-white dark:bg-slate-800` |
| Header | white | `slate-800` | `bg-white dark:bg-slate-800` |
| Table header | `slate-50` | `slate-700/50` | `bg-slate-50 dark:bg-slate-700/50` |
| Table row hover | `slate-50` | `slate-700/30` | `hover:bg-slate-50 dark:hover:bg-slate-700/30` |

### Text Colors

| Element | Light Mode | Dark Mode | Tailwind Classes |
|---|---|---|---|
| Headings | `slate-900` | white | `text-slate-900 dark:text-white` |
| Body text | `slate-600` | `slate-400` | `text-slate-600 dark:text-slate-400` |
| Muted text | `slate-500` | `slate-400` | `text-slate-500 dark:text-slate-400` |
| Labels | `slate-700` | `slate-300` | `text-slate-700 dark:text-slate-300` |

### Border Colors

| Element | Light Mode | Dark Mode | Tailwind Classes |
|---|---|---|---|
| Standard border | `slate-200` | `slate-700` | `border-slate-200 dark:border-slate-700` |
| Input border | `slate-300` | `slate-600` | `border-slate-300 dark:border-slate-600` |

### Status Badge Colors (Dark Mode)

| Status | Light Mode | Dark Mode |
|---|---|---|
| Published/Active | `bg-green-100 text-green-700` | `bg-green-900 text-green-300` |
| Draft | `bg-slate-100 text-slate-700` | `bg-slate-700 text-slate-300` |
| Inactive | `bg-red-100 text-red-700` | `bg-red-900 text-red-300` |

**Reference:** `templates/broadcast/episode_list.html:60-64`

### Toast Notification Colors (Dark Mode)

| Type | Light Mode | Dark Mode |
|---|---|---|
| Success | `bg-green-50 text-green-800 border-green-200` | `bg-green-950 text-green-300 border-green-800` |
| Error | `bg-red-50 text-red-800 border-red-200` | `bg-red-950 text-red-300 border-red-800` |
| Warning | `bg-yellow-50 text-yellow-800 border-yellow-200` | `bg-yellow-950 text-yellow-300 border-yellow-800` |
| Info | `bg-blue-50 text-blue-800 border-blue-200` | `bg-blue-950 text-blue-300 border-blue-800` |

**Reference:** `templates/dashboard_base.html:140`

---

## Coffee Palette → Dark Variants

The coffee palette is not directly mapped in dark mode. Instead, the dashboard uses Tailwind's `slate` scale for dark mode backgrounds and text, while the public site retains the coffee palette.

| Coffee Token | Light Usage | Dark Alternative |
|---|---|---|
| coffee-50 | `#FAF7F3` bg | Not used in dark |
| coffee-100 | Hover bg, borders | `slate-700` |
| coffee-200 | Border | `slate-600` |
| coffee-300 | Muted text | `slate-400` |
| coffee-400 | Primary CTA | Retained (sufficient contrast) |
| coffee-500 | CTA hover | Retained |
| coffee-600 | Active link | `blue-400` (in dashboard) |
| coffee-700 | Headings | `white` |
| coffee-800 | Dark text | `slate-200` |

---

## Persistence

Dark mode preference is stored in `localStorage`.

```javascript
// On page load (in x-data)
darkMode: localStorage.getItem('theme') === 'dark'

// On toggle
localStorage.setItem('theme', darkMode ? 'dark' : 'light');
document.documentElement.classList.add('dark'); // or remove
```

**Reference:** `templates/dashboard_base.html:4`, `templates/dashboard_base.html:22-25`

---

## Dark Mode Scope

| Area | Dark Mode Support |
|---|---|
| Admin dashboard | Yes (toggle in header) |
| Auth pages | Yes (passive, no toggle) |
| Error pages | Yes (passive, no toggle) |
| Public website | No (not implemented) |
| Settings pages | Partial (some inconsistencies) |

---

## Transition Smoothness

Dark mode changes use `transition-colors duration-200` on elements.

```html
<div class="bg-white dark:bg-slate-800 transition-colors duration-200">
```

**Reference:** `templates/dashboard_base.html:155`

---

## Future Dark Mode Improvements

1. Add system preference detection (`prefers-color-scheme`)
2. Extend dark mode to public website
3. Add dark mode toggle to public navbar
4. Unify coffee palette dark variants
5. Add `dark:` classes to all settings sub-pages
