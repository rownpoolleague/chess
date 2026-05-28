const CACHE_NAME = 'sscc-v2';

// -------------------------
// INSTALL
// -------------------------
self.addEventListener('install', (e) => {
  self.skipWaiting();
  e.waitUntil(
    caches.open(CACHE_NAME).then((cache) => cache.addAll([
      './',
      './index.html'
    ]))
  );
});

// -------------------------
// ACTIVATE
// -------------------------
self.addEventListener('activate', (e) => {
  e.waitUntil(
    caches.keys().then((keyList) => {
      return Promise.all(keyList.map((key) => {
        if (key !== CACHE_NAME) {
          return caches.delete(key);
        }
      }));
    }).then(() => self.clients.claim())
  );
});

// -------------------------
// FETCH (Network First)
// -------------------------
self.addEventListener('fetch', (e) => {
  e.respondWith(
    fetch(e.request)
      .then((response) => {
        const responseClone = response.clone();
        caches.open(CACHE_NAME).then((cache) => {
          cache.put(e.request, responseClone);
        });
        return response;
      })
      .catch(() => caches.match(e.request))
  );
});

// -------------------------
// ⭐ PUSH NOTIFICATIONS
// -------------------------
self.addEventListener('push', (event) => {
  let data = {};

  try {
    data = event.data.json();
  } catch (e) {
    data = { title: "Tournament Update", body: event.data.text() };
  }

  const title = data.title || "Tournament Update";
  const body = data.body || "New pairings or results are available.";
  const icon = "icon.png"; // optional

  event.waitUntil(
    self.registration.showNotification(title, {
      body,
      icon,
      badge: icon
    })
  );
});

// -------------------------
// OPTIONAL: Notification Click Handler
// -------------------------
self.addEventListener('notificationclick', (event) => {
  event.notification.close();

  event.waitUntil(
    clients.matchAll({ type: "window" }).then((clientList) => {
      for (const client of clientList) {
        if (client.url.includes("index.html") && "focus" in client) {
          return client.focus();
        }
      }
      if (clients.openWindow) {
        return clients.openWindow("./index.html");
      }
    })
  );
});

});
