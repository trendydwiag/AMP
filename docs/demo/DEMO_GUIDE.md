# Kabulhaden Online — Demo Guide
**Platform:** AMP Studio (Aradhana Media Platform)  
**Demo Environment:** Kabulhaden Online  
**Prepared:** July 2024

---

## Quick Start

```bash
# Seed all demo data (idempotent — safe to run multiple times)
python manage.py demo_seed

# Reset and re-seed from scratch
python manage.py demo_seed --reset

# Then start the server
python manage.py runserver 0.0.0.0:5000
```

Navigate to `http://localhost:5000/studio/` and log in with any account below.

---

## Available Users

| Username | Password | Role | Full Name | Description |
|----------|----------|------|-----------|-------------|
| `superadmin` | `DemoAdmin2024!` | Super User | Budi Santoso | Platform founder, full system access |
| `admin` | `DemoAdmin2024!` | Administrator | Admin Kabulhaden | Station administrator, manages all content |
| `editor` | `DemoEditor2024!` | Editor/Penulis | Dewi Rahayu | Senior broadcaster & content editor |
| `viewer` | `DemoViewer2024!` | Viewer/Pembaca | Reza Firmansyah | Read-only community member |

---

## Role Descriptions

### Super User (`superadmin`)
- Full access to all platform features including system settings
- Can create and manage partner accounts
- Access to all administrative functions
- Best for: showing platform administration capabilities

### Administrator (`admin`)
- Station-level administration
- Manage users, content, schedules, streaming
- Access to analytics and system health
- Best for: showing daily operations of a radio station

### Editor (`editor`)
- Create and edit articles, programs, podcast episodes
- Manage schedules and broadcast content
- Cannot access system settings or user management
- Best for: showing the content creation workflow

### Viewer (`viewer`)
- Read-only access to published content
- Cannot create or edit content
- Best for: showing permission boundaries

---

## Demo Data Summary

| Module | Records Created |
|--------|----------------|
| Partner | 1 (Kabulhaden Online - Enterprise) |
| Users | 4 (one per role) |
| Radio Station | 1 (Kabulhaden Online) |
| Streaming Provider | 1 (AzuraCast) |
| Stream Health | 31 records (current + 30-day history) |
| Listener Statistics | 91 records (current + 90-day history) |
| Live Session | 1 active |
| Programs | 8 |
| Episodes | 40 (5 per program) |
| Schedules | 36 weekly slots |
| Broadcast Sessions | 30 (past sessions) |
| Hosts | 4 |
| Articles | 12 (all published) |
| Article Categories | 10 |
| Article Tags | ~25 |
| Podcasts | 3 |
| Podcast Episodes | 15 |
| Sponsors | 5 (platinum/gold/silver) |
| Advertisements | 5 (active) |
| Announcements | 3 |
| Audit Log Entries | 6 |
| Media Folders | 6 |

---

## Demo Scenarios

### Scenario 1: First-Time Founder Tour ⭐
**Login:** `admin` / `DemoAdmin2024!`  
**Duration:** 5–8 minutes  
**Flow:**
1. Open `/studio/` → See the welcome dashboard with time-aware greeting
2. Note the live **"Now Playing"** widget (Streaming: Dewi R live on air)
3. Click **"Streaming Center"** in sidebar → Review stream URL, status, listener count (127), bitrate (128 kbps)
4. Return to Dashboard → Show the **System Health Widget** (all green)
5. Show **Dashboard Action Cards** (will be empty since data is seeded — everything is set up)
6. Open **Setup Wizard** → Walk through the 5-step wizard to show onboarding flow

**Talking points:** "This is what a fully configured station looks like on day one of using AMP Studio."

---

### Scenario 2: Content Manager Daily Workflow
**Login:** `editor` / `DemoEditor2024!`  
**Duration:** 8–12 minutes  
**Flow:**
1. Dashboard → Show today's schedule (programs visible for current day)
2. Navigate to **Berita** → Show 12 published articles with categories and tags
3. Click any article → Show the article detail and edit view
4. Navigate to **Siaran** → Show 8 programs with episode lists
5. Click "Pagi Bersama Kabulhaden" → Show episode list (5 episodes)
6. Navigate to **Podcast** → Show 3 podcasts (Bisnis Lokal, Tokoh Inspiratif, Catatan Harian)
7. Show the weekly schedule grid with 36 time slots filled

**Talking points:** "Editors have everything they need without the complexity of system settings."

---

