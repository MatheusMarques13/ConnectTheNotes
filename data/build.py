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
import math
import os
import re
import sys
from collections import deque, OrderedDict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from source_data import ARTISTS, COLLABORATIONS  # noqa: E402

OUT = os.path.join(HERE, "..", "frontend", "src", "data", "dataset.js")
FAME_FILE = os.path.join(HERE, "artist_fame.json")
# How many artists the random pickers may draw from. Small enough that a random
# puzzle lands on a name players know; large enough that puzzles stay varied.
POOL_SIZE = 900


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


def fame_scores(artists, songs):
    """Score every artist 0..1000 for "would a player recognise this name?".

    Two signals, because neither works alone:
      * Deezer fan count (data/artist_fame.json, fetched by tools/artist_fame.py)
        is real audience size — the only thing that knows Linkin Park is famous
        despite barely doing features.
      * Collaboration degree is what makes an artist a good puzzle node, and is
        the only signal we have for artists Deezer could not match by name.

    Both are compressed with a log (fan counts are power-law: the top act has
    ~1000x the tail's followers, and a raw blend would make every puzzle Drake).
    """
    deg = {a["id"]: 0 for a in artists}
    adj = {a["id"]: set() for a in artists}
    for s in songs:
        for x in s["artists"]:
            for y in s["artists"]:
                if x != y:
                    adj[x].add(y)
    for k, v in adj.items():
        deg[k] = len(v)

    fans = {}
    if os.path.exists(FAME_FILE):
        with open(FAME_FILE, encoding="utf-8") as fh:
            raw = json.load(fh)
        fans = {slug(int(k)): v for k, v in raw.items() if v is not None}

    max_fan_l = max([math.log10(1 + v) for v in fans.values()], default=1.0) or 1.0
    max_deg_l = max([math.log(1 + d) for d in deg.values()], default=1.0) or 1.0

    scores = {}
    for a in artists:
        i = a["id"]
        d_l = math.log(1 + deg[i]) / max_deg_l
        if i in fans:
            f_l = math.log10(1 + fans[i]) / max_fan_l
            s = 0.72 * f_l + 0.28 * d_l
        else:
            # No confident Deezer match: fall back to graph prominence only, at a
            # discount so an unmatched name never outranks a verified star.
            s = 0.55 * d_l
        scores[i] = int(round(1000 * max(0.0, min(1.0, s))))
    return scores, deg, fans


def famous_pool(artists, scores, deg):
    """The ids the random pickers are allowed to draw from.

    Everything else stays fully playable (search, chains, solutions) — this only
    governs what a *random* puzzle or the shuffle button may land on.
    """
    eligible = [a["id"] for a in artists if deg.get(a["id"], 0) >= 2]
    eligible.sort(key=lambda i: -scores[i])
    return eligible[:POOL_SIZE]


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


def write_js(artists, songs, pool):
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
        "// Ids the random puzzle / shuffle may pick, best-known first. Every other",
        "// artist stays searchable and playable — this only steers randomness.",
        "export const FAMOUS_IDS = " + json.dumps(pool, ensure_ascii=False, separators=sep) + ";",
        "",
    ]
    with open(OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


if __name__ == "__main__":
    artists, songs = build()
    report_components(artists, songs)
    scores, deg, fans = fame_scores(artists, songs)
    for a in artists:
        a["fame"] = scores[a["id"]]
    pool = famous_pool(artists, scores, deg)
    write_js(artists, songs, pool)
    by_id = {a["id"]: a for a in artists}
    print(f"   fame: {len(fans)} artists with Deezer fan counts, "
          f"{len(artists) - len(fans)} graph-only | random pool {len(pool)}")
    print("   pool top 15: " + ", ".join(by_id[i]["name"] for i in pool[:15]))
    multi = sum(1 for s in songs if len(s["artists"]) > 2)
    print(f"✅ {len(artists)} artists, {len(songs)} songs ({multi} with 3+ artists)")
    print(f"   wrote {os.path.relpath(OUT, os.path.join(HERE, '..'))}")
