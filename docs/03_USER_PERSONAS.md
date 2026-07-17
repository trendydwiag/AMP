# 03 — User Personas

Detailed profiles of the six primary user types who interact with Kabulhaden CMS.

---

## Persona 1: Station Manager (Budi Hartono)

> "I need one place to see everything happening at the station — who's on air, what's playing, how many listeners we have, and whether the website is up to date."

### Profile

| Attribute | Detail |
|---|---|
| **Role** | SUPERUSER |
| **Age** | 42 |
| **Tech Savviness** | Moderate — comfortable with web apps, not a developer |
| **Daily Usage** | 2-3 hours, mostly morning and afternoon |
| **Primary Device** | Desktop (office), tablet (at home) |

### Goals
- Monitor live radio status and listener counts at a glance
- Ensure broadcast schedule is accurate and programs are running on time
- Manage staff accounts and permissions (onboard new editors, deactivate departed staff)
- Review sponsor/partner status and advertising performance
- Access analytics and export reports for station management meetings

### Frustrations
- Logging into multiple systems to check different things
- Staff publishing incorrect schedule information
- Not knowing if the radio stream is down until a listener complains

### Key Workflows
1. **Morning Check**: Login → Dashboard → Radio status → Today's schedule → Check announcements
2. **Staff Management**: Login → `/akun/admin/pengguna/` → Create user → Assign role → Verify email
3. **Weekly Review**: Login → Radio analytics → Export CSV → Review broadcast sessions

### UI Preferences
- Needs the dashboard to show real-time radio status prominently
- Uses the sidebar navigation extensively
- Prefers data tables and summary cards over verbose text
- Exports data to share with non-technical stakeholders

---

## Persona 2: Content Editor (Sari Dewi)

> "I just need to upload episodes, write articles, and keep the program listings current. The simpler, the better."

### Profile

| Attribute | Detail |
|---|---|
| **Role** | EDITOR |
| **Age** | 28 |
| **Tech Savviness** | Low-moderate — knows CMS basics, prefers visual interfaces |
| **Daily Usage** | 3-4 hours, focused bursts during content creation |
| **Primary Device** | Desktop (newsroom workstation) |

### Goals
- Upload new podcast episodes with descriptions and cover art
- Write and publish news articles for the station website
- Update program descriptions and host information
- Upload media files (images, audio clips, documents) to the media library
- Schedule broadcast sessions and associate them with programs

### Frustrations
- Forgetting which programs already have episodes published
- Uploading the same image in different places because there's no centralized media library
- Not knowing if an article was published or still in draft

### Key Workflows
1. **Publish Episode**: Login → `/broadcast/episode/buat/` → Select program → Upload audio → Add description → Publish
2. **Write Article**: Login → `/broadcast/` → Or news section → Write title → Add content → Set category → Publish
3. **Upload Media**: Login → `/media/upload/` → Drag & drop files → Add tags → Assign folder
4. **Update Program**: Login → `/broadcast/program/<pk>/edit/` → Update description → Save

### UI Preferences
- Needs clear visual indicators for draft vs. published status
- Benefits from bulk upload capabilities
- Prefers form-based workflows with progress feedback
- Relies on flash messages to confirm actions succeeded

---

## Persona 3: Technical Admin (Rizky Pratama)

> "I need to configure the radio stream, manage email settings, set up 2FA for staff, and make sure the security policies are tight."

### Profile

| Attribute | Detail |
|---|---|
| **Role** | ADMINISTRATOR |
| **Age** | 35 |
| **Tech Savviness** | High — comfortable with server config, DNS, API endpoints |
| **Daily Usage** | 1-2 hours, task-driven (config changes, troubleshooting) |
| **Primary Device** | Desktop (may SSH into servers too) |

### Goals
- Configure radio streaming providers (Icecast, RadioBoss, AzuraCast URLs)
- Monitor stream health and troubleshoot connectivity issues
- Set up email SMTP configuration for system notifications
- Enforce security policies (password requirements, 2FA, session timeout, IP allowlists)
- Manage site appearance (colors, fonts, sidebar behavior)
- Configure SEO settings (meta tags, Google Analytics, custom scripts)

### Frustrations
- Needing to restart services after configuration changes
- Lack of real-time stream health visibility
- Having to explain to staff why their passwords were rejected

### Key Workflows
1. **Radio Config**: Login → `/radio/provider/buat/` → Enter stream URL → Set metadata format → Test connection
2. **Security Hardening**: Login → `/pengaturan/keamanan/` → Set password policy → Enable 2FA requirement → Configure lockout
3. **Email Setup**: Login → `/pengaturan/email/` → Enter SMTP credentials → Send test email
4. **Health Monitor**: Login → `/radio/analytics/` → Review stream health → Check listener stats → Export data

### UI Preferences
- Needs technical details (URLs, status codes, response times)
- Prefers compact data displays over decorative elements
- Uses the analytics page heavily for monitoring
- Values quick access to configuration without unnecessary navigation

---

## Persona 4: Radio DJ / On-Air Host (Maya Putri)

> "I want to see what's on air right now, what's coming up next, and quickly update my show notes if something changes."

### Profile

