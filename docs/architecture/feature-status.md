# AMP Studio — Feature Status Inventory
**Generated:** Sprint 4.0 (July 17, 2026)
**Status Legend:** ✅ Complete | 🟡 Partial | ⚪ Planned

---

## Module 1: Authentication & User Management (`apps/users`)

| Feature | Status | Notes |
|---|---|---|
| Custom User Model (UUID PK) | ✅ | AbstractBaseUser, 4 RBAC roles |
| Login with Brute-Force Protection | ✅ | django-axes, 5 attempts / 15 min lockout |
| Logout + Session Cleanup | ✅ | |
| User Registration | ✅ | Default role: VIEWER |
| Email Verification (Token-based) | ✅ | 48h expiry |
| Forgot / Reset Password | ✅ | 48h token expiry |
| Change Password | ✅ | Password history enforcement |
| Two-Factor Authentication (TOTP) | ✅ | RFC 6238 |
| 2FA Setup & Disable | ✅ | QR provisioning URI |
| User Profile (avatar, bio, phone) | ✅ | `UserProfile` O2O User |
| Session Timeout Middleware | ✅ | Configurable |
| Last Activity Tracking | ✅ | Middleware-based |
| Audit Log (all actions) | ✅ | LOGIN, LOGOUT, PASSWORD_CHANGE, etc. |
| Login History (IP + User-Agent) | ✅ | |
| Password History (reuse prevention) | ✅ | |
| Account Lock / Unlock | ✅ | Time-based + admin manual |
| Account Suspension | ✅ | Admin action |
| Admin: User List | ✅ | `/akun/admin/pengguna/` — AMP Studio layout ✓ |
| Admin: User Create | ✅ | `/akun/admin/pengguna/buat/` — AMP Studio layout ✓ |
| Admin: User Detail | ✅ | `/akun/admin/pengguna/<uuid>/` — AMP Studio layout ✓ |
| User Profile Page | ✅ | `/akun/profil/` — AMP Studio layout ✓ |
| 2FA Setup Page | ✅ | `/akun/2fa/` — AMP Studio layout ✓ |
| Force Password Change Flag | ✅ | |
| RBAC Role Enforcement | ✅ | role_tags templatetag |

---

## Module 2: Core System (`apps/core`)

| Feature | Status | Notes |
|---|---|---|
| Global Context Processor | ✅ | SiteSettings + SocialMediaSettings → all templates |
| Health Check Endpoint | ✅ | `/health/` |
| Custom Error Handlers (400/403/404/500) | ✅ | |
| AuditLog Middleware | ✅ | |
| Offline Page (PWA) | ✅ | `/offline/` |

---

## Module 3: Settings (`apps/settings`)

| Feature | Status | Notes |
|---|---|---|
| Site Identity (name, logo, tagline) | ✅ | Logo served via context processor |
| Contact Info (address, email, phone) | ✅ | Added Sprint 3.6 |
| SEO Settings | ✅ | |
| Email / SMTP Settings | ✅ | Config exists, not verified in dev |
| Security Settings | ✅ | |
| Appearance / Theming Settings | ✅ | |
| Notification Settings | ✅ | |
| Social Media Links | ✅ | Footer icons from DB (Sprint 3.6) |
| Content Defaults | ✅ | |
| Language / Localization | ✅ | |
| Media / Storage Settings | ✅ | |
| Settings Sidebar Navigation | ✅ | `/pengaturan/` — settings/base.html |
| ClearableFileInput → plain FileInput | 🟡 | TD: Django's ugly "Currently: file □ Clear" still shows on logo field |

---

## Module 4: Media Manager (`apps/media_manager`)

| Feature | Status | Notes |
|---|---|---|
| File Upload | ✅ | `/media/upload/` |
| Folder Organization | ✅ | Nested folders |
| Tag System | ✅ | |
| File List View | ✅ | |
| Media Dashboard | ✅ | AMP Studio layout ✓ (inner sidebar removed Sprint 3.6) |
| Media Search API | 🟡 | API exists; advanced filtering partial |
| Bulk Operations | 🟡 | UI partial |
| Image Compression | 🟡 | Management command only |
| Thumbnail Generation | 🟡 | Management command only |

