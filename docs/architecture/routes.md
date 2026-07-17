# AMP Studio — Route Inventory
**Generated:** Sprint 4.0 (July 17, 2026)

Auth legend: 🔓 Public | 🔒 Login Required | 👑 SUPERUSER/ADMIN only

---

## Root Config (`config/urls.py`)

| Mount | Includes | Description |
|---|---|---|
| `/studio/` | `apps.studio.urls` (ns: studio) | AMP Studio CMS hub |
| `/admin/` | `django.contrib.admin` | Django admin |
| `/akun/` | `apps.users.urls` (ns: users) | Authentication + user management |
| `/pengaturan/` | `apps.settings.urls` | Site settings |
| `/media/` | `apps.media_manager.urls` (ns: media_manager) | Media/file management |
| `/radio/` | `apps.radio.urls` (ns: radio) | Radio engine |
| `/api/v1/` | `apps.radio.api_v1_urls` | Public radio API |
| `/broadcast/` | `apps.broadcast.urls` (ns: broadcast) | Broadcast management |
| `/berita/` | `apps.news.urls` (ns: news) | News/articles |
| `/podcast/` | `apps.podcast.urls` (ns: podcast) | Podcast |
| `/konten/` | `apps.content.urls` (ns: content) | Content metadata |
| `/platform/` | `apps.platform.urls` | Platform/partner management |
| `/` | `apps.website.urls` + `apps.core.urls` | Public website |

---

## Studio (`/studio/`, namespace: `studio`)

| URL | View | Name | Auth | Status |
|---|---|---|---|---|
| `/studio/` | AMPStudioDashboardView | `dashboard` | 🔒 | ✅ |
| `/studio/kalender/` | AMPStudioCalendarView | `calendar` | 🔒 | ✅ |
| `/studio/media/` | AMPStudioMediaExplorerView | `media_explorer` | 🔒 | ✅ |
| `/studio/analytics/` | AMPStudioAnalyticsView | `analytics` | 🔒 | ✅ (stub) |
| `/studio/streaming/` | StreamingCenterView | `streaming_center` | 🔒 | ✅ |
| `/studio/komunitas/` | CommunityView | `community` | 🔒 | ✅ |
| `/studio/iklan/` | IklanView | `iklan` | 🔒 | ✅ |
| `/studio/setup/` | SetupWizardView | `setup_wizard` | 🔒 | ✅ |
| `/studio/preview/<str>/<uuid>/` | AMPStudioPreviewView | `preview` | 🔒 | ✅ |
| `/studio/partner/switch/<uuid>/` | PartnerSwitchView | `partner_switch` | 👑 | ✅ |
| `/studio/partner/list/` | PartnerListView | `partner_list` | 👑 | ✅ |

---

## Broadcast (`/broadcast/`, namespace: `broadcast`)

