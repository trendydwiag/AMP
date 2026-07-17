# 14 — Form Design

Forms in Kabulhaden CMS follow consistent patterns for input styling, validation, error handling, and label conventions. Indonesian labels are used throughout the interface.

---

## Input Styling

### Standard Text Input

```html
<input type="text"
       name="q"
       value="{{ search_form.q.value|default:'' }}"
       placeholder="Cari file..."
       class="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500">
```

**Reference:** `templates/media_manager/list.html:13`

### Dashboard Input (dark mode aware)

```html
<input type="text" name="q" value="{{ search }}" placeholder="Cari episode..."
       class="flex-1 px-4 py-2 border border-slate-300 dark:border-slate-600 rounded-lg
              text-sm bg-white dark:bg-slate-800 text-slate-900 dark:text-white">
```

**Reference:** `templates/broadcast/episode_list.html:26`

### Auth Input

```html
<label for="id_username" class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">
  Username
</label>
{{ form.username }}
{% if form.username.errors %}
<p class="mt-1 text-xs text-red-600 dark:text-red-400">{{ form.username.errors.0 }}</p>
{% endif %}
```

**Reference:** `apps/users/templates/users/login.html:29-34`

---

## Input States

| State | Classes |
|---|---|
| Default | `border border-gray-300 dark:border-slate-600 rounded-lg` |
| Focus | `focus:ring-2 focus:ring-blue-500 focus:border-blue-500` |
| Error | `border border-red-300 focus:ring-red-500 focus:border-red-500` |
| Disabled | `bg-gray-100 dark:bg-slate-700 cursor-not-allowed opacity-50` |

---

## Select Dropdown

```html
<select name="type"
        class="px-4 py-2 border border-gray-300 rounded-lg">
  <option value="">Semua Tipe</option>
  <option value="IMAGE" {% if current_type == 'IMAGE' %}selected{% endif %}>Gambar</option>
  <option value="VIDEO" {% if current_type == 'VIDEO' %}selected{% endif %}>Video</option>
  <option value="DOCUMENT" {% if current_type == 'DOCUMENT' %}selected{% endif %}>Dokumen</option>
  <option value="AUDIO" {% if current_type == 'AUDIO' %}selected{% endif %}>Audio</option>
</select>
```

**Reference:** `templates/media_manager/list.html:14`

### Program Filter Select

```html
<select name="program"
        class="px-4 py-2 border border-slate-300 dark:border-slate-600 rounded-lg
               text-sm bg-white dark:bg-slate-800 text-slate-900 dark:text-white">
  <option value="">Semua Program</option>
  {% for p in programs %}
  <option value="{{ p.pk }}"
          {% if selected_program == p.pk|stringformat:"s" %}selected{% endif %}>
    {{ p.title }}
  </option>
  {% endfor %}
</select>
```

**Reference:** `templates/broadcast/episode_list.html:27`

---

## File Input

### Drag-and-Drop Upload Zone

```html
<div id="drop-zone"
     class="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center
            hover:border-blue-400 transition-colors cursor-pointer"
     x-data="{ dragover: false }"
     @dragover.prevent="dragover = true"
     @dragleave.prevent="dragover = false"
     @drop.prevent="dragover = false;
                    $refs.fileInput.files = $event.dataTransfer.files;
                    $refs.fileInput.dispatchEvent(new Event('change'))"
     :class="{ 'border-blue-400 bg-blue-50': dragover }">
  <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor"
       viewBox="0 0 24 24">
    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
          d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"/>
  </svg>
  <p class="mt-2 text-sm text-gray-600">
    Seret file ke sini atau
    <span class="text-blue-600 font-medium">klik untuk memilih</span>
  </p>
  <p class="mt-1 text-xs text-gray-500">
    Gambar, Video, Audio, Dokumen (maks. 10MB per file)
  </p>
</div>

<input type="file" name="files" x-ref="fileInput" multiple
       accept="image/*,video/*,audio/*,.pdf,.doc,.docx,.xls,.xlsx,.ppt,.pptx,.txt,.csv"
       class="mt-4 w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-lg
              file:border-0 file:text-sm file:font-medium file:bg-blue-50 file:text-blue-700
              hover:file:bg-blue-100">
```

**Reference:** `templates/media_manager/upload.html:10-25`

---

## Form Groups

Standard pattern for grouping label + input + error + help text.

### Iterated Form Fields (Django form loop)

```html
<form method="post" enctype="multipart/form-data" class="space-y-6">
    {% csrf_token %}
    <div class="bg-white dark:bg-slate-800 rounded-xl shadow-sm border border-slate-200
                dark:border-slate-700 p-6 space-y-4">
        {% for field in form %}
        <div>
            <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">
                {{ field.label }}
            </label>
            {{ field }}
            {% if field.errors %}
            <p class="mt-1 text-sm text-red-600">{{ field.errors.0 }}</p>
            {% endif %}
            {% if field.help_text %}
            <p class="mt-1 text-sm text-slate-500">{{ field.help_text }}</p>
            {% endif %}
        </div>
        {% endfor %}
    </div>
</form>
```

**Reference:** `templates/broadcast/episode_form.html:25-39`, `templates/radio/station_form.html:25-39`

### Manual Form Group

