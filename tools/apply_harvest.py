"""Merge harvested 2023+ collaborations into data/source_data.py.

tools/harvest_recent.py collects candidates; this is the gate they have to pass
before becoming rows. It re-runs the rejection filters here rather than trusting
the crawl, because the crawl's rules changed mid-run and a stale candidate is
exactly how bad data creeps back in.

Rejected here:
  DJ service edits — transitions, mashups, blends, drumless cuts. They credit
    both source artists and read as collaborations, but nobody collaborated.
  remixes         — a remix credit is a derivative work, not a session. Guetta
    remixing U2 is not Guetta and U2 working together. Kept out by default;
    pass --with-remixes to include them typed as `remix`.
  duplicates      — anything already in COLLABORATIONS, matched on
    (pair, folded title).

Every accepted row carries its MusicBrainz recording id in
data/edge_sources.json, so any claim in the dataset can be traced back.

Run:  python3 tools/apply_harvest.py [--dry-run] [--with-remixes]
"""
import json
import os
import re
import sys
import time
import unicodedata
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
sys.path.insert(0, os.path.join(ROOT, "data"))
from source_data import ARTISTS, COLLABORATIONS  # noqa: E402

SOURCE = os.path.join(ROOT, "data", "source_data.py")
HARVEST = os.path.join(ROOT, "data", "recent_harvest.json")
SOURCES = os.path.join(ROOT, "data", "edge_sources.json")

DJ_EDIT = re.compile(
    r"\b(?:transition|drumless|mash(?:up)?|blend|bootleg|flip|segue|redrum"
    r"|quick\s?hit|short\s?edit|hype\s?edit|intro\s?edit|outro|acap"
    r"|dirty|clean|edition|super\s?cut|megamix|throwback\s?mix|continuous\s?mix|in\s?the\s?mix|version)\b"
    r"|\b\d{2,3}\s*-\s*\d{2,3}\b",
    re.I,
)
TECHNICAL = re.compile(
    r"\b(?:instrumental|a\s?cappella|acapella|sped\s?up|slowed|karaoke"
    r"|radio\s?edit|extended|censored|sessions?)\b",
    re.I,
)
# "Rather Be Rather Be" — a mashup artefact where the title got doubled.
# A DJ mix lists adjacent tracks: "Tears / I Just Might / bye (Mixed)"
# credits Bruno Mars and Sabrina Carpenter, who never worked together.
MIXED_TAG = re.compile(r"[\(\[]\s*(?:mixed|dj\s?mix)\s*[\)\]]", re.I)

DOUBLED = re.compile(r"^(.{4,40}?)\s+\1$", re.I)


def fold(s: str) -> str:
    s = unicodedata.normalize("NFKD", s or "")
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()


def rejected(title: str) -> str | None:
    if DJ_EDIT.search(title) or MIXED_TAG.search(title):
        return "dj-edit"
    if TECHNICAL.search(title):
        return "technical-variant"
    if DOUBLED.match(title.strip()):
        return "doubled-title"
    if len(title.strip()) < 2:
        return "empty-title"
    return None


def main() -> None:
    dry = "--dry-run" in sys.argv
    with_remixes = "--with-remixes" in sys.argv

    # The crawl may be running and rewriting this file; retry rather than die
    # on a snapshot caught mid-write.
    found = None
    for attempt in range(6):
        try:
            with open(HARVEST, encoding="utf-8") as fh:
                found = json.load(fh)["found"]
            break
        except json.JSONDecodeError:
            time.sleep(1.5)
    if found is None:
        sys.exit("❌ nao consegui ler data/recent_harvest.json (colheita escrevendo?)")

    known = {
        (min(a1, a2), max(a1, a2), fold(t))
        for a1, a2, t, _c, _y in COLLABORATIONS
    }
    known_pairs = {(min(a1, a2), max(a1, a2)) for a1, a2, *_ in COLLABORATIONS}

    accepted, why = [], Counter()
    seen = set()
    for c in found:
        reason = rejected(c["title"])
        if reason:
            why[reason] += 1
            continue
        if c["type"] == "remix" and not with_remixes:
            why["remix"] += 1
            continue
        key = (min(c["a1"], c["a2"]), max(c["a1"], c["a2"]), fold(c["title"]))
        if key in known or key in seen:
            why["duplicate"] += 1
            continue
        seen.add(key)
        accepted.append(c)

    print("=" * 68)
    print("TRIAGEM DA COLHEITA")
    print("=" * 68)
    print(f"  candidatos     : {len(found):,}")
    for k, v in why.most_common():
        print(f"    rejeitado {k:18s} {v:5,d}")
    print(f"  ACEITOS        : {len(accepted):,}")
    novos = sum(1 for c in accepted
                if (min(c['a1'], c['a2']), max(c['a1'], c['a2'])) not in known_pairs)
    print(f"    pares ineditos: {novos:,}")
    print(f"  por ano        : "
          f"{dict(sorted(Counter(c['year'] for c in accepted).items()))}")

    print("\n  amostra:")
    for c in accepted[:12]:
        print(f"    [{c['year']}] {c['names'][0]} × {c['names'][1]} — {c['title']!r}")

    if dry:
        print("\n(dry-run: source_data.py intacto)")
        return
    if not accepted:
        print("\nnada a aplicar.")
        return

    with open(SOURCE, encoding="utf-8") as fh:
        lines = fh.read().split("\n")
    close = max(i for i, l in enumerate(lines) if l.strip() == "]")

    rows = [
        f"    ({c['a1']}, {c['a2']}, {c['title']!r}, {c['type']!r}, {c['year']}),"
        for c in accepted
    ]
    lines[close:close] = rows
    with open(SOURCE, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))

    prov = {}
    if os.path.exists(SOURCES):
        with open(SOURCES, encoding="utf-8") as fh:
            prov = json.load(fh)
    for c in accepted:
        prov[f"{c['a1']}-{c['a2']}-{c['title']}"] = {
            "source": "musicbrainz",
            "id": c["mbid"],
            "was": "(colhido 2023+)",
        }
    with open(SOURCES, "w", encoding="utf-8") as fh:
        json.dump(prov, fh, ensure_ascii=False, indent=1)

    print(f"\n✅ {len(rows):,} arestas adicionadas a source_data.py")
    print(f"✅ provenancia total: {len(prov):,} arestas rastreaveis")


if __name__ == "__main__":
    main()