| URL | View | Name | Auth |
|---|---|---|---|
| `/broadcast/` | BroadcastDashboardView | `dashboard` | 🔒 |
| `/broadcast/program/` | ProgramListView | `program_list` | 🔒 |
| `/broadcast/program/buat/` | ProgramCreateView | `program_create` | 🔒 |
| `/broadcast/program/<uuid>/edit/` | ProgramUpdateView | `program_edit` | 🔒 |
| `/broadcast/program/<uuid>/hapus/` | ProgramDeleteView | `program_delete` | 🔒 |
| `/broadcast/host/` | HostListView | `host_list` | 🔒 |
| `/broadcast/host/buat/` | HostCreateView | `host_create` | 🔒 |
| `/broadcast/host/<uuid>/edit/` | HostUpdateView | `host_edit` | 🔒 |
| `/broadcast/host/<uuid>/hapus/` | HostDeleteView | `host_delete` | 🔒 |
| `/broadcast/jadwal/` | ScheduleListView | `schedule_list` | 🔒 |
| `/broadcast/jadwal/buat/` | ScheduleCreateView | `schedule_create` | 🔒 |
| `/broadcast/jadwal/<uuid>/edit/` | ScheduleUpdateView | `schedule_edit` | 🔒 |
| `/broadcast/jadwal/<uuid>/hapus/` | ScheduleDeleteView | `schedule_delete` | 🔒 |
| `/broadcast/sesi/` | SessionListView | `session_list` | 🔒 |
| `/broadcast/sesi/buat/` | SessionCreateView | `session_create` | 🔒 |
| `/broadcast/sesi/<uuid>/edit/` | SessionUpdateView | `session_edit` | 🔒 |
| `/broadcast/sesi/<uuid>/hapus/` | SessionDeleteView | `session_delete` | 🔒 |
| `/broadcast/episode/` | EpisodeListView | `episode_list` | 🔒 |
| `/broadcast/episode/buat/` | EpisodeCreateView | `episode_create` | 🔒 |
| `/broadcast/episode/<uuid>/edit/` | EpisodeUpdateView | `episode_edit` | 🔒 |
| `/broadcast/episode/<uuid>/hapus/` | EpisodeDeleteView | `episode_delete` | 🔒 |
| `/broadcast/pengumuman/` | AnnouncementListView | `announcement_list` | 🔒 |
| `/broadcast/pengumuman/buat/` | AnnouncementCreateView | `announcement_create` | 🔒 |
| `/broadcast/pengumuman/<uuid>/edit/` | AnnouncementUpdateView | `announcement_edit` | 🔒 |
| `/broadcast/pengumuman/<uuid>/hapus/` | AnnouncementDeleteView | `announcement_delete` | 🔒 |
| `/broadcast/kalender/` | CalendarView | `calendar` | 🔒 |
| `/broadcast/cms/program/` | CMSProgramListView | `cms_program_list` | 🔒 |
| `/broadcast/cms/program/buat/` | CMSProgramCreateView | `cms_program_create` | 🔒 |
| `/broadcast/cms/program/<uuid>/` | CMSProgramDetailView | `cms_program_detail` | 🔒 |
| `/broadcast/cms/program/<uuid>/hapus/` | CMSProgramDeleteView | `cms_program_confirm_delete` | 🔒 |
| `/broadcast/cms/episode/` | CMSEpisodeListView | `cms_episode_list` | 🔒 |
| `/broadcast/cms/episode/buat/` | CMSEpisodeCreateView | `cms_episode_create` | 🔒 |
| `/broadcast/cms/episode/<uuid>/` | CMSEpisodeDetailView | `cms_episode_detail` | 🔒 |
| `/broadcast/cms/episode/<uuid>/hapus/` | CMSEpisodeDeleteView | `cms_episode_confirm_delete` | 🔒 |
| `/broadcast/api/programs/` | — | — | 🔓 JSON |
| `/broadcast/api/schedule/` | — | — | 🔓 JSON |
| `/broadcast/api/current/` | — | — | 🔓 JSON |
| `/broadcast/api/next/` | — | — | 🔓 JSON |
| `/broadcast/api/playlist/` | — | — | 🔓 JSON |

---

## Radio (`/radio/`, namespace: `radio`)

| URL | View | Name | Auth |
|---|---|---|---|
| `/radio/` | RadioDashboardView | `dashboard` | 🔒 |
| `/radio/station/` | StationListView | `station_list` | 🔒 |
| `/radio/station/buat/` | StationCreateView | `station_create` | 🔒 |
| `/radio/station/<uuid>/edit/` | StationUpdateView | `station_edit` | 🔒 |
| `/radio/station/<uuid>/hapus/` | StationDeleteView | `station_delete` | 🔒 |
| `/radio/provider/` | ProviderListView | `provider_list` | 🔒 |
| `/radio/provider/buat/` | ProviderCreateView | `provider_create` | 🔒 |
| `/radio/provider/<uuid>/edit/` | ProviderUpdateView | `provider_edit` | 🔒 |
| `/radio/provider/<uuid>/hapus/` | ProviderDeleteView | `provider_delete` | 🔒 |
| `/radio/analytics/` | RadioAnalyticsView | `analytics` | 🔒 |
| `/radio/export/csv/<uuid>/` | ExportCSVView | `export_csv` | 🔒 |
| `/radio/api/status/` | — | — | 🔓 |
| `/radio/api/now-playing/` | — | — | 🔓 |
| `/radio/api/health/` | — | — | 🔓 |
| `/radio/api/player-config/` | — | — | 🔓 |
| `/api/v1/radio/live/` | LiveRadioAPIView | — | 🔓 |

---

## Podcast (`/podcast/`, namespace: `podcast`)

