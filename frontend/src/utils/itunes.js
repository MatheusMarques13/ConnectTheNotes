// Runtime media (cover art + 30s audio preview) from the iTunes Search API.
//
// Replaces utils/deezer.js. Two reasons, both blocking for a commercial build:
//
//   Licence — Deezer's developer terms limit use to "a non-commercial purpose
//   and in a non-commercial environment", forbid generating data from the
//   content, and forbid associating it with a brand or logo.
//
//   Expiry — Deezer preview URLs are signed (`?hdnea=exp=...`) and die about
//   15 minutes after issue, so they can never be baked into the bundle. The
//   iTunes URLs carry no token and cache like any static asset.
//
// Same shape as the module it replaces: JSONP so a static site needs no CORS
// proxy, memoised in memory and localStorage so each song is looked up once
// per device.
const norm = (s) =>
  (s || '').normalize('NFKD').replace(/[̀-ͯ]/g, '').toLowerCase().replace(/[^a-z0-9]/g, '');

const mem = new Map();
const artistMem = new Map();
const LS_KEY = 'ctn_media_v2';
let store = {};
try { store = JSON.parse(localStorage.getItem(LS_KEY) || '{}'); } catch (e) { store = {}; }
let persistTimer = 0;
const persist = () => {
  clearTimeout(persistTimer);
  persistTimer = setTimeout(() => {
    try { localStorage.setItem(LS_KEY, JSON.stringify(store)); } catch (e) { /* quota */ }
  }, 800);
};

function jsonp(url) {
  return new Promise((resolve) => {
    const cb = 'ctn_it_' + Math.random().toString(36).slice(2);
    const s = document.createElement('script');
    let done = false;
    const cleanup = () => {
      if (done) return;
      done = true;
      clearTimeout(timer);
      delete window[cb];
      if (s.parentNode) s.parentNode.removeChild(s);
    };
    const timer = setTimeout(() => { cleanup(); resolve(null); }, 7000);
    window[cb] = (data) => { cleanup(); resolve(data); };
    s.onerror = () => { cleanup(); resolve(null); };
    s.src = `${url}${url.includes('?') ? '&' : '?'}callback=${cb}`;
    document.head.appendChild(s);
  });
}

// Artwork comes back as a 100x100 thumbnail; the same path serves any size.
const artwork = (url, px) => (url ? url.replace(/\/\d+x\d+bb\./, `/${px}x${px}bb.`) : '');

const search = async (params) => {
  const qs = new URLSearchParams({ ...params, limit: params.limit || '1' }).toString();
  const data = await jsonp(`https://itunes.apple.com/search?${qs}`);
  return (data && data.results) || [];
};

// A loose title match keeps "Work" matching "Work (feat. Drake)" while still
// rejecting an unrelated song that merely shares a word.
const titleMatches = (want, got) => {
  const a = norm(want);
  const b = norm(got);
  return !a || !b || a.includes(b) || b.includes(a);
};

/**
 * Artist photo stand-in.
 *
 * The iTunes Search API exposes no artist portrait — `entity=musicArtist`
 * returns names and genres only — so this falls back to the artist's album
 * artwork. Callers already handle an empty result with initials.
 *
 * @param {string} name
 * @param {number} [px]
 * @returns {Promise<string|null>}
 */
export async function getArtistImage(name, px = 400) {
  const key = 'art::' + norm(name);
  if (artistMem.has(key)) return artistMem.get(key);
  if (key in store) { artistMem.set(key, store[key]); return store[key]; }

  const results = await search({ term: name, entity: 'album', attribute: 'artistTerm', limit: '3' });
  let url = null;
  for (const r of results) {
    const a = norm(name);
    const b = norm(r.artistName || '');
    if (a && b && (a === b || a.includes(b) || b.includes(a))) {
      url = artwork(r.artworkUrl100, px);
      if (url) break;
    }
  }
  artistMem.set(key, url);
  store[key] = url;
  persist();
  return url;
}

/**
 * Cover art and audio preview for a track.
 *
 * @param {string} title
 * @param {string} artist
 * @returns {Promise<{preview?: string, cover?: string}>} empty when nothing matches
 */
export async function getSongMedia(title, artist) {
  const key = norm(artist) + '::' + norm(title);
  if (mem.has(key)) return mem.get(key);
  if (store[key]) { mem.set(key, store[key]); return store[key]; }

  let hits = await search({ term: `${artist} ${title}`, entity: 'song', limit: '5' });
  if (!hits.length) hits = await search({ term: title, entity: 'song', limit: '5' });

  const out = {};
  for (const hit of hits) {
    if (!titleMatches(title, hit.trackName)) continue;
    if (hit.previewUrl) out.preview = hit.previewUrl;
    const cover = artwork(hit.artworkUrl100, 600);
    if (cover) out.cover = cover;
    if (out.preview) break;
  }

  mem.set(key, out);
  store[key] = out;
  persist();
  return out;
}
