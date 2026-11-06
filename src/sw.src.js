/* Service worker de Costa y Cebo: permite usar la web sin conexión.
   La versión la pone build.py; al cambiar, se descarta la caché antigua de la página. */
const VERSION = "__VERSION__";
const CORE = "core-" + VERSION;
const TILES = "tiles-v1";
const FONTS = "fonts-v1";
const MAX_TILES = 400;
const CORE_FILES = ["./", "./index.html", "./manifest.webmanifest", "./icons/icon-192.png", "./icons/icon-512.png", "./icons/favicon-32.png", "./og.png",
  "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.js"];

self.addEventListener("install", e => {
  e.waitUntil(caches.open(CORE).then(c => c.addAll(CORE_FILES)).then(() => self.skipWaiting()));
});
self.addEventListener("activate", e => {
  e.waitUntil(caches.keys().then(keys => Promise.all(keys.filter(k => k.startsWith("core-") && k !== CORE).map(k => caches.delete(k))))
    .then(() => self.clients.claim()));
});

async function trim(name, max) {
  const c = await caches.open(name), keys = await c.keys();
  for (let i = 0; i < keys.length - max; i++) await c.delete(keys[i]);
}
async function cacheFirst(req, name, max) {
  const c = await caches.open(name), hit = await c.match(req);
  if (hit) return hit;
  try {
    const res = await fetch(req);
    if (res && (res.ok || res.type === "opaque")) { c.put(req, res.clone()); if (max) trim(name, max); }
    return res;
  } catch (err) { return hit || Response.error(); }
}
async function networkFirst(req) {
  const c = await caches.open(CORE);
  try {
    const res = await fetch(req);
    if (res && res.ok) c.put(req, res.clone());
    return res;
  } catch (err) {
    return (await c.match(req)) || (await c.match("./index.html")) || (await c.match("./")) || Response.error();
  }
}

self.addEventListener("fetch", e => {
  const req = e.request;
  if (req.method !== "GET") return;
  const url = new URL(req.url);
  if (url.origin === location.origin) {
    if (req.mode === "navigate" || url.pathname.endsWith(".html") || url.pathname === "/") { e.respondWith(networkFirst(req)); return; }
    e.respondWith(cacheFirst(req, CORE)); return;
  }
  if (url.hostname === "cdnjs.cloudflare.com") { e.respondWith(cacheFirst(req, CORE)); return; }
  if (url.hostname === "fonts.googleapis.com" || url.hostname === "fonts.gstatic.com") { e.respondWith(cacheFirst(req, FONTS, 40)); return; }
  if (url.hostname.endsWith("ign.es") && url.pathname.includes("/wmts/")) { e.respondWith(cacheFirst(req, TILES, MAX_TILES)); return; }
  if (url.hostname === "ows.emodnet-bathymetry.eu") { e.respondWith(cacheFirst(req, TILES, MAX_TILES)); return; }
  /* Open-Meteo y el resto van directos a la red; la página guarda el último parte por su cuenta. */
});