```html
<div>
  <label for="id_folder" class="block text-sm font-medium text-gray-700 mb-1">Folder</label>
  <select name="folder" class="w-full px-3 py-2 border border-gray-300 rounded-lg">
    <option value="">Tanpa Folder</option>
    {% for folder in folders %}
    <option value="{{ folder.pk }}">{{ folder.name }}</option>
    {% endfor %}
  </select>
</div>
```

**Reference:** `templates/media_manager/upload.html:29-36`

---

## Validation Error Display

### Field-Level Errors

Displayed below the input field in red text.

```html
{% if field.errors %}
<p class="mt-1 text-sm text-red-600">{{ field.errors.0 }}</p>
{% endif %}
```

**Reference:** `templates/broadcast/episode_form.html:32-34`

### Non-Field Errors (form-level)

Displayed as a banner above the form.

```html
{% if form.non_field_errors %}
<div class="mb-4 p-3 rounded-lg text-sm bg-red-50 text-red-800
            dark:bg-red-950 dark:text-red-300 border border-red-200 dark:border-red-800">
    {% for error in form.non_field_errors %}
    <p>{{ error }}</p>
    {% endfor %}
</div>
{% endif %}
```

**Reference:** `apps/users/templates/users/login.html:18-24`

---

## Help Text

```html
{% if field.help_text %}
<p class="mt-1 text-sm text-slate-500">{{ field.help_text }}</p>
{% endif %}
```

**Reference:** `templates/broadcast/episode_form.html:35-37`

---

## Required Indicators

Required fields are indicated via Django form's built-in `required` attribute on the `<input>` element. Visual indicators use the asterisk pattern:

```html
<label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">
  {{ field.label }}
  {% if field.field.required %}
  <span class="text-red-500">*</span>
  {% endif %}
</label>
```

---

## Form Layout Patterns

### Search Form (inline)

```html
<form method="get" class="flex gap-2">
  <input type="text" name="q" value="{{ search }}" placeholder="Cari episode..."
         class="flex-1 px-4 py-2 border border-slate-300 dark:border-slate-600 rounded-lg
                text-sm bg-white dark:bg-slate-800 text-slate-900 dark:text-white">
  <select name="program" class="px-4 py-2 border border-slate-300 dark:border-slate-600
                                 rounded-lg text-sm bg-white dark:bg-slate-800
                                 text-slate-900 dark:text-white">
    <!-- options -->
  </select>
  <button type="submit"
          class="px-4 py-2 bg-slate-100 dark:bg-slate-700 text-slate-700
                 dark:text-slate-300 rounded-lg hover:bg-slate-200 dark:hover:bg-slate-600
                 text-sm font-medium">
    Cari
  </button>
</form>
```

**Reference:** `templates/broadcast/episode_list.html:25-34`

### Form Action Bar

Submit and cancel buttons, right-aligned.

```html
<div class="flex justify-end gap-3">
  <a href="{% url 'broadcast:episode_list' %}"
     class="px-6 py-2 border border-slate-300 dark:border-slate-600 text-slate-700
            dark:text-slate-300 rounded-lg hover:bg-slate-50 dark:hover:bg-slate-700 font-medium">
    Batal
  </a>
  <button type="submit"
          class="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 font-medium">
    {% if is_edit %}Simpan Perubahan{% else %}Buat Episode{% endif %}
  </button>
</div>
```

**Reference:** `templates/broadcast/episode_form.html:41-49`

---

## CSRF Handling

### Standard Form CSRF

```html
<form method="post" action="...">
  {% csrf_token %}
  <!-- form fields -->
</form>
```

### HTMX CSRF Configuration

CSRF token is injected into all HTMX requests via a global event listener in `base.html`.

```html
<script>
  document.body.addEventListener('htmx:configRequest', (event) => {
    event.detail.headers['X-CSRFToken'] = '{{ csrf_token }}';
  });
</script>
```

**Reference:** `templates/base.html:81-85`

### Inline Form CSRF (e.g., delete buttons in tables)

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

---

## Indonesian Label Reference

| English | Indonesian | Usage |
|---|---|---|
| Search | Cari | Search buttons, placeholders |
| Cancel | Batal | Form cancel buttons |
| Save Changes | Simpan Perubahan | Edit form submit |
| Create | Buat | Create form submit |
| Delete | Hapus | Delete actions |
| Add New | Tambah | Create new item buttons |
| Edit | Edit | Edit links |
| Upload | Upload | File upload buttons |
| All Types | Semua Tipe | Filter selects |
| All Programs | Semua Program | Filter selects |
| Without Folder | Tanpa Folder | Upload folder option |
| Public | Publik | Visibility checkbox |
| Inactive | Nonaktifkan | Deactivate action |
| Activate | Aktifkan | Activate action |
| Page X of Y | Halaman X dari Y | Pagination |
| Previous | Sebelumnya | Pagination |
| Next | Selanjutnya | Pagination |
| No data found | Tidak ada file ditemukan | Empty state |
| Login | Masuk | Auth submit |
| Register | Daftar | Auth link |
| Forgot password | Lupa password? | Auth link |
| Remember me | Ingat saya | Auth checkbox |
| Logout | Keluar | Auth action |
| Profile | Profil Saya | User menu |
