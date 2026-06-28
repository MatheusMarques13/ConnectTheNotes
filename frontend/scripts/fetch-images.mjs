// Build-time media fetcher: looks up each artist's photo and each song's cover
// art on the free Deezer API and bakes the URLs into src/data/images.generated.js,
// so the app shows real images with no runtime API calls or CORS issues.
//
// Runs as part of `yarn build`. It NEVER fails the build: any network/parse
// error just leaves that item without an image (the UI uses a fallback).
import { readFile, writeFile } from "node:fs/promises";

const DATASET = new URL("../src/data/dataset.js", import.meta.url);
const OUTPUT = new URL("../src/data/images.generated.js", import.meta.url);
const CONCURRENCY = 3;
const PACE_MS = 140;
const TIMEOUT_MS = 8000;

const norm = (s) => s.toLowerCase().replace(/[^a-z0-9]/g, "");
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

function sliceArray(text, name) {
  const marker = `export const ${name} = `;
  const start = text.indexOf(marker);
  if (start < 0) return [];
  return JSON.parse(text.slice(start + marker.length, text.indexOf(";", start)));
}

async function deezer(path) {
  const ctrl = new AbortController();
  const timer = setTimeout(() => ctrl.abort(), TIMEOUT_MS);
  try {
    const res = await fetch(`https://api.deezer.com/${path}`, {
      signal: ctrl.signal,
      headers: { "User-Agent": "connect-the-notes" },
    });
    if (!res.ok) { const e = new Error(`http ${res.status}`); e.retry = res.status === 429; throw e; }
    const data = await res.json();
    if (data?.error) { const e = new Error(data.error.message || "deezer"); e.retry = data.error.code === 4; throw e; }
    return data?.data || [];
  } finally {
    clearTimeout(timer);
  }
}

async function withRetry(fn) {
  for (let attempt = 0; attempt < 4; attempt++) {
    try { return await fn(); }
    catch (e) { if (e.retry && attempt < 3) { await sleep(1200 + attempt * 1000); continue; } return null; }
  }
  return null;
}

const artistImage = (name) => withRetry(async () => {
  const hits = await deezer(`search/artist?q=${encodeURIComponent(name)}&limit=1`);
  const hit = hits[0];
  if (!hit) return null;
  const a = norm(name), b = norm(hit.name || "");
  if (!(a === b || a.includes(b) || b.includes(a))) return null;
  const url = hit.picture_xl || hit.picture_big || hit.picture_medium || "";
  return !url || url.includes("/artist//") ? null : url;
});

const songCover = (title, artistName) => withRetry(async () => {
  const q = `artist:"${artistName}" track:"${title}"`;
  const hits = await deezer(`search?q=${encodeURIComponent(q)}&limit=1`);
  const hit = hits[0];
  if (!hit?.album) return null;
  const t = norm(title), ht = norm(hit.title || "");
  if (!(t.includes(ht) || ht.includes(t))) return null;
  const url = hit.album.cover_big || hit.album.cover_medium || "";
  return !url || url.includes("/cover//") ? null : url;
});

async function pacedMap(items, fetchOne) {
  const results = {};
  let i = 0, ok = 0;
  async function worker() {
    while (i < items.length) {
      const it = items[i++];
      const url = await fetchOne(it);
      if (url) { results[it.key] = url; ok++; }
      await sleep(PACE_MS);
    }
  }
  await Promise.all(Array.from({ length: CONCURRENCY }, worker));
  return { results, ok };
}

async function run() {
  const text = await readFile(DATASET, "utf8");
  const artists = sliceArray(text, "ARTISTS");
  const songs = sliceArray(text, "SONGS");
  const nameById = Object.fromEntries(artists.map((a) => [a.id, a.name]));

  const artistTasks = artists.map((a) => ({ key: a.name, name: a.name }));
  const songTasks = songs.map((s) => ({ key: s.id, title: s.title, artist: nameById[s.artists[0]] || "" }));

  const images = await pacedMap(artistTasks, (t) => artistImage(t.name));
  const covers = await pacedMap(songTasks, (t) => songCover(t.title, t.artist));

  const body =
    "// AUTO-GENERATED at build time by scripts/fetch-images.mjs — do not edit.\n" +
    "export const ARTIST_IMAGES = " + JSON.stringify(images.results) + ";\n" +
    "export const SONG_COVERS = " + JSON.stringify(covers.results) + ";\n";
  await writeFile(OUTPUT, body);
  console.log(`[images] ${images.ok}/${artistTasks.length} artist photos, ${covers.ok}/${songTasks.length} song covers`);
}

run().catch(async (e) => {
  console.warn("[images] fetch step failed, continuing without media:", e?.message);
  try { await writeFile(OUTPUT, "export const ARTIST_IMAGES = {};\nexport const SONG_COVERS = {};\n"); } catch {}
  process.exit(0);
});
