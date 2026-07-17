# 04 — Feature Backlog

Complete inventory of Kabulhaden CMS features with implementation status and test coverage per module.

---

## Status Legend

| Status | Meaning |
|---|---|
| **DONE** | Fully implemented, tested, and deployed |
| **PLANNED** | Designed but not yet implemented |
| **PARTIAL** | Core functionality works, enhancements pending |

---

## Module 1: Authentication & User Management

**App**: `apps/users` | **Tests**: 96 | **Status**: DONE

| # | Feature | Status | Notes |
|---|---|---|---|
| 1.1 | Custom User Model (UUID PK) | DONE | `apps/users/models.py:50` |
| 1.2 | Login with Brute-Force Protection | DONE | django-axes, 5 attempts / 15 min lockout |
| 1.3 | Logout with Session Cleanup | DONE | |
| 1.4 | User Registration | DONE | Default role: VIEWER |
| 1.5 | Email Verification (Token-based) | DONE | 48h expiry, `secrets.token_hex(32)` |
| 1.6 | Forgot Password / Password Reset | DONE | 48h token expiry |
| 1.7 | Change Password | DONE | Password history enforcement |
| 1.8 | Two-Factor Authentication (TOTP) | DONE | RFC 6238 implementation |
| 1.9 | 2FA Setup & Disable | DONE | QR provisioning URI |
| 1.10 | User Profile Management | DONE | Avatar, bio, phone, DOB, address |
| 1.11 | Session Timeout Middleware | DONE | Configurable via settings |
| 1.12 | Last Activity Tracking | DONE | Middleware-based |
| 1.13 | Audit Log (All Actions) | DONE | LOGIN, LOGOUT, PASSWORD_CHANGE, etc. |
| 1.14 | Login History (IP + User-Agent) | DONE | For security auditing |
| 1.15 | Password History (Reuse Prevention) | DONE | |
| 1.16 | Account Lock/Unlock | DONE | Time-based lockout |
| 1.17 | Account Suspension | DONE | Admin action |
| 1.18 | Admin User List | DONE | `/akun/admin/pengguna/` |
| 1.19 | Admin User Create | DONE | `/akun/admin/pengguna/buat/` |
| 1.20 | Admin User Detail | DONE | `/akun/admin/pengguna/<uuid>/` |
| 1.21 | Force Password Change Flag | DONE | `force_password_change` field |
| 1.22 | RBAC Role Enforcement | DONE | 4 roles: SUPERUSER, ADMINISTRATOR, EDITOR, VIEWER |
| 1.23 | Password Validators (12 char min) | DONE | 4 validators configured |
| 1.24 | Auth Base Template | DONE | `templates/auth_base.html` |

---

## Module 2: Core System

**App**: `apps/core` | **Tests**: 48 | **Status**: DONE

| # | Feature | Status | Notes |
|---|---|---|---|
| 2.1 | Global Context Processor | DONE | `apps/core/context_processors.py` — SITE_NAME, CURRENT_YEAR |
| 2.2 | Health Check Endpoint | DONE | `/health/` |
| 2.3 | Custom 400 Error Handler | DONE | `apps.core.views.bad_request` |
| 2.4 | Custom 403 Error Handler | DONE | `apps.core.views.permission_denied` |
| 2.5 | Custom 404 Error Handler | DONE | `apps.core.views.page_not_found` |
| 2.6 | Custom 500 Error Handler | DONE | `apps.core.views.server_error` |
| 2.7 | Audit Logging Middleware | DONE | Logs significant user actions |
| 2.8 | Core Homepage Redirect | DONE | Redirects to dashboard or website |
| 2.9 | CSP Nonce Support | DONE | `request.csp_nonce` in templates |
| 2.10 | Error Templates (400/404/500) | DONE | Custom styled error pages |

---

## Module 3: Core Settings

**App**: `apps/settings` | **Tests**: 48 | **Status**: DONE

