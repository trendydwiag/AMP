/* ============================================================
   AMP Studio — Main Application JavaScript
   Alpine.js Data Definitions & Initialization
   ============================================================ */

document.addEventListener('alpine:init', () => {
  /* ── Theme Engine ── */
  Alpine.data('themeEngine', () => ({
    theme: localStorage.getItem('amp-theme') || 'light',

    init() {
      this.applyTheme();
      window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
        if (!localStorage.getItem('amp-theme')) {
          this.theme = e.matches ? 'dark' : 'light';
          this.applyTheme();
        }
      });
    },

    applyTheme() {
      document.documentElement.setAttribute('data-theme', this.theme);
      localStorage.setItem('amp-theme', this.theme);
    },

    toggleTheme() {
      this.theme = this.theme === 'light' ? 'dark' : 'light';
      this.applyTheme();
    },

    setTheme(t) {
      this.theme = t;
      this.applyTheme();
    }
  }));
});


/* ── Main AMP Studio Data ── */
function ampStudio() {
  return {
    // Sidebar
    sidebarCollapsed: JSON.parse(localStorage.getItem('amp-sidebar-collapsed') || 'false'),
    sidebarMobileOpen: false,

    // Theme
    theme: localStorage.getItem('amp-theme') || 'light',

    // Command Palette
    commandPaletteOpen: false,
    commandQuery: '',
    commandResults: [],
    commandIndex: 0,

    // Notifications
    notificationPanelOpen: false,
    notifications: [],
    unreadCount: 0,

    // Mobile
    isMobile: window.innerWidth < 1024,

    // Quick commands
    defaultCommands: [
      {
        icon: '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>',
        title: 'Artikel Baru',
        description: 'Buat artikel baru',
        url: '/berita/cms/artikel/buat/',
        shortcut: '⌘N'
      },
      {
        icon: '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 1a3 3 0 00-3 3v8a3 3 0 006 0V4a3 3 0 00-3-3z"/><path d="M19 10v2a7 7 0 01-14 0v-2"/></svg>',
        title: 'Episode Podcast Baru',
        description: 'Unggah episode podcast',
        url: '/podcast/podcast/episode/buat/',
        shortcut: ''
      },
      {
        icon: '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"/><path d="M15.54 8.46a5 5 0 010 7.07"/></svg>',
        title: 'Jadwal Siaran',
        description: 'Kelola jadwal siaran',
        url: '/broadcast/jadwal/',
        shortcut: ''
      },
      {
        icon: '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"/><circle cx="8.5" cy="8.5" r="1.5"/><polyline points="21 15 16 10 5 21"/></svg>',
        title: 'Media Library',
        description: 'Kelola file media',
        url: '/media/',
        shortcut: ''
      },
      {
        icon: '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>',
        title: 'Analytics',
        description: 'Lihat statistik',
        url: '/radio/analytics/',
        shortcut: ''
      },
      {
        icon: '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg>',
        title: 'Artikel Berita',
        description: 'Lihat semua artikel',
        url: '/berita/cms/artikel/',
        shortcut: ''
      }
    ],

    init() {
      // Theme
      document.documentElement.setAttribute('data-theme', this.theme);

      // Keyboard shortcuts
      document.addEventListener('keydown', (e) => {
        // Ctrl+K / Cmd+K — Command Palette
        if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
          e.preventDefault();
          this.commandPaletteOpen = !this.commandPaletteOpen;
          if (this.commandPaletteOpen) {
            this.$nextTick(() => this.$refs.commandInput?.focus());
          }
        }
        // Escape — close panels
        if (e.key === 'Escape') {
          this.commandPaletteOpen = false;
          this.notificationPanelOpen = false;
          this.sidebarMobileOpen = false;
        }
      });

      // Responsive
      window.addEventListener('resize', () => {
        this.isMobile = window.innerWidth < 1024;
        if (!this.isMobile) this.sidebarMobileOpen = false;
      });

      // Close mobile sidebar on nav click
      this.$watch('sidebarMobileOpen', (val) => {
        document.body.style.overflow = val ? 'hidden' : '';
      });

      // Load notifications
      this.loadNotifications();
    },

    // ── Sidebar ──
    toggleSidebar() {
      this.sidebarCollapsed = !this.sidebarCollapsed;
      localStorage.setItem('amp-sidebar-collapsed', this.sidebarCollapsed);
    },

    // ── Theme ──
    toggleTheme() {
      this.theme = this.theme === 'light' ? 'dark' : 'light';
      document.documentElement.setAttribute('data-theme', this.theme);
      localStorage.setItem('amp-theme', this.theme);
    },

    // ── Command Palette ──
    searchCommands() {
      const q = this.commandQuery.toLowerCase().trim();
      if (!q) {
        this.commandResults = [];
        return;
      }

      const allItems = this.defaultCommands;
      const matches = allItems.filter(item =>
        item.title.toLowerCase().includes(q) ||
        item.description.toLowerCase().includes(q)
      );

      this.commandResults = matches.length > 0
        ? [{ label: 'Hasil Pencarian', items: matches }]
        : [];
    },

    executeCommand(item) {
      if (item.url) {
        window.location.href = item.url;
      }
      this.commandPaletteOpen = false;
      this.commandQuery = '';
      this.commandResults = [];
    },

    // ── Notifications ──
    loadNotifications() {
      // Static sample notifications — will be replaced with API call
      this.notifications = [
        {
          id: 1,
          type: 'warning',
          title: 'Menunggu review',
          message: 'Artikel "Perkembangan Terkini" membutuhkan persetujuan Anda',
          time: '5 menit yang lalu',
          read: false
        },
        {
          id: 2,
          type: 'success',
          title: 'Artikel diterbitkan',
          message: '"Tips Produktivitas untuk Pekerja Remote" berhasil diterbitkan',
          time: '1 jam yang lalu',
          read: false
        },
        {
          id: 3,
          type: 'danger',
          title: 'Stream terputus',
          message: 'Siaran langsung terputus selama 5 menit',
          time: '3 jam yang lalu',
          read: true
        }
      ];
      this.unreadCount = this.notifications.filter(n => !n.read).length;
    },

    markAllRead() {
      this.notifications.forEach(n => n.read = true);
      this.unreadCount = 0;
    },

    getNotificationIcon(type) {
      const icons = {
        warning: '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="var(--amp-warning)" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>',
        success: '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="var(--amp-success)" stroke-width="2"><path d="M22 11.08V12a10 10 0 11-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>',
        danger: '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="var(--amp-danger)" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/></svg>',
        info: '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="var(--amp-info)" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>'
      };
      return icons[type] || icons.info;
    },

    getNotificationBg(type) {
      const bgs = {
        warning: 'bg-[var(--amp-warning-light)]',
        success: 'bg-[var(--amp-success-light)]',
        danger: 'bg-[var(--amp-danger-light)]',
        info: 'bg-[var(--amp-info-light)]'
      };
      return bgs[type] || bgs.info;
    }
  };
}


