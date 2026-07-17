/**
 * Kabulhaden Radio Player — Alpine.js component
 * Loaded synchronously (non-deferred) before Alpine initializes.
 * Registered both as Alpine.data AND as a global function so x-data="radioPlayer()"
 * always resolves regardless of timing.
 */
(function () {
  function radioPlayerFactory() {
    return {
      isPlaying: false,
      isLoading: false,
      isLive: false,
      isMuted: false,
      volume: parseInt(localStorage.getItem('radio_volume') || '75'),
      progress: 0,
      currentTime: 0,
      duration: 0,
      audio: null,
      pollInterval: null,
      reconnectTimer: null,
      reconnectAttempts: 0,
      maxReconnectAttempts: 10,
      isOffline: false,
      streamUrl: '',
      currentTrack: { title: '', artist: '', artwork: '' },

      init() {
        // Reuse existing singleton audio instance across multiple player components
        if (window._radioPlayer) {
          this.audio = window._radioPlayer.audio;
          this.isPlaying = window._radioPlayer.isPlaying;
          this.isMuted = window._radioPlayer.isMuted;
          this.volume = window._radioPlayer.volume;
          this.streamUrl = window._radioPlayer.streamUrl;
          this.currentTrack = window._radioPlayer.currentTrack;
          this.isLive = window._radioPlayer.isLive;
          this.pollInterval = window._radioPlayer.pollInterval;
          if (typeof this.$nextTick === 'function') {
            this.$nextTick(() => this.setupMediaSession());
          }
          return;
        }

        this.audio = new Audio();
        this.audio.preload = 'auto';
        this.audio.crossOrigin = 'anonymous';
        this.audio.volume = this.volume / 100;

        this.audio.addEventListener('playing', () => {
          this.isPlaying = true;
          this.isLoading = false;
          this.reconnectAttempts = 0;
        });
        this.audio.addEventListener('pause', () => {
          if (!this.audio.ended) this.isPlaying = false;
        });
        this.audio.addEventListener('ended', () => {
          this.isPlaying = false;
          this.scheduleReconnect();
        });
        this.audio.addEventListener('error', () => {
          this.isPlaying = false;
          this.isLoading = false;
          this.scheduleReconnect();
        });
        this.audio.addEventListener('waiting', () => {
          if (this.isPlaying) this.isLoading = true;
        });
        this.audio.addEventListener('canplay', () => {
          this.isLoading = false;
        });
        this.audio.addEventListener('timeupdate', () => {
          this.currentTime = this.audio.currentTime;
          if (this.audio.duration) {
            this.duration = this.audio.duration;
            this.progress = (this.audio.currentTime / this.audio.duration) * 100;
          }
        });

        window._radioPlayer = this;
        window.addEventListener('online', () => {
          this.isOffline = false;
          if (this.streamUrl) this.scheduleReconnect();
        });
        window.addEventListener('offline', () => { this.isOffline = true; });

        this.loadVolumePreference();
        this.fetchStatus();
        this.pollInterval = setInterval(() => this.fetchStatus(), 10000);
        this.setupMediaSession();
      },

      destroy() {
        if (this.pollInterval) clearInterval(this.pollInterval);
        if (this.reconnectTimer) clearTimeout(this.reconnectTimer);
      },

      loadVolumePreference() {
        const saved = localStorage.getItem('radio_volume');
        if (saved) {
          this.volume = parseInt(saved);
          if (this.audio) this.audio.volume = this.volume / 100;
        }
      },

      saveVolumePreference() {
        localStorage.setItem('radio_volume', this.volume);
      },

      scheduleReconnect() {
        if (this.reconnectAttempts >= this.maxReconnectAttempts) return;
        if (this.reconnectTimer) clearTimeout(this.reconnectTimer);
        const delay = Math.min(1000 * Math.pow(2, this.reconnectAttempts), 30000);
        this.reconnectAttempts++;
        this.reconnectTimer = setTimeout(() => {
          if (!navigator.onLine) return;
          this.fetchStatus();
          if (this.streamUrl) {
            this.isLoading = true;
            this.audio.src = this.streamUrl;
            this.audio.play().catch(() => {});
          }
        }, delay);
      },

      fetchStatus() {
        fetch('/radio/api/status/')
          .then(r => r.json())
          .then(data => {
            this.streamUrl = data.stream_url || '';
            this.isLive = data.is_live || false;
            const newTrack = {
              title: data.title || data.track_title || 'Kabulhaden Radio',
              artist: data.artist || data.track_artist || 'Siaran Langsung',
              artwork: data.artwork || data.album_art || ''
            };
            const changed = newTrack.title !== this.currentTrack.title || newTrack.artist !== this.currentTrack.artist;
            this.currentTrack = newTrack;
            if (changed && 'mediaSession' in navigator) {
              navigator.mediaSession.metadata = new MediaMetadata({
                title: this.currentTrack.title,
                artist: this.currentTrack.artist,
                artwork: this.currentTrack.artwork
                  ? [{ src: this.currentTrack.artwork, sizes: '512x512', type: 'image/png' }]
                  : []
              });
            }
            if (this.isPlaying && this.streamUrl && this.audio.src !== window.location.origin + this.streamUrl) {
              const wasPlaying = this.isPlaying;
              this.audio.src = this.streamUrl;
              if (wasPlaying) this.audio.play().catch(() => {});
            }
          })
          .catch(() => {});
      },

      togglePlay() {
        if (this.isLoading) return;
        if (!this.streamUrl) { this.fetchStatus(); return; }
        if (this.isPlaying) {
          this.audio.pause();
          this.isPlaying = false;
        } else {
          this.isLoading = true;
          if (!this.audio.src || this.audio.src === window.location.href) {
            this.audio.src = this.streamUrl;
          }
          this.audio.play()
            .then(() => { this.isPlaying = true; this.isLoading = false; this.reconnectAttempts = 0; })
            .catch(() => { this.isPlaying = false; this.isLoading = false; this.scheduleReconnect(); });
        }
      },

      toggleMute() {
        this.isMuted = !this.isMuted;
        this.audio.muted = this.isMuted;
        this.audio.volume = this.isMuted ? 0 : this.volume / 100;
      },

      setVolume(event) {
        const rect = event.currentTarget.getBoundingClientRect();
        const percent = Math.round(((event.clientX - rect.left) / rect.width) * 100);
        this.volume = Math.max(0, Math.min(100, percent));
        this.audio.volume = this.isMuted ? 0 : this.volume / 100;
        if (this.volume > 0 && this.isMuted) { this.isMuted = false; this.audio.muted = false; }
        this.saveVolumePreference();
      },

      seek(event) {
        if (!this.audio.duration) return;
        const rect = event.currentTarget.getBoundingClientRect();
        this.audio.currentTime = ((event.clientX - rect.left) / rect.width) * this.audio.duration;
      },

      formatTime(seconds) {
        if (!seconds || isNaN(seconds)) return '0:00';
        const m = Math.floor(seconds / 60);
        const s = Math.floor(seconds % 60);
        return m + ':' + (s < 10 ? '0' : '') + s;
      },

      setupMediaSession() {
        if (!('mediaSession' in navigator)) return;
        navigator.mediaSession.metadata = new MediaMetadata({
          title: this.currentTrack.title || 'Kabulhaden Radio',
          artist: this.currentTrack.artist || 'Siaran Langsung',
          artwork: this.currentTrack.artwork
            ? [{ src: this.currentTrack.artwork, sizes: '512x512', type: 'image/png' }]
            : []
        });
        navigator.mediaSession.setActionHandler('play', () => this.togglePlay());
        navigator.mediaSession.setActionHandler('pause', () => this.togglePlay());
        navigator.mediaSession.setActionHandler('stop', () => {
          this.audio.pause(); this.audio.currentTime = 0; this.isPlaying = false;
        });
        navigator.mediaSession.setActionHandler('seekbackward', () => {
          this.audio.currentTime = Math.max(0, this.audio.currentTime - 10);
        });
        navigator.mediaSession.setActionHandler('seekforward', () => {
          this.audio.currentTime = Math.min(this.audio.duration || 0, this.audio.currentTime + 10);
        });
      },

      openMobilePlayer() {},
      copyStreamLink() {
        if (this.streamUrl) {
          navigator.clipboard.writeText(window.location.origin + this.streamUrl).catch(() => {});
        }
      },
      showTooltip() {},
      hideTooltip() {}
    };
  }

  // 1. Expose as global function — Alpine x-data="radioPlayer()" can call this directly
  window.radioPlayer = radioPlayerFactory;

  // 2. Register with Alpine.data as soon as Alpine is ready
  document.addEventListener('alpine:init', () => {
    if (typeof Alpine !== 'undefined' && Alpine.data) {
      Alpine.data('radioPlayer', radioPlayerFactory);
    }
  });
})();
