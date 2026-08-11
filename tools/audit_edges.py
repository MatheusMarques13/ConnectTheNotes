"""Classify every COLLABORATIONS row by how much we trust it.

The dataset was seeded from model knowledge rather than harvested from a
catalog, so a slice of it is fabricated: edges whose "title" is a genre label
("Indie Folk Feature"), a release format ("Ao Vivo"), or an event name ("Rock
in Rio"). Those are not songs — they are placeholders someone wrote to justify
a connection that may never have happened.

This tool finds them. It removes nothing: it writes a verdict per row so the
removal step and the catalog verifier can both consume the same judgement.

    fabricated — the title is provably not a song title. Safe to drop.
    suspect    — plausible title, but the row smells (one title shared by many
                 unrelated artists across many years). Needs catalog proof.
    trusted    — nothing suspicious found locally. Still unverified.

A live recording that genuinely exists stays trusted: "ao vivo" is a release
format in Brazil, not evidence of fabrication. The axis here is real vs
invented, never live vs studio.

Run:  python3 tools/audit_edges.py
"""
import json
import os
import re
import sys
from collections import Counter, defaultdict, deque

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
sys.path.insert(0, os.path.join(ROOT, "data"))
from source_data import ARTISTS, COLLABORATIONS  # noqa: E402

OUT = os.path.join(ROOT, "data", "edge_audit.json")

# A title shared by this many distinct artists across this many distinct years
# is not one song — real songs do not get re-recorded by 20 unrelated acts
# across two decades under the same name.
SPREAD_ARTISTS = 8
SPREAD_YEARS = 3


def norm(t: str) -> str:
    return re.sub(r"\s+", " ", (t or "").strip()).lower()


# --------------------------------------------------------------- fabricated
# A genre or scene used where a song title belongs: "Indie Folk Feature",
# "Bedroom Pop Scene", "R&B Feature".
#
# The two suffixes need different care. Nothing real is titled "... Feature",
# so that ending alone is proof — it also catches the album-name variants
# ("Pure Comedy Feature", "Bastard Feature"). "Scene" is a normal English
# word and "Ending Scene" is a genuine IU song, so a bare "... Scene" only
# counts when the title also names a genre.
GENRE_WORD = re.compile(
    r"\b(?:indie|pop|rock|folk|electronic|hyperpop|bedroom|r&b|rap|hip.?hop"
    r"|experimental|art|alt|dream|punk|metal|country|edm|techno|house|jazz"
    r"|soul|funk|ambient|shoegaze|emo|grunge|disco|gospel|trap|drill|garage"
    r"|psych|noise|lo.?fi|synth|new wave|post.?punk|post.?hardcore|pc music"
    r"|soca|calypso|worship|ccm|opm|k.?pop|afro)\b",
    re.I,
)
FEATURE_SUFFIX = re.compile(r"^[\w&/'\- ,.]{2,40}\sfeature$", re.I)
SCENE_SUFFIX = re.compile(r"^[\w&/'\- ,.]{2,40}\sscene$", re.I)

# An English phrase describing the collaboration instead of naming it.
DESCRIPTIVE = re.compile(
    r"^(?:live concert collaboration|festival co-headline|[\w' ]+ shared bill"
    r"|[\w' ]+ produced sessions?|the cypher|collaboration|joint performance)$",
    re.I,
)

# A release format standing in for a song title. Anchored so that real songs
# whose name merely begins with the same words survive — "Ao Vivo e a Cores"
# (Matheus & Kauan / Anitta) must NOT match.
FORMAT_LABEL = re.compile(
    r"^(?:"
    r"ao vivo|participa[çc][ãa]o|especial|show|dvd|turn[êe]|medley|colabora[çc][ãa]o"
    r"|parceria|dueto|tributo|homenagem|projeto|single|[áa]lbum|mixtape"
    r")"
    r"(?:\s+(?:ao vivo|especial|juntos?|juntas|do ano|de natal|de ver[ãa]o"
    r"|em\s+[\w'\- ]+|no\s+[\w'\- ]+|na\s+[\w'\- ]+))*"
    r"$",
    re.I,
)

# Event and festival names. Only forms that cannot plausibly be a song title:
# bare "Carnaval" is a real song name, "Carnaval Baiano" is a description of
# where two artists shared a stage.
EVENT_NAME = re.compile(
    r"^(?:"
    r"rock in rio|lollapalooza|glastonbury|coachella|tomorrowland|rock the bells"
    r"|festival(?:\s+[\w'ée\- ]+)?|carnaval\s+[\w'\- ]+|ver[ãa]o baiano"
    r"|rock oitentista|pop mpb(?:\s+anos\s*\d+)?|sertanejo raiz|dupla de ouro"
    r"|virada cultural|r[ée]veillon(?:\s+[\w'\- ]+)?"
    r")$",
    re.I,
)

RULES = [
    ("descriptive-phrase", DESCRIPTIVE),
    ("format-label", FORMAT_LABEL),
    ("event-name", EVENT_NAME),
]

