# 05 — Sitemap

Complete page hierarchy of Kabulhaden CMS with URL structure, authentication requirements, and template references.

---

## URL Architecture Overview

```
/ (root)
├── /admin/                    ── Django Admin (SUPERUSER only)
├── /akun/                     ── Authentication & User Management
├── /pengaturan/               ── System Settings (Admin)
├── /media/                    ── Media Manager (Staff)
├── /radio/                    ── Radio Engine (Staff)
├── /broadcast/                ── Broadcast Management (Staff)
└── (public pages)             ── Website (no auth required)
```

---

## Public Website (No Authentication)

All public pages are accessible without login. Templates live in `templates/website/`.

| URL Path | View | Template | Description |
|---|---|---|---|
| `/` | `HomeView` | `website/home.html` | Homepage with 9 sections |
| `/tentang/` | `AboutView` | `website/about.html` | About the station |
| `/program/` | `ProgramListView` | `website/program_list.html` | All active programs |
| `/program/<slug>/` | `ProgramDetailView` | `website/program_detail.html` | Program detail + episodes |
| `/jadwal/` | `ScheduleView` | `website/schedule.html` | Weekly schedule |
| `/podcast/` | `PodcastListView` | `website/podcast_list.html` | All podcasts |
| `/podcast/<slug>/` | `PodcastDetailView` | `website/podcast_detail.html` | Podcast episodes |
| `/podcast/episode/<uuid>/` | `PodcastEpisodeView` | `website/podcast_episode.html` | Single episode |
| `/berita/` | `NewsListView` | `website/news_list.html` | News articles |
| `/berita/<slug>/` | `ArticleDetailView` | `website/article_detail.html` | Single article |
| `/komunitas/` | `CommunityView` | `website/community.html` | Discussion threads |
| `/komunitas/<slug>/` | `CommunityDiscussionView` | `website/community_discussion.html` | Thread + replies |
| `/mitra/` | `PartnerListView` | `website/partner_list.html` | Partner listings |
| `/sponsor/` | `SponsorListView` | `website/sponsor_list.html` | Sponsor listings |
| `/kontak/` | `ContactView` | `website/contact.html` | Contact page |
| `/kebijakan-privasi/` | `PrivacyView` | `website/privacy.html` | Privacy policy |
| `/syarat-ketentuan/` | `TermsView` | `website/terms.html` | Terms & conditions |
| `/pencarian/` | `SearchView` | `website/search.html` | Cross-content search |
| `/pemeliharaan/` | `MaintenanceView` | `website/maintenance.html` | Maintenance mode |
| `/radio-live/` | `HomeView` | `website/home.html` | Alias for homepage |
| `/newsletter/subscribe/` | `NewsletterSubscribeView` | — (JSON response) | AJAX newsletter endpoint |

---

## Authentication & User Management (`/akun/`)

| URL Path | View | Template | Auth Required | Description |
|---|---|---|---|---|
| `/akun/masuk/` | `LoginView` | `users/login.html` | No | Login page |
| `/akun/keluar/` | `LogoutView` | — | Yes | Logout action |
| `/akun/daftar/` | `RegisterView` | `users/register.html` | No | Registration |
| `/akun/lupa-password/` | `ForgotPasswordView` | `users/forgot_password.html` | No | Password reset request |
| `/akun/ganti-password/` | `ChangePasswordView` | `users/change_password.html` | Yes | Change password |
| `/akun/profil/` | `ProfileView` | `users/profile.html` | Yes | User profile |
| `/akun/verifikasi-email/` | `VerifyEmailNoticeView` | `users/verify_email_notice.html` | No | Email verification notice |
| `/akun/verifikasi-email/<token>/` | `VerifyEmailView` | — | No | Verify email link |
| `/akun/2fa/verifikasi/` | `TwoFactorVerifyView` | `users/two_factor_verify.html` | Partial | 2FA verification |
| `/akun/2fa/setup/` | `TwoFactorSetupView` | `users/two_factor_setup.html` | Yes | 2FA setup |
| `/akun/2fa/nonaktifkan/` | `TwoFactorDisableView` | — | Yes | Disable 2FA |
| `/akun/admin/pengguna/` | `AdminUserListView` | `users/admin/user_list.html` | Staff | User management list |
| `/akun/admin/pengguna/buat/` | `AdminUserCreateView` | `users/admin/user_create.html` | Staff | Create user |
| `/akun/admin/pengguna/<uuid>/` | `AdminUserDetailView` | `users/admin/user_detail.html` | Staff | User detail |

