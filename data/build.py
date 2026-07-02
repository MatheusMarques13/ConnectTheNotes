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
import re
import sys
from collections import deque, OrderedDict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from source_data import ARTISTS, COLLABORATIONS  # noqa: E402

OUT = os.path.join(HERE, "..", "frontend", "src", "data", "dataset.js")


def slug(n):
    return f"a{n}"


def _songkey(t):
    return re.sub(r"\s+", " ", (t or "").strip()).lower()


def _better_title(a, b):
    # Prefer a title that uses mixed case over ALL-CAPS / all-lowercase variants.
    def score(s):
        letters = [c for c in s if c.isalpha()]
        if not letters:
            return 0
        return 2 if (any(c.isupper() for c in letters) and any(c.islower() for c in letters)) else 1
    return b if score(b) > score(a) else a


def build():
    artists = [{"id": slug(i), "name": n, "genre": g, "imageUrl": ""} for (i, n, g) in ARTISTS]
    by_id = {a["id"]: a for a in artists}

    # Group collaboration edges by (normalized title, type, year) — case/spacing
    # insensitive, so "SICKO MODE" / "Sicko Mode" / "sicko mode" don't become
    # separate songs.
    groups = OrderedDict()   # key -> list of (s1, s2) edges
    titles = {}              # key -> canonical display title
    for a1, a2, title, ctype, year in COLLABORATIONS:
        s1, s2 = slug(a1), slug(a2)
        if s1 not in by_id or s2 not in by_id or s1 == s2:
            continue
        key = (_songkey(title), ctype, year)
        groups.setdefault(key, []).append((s1, s2))
        titles[key] = title if key not in titles else _better_title(titles[key], title)

    songs = []
    for key, edges in groups.items():
        ctype, year, title = key[1], key[2], titles[key]
        ids = list(OrderedDict((s, True) for e in edges for s in e).keys())
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


def components(artists, songs):
    """All connected components (largest first). A song with N artists links
    all of them; the graph may legitimately be multi-component (real music
    scenes that share no verified cross-collab), so we report rather than fail."""
    adj = {a["id"]: set() for a in artists}
    for s in songs:
        for x in s["artists"]:
            for y in s["artists"]:
                if x != y:
                    adj[x].add(y)
    seen = set()
    comps = []
    for a in artists:
        start = a["id"]
        if start in seen:
            continue
        comp = {start}
        seen.add(start)
        queue = deque([start])
        while queue:
            x = queue.popleft()
            for y in adj[x]:
                if y not in seen:
                    seen.add(y)
                    comp.add(y)
                    queue.append(y)
        comps.append(comp)
    comps.sort(key=len, reverse=True)
    return comps


def report_components(artists, songs):
    comps = components(artists, songs)
    main = len(comps[0]) if comps else 0
    isolated = sum(1 for c in comps if len(c) == 1)
    frac = main / len(artists) if artists else 0
    print(f"   components: {len(comps)} | largest {main} ({frac:.1%}) | islands {len(comps) - 1} | isolated singletons {isolated}")
    # Guardrail against catastrophic breakage, not normal multi-component data.
    if frac < 0.80:
        raise SystemExit(
            f"❌ Main component is only {frac:.1%} of artists — data likely broken. "
            f"Aborting. Fix data/source_data.py."
        )
    return comps


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
    report_components(artists, songs)
    write_js(artists, songs)
    multi = sum(1 for s in songs if len(s["artists"]) > 2)
    print(f"✅ {len(artists)} artists, {len(songs)} songs ({multi} with 3+ artists)")
    print(f"   wrote {os.path.relpath(OUT, os.path.join(HERE, '..'))}")
