/* ========================================
   Kabulhaden Service Worker
   Version: 1.0.0
   ======================================== */

const CACHE_NAME = 'kabulhaden-v2';
const OFFLINE_URL = '/static/offline.html';
const STATIC_ASSETS = [
    '/',
    '/static/manifest.json',
    '/static/css/styles.css',
    '/static/css/homepage.css',
    '/static/js/homepage.js',
    '/static/icons/icon-192x192.svg',
    '/static/icons/icon-512x512.svg',
    '/offline/'
];

const API_CACHE = 'kabulhaden-api-v1';
const PAGE_CACHE = 'kabulhaden-pages-v1';
const IMAGE_CACHE = 'kabulhaden-images-v1';
const FONT_CACHE = 'kabulhaden-fonts-v1';

const NETWORK_TIMEOUT = 5000;

/* --- Install --- */
self.addEventListener('install', event => {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(cache => cache.addAll(STATIC_ASSETS))
            .then(() => self.skipWaiting())
    );
});

/* --- Activate --- */
self.addEventListener('activate', event => {
    event.waitUntil(
        caches.keys().then(keys =>
            Promise.all(
                keys.filter(key => key !== CACHE_NAME && key !== API_CACHE && key !== PAGE_CACHE && key !== IMAGE_CACHE && key !== FONT_CACHE)
                    .map(key => caches.delete(key))
            )
        ).then(() => self.clients.claim())
    );
});

/* --- Fetch Strategy Router --- */
self.addEventListener('fetch', event => {
    const { request } = event;
    const url = new URL(request.url);

    if (request.method !== 'GET') return;

    if (url.pathname.startsWith('/radio/api/') || url.pathname.startsWith('/api/')) {
        event.respondWith(networkFirstWithTimeout(request, API_CACHE, NETWORK_TIMEOUT));
        return;
    }

    if (request.destination === 'image') {
        event.respondWith(staleWhileRevalidate(request, IMAGE_CACHE));
        return;
    }

    if (request.destination === 'font') {
        event.respondWith(cacheFirst(request, FONT_CACHE));
        return;
    }

    if (url.pathname.endsWith('/') || request.headers.get('accept')?.includes('text/html')) {
        event.respondWith(staleWhileRevalidatePage(request));
        return;
    }

    event.respondWith(cacheFirst(request, CACHE_NAME));
});

/* --- Cache Strategies --- */

function cacheFirst(request, cacheName) {
    return caches.match(request).then(cached => {
        if (cached) return cached;
        return fetch(request).then(response => {
            if (response.ok) {
                const clone = response.clone();
                caches.open(cacheName).then(cache => cache.put(request, clone));
            }
            return response;
        }).catch(() => new Response('', { status: 503, statusText: 'Offline' }));
    });
}

function networkFirstWithTimeout(request, cacheName, timeout) {
    return caches.open(cacheName).then(cache =>
        fetch(request).then(response => {
            if (response.ok) {
                const clone = response.clone();
                cache.put(request, clone);
            }
            return response;
        }).catch(() => cache.match(request))
    );
}

function staleWhileRevalidate(request, cacheName) {
    return caches.open(cacheName).then(cache =>
        cache.match(request).then(cached => {
            const fetchPromise = fetch(request).then(response => {
                if (response.ok) cache.put(request, response.clone());
                return response;
            }).catch(() => cached);
            return cached || fetchPromise;
        })
    );
}

function staleWhileRevalidatePage(request) {
    return caches.open(PAGE_CACHE).then(cache =>
        cache.match(request).then(cached => {
            const fetchPromise = fetch(request).then(response => {
                if (response.ok) {
                    const clone = response.clone();
                    cache.put(request, clone);
                }
                return response;
            }).catch(() => {
                if (cached) return cached;
                return caches.match(OFFLINE_URL).then(offline => offline || new Response('Offline', { status: 503 }));
            });
            return cached || fetchPromise;
        })
    );
}

/* --- Message Handler --- */
self.addEventListener('message', event => {
    if (event.data && event.data.type === 'SKIP_WAITING') {
        self.skipWaiting();
    }
    if (event.data && event.data.type === 'GET_VERSION') {
        event.ports[0].postMessage({ version: CACHE_NAME });
    }
});

/* --- Background Sync Placeholder --- */
self.addEventListener('sync', event => {
    if (event.tag === 'sync-data') {
        event.waitUntil(Promise.resolve());
    }
});
