# Test Coverage

## Settings App (16 tests)

### Models (11 tests)
- `test_site_settings_singleton` — SiteSettings.load() returns pk=1
- `test_seo_settings_singleton` — SEOSettings singleton
- `test_email_settings_singleton` — EmailSettings singleton
- `test_security_settings_singleton` — SecuritySettings defaults
- `test_appearance_settings_singleton` — AppearanceSettings defaults
- `test_notification_settings_singleton` — NotificationSettings defaults
- `test_social_media_settings_singleton` — SocialMediaSettings singleton
- `test_content_settings_singleton` — ContentSettings defaults
- `test_language_settings_singleton` — LanguageSettings defaults
- `test_media_settings_singleton` — MediaSettings defaults
- `test_str_repr` — String representations

### Views (5 tests)
- `test_admin_can_access_site_settings` — Admin access
- `test_non_admin_redirected` — Non-admin blocked
- `test_unauthenticated_redirected` — Auth required
- `test_update_site_settings` — POST update
- `test_all_settings_urls` — All 10 settings URLs return 200

---

## Media Manager App (32 tests)

### Models (8 tests)
- `test_create_folder` — Folder creation + auto slug
- `test_folder_str` — String representation
- `test_folder_full_path` — Parent/child path
- `test_folder_file_count` — File count property
- `test_folder_unique_name_per_parent` — DB constraint
- `test_create_tag` — Tag creation + auto slug
- `test_tag_str` — String representation
- `test_create_media_file` — MediaFile creation
- `test_formatted_size` — Size formatting
- `test_file_type_properties` — is_image, is_video, etc.
- `test_type_badge_color` — CSS class mapping

### Services (9 tests)
- `FolderService.test_create_and_get` — Create folder
- `FolderService.test_delete_folder` — Delete folder
- `TagService.test_create_tag` — Create tag
- `TagService.test_delete_tag` — Delete tag
- `MediaFileService.test_upload_file` — Upload file
- `MediaFileService.test_detect_image_type` — MIME detection
- `MediaFileService.test_detect_video_type` — MIME detection
- `MediaFileService.test_delete_file` — Delete file
- `MediaFileService.test_get_stats` — Statistics

### Forms/Validators (3 tests)
- `test_validate_valid_file` — Valid file passes
- `test_validate_invalid_extension` — .exe rejected
- `test_validate_oversized_file` — >10MB rejected

### Views (8 tests)
- `test_dashboard_requires_admin` — Non-admin blocked
- `test_admin_can_access_dashboard` — Admin access
- `test_list_view` — File list
- `test_upload_view_get` — Upload form
- `test_upload_view_post` — Upload POST
- `test_folders_view` — Folder management
- `test_tags_view` — Tag management
- `test_search_api` — JSON search API

---

## Radio App (46 tests)

### Repositories (15 tests)
- `RadioStationRepositoryTest` — get_active_stations, get_primary_station, get_primary_station_none
- `RadioProviderRepositoryTest` — get_active_providers, get_for_station, get_primary_provider
- `NowPlayingCacheRepositoryTest` — get_for_station, get_for_station_none, get_or_none
- `ListenerStatisticRepositoryTest` — get_for_station, get_recent, get_latest
- `StreamHealthRepositoryTest` — get_for_station, get_latest
- `LiveSessionRepositoryTest` — get_active, get_active_none, get_for_station

### Services (31 tests)
- `NowPlayingServiceTest` — refresh_from_provider, get_now_playing, get_now_playing_none, refresh_all
- `ListenerServiceTest` — refresh_from_provider, get_current, get_hourly_stats, export_csv
- `StreamHealthServiceTest` — refresh_from_provider, get_latest
- `LiveSessionServiceTest` — get_active, get_active_none, start_session, end_session
- `MetadataServiceTest` — get_track_info, get_track_info_none
- `ArtworkServiceTest` — get_artwork, get_artwork_empty
- `FallbackServiceTest` — get_fallback_stream, get_fallback_stream_none
- `RadioStationServiceTest` — get_primary_station, get_primary_station_none, get_active_stations, create_station, toggle_active
- `RadioProviderServiceTest` — get_for_station, get_primary_provider, create_provider, toggle_active

---

## Total: 194 tests (all passing)
