/**
 * AntWorld Service Worker v11
 * Precache ENTIRE site + better URL matching for back navigation
 */

const CACHE_NAME = 'antworld-v11';
const OFFLINE_URL = '/offline';

// ALL pages and assets to precache on install
const PRECACHE = [
  // Core pages (multiple URL formats for home)
  '/',
  '/index',
  '/offline',
  '/morpho',
  '/diversity',
  '/geo_diversity',
  '/tax_diversity',
  '/sources',
  '/training',
  '/credits',
  '/privacy',
  '/list_species',

  // ID keys - main
  '/id/formicinae_ergate',
  '/id/myrmicinae_ergate',
  '/id/ponerinae_ergate',
  '/id/amblyoponinae_ergate',
  '/id/aenictinae_ergate',
  '/id/leptanillinae_ergate',

  // ID keys - subfamilies/genera
  '/id/acropyga_ergate',
  '/id/acropyga_rhyzomyrma2_ergate',
  '/id/camponotini_ergate',
  '/id/cauto&chthonolasius_ergate',
  '/id/cerapachys_ergate',
  '/id/cerapachys&leptogenys_ergate',
  '/id/confirmed.ergate_id',
  '/id/crematogaster',
  '/id/lasiini_ergate',
  '/id/lasius_ergate',
  '/id/leptanilla_ergate',
  '/id/leptanilla_sp_ergate',
  '/id/littleformicinae_ergate',
  '/id/palm_ergate_id',
  '/id/pdf_ergate',
  '/id/polyergus_ergate',
  '/id/polyrhachis1.1_ergate',
  '/id/polyrhachis2_4_ergate',

  // Species pages
  '/id/species/discothyrea_kamiteta_ergate',
  '/id/species/polyergus_nigerrimus_ergate',
  '/id/species/polyergus_rufescens_ergate',
  '/id/species/polyergus_samurai_ergate',

  // CSS
  '/css/css_antworld.css',
  '/css/antworld-icons.css',

  // JavaScript
  '/js/jquery-3.1.1.min.js',
  '/js/lang.js',
  '/js/chart.min.js',
  '/js/highcharts.js',
  '/js/highmaps.js',
  '/js/d3.min.js',
  '/js/d3pie.min.js',
  '/js/world.js',
  '/js/magglass.js',
  '/js/jszip.min.js',
  '/js/modules/exporting.js',
  '/js/modules/offline-exporting.js',
  '/js/modules/data.js',

  // Icons
  '/icon/favicon.ico',
  '/icon/favicon.svg'
];

const SKIP_PATHS = ['/photo-id', '/api/', '/upload'];

// Install: download and cache EVERYTHING
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => {
      console.log('[SW] Downloading entire site...');
      return Promise.all(
        PRECACHE.map(url => cache.add(url).catch(() => console.log('[SW] Skip:', url)))
      );
    }).then(() => self.skipWaiting())
  );
});

// Activate: clean old caches
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.filter(k => k !== CACHE_NAME).map(k => caches.delete(k)))
    ).then(() => self.clients.claim())
  );
});

// Fetch: cache-first with smart URL matching
self.addEventListener('fetch', event => {
  const url = new URL(event.request.url);

  // Only handle same-origin GET requests
  if (event.request.method !== 'GET') return;
  if (url.origin !== location.origin) return;
  if (SKIP_PATHS.some(p => url.pathname.startsWith(p))) return;

  event.respondWith(
    caches.open(CACHE_NAME).then(async cache => {
      // Normalize pathname for matching
      let pathname = url.pathname;

      // Try exact match first
      let cached = await cache.match(event.request);

      // Try variations if not found
      if (!cached) {
        const variations = [
          pathname,
          pathname.replace(/\.html$/, ''),           // without .html
          pathname.replace(/\/$/, ''),               // without trailing slash
          pathname === '/' ? '/index' : null,        // home as /index
          pathname + '/',                            // with trailing slash
        ].filter(Boolean);

        for (const variant of variations) {
          cached = await cache.match(url.origin + variant);
          if (cached) break;
        }
      }

      if (cached) return cached;

      // Not in cache: fetch and cache
      try {
        const response = await fetch(event.request);
        if (response.ok) {
          cache.put(event.request, response.clone());
        }
        return response;
      } catch (e) {
        if (event.request.mode === 'navigate') {
          return cache.match(OFFLINE_URL);
        }
        throw e;
      }
    })
  );
});
