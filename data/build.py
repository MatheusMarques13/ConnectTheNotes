"""Build & validate the shipped game dataset.

Reads the human-editable source (data/source_data.py) and writes the browser
dataset at frontend/src/data/dataset.js.

A SONG is the node that links artists: every collaboration row sharing the same
(title, type, year) is merged into ONE song crediting ALL its artists, so a
track with 3+ collaborators connects all of them. The build asserts the graph is
a single connected component (every puzzle solvable) and fails loudly otherwise.

Run:  python data/build.py
"""
import json
import os
import sys
from collections import deque, OrderedDict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from source_data import ARTISTS, COLLABORATIONS  # noqa: E402

OUT = os.path.join(HERE, "..", "frontend", "src", "data", "dataset.js")


def slug(n):
    return f"a{n}"


def build():
    artists = [{"id": slug(i), "name": n, "genre": g, "imageUrl": ""} for (i, n, g) in ARTISTS]
    by_id = {a["id"]: a for a in artists}

    # Merge collaborations that are the same track (title, type, year) into one
    # song crediting every artist on it.
    grouped = OrderedDict()  # (title, type, year) -> ordered set of artist slugs
    for a1, a2, title, ctype, year in COLLABORATIONS:
        s1, s2 = slug(a1), slug(a2)
        if s1 not in by_id or s2 not in by_id or s1 == s2:
            continue
        key = (title, ctype, year)
        members = grouped.setdefault(key, OrderedDict())
        members[s1] = True
        members[s2] = True

    songs = []
    for (title, ctype, year), members in grouped.items():
        ids = list(members.keys())
        if len(ids) < 2:
            continue
        songs.append({
            "id": f"s{len(songs)}",
            "title": title,
            "type": ctype,
            "year": year,
            "coverUrl": "",
            "artists": ids,
        })
    return artists, songs


def assert_single_component(artists, songs):
    adj = {a["id"]: set() for a in artists}
    for s in songs:
        for x in s["artists"]:
            for y in s["artists"]:
                if x != y:
                    adj[x].add(y)
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


def write_js(artists, songs):
    sep = (",", ": ")
    lines = [
        "// AUTO-GENERATED from data/source_data.py via data/build.py",
        "// Songs link artists; a track with N collaborators connects all of them.",
        "// Single connected component -> every artist pair is solvable.",
        "// Do not edit by hand; regenerate instead.",
        "",
        "export const ARTISTS = " + json.dumps(artists, ensure_ascii=False, separators=sep) + ";",
        "",
        "export const SONGS = " + json.dumps(songs, ensure_ascii=False, separators=sep) + ";",
        "",
    ]
    with open(OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


if __name__ == "__main__":
    artists, songs = build()
    assert_single_component(artists, songs)
    write_js(artists, songs)
    multi = sum(1 for s in songs if len(s["artists"]) > 2)
    print(f"✅ {len(artists)} artists, {len(songs)} songs ({multi} with 3+ artists) — single connected component verified")
    print(f"   wrote {os.path.relpath(OUT, os.path.join(HERE, '..'))}")