/* ── Stream Status Widget ── */
function streamStatus() {
  return {
    isLive: false,
    listenerCount: 0,
    currentProgram: '',
    currentHost: '',
    streamUrl: '',
    _interval: null,

    init() {
      this.fetchStatus();
      this._interval = setInterval(() => this.fetchStatus(), 15000);
    },

    destroy() {
      if (this._interval) clearInterval(this._interval);
    },

    async fetchStatus() {
      try {
        const res = await fetch('/radio/api/status/');
        if (!res.ok) throw new Error('API error');
        const data = await res.json();
        this.isLive = data.stream_status === 'PLAYING' || data.is_active;
        this.listenerCount = data.current_listeners || 0;
        this.currentProgram = data.current_program || '';
        this.currentHost = data.current_host || '';
        this.streamUrl = data.stream_url || '';
      } catch (e) {
        this.isLive = false;
      }
    }
  };
}


/* ── AMP Player ── */
function ampPlayer() {
  return {
    isPlaying: false,
    volume: parseInt(localStorage.getItem('amp-volume') || '75'),
    currentSong: '',
    currentProgram: '',
    bitrate: 0,
    listeners: 0,
    streamUrl: '',
    _audio: null,
    _interval: null,

    init() {
      this._audio = new Audio();
      this._audio.volume = this.volume / 100;
      this._audio.preload = 'none';

      this._audio.addEventListener('playing', () => { this.isPlaying = true; });
      this._audio.addEventListener('pause', () => { this.isPlaying = false; });
      this._audio.addEventListener('error', () => { this.isPlaying = false; });

      this.fetchConfig();
      this._interval = setInterval(() => this.fetchNowPlaying(), 20000);
    },

    destroy() {
      if (this._audio) { this._audio.pause(); this._audio.src = ''; }
      if (this._interval) clearInterval(this._interval);
    },

    async fetchConfig() {
      try {
        const res = await fetch('/radio/api/player-config/');
        if (!res.ok) return;
        const data = await res.json();
        this.streamUrl = data.stream_url || '';
        this.bitrate = data.stream_bitrate || 128;
      } catch (e) { /* silent */ }
    },

    async fetchNowPlaying() {
      try {
        const res = await fetch('/radio/api/status/');
        if (!res.ok) return;
        const data = await res.json();
        this.currentSong = data.song_title
          ? `${data.song_title}${data.artist ? ' — ' + data.artist : ''}`
          : '';
        this.currentProgram = data.current_program || 'Radio Kabulhaden';
        this.listeners = data.current_listeners || 0;
        if (!this.streamUrl && data.stream_url) this.streamUrl = data.stream_url;
      } catch (e) { /* silent */ }
    },

    togglePlay() {
      if (!this.streamUrl) return;
      if (this.isPlaying) {
        this._audio.pause();
      } else {
        this._audio.src = this.streamUrl;
        this._audio.load();
        this._audio.play().catch(() => {});
      }
    },

    setVolume() {
      if (this._audio) this._audio.volume = this.volume / 100;
      localStorage.setItem('amp-volume', this.volume);
    },

    reconnect() {
      if (this._audio) {
        this._audio.pause();
        this._audio.src = '';
      }
      this.fetchConfig();
      if (this.isPlaying) {
        setTimeout(() => {
          this._audio.src = this.streamUrl;
          this._audio.load();
          this._audio.play().catch(() => {});
        }, 500);
      }
    }
  };
}


