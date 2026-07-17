# 30. Desktop Integration Guide (Future)

## Overview

This guide covers integrating desktop OS features with Kabulhaden CMS, enabling richer interactions like file system access, native menus, and system-level shortcuts for power users.

---

## Integration Scenarios

### Scenario A: Web App on Desktop

The existing Django CMS accessed via desktop browsers. Limited OS integration.

| Capability | Support |
|------------|---------|
| File drag-and-drop | Yes (HTML5) |
| Keyboard shortcuts | Yes (JavaScript) |
| Notifications | Yes (Web Notifications API) |
| File system access | No (File System Access API - Chrome only) |
| Native menus | No |
| System tray | No |

### Scenario B: Electron/Tauri Wrapper

Native desktop app wrapping the web CMS. Full OS integration.

| Capability | Support |
|------------|---------|
| File drag-and-drop | Yes |
| Keyboard shortcuts | Yes |
| Notifications | Yes |
| File system access | Yes |
| Native menus | Yes |
| System tray | Yes |
| Auto-updater | Yes |

---

## File System Integration

### Drag-and-Drop Upload

```javascript
// Static/js/upload-dragdrop.js
document.addEventListener('DOMContentLoaded', () => {
  const dropZone = document.querySelector('[data-drop-zone]');
  
  dropZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    e.stopPropagation();
    dropZone.classList.add('drag-over');
  });
  
  dropZone.addEventListener('dragleave', (e) => {
    e.preventDefault();
    dropZone.classList.remove('drag-over');
  });
  
  dropZone.addEventListener('drop', async (e) => {
    e.preventDefault();
    e.stopPropagation();
    dropZone.classList.remove('drag-over');
    
    const files = Array.from(e.dataTransfer.files);
    const audioFiles = files.filter(f => f.type.startsWith('audio/'));
    
    for (const file of audioFiles) {
      await uploadFile(file);
    }
  });
});

async function uploadFile(file) {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('csrfmiddlewaretoken', getCsrfToken());
  
  const response = await fetch('/media/upload/', {
    method: 'POST',
    body: formData,
  });
  
  return response.json();
}
```

### File System Access API (Chrome)

```javascript
// Open local folder for batch import
async function openLocalFolder() {
  const dirHandle = await window.showDirectoryPicker();
  
  for await (const entry of dirHandle.values()) {
    if (entry.kind === 'file') {
      const file = await entry.getFile();
      if (file.type.startsWith('audio/')) {
        await uploadFile(file);
      }
    }
  }
}
```

---

## Keyboard Shortcuts

### CMS Shortcuts

| Shortcut | Action | Context |
|----------|--------|---------|
| `Ctrl+S` | Save current form | Editor |
| `Ctrl+Shift+P` | Publish content | Editor |
| `Ctrl+K` | Command palette | Global |
| `Ctrl+/` | Toggle sidebar | Global |
| `Esc` | Close modal/dialog | Global |
| `Ctrl+Shift+M` | Open media manager | Global |

### Shortcut Implementation

```javascript
// Static/js/shortcuts.js
document.addEventListener('keydown', (e) => {
  // Ctrl+S: Save
  if (e.ctrlKey && e.key === 's') {
    e.preventDefault();
    const form = document.querySelector('form[data-autosave]');
    if (form) form.submit();
  }
  
  // Ctrl+K: Command palette
  if (e.ctrlKey && e.key === 'k') {
    e.preventDefault();
    openCommandPalette();
  }
});

function openCommandPalette() {
  // Modal with search input for quick navigation
  const modal = document.getElementById('command-palette');
  modal.classList.remove('hidden');
  modal.querySelector('input').focus();
}
```

### Shortcut Help Overlay

```
┌──────────────────────────────────────────────┐
│  Keyboard Shortcuts                          │
│                                              │
│  Navigation                                 │
│  ────────                                   │
│  Ctrl+K        Command palette              │
│  Ctrl+/        Toggle sidebar               │
│  G then D      Go to Dashboard              │
│  G then R      Go to Radio                  │
│  G then N      Go to News                   │
│                                              │
│  Editing                                    │
│  ────────                                   │
│  Ctrl+S        Save draft                   │
│  Ctrl+Shift+P Publish                       │
│  Ctrl+Shift+D Delete                        │
│                                              │
│  Media                                      │
│  ────────                                   │
│  Ctrl+Shift+M  Media manager                │
│  U             Upload file                  │
│                                              │
│  Press ? for this help                       │
│                               [Close]        │
└──────────────────────────────────────────────┘
```

