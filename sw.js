const V='swish-v1', SHELL=['./','./index.html','./manifest.webmanifest','./icon-192.png','./icon-512.png','./icon-180.png'];
self.addEventListener('install',e=>{e.waitUntil(caches.open(V).then(c=>c.addAll(SHELL)).then(()=>self.skipWaiting()))});
self.addEventListener('activate',e=>{e.waitUntil(caches.keys().then(k=>Promise.all(k.filter(x=>x!==V).map(x=>caches.delete(x)))).then(()=>self.clients.claim()))});
// Cache-first for everything (app shell, TF.js, COCO-SSD model weights); fills the cache on first online use.
self.addEventListener('fetch',e=>{
 if(e.request.method!=='GET')return;
 e.respondWith(caches.match(e.request).then(hit=>hit||fetch(e.request).then(r=>{
  if(r&&(r.ok||r.type==='opaque')){const c=r.clone();caches.open(V).then(ch=>ch.put(e.request,c))}
  return r;
 }).catch(()=>caches.match('./index.html'))));
});
