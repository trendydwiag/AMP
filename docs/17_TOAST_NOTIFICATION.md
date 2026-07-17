# 17 — Toast Notification

Feedback messages in Kabulhaden CMS use Django's messages framework with consistent Tailwind CSS styling. Messages appear as dismissible banners at the top of the content area.

---

## Django Messages Framework Integration

### Backend (View)

```python
from django.contrib import messages

def my_view(request):
    # Success message
    messages.success(request, 'Episode berhasil disimpan.')

    # Error message
    messages.error(request, 'Gagal menghapus file.')

    # Warning message
    messages.warning(request, 'Ukuran file melebihi batas.')

    # Info message (default)
    messages.info(request, 'Proses upload sedang berlangsung.')
```

### Frontend (Template)

Messages are rendered in the dashboard base template, above the content block.

```html
<!-- templates/dashboard_base.html -->
{% if messages %}
<div class="mb-6 space-y-2">
    {% for message in messages %}
    <div x-data="{ show: true }" x-show="show"
         class="p-4 rounded-lg flex items-center justify-between transition-opacity duration-300
                {% if message.tags == 'success' %}
                  bg-green-50 text-green-800 dark:bg-green-950 dark:text-green-300
                  border border-green-200 dark:border-green-800
                {% elif message.tags == 'error' or message.tags == 'danger' %}
                  bg-red-50 text-red-800 dark:bg-red-950 dark:text-red-300
                  border border-red-200 dark:border-red-800
                {% elif message.tags == 'warning' %}
                  bg-yellow-50 text-yellow-800 dark:bg-yellow-950 dark:text-yellow-300
                  border border-yellow-200 dark:border-yellow-800
                {% else %}
                  bg-blue-50 text-blue-800 dark:bg-blue-950 dark:text-blue-300
                  border border-blue-200 dark:border-blue-800
                {% endif %}">
        <div class="flex items-center gap-2">
            <span>{{ message }}</span>
        </div>
        <button @click="show = false" class="hover:opacity-70 p-1">
            <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M6 18L18 6M6 6l12 12" />
            </svg>
        </button>
    </div>
    {% endfor %}
</div>
{% endif %}
```

**Reference:** `templates/dashboard_base.html:137-152`

---

## Message Types

| Type | Django Tag | Background | Text | Border |
|---|---|---|---|---|
| Success | `success` | `bg-green-50` | `text-green-800` | `border-green-200` |
| Error | `error` / `danger` | `bg-red-50` | `text-red-800` | `border-red-200` |
| Warning | `warning` | `bg-yellow-50` | `text-yellow-800` | `border-yellow-200` |
| Info | `info` / default | `bg-blue-50` | `text-blue-800` | `border-blue-200` |

### Dark Mode Variants

| Type | Background | Text | Border |
|---|---|---|---|
| Success | `dark:bg-green-950` | `dark:text-green-300` | `dark:border-green-800` |
| Error | `dark:bg-red-950` | `dark:text-red-300` | `dark:border-red-800` |
| Warning | `dark:bg-yellow-950` | `dark:text-yellow-300` | `dark:border-yellow-800` |
| Info | `dark:bg-blue-950` | `dark:text-blue-300` | `dark:border-blue-800` |

---

## Auth Page Messages

Auth pages have a slightly different message rendering (no Alpine.js dismiss, smaller text).

```html
<!-- templates/users/login.html -->
{% if messages %}
<div class="mb-4 space-y-2">
    {% for message in messages %}
    <div class="p-3 rounded-lg text-sm
                {% if message.tags == 'error' %}
                  bg-red-50 text-red-800 dark:bg-red-950 dark:text-red-300
                  border border-red-200 dark:border-red-800
                {% elif message.tags == 'success' %}
                  bg-green-50 text-green-800 dark:bg-green-950 dark:text-green-300
                  border border-green-200 dark:border-green-800
                {% elif message.tags == 'warning' %}
                  bg-yellow-50 text-yellow-800 dark:bg-yellow-950 dark:text-yellow-300
                  border border-yellow-200 dark:border-yellow-800
                {% else %}
                  bg-blue-50 text-blue-800 dark:bg-blue-950 dark:text-blue-300
                  border border-blue-200 dark:border-blue-800
                {% endif %}">
        {{ message }}
    </div>
    {% endfor %}
</div>
{% endif %}
```

**Reference:** `apps/users/templates/users/login.html:8-16`

---

## Settings Page Messages

Settings pages have a simpler message pattern.

```html
<!-- templates/settings/base.html -->
{% if messages %}
{% for message in messages %}
<div class="mb-4 p-4 rounded-lg
            {% if message.tags == 'success' %}
              bg-green-50 text-green-800 border border-green-200
            {% elif message.tags == 'error' %}
              bg-red-50 text-red-800 border border-red-200
            {% else %}
              bg-blue-50 text-blue-800 border border-blue-200
            {% endif %}">
  {{ message }}
</div>
{% endfor %}
{% endif %}
```

**Reference:** `templates/settings/base.html:17-23`

---

## Dismiss Behavior

### Alpine.js Auto-dismiss Pattern

Messages can be auto-dismissed using Alpine.js with a timeout.

```html
<div x-data="{ show: true }"
     x-show="show"
     x-init="setTimeout(() => show = false, 5000)"
     class="p-4 rounded-lg ...">
  <span>{{ message }}</span>
</div>
```

### Manual Dismiss

Current implementation uses a manual close button.

```html
<button @click="show = false" class="hover:opacity-70 p-1">
  <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
          d="M6 18L18 6M6 6l12 12" />
  </svg>
</button>
```

**Reference:** `templates/dashboard_base.html:144-148`

---

## Auto-dismiss Timing

| Message Type | Recommended Duration | Reason |
|---|---|---|
| Success | 5 seconds | Quick acknowledgment |
| Info | 5 seconds | Informational |
| Warning | 8 seconds | Needs more reading time |
| Error | No auto-dismiss | User needs to read and act |

---

## Toast Container Positioning

Messages appear in the dashboard content area, above the content card, with `mb-6` spacing.

```html
<main class="flex-1 min-w-0 flex flex-col p-4 sm:p-6 lg:p-8">
    <!-- Breadcrumbs -->
    <nav class="flex text-sm text-slate-500 dark:text-slate-400 mb-4">...</nav>

    <!-- Flash Messages -->
    {% if messages %}
    <div class="mb-6 space-y-2">
        <!-- messages here -->
    </div>
    {% endif %}

    <!-- Content Card -->
    <div class="flex-1 bg-white dark:bg-slate-800 rounded-xl shadow-sm ...">
        {% block content %}{% endblock %}
    </div>
</main>
```

---

## Message Styling Summary

| Property | Value |
|---|---|
| Container | `mb-6 space-y-2` |
| Message box | `p-4 rounded-lg flex items-center justify-between` |
| Transition | `transition-opacity duration-300` |
| Close button | `hover:opacity-70 p-1` |
| Close icon | 16x16 (`h-4 w-4`) X icon |
| Text size | Default (16px) on dashboard, `text-sm` on auth pages |
