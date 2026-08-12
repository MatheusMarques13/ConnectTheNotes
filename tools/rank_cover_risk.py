"""Rank duo edges by how likely they are a cover rather than a collaboration.

Checking all 18k duos against MusicBrainz costs ~22 hours at the catalogue's
1 req/s. Most of them are fine, so spend the budget where the risk is.

A cover pretending to be a collaboration has a shape:

  one shared song   Seu Jorge and David Bowie meet exactly once, on "Life on
                    Mars". Real collaborators usually meet more than once, or
                    at least sit in the same scene.
  no provenance     it came from the seeded data, not from a catalogue crawl.
  era gap           the two artists work decades apart. Lorde singing Bowie at
                    the Brits and Seu Jorge recording him for The Life Aquatic
                    both look like this; a genuine duet rarely does.

Writes data/cover_risk.json, highest risk first, for tools/verify_casts.py to
work through.

Run:  python3 tools/rank_cover_risk.py
"""
import json
import os
import statistics
import sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
sys.path.insert(0, os.path.join(ROOT, "data"))
from source_data import ARTISTS, COLLABORATIONS  # noqa: E402

SOURCES = os.path.join(ROOT, "data", "edge_sources.json")
OUT = os.path.join(ROOT, "data", "cover_risk.json")

# Two artists whose catalogues sit this far apart did not casually duet.
ERA_GAP = 15


def main() -> None:
    name = {i: n for (i, n, _g) in ARTISTS}
    prov = {}
    if os.path.exists(SOURCES):
        with open(SOURCES, encoding="utf-8") as fh:
            prov = json.load(fh)

    years = defaultdict(list)
    pairs = defaultdict(list)
    for a1, a2, title, ctype, year in COLLABORATIONS:
        if a1 == a2:
            continue
        years[a1].append(year)
        years[a2].append(year)
        pairs[(min(a1, a2), max(a1, a2))].append((title, ctype, year))

    era = {i: statistics.median(v) for i, v in years.items() if v}

    ranked = []
    for (a, b), songs in pairs.items():
        if len(songs) != 1:
            continue
        title, ctype, year = songs[0]
        sourced = (f"{a}-{b}-{title}" in prov) or (f"{b}-{a}-{title}" in prov)
        if sourced:
            continue
        gap = abs(era.get(a, year) - era.get(b, year))
        if gap < ERA_GAP:
            continue
        ranked.append(
            {
                "a1": a, "a2": b,
                "names": [name.get(a, ""), name.get(b, "")],
                "title": title, "type": ctype, "year": year,
                "era_gap": gap,
                "eras": [era.get(a), era.get(b)],
            }
        )

    ranked.sort(key=lambda r: -r["era_gap"])
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(ranked, fh, ensure_ascii=False, indent=1)

    print("=" * 70)
    print(f"DUPLAS DE ALTO RISCO DE COVER: {len(ranked):,}")
    print(f"  (de {sum(1 for s in pairs.values() if len(s) == 1):,} duplas com "
          f"uma unica musica)")
    print("=" * 70)
    for r in ranked[:20]:
        print(f"  gap {r['era_gap']:5.0f}a  {r['names'][0]} × {r['names'][1]}")
        print(f"             {r['title']!r} ({r['year']})")
    print(f"\n✅ data/cover_risk.json — a 14/min sao "
          f"{len(ranked) / 14 / 60:.1f}h")


if __name__ == "__main__":
    main()
