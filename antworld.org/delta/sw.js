/**
 * AntWorld Service Worker - Self-unregistering
 * PWA functionality removed. This SW clears caches and unregisters itself.
 */

// Clear all caches and unregister
self.addEventListener('install', () => self.skipWaiting());
self.addEventListener('activate', async () => {
  // Delete all caches
  const keys = await caches.keys();
  await Promise.all(keys.map(k => caches.delete(k)));

  // Unregister this service worker
  const registrations = await self.registration.unregister();

  // Claim clients to take effect immediately
  await self.clients.claim();

  console.log('[SW] PWA disabled - caches cleared, service worker unregistered');
});
