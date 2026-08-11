"""Drop artists that no longer appear in any collaboration.

Cleaning out fabricated rows leaves artists behind with nothing attached. They
are real people, but in a game about connections an artist with no connection
is dead weight: unreachable in play, noise in search, and a puzzle generator
trap if one ever slipped into the drawable pool.

Removed entries are written to data/pruned_artists.json with the row verbatim,
so re-adding one costs a paste once a real collaboration for them is found.

Run:  python3 tools/prune_orphans.py [--dry-run]
"""
import json
import os
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
sys.path.insert(0, os.path.join(ROOT, "data"))
from source_data import ARTISTS, COLLABORATIONS  # noqa: E402

SOURCE = os.path.join(ROOT, "data", "source_data.py")
PRUNED = os.path.join(ROOT, "data", "pruned_artists.json")


def main() -> None:
    dry = "--dry-run" in sys.argv

    deg = Counter()
    for a1, a2, *_ in COLLABORATIONS:
        if a1 != a2:
            deg[a1] += 1
            deg[a2] += 1

    orphans = [(i, n, g) for (i, n, g) in ARTISTS if not deg[i]]
    print("=" * 68)
    print(f"ARTISTAS SEM NENHUMA COLABORACAO: {len(orphans)}")
    print("=" * 68)
    for i, n, g in orphans[:25]:
        print(f"   {n}  [{g}]")
    if len(orphans) > 25:
        print(f"   ... e mais {len(orphans) - 25}")
    print(f"\n  roster: {len(ARTISTS):,} -> {len(ARTISTS) - len(orphans):,}")

    if dry:
        print("\n(dry-run: nada removido)")
        return
    if not orphans:
        print("\nnada a remover.")
        return

    drop = {i for i, _n, _g in orphans}
    with open(SOURCE, encoding="utf-8") as fh:
        lines = fh.read().split("\n")

    start = next(i for i, l in enumerate(lines) if l.startswith("ARTISTS"))
    first = start + 1
    tail = next(i for i, l in enumerate(lines[first:], first) if l.strip() == "]")
    if tail - first != len(ARTISTS):
        sys.exit(
            f"❌ layout inesperado: {tail - first} linhas para {len(ARTISTS)} "
            f"artistas. Abortando."
        )

    kept, removed = [], []
    for n, (i, name, genre) in enumerate(ARTISTS):
        raw = lines[first + n]
        if i in drop:
            removed.append({"id": i, "name": name, "genre": genre,
                            "line": raw.strip()})
        else:
            kept.append(raw)

    lines[first:tail] = kept
    with open(SOURCE, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))

    with open(PRUNED, "w", encoding="utf-8") as fh:
        json.dump(
            {
                "removed": removed,
                "note": "cole a chave 'line' de volta em ARTISTS para restaurar",
            },
            fh, ensure_ascii=False, indent=1,
        )

    print(f"\n✅ {len(removed)} artistas removidos")
    print(f"✅ reversiveis em data/pruned_artists.json")


if __name__ == "__main__":
    main()