---

## Module 5: Radio Engine (`apps/radio`)

| Feature | Status | Notes |
|---|---|---|
| Multi-Provider Framework | ✅ | Provider type enum: Broadcastindo, AzuraCast, Icecast, RadioBoss, Shoutcast |
| Broadcastindo Adapter | ✅ | Active in dev (a7.siar.us) |
| AzuraCast Adapter | 🟡 | Adapter exists; not configured in dev |
| Now-Playing Cache (20s TTL) | ✅ | `NowPlayingCache` model + cache key |
| Stream Health Monitoring | ✅ | `StreamHealth` model, `check_stream_health` command |
| Listener Statistics | ✅ | `ListenerStatistic` model |
| Live Session Tracking | ✅ | `LiveSession` model |
| Radio Dashboard | ✅ | AMP Studio layout ✓ |
| Station CRUD | ✅ | |
| Provider CRUD | ✅ | |
| Analytics View | ✅ | Template + view exist |
| Export (CSV/Excel) | ✅ | |
| Public API: `/api/v1/radio/live/` | ✅ | Normalized schema, provider-agnostic |
| Program field in live API | ❌ | **TD-001** — always returns null |
| Fallback stream URL | ❌ | **TD-002** — empty string if provider omits it |
| Automated tests for live API | ❌ | **TD-003** |
| WebSocket / SSE for real-time | ⚪ | Planned (ADR future: Django Channels) |
| Streaming Center | ✅ | `/studio/streaming/` — template field names fixed Sprint 4.0 |

---

## Module 6: Broadcast Management (`apps/broadcast`)

| Feature | Status | Notes |
|---|---|---|
| Program CRUD | ✅ | AMP Studio layout ✓ |
| Host CRUD | ✅ | AMP Studio layout ✓ |
| Schedule Management (day/time) | ✅ | AMP Studio layout ✓ |
| Broadcast Sessions | ✅ | |
| Episode Management | ✅ | AMP Studio layout ✓ |
| Guest Star Management | ✅ | |
| Playlist + Items | ✅ | Drag-reorder via PlalistItemService |
| Announcements | ✅ | AMP Studio layout ✓ |
| Calendar View | ✅ | AMP Studio layout ✓ |
| CMS Workflow (cms/program/, cms/episode/) | ✅ | Detailed review/publish workflow |
| Public APIs (programs, schedule, current, next, playlist) | ✅ | JSON endpoints |
| Broadcast Dashboard | ✅ | AMP Studio layout ✓ |

---

## Module 7: Podcast (`apps/podcast`)

| Feature | Status | Notes |
|---|---|---|
| Podcast Series CRUD | ✅ | AMP Studio layout ✓ |
| Episode CRUD | ✅ | AMP Studio layout ✓ |
| Season/Episode Numbering | ✅ | |
| External Platform Links | ✅ | Spotify, iTunes, Google Podcasts fields |
| Download Tracking | 🟡 | Field exists; no dedicated download endpoint |
| RSS Feed | ⚪ | Planned |
| Podcast Dashboard | ✅ | |

---

## Module 8: News (`apps/news`)

| Feature | Status | Notes |
|---|---|---|
| Article CRUD | ✅ | AMP Studio layout ✓ |
| Draft / Published Workflow | ✅ | |
| Article Scheduling | ✅ | Via PublishingQueue in content module |
| Category Management | 🟡 | Exists in news app; also in content app (potential overlap) |
| Tag Management | 🟡 | Exists in news app; also in content app |
| View Count | ✅ | |
| SEO per Article | ✅ | Via content.SEOModel |
| Autosave | ✅ | HTMX-based autosave |
| Related Articles | ✅ | M2M self |
| Article Dashboard | ✅ | |

