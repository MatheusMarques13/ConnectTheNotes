// Client-side game engine. The game is a small static graph, so there is no
// backend at runtime — everything is computed locally from the embedded dataset.
// A SONG links artists: a track with N collaborators connects all of them.
import { ARTISTS, SONGS } from '../data/dataset';
import { ARTIST_IMAGES, SONG_COVERS, SONG_PREVIEWS } from '../data/images.generated';

// ── Indexes ─────────────────────────────────────────────
const ARTISTS_BY_ID = {};
ARTISTS.forEach((a) => { ARTISTS_BY_ID[a.id] = a; });

// adjacency: artist_id -> [{ to, song }] for every co-credit on every shared song
const ADJ = {};
for (const s of SONGS) {
  const song = { id: s.id, title: s.title, type: s.type, year: s.year, coverUrl: s.coverUrl };
  for (const a of s.artists) {
    for (const b of s.artists) {
      if (a === b) continue;
      if (!ADJ[a]) ADJ[a] = [];
      ADJ[a].push({ to: b, song });
    }
  }
}
const ARTIST_IDS = ARTISTS.map((a) => a.id);

const DIFFICULTY_BANDS = { easy: [2, 3], medium: [3, 4], hard: [4, 7], any: [2, 7] };

const songCover = (s) => SONG_COVERS[s.id] || s.coverUrl || '';
const songPreview = (s) => (s && s.id != null ? SONG_PREVIEWS[s.id] : '') || '';
const songObj = (s) => ({ id: s.id, title: s.title, type: s.type, year: s.year, coverUrl: songCover(s), previewUrl: songPreview(s) });
const normSong = (s = {}) => ({
  id: s.id,
  title: s.title || 'Unknown',
  type: s.type || 'song',
  year: s.year || 2024,
  coverUrl: songCover(s),
  previewUrl: songPreview(s),
});

// Levenshtein edit distance (tiny strings) — for "did you mean…?" suggestions.
function lev(a, b) {
  const m = a.length, n = b.length;
  if (!m) return n; if (!n) return m;
  let prev = Array.from({ length: n + 1 }, (_, i) => i);
  for (let i = 1; i <= m; i++) {
    let cur = [i];
    for (let j = 1; j <= n; j++) {
      const cost = a[i - 1] === b[j - 1] ? 0 : 1;
      cur[j] = Math.min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + cost);
    }
    prev = cur;
  }
  return prev[n];
}

// ── Graph traversal ─────────────────────────────────────
function bfsSteps(start, end) {
  if (start === end) return [];
  const visited = new Set([start]);
  const queue = [[start, []]];
  let qi = 0;
  while (qi < queue.length) {
    const [cur, path] = queue[qi++];
    for (const { to, song } of ADJ[cur] || []) {
      const step = { fromArtist: cur, song, toArtist: to };
      if (to === end) return [...path, step];
      if (!visited.has(to)) {
        visited.add(to);
        queue.push([to, [...path, step]]);
      }
    }
  }
  return null;
}

function bfsDistances(start) {
  const dist = { [start]: 0 };
  const queue = [start];
  let qi = 0;
  while (qi < queue.length) {
    const cur = queue[qi++];
    for (const { to } of ADJ[cur] || []) {
      if (!(to in dist)) { dist[to] = dist[cur] + 1; queue.push(to); }
    }
  }
  return dist;
}

