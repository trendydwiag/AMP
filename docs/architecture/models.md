# AMP Studio — Data Model Inventory
**Generated:** Sprint 4.0 (July 17, 2026)

All models use `UUIDPrimaryKeyMixin` (UUID PK) and `TimeStampedModel` (created_at, updated_at) unless noted.

---

## apps/users

### User (AbstractBaseUser + PermissionsMixin)
| Field | Type | Notes |
|---|---|---|
| username | CharField | unique |
| email | EmailField | unique |
| first_name | CharField | |
| last_name | CharField | |
| role | CharField (Choice) | SUPERUSER, ADMINISTRATOR, EDITOR, VIEWER |
| is_active | BooleanField | |
| is_staff | BooleanField | |
| email_verified | BooleanField | |
| force_password_change | BooleanField | |
| last_activity | DateTimeField | |
| two_factor_enabled | BooleanField | |
| account_status | CharField (Choice) | ACTIVE, SUSPENDED, INACTIVE, PENDING |
| account_locked_until | DateTimeField | nullable |
| failed_login_attempts | IntegerField | |

**Meta:** ordering=['-created_at']  
**Methods:** lock_account, activate, suspend, verify_totp, get_full_name (property)

### UserProfile
| Field | Type | Relationship |
|---|---|---|
| user | OneToOneField | → User |
| avatar | ImageField | |
| bio | TextField | |
| phone | CharField | |
| date_of_birth | DateField | |
| address | TextField | |

### LoginHistory (FK → User)
Fields: username_attempted, ip_address, user_agent, status, failure_reason, timestamp

### PasswordHistory (FK → User)
Fields: password (hashed), created_at

### AuditLog (FK → User)
Fields: action, resource, details, ip_address, timestamp

### EmailVerification (FK → User)
Fields: token, created_at, expires_at, verified

### TwoFactorDevice (FK → User)
Fields: name, secret, is_primary

---

## apps/platform

### Partner
| Field | Type | Notes |
|---|---|---|
| name | CharField | |
| slug | SlugField | unique |
| api_key | CharField | |
| status | CharField | ACTIVE, SUSPENDED, TRIAL |
| tier | CharField | FREE, BASIC, PRO, ENTERPRISE |
| owner | FK | → users.User |
| logo | ImageField | |
| favicon | ImageField | |
| primary_color | CharField | hex |
| primary_domain | CharField | |
| custom_domains | TextField | |
| max_users | IntegerField | |
| storage_limit | BigIntegerField | bytes |

### PartnerMembership
| Field | Type | Notes |
|---|---|---|
| user | FK | → users.User |
| partner | FK | → Partner |
| role | CharField | |
| is_active | BooleanField | |
**Meta:** unique_together=['user', 'partner']

### PartnerDomain (FK → Partner)
Fields: domain, is_primary, is_verified, ssl_enabled

### PartnerInvitation (FK → Partner, invited_by → users.User)
Fields: email, role, token, status, expires_at

### FeatureFlag
Fields: key, name, description, scope, is_enabled, rollout_percentage, config (JSON), category, required_tier

### FeatureFlagPartner (FK → FeatureFlag, FK → Partner)
Fields: is_enabled, config

### FeatureFlagLog (FK → FeatureFlag, changed_by → users.User)
Fields: action, old_value, new_value

### PartnerTheme (OneToOneField → Partner)
Fields: base_theme, custom_css, colors (JSON), typography (JSON), logo_url, favicon_url

### ThemePreset
Fields: name, slug, description, config (JSON)

---

## apps/broadcast

### Program (FK → platform.Partner, FK → content.Author, M2M → content.ContentTag)
Fields: title, slug, short_description, description, cover_image, thumbnail, category, status (Choice: ACTIVE/INACTIVE/ARCHIVED), seo_title, seo_description, og_image

### Host
Fields: full_name, stage_name, bio, email, phone, instagram, twitter, youtube, avatar

### HostMember (FK → Host, FK → Program)
Fields: is_lead, joined_date

### Schedule (FK → Program)
| Field | Type | Notes |
|---|---|---|
| day_of_week | IntegerField | 0=Monday…6=Sunday |
| start_time | TimeField | |
| end_time | TimeField | |
| timezone | CharField | |
| repeat_weekly | BooleanField | |

