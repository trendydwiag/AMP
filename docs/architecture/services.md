# AMP Studio — Service & Repository Inventory
**Generated:** Sprint 4.0 (July 17, 2026)

---

## Base Infrastructure (`utils/`)

### BaseRepository (`utils/repositories.py`)
Generic CRUD operations. All app repositories extend this.

| Method | Signature | Description |
|---|---|---|
| `get_by_id` | `(pk)` | Get single record by UUID |
| `list_all` | `(**filters)` | List with optional filters |
| `create` | `(**data)` | Create + full_clean validation |
| `update` | `(instance, **data)` | Update + full_clean |
| `delete` | `(instance)` | Hard delete |

### BaseService (`utils/services.py`)
Transaction wrapper. All app services extend this.

| Method | Description |
|---|---|
| `execute_in_transaction(fn)` | Wraps callable in `atomic()` |

---

## Broadcast Module (`apps/broadcast/`)

### Services

| Service | Key Methods | Notes |
|---|---|---|
| `ProgramService` | create, update, delete, get_featured, get_active | Program lifecycle |
| `HostService` | create, update, delete, get_by_program | Host management |
| `ScheduleService` | create, update, delete, check_overlap, get_available_slots | Time conflict detection |
| `BroadcastService` | start_session, end_session, get_live_session | Session state |
| `EpisodeService` | create, update, publish, archive | Episode lifecycle |
| `PlaylistService` | add_item, remove_item, reorder_items | Sequence management |
| `AnnouncementService` | create, update, get_active | Active window filtering |
| `CalendarService` | get_week_view, get_day_view | Calendar data assembly |

### Repositories

| Repository | Key Queries |
|---|---|
| `ProgramRepository` | get_active, get_featured, get_by_partner |
| `HostRepository` | get_by_program, get_available |
| `ScheduleRepository` | get_by_day, get_current, get_upcoming |
| `EpisodeRepository` | get_published, get_by_program, get_recent |
| `AnnouncementRepository` | get_active_now |

---

## Radio Module (`apps/radio/`)

### Services

| Service | Key Methods | Notes |
|---|---|---|
| `RadioStationService` | create, update, get_by_partner | Station management |
| `RadioProviderService` | create, update, set_primary | Provider management |
| `StreamHealthService` | check_health, get_health_history | Health probing |
| `ListenerService` | get_current, get_peak, record | Listener tracking |
| `NowPlayingService` | get_cached, refresh, clear_cache | Now-playing cache management |

### Repositories

| Repository | Key Queries |
|---|---|
| `RadioStationRepository` | get_by_partner, get_active |
| `RadioProviderRepository` | get_by_station, get_primary |
| `StreamHealthRepository` | get_latest, get_history(limit) |
| `ListenerRepository` | get_peak, get_by_date_range |

### Adapters (Provider Abstraction)

| Adapter | Provider | Status |
|---|---|---|
| `BroadcastindoAdapter` | Broadcastindo (`a7.siar.us`) | ✅ Active |
| `AzuraCastAdapter` | AzuraCast | 🟡 Exists, not configured |
| `IcecastAdapter` | Icecast | ⚪ Stub |
| `ShoutcastAdapter` | Shoutcast | ⚪ Stub |
| `RadioBossAdapter` | RadioBoss | ⚪ Stub |

**Pattern:** All adapters implement `get_now_playing()` and `get_listener_count()`.

---

## Podcast Module (`apps/podcast/`)

### Services

| Service | Key Methods |
|---|---|
| `PodcastService` | create, update, publish, archive |
| `PodcastEpisodeService` | create, update, publish, track_download |

### Repositories

| Repository | Key Queries |
|---|---|
| `PodcastRepository` | get_published, get_by_partner |
| `PodcastEpisodeRepository` | get_by_podcast, get_published, get_latest |

---

## News Module (`apps/news/`)

### Services

| Service | Key Methods |
|---|---|
| `ArticleService` | create, update, publish, archive, schedule |
| `CategoryService` | create, update, delete |
| `TagService` | create, find_or_create |

