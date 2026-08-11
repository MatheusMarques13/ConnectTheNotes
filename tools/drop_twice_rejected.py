"""Remove the placeholder rows that BOTH catalogues failed to find.

The Brazilian rows were held back for a reason: MusicBrainz files joint projects
under the project name, so its miss on Raça Negra × Só Pra Contrariar said
nothing about whether "Gigantes do Samba" exists. Deezer answered that question
— 57% of the held pairs turned out real.

What is left are pairs neither catalogue can find under any title. Two
independent misses is the strongest evidence available without hand research,
so those rows go. Anything with a hit in either source stays, whatever its
title looks like.

Appends to data/quarantine.json rather than replacing it, so the full removal
history stays in one place and reversible.

Run:  python3 tools/drop_twice_rejected.py [--dry-run]
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

SOURCE = os.path.join(ROOT, "data", "source_data.py")
REPAIR = os.path.join(ROOT, "data", "edge_repair.json")
BR = os.path.join(ROOT, "data", "br_evidence.json")
QUARANTINE = os.path.join(ROOT, "data", "quarantine.json")


def fold(s: str) -> str:
    s = unicodedata.normalize("NFKD", s or "")
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()


def main() -> None:
    dry = "--dry-run" in sys.argv
    name = {i: n for (i, n, _g) in ARTISTS}

    with open(REPAIR, encoding="utf-8") as fh:
        repair = json.load(fh)
    with open(BR, encoding="utf-8") as fh:
        br = json.load(fh)

    # Pairs rejected by MusicBrainz AND by Deezer.
    doomed = {
        key
        for key, v in br.items()
        if v["verdict"] == "none" and repair.get(key, {}).get("verdict") == "drop"
    }
    placeholders = defaultdict(set)
    for key in doomed:
        for t in repair[key].get("placeholders") or []:
            placeholders[key].add(fold(t))

    by_pair = {}
    for key in doomed:
        a1, a2 = (int(x) for x in key.split("-"))
        by_pair[(a1, a2)] = key

    victims = []
    for i, (a1, a2, title, ctype, year) in enumerate(COLLABORATIONS):
        key = by_pair.get((min(a1, a2), max(a1, a2)))
        if key and fold(title) in placeholders[key]:
            victims.append((i, a1, a2, title, ctype, year, key))

    print("=" * 68)
    print("REJEITADAS POR DUAS FONTES")
    print("=" * 68)
    print(f"  pares sem prova em MusicBrainz nem Deezer : {len(doomed)}")
    print(f"  linhas correspondentes ainda no dataset   : {len(victims)}")
    for _i, a1, a2, title, _c, _y, _k in victims[:12]:
        print(f"    {name.get(a1)} × {name.get(a2)} — {title!r}")

    if dry:
        print("\n(dry-run: nada removido)")
        return
    if not victims:
        print("\nnada a remover.")
        return

    with open(SOURCE, encoding="utf-8") as fh:
        lines = fh.read().split("\n")
    start = next(i for i, l in enumerate(lines) if l.startswith("COLLABORATIONS"))
    first = start + 1
    tail = next(i for i, l in enumerate(lines[first:], first) if l.strip() == "]")
    if tail - first != len(COLLABORATIONS):
        sys.exit("❌ layout inesperado em source_data.py. Abortando.")

    drop_idx = {v[0] for v in victims}
    removed = []
    kept_lines = []
    for i in range(len(COLLABORATIONS)):
        raw = lines[first + i]
        if i in drop_idx:
            a1, a2, title, ctype, year = COLLABORATIONS[i]
            removed.append(
                {
                    "row": [a1, a2, title, ctype, year],
                    "line": raw.strip(),
                    "artists": [name.get(a1, ""), name.get(a2, "")],
                    "pair": [name.get(a1, ""), name.get(a2, "")],
                    "reason": "not found in MusicBrainz nor Deezer",
                    "searched": 2,
                }
            )
        else:
            kept_lines.append(raw)

    lines[first:tail] = kept_lines
    with open(SOURCE, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))

    q = {"removed": [], "note": ""}
    if os.path.exists(QUARANTINE):
        with open(QUARANTINE, encoding="utf-8") as fh:
            q = json.load(fh)
    q["removed"].extend(removed)
    q["note"] = ("cole a chave 'line' de volta em COLLABORATIONS para restaurar "
                 "qualquer linha")
    with open(QUARANTINE, "w", encoding="utf-8") as fh:
        json.dump(q, fh, ensure_ascii=False, indent=1)

    print(f"\n✅ {len(removed)} linhas removidas")
    print(f"✅ quarentena agora com {len(q['removed'])} linhas (todas reversiveis)")


if __name__ == "__main__":
    main()
