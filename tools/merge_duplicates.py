"""Merge roster entries that are the same artist under two spellings.

The roster grew from several import passes, so some acts exist twice ("Charli
XCX" and "Charlie XCX", "Alok" and "DJ Alok"). It shows: 29 songs credit BOTH
twins, so the solution screen lists the same person twice.

Two merge rules, both evidence-based rather than name guessing:
  A. Both entries resolve to the same Deezer artist id (data/artist_fame.json).
  B. The two entries appear together on a song AND their names are equal once
     leetspeak is folded ("P!nk" -> "pink"). Sharing a credit is what makes this
     safe: two different artists with near-identical names would not both be
     credited on the same recording.

The surviving node is the better-connected one (it carries the most real
collaborations); edges are rewritten onto it, the self-edge the merge creates is
dropped, and duplicate rows are collapsed.

Run:  python3 tools/merge_duplicates.py [--apply]
"""
import json
import os
import re
import sys
import unicodedata
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
sys.path.insert(0, os.path.join(ROOT, "data"))

from source_data import ARTISTS, COLLABORATIONS  # noqa: E402

FAME = os.path.join(ROOT, "data", "artist_fame.json")
OUT = os.path.join(ROOT, "data", "source_data.py")

LEET = str.maketrans({"!": "i", "$": "s", "0": "o", "1": "i", "3": "e", "@": "a"})


def fold(s):
    s = unicodedata.normalize("NFKD", s or "")
    s = "".join(c for c in s if not unicodedata.combining(c)).lower()
    return re.sub(r"[^a-z0-9]+", "", s.translate(LEET))


def songkey(t):
    return re.sub(r"\s+", " ", (t or "").strip()).lower()


def main():
    apply = "--apply" in sys.argv
    names = {i: n for i, n, _g in ARTISTS}
    deg = defaultdict(set)
    songs = defaultdict(set)
    for a, b, t, ty, y in COLLABORATIONS:
        deg[a].add(b)
        deg[b].add(a)
        songs[(songkey(t), ty, y)].update((a, b))

    dz, fans, dz_name = {}, {}, {}
    if os.path.exists(FAME):
        with open(FAME, encoding="utf-8") as fh:
            for k, v in json.load(fh).items():
                if isinstance(v, dict) and v.get("dz") is not None:
                    dz[int(k)] = v["dz"]
                    fans[int(k)] = v.get("fans") or 0
                    if v.get("name"):
                        dz_name[int(k)] = v["name"]

    groups = defaultdict(set)
    for i, d in dz.items():
        if i in names:
            groups[("dz", d)].add(i)
    # Rule B: same song + same folded name.
    for members in songs.values():
        members = sorted(members)
        for x in range(len(members)):
            for y in range(x + 1, len(members)):
                a, b = members[x], members[y]
                if fold(names.get(a, "")) == fold(names.get(b, "")):
                    groups[("name", fold(names[a]))].update((a, b))

    # union-find so a node caught by both rules lands in one group
    parent = {}

    def find(x):
        parent.setdefault(x, x)
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(x, y):
        rx, ry = find(x), find(y)
        if rx != ry:
            parent[rx] = ry

    for g in groups.values():
        g = sorted(g)
        for other in g[1:]:
            union(g[0], other)

    clusters = defaultdict(set)
    for i in list(parent):
        clusters[find(i)].add(i)
    clusters = {k: v for k, v in clusters.items() if len(v) > 1}

    canon, rename = {}, {}
    for members in clusters.values():
        # Keep the best-connected node so no collaboration is orphaned...
        keep = max(members, key=lambda i: (len(deg[i]), len(names.get(i, ""))))
        for i in members:
            if i != keep:
                canon[i] = keep
        # ...but take the spelling from the catalog, because the better-connected
        # entry is often the misspelled one ("Pink" for P!nk, "Murillo Huff").
        best_dz = max((i for i in members if i in dz_name),
                      key=lambda i: fans.get(i, 0), default=None)
        label = names[keep]
        if best_dz is not None:
            official = dz_name[best_dz]
            exact = [names[i] for i in members if names[i] == official]
            close = [names[i] for i in members if fold(names[i]) == fold(official)]
            if exact:
                label = exact[0]
            elif close:
                # Prefer a mixed-case variant: Deezer sometimes stores "Charli xcx".
                label = max(close, key=lambda n: any(c.isupper() for c in n[1:]))
            else:
                label = official
        if label != names[keep]:
            rename[keep] = label
        print(f"  keep {label!r} ({len(deg[keep])} collabs)"
              + (f"  [renamed from {names[keep]!r}]" if label != names[keep] else "")
              + "  <-  " + ", ".join(f"{names[i]!r}" for i in members if i != keep))

    print(f"\n{len(clusters)} clusters, {len(canon)} entries merged away")
    if not apply:
        print("(dry run — pass --apply to write)")
        return

    seen, out_rows, selfies = set(), [], 0
    for a, b, t, ty, y in COLLABORATIONS:
        a, b = canon.get(a, a), canon.get(b, b)
        if a == b:
            selfies += 1
            continue
        key = (min(a, b), max(a, b), songkey(t), ty, y)
        if key in seen:
            continue
        seen.add(key)
        out_rows.append((a, b, t, ty, y))

    kept = [(i, rename.get(i, n), g) for (i, n, g) in ARTISTS if i not in canon]
    lines = ['"""Canonical, human-editable source data for Connect the Notes.', "",
             "Single connected component target; regenerate dataset.js via",
             "python data/build.py.", '"""', "", "# (id, name, genre)", "ARTISTS = ["]
    for i, n, g in kept:
        lines.append(f"    ({i}, {n!r}, {g!r}),")
    lines += ["]", "", "# (artist1_id, artist2_id, title, type, year)", "COLLABORATIONS = ["]
    for a, b, t, ty, y in out_rows:
        lines.append(f"    ({a}, {b}, {t!r}, {ty!r}, {y}),")
    lines += ["]", ""]
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))
    print(f"wrote {len(kept)} artists ({len(ARTISTS) - len(kept)} removed), "
          f"{len(out_rows)} collabs (dropped {selfies} twin self-edges, "
          f"{len(COLLABORATIONS) - len(out_rows) - selfies} duplicate rows)")


if __name__ == "__main__":
    main()