| URL | View | Name | Auth |
|---|---|---|---|
| `/podcast/cms/podcast/` | CMSPodcastListView | `cms_podcast_list` | 🔒 |
| `/podcast/cms/podcast/buat/` | CMSPodcastCreateView | `cms_podcast_create` | 🔒 |
| `/podcast/cms/podcast/<uuid>/` | CMSPodcastDetailView | `cms_podcast_detail` | 🔒 |
| `/podcast/cms/podcast/<uuid>/hapus/` | CMSPodcastDeleteView | `cms_podcast_confirm_delete` | 🔒 |
| `/podcast/cms/episode/` | CMSEpisodeListView | `cms_episode_list` | 🔒 |
| `/podcast/cms/episode/buat/` | CMSEpisodeCreateView | `cms_episode_create` | 🔒 |
| `/podcast/cms/episode/<uuid>/` | CMSEpisodeDetailView | `cms_episode_detail` | 🔒 |
| `/podcast/cms/episode/<uuid>/hapus/` | CMSEpisodeDeleteView | `cms_episode_confirm_delete` | 🔒 |

---

## News (`/berita/`, namespace: `news`)

| URL | View | Name | Auth |
|---|---|---|---|
| `/berita/cms/artikel/` | CMSArticleListView | `cms_article_list` | 🔒 |
| `/berita/cms/artikel/buat/` | CMSArticleCreateView | `cms_article_create` | 🔒 |
| `/berita/cms/artikel/<uuid>/` | CMSArticleDetailView | `cms_article_detail` | 🔒 |
| `/berita/cms/artikel/<uuid>/hapus/` | CMSArticleDeleteView | `cms_article_confirm_delete` | 🔒 |

---

## Content Metadata (`/konten/`, namespace: `content`)

| URL | View | Name | Auth |
|---|---|---|---|
| `/konten/` | ContentDashboardView | `dashboard` | 🔒 |
| `/konten/categories/` | CategoryListView | `category_list` | 🔒 |
| `/konten/categories/buat/` | CategoryCreateView | `category_create` | 🔒 |
| `/konten/categories/<uuid>/edit/` | CategoryUpdateView | `category_edit` | 🔒 |
| `/konten/categories/<uuid>/hapus/` | CategoryDeleteView | `category_confirm_delete` | 🔒 |
| `/konten/tags/` | TagListView | `tag_list` | 🔒 |
| `/konten/tags/buat/` | TagCreateView | `tag_create` | 🔒 |
| `/konten/tags/<uuid>/edit/` | TagUpdateView | `tag_edit` | 🔒 |
| `/konten/tags/<uuid>/hapus/` | TagDeleteView | `tag_confirm_delete` | 🔒 |
| `/konten/authors/` | AuthorListView | `author_list` | 🔒 |
| `/konten/authors/buat/` | AuthorCreateView | `author_create` | 🔒 |
| `/konten/authors/<uuid>/` | AuthorDetailView | `author_detail` | 🔒 |
| `/konten/authors/<uuid>/hapus/` | AuthorDeleteView | `author_confirm_delete` | 🔒 |
| `/konten/seo/` | SEOListView | `seo_list` | 🔒 |
| `/konten/seo/buat/` | SEOCreateView | `seo_form` | 🔒 |
| `/konten/highlights/` | HighlightListView | `highlight_list` | 🔒 |
| `/konten/highlights/buat/` | HighlightCreateView | `highlight_create` | 🔒 |
| `/konten/highlights/<uuid>/hapus/` | HighlightDeleteView | `highlight_confirm_delete` | 🔒 |
| `/konten/schedule/` | PublishingQueueView | `publishing_queue` | 🔒 |
| `/konten/versions/` | VersionListView | `version_list` | 🔒 |
| `/konten/versions/<uuid>/` | VersionDetailView | `version_detail` | 🔒 |
| `/konten/audit/` | AuditLogView | `audit_log` | 🔒 |
| `/konten/preview/` | PreviewView | `preview` | 🔒 |
| `/konten/search/` | SearchView | `search_results` | 🔒 |

---

## Media Manager (`/media/`, namespace: `media_manager`)

