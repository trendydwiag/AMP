# 40. Project Glossary

## Overview

This glossary defines all technical terms, roles, modules, and domain-specific vocabulary used throughout the Kabulhaden CMS project documentation and codebase.

---

## A

| Term | Definition |
|------|------------|
| **Admin** | Short for Administrator role; user with CMS management privileges |
| **API** | Application Programming Interface; allows programmatic access to CMS data |
| **Axes** | Django package for brute-force login protection; tracks failed attempts |
| **Audit Log** | System record of user actions for security and compliance tracking |

---

## B

| Term | Definition |
|------|------------|
| **Broadcast** | Module managing live audio streams, encoders, playlists, and recordings |
| **Broadcast Dashboard** | Main view for monitoring and controlling live broadcasts |

---

## C

| Term | Definition |
|------|------------|
| **Cache** | Temporary storage for frequently accessed data to improve performance |
| **CICD** | Continuous Integration/Continuous Deployment; automated testing and deployment pipeline |
| **Community** | Module for community posts, events, and interactive content |
| **CSRF** | Cross-Site Request Forgery; security protection for form submissions |
| **CRUD** | Create, Read, Update, Delete; basic database operations |
| **CustomUser** | Extended Django user model with additional fields (role, avatar, etc.) |

---

## D

| Term | Definition |
|------|------------|
| **Decorator** | Python function that adds behavior to views (e.g., `@login_required`) |
| **Docker** | Containerization platform for consistent development and deployment |
| **Docker Compose** | Tool for defining multi-container Docker applications |
| **DRF** | Django REST Framework; toolkit for building Web APIs |

---

## E

| Term | Definition |
|------|------------|
| **Encoder** | Software/hardware that converts audio to streaming format (e.g., Icecast) |
| **Episode** | A single program recording; part of a Program |
| **Endpoint** | Specific URL where an API resource can be accessed |
| **Episode** | Single broadcast content unit within a Program |

---

## F

| Term | Definition |
|------|------------|
| **FIFO** | First In, First Out; queue order for play queue management |

---

## G

| Term | Definition |
|------|------------|
| **Gunicorn** | Python WSGI HTTP server for serving Django in production |

---

## H

| Term | Definition |
|------|------------|
| **HSTS** | HTTP Strict Transport Security; forces HTTPS connections |
| **Health Check** | Automated test to verify service availability |

---

## I

| Term | Definition |
|------|------------|
| **Icecast** | Open-source streaming media server for audio broadcasting |
| **Inactivity Timeout** | Auto-logout after period of no user activity (30 min default) |

---

## J

| Term | Definition |
|------|------------|
| **Jadwal** | Indonesian word for "Schedule"; Radio module for program scheduling |
| **JSON** | JavaScript Object Notation; data format for APIs |

---

## K

| Term | Definition |
|------|------------|
| **Kabulhaden** | The project name; a community radio station CMS |

---

## L

| Term | Definition |
|------|------------|
| **Listener** | Person connected to a radio stream |
| **Login Required** | Decorator ensuring user is authenticated before accessing view |

---

## M

| Term | Definition |
|------|------------|
| **Middleware** | Django component that processes requests/responses globally |
| **Media** | Uploaded files (audio, images, documents) managed by the CMS |
| **Media Manager** | Module for organizing, uploading, and managing media files |
| **Migration** | Django's system for evolving database schema |
| **Mount Point** | URL path where a stream is accessible (e.g., `/live`) |

---

## N

| Term | Definition |
|------|------------|
| **Nginx** | Web server/reverse proxy used in production |
| **Now Playing** | Currently airing program or track on a station |

---

## O

| Term | Definition |
|------|------------|
| **Orphaned Media** | Media files in storage without corresponding database records |

---

## P

| Term | Definition |
|------|------------|
| **Play Queue** | Ordered list of tracks/episodes to be played on a station |
| **Playlist** | Curated collection of episodes for scheduled playback |
| **Podcast** | Module for on-demand audio content |
| **Program** | Recurring radio show with scheduled time slots |
| **PWA** | Progressive Web App; web app with offline and install capabilities |
| **PyVAPID** | Python implementation of VAPID for web push notifications |

---

## Q

| Term | Definition |
|------|------------|
| **Queue** | See Play Queue; ordered list of tracks to play |

