/**
 * AntWorld Service Worker
 * Enables offline access for most of the site
 * EXCLUDES: /photo-id/ (image-based identification requires server ML processing)
 */

const CACHE_NAME = 'antworld-v1';
const OFFLINE_URL = '/offline.html';


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


const NETWORK_ONLY_PATHS = [
  '/photo-id',      // Future ML image identification
  '/id-image',      // Alternative path for image ID
  '/api/',          // Any API calls
  '/upload'         // Image uploads
];


function shouldSkipCache(url) {
  const urlPath = new URL(url).pathname;
  return NETWORK_ONLY_PATHS.some(path => urlPath.startsWith(path));
}


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


self.addEventListener('fetch', event => {
  const request = event.request;


  if (request.method !== 'GET') return;


  if (shouldSkipCache(request.url)) {
    event.respondWith(
      fetch(request).catch(() => {

        return new Response(
          JSON.stringify({ error: 'offline', message: 'Image identification requires an internet connection' }),
          { headers: { 'Content-Type': 'application/json' } }
        );
      })
    );
    return;
  }


  event.respondWith(
    caches.match(request)
      .then(cachedResponse => {
        if (cachedResponse) {

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


        return fetch(request)
          .then(response => {

            if (!response.ok || response.type !== 'basic') {
              return response;
            }


            const responseToCache = response.clone();
            caches.open(CACHE_NAME)
              .then(cache => cache.put(request, responseToCache));

            return response;
          })
          .catch(() => {

            if (request.headers.get('Accept').includes('text/html')) {
              return caches.match(OFFLINE_URL);
            }
          });
      })
  );
});
