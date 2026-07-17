# 06 — User Flows

Key user journeys through Kabulhaden CMS, mapping each step from entry to completion.

---

## Flow 1: Login → Dashboard

The primary entry point for all authenticated staff members.

```
START: User visits /akun/masuk/
  │
  ├─ Step 1: View login form (template: users/login.html)
  │   └── Fields: username, password
  │
  ├─ Step 2: Submit credentials
  │   ├─ SUCCESS ──► Redirect to LOGIN_REDIRECT_URL (/)
  │   │   ├─ Check force_password_change flag
  │   │   │   ├─ TRUE ──► Redirect to /akun/ganti-password/
  │   │   │   └─ FALSE ──► Continue to dashboard
  │   │   ├─ Check 2FA enabled
  │   │   │   ├─ TRUE ──► Redirect to /akun/2fa/verifikasi/
  │   │   │   └─ FALSE ──► Continue to dashboard
  │   │   └─ Session created, audit log recorded
  │   │
  │   └─ FAILURE ──► Show error message
  │       ├─ Check if account locked (axes)
  │       │   └─ TRUE ──► Show "Akun dikunci" message
  │       └─ Increment failed_login_attempts
  │           └─ If >= 5 ──► Lock account for 15 minutes
  │
  └─ Step 3: Dashboard loads (template: dashboard_base.html)
      ├─ Sidebar shows role-appropriate navigation
      ├─ Flash messages displayed if any
      └─ User menu shows name, profile link, logout
```

### RBAC-Based Dashboard Navigation

```
After login, sidebar adapts to role:
│
├─ ALL ROLES: Dashboard link, Radio Engine, Broadcast Management
│
├─ STAFF+ (is_staff=True): Also shows:
│   ├─ "Kelola Pengguna" → /akun/admin/pengguna/
│   └─ "Django Admin" → /admin/
│
└─ VIEWER: Read-only access to all visible modules
```

---

## Flow 2: Upload Media

Content editors uploading files to the media library.

```
START: User navigates to /media/upload/
  │
  ├─ Step 1: View upload form (template: media_manager/upload.html)
  │   └── Fields: file(s), title, alt text, caption, folder, tags
  │
  ├─ Step 2: Select or drag-and-drop files
  │   └── Client-side validation:
  │       ├─ File size check (against max_upload_size_mb)
  │       ├─ File type check (against allowed_upload_types)
  │       └─ Preview thumbnails for images
  │
  ├─ Step 3: Fill metadata
  │   ├─ Title (required)
  │   ├─ Alt text (for accessibility)
  │   ├─ Caption (optional description)
  │   ├─ Folder (select from existing or "No Folder")
  │   └─ Tags (multi-select from existing tags)
  │
  ├─ Step 4: Submit form
  │   ├─ SUCCESS ──►
  │   │   ├─ File saved with UUID filename (utils/storage.py)
  │   │   ├─ File type auto-detected (IMAGE/VIDEO/DOCUMENT/AUDIO/OTHER)
  │   │   ├─ File size recorded
  │   │   ├─ Dimensions recorded (for images)
  │   │   ├─ Thumbnail generated (if auto_generate_thumbnails enabled)
  │   │   ├─ Flash message: "File berhasil diunggah!"
  │   │   └─ Redirect to /media/file/<uuid>/
  │   │
  │   └─ FAILURE ──►
  │       ├─ Show validation errors
  │       └─ Preserve form inputs for retry
  │
  └─ Step 5: File appears in media list (/media/file/)
      └── Available for use in other CMS modules
```

---

## Flow 3: Configure Radio Station

Technical admins setting up radio streaming providers.

