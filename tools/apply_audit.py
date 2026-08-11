"""Write the audit's conclusions back into data/source_data.py.

Two edits, both driven by data/edge_repair.json:

    repair — the pair is real, the title was a placeholder. Swap in the title
             MusicBrainz confirmed and record the MBID as provenance.
    remove — no shared recording anywhere. The row leaves source_data.py and
             lands in data/quarantine.json, reason and evidence attached.

Brazilian pairs are held back. MusicBrainz catalogues joint projects under the
project name rather than two credited artists, so a miss there is not evidence
of fabrication — Raça Negra and Só Pra Contrariar really did record "Gigantes
do Samba". Those wait for tools/verify_br_pairs.py.

Nothing is destroyed: every removed row is reproduced verbatim in the
quarantine file and can be pasted back.

Run:  python3 tools/apply_audit.py [--dry-run]
"""
import json
import os
import re
import sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
sys.path.insert(0, os.path.join(ROOT, "data"))
from source_data import ARTISTS, COLLABORATIONS  # noqa: E402

SOURCE = os.path.join(ROOT, "data", "source_data.py")
AUDIT = os.path.join(ROOT, "data", "edge_audit.json")
REPAIR = os.path.join(ROOT, "data", "edge_repair.json")
BR_EVIDENCE = os.path.join(ROOT, "data", "br_evidence.json")
QUARANTINE = os.path.join(ROOT, "data", "quarantine.json")
SOURCES = os.path.join(ROOT, "data", "edge_sources.json")

BR_TAGS = (
    "Sertanejo", "Agronejo", "Pagode", "Axé", "Forró", "MPB", "Samba",
    "Brazilian", "Funk Carioca", "Funk Paulista", "Funk Ostentação",
    "Tropicália",
)

# The artist's genre tag is an unreliable nationality signal: Anitta is filed
# under "Latin Pop", Iza under "R&B/Pop", Ana Castela under "Agronejo". The
# placeholder's own language is the sturdier clue — a Portuguese title means
# Brazilian repertoire whatever the tag says, so the row waits for the Deezer
# pass instead of being deleted on a MusicBrainz miss.
PT_TITLE = re.compile(
    r"ao vivo|juntas?|juntos|carnaval|especial|participa[çc][ãa]o|ver[ãa]o"
    r"|salvador|fortaleza|goi[âa]nia|s[ãa]o paulo|bahia|nordestino|baiano"
    r"|sertanejo|forr[óo]|pagode|samba",
    re.I,
)

# Titles that are themselves placeholders — never accept one as a repair.
PLACEHOLDER = re.compile(
    r"^(?:ao vivo|participa[çc][ãa]o|especial|show|dvd|medley\b.*)$", re.I
)


def is_br(genre: str) -> bool:
    return any(t in (genre or "") for t in BR_TAGS)


# Catalogue titles carry the credit inline ("O Portão (feat. Zezé Di Camargo &
# Luciano) Ao Vivo"). The game already shows who is on the song, so the credit
# is noise in a puzzle board — strip it, keep the live marker.
FEAT_SUFFIX = re.compile(
    r"\s*[\(\[]\s*(?:feat|ft|com|with|participa[çc][ãa]o)\.?\s[^)\]]*[\)\]]", re.I
)


def clean_title(title: str) -> str:
    return re.sub(r"\s{2,}", " ", FEAT_SUFFIX.sub("", title or "")).strip()


def pick_titles(candidates: list[dict], n_rows: int) -> list[dict]:
    """Give each placeholder row its own confirmed title where possible.

    A pair often carries several placeholder rows. Reusing one title for all of
    them would collapse them into a single song in build.py, silently dropping
    edges the audit meant to keep.
    """
    usable = [c for c in candidates if c.get("title") and not PLACEHOLDER.match(c["title"])]
    if not usable:
        usable = [c for c in candidates if c.get("title")]
    if not usable:
        return []
    return [usable[i % len(usable)] for i in range(n_rows)]


