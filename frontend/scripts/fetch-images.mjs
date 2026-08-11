// Build-time media step: bakes the artist photos we already have into
// src/data/images.generated.js. It makes no network calls.
//
// It used to search the Deezer API for every artist without a preset, under an
// 18-minute deadline. That went away for two reasons:
//
//   Licence — Deezer's developer terms restrict use to "a non-commercial
//   purpose and in a non-commercial environment" and forbid generating data
//   from the content. A build that harvests URLs into a committed artefact is
//   squarely inside that.
//
//   Determinism — the search was racing a deadline, so the same commit
//   produced different output depending on how fast the API answered that day.
//
// Anything without a preset photo now resolves at runtime through
// utils/itunes.js, cached per device, and falls back to a styled initials
// avatar. The iTunes Search API caps around 20 requests/minute, so baking
// 5,625 artists here was never an option anyway — it would take ~4.7 hours.
//
// STILL OPEN: the preset URLs in data/artist_images.json point at Deezer's CDN
// and were themselves derived from the Deezer API. Replacing them needs a
// licence-clean source for artist photography (Wikidata/Wikimedia Commons is
// the obvious candidate) — see tools/artist_images.py.
import { readFile, writeFile } from "node:fs/promises";

const DATASET = new URL("../src/data/dataset.js", import.meta.url);
const OUTPUT = new URL("../src/data/images.generated.js", import.meta.url);
const PRESET = new URL("../../data/artist_images.json", import.meta.url);

// dataset.js ships positional rows to keep the payload small:
//   const A = [[1,"Drake","Hip-Hop/R&B",943], ...]
// so read the raw rows rather than the rehydrated ARTISTS export, which is a
// computed expression and not parseable as JSON.
function artistRows(text) {
  const marker = "const A = ";
  const start = text.indexOf(marker);
  if (start < 0) return [];
  const end = text.indexOf("];", start);
  if (end < 0) return [];
  try {
    return JSON.parse(text.slice(start + marker.length, end + 1));
  } catch {
    return [];
  }
}

async function run() {
  const text = await readFile(DATASET, "utf8");
  const rows = artistRows(text);
  if (!rows.length) throw new Error("could not parse artist rows from dataset.js");

  const nameById = new Map(rows.map(([id, name]) => [String(id), name]));

  let preset = {};
  try {
    preset = JSON.parse(await readFile(PRESET, "utf8"));
  } catch {
    preset = {};                       // absent -> everything resolves at runtime
  }

  const images = {};
  for (const [id, url] of Object.entries(preset)) {
    const name = nameById.get(String(id));
    if (name && url) images[name] = url;
  }

  const body =
    "// AUTO-GENERATED at build time by scripts/fetch-images.mjs — do not edit.\n" +
    "export const ARTIST_IMAGES = " + JSON.stringify(images) + ";\n" +
    "export const SONG_COVERS = {};\n" +
    "export const SONG_PREVIEWS = {};\n";
  await writeFile(OUTPUT, body);

  console.log(
    `[images] ${Object.keys(images).length}/${rows.length} artist photos from ` +
    `preset; the rest resolve at runtime via iTunes (no network calls here)`,
  );
}

run().catch(async (e) => {
  console.warn("[images] step failed, continuing without media:", e?.message);
  try {
    await writeFile(
      OUTPUT,
      "export const ARTIST_IMAGES = {};\nexport const SONG_COVERS = {};\nexport const SONG_PREVIEWS = {};\n",
    );
  } catch {}
  process.exit(0);
});
