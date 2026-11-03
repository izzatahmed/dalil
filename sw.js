'use strict';
const PREFIX='jma:'+self.registration.scope+':',CACHE=PREFIX+'v0.13.0';
const FILES=['./','./index.html','./styles.css?v=0.13.0','./app.js?v=0.13.0','./core.js?v=0.13.0','./search.js?v=0.13.0','./catalogue.json','./prices.json','./renalrounds.json','./barcodes.json','./manifest.webmanifest?v=0.13.0','./manifest.en.webmanifest?v=0.13.0','./icon.svg?v=0.13.0','./icon-192.png?v=0.13.0','./icon-512.png?v=0.13.0'];
const paths=new Set(FILES.map(f=>new URL(f,self.registration.scope).pathname));
self.addEventListener('install',e=>e.waitUntil(caches.open(CACHE).then(c=>c.addAll(FILES)).then(()=>self.skipWaiting())));
self.addEventListener('activate',e=>e.waitUntil(caches.keys().then(keys=>Promise.all(keys.filter(k=>k.startsWith(PREFIX)&&k!==CACHE).map(k=>caches.delete(k)))).then(()=>self.clients.claim())));
self.addEventListener('fetch',e=>{const u=new URL(e.request.url);if(e.request.method!=='GET'||u.origin!==self.location.origin||!paths.has(u.pathname))return;e.respondWith(fetch(e.request).then(async r=>{if(r.ok&&!r.redirected&&r.type!=='opaqueredirect'){const cache=await caches.open(CACHE);await cache.put(e.request,r.clone());}return r;}).catch(()=>caches.match(e.request,{cacheName:CACHE}).then(r=>r||new Response('Offline file unavailable',{status:503}))));});
