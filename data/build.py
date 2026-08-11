"""Build & validate the shipped game dataset.

Reads the human-editable source (data/source_data.py) and writes the browser
dataset at frontend/src/data/dataset.js.

A SONG is the node that links artists: every collaboration row sharing the same
(title, type, year) is merged into ONE song crediting ALL its artists, so a
track with 3+ collaborators connects all of them.

The graph is deliberately NOT a single connected component: real scenes exist
that share no verified cross-collaboration, and inventing a bridge edge to join
them is exactly the fabrication this dataset is being cleaned of. What the build
does guarantee is that every artist the game can DRAW sits in the main
component, so no puzzle is ever unsolvable — see report_components() and
famous_pool(). It aborts only if the main component falls below 80% of the
roster, which means the data broke rather than merely fragmented.

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
# How many artists the random pickers may draw from. Small enough that the tail
# is still household names (at 1000 it was full of regionally-big-but-obscure
# ones), big enough to hold both today's stars and the era-corrected legends.
# All four difficulty bands still fill from it without fallbacks
# (tools/sim_random.py).
POOL_SIZE = 300


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


def _casts(edges):
    """Split pairwise rows sharing a (title, type, year) into connected casts.

    Returns a list of artist-id lists, each one a group the rows actually tie
    together, in first-seen order so the output stays stable across builds.
    """
    adj = OrderedDict()
    for s1, s2 in edges:
        adj.setdefault(s1, []).append(s2)
        adj.setdefault(s2, []).append(s1)

    seen, casts = set(), []
    for start in adj:
        if start in seen:
            continue
        seen.add(start)
        queue, cast = deque([start]), [start]
        while queue:
            node = queue.popleft()
            for nxt in adj[node]:
                if nxt not in seen:
                    seen.add(nxt)
                    cast.append(nxt)
                    queue.append(nxt)
        casts.append(cast)
    return casts


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
        # Two different songs can share a title and a year. Unioning everyone
        # under that key invents collaborations: "Like That" (2024) is Future,
        # Metro Boomin and Kendrick Lamar — and, separately, Cardi B with Sam
        # Smith. Merged, Kendrick ends up credited alongside Sam Smith on a
        # track neither shares. Split the rows into connected casts and emit one
        # song per cast, so a clique only ever spans people an actual row links.
        for ids in _casts(edges):
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

    # An act that started decades ago and STILL has a big audience is a legend;
    # the raw fan count understates them badly because their peak predates
    # streaming (The Beatles show 8M followers, Drake 24M). Scaling the audience
    # by how early the catalogue starts corrects for that era gap. It stays
    # data-driven — a genuinely obscure old artist has too few fans for the
    # multiplier to lift them anywhere near the pool.
    debut = {}
    for s in songs:
        y = s.get("year") or 0
        if not y:
            continue
        for i in s["artists"]:
            if y < debut.get(i, 9999):
                debut[i] = y

    def era_factor(i):
        y = debut.get(i)
        if y is None:
            return 1.0
        if y <= 1970:
            return 6.0
        if y <= 1985:
            return 4.0
        if y <= 1995:
            return 2.5
        if y <= 2004:
            return 1.5
        return 1.0

    fans, dz = {}, {}
    if os.path.exists(FAME_FILE):
        with open(FAME_FILE, encoding="utf-8") as fh:
            raw = json.load(fh)
        for k, v in raw.items():
            i = slug(int(k))
            if isinstance(v, dict):
                if v.get("fans") is not None:
                    fans[i] = v["fans"]
                if v.get("dz") is not None:
                    dz[i] = v["dz"]
            elif v is not None:
                fans[i] = v

    # Audience as the game should weigh it: real followers, era-corrected.
    weighted_fans = {i: v * era_factor(i) for i, v in fans.items()}
    max_fan_l = max([math.log10(1 + v) for v in weighted_fans.values()], default=1.0) or 1.0
    max_deg_l = max([math.log(1 + d) for d in deg.values()], default=1.0) or 1.0

    scores = {}
    for a in artists:
        i = a["id"]
        d_l = math.log(1 + deg[i]) / max_deg_l
        if i in fans:
            f_l = math.log10(1 + weighted_fans[i]) / max_fan_l
            # Audience dominates; degree is a light tiebreak that rewards
            # collab-heavy artists. It stays small on purpose: a legend with one
            # credited feature (Elvis, Nirvana) must not be pushed under a
            # working feature artist just for collaborating less.
            s = 0.88 * f_l + 0.12 * d_l
        else:
            # No confident Deezer match: fall back to graph prominence only, at a
            # discount so an unmatched name never outranks a verified star.
            s = 0.55 * d_l
        scores[i] = int(round(1000 * max(0.0, min(1.0, s))))
    return scores, deg, fans, adj, dz


# Lowercase/underscore handles ("kendji_girac") are leftovers from an earlier
# generation pass. They are real artists but the label looks broken, so they are
# never served as a random prompt.
HANDLE_RE = re.compile(r"^[a-z0-9_]+$")


def famous_pool(artists, scores, deg, adj, dz):
    """The ids the random pickers are allowed to draw from.

    Everything else stays fully playable (search, chains, solutions) — this only
    governs what a *random* puzzle or the shuffle button may land on.

    Degree-1 artists are admitted only when their single collaborator is itself
    well known: that keeps Nirvana (-> David Bowie) and Destiny's Child
    (-> Beyoncé) in play while leaving out acts whose only link is a name the
    player has no chance of guessing.
    """
    ok = {a["id"] for a in artists if not HANDLE_RE.match(a["name"])}
    # Several roster entries are the same act under a second spelling ("Bieber"
    # vs "Justin Bieber", "MC Anitta" vs "Anitta"). They resolve to one Deezer
    # artist, so they'd inherit the same huge fan count and the picker could
    # serve the misspelled twin. Keep only the best-scoring node of each pair.
    best_of = {}
    for a in artists:
        d = dz.get(a["id"])
        if d is None:
            continue
        cur = best_of.get(d)
        if cur is None or scores[a["id"]] > scores[cur]:
            best_of[d] = a["id"]
    ok -= {a["id"] for a in artists
           if dz.get(a["id"]) is not None and best_of[dz[a["id"]]] != a["id"]}
    # Rank strictly: ties broken by artist id, never by set iteration order.
    # Python randomises string hashing per process, so without this the pool
    # membership at the score cutoff changes between builds of identical data.
    def rank(i):
        return (-scores[i], int(i[1:]))

    core = sorted((i for i in ok if deg.get(i, 0) >= 2), key=rank)
    core_set = set(core[:POOL_SIZE])
    bridged = [i for i in ok
               if deg.get(i, 0) == 1 and next(iter(adj[i])) in core_set]
    eligible = sorted(set(core) | set(bridged), key=rank)
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
    """Emit the dataset as positional rows, rehydrated on import.

    Written as objects this file was 2.0 MB (326 KB gzipped) against a 150 KB
    budget, and roughly a third of that was the same six keys repeated once per
    song. Rows drop the keys; the module rebuilds the objects at import, which
    costs a few milliseconds and keeps every consumer's shape unchanged.

    imageUrl and coverUrl are gone entirely — they were empty strings on all
    5,625 artists and 14,246 songs. Real media arrives from images.generated.js
    or the runtime lookup, and every reader already falls back on a missing
    value.
    """
    sep = (",", ":")
    at = {a["id"]: n for n, a in enumerate(artists)}
    art_rows = [[int(a["id"][1:]), a["name"], a["genre"], a["fame"]] for a in artists]
    # Songs reference artists by row index, not by "a1234" string: there are
    # ~36k of those references and the quoted form was the single heaviest
    # thing in the file.
    song_rows = [
        [s["title"], s["type"], s["year"], [at[x] for x in s["artists"]]]
        for s in songs
    ]

    lines = [
        "// AUTO-GENERATED from data/source_data.py via data/build.py",
        "// Songs link artists; a track with N collaborators connects all of them.",
        "// Multi-component by design; every artist in FAMOUS_IDS sits in the",
        "// main component, so every DRAWN pair is solvable.",
        "// Do not edit by hand; regenerate instead.",
        "",
        "// Positional rows to keep the payload small; see write_js in data/build.py.",
        "// A: [id, name, genre, fame]   S: [title, type, year, [artist row indexes]]",
        "const A = " + json.dumps(art_rows, ensure_ascii=False, separators=sep) + ";",
        "const S = " + json.dumps(song_rows, ensure_ascii=False, separators=sep) + ";",
        "",
        "export const ARTISTS = A.map(([id, name, genre, fame]) => "
        "({ id: 'a' + id, name, genre, fame }));",
        "",
        "// Song ids stay positional, exactly as the build assigned them.",
        "export const SONGS = S.map(([title, type, year, ix], i) => "
        "({ id: 's' + i, title, type, year, artists: ix.map((j) => ARTISTS[j].id) }));",
        "",
        "// Ids the random puzzle / shuffle may pick, best-known first. Every other",
        "// artist stays searchable and playable — this only steers randomness.",
        "export const FAMOUS_IDS = " + json.dumps(pool, ensure_ascii=False, separators=sep) + ";",
        "",
    ]
    with open(OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def assert_pool_solvable(pool, comps):
    """Every drawable artist must live in the main component.

    This is the invariant the game actually depends on. Islands are fine and
    expected, but the moment a pool member sits on one, some fraction of drawn
    puzzles becomes unsolvable with no way for the player to tell — a silent
    failure worth failing the build over.
    """
    main = comps[0] if comps else set()
    stranded = [i for i in pool if i not in main]
    if stranded:
        raise SystemExit(
            f"❌ {len(stranded)} artist(s) in the random pool are outside the "
            f"main component, so puzzles drawing them are unsolvable: "
            f"{', '.join(stranded[:8])}. Fix data/source_data.py."
        )
    print(f"   solvability: all {len(pool)} drawable artists in the main component ✓")


if __name__ == "__main__":
    artists, songs = build()
    comps = report_components(artists, songs)
    scores, deg, fans, adj, dz = fame_scores(artists, songs)
    for a in artists:
        a["fame"] = scores[a["id"]]
    pool = famous_pool(artists, scores, deg, adj, dz)
    assert_pool_solvable(pool, comps)
    write_js(artists, songs, pool)
    by_id = {a["id"]: a for a in artists}
    print(f"   fame: {len(fans)} artists with Deezer fan counts, "
          f"{len(artists) - len(fans)} graph-only | random pool {len(pool)}")
    print("   pool top 15: " + ", ".join(by_id[i]["name"] for i in pool[:15]))
    multi = sum(1 for s in songs if len(s["artists"]) > 2)
    print(f"✅ {len(artists)} artists, {len(songs)} songs ({multi} with 3+ artists)")
    print(f"   wrote {os.path.relpath(OUT, os.path.join(HERE, '..'))}")