// ── Deterministic RNG (for the daily puzzle) ────────────
function xmur3(str) {
  let h = 1779033703 ^ str.length;
  for (let i = 0; i < str.length; i++) {
    h = Math.imul(h ^ str.charCodeAt(i), 3432918353);
    h = (h << 13) | (h >>> 19);
  }
  return () => {
    h = Math.imul(h ^ (h >>> 16), 2246822507);
    h = Math.imul(h ^ (h >>> 13), 3266489909);
    h ^= h >>> 16;
    return h >>> 0;
  };
}
function mulberry32(a) {
  return () => {
    a |= 0; a = (a + 0x6d2b79f5) | 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}
const seededRng = (str) => mulberry32(xmur3(str)());

const choice = (rng, arr) => arr[Math.floor(rng() * arr.length)];

function pickPairInBand(rng, lo, hi) {
  for (let i = 0; i < 60; i++) {
    const start = choice(rng, ARTIST_IDS);
    const dist = bfsDistances(start);
    const candidates = Object.keys(dist).filter((id) => dist[id] >= lo && dist[id] <= hi);
    if (candidates.length) {
      const end = choice(rng, candidates);
      return { start, end, dist: dist[end] };
    }
  }
  const start = choice(rng, ARTIST_IDS);
  const dist = bfsDistances(start);
  const far = Object.keys(dist).filter((id) => dist[id] >= 2);
  if (far.length) { const end = choice(rng, far); return { start, end, dist: dist[end] }; }
  return null;
}

// ── Public API (async to match existing callers) ────────
export async function searchArtists(query, limit = 8) {
  if (!query || query.length < 1) return [];
  const q = query.toLowerCase();
  return ARTISTS.filter((a) => a.name.toLowerCase().includes(q)).slice(0, limit);
}

export async function getRandomArtist(excludeIds = []) {
  const ex = new Set(excludeIds);
  const pool = ARTISTS.filter((a) => !ex.has(a.id));
  return pool.length ? pool[Math.floor(Math.random() * pool.length)] : null;
}

export async function getArtistById(id) {
  return ARTISTS_BY_ID[id] || null;
}

// Every song the artist is on, each carrying ALL its other collaborators —
// so a track with 2+ guests lets the player reach any of them.
export async function getArtistSongs(artistId) {
  const out = [];
  for (const s of SONGS) {
    if (!s.artists.includes(artistId)) continue;
    const collaborators = s.artists
      .filter((id) => id !== artistId)
      .map((id) => ARTISTS_BY_ID[id])
      .filter(Boolean);
    if (!collaborators.length) continue;
    out.push({ id: s.id, title: s.title, type: s.type, year: s.year, coverUrl: songCover(s), collaborators });
  }
  out.sort((a, b) =>
    (a.collaborators[0]?.name || '').localeCompare(b.collaborators[0]?.name || '') ||
    a.title.localeCompare(b.title)
  );
  return out;
}

// Recall move for the "web" mode: the player types a song title; we match it
// against every song that credits at least one artist they've already found,
// and return the song with ALL of its credited artists (so multi-feature tracks
// reveal everyone). Returns null if nothing real matches.
const normTitle = (s) => (s || '').toLowerCase().replace(/[^a-z0-9]/g, '');

export async function nameSong(foundIds, typed) {
  const set = new Set(foundIds);
  const nq = normTitle(typed);
  if (nq.length < 2) return null;
  const candidates = SONGS.filter((s) => s.artists.some((a) => set.has(a)));
  const exact = candidates.filter((s) => normTitle(s.title) === nq);
  const partial = candidates.filter((s) => {
    const nt = normTitle(s.title);
    return nt.includes(nq) || (nq.length >= 4 && nq.includes(nt) && nt.length >= 4);
  });
  const pool = exact.length ? exact : partial;
  if (pool.length) {
    const s = pool[0];
    return { song: songObj(s), artists: s.artists.map((id) => ARTISTS_BY_ID[id]).filter(Boolean) };
  }
  // Near-miss: the player typed it ALMOST right (a few letters off) — suggest
  // the real title with a "did you mean…?" so they can confirm.
  let best = null, bestD = Infinity;
  for (const s of candidates) {
    const nt = normTitle(s.title);
    if (!nt || Math.abs(nt.length - nq.length) > 3) continue;
    const d = lev(nq, nt);
    if (d < bestD) { bestD = d; best = s; }
  }
  const tol = nq.length <= 5 ? 1 : nq.length <= 9 ? 2 : 3;
  if (best && bestD <= tol) return { suggestion: best.title };
  return null;
}

// Returns { steps, chain, optimalSteps }. steps === null => unreachable.
export async function findConnection(startId, endId) {
  if (startId === endId) return { steps: [], chain: [], optimalSteps: 0 };
  const raw = bfsSteps(startId, endId);
  if (raw === null) return { steps: null, chain: null, optimalSteps: null };
  const steps = raw.map((s) => ({ fromArtist: s.fromArtist, toArtist: s.toArtist, collab: normSong(s.song) }));
  const chain = [{ artist: ARTISTS_BY_ID[startId], collab: null }];
  for (const s of raw) chain.push({ artist: ARTISTS_BY_ID[s.toArtist], collab: normSong(s.song) });
  return { steps, chain, optimalSteps: steps.length };
}

export async function getRandomPair(difficulty = 'any') {
  const [lo, hi] = DIFFICULTY_BANDS[difficulty] || DIFFICULTY_BANDS.any;
  const p = pickPairInBand(Math.random, lo, hi);
  if (!p) return null;
  return { artist1: ARTISTS_BY_ID[p.start], artist2: ARTISTS_BY_ID[p.end], optimalSteps: p.dist };
}

export async function getDailyPuzzle(dateStr) {
  const day = dateStr || new Date().toISOString().slice(0, 10);
  const [lo, hi] = DIFFICULTY_BANDS.medium;
  const p = pickPairInBand(seededRng(day), lo, hi);
  if (!p) return null;
  return { date: day, artist1: ARTISTS_BY_ID[p.start], artist2: ARTISTS_BY_ID[p.end], optimalSteps: p.dist };
}

export async function getStats() {
  return { totalArtists: ARTISTS.length, totalSongs: SONGS.length };
}