### Scenario 3: Streaming & Analytics Deep Dive
**Login:** `superadmin` / `DemoAdmin2024!`  
**Duration:** 6–10 minutes  
**Flow:**
1. Dashboard → Review the **Radio Health Widget** (Streaming ✅, Database ✅, Storage ✅)
2. Click **"Streaming Center"** → Show live status banner (ON AIR)
3. Show stream URL: `https://stream.kabulhaden.online:8000/radio.mp3`
4. Copy stream URL → demonstrate one-click copy
5. Show **health history table** (30 days, mostly HEALTHY)
6. Show **"Now Playing"** widget with current song
7. Show current listeners (127), peak (312), response time (42ms)
8. Navigate to **Pengaturan > Streaming** → Show provider configuration

**Talking points:** "Real-time monitoring so the station owner always knows what's happening."

---

### Scenario 4: Sponsor & Monetization View
**Login:** `admin` / `DemoAdmin2024!`  
**Duration:** 4–6 minutes  
**Flow:**
1. Navigate to `/admin/sponsor/` → Show 5 active sponsors
2. Point out sponsor tiers: BKR Kabulhaden (Platinum), Maju Jaya & RS Sehat Sejahtera (Gold)
3. Show 5 active advertisements with impression/click data
4. Show total impressions: >55,000 across all ads
5. Highlight the partnership with Dinas Pariwisata (government partnership)

**Talking points:** "Sponsors see real ROI data. The platform is already generating revenue."

---

### Scenario 5: Permission Demo (Role Comparison)
**Duration:** 5 minutes  
**Flow:**
1. Login as `editor` → Show available menu items (no Settings, no User Management)
2. Logout → Login as `viewer` → Show even more restricted access
3. Logout → Login as `admin` → Show full menu
4. Compare the three views side by side

**Talking points:** "Each team member sees exactly what they need — nothing more, nothing less."

---

### Scenario 6: Mobile/Responsive Demo
**Duration:** 3 minutes  
**Flow:**
1. Open DevTools → Switch to mobile view (375px)
2. Navigate through: Dashboard → Streaming Center → Schedule → Article list
3. Show that all layouts adapt properly
4. Demonstrate the floating Help Button on mobile

---

## Suggested Presentation Flow (30-Minute Demo)

| Time | Activity |
|------|----------|
| 00:00–02:00 | Introduction: "This is Kabulhaden Online, a real-world AMP Studio deployment" |
| 02:00–08:00 | Scenario 1: First-Time Founder Tour (Dashboard + Streaming Center + Health Widget) |
| 08:00–16:00 | Scenario 2: Content Manager Workflow (Articles + Programs + Podcasts + Schedule) |
| 16:00–22:00 | Scenario 3: Streaming & Analytics Deep Dive |
| 22:00–26:00 | Scenario 4: Sponsors & Monetization |
| 26:00–28:00 | Scenario 5: Quick Permission Role Comparison |
| 28:00–30:00 | Q&A + Setup Wizard walkthrough if time permits |

---

## Demo Reset

If the demo data gets modified during a presentation, reset it cleanly:

```bash
python manage.py demo_seed --reset
```

This will:
1. Delete all seeded content (articles, programs, podcasts, etc.)
2. Re-create everything from scratch with fresh timestamps
3. Preserve the `admin` user account if it already exists

> **Note:** The `--reset` flag does NOT delete users. To also reset users, add the `viewer` and `editor` accounts to the deletion list in the command.

---

## Kabulhaden Online — Organization Context

| Detail | Value |
|--------|-------|
| Station Name | Kabulhaden Online |
| Company | PT Kabulhaden Media Digital |
| Founded | 2012 |
| Tagline | "Suara Kabulhaden, Hati Nusantara" |
| Primary Color | Coffee (#8B5E3C) |
| Stream URL | https://stream.kabulhaden.online:8000/radio.mp3 |
| Listeners (Monthly) | 50,000+ |
| Current Listeners | 127 (live demo) |
| Active Programs | 8 |
| Sponsor Partners | 5 |

---

## Known Demo Limitations

1. **Stream URL is fictitious** — `stream.kabulhaden.online` does not resolve. The "Test Stream" button in the Streaming Center will not play audio. This is expected for a demo environment.

2. **No media files** — Article images, program thumbnails, and podcast covers show broken images since no actual media files are uploaded. The folders structure is created.

3. **Alpine.js interactive features** — The guided tour and help button dropdown require Alpine.js to be unblocked (Task #3). Static layout renders correctly.

4. **Timestamps are relative** — All dates are generated relative to the time `demo_seed` was last run.