| Attribute | Detail |
|---|---|
| **Role** | EDITOR (limited scope) |
| **Age** | 26 |
| **Tech Savviness** | Low — primarily uses smartphone, minimal desktop use |
| **Daily Usage** | 30 minutes, before/during/after on-air shifts |
| **Primary Device** | Smartphone (60%), Desktop (40%) |

### Goals
- Quickly view the current and upcoming broadcast schedule
- Update show descriptions or episode notes for their program
- Check what was previously played (now-playing history)
- Upload a cover image or promotional material for their show

### Frustrations
- Can't easily see what's live right now without navigating multiple pages
- Typing long descriptions on a phone is tedious
- Not sure if their changes went live immediately

### Key Workflows
1. **Pre-Show Check**: Mobile → Homepage → Check today's programs → Verify their show is listed
2. **Update Show Notes**: Desktop → `/broadcast/program/<pk>/edit/` → Update description → Save
3. **During Show**: Mobile → Homepage → See now-playing widget → Verify track info is correct

### UI Preferences
- **Mobile-first** — most interactions happen on a phone
- Needs large touch targets and minimal form fields
- Benefits from the sticky radio player on the public website
- Prefers visual schedules (calendar view) over text lists

---

## Persona 5: Website Visitor / Listener (Audi)

> "I just want to listen to the live stream, check when my favorite show is on, and maybe catch up on a podcast episode I missed."

### Profile

| Attribute | Detail |
|---|---|
| **Role** | None (unauthenticated public visitor) |
| **Age** | 22 |
| **Tech Savviness** | High (digital native) but not technical |
| **Daily Usage** | 15-60 minutes, mostly during commute or work |
| **Primary Device** | Smartphone (80%), Desktop (20%) |

### Goals
- Listen to live radio with minimal friction (one-click play)
- Find the broadcast schedule for specific programs
- Browse and listen to podcast episodes on-demand
- Read latest news from the station
- Join community discussions about shows or topics

### Frustrations
- Website loads slowly on mobile data
- Can't find the play button quickly
- Schedule page doesn't clearly show what's on right now
- Podcast player doesn't remember where they left off

### Key Workflows
1. **Quick Listen**: Homepage → Hero section → Tap "DENGARKAN LIVE" → Player starts
2. **Browse Programs**: Navbar → Program dropdown → Select program → View episodes
3. **Catch Up on Podcast**: Homepage → Latest Podcasts section → Tap episode → Play
4. **Read News**: Navbar → Berita → Select article → Read
5. **Join Discussion**: Navbar → Komunitas → Select thread → Post reply

### UI Preferences
- **Speed is critical** — must load in under 3 seconds on 3G
- Needs a prominent, always-visible play button (sticky player)
- Prefers card-based layouts with large images
- Expects standard mobile patterns (hamburger menu, swipe gestures)
- Dark mode support is a plus

---

## Persona 6: New Staff Member (Andi)

> "I just started here. I need to learn the system quickly without reading a 50-page manual."

### Profile

| Attribute | Detail |
|---|---|
| **Role** | VIEWER (initially), promoted to EDITOR after onboarding |
| **Age** | 24 |
| **Tech Savviness** | Moderate — has used other CMS platforms before |
| **Daily Usage** | Varies — heavy during first week, normal after |
| **Primary Device** | Desktop (learning phase), transitions to preferred device |

### Goals
- Understand the dashboard layout and where things are
- Learn how to navigate between CMS modules
- Know which actions require which permissions
- Feel confident using the system within the first week

### Frustrations
- Overwhelmed by the number of modules and options
- Doesn't know the Indonesian UI labels yet (e.g., "Buat" = Create, "Hapus" = Delete)
- Afraid of accidentally deleting something important
- Can't find a help page or getting-started guide

### Key Workflows
1. **First Login**: Login → Explore dashboard → Click through each sidebar module → Get oriented
2. **First Content Creation**: Follow colleague's instructions → Create a test program → Save → Verify it appears in the list
3. **Permission Discovery**: Try to access a restricted page → See permission error → Understand role boundaries

### UI Preferences
- Needs clear visual hierarchy to understand page structure
- Benefits from consistent patterns across modules (list → create → edit → delete)
- Appreciates flash messages that confirm actions ("Program berhasil dibuat!")
- Would benefit from tooltips or contextual help labels

---

## Persona Summary Matrix

| Persona | Role | Device | Frequency | Primary Module | Pain Level |
|---|---|---|---|---|---|
| Budi (Manager) | SUPERUSER | Desktop/Tablet | Daily | Dashboard, Settings | Medium |
| Sari (Editor) | EDITOR | Desktop | Daily | Broadcast, Media | Low |
| Rizky (Tech Admin) | ADMINISTRATOR | Desktop | Task-based | Radio, Settings | Medium |
| Maya (DJ) | EDITOR | Mobile/Desktop | Per-shift | Homepage, Broadcast | High (mobile) |
| Audi (Listener) | Public | Mobile | Daily | Homepage, Podcast | Low (if well-designed) |
| Andi (New Staff) | VIEWER→EDITOR | Desktop | Heavy (week 1) | All modules | High (onboarding) |
