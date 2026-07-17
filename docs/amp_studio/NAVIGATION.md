# AMP Studio — Navigation

## Sidebar Structure

The sidebar is the primary navigation element in AMP Studio. It adapts based on user role.

### Top-Level Items

| Section | Icon | URL | Children |
|---------|------|-----|----------|
| **Beranda** | Grid | `/studio/` | — |
| **Siaran** | Broadcast | — | Program, Episode, Jadwal, Host, Pengumuman |
| **Konten** | Document | — | Artikel, Kategori, Tag, Penulis, SEO |
| **Podcast** | Mic | — | Program, Episode |
| **Komunitas** | Users | — | — |
| **Iklan** | Credit Card | — | — |
| **Media** | Image | — | Semua File, Upload, Folder, Tag |
| **Analytics** | Bar Chart | `/radio/analytics/` | — |
| **Partner** | Heart | — | — |
| **Radio** | Signal | `/radio/` | — |
| **Pengaturan** | Settings | — | Situs, Tampilan, Email, Bahasa, Keamanan, Pengguna |

### Sidebar Behaviors
- **Collapse/Expand**: Toggle via header button or keyboard shortcut
- **Collapsed state**: Shows only icons (72px width)
- **Expanded state**: Icons + labels (260px width)
- **Mobile**: Off-canvas with backdrop overlay
- **Section collapse**: Each expandable section remembers state (Alpine.js)

### Active State
- Active item gets `amp-nav-item active` class
- Background: `var(--amp-coffee-50)`
- Text color: `var(--amp-coffee-700)`
- Detection: `request.resolver_match.url_name` or `app_name`

## Breadcrumbs
Not yet implemented. Planned for Phase 3.

## URL Mapping

```
/studio/                              → Dashboard
/studio/kalender/                     → Calendar
/studio/media/                        → Media Explorer
/studio/analytics/                    → Analytics
/studio/preview/<type>/<pk>/          → Content Preview
/berita/cms/artikel/                  → Article List
/berita/cms/artikel/buat/             → Create Article
/berita/cms/artikel/<pk>/edit/        → Edit Article
/podcast/podcast/                     → Podcast List
/podcast/podcast/episode/             → Episode List
/broadcast/program/                   → Program List
/broadcast/jadwal/                    → Schedule List
/media/                               → Media Manager
/media/upload/                        → Upload
/radio/                               → Radio Dashboard
/radio/analytics/                     → Radio Analytics
/pengaturan/                          → Settings
/akun/                                → Authentication
/konten/                              → Content Management
```

## Cross-Module Navigation
- Sidebar links to other modules use absolute URLs
- Command palette provides search across all modules
- Header search triggers command palette
- User menu provides logout and profile links