def main() -> None:
    dry = "--dry-run" in sys.argv
    genre = {i: g for (i, _n, g) in ARTISTS}
    name = {i: n for (i, n, _g) in ARTISTS}

    with open(AUDIT, encoding="utf-8") as fh:
        audit = json.load(fh)
    with open(REPAIR, encoding="utf-8") as fh:
        repair = json.load(fh)

    pairs = defaultdict(list)
    for e in audit["edges"]:
        if e["verdict"] == "fabricated":
            pairs[f"{min(e['a1'], e['a2'])}-{max(e['a1'], e['a2'])}"].append(e)

    br = {}
    if os.path.exists(BR_EVIDENCE):
        with open(BR_EVIDENCE, encoding="utf-8") as fh:
            br = json.load(fh)

    retitle: dict[int, tuple[str, int | None, str, str]] = {}  # idx -> title, year, id, src
    remove: dict[int, dict] = {}                               # idx -> reason payload
    held = 0
    from_br = 0

    for key, v in repair.items():
        rows = pairs.get(key, [])
        if not rows:
            continue
        if v["verdict"] == "repair":
            chosen = pick_titles(v.get("candidates") or [], len(rows))
            for row, cand in zip(rows, chosen):
                retitle[row["i"]] = (
                    clean_title(cand["title"]), cand.get("year"),
                    cand.get("mbid", ""), "musicbrainz",
                )
            continue

        # Deezer covers the Brazilian catalogue MusicBrainz misses, so a
        # confirmed hit there repairs the row the same way.
        ev = br.get(key)
        if ev and ev["verdict"] == "confirmed" and ev.get("confirmed"):
            chosen = pick_titles(ev["confirmed"], len(rows))
            for row, cand in zip(rows, chosen):
                retitle[row["i"]] = (
                    clean_title(cand["title"]), None,
                    str(cand.get("deezer_id", "")), "deezer",
                )
            from_br += len(rows)
            continue

        br_artist = is_br(genre.get(v["a1"])) or is_br(genre.get(v["a2"]))
        br_title = any(PT_TITLE.search(r["title"]) for r in rows)
        if br_artist or br_title:
            held += len(rows)
            continue
        for row in rows:
            remove[row["i"]] = {
                "pair": v["names"],
                "reason": "no shared recording in MusicBrainz",
                "searched": v.get("count", 0),
            }

    print("=" * 68)
    print("PLANO")
    print("=" * 68)
    print(f"  reescrever titulo : {len(retitle):4d} linhas "
          f"({from_br} vindos do Deezer)")
    print(f"  remover           : {len(remove):4d} linhas -> data/quarantine.json")
    print(f"  segurar (BR)      : {held:4d} linhas (sem prova em nenhuma fonte)")

    # ---------------------------------------------------------- rewrite file
    with open(SOURCE, encoding="utf-8") as fh:
        lines = fh.read().split("\n")

    start = next(i for i, l in enumerate(lines) if l.startswith("COLLABORATIONS"))
    first = start + 1                       # first tuple line, 0-based

    # The block is one tuple per line with no comments (verified), so edge i
    # lives on line first + i. Assert it before touching anything.
    tail = [i for i, l in enumerate(lines[first:], first) if l.strip() == "]"]
    if not tail or tail[0] - first != len(COLLABORATIONS):
        sys.exit(
            f"❌ layout inesperado: {tail[0] - first if tail else '?'} linhas de "
            f"tupla para {len(COLLABORATIONS)} arestas. Abortando."
        )

    out, quarantined, provenance = [], [], {}
    for i, (a1, a2, title, ctype, year) in enumerate(COLLABORATIONS):
        raw = lines[first + i]
        if i in remove:
            quarantined.append(
                {
                    "row": [a1, a2, title, ctype, year],
                    "line": raw.strip(),
                    "artists": [name.get(a1, ""), name.get(a2, "")],
                    **remove[i],
                }
            )
            continue
        if i in retitle:
            new_title, new_year, ref, src = retitle[i]
            year = new_year or year
            out.append(f"    ({a1}, {a2}, {new_title!r}, {ctype!r}, {year}),")
            if ref:
                provenance[f"{a1}-{a2}-{new_title}"] = {
                    "source": src,
                    "id": ref,
                    "was": title,
                }
            continue
        out.append(raw)

    if dry:
        print("\n(dry-run: nada escrito)")
        return

    rebuilt = lines[: first] + out + lines[first + len(COLLABORATIONS):]
    with open(SOURCE, "w", encoding="utf-8") as fh:
        fh.write("\n".join(rebuilt))

    with open(QUARANTINE, "w", encoding="utf-8") as fh:
        json.dump(
            {"removed": quarantined, "note": "cole a chave 'line' de volta em "
             "COLLABORATIONS para restaurar qualquer linha"},
            fh, ensure_ascii=False, indent=1,
        )
    with open(SOURCES, "w", encoding="utf-8") as fh:
        json.dump(provenance, fh, ensure_ascii=False, indent=1)

    print(f"\n✅ source_data.py reescrito: {len(out):,} arestas "
          f"(era {len(COLLABORATIONS):,})")
    print(f"✅ {len(quarantined)} linhas em data/quarantine.json (reversivel)")
    print(f"✅ {len(provenance)} MBIDs de origem em data/edge_sources.json")


if __name__ == "__main__":
    main()