---

## Module 9: Sponsor / Advertisement (`apps/sponsor`)

| Feature | Status | Notes |
|---|---|---|
| Sponsor/Partner List | ✅ | |
| Tier Classification | ✅ | Platinum/Gold/Silver/Bronze |
| Advertisement Management | ✅ | Banner, popup types |
| Impression / Click Tracking | ✅ | Counter fields |
| Ad Scheduling | 🟡 | Date fields exist; no auto-activation |
| Iklan page in Studio | ✅ | `/studio/iklan/` — AMP Studio layout ✓ |

---

## Module 10: Community (`apps/community`)

| Feature | Status | Notes |
|---|---|---|
| Discussion Threads | ✅ | |
| Replies | ✅ | Reply locking |
| View/Reply Count | ✅ | |
| Community page in Studio | ✅ | `/studio/komunitas/` — AMP Studio layout ✓ |
| Moderation / Reporting | ⚪ | Planned |
| Listener Registration | ⚪ | Planned |

---

## Module 11: Platform / Multi-Tenant (`apps/platform`)

| Feature | Status | Notes |
|---|---|---|
| Partner Model | ✅ | UUID PK, tier, branding, limits |
| Partner Membership | ✅ | User → Partner with role |
| Partner Domain Resolution | ✅ | `PartnerDomain` model |
| Partner Invitation System | ✅ | Token-based, role-scoped |
| Feature Flags | ✅ | Per-flag + per-partner override |
| Feature Flag Logging | ✅ | |
| Per-Partner Theme Engine | ✅ | `PartnerTheme` O2O Partner |
| Theme Presets | ✅ | |
| Partner Switch (Studio sidebar) | ✅ | SUPERUSER/ADMIN only |
| Unapplied migrations in platform | ❌ | **TD-006** — migration state unconfirmed |

---

## Module 12: AMP Studio CMS Hub (`apps/studio`)

| Feature | Status | Notes |
|---|---|---|
| Studio Dashboard | ✅ | Aggregates stats from all apps |
| Dark Mode Toggle | ✅ | data-theme + .dark class (fixed Sprint 4.0) |
| Sidebar Navigation | ✅ | Collapsible, role-filtered |
| Command Palette (Ctrl+K) | ✅ | |
| Notification Panel | ✅ | |
| Radio Player Bar | ✅ | Alpine.store('radio') |
| Setup Wizard | ✅ | Session-based, 5 steps |
| Guided Tour | ✅ | localStorage-based |
| Health Widget | ✅ | Stream health in header |
| Partner Switcher Dropdown | ✅ | |
| Calendar View | ✅ | |
| Media Explorer | ✅ | |
| Analytics Dashboard | 🟡 | View + template exist; data stub |
| Setup Wizard | ✅ | |
| Streaming Center | ✅ | Field name bug fixed Sprint 4.0 |
| Komunitas Hub | ✅ | |
| Iklan / Sponsor Hub | ✅ | |

---

## Module 13: Public Website (`apps/website`)

| Feature | Status | Notes |
|---|---|---|
| Homepage with live radio player | ✅ | |
| Program Listing | ✅ | |
| Broadcast Schedule | ✅ | |
| Podcast Listing | ✅ | |
| News / Article Listing | ✅ | |
| Community Page | ✅ | |
| Sponsor / Mitra Page | ✅ | |
| Contact Page | ✅ | |
| Newsletter Subscribe | ✅ | |
| About Page | ✅ | |
| Privacy / Terms Pages | ✅ | |
| Offline Page (PWA) | ✅ | |
| Search | 🟡 | `/pencarian/` exists; full-text depth varies |
| Maintenance Mode | ✅ | |
| Logo from DB | ✅ | Via context processor (Sprint 3.6) |
| Social Media links from DB | ✅ | Footer icons (Sprint 3.6) |
| Contact info from DB | ✅ | Footer Hubungi Kami (Sprint 3.6) |
