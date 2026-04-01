/**
 * AntWorld Service Worker
 * Enables offline access for most of the site
 * EXCLUDES: /photo-id/ (image-based identification requires server ML processing)
 */

const CACHE_NAME = 'antworld-v1';
const OFFLINE_URL = '/offline.html';

// Assets to cache on install
const PRECACHE_ASSETS = [
  '/',
  '/index.html',
  '/morpho.html',
  '/diversity.html',
  '/sources.html',
  '/training.html',
  '/credits.html',
  '/privacy.html',
  '/css/css_antworld.css',
  '/css/antworld-icons.css',
  '/js/jquery-3.1.1.min.js',
  '/js/lang.js',
  '/img/logo.png',
  '/icon/favicon.ico',
  '/icon/favicon.svg'
];

// Paths that should NEVER be cached (require live server)
const NETWORK_ONLY_PATHS = [
  '/photo-id',      // Future ML image identification
  '/id-image',      // Alternative path for image ID
  '/api/',          // Any API calls
  '/upload'         // Image uploads
];

// Check if URL should skip cache
function shouldSkipCache(url) {
  const urlPath = new URL(url).pathname;
  return NETWORK_ONLY_PATHS.some(path => urlPath.startsWith(path));
}

// Install event - precache core assets
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        console.log('[SW] Precaching core assets');
        return cache.addAll(PRECACHE_ASSETS);
      })
      .then(() => self.skipWaiting())
      .catch(err => console.log('[SW] Precache failed:', err))
  );
});

// Activate event - clean old caches
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cacheName => {
          if (cacheName !== CACHE_NAME) {
            console.log('[SW] Deleting old cache:', cacheName);
            return caches.delete(cacheName);
          }
        })
      );
    }).then(() => self.clients.claim())
  );
});

// Fetch event - cache-first for most, network-only for excluded paths
self.addEventListener('fetch', event => {
  const request = event.request;

  // Only handle GET requests
  if (request.method !== 'GET') return;

  // Network-only for excluded paths (photo ID, API, etc.)
  if (shouldSkipCache(request.url)) {
    event.respondWith(
      fetch(request).catch(() => {
        // Return offline message for excluded paths
        return new Response(
          JSON.stringify({ error: 'offline', message: 'Image identification requires an internet connection' }),
          { headers: { 'Content-Type': 'application/json' } }
        );
      })
    );
    return;
  }

  // Cache-first strategy for everything else
  event.respondWith(
    caches.match(request)
      .then(cachedResponse => {
        if (cachedResponse) {
          // Return cached version, but also update cache in background
          event.waitUntil(
            fetch(request)
              .then(response => {
                if (response.ok) {
                  caches.open(CACHE_NAME)
                    .then(cache => cache.put(request, response));
                }
              })
              .catch(() => {}) // Ignore network errors during background update
          );
          return cachedResponse;
        }

        // Not in cache - fetch from network and cache it
        return fetch(request)
          .then(response => {
            // Don't cache non-OK responses or non-same-origin
            if (!response.ok || response.type !== 'basic') {
              return response;
            }

            // Clone and cache the response
            const responseToCache = response.clone();
            caches.open(CACHE_NAME)
              .then(cache => cache.put(request, responseToCache));

            return response;
          })
          .catch(() => {
            // Offline fallback for HTML pages
            if (request.headers.get('Accept').includes('text/html')) {
              return caches.match(OFFLINE_URL);
            }
          });
      })
  );
});