# Titles rescued from the rules above because they are verifiably real songs.
# Keep this list short and only for names confirmed in a catalog.
ALLOWLIST = {
    "ao vivo e a cores",   # Matheus & Kauan feat. Anitta, 2018
    "especial",            # ambiguous alone; handled as suspect instead
}

# ------------------------------------------------------------ artist naming
# Scraped social handles that leaked in as display names. Real stylised names
# keep capitals or single tokens (Coma_Cose, Go_A, 88rising, mxmtoon), so
# require all-lowercase snake_case or an explicit _official suffix.
HANDLE = re.compile(r"^[a-z0-9]+(?:_[a-z0-9]+)+$|_official$")


def classify_title(title: str) -> str | None:
    n = norm(title)
    if n in ALLOWLIST:
        return None
    if FEATURE_SUFFIX.match(n) or (SCENE_SUFFIX.match(n) and GENRE_WORD.search(n)):
        return "genre-label"
    for reason, rx in RULES:
        if rx.match(n):
            return reason
    return None


def build_spread() -> set[str]:
    """Titles used by many unrelated artists across many years."""
    artists, years = defaultdict(set), defaultdict(set)
    for a1, a2, title, _ctype, year in COLLABORATIONS:
        n = norm(title)
        artists[n].update((a1, a2))
        years[n].add(year)
    return {
        n
        for n in artists
        if len(artists[n]) >= SPREAD_ARTISTS and len(years[n]) >= SPREAD_YEARS
    }


def degrees(rows: list[tuple]) -> dict[int, set[int]]:
    deg = defaultdict(set)
    for a1, a2, *_ in rows:
        if a1 != a2:
            deg[a1].add(a2)
            deg[a2].add(a1)
    return deg


def main() -> None:
    spread = build_spread()
    name = {i: n for (i, n, _g) in ARTISTS}

    verdicts = []
    counts = Counter()
    for idx, row in enumerate(COLLABORATIONS):
        a1, a2, title, ctype, year = row
        reason = classify_title(title)
        if reason:
            verdict = "fabricated"
        elif norm(title) in spread:
            verdict, reason = "suspect", "overused-title"
        else:
            verdict, reason = "trusted", ""
        counts[verdict] += 1
        verdicts.append(
            {
                "i": idx,
                "a1": a1,
                "a2": a2,
                "title": title,
                "type": ctype,
                "year": year,
                "verdict": verdict,
                "reason": reason,
            }
        )

    total = len(COLLABORATIONS)
    print("=" * 70)
    print("VEREDITO POR ARESTA")
    print("=" * 70)
    for v in ("fabricated", "suspect", "trusted"):
        print(f"  {v:11s} {counts[v]:6,d}  ({100 * counts[v] / total:.1f}%)")

    print()
    print("  por motivo:")
    for reason, n in Counter(
        v["reason"] for v in verdicts if v["verdict"] == "fabricated"
    ).most_common():
        print(f"    {reason:20s} {n:5,d}")

    print()
    print("  amostra do que sai (fabricated):")
    seen = set()
    for v in verdicts:
        if v["verdict"] != "fabricated" or v["title"] in seen:
            continue
        seen.add(v["title"])
        print(f"    [{v['reason']:18s}] {v['title']!r}  "
              f"{name.get(v['a1'], '?')} × {name.get(v['a2'], '?')}")
        if len(seen) >= 18:
            break

    # ------------------------------------------------------ blast radius
    kept = [
        COLLABORATIONS[v["i"]] for v in verdicts if v["verdict"] != "fabricated"
    ]
    before, after = degrees(COLLABORATIONS), degrees(kept)
    orphaned = sorted(
        i for (i, _n, _g) in ARTISTS if before.get(i) and not after.get(i)
    )

    print()
    print("=" * 70)
    print("IMPACTO NO GRAFO (removendo so os 'fabricated')")
    print("=" * 70)
    print(f"  arestas removidas : {counts['fabricated']:,}")
    print(f"  arestas restantes : {len(kept):,}")
    print(f"  artistas orfaos   : {len(orphaned):,}")
    if orphaned:
        print("  quem fica sem nenhuma conexao:")
        for i in orphaned[:20]:
            print(f"    - {name.get(i, i)}")
        if len(orphaned) > 20:
            print(f"    ... e mais {len(orphaned) - 20}")

    # ------------------------------------------------------ artist names
    handles = [(i, n) for (i, n, _g) in ARTISTS if HANDLE.search(n)]
    print()
    print("=" * 70)
    print("NOMES DE ARTISTA QUE SAO HANDLE, NAO NOME")
    print("=" * 70)
    print(f"  {len(handles)} artistas precisam de correcao de nome")
    for _i, n in handles[:15]:
        print(f"    {n}")
    if len(handles) > 15:
        print(f"    ... e mais {len(handles) - 15}")

    payload = {
        "totals": dict(counts),
        "orphaned_if_removed": [
            {"id": i, "name": name.get(i, "")} for i in orphaned
        ],
        "handle_names": [{"id": i, "name": n} for i, n in handles],
        "edges": verdicts,
    }
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=1)
    print()
    print(f"✅ veredito de {total:,} arestas escrito em data/edge_audit.json")


if __name__ == "__main__":
    main()
