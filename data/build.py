"""Build & validate the shipped game dataset.

Reads the human-editable source (data/source_data.py), builds the artist/
connection graph, asserts it is a single connected component (so every puzzle is
solvable), and writes the browser dataset at frontend/src/data/dataset.js.

Run:  python data/build.py
It fails loudly if the source graph is ever split into multiple components.
"""
import json
import os
import sys
from collections import deque

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from source_data import ARTISTS, COLLABORATIONS  # noqa: E402

OUT = os.path.join(HERE, "..", "frontend", "src", "data", "dataset.js")


def slug(n):
    return f"a{n}"


def build():
    artists = [{"id": slug(i), "name": n, "genre": g, "imageUrl": ""} for (i, n, g) in ARTISTS]
    by_id = {a["id"]: a for a in artists}

    connections = []
    seen = set()
    for a1, a2, title, ctype, year in COLLABORATIONS:
        s1, s2 = slug(a1), slug(a2)
        if s1 not in by_id or s2 not in by_id or s1 == s2:
            continue
        key = (min(a1, a2), max(a1, a2), title)
        if key in seen:
            continue
        seen.add(key)
        connections.append({
            "id": f"c{len(connections)}",
            "artist1": s1,
            "artist2": s2,
            "song": {"title": title, "type": ctype, "year": year, "coverUrl": ""},
        })
    return artists, connections


def assert_single_component(artists, connections):
    adj = {a["id"]: set() for a in artists}
    for c in connections:
        adj[c["artist1"]].add(c["artist2"])
        adj[c["artist2"]].add(c["artist1"])
    start = artists[0]["id"]
    seen = {start}
    queue = deque([start])
    while queue:
        x = queue.popleft()
        for y in adj[x]:
            if y not in seen:
                seen.add(y)
                queue.append(y)
    if len(seen) != len(artists):
        unreachable = sorted(a["id"] for a in artists if a["id"] not in seen)
        raise SystemExit(
            f"❌ Dataset is NOT a single connected component: "
            f"{len(unreachable)} artist(s) unreachable -> {unreachable}.\n"
            f"   Every pair must be solvable. Fix data/source_data.py."
        )


def write_js(artists, connections):
    sep = (",", ": ")  # compact: no space after commas, space after colons
    lines = [
        "// AUTO-GENERATED from data/source_data.py via data/build.py",
        "// Single connected component -> every artist pair is solvable.",
        "// Do not edit by hand; regenerate instead.",
        "",
        "export const ARTISTS = " + json.dumps(artists, ensure_ascii=False, separators=sep) + ";",
        "",
        "export const CONNECTIONS = " + json.dumps(connections, ensure_ascii=False, separators=sep) + ";",
        "",
    ]
    with open(OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


if __name__ == "__main__":
    artists, connections = build()
    assert_single_component(artists, connections)
    write_js(artists, connections)
    print(f"✅ {len(artists)} artists, {len(connections)} connections — single connected component verified")
    print(f"   wrote {os.path.relpath(OUT, os.path.join(HERE, '..'))}")
