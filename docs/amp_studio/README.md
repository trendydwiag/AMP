# AMP Studio — Documentation Suite

AMP Studio is the premium administration interface for the Aradhana Media Platform (AMP Core). It provides a Notion/Spotify/YouTube Studio/Linear-inspired experience for managing Kabulhaden Online's content, broadcasts, podcasts, and media.

## Documentation Index

| File | Description |
|------|-------------|
| [README.md](README.md) | This file — overview and quick start |
| [UI_GUIDELINES.md](UI_GUIDELINES.md) | Visual design principles and patterns |
| [UX_GUIDELINES.md](UX_GUIDELINES.md) | User experience patterns and workflows |
| [NAVIGATION.md](NAVIGATION.md) | Sidebar structure and navigation logic |
| [COMPONENT_LIBRARY.md](COMPONENT_LIBRARY.md) | All reusable UI components |
| [ROLE_WORKSPACES.md](ROLE_WORKSPACES.md) | Role-based sidebar and feature access |
| [DESIGN_TOKENS.md](DESIGN_TOKENS.md) | CSS custom properties and design tokens |
| [THEME_ENGINE.md](THEME_ENGINE.md) | Theme switching (light/dark/coffee) |
| [RESPONSIVE_GUIDE.md](RESPONSIVE_GUIDE.md) | Responsive breakpoints and mobile behavior |
| [ACCESSIBILITY.md](ACCESSIBILITY.md) | Accessibility standards and ARIA patterns |
| [CHANGELOG.md](CHANGELOG.md) | Version history and updates |

## Quick Start

### Access AMP Studio
- URL: `/studio/`
- Login: `/akun/login/`
- After login, users are redirected to `/studio/` (AMP Studio Dashboard)

### Architecture
```
templates/amp_studio/
├── base.html                    # App shell (sidebar + header + player + content)
├── dashboard.html               # Main dashboard with 12 widgets
├── calendar.html                # Broadcast schedule calendar
├── media_explorer.html          # Media file browser
├── analytics.html               # Analytics dashboard
├── preview.html                 # Content preview
└── components/
    ├── sidebar.html             # Role-based sidebar navigation
    ├── header.html              # Top bar with stream status, search, notifications
    ├── player_bar.html          # Persistent audio player
    ├── command_palette.html     # Ctrl+K command palette
    └── notifications.html       # Notification panel

static/css/amp-studio/
├── amp-studio.css               # Main entry (base resets + imports)
├── design-tokens.css            # CSS custom properties
├── components.css               # Reusable component styles
└── layout.css                   # App shell, sidebar, header, grid

static/js/amp-studio/
└── amp-studio.js                # Alpine.js data + stream/player/command palette
```

### Key Features
- **Role-based navigation** — Each role sees only relevant sidebar items
- **Stream Status Widget** — Persistent header indicator for LIVE/OFFLINE status
- **Command Palette** — Ctrl+K for quick search and navigation
- **Persistent Player** — Bottom audio player for radio stream
- **Theme Engine** — Light/Dark/Coffee themes with localStorage persistence
- **Toast Notifications** — Non-intrusive feedback messages
- **Calendar View** — Day/Week/Month views for broadcast scheduling
- **Media Explorer** — Grid/List view for file management