| # | Feature | Status | Notes |
|---|---|---|---|
| 3.1 | Site Settings (Singleton) | DONE | Name, tagline, logo, favicon, maintenance mode |
| 3.2 | SEO Settings | DONE | Meta tags, OG tags, Twitter cards, GA/GTM, custom scripts |
| 3.3 | Email Settings (SMTP) | DONE | Backend, host, port, TLS/SSL, credentials |
| 3.4 | Security Settings | DONE | Session timeout, password policy, 2FA, IP ranges |
| 3.5 | Appearance Settings | DONE | Colors, fonts, sidebar, dark mode, compact mode |
| 3.6 | Notification Settings | DONE | Email triggers for system events |
| 3.7 | Social Media Settings | DONE | Facebook, Twitter, Instagram, YouTube, TikTok, WhatsApp, Telegram |
| 3.8 | Content Settings | DONE | Posts per page, comments, upload limits |
| 3.9 | Language Settings | DONE | Bahasa Indonesia/English, date/time format, timezone |
| 3.10 | Media Settings | DONE | Storage backend, compression, thumbnails, extensions |
| 3.11 | Settings Dashboard | DONE | `/pengaturan/` — overview page |
| 3.12 | Settings Pages (10 tabs) | DONE | Each model has a dedicated view |

---

## Module 4: Media Manager

**App**: `apps/media_manager` | **Tests**: — | **Status**: DONE

| # | Feature | Status | Notes |
|---|---|---|---|
| 4.1 | Media Dashboard | DONE | `/media/` |
| 4.2 | File Upload | DONE | UUID filename generation |
| 4.3 | Media List (Filterable) | DONE | `/media/file/` |
| 4.4 | Media Detail View | DONE | `/media/file/<uuid>/` |
| 4.5 | Media Delete | DONE | `/media/file/<uuid>/hapus/` |
| 4.6 | Bulk Delete | DONE | `/media/bulk-delete/` |
| 4.7 | Folder Management | DONE | Hierarchical folders with slug |
| 4.8 | Folder Create | DONE | `/media/folder/buat/` |
| 4.9 | Folder Delete | DONE | `/media/folder/<uuid>/hapus/` |
| 4.10 | Tag Management | DONE | Colored tags with slug |
| 4.11 | Tag Create | DONE | `/media/tag/buat/` |
| 4.12 | Tag Delete | DONE | `/media/tag/<uuid>/hapus/` |
| 4.13 | Media Search API | DONE | `/media/api/search/` — JSON endpoint |
| 4.14 | File Type Detection | DONE | IMAGE, VIDEO, DOCUMENT, AUDIO, OTHER |
| 4.15 | File Size Formatting | DONE | Auto-scales B/KB/MB/GB/TB |
| 4.16 | Thumbnail Support | DONE | `thumbnail` field on MediaFile |

---

## Module 5: Radio Engine

**App**: `apps/radio` | **Tests**: 69 | **Status**: DONE

| # | Feature | Status | Notes |
|---|---|---|---|
| 5.1 | Radio Dashboard | DONE | `/radio/` |
| 5.2 | Radio Station CRUD | DONE | Create, edit, delete stations |
| 5.3 | Radio Provider CRUD | DONE | Create, edit, delete streaming providers |
| 5.4 | Multi-Provider Support | DONE | Icecast, Shoutcast, RadioBoss, AzuraCast |
| 5.5 | Now Playing Cache | DONE | Database-cached track info |
| 5.6 | Listener Statistics | DONE | Current + peak listeners |
| 5.7 | Stream Health Monitoring | DONE | Response time, HTTP status, bitrate |
| 5.8 | Live Session Tracking | DONE | Program, host, peak listeners |
| 5.9 | Radio Analytics Page | DONE | `/radio/analytics/` |
| 5.10 | CSV Export | DONE | `/radio/export/csv/<station_id>/` |
| 5.11 | Excel Export | DONE | `/radio/export/excel/<station_id>/` |
| 5.12 | Status API | DONE | `/radio/api/status/` |
| 5.13 | Player API | DONE | `/radio/api/player/` |
| 5.14 | Now Playing API | DONE | `/radio/api/now-playing/` |
| 5.15 | Listener API | DONE | `/radio/api/listener/` |
| 5.16 | Health Check API | DONE | `/radio/api/health/` |
| 5.17 | Current Program API | DONE | `/radio/api/current-program/` |
| 5.18 | Current Host API | DONE | `/radio/api/current-host/` |
| 5.19 | Providers API | DONE | `/radio/api/providers/` |
| 5.20 | Player Config API | DONE | `/radio/api/player-config/` |
| 5.21 | Station Player Preview | DONE | `templates/radio/player.html` |
| 5.22 | Wave Animation Component | DONE | `templates/radio/components/wave_animation.html` |
| 5.23 | Floating Player Component | DONE | `templates/radio/components/floating_player.html` |
| 5.24 | Listener Counter Component | DONE | `templates/radio/components/listener_counter.html` |
| 5.25 | Status Badge Component | DONE | `templates/radio/components/status_badge.html` |
| 5.26 | Mini Player Component | DONE | `templates/radio/components/mini_player.html` |

