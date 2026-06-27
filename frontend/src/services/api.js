// Client-side game engine — the whole game is a small static graph, so there is
// no backend at runtime. These functions keep the same names/shapes the app
// already expects, but compute everything locally from the embedded dataset.
import { ARTISTS, CONNECTIONS } from '../data/dataset';

// ── Indexes ─────────────────────────────────────────────
const ARTISTS_BY_ID = {};
ARTISTS.forEach((a) => { ARTISTS_BY_ID[a.id] = a; });

const ADJ = {}; // id -> [{ to, song }]
CONNECTIONS.forEach((c) => {
  if (!ADJ[c.artist1]) ADJ[c.artist1] = [];
  if (!ADJ[c.artist2]) ADJ[c.artist2] = [];
  ADJ[c.artist1].push({ to: c.artist2, song: c.song });
  ADJ[c.artist2].push({ to: c.artist1, song: c.song });
});
const ARTIST_IDS = ARTISTS.map((a) => a.id);

const DIFFICULTY_BANDS = { easy: [2, 3], medium: [3, 4], hard: [4, 7], any: [2, 7] };

const normSong = (s = {}) => ({
  title: s.title || 'Unknown',
  type: s.type || 'song',
  year: s.year || 2024,
  coverUrl: s.coverUrl || '',
});

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

export async function getConnectedArtists(artistId) {
  const ids = new Set();
  for (const { to } of ADJ[artistId] || []) ids.add(to);
  return [...ids].map((id) => ARTISTS_BY_ID[id]).filter(Boolean);
}

// Every song the artist appears on, with the collaborator resolved — this is
// what the player browses to travel through the music web.
export async function getArtistSongs(artistId) {
  return CONNECTIONS
    .filter((c) => c.artist1 === artistId || c.artist2 === artistId)
    .map((c) => {
      const otherId = c.artist1 === artistId ? c.artist2 : c.artist1;
      const collaborator = ARTISTS_BY_ID[otherId];
      if (!collaborator) return null;
      return {
        id: c.id,
        title: c.song.title,
        type: c.song.type,
        year: c.song.year,
        coverUrl: c.song.coverUrl || '',
        collaborator,
      };
    })
    .filter(Boolean)
    .sort((a, b) =>
      a.collaborator.name.localeCompare(b.collaborator.name) || a.title.localeCompare(b.title)
    );
}

export async function getCollaborationsBetween(id1, id2) {
  return CONNECTIONS
    .filter((c) => (c.artist1 === id1 && c.artist2 === id2) || (c.artist1 === id2 && c.artist2 === id1))
    .map((c) => ({
      id: c.id,
      title: c.song.title,
      type: c.song.type,
      year: c.song.year,
      artistIds: [c.artist1, c.artist2],
      coverUrl: c.song.coverUrl || '',
    }));
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
  return { totalArtists: ARTISTS.length, totalConnections: CONNECTIONS.length };
}
