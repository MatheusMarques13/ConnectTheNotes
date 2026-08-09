// Build-time media fetcher: looks up each artist's photo and each song's cover
// art on the free Deezer API and bakes the URLs into src/data/images.generated.js,
// so the app shows real images with no runtime API calls or CORS issues.
//
// Runs as part of `yarn build`. It NEVER fails the build: any network/parse
// error just leaves that item without an image (the UI uses a fallback).
import { readFile, writeFile } from "node:fs/promises";

const DATASET = new URL("../src/data/dataset.js", import.meta.url);
const OUTPUT = new URL("../src/data/images.generated.js", import.meta.url);
const PRESET = new URL("../../data/artist_images.json", import.meta.url);
const CONCURRENCY = 5;
const PACE_MS = 110;
const TIMEOUT_MS = 8000;
// Hard cap on total media-fetch time so a 5k-artist / 12k-song dataset can never
// stall the Vercel build. Whatever isn't fetched in time just uses the fallback.
const DEADLINE_MS = 18 * 60 * 1000;

// Accent-insensitive so our "Celine Dion" matches Deezer's "Céline Dion"
// (folds é->e etc. instead of deleting the accented char).
const norm = (s) => s.normalize("NFKD").replace(/[̀-ͯ]/g, "").toLowerCase().replace(/[^a-z0-9]/g, "");
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

// One lookup gets both the cover art AND a 30s audio preview (Deezer's `preview`
// MP3). Returns { cover?, preview? } so adding songs auto-gets both.
const songMedia = (title, artistName) => withRetry(async () => {
  const q = `artist:"${artistName}" track:"${title}"`;
  const hits = await deezer(`search?q=${encodeURIComponent(q)}&limit=1`);
  const hit = hits[0];
  if (!hit) return null;
  const t = norm(title), ht = norm(hit.title || "");
  if (!(t.includes(ht) || ht.includes(t))) return null;
  const out = {};
  const cover = (hit.album && (hit.album.cover_big || hit.album.cover_medium)) || "";
  if (cover && !cover.includes("/cover//")) out.cover = cover;
  if (hit.preview) out.preview = hit.preview;
  return Object.keys(out).length ? out : null;
});

async function pacedMap(items, fetchOne, deadline) {
  const results = {};
  let i = 0, ok = 0;
  async function worker() {
    while (i < items.length && Date.now() < deadline) {
      const it = items[i++];
      const url = await fetchOne(it);
      if (url) { results[it.key] = url; ok++; }
      await sleep(PACE_MS);
    }
  }
  await Promise.all(Array.from({ length: CONCURRENCY }, worker));
  return { results, ok };
}

// Photos resolved once by exact Deezer artist id (tools/artist_images.py) and
// committed to the repo. Searching by name here missed a lot of artists — the
// top hit for a common name is often the wrong act, and every build re-did the
// whole list under a deadline. Anything in this file needs no lookup at all.
async function bakedByName(artists) {
  const out = {};
  let raw;
  try {
    raw = JSON.parse(await readFile(PRESET, "utf8"));
  } catch {
    return out;                       // file absent -> fall back to searching
  }
  const nameById = new Map(artists.map((a) => [a.id, a.name]));
  for (const [id, url] of Object.entries(raw)) {
    const name = nameById.get(`a${id}`);
    if (name && url) out[name] = url;
  }
  return out;
}

async function run() {
  const text = await readFile(DATASET, "utf8");
  const artists = sliceArray(text, "ARTISTS");

  // Only artist photos are baked at build time. Song covers + 30s previews are
  // fetched on demand at RUNTIME (Deezer JSONP), so the build no longer does
  // ~12k song lookups — this keeps the production build fast.
  const preset = await bakedByName(artists);
  const missing = artists.filter((a) => !preset[a.name]);
  const deadline = Date.now() + DEADLINE_MS;
  const images = await pacedMap(
    missing.map((a) => ({ key: a.name, name: a.name })),
    (t) => artistImage(t.name),
    deadline,
  );

  const merged = { ...preset, ...images.results };
  const body =
    "// AUTO-GENERATED at build time by scripts/fetch-images.mjs — do not edit.\n" +
    "export const ARTIST_IMAGES = " + JSON.stringify(merged) + ";\n" +
    "export const SONG_COVERS = {};\n" +
    "export const SONG_PREVIEWS = {};\n";
  await writeFile(OUTPUT, body);
  console.log(
    `[images] ${Object.keys(merged).length}/${artists.length} artist photos ` +
    `(${Object.keys(preset).length} preset by id, ${images.ok} searched by name)`,
  );
}

run().catch(async (e) => {
  console.warn("[images] fetch step failed, continuing without media:", e?.message);
  try { await writeFile(OUTPUT, "export const ARTIST_IMAGES = {};\nexport const SONG_COVERS = {};\nexport const SONG_PREVIEWS = {};\n"); } catch {}
  process.exit(0);
});