---

## System Settings (`/pengaturan/`)

All settings pages require authentication and are restricted to ADMINISTRATOR+ roles.

| URL Path | View | Template | Description |
|---|---|---|---|
| `/pengaturan/` | `SiteSettingsView` | `settings/site.html` | Site identity & maintenance |
| `/pengaturan/seo/` | `SEOSettingsView` | `settings/seo.html` | Meta tags, analytics, scripts |
| `/pengaturan/email/` | `EmailSettingsView` | `settings/email.html` | SMTP configuration |
| `/pengaturan/keamanan/` | `SecuritySettingsView` | `settings/security.html` | Password, 2FA, IP rules |
| `/pengaturan/tampilan/` | `AppearanceSettingsView` | `settings/appearance.html` | Colors, fonts, layout |
| `/pengaturan/notifikasi/` | `NotificationSettingsView` | `settings/notification.html` | Email notification triggers |
| `/pengaturan/media-sosial/` | `SocialMediaSettingsView` | `settings/social_media.html` | Social platform links |
| `/pengaturan/konten/` | `ContentSettingsView` | `settings/content.html` | Pagination, comments, uploads |
| `/pengaturan/bahasa/` | `LanguageSettingsView` | `settings/language.html` | Language, timezone, date format |
| `/pengaturan/media/` | `MediaSettingsView` | `settings/media.html` | Storage, compression, thumbnails |

---

## Media Manager (`/media/`)

All media pages require authentication (EDITOR+).

| URL Path | View | Template | Description |
|---|---|---|---|
| `/media/` | `MediaDashboardView` | `media_manager/dashboard.html` | Media overview |
| `/media/file/` | `MediaListView` | `media_manager/list.html` | All files |
| `/media/upload/` | `MediaUploadView` | `media_manager/upload.html` | Upload form |
| `/media/file/<uuid>/` | `MediaDetailView` | `media_manager/detail.html` | File detail |
| `/media/file/<uuid>/hapus/` | `MediaDeleteView` | — | Delete action |
| `/media/bulk-delete/` | `MediaBulkDeleteView` | — | Bulk delete action |
| `/media/folder/` | `FoldersView` | `media_manager/folders.html` | Folder list |
| `/media/folder/buat/` | `FolderCreateView` | — | Create folder |
| `/media/folder/<uuid>/hapus/` | `FolderDeleteView` | — | Delete folder |
| `/media/tag/` | `TagsView` | `media_manager/tags.html` | Tag list |
| `/media/tag/buat/` | `TagCreateView` | — | Create tag |
| `/media/tag/<uuid>/hapus/` | `TagDeleteView` | — | Delete tag |
| `/media/api/search/` | `MediaSearchAPIView` | — (JSON) | Search media files |

---

## Radio Engine (`/radio/`)

All radio pages require authentication (ADMINISTRATOR+).

