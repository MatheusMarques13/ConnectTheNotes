"""Generate frontend/src/data/dataset.js from the Python store (single source
of truth), so the client-side game uses the exact same graph that the backend
tests validate."""
import os, sys, json
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "backend"))
import store

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "frontend", "src", "data", "dataset.js")

artists = store.ARTIST_LIST
conns = store.CONNECTIONS

lines = []
lines.append("// AUTO-GENERATED from backend/seed_data.py via scripts/gen_dataset_js.py")
lines.append("// 95 artists in a single connected component → every pair is solvable.")
lines.append("// Do not edit by hand; regenerate instead.")
lines.append("")
lines.append("export const ARTISTS = " + json.dumps(artists, ensure_ascii=False, indent=0).replace("\n", "") + ";")
lines.append("")
lines.append("export const CONNECTIONS = " + json.dumps(conns, ensure_ascii=False, indent=0).replace("\n", "") + ";")
lines.append("")
open(OUT, "w", encoding="utf-8").write("\n".join(lines))
print(f"Wrote {OUT}: {len(artists)} artists, {len(conns)} connections")
