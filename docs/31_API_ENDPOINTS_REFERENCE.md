# 31. API Endpoints Reference

## Overview

This document provides a comprehensive reference for all API endpoints in the Kabulhaden CMS. The current system uses Django views (server-rendered HTML). This reference documents existing URL patterns and proposes a future REST API structure.

---

## Current URL Structure

### Root Configuration

```python
# config/urls.py
urlpatterns = [
    path('admin/', admin.site.urls),
    path('akun/', include('apps.users.urls')),
    path('pengaturan/', include('apps.settings.urls')),
    path('media/', include('apps.media_manager.urls')),
    path('radio/', include('apps.radio.urls')),
    path('broadcast/', include('apps.broadcast.urls')),
    path('', include('apps.website.urls')),
]
```

---

## Users (`/akun/`)

| URL Pattern | View | Method | Description |
|-------------|------|--------|-------------|
| `/akun/masuk/` | `LoginView` | GET/POST | User login |
| `/akun/keluar/` | `LogoutView` | POST | User logout |
| `/akun/profil/` | `ProfileView` | GET/POST | View/edit profile |
| `/akun/profil/edit/` | `ProfileEditView` | GET/POST | Edit profile details |
| `/akun/profil/ganti-password/` | `ChangePasswordView` | GET/POST | Change password |
| `/akun/verifikasi-email/` | `EmailVerificationView` | GET | Verify email address |
| `/akun/kirim-ulang-verifikasi/` | `ResendVerificationView` | POST | Resend verification email |
| `/akun/reset-password/` | `PasswordResetView` | GET/POST | Request password reset |
| `/akun/reset-password/konfirmasi/` | `PasswordResetConfirmView` | GET/POST | Confirm password reset |
| `/akun/dashboard/` | `DashboardView` | GET | User dashboard |
| `/akun/pengguna/` | `UserListView` | GET | List users (admin) |
| `/akun/pengguna/tambah/` | `UserCreateView` | GET/POST | Create user (admin) |
| `/akun/pengguna/<uuid>/` | `UserDetailView` | GET | View user details |
| `/akun/pengguna/<uuid>/edit/` | `UserUpdateView` | GET/POST | Edit user (admin) |
| `/akun/pengguna/<uuid>/hapus/` | `UserDeleteView` | POST | Delete user (admin) |

### Decorator Protection

| View | Decorators |
|------|------------|
| `DashboardView` | `@login_required_custom` |
| `UserListView` | `@login_required_custom`, `@role_required('ADMINISTRATOR', 'SUPERUSER')` |
| `UserCreateView` | `@admin_required` |
| `UserDeleteView` | `@admin_required` |

---

## Settings (`/pengaturan/`)

| URL Pattern | View | Method | Description |
|-------------|------|--------|-------------|
| `/pengaturan/` | `SettingsIndexView` | GET | Settings dashboard |
| `/pengaturan/profil/` | `SiteSettingsView` | GET/POST | Site configuration |
| `/pengaturan/seo/` | `SEOSettingsView` | GET/POST | SEO settings |
| `/pengaturan/email/` | `EmailSettingsView` | GET/POST | Email configuration |
| `/pengaturan/keamanan/` | `SecuritySettingsView` | GET/POST | Security settings |
| `/pengaturan/tampilan/` | `AppearanceSettingsView` | GET/POST | Theme/appearance |
| `/pengaturan/notifikasi/` | `NotificationSettingsView` | GET/POST | Notification preferences |
| `/pengaturan/media-sosial/` | `SocialMediaSettingsView` | GET/POST | Social media links |
| `/pengaturan/konten/` | `ContentSettingsView` | GET/POST | Content defaults |
| `/pengaturan/bahasa/` | `LanguageSettingsView` | GET/POST | Language settings |
| `/pengaturan/media/` | `MediaSettingsView` | GET/POST | Media storage settings |

### All Settings Views

Protected by: `@login_required_custom`, `@role_required('ADMINISTRATOR', 'SUPERUSER')`

---

## Media Manager (`/media/`)

| URL Pattern | View | Method | Description |
|-------------|------|--------|-------------|
| `/media/` | `MediaListView` | GET | List all media |
| `/media/upload/` | `MediaUploadView` | GET/POST | Upload media |
| `/media/<uuid>/` | `MediaDetailView` | GET | View media details |
| `/media/<uuid>/edit/` | `MediaUpdateView` | GET/POST | Edit media metadata |
| `/media/<uuid>/hapus/` | `MediaDeleteView` | POST | Delete media |
| `/media/<uuid>/download/` | `MediaDownloadView` | GET | Download media file |
| `/media/folder/` | `FolderListView` | GET | List folders |
| `/media/folder/buat/` | `FolderCreateView` | GET/POST | Create folder |
| `/media/folder/<uuid>/` | `FolderDetailView` | GET | View folder contents |
| `/media/folder/<uuid>/edit/` | `FolderUpdateView` | GET/POST | Edit folder |
| `/media/folder/<uuid>/hapus/` | `FolderDeleteView` | POST | Delete folder |
| `/media/cleanup/` | `CleanupView` | POST | Cleanup orphaned media |
| `/media/compress/` | `CompressView` | POST | Compress media files |
| `/media/thumbnails/` | `ThumbnailView` | POST | Generate thumbnails |

