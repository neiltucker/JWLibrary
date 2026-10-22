// Service Worker for JW Library Tutorial (Offline PWA) - Version 10
// When you publish changes to any page or file listed below, raise the version
// (e.g. 'jw-tutorial-v4' -> 'jw-tutorial-v5') so phones replace their saved copies.
const CACHE_NAME = 'jw-tutorial-v10';

// How long to wait for the internet before showing the saved copy of a page.
// Keeps the guide quick on a weak signal (e.g. one bar of mobile data).
const NETWORK_TIMEOUT_MS = 3000;

// Saved on every learner's device on the first visit, so the guide works offline.
const CORE_FILES = [
  './',
  './index.html',
  './sw.html',
  './lg.html',
  './din.html',
  './manifest-en.json',
  './manifest-sw.json',
  './manifest-lg.json',
  './manifest-din.json',
  './icon-192.png',
  './icon-512.png'
];

// Facilitator files. Learners don't need these, so by default they are NOT downloaded
// in advance (saves about 0.35 MB of mobile data per learner). Anyone who opens one
// while online gets it saved for offline use automatically.
// Change false to true if you want every device to download them in advance.
const SAVE_FACILITATOR_FILES_FOR_EVERYONE = false;
const FACILITATOR_FILES = [
  './QR_English_en.png',
  './QR_English_en.svg',
  './QR_Kiswahili_sw.png',
  './QR_Kiswahili_sw.svg',
  './QR_Luganda_lg.png',
  './QR_Luganda_lg.svg',
  './QR_Dinka_din.png',
  './QR_Dinka_din.svg',
  './Table_Cards_English_en.pdf',
  './Table_Cards_Kiswahili_sw.pdf',
  './Table_Cards_Luganda_lg.pdf',
  './Table_Cards_Dinka_din.pdf'
];

const PRECACHE_FILES = SAVE_FACILITATOR_FILES_FOR_EVERYONE
  ? CORE_FILES.concat(FACILITATOR_FILES)
  : CORE_FILES;

// Save each file separately: one missing file or one dropped download
// no longer stops all the others from being saved (issue #6).
function saveFiles(files) {
  return caches.open(CACHE_NAME).then((cache) =>
    Promise.all(files.map((file) => cache.add(file).catch(() => null)))
  );
}

// Fill in any files that failed to download earlier (checked on each online page visit).
function saveMissingFiles() {
  return caches.open(CACHE_NAME).then((cache) =>
    Promise.all(PRECACHE_FILES.map((file) =>
      cache.match(file).then((found) => found ? null : cache.add(file).catch(() => null))
    ))
  );
}

self.addEventListener('install', (event) => {
  event.waitUntil(saveFiles(PRECACHE_FILES).then(() => self.skipWaiting()));
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) => {
      return Promise.all(
        keys.filter((key) => key !== CACHE_NAME).map((key) => caches.delete(key))
      );
    }).then(() => self.clients.claim())
  );
});

// Find the saved copy of a page (ignoring anything after "?", e.g. from a QR or shared link).
// orHomePage: if that page was never saved, use the saved English home page instead.
function findSavedPage(url, orHomePage) {
  return caches.match(url.origin + url.pathname, { ignoreSearch: true }).then((saved) => {
    if (saved || !orHomePage) return saved;
    return caches.match('./index.html');
  });
}

// HTML pages: newest version from the internet first; if the internet fails, or has not
// answered within NETWORK_TIMEOUT_MS, show the saved copy instead (issue #7).
function respondToPage(event, url) {
  const pageKey = url.origin + url.pathname;
  let saving = Promise.resolve();

  const fromNetwork = fetch(event.request).then((networkResponse) => {
    if (networkResponse && networkResponse.ok) {
      const responseClone = networkResponse.clone();
      saving = caches.open(CACHE_NAME)
        .then((cache) => cache.put(pageKey, responseClone))
        .then(saveMissingFiles);
    }
    return networkResponse;
  });

  // Let saving finish in the background even if the saved copy was shown first.
  event.waitUntil(fromNetwork.then(() => saving, () => null));

  return new Promise((resolve) => {
    let answered = false;
    const answer = (response) => {
      if (!answered && response) {
        answered = true;
        resolve(response);
      }
    };

    // Slow connection: after the time limit, show the saved copy of THIS page if there is one.
    // (If it isn't saved yet, keep waiting for the internet rather than showing another page.)
    const timer = setTimeout(() => {
      findSavedPage(url, false).then(answer);
    }, NETWORK_TIMEOUT_MS);

    fromNetwork
      .then((networkResponse) => {
        clearTimeout(timer);
        answer(networkResponse);
      })
      .catch(() => {
        // No connection at all (e.g. Airplane Mode): show the saved copy straight away.
        clearTimeout(timer);
        findSavedPage(url, true).then((saved) => answer(saved || Response.error()));
      });
  });
}

self.addEventListener('fetch', (event) => {
  if (event.request.method !== 'GET') return;

  const url = new URL(event.request.url);
  if (url.origin !== self.location.origin) return; // JW.ORG and other sites go straight to the internet

  if (event.request.mode === 'navigate') {
    event.respondWith(respondToPage(event, url));
    return;
  }

  // For static assets (images, icons, PDFs): Stale-While-Revalidate
  // Serve the saved copy immediately; refresh it in the background when online.
  const fetchPromise = fetch(event.request).then((networkResponse) => {
    if (networkResponse && networkResponse.ok) {
      const responseClone = networkResponse.clone();
      return caches.open(CACHE_NAME)
        .then((cache) => cache.put(event.request, responseClone))
        .then(() => networkResponse);
    }
    return networkResponse;
  });
  event.waitUntil(fetchPromise.catch(() => null));

  event.respondWith(
    caches.match(event.request, { ignoreSearch: true }).then((cachedResponse) => {
      return cachedResponse || fetchPromise.catch(() => Response.error());
    })
  );
});
