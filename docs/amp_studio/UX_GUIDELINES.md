# AMP Studio — UX Guidelines

## Interaction Patterns

### Click Targets
- Minimum 44×44px for touch targets
- 32×32px minimum for icon buttons
- Adequate spacing between clickable elements (8px minimum)

### Feedback
- **Hover**: Background color change (`--amp-surface-tertiary`)
- **Active/Focus**: Subtle ring or border color change
- **Loading**: Skeleton placeholders for content areas
- **Success**: Toast notification (bottom-right, auto-dismiss 4s)
- **Error**: Toast notification + inline validation
- **Destructive**: Confirmation dialog required

### Navigation
- Sidebar sections collapse/expand independently
- Active item highlighted with coffee-50 background
- Breadcrumb trail for nested pages
- Back button on all detail pages

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `⌘K` / `Ctrl+K` | Open Command Palette |
| `ESC` | Close any overlay |
| `⌘N` / `Ctrl+N` | New content (context-aware) |
| `⌘S` / `Ctrl+S` | Save current form |
| `↑↓` | Navigate command palette results |
| `↵` | Execute selected command |

## Command Palette
The command palette (`⌘K`) is the power-user interface:
1. Opens with keyboard shortcut or search button
2. Search across all content, settings, and actions
3. Quick actions for common tasks (new article, new episode, etc.)
4. Results grouped by category
5. Keyboard navigation with arrow keys
6. `↵` to execute, `ESC` to close

## Stream Status
- Persistent header widget shows LIVE/OFFLINE status
- Polls `/radio/api/status/` every 15 seconds
- Shows listener count and current program
- Red pulse animation when LIVE

## Player Bar
- Persistent bottom bar (fixed position)
- Always visible when AMP Studio is open
- Play/Pause, Volume, Reconnect controls
- Shows current song/program info
- Bitrate and listener count display

## Notifications
- Bell icon with unread count badge
- Panel slides in from right
- Grouped by type (approval, publication, system)
- "Mark all as read" action
- Each notification links to relevant content

## Form Patterns
- **Create**: Full-page form with back button
- **Edit**: Full-page form pre-populated with data
- **Delete**: Confirmation dialog with red "Hapus" button
- **Workflow**: Inline action buttons (Submit, Approve, Publish)
- **Autosave**: Draft auto-save every 30 seconds (if implemented)

## Calendar Interactions
- **Day View**: Hour-by-hour timeline
- **Week View**: 7-column grid with events
- **Month View**: Compact grid with event dots
- **Navigation**: Arrow buttons for prev/next period
- **Events**: Click to view/edit details

## Loading States
- Skeleton cards for dashboard widgets
- Skeleton rows for table/list views
- Spinner for individual action buttons
- Progress bar for file uploads

## Error Handling
- 404: Custom page with back link
- 403: Custom page with contact info
- 500: Custom page with auto-report
- Network errors: Toast with retry option
