const cacheName = 'scms-app-cache-v1';  // Name of the cache

// List only essential pages to cache (core pages, icons, etc.)
const assetsToCache = [
    '/',  // Home page
    "/static/assets/img/vit_icon.png",
];

// Install event - Cache core files and static assets (CSS, JS, images)
self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open(cacheName).then((cache) => {
            return cache.addAll(assetsToCache);
        })
    );
});

// Fetch event - Cache all requests for static assets (JS, CSS, images, etc.)
self.addEventListener('fetch', (event) => {
    if (event.request.url.includes('/static/')) {
        event.respondWith(
            caches.match(event.request).then((cachedResponse) => {
                return cachedResponse || fetch(event.request);  // Cache-first approach
            })
        );
    } else {
        // For other requests (like HTML pages), fallback to network-first approach
        event.respondWith(
            caches.match(event.request).then((cachedResponse) => {
                return cachedResponse || fetch(event.request);
            })
        );
    }
});

// Activate event - Cleanup old caches when new version of service worker is installed
self.addEventListener('activate', (event) => {
    const cacheWhitelist = [cacheName];
    event.waitUntil(
        caches.keys().then((cacheNames) => {
            return Promise.all(
                cacheNames.map((cache) => {
                    if (!cacheWhitelist.includes(cache)) {
                        return caches.delete(cache);  // Delete old caches
                    }
                })
            );
        })
    );
});