```
START: User navigates to /radio/provider/buat/
  │
  ├─ Step 1: View provider form (template: radio/provider_form.html)
  │   └── Fields: name, type, stream URL, API URL, metadata format, credentials
  │
  ├─ Step 2: Select provider type
  │   ├─ Icecast
  │   ├─ Shoutcast
  │   ├─ RadioBoss Advance
  │   └─ AzuraCast
  │
  ├─ Step 3: Configure endpoints
  │   ├─ Stream URL (required) ── e.g., http://stream.example.com:8000/radio
  │   ├─ API URL (optional) ── for status/metadata retrieval
  │   ├─ Backup Stream URL (optional) ── failover stream
  │   ├─ Metadata URL (optional) ── now-playing data endpoint
  │   ├─ Listener URL (optional) ── listener count endpoint
  │   ├─ Healthcheck URL (optional) ── health monitoring endpoint
  │   └─ Metadata format: JSON / XML / ICY / HTTP
  │
  ├─ Step 4: Enter credentials (if authenticated stream)
  │   ├─ Username
  │   └─ Password (stored masked, shown as ******** in UI)
  │
  ├─ Step 5: Set timeout and active status
  │   ├─ Timeout: default 10 seconds
  │   └─ Active: toggle on/off
  │
  ├─ Step 6: Save
  │   ├─ SUCCESS ──►
  │   │   ├─ Provider saved and linked to station
  │   │   ├─ Now Playing cache begins updating
  │   │   ├─ Health checks start running
  │   │   └─ Flash message: "Provider berhasil disimpan!"
  │   │
  │   └─ FAILURE ──► Show validation errors
  │
  └─ Step 7: Verify at /radio/analytics/
      ├─ Stream status: ONLINE / OFFLINE / AUTO_DJ / LIVE_DJ
      ├─ Now playing: artist - track
      ├─ Listener count: current / peak
      └─ Health: response time, bitrate, format
```

---

## Flow 4: Create Broadcast Program + Schedule

Content editors setting up a new program with its broadcast schedule.

```
START: User navigates to /broadcast/program/buat/
  │
  ├─ Step 1: Create Program (template: broadcast/program_form.html)
  │   ├─ Title (required)
  │   ├─ Short description
  │   ├─ Full description
  │   ├─ Thumbnail image
  │   ├─ Banner image
  │   ├─ Category (free text)
  │   ├─ Language (default: "id")
  │   ├─ Genre
  │   ├─ Target audience
  │   ├─ Content rating: G / PG / T / M
  │   ├─ Featured flag
  │   ├─ SEO title & description
  │   └─ Save → Program created with auto-generated slug
  │
  ├─ Step 2: Assign Hosts → /broadcast/host/buat/
  │   ├─ Full name
  │   ├─ Stage name (display name)
  │   ├─ Nickname
  │   ├─ Biography
  │   ├─ Avatar image
  │   ├─ Contact: email, phone
  │   ├─ Social: Instagram, YouTube, Spotify, Facebook
  │   └─ Link to Program via HostMember (is_lead flag)
  │
  ├─ Step 3: Create Schedule → /broadcast/jadwal/buat/
  │   ├─ Program (select from list)
  │   ├─ Day of week: MON–SUN
  │   ├─ Start time (e.g., 08:00)
  │   ├─ End time (e.g., 10:00)
  │   ├─ Timezone (default: Asia/Jakarta)
  │   ├─ Repeat weekly (default: true)
  │   └─ Active (default: true)
  │
  ├─ Step 4: (Optional) Create Broadcast Session → /broadcast/sesi/buat/
  │   ├─ Program (select)
  │   ├─ Schedule (select, optional)
  │   ├─ Start datetime
  │   ├─ End datetime
  │   └─ Status: SCHEDULED / LIVE / FINISHED / CANCELLED / DELAYED
  │
  └─ Step 5: Verify on Calendar → /broadcast/kalender/
      └── Program appears in weekly calendar grid
```

---

## Flow 5: Visit Website & Listen to Live Radio

The primary journey for public website visitors (listeners).

```
START: User visits /
  │
  ├─ Step 1: Homepage loads (template: website/home.html)
  │   ├─ Announcement bar (if active) ── dismissible with AlpineJS
  │   ├─ Hero section with live radio player
  │   │   ├─ Now playing: artist - track (from /radio/api/now-playing/)
  │   │   ├─ Stream status: live indicator (pulsing dot)
  │   │   ├─ Play/Pause button
  │   │   ├─ Volume control
  │   │   └─ Listener count
  │   ├─ Today's Programs section
  │   ├─ Weekly Schedule section
  │   ├─ About section
  │   ├─ Latest Podcasts section
  │   ├─ Latest News section
  │   ├─ Community section
  │   ├─ Sponsors section
  │   └─ Newsletter CTA section
  │
  ├─ Step 2: User clicks "DENGARKAN LIVE"
  │   ├─ Sticky player activates at bottom of page
  │   ├─ Audio stream begins playing
  │   ├─ Player shows: now playing info, play/pause, volume
  │   └─ Player persists across page navigation
  │
  ├─ Step 3: (Optional) Explore content
  │   ├─ Navbar → Program dropdown → Program list or Podcast list
  │   ├─ Navbar → Jadwal → Weekly schedule page
  │   ├─ Navbar → Berita → News articles
  │   ├─ Navbar → Komunitas → Community discussions
  │   ├─ Search (⌘K) → Modal search across all content
  │   └─ Mobile: Hamburger menu → Full navigation
  │
  ├─ Step 4: (Optional) Mobile fullscreen player
  │   └─ Tap player bar → Full screen overlay
  │       ├─ Album artwork (large)
  │       ├─ Track info
  │       ├─ Play/Pause (large button)
  │       ├─ Volume/Mute
  │       ├─ Copy stream link
  │       └─ Close button
  │
  └─ Step 5: (Optional) Subscribe to newsletter
      └─ Enter email in newsletter form → POST /newsletter/subscribe/
          └─ JSON response: success/failure message
```

