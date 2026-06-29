// Runtime media (album cover + 30s audio preview) from the free Deezer API,
// fetched on demand via JSONP so it works on a static site with no CORS proxy
// and no build-time cost. Results are cached in memory + localStorage, so each
// song is looked up at most once per device.
const norm = (s) =>
  (s || '').normalize('NFKD').replace(/[̀-ͯ]/g, '').toLowerCase().replace(/[^a-z0-9]/g, '');

const mem = new Map();
const LS_KEY = 'ctn_media_v1';
let store = {};
try { store = JSON.parse(localStorage.getItem(LS_KEY) || '{}'); } catch (e) { store = {}; }
let persistTimer = 0;
const persist = () => {
  clearTimeout(persistTimer);
  persistTimer = setTimeout(() => { try { localStorage.setItem(LS_KEY, JSON.stringify(store)); } catch (e) { /* quota */ } }, 800);
};

function jsonp(url) {
  return new Promise((resolve) => {
    const cb = 'ctn_dz_' + Math.random().toString(36).slice(2);
    const s = document.createElement('script');
    let done = false;
    const cleanup = () => { if (done) return; done = true; clearTimeout(timer); delete window[cb]; if (s.parentNode) s.parentNode.removeChild(s); };
    const timer = setTimeout(() => { cleanup(); resolve(null); }, 7000);
    window[cb] = (data) => { cleanup(); resolve(data); };
    s.onerror = () => { cleanup(); resolve(null); };
    s.src = `${url}${url.includes('?') ? '&' : '?'}output=jsonp&callback=${cb}`;
    document.head.appendChild(s);
  });
}

async function search(q) {
  const data = await jsonp(`https://api.deezer.com/search?q=${encodeURIComponent(q)}&limit=1`);
  return (data && data.data && data.data[0]) || null;
}

// Returns { preview?, cover? } for a (title, artist) pair. Always resolves
// (never throws); returns {} when nothing usable is found.
export async function getSongMedia(title, artist) {
  const key = norm(artist) + '::' + norm(title);
  if (mem.has(key)) return mem.get(key);
  if (store[key]) { mem.set(key, store[key]); return store[key]; }

  let hit = await search(`artist:"${artist}" track:"${title}"`);
  if (!hit) hit = await search(`${artist} ${title}`);

  const out = {};
  if (hit) {
    const t = norm(title), ht = norm(hit.title || '');
    if (!t || !ht || t.includes(ht) || ht.includes(t)) {
      if (hit.preview) out.preview = hit.preview;
      const cover = hit.album && (hit.album.cover_big || hit.album.cover_medium || hit.album.cover);
      if (cover) out.cover = cover;
    }
  }
  mem.set(key, out);
  store[key] = out;
  persist();
  return out;
}
