# AMP Studio — Role-Based Workspaces

## Role Definitions

Each role in AMP Studio sees a tailored sidebar with only the sections relevant to their work.

### Administrator
**Full access to everything.**
- Beranda ✅
- Siaran (Program, Episode, Jadwal, Host, Pengumuman) ✅
- Konten (Artikel, Kategori, Tag, Penulis, SEO) ✅
- Podcast (Program, Episode) ✅
- Komunitas ✅
- Iklan ✅
- Media (Semua File, Upload, Folder, Tag) ✅
- Analytics ✅
- Partner ✅
- Radio ✅
- Pengaturan (Situs, Tampilan, Email, Bahasa, Keamanan, Pengguna) ✅

### Station Manager
**Operations-focused: broadcasts, schedules, analytics.**
- Beranda ✅
- Siaran (Program, Episode, Jadwal, Host) ✅
- Media (Semua File) ✅
- Analytics ✅
- Radio ✅
- Pengaturan (Situs, Keamanan) ✅

### Program Director
**Content planning and broadcast management.**
- Beranda ✅
- Siaran (Program, Episode, Jadwal) ✅
- Konten (Artikel) ✅
- Podcast (Program, Episode) ✅
- Analytics ✅

### Host
**Personal content and schedule viewing.**
- Beranda ✅
- Siaran (Jadwal — read only) ✅
- Konten (Artikel — own only) ✅
- Podcast (Episode — own only) ✅

### Content Editor
**Article and content management.**
- Beranda ✅
- Konten (Artikel, Kategori, Tag, Penulis, SEO) ✅
- Media (Semua File, Upload) ✅

### Marketing
**Content promotion and community.**
- Beranda ✅
- Konten (Artikel — read only) ✅
- Komunitas ✅
- Iklan ✅
- Analytics ✅

### Sponsor Manager
**Sponsor relationship management.**
- Beranda ✅
- Partner ✅
- Iklan ✅
- Analytics ✅

### Finance
**Financial reporting (limited CMS access).**
- Beranda ✅
- Analytics ✅
- Partner (read only) ✅

### Guest
**Read-only access to public content.**
- Beranda ✅
- (No sidebar navigation beyond dashboard)

---

## Implementation

The sidebar component (`templates/amp_studio/components/sidebar.html`) checks `user.role` to determine which sections to display.

### Django Template Pattern
```django
{% if user.role == 'administrator' or user.role == 'station_manager' %}
  {# Show Siaran section #}
{% endif %}
```

### Alpine.js Pattern (Planned)
```html
<nav x-data="{ userRole: '{{ user.role }}' }">
  <template x-if="['administrator', 'station_manager'].includes(userRole)">
    <div class="amp-nav-section">...</div>
  </template>
</nav>
```

---

## Access Control Matrix

| Feature | Admin | Station Mgr | Program Dir | Host | Editor | Marketing | Sponsor Mgr | Finance | Guest |
|---------|:-----:|:-----------:|:-----------:|:----:|:------:|:---------:|:-----------:|:-------:|:-----:|
| Dashboard | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Create Article | ✅ | — | ✅ | ✅ | ✅ | — | — | — | — |
| Edit Any Article | ✅ | — | ✅ | — | ✅ | — | — | — | — |
| Publish Article | ✅ | ✅ | ✅ | — | — | — | — | — | — |
| Manage Programs | ✅ | ✅ | ✅ | — | — | — | — | — | — |
| Manage Schedule | ✅ | ✅ | ✅ | 👁 | — | — | — | — | — |
| Upload Media | ✅ | ✅ | ✅ | ✅ | ✅ | — | — | — | — |
| View Analytics | ✅ | ✅ | ✅ | — | — | ✅ | ✅ | ✅ | — |
| Manage Settings | ✅ | 👁 | — | — | — | — | — | — | — |
| Manage Users | ✅ | — | — | — | — | — | — | — | — |
| Manage Sponsors | ✅ | — | — | — | — | ✅ | ✅ | 👁 | — |
| Community | ✅ | — | — | — | — | ✅ | — | — | — |
| Django Admin | ✅ | — | — | — | — | — | — | — | — |

Legend: ✅ Full access | 👁 Read-only | — No access