---

## Flow 6: Register Account

New staff members creating their accounts.

```
START: User visits /akun/daftar/
  │
  ├─ Step 1: View registration form (template: users/register.html)
  │   └── Fields: username, email, first name, last name, password, confirm password
  │
  ├─ Step 2: Fill form and submit
  │   ├─ Client-side validation (required fields, password match)
  │   └─ Server-side validation:
  │       ├─ Username uniqueness
  │       ├─ Email uniqueness
  │       ├─ Password policy (12+ chars, uppercase, lowercase, number, special)
  │       └─ Password similarity check
  │
  ├─ Step 3: Account created
  │   ├─ Role defaults to VIEWER
  │   ├─ is_active = True
  │   ├─ email_verified = False
  │   ├─ Email verification token generated (48h expiry)
  │   └─ Audit log: USER_CREATE recorded
  │
  ├─ Step 4: Redirect to email verification notice
  │   └─ /akun/verifikasi-email/ ── "Silakan cek email Anda"
  │
  ├─ Step 5: User clicks verification link in email
  │   └─ /akun/verifikasi-email/<token>/
  │       ├─ Token valid & not expired ──► email_verified = True
  │       ├─ Flash: "Email berhasil diverifikasi!"
  │       └─ Redirect to /akun/masuk/
  │
  └─ Step 6: User logs in with new credentials
      └─ Normal login flow (Flow 1)
```

---

## Flow 7: Password Reset

Users recovering access to their accounts.

```
START: User clicks "Lupa Password?" on login page
  │
  ├─ Step 1: View forgot password form (template: users/forgot_password.html)
  │   └── Field: email address
  │
  ├─ Step 2: Submit email
  │   ├─ Email exists in system ──►
  │   │   ├─ Password reset token generated (48h expiry)
  │   │   ├─ Email sent with reset link
  │   │   └─ Flash: "Email reset password telah dikirim"
  │   │
  │   └─ Email not found ──►
  │       └─ Same flash message (prevents email enumeration)
  │
  ├─ Step 3: User clicks link in email
  │   └─ Password reset form displayed
  │       ├─ New password field
  │       ├─ Confirm password field
  │       └─ Password policy hints displayed
  │
  ├─ Step 4: Submit new password
  │   ├─ Token valid & not expired ──►
  │   │   ├─ Password updated
  │   │   ├─ Password history entry created
  │   │   ├─ All existing sessions invalidated
  │   │   ├─ Audit log: PASSWORD_RESET recorded
  │   │   └─ Redirect to /akun/masuk/
  │   │
  │   └─ Token expired ──►
  │       └─ Error: "Token sudah kedaluwarsa. Silakan minta link baru."
  │
  └─ Step 5: User logs in with new password
      └─ Normal login flow (Flow 1)
```

---

## Flow Summary Diagram

```
                        ┌─────────────────────┐
                        │   Kabulhaden CMS     │
                        └──────────┬──────────┘
                                   │
            ┌──────────────────────┼──────────────────────┐
            │                      │                      │
     ┌──────▼──────┐      ┌──────▼──────┐      ┌──────▼──────┐
     │   Public     │      │   Staff     │      │   Admin     │
     │   Website    │      │   Login     │      │   Panel     │
     └──────┬──────┘      └──────┬──────┘      └──────┬──────┘
            │                      │                      │
     ┌──────▼──────┐      ┌──────▼──────┐      ┌──────▼──────┐
     │ • Homepage   │      │ • Dashboard │      │ • Django    │
     │ • Programs   │      │ • Radio     │      │   Admin     │
     │ • Podcast    │      │ • Broadcast │      │ • Raw data  │
     │ • News       │      │ • Media     │      │   access    │
     │ • Community  │      │ • Settings  │      └─────────────┘
     │ • Live Radio │      │ • Users     │
     │ • Search     │      └─────────────┘
     └─────────────┘
```