---

## Native Notifications

### Web Notifications API

```javascript
// Static/js/notifications.js
class CMSNotifier {
  constructor() {
    this.permission = 'default';
  }
  
  async requestPermission() {
    if ('Notification' in window) {
      this.permission = await Notification.requestPermission();
    }
  }
  
  notify(title, options = {}) {
    if (this.permission === 'granted') {
      new Notification(title, {
        icon: '/static/icons/icon-192x192.png',
        badge: '/static/icons/badge-72x72.png',
        ...options,
      });
    }
  }
  
  streamLive(stationName) {
    this.notify('Radio is Live!', {
      body: `${stationName} is now broadcasting`,
      tag: 'stream-live',
    });
  }
  
  contentPublished(title) {
    this.notify('Content Published', {
      body: `"${title}" is now live`,
      tag: 'content-published',
    });
  }
}
```

---

## Electron Integration (Future)

### Main Process

```javascript
// electron/main.js
const { app, BrowserWindow, Menu, globalShortcut } = require('electron');

function createWindow() {
  const win = new BrowserWindow({
    width: 1280,
    height: 800,
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
    },
  });
  
  win.loadURL('http://localhost:8000');
}

// Global shortcuts
app.whenReady().then(() => {
  globalShortcut.register('CommandOrControl+Shift+R', () => {
    // Quick record/push to stream
  });
});

// App menu
const menu = Menu.buildFromTemplate([
  {
    label: 'Kabulhaden',
    submenu: [
      { role: 'about' },
      { type: 'separator' },
      { role: 'quit' },
    ],
  },
  {
    label: 'Stream',
    submenu: [
      { label: 'Start Broadcast', accelerator: 'CmdOrCtrl+Shift+B' },
      { label: 'Stop Broadcast', accelerator: 'CmdOrCtrl+Shift+X' },
      { type: 'separator' },
      { label: 'Stream Status' },
    ],
  },
]);
Menu.setApplicationMenu(menu);
```

### Preload Script

```javascript
// electron/preload.js
const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('electronAPI', {
  startBroadcast: () => ipcRenderer.invoke('stream:start'),
  stopBroadcast: () => ipcRenderer.invoke('stream:stop'),
  getStreamStatus: () => ipcRenderer.invoke('stream:status'),
  exportContent: (data) => ipcRenderer.invoke('export:content', data),
});
```

---

## System Tray (Electron)

```javascript
// electron/tray.js
const { Tray, Menu } = require('electron');
const path = require('path');

let tray = null;

function createTray() {
  tray = new Tray(path.join(__dirname, 'icons/tray.png'));
  
  const contextMenu = Menu.buildFromTemplate([
    { label: 'Now Playing: News Hour', enabled: false },
    { type: 'separator' },
    { label: 'Start Broadcast', click: startBroadcast },
    { label: 'Stop Broadcast', click: stopBroadcast },
    { type: 'separator' },
    { label: 'Open CMS', click: showWindow },
    { label: 'Quit', click: () => app.quit() },
  ]);
  
  tray.setToolTip('Kabulhaden CMS');
  tray.setContextMenu(contextMenu);
}
```

---

## Desktop-Specific UX Patterns

### System Notification Toast

```
┌─────────────────────────────────┐
│ 🔴 LIVE: News Hour is on air    │
│    Started 2 minutes ago        │
│    [Open Player]                │
└─────────────────────────────────┘
```

### Quick Import Dialog

```
┌──────────────────────────────────┐
│  Import Audio Files              │
│                                  │
│  ┌────────────────────────────┐  │
│  │                            │  │
│  │   Drop audio files here    │  │
│  │   or click to browse       │  │
│  │                            │  │
│  └────────────────────────────┘  │
│                                  │
│  Supported: MP3, WAV, OGG, FLAC  │
│  Max size: 500 MB                │
│                                  │
│  [Cancel]           [Import]     │
└──────────────────────────────────┘
```

---

## Related Documentation

- `28_FUTURE_DESKTOP_GUIDE.md` - Desktop app architecture
- `29_OFFLINE_PWA_GUIDE.md` - PWA offline support
- `11_COMPONENT_LIBRARY.md` - UI component patterns
- `13_NAVIGATION_SYSTEM.md` - Navigation and shortcuts

---

*Last updated: 2026-07-15*
