/* ========================================
   Kabulhaden — App Experience JavaScript
   PWA · Keyboard · Network · Toast · Search · Share
   ======================================== */

(function () {
    'use strict';

    /* ----------------------------------------
       1. INTERSECTION OBSERVER — Lazy Load
       ---------------------------------------- */
    function initLazyLoad() {
        const imgs = document.querySelectorAll('img[data-src]');
        if (imgs.length && 'IntersectionObserver' in window) {
            const imgObs = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const img = entry.target;
                        img.src = img.dataset.src;
                        img.removeAttribute('data-src');
                        img.classList.add('animate-fade-in');
                        imgObs.unobserve(img);
                    }
                });
            }, { rootMargin: '200px 0px' });
            imgs.forEach(el => imgObs.observe(el));
        }

        const sections = document.querySelectorAll('.reveal, .reveal-left, .reveal-right');
        if (sections.length && 'IntersectionObserver' in window) {
            const secObs = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        entry.target.classList.add('revealed');
                        secObs.unobserve(entry.target);
                    }
                });
            }, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });
            sections.forEach(el => secObs.observe(el));
        }

        const lazyComps = document.querySelectorAll('[data-lazy-component]');
        if (lazyComps.length && 'IntersectionObserver' in window) {
            const compObs = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        entry.target.classList.add('animate-fade-in-up');
                        compObs.unobserve(entry.target);
                    }
                });
            }, { threshold: 0.15 });
            lazyComps.forEach(el => compObs.observe(el));
        }
    }

    /* ----------------------------------------
       2. ANIMATED COUNTER
       ---------------------------------------- */
    function initCounters() {
        const counters = document.querySelectorAll('[data-counter]');
        if (!counters.length || !('IntersectionObserver' in window)) return;
        const obs = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const el = entry.target;
                    const target = parseInt(el.getAttribute('data-counter'), 10);
                    const suffix = el.getAttribute('data-suffix') || '';
                    const duration = 2000;
                    const start = performance.now();
                    const ease = t => t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
                    function tick(now) {
                        const elapsed = now - start;
                        const progress = Math.min(elapsed / duration, 1);
                        el.textContent = Math.round(ease(progress) * target).toLocaleString('id-ID') + suffix;
                        if (progress < 1) requestAnimationFrame(tick);
                    }
                    requestAnimationFrame(tick);
                    obs.unobserve(el);
                }
            });
        }, { threshold: 0.3 });
        counters.forEach(el => obs.observe(el));
    }

    /* ----------------------------------------
       3. SMOOTH SCROLL
       ---------------------------------------- */
    function initSmoothScroll() {
        document.querySelectorAll('a[href^="#"]').forEach(a => {
            a.addEventListener('click', e => {
                const id = a.getAttribute('href');
                if (id.length > 1) {
                    const target = document.querySelector(id);
                    if (target) {
                        e.preventDefault();
                        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
                    }
                }
            });
        });
    }

    /* ----------------------------------------
       4. DRAG-TO-SCROLL
       ---------------------------------------- */
    function initDragScroll() {
        document.querySelectorAll('[data-drag-scroll]').forEach(container => {
            let isDown = false, startX, scrollLeft;
            container.addEventListener('mousedown', e => {
                if (e.target.closest('a, button')) return;
                isDown = true;
                container.style.cursor = 'grabbing';
                startX = e.pageX - container.offsetLeft;
                scrollLeft = container.scrollLeft;
            });
            container.addEventListener('mouseleave', () => { isDown = false; container.style.cursor = ''; });
            container.addEventListener('mouseup', () => { isDown = false; container.style.cursor = ''; });
            container.addEventListener('mousemove', e => {
                if (!isDown) return;
                e.preventDefault();
                const x = e.pageX - container.offsetLeft;
                container.scrollLeft = scrollLeft - (x - startX) * 1.5;
            });
        });
    }

    /* ----------------------------------------
       5. SEARCH MODAL
       ---------------------------------------- */
    function initSearch() {
        const searchModal = document.getElementById('search-modal');
        if (searchModal) {
            document.addEventListener('keydown', e => {
                if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
                    e.preventDefault();
                    toggleSearch();
                }
                if (e.key === 'Escape' && !searchModal.classList.contains('hidden')) {
                    toggleSearch();
                }
            });
        }
    }

    window.toggleSearch = function () {
        const modal = document.getElementById('search-modal');
        if (!modal) return;
        const isHidden = modal.classList.contains('hidden');
        modal.classList.toggle('hidden');
        if (isHidden) {
            document.body.style.overflow = 'hidden';
            const input = modal.querySelector('input[type="search"]');
            if (input) setTimeout(() => input.focus(), 100);
        } else {
            document.body.style.overflow = '';
        }
    };

    window.handleSearch = function (query) {
        const resultsContainer = document.getElementById('search-results');
        if (!resultsContainer) return;
        if (query.length < 2) {
            resultsContainer.innerHTML = '<p class="text-center text-coffee-300 text-sm py-8">Ketik minimal 2 karakter...</p>';
            return;
        }
        resultsContainer.innerHTML = '<div class="flex items-center justify-center py-8"><div class="w-6 h-6 border-2 border-coffee-400 border-t-transparent rounded-full animate-spin"></div></div>';
        fetch('/pencarian/?q=' + encodeURIComponent(query), {
            headers: { 'X-Requested-With': 'XMLHttpRequest' }
        })
        .then(r => r.text())
        .then(html => {
            resultsContainer.innerHTML = html;
            saveRecentSearch(query);
        })
        .catch(() => {
            resultsContainer.innerHTML = '<p class="text-center text-coffee-300 py-8 text-sm">Gagal memuat hasil pencarian.</p>';
        });
    };

    /* ----------------------------------------
       6. RECENT SEARCHES
       ---------------------------------------- */
    function getRecentSearches() {
        try {
            return JSON.parse(localStorage.getItem('kabulhaden_recent_searches') || '[]');
        } catch { return []; }
    }

    function saveRecentSearch(query) {
        const searches = getRecentSearches().filter(s => s !== query);
        searches.unshift(query);
        localStorage.setItem('kabulhaden_recent_searches', JSON.stringify(searches.slice(0, 8)));
    }

    window.clearRecentSearches = function () {
        localStorage.removeItem('kabulhaden_recent_searches');
        const container = document.getElementById('recent-searches');
        if (container) container.innerHTML = '';
    };

    /* ----------------------------------------
       7. SCHEDULE DAY TABS
       ---------------------------------------- */
    window.switchScheduleDay = function (day, el) {
        document.querySelectorAll('.schedule-day-content').forEach(c => c.classList.add('hidden'));
        document.querySelectorAll('.schedule-tab').forEach(t => t.classList.remove('active'));
        const target = document.getElementById('schedule-' + day);
        if (target) target.classList.remove('hidden');
        if (el) el.classList.add('active');
    };

    /* ----------------------------------------
       8. MOBILE PLAYER FULLSCREEN
       ---------------------------------------- */
    window.openMobilePlayer = function () {
        const fs = document.getElementById('mobile-player-fullscreen');
        if (fs) { fs.style.display = 'flex'; document.body.style.overflow = 'hidden'; }
    };
    window.closeMobilePlayer = function () {
        const fs = document.getElementById('mobile-player-fullscreen');
        if (fs) { fs.style.display = 'none'; document.body.style.overflow = ''; }
    };

    /* ----------------------------------------
       9. COPY STREAM LINK
       ---------------------------------------- */
    window.copyStreamLink = function () {
        const url = window.location.origin;
        if (navigator.clipboard) {
            navigator.clipboard.writeText(url).then(() => {
                showToast('Link berhasil disalin!', 'success');
            });
        }
    };

    /* ----------------------------------------
       10. SHARE EXPERIENCE
       ---------------------------------------- */
    window.shareContent = function (title, text, url) {
        url = url || window.location.href;
        text = text || document.title;
        title = title || 'Kabulhaden';
        if (navigator.share) {
            navigator.share({ title: title, text: text, url: url }).catch(() => {});
        } else {
            const shareMenu = document.createElement('div');
            shareMenu.className = 'fixed inset-0 z-[200] flex items-end sm:items-center justify-center bg-black/50 p-4';
            shareMenu.innerHTML = '<div class="bg-white rounded-2xl w-full max-w-sm overflow-hidden animate-fade-in-up">' +
                '<div class="p-4 border-b border-coffee-100"><h3 class="font-heading font-semibold text-coffee-700">Bagikan</h3></div>' +
                '<div class="p-2">' +
                '<button onclick="shareToWhatsApp(\'' + encodeURIComponent(text) + '\', \'' + encodeURIComponent(url) + '\')" class="w-full flex items-center gap-3 p-3 rounded-xl hover:bg-coffee-50 transition-colors text-left"><span class="w-10 h-10 rounded-full bg-green-100 flex items-center justify-center"><svg class="w-5 h-5 text-green-600" fill="currentColor" viewBox="0 0 24 24"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347z"/><path d="M12 0C5.373 0 0 5.373 0 12c0 2.625.846 5.059 2.284 7.034L.789 23.492a.5.5 0 00.611.611l4.458-1.495A11.952 11.952 0 0012 24c6.627 0 12-5.373 12-12S18.627 0 12 0zm0 22c-2.37 0-4.567-.82-6.293-2.192l-.44-.371-2.635.882.882-2.635-.371-.44A9.965 9.965 0 012 12C2 6.477 6.477 2 12 2s10 4.477 10 10-4.477 10-10 10z"/></svg></span><div><p class="font-medium text-sm text-coffee-700">WhatsApp</p><p class="text-xs text-coffee-300">Bagikan via WhatsApp</p></div></button>' +
                '<button onclick="shareToTelegram(\'' + encodeURIComponent(url) + '\')" class="w-full flex items-center gap-3 p-3 rounded-xl hover:bg-coffee-50 transition-colors text-left"><span class="w-10 h-10 rounded-full bg-blue-100 flex items-center justify-center"><svg class="w-5 h-5 text-blue-500" fill="currentColor" viewBox="0 0 24 24"><path d="M11.944 0A12 12 0 000 12a12 12 0 0012 12 12 12 0 0012-12A12 12 0 0012 0a12 12 0 00-.056 0zm4.962 7.224c.1-.002.321.023.465.14a.506.506 0 01.171.325c.016.093.036.306.02.472-.18 1.898-.962 6.502-1.36 8.627-.168.9-.499 1.201-.82 1.23-.696.065-1.225-.46-1.9-.902-1.056-.693-1.653-1.124-2.678-1.8-1.185-.78-.417-1.21.258-1.91.177-.184 3.247-2.977 3.307-3.23.007-.032.014-.15-.056-.212s-.174-.041-.249-.024c-.106.024-1.793 1.14-5.061 3.345-.479.33-.913.49-1.302.48-.428-.008-1.252-.241-1.865-.44-.752-.245-1.349-.374-1.297-.789.027-.216.325-.437.893-.663 3.498-1.524 5.83-2.529 6.998-3.014 3.332-1.386 4.025-1.627 4.476-1.635z"/></svg></span><div><p class="font-medium text-sm text-coffee-700">Telegram</p><p class="text-xs text-coffee-300">Bagikan via Telegram</p></div></button>' +
                '<button onclick="shareToFacebook(\'' + encodeURIComponent(url) + '\')" class="w-full flex items-center gap-3 p-3 rounded-xl hover:bg-coffee-50 transition-colors text-left"><span class="w-10 h-10 rounded-full bg-blue-100 flex items-center justify-center"><svg class="w-5 h-5 text-blue-600" fill="currentColor" viewBox="0 0 24 24"><path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/></svg></span><div><p class="font-medium text-sm text-coffee-700">Facebook</p><p class="text-xs text-coffee-300">Bagikan via Facebook</p></div></button>' +
                '<button onclick="shareToX(\'' + encodeURIComponent(text) + '\', \'' + encodeURIComponent(url) + '\')" class="w-full flex items-center gap-3 p-3 rounded-xl hover:bg-coffee-50 transition-colors text-left"><span class="w-10 h-10 rounded-full bg-slate-100 flex items-center justify-center"><svg class="w-5 h-5 text-slate-900" fill="currentColor" viewBox="0 0 24 24"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg></span><div><p class="font-medium text-sm text-coffee-700">X (Twitter)</p><p class="text-xs text-coffee-300">Bagikan via X</p></div></button>' +
                '<button onclick="shareByEmail(\'' + encodeURIComponent(text) + '\', \'' + encodeURIComponent(url) + '\')" class="w-full flex items-center gap-3 p-3 rounded-xl hover:bg-coffee-50 transition-colors text-left"><span class="w-10 h-10 rounded-full bg-coffee-100 flex items-center justify-center"><svg class="w-5 h-5 text-coffee-500" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/></svg></span><div><p class="font-medium text-sm text-coffee-700">Email</p><p class="text-xs text-coffee-300">Bagikan via Email</p></div></button>' +
                '<button onclick="copyShareLink(\'' + encodeURIComponent(url) + '\')" class="w-full flex items-center gap-3 p-3 rounded-xl hover:bg-coffee-50 transition-colors text-left"><span class="w-10 h-10 rounded-full bg-coffee-100 flex items-center justify-center"><svg class="w-5 h-5 text-coffee-500" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 105.367-2.684 3 3 0 00-5.367 2.684zm0 9.316a3 3 0 105.368 2.684 3 3 0 00-5.368-2.684z"/></svg></span><div><p class="font-medium text-sm text-coffee-700">Salin Link</p><p class="text-xs text-coffee-300">Salin ke clipboard</p></div></button>' +
                '</div>' +
                '<div class="p-2 border-t border-coffee-100"><button onclick="this.closest(\'.fixed\').remove()" class="w-full py-2.5 rounded-xl text-sm font-medium text-coffee-400 hover:bg-coffee-50 transition-colors">Batal</button></div>' +
                '</div>';
            document.body.appendChild(shareMenu);
            shareMenu.addEventListener('click', e => { if (e.target === shareMenu) shareMenu.remove(); });
        }
    };

    window.shareToWhatsApp = function (text, url) { window.open('https://wa.me/?text=' + text + '%20' + url, '_blank'); document.querySelector('.fixed.z-\\[200\\]')?.remove(); };
    window.shareToTelegram = function (url) { window.open('https://t.me/share/url?url=' + url, '_blank'); document.querySelector('.fixed.z-\\[200\\]')?.remove(); };
    window.shareToFacebook = function (url) { window.open('https://www.facebook.com/sharer/sharer.php?u=' + url, '_blank'); document.querySelector('.fixed.z-\\[200\\]')?.remove(); };
    window.shareToX = function (text, url) { window.open('https://twitter.com/intent/tweet?text=' + text + '&url=' + url, '_blank'); document.querySelector('.fixed.z-\\[200\\]')?.remove(); };
    window.shareByEmail = function (text, url) { window.open('mailto:?subject=' + text + '&body=' + url, '_blank'); document.querySelector('.fixed.z-\\[200\\]')?.remove(); };
    window.copyShareLink = function (url) {
        if (navigator.clipboard) navigator.clipboard.writeText(decodeURIComponent(url));
        showToast('Link berhasil disalin!', 'success');
        document.querySelector('.fixed.z-\\[200\\]')?.remove();
    };

    /* ----------------------------------------
       11. TOAST NOTIFICATION SYSTEM
       ---------------------------------------- */
    window.showToast = function (message, type, duration) {
        type = type || 'info';
        duration = duration || (type === 'error' ? 8000 : 4000);
        const colors = {
            success: 'bg-green-600',
            error: 'bg-red-600',
            warning: 'bg-yellow-500',
            info: 'bg-coffee-600'
        };
        const icons = {
            success: '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>',
            error: '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>',
            warning: '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.34 16.5c-.77.833.192 2.5 1.732 2.5z"/>',
            info: '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>'
        };
        const existing = document.getElementById('kabulhaden-toast');
        if (existing) existing.remove();
        const toast = document.createElement('div');
        toast.id = 'kabulhaden-toast';
        toast.className = 'fixed top-24 left-1/2 -translate-x-1/2 z-[200] px-5 py-3 rounded-2xl ' + (colors[type] || colors.info) + ' text-white text-sm font-medium shadow-lg flex items-center gap-3 animate-fade-in-up max-w-[90vw]';
        toast.innerHTML = '<svg class="w-5 h-5 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">' + (icons[type] || icons.info) + '</svg><span>' + message + '</span>';
        document.body.appendChild(toast);
        setTimeout(() => {
            toast.style.transition = 'opacity 0.3s, transform 0.3s';
            toast.style.opacity = '0';
            toast.style.transform = 'translateX(-50%) translateY(-10px)';
            setTimeout(() => toast.remove(), 300);
        }, duration);
    };

    /* ----------------------------------------
       12. NETWORK AWARENESS
       ---------------------------------------- */
    function initNetworkAwareness() {
        let banner = null;

        function showOfflineBanner() {
            if (banner) return;
            banner = document.createElement('div');
            banner.id = 'network-banner';
            banner.className = 'fixed top-0 left-0 right-0 z-[250] px-4 py-2.5 bg-red-600 text-white text-sm font-medium text-center flex items-center justify-center gap-2';
            banner.innerHTML = '<svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M18.364 5.636a9 9 0 010 12.728m0 0l-2.829-2.829m2.829 2.829L21 21M15.536 8.464a5 5 0 010 7.072m0 0l-2.829-2.829m-4.243 2.829a5 5 0 01-1.414-2.83m-1.414 5.658a9 9 0 01-2.167-9.238m7.824 2.167a1 1 0 111.414 1.414m-1.414-1.414L3 3"/></svg>Tidak ada koneksi internet';
            document.body.prepend(banner);
        }

        function showReconnectBanner() {
            if (banner) banner.remove();
            banner = document.createElement('div');
            banner.id = 'network-banner';
            banner.className = 'fixed top-0 left-0 right-0 z-[250] px-4 py-2.5 bg-green-600 text-white text-sm font-medium text-center flex items-center justify-center gap-2 animate-fade-in';
            banner.innerHTML = '<svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7"/></svg>Koneksi tersambung kembali';
            document.body.prepend(banner);
            setTimeout(() => {
                if (banner) {
                    banner.style.transition = 'opacity 0.3s';
                    banner.style.opacity = '0';
                    setTimeout(() => { if (banner) banner.remove(); banner = null; }, 300);
                }
            }, 3000);
        }

        window.addEventListener('offline', showOfflineBanner);
        window.addEventListener('online', showReconnectBanner);
        if (!navigator.onLine) showOfflineBanner();
    }

    /* ----------------------------------------
       13. KEYBOARD SHORTCUTS
       ---------------------------------------- */
    function initKeyboardShortcuts() {
        document.addEventListener('keydown', e => {
            if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA' || e.target.isContentEditable) return;

            if (e.key === '/') {
                e.preventDefault();
                toggleSearch();
                return;
            }

            if (e.key === 'm' || e.key === 'M') {
                const player = window._radioPlayer;
                if (player) player.toggleMute();
                return;
            }

            if (e.key === ' ' && !e.target.closest('button, a, input, select, textarea')) {
                e.preventDefault();
                const player = window._radioPlayer;
                if (player) player.togglePlay();
                return;
            }

            if (e.key === 'ArrowUp') {
                e.preventDefault();
                const player = window._radioPlayer;
                if (player) {
                    player.volume = Math.min(100, player.volume + 5);
                    player.audio.volume = player.isMuted ? 0 : player.volume / 100;
                    player.saveVolumePreference();
                }
                return;
            }

            if (e.key === 'ArrowDown') {
                e.preventDefault();
                const player = window._radioPlayer;
                if (player) {
                    player.volume = Math.max(0, player.volume - 5);
                    player.audio.volume = player.isMuted ? 0 : player.volume / 100;
                    player.saveVolumePreference();
                }
                return;
            }

            if (e.key === 'Escape') {
                const fullscreen = document.getElementById('mobile-player-fullscreen');
                if (fullscreen && fullscreen.style.display !== 'none') {
                    closeMobilePlayer();
                    return;
                }
                const searchModal = document.getElementById('search-modal');
                if (searchModal && !searchModal.classList.contains('hidden')) {
                    toggleSearch();
                    return;
                }
            }
        });
    }

    /* ----------------------------------------
       14. SKELETON LOADING PLACEHOLDER
       ---------------------------------------- */
    window.createSkeleton = function (type) {
        type = type || 'card';
        const skeletons = {
            card: '<div class="bg-white rounded-card border border-coffee-200 overflow-hidden animate-pulse"><div class="aspect-video bg-coffee-100 skeleton"></div><div class="p-4 space-y-3"><div class="h-4 bg-coffee-100 rounded-full w-3/4 skeleton"></div><div class="h-3 bg-coffee-100 rounded-full w-1/2 skeleton"></div><div class="h-3 bg-coffee-100 rounded-full w-full skeleton"></div></div></div>',
            list: '<div class="flex items-center gap-4 p-4 bg-white rounded-xl border border-coffee-200 animate-pulse"><div class="w-12 h-12 bg-coffee-100 rounded-xl skeleton flex-shrink-0"></div><div class="flex-1 space-y-2"><div class="h-4 bg-coffee-100 rounded-full w-3/4 skeleton"></div><div class="h-3 bg-coffee-100 rounded-full w-1/2 skeleton"></div></div></div>',
            text: '<div class="space-y-2 animate-pulse"><div class="h-4 bg-coffee-100 rounded-full w-full skeleton"></div><div class="h-4 bg-coffee-100 rounded-full w-5/6 skeleton"></div><div class="h-4 bg-coffee-100 rounded-full w-4/6 skeleton"></div></div>'
        };
        return skeletons[type] || skeletons.card;
    };

    /* ----------------------------------------
       15. HTMX ENHANCEMENTS
       ---------------------------------------- */
    function initHTMXEnhancements() {
        if (typeof htmx === 'undefined') return;

        document.body.addEventListener('htmx:beforeRequest', function (e) {
            const target = e.detail.target;
            if (target && target.dataset.htmxIndicator) {
                const indicator = document.querySelector(target.dataset.htmxIndicator);
                if (indicator) indicator.classList.remove('htmx-indicator');
            }
        });

        document.body.addEventListener('htmx:afterSwap', function (e) {
            const target = e.detail.target;
            if (target) {
                target.style.opacity = '0';
                target.style.transform = 'translateY(8px)';
                requestAnimationFrame(() => {
                    target.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
                    target.style.opacity = '1';
                    target.style.transform = 'translateY(0)';
                });
            }
            initLazyLoad();
            initCounters();
        });
    }

    /* ----------------------------------------
       16. PWA INSTALL PROMPT
       ---------------------------------------- */
    function initInstallPrompt() {
        let deferredPrompt = null;

        window.addEventListener('beforeinstallprompt', (e) => {
            e.preventDefault();
            deferredPrompt = e;
            showInstallBanner(deferredPrompt);
        });

        function showInstallBanner(prompt) {
            const existing = document.getElementById('pwa-install-banner');
            if (existing) return;
            const banner = document.createElement('div');
            banner.id = 'pwa-install-banner';
            banner.className = 'fixed bottom-24 left-4 right-4 sm:left-auto sm:right-4 sm:w-80 z-[90] bg-white rounded-2xl shadow-card-hover border border-coffee-200 p-4 flex items-center gap-4 animate-fade-in-up';
            banner.innerHTML = '<div class="w-12 h-12 rounded-xl bg-coffee-100 flex items-center justify-center flex-shrink-0"><svg class="w-6 h-6 text-coffee-500" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M12 18h.01M8 21h8a2 2 0 002-2V5a2 2 0 00-2-2H8a2 2 0 00-2 2v14a2 2 0 002 2z"/></svg></div><div class="flex-1 min-w-0"><p class="font-heading font-semibold text-sm text-coffee-700">Install Kabulhaden</p><p class="text-xs text-coffee-300">Akses cepat dari layar utama</p></div><div class="flex items-center gap-2"><button id="pwa-install-dismiss" class="p-1.5 rounded-lg text-coffee-300 hover:text-coffee-500 hover:bg-coffee-50 transition-colors"><svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12"/></svg></button><button id="pwa-install-accept" class="px-4 py-2 rounded-xl bg-coffee-400 text-white text-sm font-heading font-semibold hover:bg-coffee-500 transition-colors">Install</button></div>';
            document.body.appendChild(banner);

            document.getElementById('pwa-install-accept').addEventListener('click', () => {
                prompt.prompt();
                prompt.userChoice.then(choice => {
                    if (choice.outcome === 'accepted') showToast('Kabulhaden berhasil diinstall!', 'success');
                    banner.remove();
                    deferredPrompt = null;
                });
            });
            document.getElementById('pwa-install-dismiss').addEventListener('click', () => banner.remove());
        }

        window.addEventListener('appinstalled', () => {
            deferredPrompt = null;
            showToast('Kabulhaden berhasil diinstall!', 'success');
        });
    }

    /* ----------------------------------------
       17. STANDALONE MODE DETECTION
       ---------------------------------------- */
    function initStandaloneDetection() {
        if (window.matchMedia('(display-mode: standalone)').matches || window.navigator.standalone === true) {
            document.body.classList.add('pwa-standalone');
        }
    }

    /* ----------------------------------------
       18. VIEWPORT UNITS FIX (Mobile)
       ---------------------------------------- */
    function initViewportFix() {
        function setVH() {
            const vh = window.innerHeight * 0.01;
            document.documentElement.style.setProperty('--vh', vh + 'px');
        }
        setVH();
        window.addEventListener('resize', setVH);
    }

    /* ----------------------------------------
       INIT
       ---------------------------------------- */
    document.addEventListener('DOMContentLoaded', () => {
        initLazyLoad();
        initCounters();
        initSmoothScroll();
        initDragScroll();
        initSearch();
        initKeyboardShortcuts();
        initNetworkAwareness();
        initHTMXEnhancements();
        initInstallPrompt();
        initStandaloneDetection();
        initViewportFix();
    });

})();
