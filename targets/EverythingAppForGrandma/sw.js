/**
 * sw.js -- CK Service Worker: Offline-First
 * ===========================================
 * CK works without internet. All operator algebra runs locally.
 * The service worker caches everything on first load.
 *
 * (c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
 */

const CACHE_NAME = 'ck-app-v2';
const CORE_ASSETS = [
    '/',
    '/index.html',
    '/style.css',
    '/app.js',
    '/ck_core.js',
    '/ck_audio.js',
    '/manifest.json',
];

// Install: cache all core assets
self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME).then((cache) => {
            return cache.addAll(CORE_ASSETS);
        })
    );
    self.skipWaiting();
});

// Activate: clean up old caches
self.addEventListener('activate', (event) => {
    event.waitUntil(
        caches.keys().then((names) => {
            return Promise.all(
                names.filter((name) => name !== CACHE_NAME)
                     .map((name) => caches.delete(name))
            );
        })
    );
    self.clients.claim();
});

// Fetch: cache-first, fallback to network
self.addEventListener('fetch', (event) => {
    // Skip non-GET and API requests
    if (event.request.method !== 'GET') return;
    if (event.request.url.includes('/api/')) return;
    if (event.request.url.includes('/ask')) return;

    event.respondWith(
        caches.match(event.request).then((cached) => {
            if (cached) return cached;
            return fetch(event.request).then((response) => {
                // Cache new assets
                if (response.ok) {
                    const clone = response.clone();
                    caches.open(CACHE_NAME).then((cache) => {
                        cache.put(event.request, clone);
                    });
                }
                return response;
            }).catch(() => {
                // Offline fallback
                return caches.match('/index.html');
            });
        })
    );
});
