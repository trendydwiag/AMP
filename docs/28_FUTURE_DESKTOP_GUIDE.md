# 28. Desktop Development Guide (Future)

## Overview

This guide covers considerations for a potential future desktop application version of Kabulhaden CMS. Currently, the project is web-based using Django. Desktop support would extend the platform to editors who prefer native desktop applications.

---

## Current State

| Aspect | Status |
|--------|--------|
| Web CMS | Production-ready |
| Mobile PWA | Planned (see `27_FUTURE_MOBILE_GUIDE.md`) |
| Desktop App | Future consideration |

---

## Recommended Desktop Framework

### Electron (Cross-Platform)

- **Pros**: Large ecosystem, Web Technologies, auto-updater support
- **Cons**: Large binary size, memory usage
- **Best for**: Windows/macOS/Linux support with existing team skills

### Tauri (Lightweight)

- **Pros**: Small binary size, Rust backend performance, lower memory usage
- **Cons**: Newer ecosystem, Rust learning curve
- **Best for**: Performance-critical desktop experience

### Desktop (Python - PyInstaller/cx_Freeze)

- **Pros**: No new language needed, direct Django integration
- **Cons**: Poor UX widgets, limited OS integration
- **Best for**: Internal admin tools only

---

## Proposed Architecture

```
┌─────────────────────────────────────────┐
│           Desktop Shell                  │
│    ┌───────────────────────────────┐     │
│    │    WebView / Browser Engine    │     │
│    │  ┌───────────────────────┐    │     │
│    │  │   Django CMS (Web)    │    │     │
│    │  │   (localhost:8000)    │    │     │
│    │  └───────────────────────┘    │     │
│    └───────────────────────────────┘     │
│    ┌───────────────────────────────┐     │
│    │    Native OS Features         │     │
│    │    - File System Access       │     │
│    │    - System Notifications     │     │
│    │    - Auto-Update              │     │
│    │    - Tray Icon                │     │
│    └───────────────────────────────┘     │
└─────────────────────────────────────────┘
```

---

## Key Desktop-Specific Features

### 1. Offline Editing

```python
# Hypothetical offline sync service
class DesktopSyncService:
    def sync_content(self, content_id):
        """Sync content between local DB and server."""
        local = self.local_db.get(content_id)
        remote = self.api.fetch(content_id)
        
        if local.updated_at > remote.updated_at:
            self.api.push(local)
        else:
            self.local_db.update(remote)
    
    def offline_queue(self):
        """Queue changes made while offline."""
        pass
```

### 2. File System Integration

- Import media directly from desktop folders
- Drag-and-drop file uploads
- Export content to local files (Markdown, HTML, PDF)

### 3. Native OS Notifications

- Stream status alerts (encoder issues, disconnects)
- New comment/review notifications
- Scheduled publish reminders

### 4. System Tray

- Quick access to stream controls
- Now-playing display
- Minimal footprint mode

---

## Authentication Considerations

| Scenario | Strategy |
|----------|----------|
| Desktop → Local Django | Local auth (SQLite or PostgreSQL) |
| Desktop → Remote API | OAuth2 / JWT tokens |
| Offline Mode | Cached credentials + sync queue |

### Token Management

```python
# Hypothetical token store
class DesktopTokenStore:
    def store_token(self, token):
        """Store encrypted token in OS keychain."""
        keyring.set_password("kabulhaden", "api_token", token)
    
    def get_token(self):
        """Retrieve token from OS keychain."""
        return keyring.get_password("kabulhaden", "api_token")
```

---

## Database Strategy

| Mode | Database | Use Case |
|------|----------|----------|
| Online | PostgreSQL (remote) | Full CMS functionality |
| Offline | SQLite (local) | Read-only cache, queued edits |
| Hybrid | Both | Sync when online, local when offline |

---

## Auto-Update System

```
┌─────────────────┐
│  Update Check    │──→ GitHub Releases / Update Server
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Download Update │──→ Verify signature
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Apply Update    │──→ Restart application
└─────────────────┘
```

---

## Performance Targets

| Metric | Target |
|--------|--------|
| Cold start | < 3 seconds |
| Memory usage | < 200 MB idle |
| Binary size | < 150 MB (Tauri) / < 200 MB (Electron) |
| Auto-update download | < 30 seconds on broadband |

---

## Development Roadmap (Hypothetical)

| Phase | Milestone |
|-------|-----------|
| 1 | Desktop shell with WebView pointing to web CMS |
| 2 | OS integration (notifications, tray, file dialogs) |
| 3 | Offline mode with local SQLite cache |
| 4 | Auto-update system |
| 5 | Native media editor integration |

---

## Related Documentation

- `27_FUTURE_MOBILE_GUIDE.md` - Mobile PWA considerations
- `04_FEATURE_BACKLOG.md` - Feature prioritization
- `12_DASHBOARD_LAYOUT.md` - Dashboard UI patterns

---

*Last updated: 2026-07-15*