| URL Path | View | Template | Description |
|---|---|---|---|
| `/radio/` | `RadioDashboardView` | `radio/dashboard.html` | Radio overview |
| `/radio/station/` | `RadioStationListView` | `radio/station_list.html` | Station list |
| `/radio/station/buat/` | `RadioStationCreateView` | `radio/station_form.html` | Create station |
| `/radio/station/<uuid>/edit/` | `RadioStationEditView` | `radio/station_form.html` | Edit station |
| `/radio/station/<uuid>/hapus/` | `RadioStationDeleteView` | `radio/station_confirm_delete.html` | Delete station |
| `/radio/provider/` | `RadioProviderListView` | `radio/provider_list.html` | Provider list |
| `/radio/provider/buat/` | `RadioProviderCreateView` | `radio/provider_form.html` | Create provider |
| `/radio/provider/<uuid>/edit/` | `RadioProviderEditView` | `radio/provider_form.html` | Edit provider |
| `/radio/provider/<uuid>/hapus/` | `RadioProviderDeleteView` | `radio/provider_confirm_delete.html` | Delete provider |
| `/radio/analytics/` | `RadioAnalyticsView` | `radio/analytics.html` | Analytics dashboard |
| `/radio/export/csv/<uuid>/` | `ExportCSVView` | — (CSV download) | Export CSV |
| `/radio/export/excel/<uuid>/` | `ExportExcelView` | — (Excel download) | Export Excel |
| `/radio/api/status/` | `RadioStatusAPIView` | — (JSON) | Stream status |
| `/radio/api/player/` | `RadioPlayerAPIView` | — (JSON) | Player data |
| `/radio/api/now-playing/` | `RadioNowPlayingAPIView` | — (JSON) | Now playing |
| `/radio/api/listener/` | `RadioListenerAPIView` | — (JSON) | Listener count |
| `/radio/api/health/` | `RadioHealthAPIView` | — (JSON) | Health check |
| `/radio/api/current-program/` | `RadioCurrentProgramAPIView` | — (JSON) | Current program |
| `/radio/api/current-host/` | `RadioCurrentHostAPIView` | — (JSON) | Current host |
| `/radio/api/providers/` | `RadioProvidersAPIView` | — (JSON) | All providers |
| `/radio/api/player-config/` | `RadioPlayerConfigAPIView` | — (JSON) | Player configuration |

---

## Broadcast Management (`/broadcast/`)

All broadcast pages require authentication (EDITOR+).