/* ── Toast Utility ── */
function ampToast(message, type = 'info', duration = 4000) {
  const container = document.getElementById('toast-container');
  if (!container) return;

  const colors = {
    success: 'bg-[var(--amp-success)] text-white',
    error: 'bg-[var(--amp-danger)] text-white',
    warning: 'bg-[var(--amp-warning)] text-white',
    info: 'bg-[var(--amp-coffee-600)] text-white'
  };

  const icons = {
    success: '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 11.08V12a10 10 0 11-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>',
    error: '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/></svg>',
    warning: '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>',
    info: '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>'
  };

  const toast = document.createElement('div');
  toast.className = `flex items-center gap-3 px-4 py-3 rounded-xl shadow-lg text-sm font-medium ${colors[type]} transform transition-all duration-300 translate-x-full opacity-0`;
  toast.innerHTML = `
    <span>${icons[type] || icons.info}</span>
    <span>${message}</span>
    <button onclick="this.parentElement.remove()" class="ml-2 opacity-70 hover:opacity-100">
      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
    </button>
  `;

  container.appendChild(toast);
  requestAnimationFrame(() => {
    toast.classList.remove('translate-x-full', 'opacity-0');
  });

  setTimeout(() => {
    toast.classList.add('translate-x-full', 'opacity-0');
    setTimeout(() => toast.remove(), 300);
  }, duration);
}


/* ── Partner Switcher ── */
function partnerSwitcher() {
  return {
    open: false,
    partners: [],
    currentPartner: null,

    async init() {
      try {
        const resp = await fetch('/studio/partner/list/');
        const data = await resp.json();
        this.partners = data.partners || [];
        if (data.current) {
          this.currentPartner = this.partners.find(p => p.pk === data.current) || this.partners[0] || null;
        } else if (this.partners.length > 0) {
          this.currentPartner = this.partners[0];
        }
      } catch (e) {
        console.warn('Failed to load partners:', e);
      }
    },

    async switchPartner(partner) {
      if (partner.pk === this.currentPartner?.pk) {
        this.open = false;
        return;
      }
      try {
        const form = new FormData();
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value
          || document.cookie.match(/csrftoken=([^;]+)/)?.[1] || '';
        
        const resp = await fetch(`/studio/partner/switch/${partner.pk}/`, {
          method: 'POST',
          headers: {
            'X-CSRFToken': csrfToken,
          },
        });
        
        if (resp.redirected || resp.ok) {
          window.location.reload();
        }
      } catch (e) {
        console.error('Failed to switch partner:', e);
      }
      this.open = false;
    }
  };
}
