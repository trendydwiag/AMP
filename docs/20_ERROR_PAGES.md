# 20 — Error Pages

Kabulhaden CMS has custom error pages for 400, 403, 404, and 500 errors. Each follows the same centered layout pattern with the coffee palette styling.

---

## Error Page Pattern

All error pages share the same layout structure:

```html
{% extends 'base.html' %}

{% block title %}Error Title (CODE) | {{ SITE_NAME }}{% endblock %}

{% block layout %}
<div class="min-h-screen flex items-center justify-center bg-slate-100 dark:bg-slate-900
            px-4 sm:px-6 lg:px-8 transition-colors duration-200">
  <div class="max-w-md w-full text-center space-y-6">
    <h1 class="text-7xl font-extrabold [COLOR]">{{ CODE }}</h1>
    <h2 class="text-2xl font-bold text-slate-800 dark:text-white">Error Title</h2>
    <p class="text-slate-500 dark:text-slate-400">Description message.</p>
    <div class="pt-4">
      <a href="{% url 'core:home' %}"
         class="inline-flex items-center px-4 py-2 bg-brand-500 hover:bg-brand-600 text-white
                text-sm font-semibold rounded-lg shadow-sm transition">
        Kembali ke Dashboard
      </a>
    </div>
  </div>
</div>
{% endblock %}
```

---

## 400 — Bad Request

**Template:** `templates/400.html`

```html
{% extends 'base.html' %}

{% block title %}Permintaan Tidak Valid (400) | {{ SITE_NAME }}{% endblock %}

{% block layout %}
<div class="min-h-screen flex items-center justify-center bg-slate-100 dark:bg-slate-900
            px-4 sm:px-6 lg:px-8 transition-colors duration-200">
  <div class="max-w-md w-full text-center space-y-6">
    <h1 class="text-7xl font-extrabold text-yellow-600 dark:text-yellow-400">400</h1>
    <h2 class="text-2xl font-bold text-slate-800 dark:text-white">Permintaan Tidak Valid</h2>
    <p class="text-slate-500 dark:text-slate-400">
      Permintaan Anda tidak dapat diproses. Silakan coba lagi.
    </p>
    <div class="pt-4">
      <a href="{% url 'core:home' %}"
         class="inline-flex items-center px-4 py-2 bg-brand-500 hover:bg-brand-600 text-white
                text-sm font-semibold rounded-lg shadow-sm transition">
        Kembali ke Dashboard
      </a>
    </div>
  </div>
</div>
{% endblock %}
```

**Reference:** `templates/400.html`

---

## 403 — Forbidden

**Template:** `templates/403.html`

```html
{% extends 'base.html' %}

{% block title %}Akses Ditolak (403) | {{ SITE_NAME }}{% endblock %}

{% block layout %}
<div class="min-h-screen flex items-center justify-center bg-slate-100 dark:bg-slate-900
            px-4 sm:px-6 lg:px-8 transition-colors duration-200">
  <div class="max-w-md w-full text-center space-y-6">
    <h1 class="text-7xl font-extrabold class text-red-600 dark:text-red-400">403</h1>
    <h2 class="text-2xl font-bold text-slate-800 dark:text-white">Akses Dilarang</h2>
    <p class="text-slate-500 dark:text-slate-400">
      Anda tidak memiliki izin (role yang cukup) untuk mengakses halaman atau resource ini.
    </p>
    <div class="pt-4">
      <a href="{% url 'core:home' %}"
         class="inline-flex items-center px-4 py-2 bg-brand-500 hover:bg-brand-600 text-white
                text-sm font-semibold rounded-lg shadow-sm transition">
        Kembali ke Dashboard
      </a>
    </div>
  </div>
</div>
{% endblock %}
```

**Reference:** `templates/403.html`

---

## 404 — Not Found

**Template:** `templates/404.html`

```html
{% extends 'base.html' %}

{% block title %}Halaman Tidak Ditemukan (404) | {{ SITE_NAME }}{% endblock %}

{% block layout %}
<div class="min-h-screen flex items-center justify-center bg-slate-100 dark:bg-slate-900
            px-4 sm:px-6 lg:px-8 transition-colors duration-200">
  <div class="max-w-md w-full text-center space-y-6">
    <h1 class="text-7xl font-extrabold text-brand-500 dark:text-blue-400">404</h1>
    <h2 class="text-2xl font-bold text-slate-800 dark:text-white">Halaman Tidak Ditemukan</h2>
    <p class="text-slate-500 dark:text-slate-400">
      Maaf, halaman yang Anda cari tidak tersedia atau telah dipindahkan.
    </p>
    <div class="pt-4">
      <a href="{% url 'core:home' %}"
         class="inline-flex items-center px-4 py-2 bg-brand-500 hover:bg-brand-600 text-white
                text-sm font-semibold rounded-lg shadow-sm transition">
        Kembali ke Dashboard
      </a>
    </div>
  </div>
</div>
{% endblock %}
```

