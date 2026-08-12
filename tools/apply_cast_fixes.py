"""Remove artists from songs they are not credited on.

Reads the verdicts from tools/verify_casts.py and deletes the pairwise rows
that put an uncredited artist on a track. Removing Shakira from 'I Like It'
means dropping every row that pairs her with someone else on that song, not
just one — the rows are pairwise but the song is a clique.

Four guards, because a wrong removal deletes a real collaboration and the
player never learns it was there:

  evidence  Only songs where at least MIN_RECORDINGS matching recordings were
            found. One hit could be a same-named song by other people.
  franchise Numbered series and titles that call themselves a remix or version
            are skipped — see the FRANCHISE note below.
  band      Nobody is stripped from a track their own group is credited on.
            Catalogues say Migos where we say Offset and Quavo.
  keep-two  A song is never reduced below two artists. If the verdict would
            empty it, the disagreement is about the song's identity, not its
            cast, and a human should look.

The first two came from an independent web check of 12 proposed removals
(11 right); the band guard came from reading the next batch by hand, where
'Motorsport', 'Lean On' and 'Wells Fargo' would all have lost real members.

Everything removed lands in data/quarantine.json with the recording count that
justified it.

Run:  python3 tools/apply_cast_fixes.py [--dry-run] [--min-recordings N]
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
AUDIT = os.path.join(ROOT, "data", "cast_audit.json")
GROUPS = os.path.join(ROOT, "data", "artist_groups.json")
QUARANTINE = os.path.join(ROOT, "data", "quarantine.json")

MIN_RECORDINGS = 2
MIN_CAST_AFTER = 2

# Franchise titles are where cast verification goes wrong. An independent web
# check of 12 proposed removals got 11 right; the one miss was "Mayor Que Yo",
# a series with five different line-ups across "Mayor Que Yo", "…2" and "…3".
# Our row was dated 2007 but its cast is the 2015 sequel's, in which Don Omar
# is a lead artist — removing him would have deleted a real collaboration.
#
# So any title that looks like part of a numbered series, or that names itself
# a remix/version, never gets auto-corrected: the disagreement there is about
# WHICH recording the row means, not about who is on it.
FRANCHISE = re.compile(
    r"(?:\b(?:pt|part|parte|vol|volume)\.?\s*\d|\b(?:ii|iii|iv)\b|\s\d\s*$"
    r"|\bremix\b|\bversion\b|\bvers[ãa]o\b|\breload\b|\bredux\b)",
    re.I,
)


def fold(s: str) -> str:
    s = unicodedata.normalize("NFKD", s or "")
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()


def song_key(title: str, ctype: str, year: int) -> tuple:
    return (re.sub(r"\s+", " ", (title or "").strip()).lower(), ctype, year)


def main() -> None:
    dry = "--dry-run" in sys.argv
    floor = MIN_RECORDINGS
    if "--min-recordings" in sys.argv:
        floor = int(sys.argv[sys.argv.index("--min-recordings") + 1])

    name = {i: n for (i, n, _g) in ARTISTS}
    with open(AUDIT, encoding="utf-8") as fh:
        audit = json.load(fh)

    groups = {}
    if os.path.exists(GROUPS):
        with open(GROUPS, encoding="utf-8") as fh:
            groups = json.load(fh)
    linked = {fold(k): {fold(x) for x in v} for k, v in groups.items()}

    def in_band_with(person: str, cast: list[str]) -> str | None:
        """Is `person` a member of a group still credited on this track?

        MusicBrainz credits Migos where we credit Offset and Quavo, and Major
        Lazer where we credit Diplo. Read naively that looks like two impostors
        and one impostor; it is actually the same act named at a different
        level. Never strip someone whose band is standing right there.
        """
        me = fold(person)
        mine = linked.get(me, set())
        for other in cast:
            o = fold(other)
            if o == me:
                continue
            if o in mine or me in linked.get(o, set()):
                return other
        return None

    # Which artists to strip from which merged song.
    strip = {}
    weak, tiny, series, bands = 0, 0, 0, 0
    held = []
    for v in audit.values():
        if v.get("verdict") != "extra-artists":
            continue
        if v.get("recordings_matched", 0) < floor:
            weak += 1
            held.append((v["title"], v["year"], "poucas gravacoes"))
            continue
        if FRANCHISE.search(v["title"]):
            series += 1
            held.append((v["title"], v["year"], "titulo de franquia/versao"))
            continue
        keeping = [x for x in v["cast"] if x not in set(v["not_credited"])]
        safe = []
        for person in v["not_credited"]:
            band = in_band_with(person, keeping)
            if band:
                bands += 1
                held.append((v["title"], v["year"], f"{person} e do {band}"))
                continue
            safe.append(person)
        if not safe:
            continue

        drop = {i for i in v["ids"] if name.get(i) in set(safe)}
        if len(v["ids"]) - len(drop) < MIN_CAST_AFTER:
            tiny += 1
            held.append((v["title"], v["year"], "esvaziaria o elenco"))
            continue
        strip[(fold(v["title"]), v["year"])] = drop

    # Duos judged by tools/verify_casts.py --duos: the catalogue has the song,
    # more than once, and no single recording credits both. That is a cover or a
    # tribute, not a collaboration — Seu Jorge recording "Life on Mars" for The
    # Life Aquatic, Lorde singing Bowie at the Brits. The whole row goes.
    #
    # Unless they are bandmates. A catalogue credits "Cream", never "Cream and
    # Eric Clapton", so every band-and-member pair looks identical to a cover
    # here and would be deleted on the same evidence.
    cover_rows, bandmates = set(), 0
    for v in audit.values():
        if v.get("verdict") != "no-joint-recording":
            continue
        cast = v.get("cast") or []
        if len(cast) != 2:
            continue
        if in_band_with(cast[0], [cast[1]]):
            bandmates += 1
            held.append((v["title"], v["year"], f"{cast[0]} e {cast[1]} sao a mesma banda"))
            continue
        cover_rows.add((fold(v["title"]), v["year"], frozenset(v["ids"])))

    # Rows to delete: any pair where at least one side is stripped from that song.
    victims = []
    for idx, (a1, a2, title, ctype, year) in enumerate(COLLABORATIONS):
        drop = strip.get((fold(title), year))
        if drop and (a1 in drop or a2 in drop):
            victims.append((idx, a1, a2, title, ctype, year, drop))
        elif (fold(title), year, frozenset((a1, a2))) in cover_rows:
            victims.append((idx, a1, a2, title, ctype, year, {a1, a2}))

    print("=" * 70)
    print("CORRECAO DE ELENCO")
    print("=" * 70)
    print(f"  musicas com artista a mais : {len(strip):,}")
    print(f"  seguradas (poucas gravacoes <{floor}) : {weak}")
    print(f"  seguradas (franquia/versao)           : {series}")
    print(f"  seguradas (esvaziaria o elenco)       : {tiny}")
    print(f"  poupados (membro de grupo creditado)  : {bands}")
    print(f"  duplas sem gravacao conjunta (cover)  : {len(cover_rows)}")
    print(f"  poupadas (sao a mesma banda)          : {bandmates}")
    print(f"  linhas a remover           : {len(victims):,}")
    for _i, a1, a2, title, _c, year in [(v[0], v[1], v[2], v[3], v[4], v[5]) for v in victims[:12]]:
        print(f"    {title!r} ({year}) — {name.get(a1)} × {name.get(a2)}")

    if held:
        print(f"\n  amostra do que ficou para revisao humana:")
        for t, y, why in held[:8]:
            print(f"    {t!r} ({y}) — {why}")

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
    kept, removed = [], []
    for i, row in enumerate(COLLABORATIONS):
        raw = lines[first + i]
        if i in drop_idx:
            a1, a2, title, ctype, year = row
            removed.append(
                {
                    "row": list(row), "line": raw.strip(),
                    "artists": [name.get(a1, ""), name.get(a2, "")],
                    "pair": [name.get(a1, ""), name.get(a2, "")],
                    "reason": (
                        "cover/tribute: no recording credits both"
                        if (fold(title), year, frozenset((a1, a2))) in cover_rows
                        else "artist not credited on this recording"
                    ),
                    "searched": audit.get(
                        f"{fold(title)}|{year}", {}
                    ).get("recordings_matched", 0),
                }
            )
        else:
            kept.append(raw)

    lines[first:tail] = kept
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

    print(f"\n✅ {len(removed):,} linhas removidas")
    print(f"✅ quarentena agora com {len(q['removed']):,} linhas")


if __name__ == "__main__":
    main()
