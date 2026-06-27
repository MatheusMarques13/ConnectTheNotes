// Build-time image fetcher: looks up each artist's photo on the free Deezer API
// and bakes the URLs into src/data/images.generated.js, so the app shows real
// photos with no runtime API calls or CORS issues.
//
// Runs as part of `yarn build` (see package.json). It NEVER fails the build:
// any network/parse error just leaves that artist without a photo (the UI falls
// back to a styled initials avatar).
import { readFile, writeFile } from "node:fs/promises";

const DATASET = new URL("../src/data/dataset.js", import.meta.url);
const OUTPUT = new URL("../src/data/images.generated.js", import.meta.url);
// Deezer rate-limits to ~50 requests / 5s, so keep concurrency low, pace each
// request, and retry on a quota error.
const CONCURRENCY = 3;
const PACE_MS = 150;
const TIMEOUT_MS = 8000;

const norm = (s) => s.toLowerCase().replace(/[^a-z0-9]/g, "");
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

async function artistNames() {
  const text = await readFile(DATASET, "utf8");
  const start = text.indexOf("export const ARTISTS = ");
  const json = text.slice(start + "export const ARTISTS = ".length, text.indexOf(";", start));
  return JSON.parse(json).map((a) => a.name);
}

async function deezerSearch(name) {
  const ctrl = new AbortController();
  const timer = setTimeout(() => ctrl.abort(), TIMEOUT_MS);
  try {
    const res = await fetch(
      `https://api.deezer.com/search/artist?q=${encodeURIComponent(name)}&limit=1`,
      { signal: ctrl.signal, headers: { "User-Agent": "connect-the-notes" } }
    );
    if (!res.ok) { const e = new Error(`http ${res.status}`); e.retry = res.status === 429; throw e; }
    const data = await res.json();
    if (data?.error) { const e = new Error(data.error.message || "deezer error"); e.retry = data.error.code === 4; throw e; }
    return data?.data?.[0] || null;
  } finally {
    clearTimeout(timer);
  }
}

async function fetchImage(name) {
  for (let attempt = 0; attempt < 4; attempt++) {
    try {
      const hit = await deezerSearch(name);
      if (!hit) return null;
      // Guard against a wildly wrong match.
      const a = norm(name), b = norm(hit.name || "");
      if (!(a === b || a.includes(b) || b.includes(a))) return null;
      const url = hit.picture_xl || hit.picture_big || hit.picture_medium || "";
      // Deezer returns a placeholder with an empty id ("/artist//...") when the
      // artist has no photo — treat that as "no image".
      if (!url || url.includes("/artist//")) return null;
      return url;
    } catch (e) {
      if (e.retry && attempt < 3) { await sleep(1200 + attempt * 1000); continue; }
      return null;
    }
  }
  return null;
}

async function run() {
  let names;
  try {
    names = await artistNames();
  } catch (e) {
    console.warn("[images] could not read dataset, skipping:", e.message);
    await writeFile(OUTPUT, "export const ARTIST_IMAGES = {};\n");
    return;
  }

  const images = {};
  let i = 0, ok = 0;
  async function worker() {
    while (i < names.length) {
      const name = names[i++];
      const url = await fetchImage(name);
      if (url) { images[name] = url; ok++; }
      await sleep(PACE_MS); // respect Deezer's rate limit
    }
  }
  await Promise.all(Array.from({ length: CONCURRENCY }, worker));

  const body =
    "// AUTO-GENERATED at build time by scripts/fetch-images.mjs — do not edit.\n" +
    "export const ARTIST_IMAGES = " + JSON.stringify(images, null, 0) + ";\n";
  await writeFile(OUTPUT, body);
  console.log(`[images] resolved ${ok}/${names.length} artist photos`);
}

run().catch(async (e) => {
  console.warn("[images] fetch step failed, continuing without photos:", e?.message);
  try { await writeFile(OUTPUT, "export const ARTIST_IMAGES = {};\n"); } catch {}
  // Never break the build.
  process.exit(0);
});