---

## Module 6: Broadcast Management

**App**: `apps/broadcast` | **Tests**: 120 | **Status**: DONE

| # | Feature | Status | Notes |
|---|---|---|---|
| 6.1 | Broadcast Dashboard | DONE | `/broadcast/` |
| 6.2 | Program CRUD | DONE | Title, slug, description, category, rating, SEO |
| 6.3 | Host CRUD | DONE | Full name, stage name, bio, social links |
| 6.4 | Host-Program Membership | DONE | `HostMember` model, lead flag |
| 6.5 | Schedule CRUD | DONE | Day-of-week, start/end time, timezone, repeat |
| 6.6 | Broadcast Session CRUD | DONE | Scheduled, Live, Finished, Cancelled, Delayed |
| 6.7 | Episode CRUD | DONE | Episode number, audio/video recording, publish date |
| 6.8 | Announcement CRUD | DONE | Time-bounded, with image |
| 6.9 | Calendar View | DONE | `/broadcast/kalender/` |
| 6.10 | Playlist Management | DONE | Per-program playlists with ordered items |
| 6.11 | Guest Star Management | DONE | Bio, photo, organization, social links |
| 6.12 | Episode Guest Association | DONE | Role per episode |
| 6.13 | Programs API | DONE | `/broadcast/api/programs/` |
| 6.14 | Program Detail API | DONE | `/broadcast/api/program/<slug>/` |
| 6.15 | Schedule API | DONE | `/broadcast/api/schedule/` |
| 6.16 | Today Schedule API | DONE | `/broadcast/api/today/` |
| 6.17 | Current Broadcast API | DONE | `/broadcast/api/current/` |
| 6.18 | Next Broadcast API | DONE | `/broadcast/api/next/` |
| 6.19 | Hosts API | DONE | `/broadcast/api/hosts/` |
| 6.20 | Host Detail API | DONE | `/broadcast/api/host/<uuid>/` |
| 6.21 | Episodes API | DONE | `/broadcast/api/episodes/` |
| 6.22 | Playlist API | DONE | `/broadcast/api/playlist/` |

---

## Module 7: Podcast

**App**: `apps/podcast` | **Tests**: — | **Status**: DONE

| # | Feature | Status | Notes |
|---|---|---|---|
| 7.1 | Podcast CRUD | DONE | Title, slug, description, category, external links |
| 7.2 | Podcast Episode CRUD | DONE | Audio file, duration, season/episode numbers |
| 7.3 | Category System | DONE | 12 categories (News, Entertainment, Education, etc.) |
| 7.4 | External Platform Links | DONE | Spotify, iTunes, Google Podcasts |
| 7.5 | Download Counter | DONE | `download_count` field |
| 7.6 | Featured Podcasts | DONE | `featured` boolean flag |
| 7.7 | SEO per Podcast | DONE | `seo_title`, `seo_description` |

---

## Module 8: News

**App**: `apps/news` | **Tests**: — | **Status**: DONE

| # | Feature | Status | Notes |
|---|---|---|---|
| 8.1 | Article CRUD | DONE | Title, slug, content, featured image |
| 8.2 | Category System | DONE | Name, slug, description |
| 8.3 | Tag System | DONE | Name, slug |
| 8.4 | Draft/Published Workflow | DONE | `status` field with publish date |
| 8.5 | View Counter | DONE | `view_count` field |
| 8.6 | SEO per Article | DONE | `seo_title`, `seo_description` |
| 8.7 | Author Name | DONE | `author_name` field (default: "Redaksi") |

---

## Module 9: Sponsor & Partner

**App**: `apps/sponsor` | **Tests**: — | **Status**: DONE

| # | Feature | Status | Notes |
|---|---|---|---|
| 9.1 | Partner CRUD | DONE | Name, slug, logo, website, type, tier |
| 9.2 | Partner Types | DONE | Sponsor, Partner, Media Partner |
| 9.3 | Tier System | DONE | Platinum, Gold, Silver, Bronze |
| 9.4 | Advertisement CRUD | DONE | Title, image, link, type, scheduling |
| 9.5 | Ad Types | DONE | Banner, Sidebar, Popup, Footer |
| 9.6 | Impression/Click Tracking | DONE | `impressions`, `clicks` fields |
| 9.7 | Active/Featured Flags | DONE | Filter and sort |

