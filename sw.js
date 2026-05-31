importScripts('https://www.gstatic.com/firebasejs/12.14.0/firebase-app-compat.js');
importScripts('https://www.gstatic.com/firebasejs/12.14.0/firebase-messaging-compat.js');

firebase.initializeApp({
  apiKey: "AIzaSyBek60G1Ns_PVhODcp02H0S2jryhdUKFuQ",
  projectId: "sscc-push",
  messagingSenderId: "954838466310",
  appId: "1:954838466310:web:d7ba03562b6c0b8db66887"
});

const messaging = firebase.messaging();

// --- PUSH MESSAGE HANDLING ---
messaging.onBackgroundMessage((payload) => {
  const notificationTitle = payload.notification.title;
  const notificationOptions = {
    body: payload.notification.body,
    icon: '/chess/iconking.png',
    data: { url: payload.data.url } // Store the URL here so we can use it on click
  };

  self.registration.showNotification(notificationTitle, notificationOptions);
});

// --- HANDLE NOTIFICATION CLICK ---
self.addEventListener('notificationclick', (event) => {
  event.notification.close();
  const urlToOpen = event.notification.data.url;

  if (urlToOpen) {
    event.waitUntil(
      clients.openWindow(urlToOpen)
    );
  }
});

// --- YOUR EXISTING CACHE LOGIC ---

const CACHE_NAME = 'sscc-v2';

self.addEventListener('install', (e) => {
  self.skipWaiting();
  e.waitUntil(
    caches.open(CACHE_NAME).then((cache) => cache.addAll([
      './',
      './index.html'
    ]))
  );
});

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
      .catch(() => {
        return caches.match(e.request);
      })
  );
});
