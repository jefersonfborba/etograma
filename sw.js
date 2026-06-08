const CACHE = 'etograma-v1.0.2';
const SHELL = './etograma.html';
const ASSETS = [
  './',
  './index.html',
  './etograma.html',
  './manifest.json',
  './icons/icon-192.png',
  './icons/icon-512.png'
];

self.addEventListener('install', e => {
  e.waitUntil(
    caches.open(CACHE).then(c => c.addAll(ASSETS)).then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys()
      .then(keys => Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', e => {
  // Navegações (abrir pelo ícone, F5, links) sempre servem o shell cacheado
  if (e.request.mode === 'navigate') {
    e.respondWith(
      caches.match(SHELL).then(cached => cached || fetch(e.request))
    );
    return;
  }
  e.respondWith(
    caches.match(e.request).then(cached => cached || fetch(e.request))
  );
});