### Management Commands

```bash
python manage.py cleanup_media        # Remove orphaned files
python manage.py compress_media       # Compress media files
python manage.py generate_thumbnails  # Generate thumbnails
```

---

## Radio (`/radio/`)

### AMP Studio Management (Login Required)

| URL Pattern | View | Method | Description |
|-------------|------|--------|-------------|
| `/radio/` | `RadioDashboardView` | GET | Radio dashboard |
| `/radio/station/` | `RadioStationListView` | GET | List radio stations |
| `/radio/station/buat/` | `RadioStationCreateView` | GET/POST | Create station |
| `/radio/station/<pk>/edit/` | `RadioStationEditView` | GET/POST | Edit station |
| `/radio/station/<pk>/toggle/` | `RadioStationDeleteView` | POST | Toggle station active/inactive |
| `/radio/provider/` | `RadioProviderListView` | GET | List providers |
| `/radio/provider/buat/` | `RadioProviderCreateView` | GET/POST | Create provider |
| `/radio/provider/<pk>/edit/` | `RadioProviderEditView` | GET/POST | Edit provider (stream URL, API URL, credentials) |
| `/radio/provider/<pk>/toggle/` | `RadioProviderDeleteView` | POST | Toggle provider active/inactive |
| `/radio/listener/export/<station_id>/` | `ExportCSVView` | GET | Export listener stats CSV |
| `/radio/listener/export/<station_id>/excel/` | `ExportExcelView` | GET | Export listener stats Excel |

### Internal Radio APIs (No Auth Required)

| URL Pattern | View | Method | Description |
|-------------|------|--------|-------------|
| `/radio/api/status/` | `RadioStatusAPIView` | GET | Full station status JSON |
| `/radio/api/now-playing/` | `RadioNowPlayingAPIView` | GET | Current song/artist |
| `/radio/api/player-config/` | `RadioPlayerConfigAPIView` | GET | Player config (volume, autoplay) |
| `/radio/api/listeners/` | `RadioListenerAPIView` | GET | Current & peak listener count |
| `/radio/api/health/` | `RadioHealthAPIView` | GET | Stream health status |
| `/radio/api/current-program/` | `RadioCurrentProgramAPIView` | GET | Current live program info |
| `/radio/api/current-host/` | `RadioCurrentHostAPIView` | GET | Current broadcast host |
| `/radio/api/providers/` | `RadioProvidersAPIView` | GET | List active providers |
| `/radio/stream/` | `RadioStreamProxyView` | GET | **Same-origin audio proxy** — relays Icecast stream; adds ngrok bypass header. Not used as default in Replit dev (buffering issue). Available for production deployments behind Nginx. |

### Public Live Radio API

| URL Pattern | View | Method | Description |
|-------------|------|--------|-------------|
| `/api/v1/radio/live/` | `LiveRadioAPIView` | GET | **Primary endpoint** — normalized live data for all UI components. DB-first provider lookup. 20 s cache. Never crashes (offline fallback). |

#### `/api/v1/radio/live/` Response Schema

```json
{
  "status": "live",
  "station": "Kabulhaden Online",
  "program": null,
  "title": "Song Title",
  "artist": "Artist Name",
  "cover": "",
  "listeners": 3,
  "started_at": null,
  "stream_url": "https://<ngrok-subdomain>.ngrok-free.app/kabulhaden.mp3",
  "is_live": true,
  "provider": "icecast"
}
```

**Notes:**
- `stream_url` adalah URL langsung ke Icecast/ngrok. Browser connect langsung — tidak melalui Django proxy.
- `program` selalu `null` (TD-001 — integrasi broadcast schedule belum dilakukan).
- Response di-cache 20 detik (`STREAM_CACHE_TTL` setting).

### Management Commands

```bash
python manage.py demo_seed [--reset]   # Seed demo data including radio station
```

---

## Broadcast (`/broadcast/`)