| URL Path | View | Template | Description |
|---|---|---|---|
| `/broadcast/` | `BroadcastDashboardView` | `broadcast/dashboard.html` | Broadcast overview |
| `/broadcast/program/` | `ProgramListView` | `broadcast/program_list.html` | Program list |
| `/broadcast/program/buat/` | `ProgramCreateView` | `broadcast/program_form.html` | Create program |
| `/broadcast/program/<uuid>/edit/` | `ProgramEditView` | `broadcast/program_form.html` | Edit program |
| `/broadcast/program/<uuid>/hapus/` | `ProgramDeleteView` | — | Delete program |
| `/broadcast/host/` | `HostListView` | `broadcast/host_list.html` | Host list |
| `/broadcast/host/buat/` | `HostCreateView` | `broadcast/host_form.html` | Create host |
| `/broadcast/host/<uuid>/edit/` | `HostEditView` | `broadcast/host_form.html` | Edit host |
| `/broadcast/host/<uuid>/hapus/` | `HostDeleteView` | — | Delete host |
| `/broadcast/jadwal/` | `ScheduleListView` | `broadcast/schedule_list.html` | Schedule list |
| `/broadcast/jadwal/buat/` | `ScheduleCreateView` | `broadcast/schedule_form.html` | Create schedule |
| `/broadcast/jadwal/<uuid>/edit/` | `ScheduleEditView` | `broadcast/schedule_form.html` | Edit schedule |
| `/broadcast/jadwal/<uuid>/hapus/` | `ScheduleDeleteView` | — | Delete schedule |
| `/broadcast/sesi/` | `BroadcastSessionListView` | `broadcast/session_list.html` | Session list |
| `/broadcast/sesi/buat/` | `BroadcastSessionCreateView` | `broadcast/session_form.html` | Create session |
| `/broadcast/sesi/<uuid>/edit/` | `BroadcastSessionEditView` | `broadcast/session_form.html` | Edit session |
| `/broadcast/sesi/<uuid>/hapus/` | `BroadcastSessionDeleteView` | — | Delete session |
| `/broadcast/episode/` | `EpisodeListView` | `broadcast/episode_list.html` | Episode list |
| `/broadcast/episode/buat/` | `EpisodeCreateView` | `broadcast/episode_form.html` | Create episode |
| `/broadcast/episode/<uuid>/edit/` | `EpisodeEditView` | `broadcast/episode_form.html` | Edit episode |
| `/broadcast/episode/<uuid>/hapus/` | `EpisodeDeleteView` | — | Delete episode |
| `/broadcast/pengumuman/` | `AnnouncementListView` | `broadcast/announcement_list.html` | Announcement list |
| `/broadcast/pengumuman/buat/` | `AnnouncementCreateView` | `broadcast/announcement_form.html` | Create announcement |
| `/broadcast/pengumuman/<uuid>/edit/` | `AnnouncementEditView` | `broadcast/announcement_form.html` | Edit announcement |
| `/broadcast/pengumuman/<uuid>/hapus/` | `AnnouncementDeleteView` | — | Delete announcement |
| `/broadcast/kalender/` | `CalendarView` | `broadcast/calendar.html` | Calendar view |
| `/broadcast/api/programs/` | `ProgramListAPIView` | — (JSON) | Public programs API |
| `/broadcast/api/program/<slug>/` | `ProgramDetailAPIView` | — (JSON) | Program detail API |
| `/broadcast/api/schedule/` | `ScheduleAPIView` | — (JSON) | Schedule API |
| `/broadcast/api/today/` | `TodayScheduleAPIView` | — (JSON) | Today's schedule |
| `/broadcast/api/current/` | `CurrentBroadcastAPIView` | — (JSON) | Current broadcast |
| `/broadcast/api/next/` | `NextBroadcastAPIView` | — (JSON) | Next broadcast |
| `/broadcast/api/hosts/` | `HostListAPIView` | — (JSON) | Hosts API |
| `/broadcast/api/host/<uuid>/` | `HostDetailAPIView` | — (JSON) | Host detail API |
| `/broadcast/api/episodes/` | `EpisodeListAPIView` | — (JSON) | Episodes API |
| `/broadcast/api/playlist/` | `PlaylistAPIView` | — (JSON) | Playlist API |

---

## Django Admin Panel (`/admin/`)

| URL Path | Access | Description |
|---|---|---|
| `/admin/` | SUPERUSER only | Django Admin dashboard |
| `/admin/` + model URLs | SUPERUSER only | Direct model CRUD for all registered models |

Branding customized in `config/urls.py`:
- `site_header`: "Kabulhaden CMS"
- `site_title`: "Kabulhaden CMS Admin"
- `index_title`: "Panel Kontrol Kabulhaden CMS"

---

## System Endpoints

| URL Path | Auth | Description |
|---|---|---|
| `/health/` | No | System health check (JSON) |
| `/__debug__/` | Dev only | django-debug-toolbar (development only) |

---

## URL Pattern Summary

| Namespace | URL Prefix | App | Auth Level |
|---|---|---|---|
| `website` | `/` | `apps.website` | Public |
| `core` | `/` | `apps.core` | Public |
| `users` | `/akun/` | `apps.users` | Mixed |
| `settings` | `/pengaturan/` | `apps.settings` | ADMINISTRATOR+ |
| `media_manager` | `/media/` | `apps.media_manager` | EDITOR+ |
| `radio` | `/radio/` | `apps.radio` | ADMINISTRATOR+ |
| `broadcast` | `/broadcast/` | `apps.broadcast` | EDITOR+ |
| `admin` | `/admin/` | Django Admin | SUPERUSER |