**Reference:** `templates/404.html`

### Public Site 404

**Template:** `templates/website/404.html`

```html
{% extends 'website/main.html' %}

{% block title %}Halaman Tidak Ditemukan | {{ SITE_NAME }}{% endblock %}

{% block content %}
<div class="min-h-[60vh] flex items-center justify-center px-4">
  <div class="text-center space-y-6">
    <h1 class="text-7xl font-extrabold text-coffee-400">404</h1>
    <h2 class="text-2xl font-heading font-bold text-coffee-700">Halaman Tidak Ditemukan</h2>
    <p class="text-[#666666] max-w-md mx-auto">
      Maaf, halaman yang Anda cari tidak tersedia atau telah dipindahkan.
    </p>
    <a href="{% url 'website:home' %}"
       class="inline-flex items-center px-6 py-3 bg-coffee-400 text-white rounded-xl
              font-heading font-semibold text-sm hover:bg-coffee-500 transition-all
              shadow-md hover:shadow-lg active:scale-[.98]">
      Kembali ke Beranda
    </a>
  </div>
</div>
{% endblock %}
```

---

## 500 — Server Error

**Template:** `templates/500.html`

```html
{% extends 'base.html' %}

{% block title %}Masalah Server Internal (500) | {{ SITE_NAME }}{% endblock %}

{% block layout %}
<div class="min-h-screen flex items-center justify-center bg-slate-100 dark:bg-slate-900
            px-4 sm:px-6 lg:px-8 transition-colors duration-200">
  <div class="max-w-md w-full text-center space-y-6">
    <h1 class="text-7xl font-extrabold text-red-600 dark:text-red-400">500</h1>
    <h2 class="text-2xl font-bold text-slate-800 dark:text-white">Kesalahan Server Internal</h2>
    <p class="text-slate-500 dark:text-slate-400">
      Terjadi gangguan internal pada server kami. Teknisi kami telah mendokumentasikan error ini
      dan sedang memperbaikinya.
    </p>
    <div class="pt-4">
      <a href="{% url 'core:home' %}"
         class="inline-flex items-center px-4 py-2 bg-brand-500 hover:bg-brand-600 text-white
                text-sm font-semibold rounded-lg shadow-sm transition">
        Kembali ke Dashboard
      </a>
    </div>
  </div>
</div>
{% endblock %}
```

**Reference:** `templates/500.html`

---

## Error Page Styling Summary

| Error | Number Color | Title |
|---|---|---|
| 400 | `text-yellow-600 dark:text-yellow-400` | Permintaan Tidak Valid |
| 403 | `text-red-600 dark:text-red-400` | Akses Dilarang |
| 404 | `text-brand-500 dark:text-blue-400` | Halaman Tidak Ditemukan |
| 500 | `text-red-600 dark:text-red-400` | Kesalahan Server Internal |

---

## Error Page Layout Properties

| Property | Value |
|---|---|
| Container | `min-h-screen flex items-center justify-center` |
| Background | `bg-slate-100 dark:bg-slate-900` |
| Max width | `max-w-md` |
| Error code | `text-7xl font-extrabold` |
| Title | `text-2xl font-bold text-slate-800 dark:text-white` |
| Description | `text-slate-500 dark:text-slate-400` |
| CTA button | `bg-brand-500 hover:bg-brand-600 text-white text-sm font-semibold rounded-lg shadow-sm transition` |
| Padding | `px-4 sm:px-6 lg:px-8` |
| Transition | `transition-colors duration-200` |

---

## Django Configuration

Error pages are configured in the root URLconf.

```python
# config/urls.py
handler400 = 'core.views.bad_request'
handler403 = 'core.views.permission_denied'
handler404 = 'core.views.page_not_found'
handler500 = 'core.views.server_error'
```

Django automatically looks for `400.html`, `403.html`, `404.html`, `500.html` in the `templates/` directory.

---

## User Flow After Error

All error pages provide a single escape route:

- **Dashboard errors (400, 403, 404, 500):** "Kembali ke Dashboard" → `core:home`
- **Public 404:** "Kembali ke Beranda" → `website:home`