| URL Pattern | View | Method | Description |
|-------------|------|--------|-------------|
| `/broadcast/` | `BroadcastDashboardView` | GET | Broadcast dashboard |
| `/broadcast/encoder/` | `EncoderListView` | GET | List encoders |
| `/broadcast/encoder/tambah/` | `EncoderCreateView` | GET/POST | Create encoder |
| `/broadcast/encoder/<uuid>/` | `EncoderDetailView` | GET | View encoder |
| `/broadcast/encoder/<uuid>/edit/` | `EncoderUpdateView` | GET/POST | Edit encoder |
| `/broadcast/encoder/<uuid>/hapus/` | `EncoderDeleteView` | POST | Delete encoder |
| `/broadcast/encoder/<uuid>/status/` | `EncoderStatusView` | GET | Get encoder status |
| `/broadcast/encoder/<uuid>/start/` | `EncoderStartView` | POST | Start encoder |
| `/broadcast/encoder/<uuid>/stop/` | `EncoderStopView` | POST | Stop encoder |
| `/broadcast/stream/` | `StreamListView` | GET | List streams |
| `/broadcast/stream/tambah/` | `StreamCreateView` | GET/POST | Create stream |
| `/broadcast/stream/<uuid>/` | `StreamDetailView` | GET | View stream |
| `/broadcast/stream/<uuid>/edit/` | `StreamUpdateView` | GET/POST | Edit stream |
| `/broadcast/stream/<uuid>/hapus/` | `StreamDeleteView` | POST | Delete stream |
| `/broadcast/playlist/` | `PlaylistListView` | GET | List playlists |
| `/broadcast/playlist/tambah/` | `PlaylistCreateView` | GET/POST | Create playlist |
| `/broadcast/playlist/<uuid>/` | `PlaylistDetailView` | GET | View playlist |
| `/broadcast/playlist/<uuid>/edit/` | `PlaylistUpdateView` | GET/POST | Edit playlist |
| `/broadcast/playlist/<uuid>/hapus/` | `PlaylistDeleteView` | POST | Delete playlist |
| `/broadcast/playlist/<uuid>/tracks/` | `PlaylistTracksView` | GET | List playlist tracks |
| `/broadcast/playlist/<uuid>/tracks/tambah/` | `TrackAddView` | POST | Add track to playlist |
| `/broadcast/playlist/<uuid>/tracks/<uuid>/hapus/` | `TrackRemoveView` | POST | Remove track |
| `/broadcast/playlist/<uuid>/tracks/reorder/` | `TrackReorderView` | POST | Reorder tracks |
| `/broadcast/rekaman/` | `RecordingListView` | GET | List recordings |
| `/broadcast/rekaman/<uuid>/` | `RecordingDetailView` | GET | View recording |
| `/broadcast/rekaman/<uuid>/download/` | `RecordingDownloadView` | GET | Download recording |
| `/broadcast/statistik/` | `BroadcastStatsView` | GET | View statistics |
| `/broadcast/health/` | `HealthCheckView` | GET | Health check endpoint |
| `/broadcast/api/status/` | `StreamStatusAPI` | GET | Stream status JSON |

### Management Commands

```bash
python manage.py init_settings  # Initialize default settings
```

---

## Website (`/`)

| URL Pattern | View | Method | Description |
|-------------|------|--------|-------------|
| `/` | `HomeView` | GET | Homepage |
| `/berita/` | `NewsListView` | GET | News listing |
| `/berita/<slug>/` | `NewsDetailView` | GET | News article |
| `/podcast/` | `PodcastListView` | GET | Podcast listing |
| `/podcast/<slug>/` | `PodcastDetailView` | GET | Podcast episode |
| `/komunitas/` | `CommunityListView` | GET | Community listing |
| `/komunitas/<slug>/` | `CommunityDetailView` | GET | Community post |
| `/sponsor/` | `SponsorListView` | GET | Sponsors page |
| `/sponsor/<slug>/` | `SponsorDetailView` | GET | Sponsor profile |
| `/tentang/` | `AboutView` | GET | About page |
| `/kontak/` | `ContactView` | GET/POST | Contact form |

---

## Proposed REST API Endpoints (Future)

### Authentication

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/auth/login/` | POST | Login, get token |
| `/api/v1/auth/logout/` | POST | Invalidate token |
| `/api/v1/auth/refresh/` | POST | Refresh token |
| `/api/v1/auth/me/` | GET | Current user info |

### Content API

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/news/` | GET | List news articles |
| `/api/v1/news/<uuid>/` | GET | Get news article |
| `/api/v1/podcast/` | GET | List podcast episodes |
| `/api/v1/podcast/<uuid>/` | GET | Get podcast episode |
| `/api/v1/schedule/` | GET | Get current schedule |
| `/api/v1/stream/status/` | GET | Current stream status |

### Admin API (JWT Protected)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/admin/users/` | GET/POST | List/create users |
| `/api/v1/admin/users/<uuid>/` | GET/PUT/DELETE | User CRUD |
| `/api/v1/admin/media/` | GET/POST | List/upload media |
| `/api/v1/admin/radio/stations/` | GET/POST | Station CRUD |
| `/api/v1/admin/radio/programs/` | GET/POST | Program CRUD |
| `/api/v1/admin/radio/schedules/` | GET/POST | Schedule CRUD |
| `/api/v1/admin/broadcast/encoders/` | GET/POST | Encoder CRUD |
| `/api/v1/admin/broadcast/playlists/` | GET/POST | Playlist CRUD |

---

## Related Documentation

- `erd.md` - Entity relationship diagrams
- `url_list.md` - Simplified URL reference
- `permission_matrix.md` - Role-based access control
- `14_FORM_DESIGN.md` - Form patterns

---

*Last updated: 2026-07-20 — Sprint 4.3 (radio API endpoints, RadioStreamProxyView, LiveRadioAPIView schema)*