---

## R

| Term | Definition |
|------|------------|
| **RBAC** | Role-Based Access Control; permission system based on user roles |
| **Radio** | Module managing stations, programs, schedules, and episodes |
| **Recording** | Archived copy of a live broadcast stream |
| **Repository** | Data access layer providing CRUD operations (e.g., `BaseRepository`) |

---

## S

| Term | Definition |
|------|------------|
| **Schedule** | Time-based assignment of Programs to Stations with day/time |
| **Service** | Business logic layer handling operations (e.g., `BaseService`) |
| **Session Timeout** | Automatic logout after inactivity period |
| **Slug** | URL-friendly version of a name/title (e.g., `berita-hari-ini`) |
| **Singleton** | Pattern ensuring only one instance exists (used in Settings models) |
| **SMTP** | Simple Mail Transfer Protocol; email sending protocol |
| **Stream** | Live audio broadcast output from an Encoder |

---

## T

| Term | Definition |
|------|------------|
| **TimeStampMixin** | Django mixin adding `created_at` and `updated_at` fields |
| **Toast** | Small notification popup that appears briefly on screen |

---

## U

| Term | Definition |
|------|------------|
| **UUID** | Universally Unique Identifier; used as primary keys in all models |

---

## V

| Term | Definition |
|------|------------|
| **VAPID** | Voluntary Application Server Identification; for web push authentication |
| **View** | Django component handling HTTP requests and returning responses |
| **Viewer** | Read-only user role; can view content but not edit |

---

## W

| Term | Definition |
|------|------------|
| **WhiteNoise** | Django middleware for serving static files in production |
| **WSGI** | Web Server Gateway Interface; Python web app server standard |

---

## Roles

| Role | Description | Key Permissions |
|------|-------------|-----------------|
| **SUPERUSER** | Full system access | Everything; can manage admins |
| **ADMINISTRATOR** | CMS management | Users, settings, all content, broadcast |
| **EDITOR** | Content creation | Create/edit own content, upload media |
| **VIEWER** | Read-only | View published content only |

---

## Modules

| Module | URL Prefix | Purpose |
|--------|------------|---------|
| **users** | `/akun/` | Authentication, profiles, user management |
| **settings** | `/pengaturan/` | Site configuration (singleton models) |
| **media_manager** | `/media/` | File uploads, folders, thumbnails |
| **radio** | `/radio/` | Stations, programs, schedules, episodes |
| **broadcast** | `/broadcast/` | Encoders, streams, playlists, recordings |
| **news** | `/berita/` | News articles (website) |
| **podcast** | `/podcast/` | Podcast episodes (website) |
| **community** | `/komunitas/` | Community posts (website) |
| **sponsor** | `/sponsor/` | Sponsor profiles (website) |
| **website** | `/` | Homepage, about, contact |

---

## Indonesian Terms

| Indonesian | English | Usage |
|------------|---------|-------|
| **Masuk** | Login | Login page/button |
| **Keluar** | Logout | Logout button |
| **Profil** | Profile | User profile section |
| **Pengaturan** | Settings | Settings module |
| **Pengguna** | Users | User management |
| **Media** | Media | Media manager |
| **Stasiun** | Station | Radio station |
| **Program** | Program | Radio program |
| **Jadwal** | Schedule | Program schedule |
| **Episode** | Episode | Program episode |
| **Antrian** | Queue | Play queue |
| **Berita** | News | News articles |
| **Komunitas** | Community | Community section |
| **Sponsor** | Sponsor | Sponsor profiles |
| **Simpan** | Save | Form save button |
| **Hapus** | Delete | Delete action |
| **Edit** | Edit | Edit action |
| **Tambah** | Add/Create | Create new item |
| **Kembali** | Back | Navigation back |
| **Cari** | Search | Search functionality |
| **Filter** | Filter | Filter/search options |
| **Status** | Status | Current state |
| **Aktif** | Active | Active status |
| **Tidak Aktif** | Inactive | Inactive status |
| **Semua** | All | Show all items |

---

## Related Documentation

- `README.md` - Project overview
- `erd.md` - Entity relationship diagrams
- `url_list.md` - URL patterns
- `permission_matrix.md` - Access control matrix

---

*Last updated: 2026-07-15*
