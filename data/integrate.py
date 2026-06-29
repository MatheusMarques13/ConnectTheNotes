"""Integrate generated artist/collaboration batches into data/source_data.py.

Usage: python data/integrate.py batches.json
- Reuses existing artist ids; assigns new ids to genuinely new artists (deduped
  by normalized name across all batches + existing).
- Resolves each collaboration's two artists by name; drops collabs whose names
  can't be matched. Dedups exact tuples.
- Rewrites data/source_data.py with the combined lists.
"""
import json
import os
import re
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import source_data as sd  # noqa: E402

OUT = os.path.join(HERE, "source_data.py")


def norm(n):
    # Accent-insensitive: "Beyoncé" == "Beyonce", "Sơn Tùng" == "Son Tung".
    s = unicodedata.normalize("NFKD", (n or "").lower())
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]", "", s)


def main(path):
    batches = json.load(open(path, encoding="utf-8"))

    artists = [list(a) for a in sd.ARTISTS]          # (id, name, genre)
    collabs = [list(c) for c in sd.COLLABORATIONS]   # (a, b, title, type, year)
    by_norm = {norm(name): aid for (aid, name, genre) in artists}
    next_id = max(a[0] for a in artists) + 1

    added_artists = 0
    for batch in batches:
        for art in batch.get("artists", []):
            name = (art.get("name") or "").strip()
            if not name:
                continue
            k = norm(name)
            if k in by_norm:
                continue
            by_norm[k] = next_id
            artists.append([next_id, name, (art.get("genre") or "Unknown").strip()])
            next_id += 1
            added_artists += 1

    def resolve_or_add(name):
        """Map a collaborator name to an id, auto-adding a real referenced
        artist that wasn't in any artists list (so bridges aren't lost)."""
        nonlocal next_id, added_artists
        name = (name or "").strip()
        k = norm(name)
        if not k:
            return None
        if k in by_norm:
            return by_norm[k]
        if len(name) < 2:
            return None
        by_norm[k] = next_id
        artists.append([next_id, name, "Other"])
        next_id += 1
        added_artists += 1
        return by_norm[k]

    seen = set((min(a, b), max(a, b), t, ty, y) for (a, b, t, ty, y) in collabs)
    added_collabs = dropped = 0
    for batch in batches:
        for c in batch.get("collaborations", []):
            title = (c.get("title") or "").strip()
            ctype = (c.get("type") or "song").strip()
            year = c.get("year")
            if not title or not isinstance(year, (int, float)):
                dropped += 1
                continue
            ai = resolve_or_add(c.get("a", ""))
            bi = resolve_or_add(c.get("b", ""))
            if not ai or not bi or ai == bi:
                dropped += 1
                continue
            key = (min(ai, bi), max(ai, bi), title, ctype, int(year))
            if key in seen:
                continue
            seen.add(key)
            collabs.append([ai, bi, title, ctype, int(year)])
            added_collabs += 1

    write(artists, collabs)
    print(f"Added {added_artists} new artists (total {len(artists)})")
    print(f"Added {added_collabs} new collaborations (total {len(collabs)}); dropped {dropped} unresolved")


def write(artists, collabs):
    lines = ['"""Canonical, human-editable source data for Connect the Notes.',
             "",
             "Edit ARTISTS / COLLABORATIONS, then run `python data/build.py` to regenerate",
             "frontend/src/data/dataset.js. The build merges same-title/year collaborations",
             "into one multi-artist song and asserts the graph is a single connected",
             "component (every puzzle solvable).",
             '"""',
             "",
             "# (id, name, genre)",
             "ARTISTS = ["]
    for aid, name, genre in artists:
        lines.append(f"    ({aid}, {name!r}, {genre!r}),")
    lines.append("]")
    lines.append("")
    lines.append("# (artist1_id, artist2_id, title, type, year)  type: song|album|ep|mixtape|live|dvd|feature|video")
    lines.append("COLLABORATIONS = [")
    for a, b, t, ty, y in collabs:
        lines.append(f"    ({a}, {b}, {t!r}, {ty!r}, {y}),")
    lines.append("]")
    lines.append("")
    open(OUT, "w", encoding="utf-8").write("\n".join(lines))


if __name__ == "__main__":
    main(sys.argv[1])
