# AMP Studio — Changelog

## [1.0.0] — 2025-07-15

### Added
#### Foundation
- **AMP Studio base template** (`templates/amp_studio/base.html`) — App shell with sidebar, header, player bar, command palette, notifications, toast container
- **Sidebar component** (`templates/amp_studio/components/sidebar.html`) — Role-based collapsible navigation with 11 top-level sections
- **Header component** (`templates/amp_studio/components/header.html`) — Stream status widget, search trigger (⌘K), notifications, theme toggle, user menu
- **Player bar component** (`templates/amp_studio/components/player_bar.html`) — Persistent audio player with play/pause, volume, reconnect, stream info
- **Command palette** (`templates/amp_studio/components/command_palette.html`) — ⌘K search interface with quick actions and keyboard hints
- **Notification panel** (`templates/amp_studio/components/notifications.html`) — Slide-in notification panel with typed alerts

#### Design System
- **Design tokens** (`static/css/amp-studio/design-tokens.css`) — Complete CSS custom property system for colors, spacing, typography, radius, shadows, transitions, z-index, layout
- **Component library** (`static/css/amp-studio/components.css`) — 20+ reusable components (buttons, cards, badges, inputs, metrics, empty states, skeletons, avatars, dropdowns, toasts, modals, drawers, tabs, tooltips, progress bars)
- **Layout system** (`static/css/amp-studio/layout.css`) — App shell, sidebar, header, player bar, content area, grid system, responsive breakpoints
- **Main entry stylesheet** (`static/css/amp-studio/amp-studio.css`) — Base resets, imports, scrollbar styling, utilities

#### JavaScript
- **AMP Studio JS** (`static/js/amp-studio/amp-studio.js`) — Alpine.js data definitions:
  - `ampStudio()` — Sidebar, theme, command palette, notifications management
  - `streamStatus()` — Polls radio status API every 15s for LIVE/OFFLINE indicator
  - `ampPlayer()` — Audio stream control with volume persistence
  - `ampToast()` — Toast notification utility

#### Pages
- **Dashboard** (`templates/amp_studio/dashboard.html`) — Full dashboard with 12 widgets: Live Broadcast, Today's Schedule, Articles, Podcasts, Programs, Pending Reviews, Quick Actions, Notifications, Storage, Activity, Popular Programs, Sponsor Summary
- **Calendar** (`templates/amp_studio/calendar.html`) — Broadcast schedule calendar with Day/Week/Month views
- **Media Explorer** (`templates/amp_studio/media_explorer.html`) — File browser with Grid/List views and type filtering
- **Analytics** (`templates/amp_studio/analytics.html`) — Analytics dashboard placeholder with metric cards
- **Preview** (`templates/amp_studio/preview.html`) — Content preview page

#### Backend
- **Studio app** (`apps/studio/`) — New Django app with:
  - `AMPStudioDashboardView` — Dashboard with stats, schedule, articles, reviews, activity, storage, programs
  - `AMPStudioCalendarView` — Calendar page
  - `AMPStudioMediaExplorerView` — Media explorer
  - `AMPStudioAnalyticsView` — Analytics
  - `AMPStudioPreviewView` — Content preview
- **URL routes** — `/studio/`, `/studio/kalender/`, `/studio/media/`, `/studio/analytics/`, `/studio/preview/<type>/<pk>/`
- **Login redirect** — Updated `LOGIN_REDIRECT_URL` to `/studio/`

#### Documentation
- Complete documentation suite in `docs/amp_studio/` (11 files):
  - README, UI Guidelines, UX Guidelines, Navigation, Component Library, Role Workspaces, Design Tokens, Theme Engine, Responsive Guide, Accessibility, Changelog

### Changed
- Sidebar "Beranda" link now points to `/studio/` (AMP Studio Dashboard)
- `LOGIN_REDIRECT_URL` updated from `/` to `/studio/`
- `INSTALLED_APPS` includes `apps.studio.apps.StudioConfig`

### Fixed
- Fixed template syntax error in dashboard (`stats.episodes_scheduled` bracket)