### BroadcastSession (FK → Program, FK → Schedule)
Fields: start_datetime, end_datetime, status (Choice: SCHEDULED/LIVE/FINISHED/CANCELLED)

### Episode (FK → BroadcastSession, FK → Program, FK → platform.Partner)
Fields: title, recording_audio, recording_video, status, notes, published_at

### GuestStar
Fields: full_name, biography, photo, organization

### EpisodeGuest (FK → Episode, FK → GuestStar)

### Playlist (FK → Program)
Fields: title, is_active

### PlaylistItem (FK → Playlist)
Fields: title, artist, duration, sequence

### Announcement
Fields: title, content, image, start_date, end_date, is_active

---

## apps/radio

### RadioStation (FK → platform.Partner)
Fields: station_name, logo, timezone, default_volume, autoplay

### RadioProvider (FK → RadioStation)
| Field | Type | Notes |
|---|---|---|
| provider_type | CharField (Choice) | BROADCASTINDO, AZURACAST, ICECAST, SHOUTCAST, RADIOBOSS |
| stream_url | URLField | |
| metadata_url | URLField | |
| username | CharField | auth |
| password | CharField | auth |
| stream_status | CharField (Choice) | ONLINE, OFFLINE, DEGRADED |

**Property:** is_healthy → `stream_status == StreamStatus.ONLINE`

### NowPlayingCache (O2O → RadioStation, FK → RadioProvider)
Fields: song_title, artist, artwork_url, stream_status, cached_at

### ListenerStatistic (FK → RadioStation, FK → RadioProvider)
Fields: current_listeners, peak_listeners, recorded_at

### StreamHealth (FK → RadioStation, FK → RadioProvider)
| Field | Type | Notes |
|---|---|---|
| response_time | FloatField | milliseconds |
| http_status | PositiveIntegerField | HTTP code |
| provider_status | CharField (Choice) | HEALTHY, DEGRADED, DOWN, TIMEOUT |
| stream_bitrate | PositiveIntegerField | kbps |
| stream_format | CharField | e.g. "MP3", "AAC" |
| error_message | TextField | |
| last_checked | DateTimeField | auto_now_add |

### LiveSession (FK → RadioStation)
Fields: program, host, listener_peak, started_at, ended_at

---

## apps/podcast

### Podcast (FK → platform.Partner, FK → content.Author, M2M → content.ContentTag)
Fields: title, slug, description, cover_image, spotify_url, itunes_url, google_podcasts_url, status

### PodcastEpisode (FK → Podcast, FK → platform.Partner)
Fields: title, audio_file, duration, season_number, episode_number, description, status, published_at, download_count

---

## apps/news

### Category (FK → platform.Partner)
Fields: name, slug

### Tag (FK → platform.Partner)
Fields: name, slug

### Article (FK → Category, M2M → Tag, FK → platform.Partner, FK → content.Author, M2M → content.ContentTag, M2M → self as related_articles)
Fields: title, slug, content, excerpt, cover_image, status (DRAFT/PUBLISHED/ARCHIVED), view_count, reading_time, published_at, seo fields

---

## apps/content

### ContentCategory (FK → self as parent)
Fields: name, slug, content_type (Choice: ARTICLE/PROGRAM/PODCAST/GENERAL)

### ContentTag
Fields: name, usage_count

### Author (O2O → users.User)
Fields: display_name, bio, avatar, website, twitter, instagram

### SEOModel (Generic: FK → ContentType + object_id)
Fields: seo_title, seo_description, og_title, og_description, og_image, twitter_title, twitter_description

### ContentVersion (FK → users.User as author)
Fields: content_type (str), content_id (UUID), version_number, data_snapshot (JSON), change_summary

### PublishingQueue (FK → users.User as created_by)
Fields: content_type (str), content_id (UUID), scheduled_at, status (PENDING/PUBLISHED/FAILED/CANCELLED)

### ContentHighlight
Fields: highlight_type, content_type (str), content_id (UUID), active, order

---

## apps/media_manager

### Folder (FK → self as parent, FK → users.User, FK → platform.Partner)
Fields: name, slug