### Repositories

| Repository | Key Queries |
|---|---|
| `ArticleRepository` | get_published, get_by_category, get_by_tag, get_recent |
| `CategoryRepository` | get_by_partner |
| `TagRepository` | get_by_partner, get_popular |

---

## Content Module (`apps/content/`)

### Services

| Service | Key Methods | Notes |
|---|---|---|
| `ContentTagService` | find_or_create, increment_usage | Global tag management |
| `AuthorService` | create, update, get_by_user | Author profile management |
| `ContentVersionService` | create_snapshot, get_history, restore | Version control |
| `PublishingQueueService` | schedule, cancel, get_pending, process_due | Publishing queue |
| `ContentHighlightService` | set_highlight, remove_highlight | Content featuring |
| `SEOService` | get_or_create, update | Generic SEO metadata |

---

## Media Manager Module (`apps/media_manager/`)

### Services

| Service | Key Methods |
|---|---|
| `MediaFileService` | upload, delete, get_by_folder, get_by_type, search |
| `FolderService` | create, rename, delete, get_tree |
| `TagService` | create, find_or_create, get_popular |

### Repositories

| Repository | Key Queries |
|---|---|
| `MediaFileRepository` | get_by_folder, get_by_type, get_by_partner, search |
| `FolderRepository` | get_tree, get_by_partner |

---

## Settings Module (`apps/settings/`)

All settings services use the **singleton pattern**: `SettingsModel.objects.get_or_create(pk=1)`.

| Service | Key Methods |
|---|---|
| `SiteSettingsService` | load, save |
| `SEOSettingsService` | load, save |
| `EmailSettingsService` | load, save, test_connection |
| `SecuritySettingsService` | load, save |
| `AppearanceSettingsService` | load, save |
| `NotificationSettingsService` | load, save |
| `SocialMediaSettingsService` | load, save |
| `ContentSettingsService` | load, save |
| `LanguageSettingsService` | load, save |
| `MediaSettingsService` | load, save |

---

## Users Module (`apps/users/`)

### Services

| Service | Key Methods |
|---|---|
| `UserService` | create_user, update_role, suspend, activate, lock, unlock |
| `ProfileService` | get_or_create, update_avatar, update_bio |
| `AuthService` | login, logout, verify_email, reset_password, change_password |

### Repositories

| Repository | Key Queries |
|---|---|
| `UserRepository` | get_by_role, get_by_status, get_active |
| `ProfileRepository` | get_by_user |

---

## Community Module (`apps/community/`)

| Service | Key Methods |
|---|---|
| `DiscussionService` | create, get_trending, increment_view |
| `ReplyService` | create, lock, increment_count |

---

## Sponsor Module (`apps/sponsor/`)

| Service | Key Methods |
|---|---|
| `SponsorPartnerService` | create, update, get_active, get_by_tier |
| `AdvertisementService` | create, update, record_impression, record_click, get_active |

---

## Studio Views (Inline Logic — Technical Debt)

`AMPStudioDashboardView` in `apps/studio/views.py` contains **direct model queries** that bypass the service layer:
- Calculates total storage used from `MediaFile`
- Aggregates health check results from `StreamHealth`
- Counts pending review items from multiple models
- Queries system stats from `users.User`, `news.Article`, `podcast.PodcastEpisode`, etc.

**TD Note:** This logic should eventually be extracted to a `StudioService` or `DashboardService`.

---

## Utilities

| Location | Purpose |
|---|---|
| `utils/services.py` | BaseService (transaction wrapper) |
| `utils/repositories.py` | BaseRepository (generic CRUD) |
| `apps/core/context_processors.py` | Global template context (SiteSettings, SocialMediaSettings) |
| `apps/broadcast/templatetags/` | Broadcast-specific template filters |
| `apps/users/templatetags/role_tags.py` | `{% has_role %}` templatetag for RBAC checks in templates |