| URL | View | Name | Auth |
|---|---|---|---|
| `/media/` | MediaDashboardView | `dashboard` | 🔒 |
| `/media/file/` | MediaListView | `list` | 🔒 |
| `/media/upload/` | MediaUploadView | `upload` | 🔒 |
| `/media/folder/` | FolderListView | `folders` | 🔒 |
| `/media/tag/` | TagListView | `tags` | 🔒 |

---

## Settings (`/pengaturan/`)

| URL | View | Auth |
|---|---|---|
| `/pengaturan/` | SiteSettingsView | 🔒 |
| `/pengaturan/seo/` | SEOSettingsView | 🔒 |
| `/pengaturan/email/` | EmailSettingsView | 🔒 |
| `/pengaturan/keamanan/` | SecuritySettingsView | 🔒 |
| `/pengaturan/tampilan/` | AppearanceSettingsView | 🔒 |
| `/pengaturan/notifikasi/` | NotificationSettingsView | 🔒 |
| `/pengaturan/media-sosial/` | SocialMediaSettingsView | 🔒 |
| `/pengaturan/konten/` | ContentSettingsView | 🔒 |
| `/pengaturan/bahasa/` | LanguageSettingsView | 🔒 |
| `/pengaturan/media/` | MediaSettingsView | 🔒 |

---

## Users (`/akun/`, namespace: `users`)

| URL | View | Name | Auth |
|---|---|---|---|
| `/akun/masuk/` | LoginView | `login` | 🔓 |
| `/akun/keluar/` | LogoutView | `logout` | 🔒 |
| `/akun/daftar/` | RegisterView | `register` | 🔓 |
| `/akun/lupa-password/` | ForgotPasswordView | `forgot_password` | 🔓 |
| `/akun/ganti-password/` | ChangePasswordView | `change_password` | 🔒 |
| `/akun/profil/` | ProfileView | `profile` | 🔒 |
| `/akun/verifikasi-email/` | EmailVerificationView | `verify_email` | 🔒 |
| `/akun/2fa/` | TwoFactorSetupView | `two_factor_setup` | 🔒 |
| `/akun/admin/pengguna/` | AdminUserListView | `admin_user_list` | 👑 |
| `/akun/admin/pengguna/buat/` | AdminUserCreateView | `admin_user_create` | 👑 |
| `/akun/admin/pengguna/<uuid>/` | AdminUserDetailView | `admin_user_detail` | 👑 |

---

## Public Website (`/`, namespace: `website`)

| URL | View | Name | Auth |
|---|---|---|---|
| `/` | HomeView | `home` | 🔓 |
| `/tentang/` | AboutView | `about` | 🔓 |
| `/program/` | ProgramListView | `program_list` | 🔓 |
| `/program/<slug>/` | ProgramDetailView | `program_detail` | 🔓 |
| `/jadwal/` | ScheduleView | `schedule` | 🔓 |
| `/podcast/` | PodcastListView | `podcast_list` | 🔓 |
| `/podcast/<slug>/` | PodcastDetailView | `podcast_detail` | 🔓 |
| `/podcast/episode/<uuid>/` | PodcastEpisodeView | `podcast_episode` | 🔓 |
| `/berita/` | NewsListView | `news_list` | 🔓 |
| `/berita/<slug>/` | ArticleDetailView | `article_detail` | 🔓 |
| `/komunitas/` | CommunityView | `community` | 🔓 |
| `/komunitas/<slug>/` | DiscussionView | `community_discussion` | 🔓 |
| `/mitra/` | PartnerListView | `partner_list` | 🔓 |
| `/sponsor/` | SponsorListView | `sponsor_list` | 🔓 |
| `/kontak/` | ContactView | `contact` | 🔓 |
| `/kebijakan-privasi/` | PrivacyView | `privacy` | 🔓 |
| `/syarat-ketentuan/` | TermsView | `terms` | 🔓 |
| `/pencarian/` | SearchView | `search` | 🔓 |
| `/pemeliharaan/` | MaintenanceView | `maintenance` | 🔓 |
| `/radio-live/` | HomeView (alias) | `radio_live` | 🔓 |
| `/newsletter/subscribe/` | NewsletterSubscribeView | `newsletter_subscribe` | 🔓 POST |
| `/offline/` | OfflineView | `offline` | 🔓 |
| `/health/` | health_check | `health_check` | 🔓 |