### Tag (⚠ naming conflict with news.Tag)
Fields: name, slug, color

### MediaFile (FK → Folder, M2M → Tag, FK → users.User as uploaded_by, FK → platform.Partner)
Fields: title, file, file_type (Choice: IMAGE/VIDEO/AUDIO/DOCUMENT), mime_type, file_size

---

## apps/community

### Discussion
Fields: title, content, author_name, view_count, reply_count, created_at

### Reply (FK → Discussion)
Fields: content, author_name, is_locked

---

## apps/sponsor

### Partner ⚠ (naming conflict with platform.Partner — different model)
Fields: name, logo, website, partner_type (Choice: SPONSOR/PARTNER/MEDIA_PARTNER), tier (Choice: PLATINUM/GOLD/SILVER/BRONZE), is_active

### Advertisement (FK → sponsor.Partner)
Fields: title, image, link_url, ad_type (Choice: BANNER/POPUP), impressions, clicks, start_date, end_date, is_active

---

## apps/settings (Singleton models — pk=1, no UUID mixin)

All extend `TimeStampedModel` only. Each uses `.load()` class method for singleton access.

| Model | Key Fields |
|---|---|
| SiteSettings | site_name, tagline, logo, favicon, address, contact_email, contact_phone |
| SEOSettings | meta_title, meta_description, google_analytics_id, google_tag_manager_id |
| EmailSettings | smtp_host, smtp_port, smtp_user, from_email |
| SecuritySettings | session_timeout, max_login_attempts, lockout_duration |
| AppearanceSettings | primary_color, secondary_color, font_family |
| NotificationSettings | email_on_registration, email_on_article_publish |
| SocialMediaSettings | facebook, instagram, twitter, youtube, tiktok, spotify, whatsapp, telegram |
| ContentSettings | default_author, articles_per_page, enable_comments |
| LanguageSettings | default_language, timezone, date_format |
| MediaSettings | max_upload_size, allowed_extensions, storage_backend |

---

## Key Relationships Summary

```
platform.Partner
    ├── users.User (owner FK)
    ├── PartnerMembership (M2M → User)
    ├── PartnerDomain (1:N)
    ├── PartnerInvitation (1:N)
    ├── PartnerTheme (1:1)
    ├── FeatureFlagPartner (M2M → FeatureFlag)
    ├── broadcast.Program (1:N)
    ├── broadcast.Episode (1:N)
    ├── radio.RadioStation (1:N)
    ├── podcast.Podcast (1:N)
    ├── podcast.PodcastEpisode (1:N)
    ├── news.Category (1:N)
    ├── news.Tag (1:N)
    ├── news.Article (1:N)
    ├── media_manager.Folder (1:N)
    └── media_manager.MediaFile (1:N)

users.User
    ├── UserProfile (1:1)
    ├── content.Author (1:1)
    ├── LoginHistory (1:N)
    ├── PasswordHistory (1:N)
    ├── AuditLog (1:N)
    ├── EmailVerification (1:N)
    ├── TwoFactorDevice (1:N)
    └── PartnerMembership (M2M → Partner)

broadcast.Program
    ├── broadcast.Schedule (1:N)
    │   └── broadcast.BroadcastSession (1:N)
    │       └── broadcast.Episode (1:N)
    ├── broadcast.HostMember (M2M → Host)
    ├── broadcast.Playlist (1:N)
    │   └── broadcast.PlaylistItem (1:N)
    ├── content.ContentTag (M2M)
    └── content.Author (FK)

radio.RadioStation
    ├── radio.RadioProvider (1:N)
    │   ├── radio.NowPlayingCache (via O2O on station)
    │   ├── radio.ListenerStatistic (1:N)
    │   └── radio.StreamHealth (1:N)
    └── radio.LiveSession (1:N)
```

---

## ⚠ Known Model Issues

| Issue | Description |
|---|---|
| `sponsor.Partner` vs `platform.Partner` | Two models named "Partner" in different apps — confusing imports |
| `news.Tag` vs `media_manager.Tag` vs `content.ContentTag` | Three tag models across different apps |
| `news.Category` vs `content.ContentCategory` | Two category models; potential overlap |
| `community.Discussion.author_name` | CharField, not FK → User — discussions are anonymous |