---

## Module 10: Community

**App**: `apps/community` | **Tests**: — | **Status**: DONE

| # | Feature | Status | Notes |
|---|---|---|---|
| 10.1 | Discussion CRUD | DONE | Title, slug, content, author |
| 10.2 | Reply System | DONE | Per-discussion threaded replies |
| 10.3 | Pin/Lock Discussions | DONE | `is_pinned`, `is_locked` flags |
| 10.4 | View Counter | DONE | `view_count` field |
| 10.5 | Reply Counter | DONE | `reply_count` field |
| 10.6 | Category Tagging | DONE | `category` field on discussions |

---

## Module 11: Public Website

**App**: `apps/website` | **Tests**: 172 | **Status**: DONE

| # | Feature | Status | Notes |
|---|---|---|---|
| 11.1 | Homepage | DONE | 9 sections: hero, programs, schedule, about, podcast, news, community, sponsors, newsletter |
| 11.2 | About Page | DONE | Site info, social media, partners |
| 11.3 | Program List | DONE | Active programs grid |
| 11.4 | Program Detail | DONE | Episodes + schedules per program |
| 11.5 | Schedule Page | DONE | Weekly calendar view |
| 11.6 | Podcast List | DONE | Active + featured podcasts |
| 11.7 | Podcast Detail | DONE | Episodes list |
| 11.8 | Podcast Episode | DONE | Audio player |
| 11.9 | News List | DONE | Published articles |
| 11.10 | Article Detail | DONE | With related articles + view increment |
| 11.11 | Community Page | DONE | Discussions + pinned threads |
| 11.12 | Community Discussion | DONE | Thread + replies |
| 11.13 | Partner List | DONE | Active partners by type |
| 11.14 | Sponsor List | DONE | Active sponsors |
| 11.15 | Contact Page | DONE | Site settings + social media |
| 11.16 | Privacy Policy | DONE | Static page |
| 11.17 | Terms & Conditions | DONE | Static page |
| 11.18 | Search | DONE | Cross-content search (programs, articles, podcasts) |
| 11.19 | Maintenance Mode | DONE | Template with site settings |
| 11.20 | Newsletter Subscribe | DONE | AJAX POST endpoint |
| 11.21 | Navbar (Responsive) | DONE | Desktop dropdown, mobile hamburger menu |
| 11.22 | Sticky Radio Player | DONE | Bottom player bar with AlpineJS |
| 11.23 | Search Modal (⌘K) | DONE | Keyboard shortcut trigger |
| 11.24 | SEO Structured Data | DONE | JSON-LD: website, organization, article, podcast, breadcrumb |
| 11.25 | Footer | DONE | Links, social media, newsletter |
| 11.26 | Mobile Fullscreen Player | DONE | Touch-optimized player overlay |

---

## Test Coverage Summary

| Module | Tests | Coverage Focus |
|---|---|---|
| Authentication & Users | 96 | Login, registration, 2FA, RBAC, audit, password policies |
| Core System | 48 | Context processors, health checks, error handlers, middleware |
| Core Settings | 48 | All 10 singleton settings, CRUD operations |
| Radio Engine | 69 | Provider integration, now-playing, listeners, health, APIs |
| Broadcast Management | 120 | All CRUD operations, scheduling, episodes, APIs |
| Public Website | 172 | All public pages, search, newsletter, SEO, responsiveness |
| **Total** | **509** | |

---

## Planned Features (Not Yet Implemented)

| # | Feature | Module | Priority |
|---|---|---|---|
| P-1 | Dark mode for public website | Website | Medium |
| P-2 | Push notifications for live shows | Radio | Low |
| P-3 | Multi-language podcast metadata | Podcast | Low |
| P-4 | Real-time WebSocket listener count | Radio | Medium |
| P-5 | Drag-and-drop schedule builder | Broadcast | High |
| P-6 | Automated social media posting | Broadcast | Medium |
| P-7 | Advanced analytics dashboard | Radio | Medium |
| P-8 | Content versioning / revision history | News | High |
| P-9 | Multi-station support | Radio | Low |
| P-10 | API rate limiting | Core | Medium |
