'use strict';
// Scope caches to this repository path so multiple Pages apps do not collide.
const PREFIX='jma:'+self.registration.scope+':';
const CACHE=PREFIX+'v0.2.0';
const FILES=['./','./index.html','./styles.css','./app.js','./catalogue.json','./icon.svg','./manifest.webmanifest','./icon-192.png','./icon-512.png'];
self.addEventListener('install',e=>e.waitUntil(caches.open(CACHE).then(c=>c.addAll(FILES)).then(()=>self.skipWaiting())));
self.addEventListener('activate',e=>e.waitUntil(caches.keys().then(keys=>Promise.all(keys.filter(k=>k.startsWith(PREFIX)&&k!==CACHE).map(k=>caches.delete(k)))).then(()=>self.clients.claim())));
self.addEventListener('fetch',e=>{const u=new URL(e.request.url);if(e.request.method!=='GET'||u.origin!==self.location.origin)return;const allowed=FILES.map(f=>new URL(f,self.registration.scope).href);if(!allowed.includes(u.origin+u.pathname))return;e.respondWith(fetch(e.request).then(async r=>{if(r.ok&&!r.redirected&&r.type!=='opaqueredirect'){const c=await caches.open(CACHE);await c.put(e.request,r.clone());}return r;}).catch(()=>caches.match(e.request,{cacheName:CACHE}).then(r=>r||new Response('Offline file unavailable',{status:503}))));});
