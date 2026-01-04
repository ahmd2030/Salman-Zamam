const CACHE_NAME = 'salman-app-v3.3-fast-prompt'; // Bumped for Fast Install Prompt
const ASSETS = [
    './',
    './index.html',
    './theme.css',
    './main.js',
    './logo.png',
    'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css',
    'https://cdnjs.cloudflare.com/ajax/libs/qrcodejs/1.0.0/qrcode.min.js',
    'https://unpkg.com/html5-qrcode'
];

// Install Event - IMMEDIATE ACTIVATE
self.addEventListener('install', (e) => {
    self.skipWaiting(); // Force new SW to take over
    e.waitUntil(
        caches.open(CACHE_NAME)
            .then((cache) => cache.addAll(ASSETS))
    );
});

// Activate Event - CLAIM CLIENTS & CLEAR OLD CACHE
self.addEventListener('activate', (e) => {
    e.waitUntil(
        Promise.all([
            clients.claim(), // Take control of open pages immediately
            caches.keys().then((keys) => {
                return Promise.all(
                    keys.map((key) => {
                        if (key !== CACHE_NAME) {
                            console.log('Clearing old cache:', key);
                            return caches.delete(key);
                        }
                    })
                );
            })
        ])
    );
});

// Fetch Event - NETWORK FIRST strategy for HTML to avoid stuck index
self.addEventListener('fetch', (e) => {
    // For HTML, try network first, fallback to cache
    if (e.request.mode === 'navigate') {
        e.respondWith(
            fetch(e.request).catch(() => caches.match(e.request))
        );
        return;
    }

    // For assets, Cache First
    e.respondWith(
        caches.match(e.request)
            .then((res) => res || fetch(e.request))
    );
});
