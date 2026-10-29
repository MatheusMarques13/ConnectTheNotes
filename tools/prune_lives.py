"""Remove live rows no catalogue backs: all of them abroad, and in Brazil only
the ones neither Deezer nor MusicBrainz can find.

A live row is doubtful when nothing in data/edge_sources.json backs it. The
seeded data wrote stage appearances down as songs — "Cruel Summer (tribute)"
with Olivia Rodrigo and Taylor Swift never existed. Abroad, doubtful is enough
to drop it. In Brazil the live DVD is the main release format, so each row is
looked up. Most seeded Brazilian rows pair the right artists under the wrong
song — Bruno & Marrone and Leonardo never recorded "Sentimental Demais", but
they did record "Talismã (Ao Vivo)" — so when the exact song is missing but the
pair has a real joint recording, the row is retitled to it and the connection
survives. Only pairs with no joint recording anywhere are removed. Rows that came from a catalogue
(a released live album) are never touched.

Brazilian means either artist is, or the title is in Portuguese. The genre tag
alone misses Anitta ("Latin Pop") and Iza ("R&B/Pop"), so an artist also counts
when at least 30% of their collaborators carry a Brazilian tag.

Removed rows go to data/quarantine.json; confirmed ones get their catalogue id
in data/edge_sources.json. Lookups are cached in data/live_check.json, so an
interrupted run picks up where it stopped.

Run:  python3 tools/prune_lives.py [--dry-run]
"""
import json
import os
import re
import sys
import time
import urllib.parse
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, "data"))
from source_data import ARTISTS, COLLABORATIONS  # noqa: E402
from apply_audit import BR_TAGS, PT_TITLE, clean_title  # noqa: E402
import repair_edges as mb  # noqa: E402
import verify_br_pairs as dz  # noqa: E402

SOURCE = os.path.join(ROOT, "data", "source_data.py")
SOURCES = os.path.join(ROOT, "data", "edge_sources.json")
QUARANTINE = os.path.join(ROOT, "data", "quarantine.json")
CACHE = os.path.join(ROOT, "data", "live_check.json")

BR_PARTNER_SHARE = 0.3

# Positional, so "Runnin' (Dying to Live)" and "Long Live" stay songs.
LIVE = re.compile(
    r"[\(\[]\s*(?:live|ao vivo|en vivo)\b"
    r"|[\(\[][^)\]]*\b(?:ao vivo|en vivo|unplugged|tribute|tributo|homenagem|performance"
    r"|live (?:at|from|in|duet|version|session|tribute))\b"
    r"|[-–—]\s*(?:ao vivo|en vivo|live)\b"
    r"|\b(?:ao vivo|en vivo)\s*$",
    re.I,
)


def is_live(title: str, ctype: str) -> bool:
    return ctype in ("live", "dvd") or bool(LIVE.search(title))


def base(title: str) -> str:
    """Song title with the live tail and any parenthetical stripped."""
    t = re.sub(r"\s*[\(\[][^)\]]*[\)\]]", " ", title or "")
    t = re.sub(r"\s*[-–—]\s*(?:ao vivo|en vivo|live)\b.*$", "", t, flags=re.I)
    return dz.fold(t)


def brazilians() -> set[int]:
    genre = {i: g for (i, _n, g) in ARTISTS}
    tagged = {i for i, g in genre.items() if any(t in (g or "") for t in BR_TAGS)}
    partners = defaultdict(set)
    for a1, a2, *_ in COLLABORATIONS:
        partners[a1].add(a2)
        partners[a2].add(a1)
    return tagged | {
        i for i, p in partners.items() if p and len(p & tagged) / len(p) >= BR_PARTNER_SHARE
    }


def credited_on(n: str, names: list[str]) -> bool:
    """Is `n` among `names`? "Henrique & Juliano" must match "Henrique e Juliano"."""
    def norm(x: str) -> str:
        return f" {dz.fold(x)} ".replace(" e ", " ").replace(" and ", " ").strip()
    want = norm(n)
    return any(want == norm(x) or (len(want) > 3 and want in norm(x)) for x in names)


def on_deezer(n1: str, n2: str, title: str, taken: set[str]) -> dict | None:
    """Exact song first; failing that, any joint recording the pair does not have yet."""
    want = base(title)
    for query, exact in ((f"{n2} {want}", True), (n2, False)):
        for hit in dz.search(n1, query):
            time.sleep(dz.INTERVAL)
            if exact and base(hit.get("title") or "") != want:
                continue
            if not exact and base(hit.get("title") or "") in taken:
                continue
            track = dz.get(f"{dz.TRACK}{hit['id']}") or {}
            time.sleep(dz.INTERVAL)
            names = [c.get("name", "") for c in track.get("contributors") or []]
            if credited_on(n1, names) and credited_on(n2, names):
                year = (track.get("release_date") or "")[:4]
                return {"source": "deezer", "id": str(hit["id"]), "exact": exact,
                        "title": clean_title(hit.get("title") or title),
                        "year": int(year) if year.isdigit() else None}
    return None


def on_musicbrainz(n1: str, n2: str, title: str, taken: set[str]) -> dict | None:
    want = base(title)
    term = mb.LUCENE.sub(" ", want).strip()
    if term:
        for anchor in (n1, n2):
            qs = urllib.parse.urlencode({
                "query": f'recording:"{term}" AND artist:"{mb.term(anchor)}"',
                "fmt": "json", "limit": 10,
            })
            data = mb.get(f"{mb.BASE}?{qs}")
            time.sleep(mb.INTERVAL)
            for rec in (data or {}).get("recordings") or []:
                if base(rec.get("title") or "") == want and mb.credits_both(rec, n1, n2):
                    return {"source": "musicbrainz", "id": rec["id"], "exact": True,
                            "title": title, "year": None}
    data = mb.query_pair(n1, n2)
    time.sleep(mb.INTERVAL)
    for rec in (data or {}).get("recordings") or []:
        if base(rec.get("title") or "") not in taken and mb.credits_both(rec, n1, n2):
            return {"source": "musicbrainz", "id": rec["id"], "exact": False,
                    "title": clean_title(rec["title"]), "year": mb.year_of(rec)}
    return None


def _selfcheck() -> None:
    for t in ("Royals (Live Duet)", "Cruel Summer (tribute)", "Stan (Grammy Performance)",
              "Evidências - Ao Vivo", "Sozinho (Ao Vivo em Goiânia)"):
        assert is_live(t, "song"), t
    for t in ("Runnin' (Dying to Live)", "Long Live", "Live and Let Die",
              "Ao Vivo e a Cores", "I Don't Wanna Live Forever"):
        assert not is_live(t, "song"), t
    assert base("Evidências (Ao Vivo)") == base("Evidências - Ao Vivo") == "evidencias"


def main() -> None:
    _selfcheck()
    dry = "--dry-run" in sys.argv
    name = {i: n for (i, n, _g) in ARTISTS}
    prov = json.load(open(SOURCES, encoding="utf-8")) if os.path.exists(SOURCES) else {}
    br = brazilians()

    def sourced(a1: int, a2: int, title: str) -> bool:
        return f"{a1}-{a2}-{title}" in prov or f"{a2}-{a1}-{title}" in prov

    intl, local = [], []
    for i, (a1, a2, title, ctype, year) in enumerate(COLLABORATIONS):
        if not is_live(title, ctype) or sourced(a1, a2, title):
            continue
        is_br = a1 in br or a2 in br or bool(PT_TITLE.search(title))
        (local if is_br else intl).append(i)

    print(f"live internacional sem fonte (sai): {len(intl)}")
    print(f"live brasileira sem fonte (confere): {len(local)}", flush=True)
    if dry:
        print("(dry-run: nada consultado nem escrito)")
        return

    cache = json.load(open(CACHE, encoding="utf-8")) if os.path.exists(CACHE) else {}
    # Titles each pair already has, so a retitle never duplicates a real row.
    taken = defaultdict(set)
    for a1, a2, title, _c, _y in COLLABORATIONS:
        taken[(min(a1, a2), max(a1, a2))].add(base(title))
    started = time.time()
    for n, i in enumerate(local, 1):
        a1, a2, title, _c, year = COLLABORATIONS[i]
        key = f"{a1}|{a2}|{title}|{year}"
        if key in cache:
            continue
        n1, n2 = name[a1], name[a2]
        own = taken[(min(a1, a2), max(a1, a2))]
        hit = on_deezer(n1, n2, title, own) or on_musicbrainz(n1, n2, title, own)
        cache[key] = hit or {}
        if hit and not hit["exact"]:
            own.add(base(hit["title"]))
        tag = "--" if not hit else ("OK" if hit["exact"] else "->")
        extra = f"  ->  {hit['title']!r}" if hit and not hit["exact"] else ""
        print(f"  {tag} {n}/{len(local)}  {n1} × {n2} — {title!r}{extra}", flush=True)
        if n % 10 == 0:
            json.dump(cache, open(CACHE, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
            el = time.time() - started
            print(f"     [faltam ~{(len(local) - n) * el / n / 60:.0f} min]", flush=True)
    json.dump(cache, open(CACHE, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    drop, retitle = set(intl), {}
    for i in local:
        a1, a2, title, ctype, year = COLLABORATIONS[i]
        found = cache.get(f"{a1}|{a2}|{title}|{year}") or {}
        if not found.get("id"):
            drop.add(i)
            continue
        new_title = found["title"] if not found["exact"] else title
        if not found["exact"]:
            retitle[i] = (new_title, found.get("year") or year)
        prov[f"{a1}-{a2}-{new_title}"] = {"source": found["source"], "id": found["id"],
                                          "was": title}

    with open(SOURCE, encoding="utf-8") as fh:
        lines = fh.read().split("\n")
    start = next(k for k, l in enumerate(lines) if l.startswith("COLLABORATIONS"))
    first = start + 1
    tail = next(k for k, l in enumerate(lines[first:], first) if l.strip() == "]")
    if tail - first != len(COLLABORATIONS):
        sys.exit("❌ layout inesperado em source_data.py. Abortando.")

    kept, removed = [], []
    for i, row in enumerate(COLLABORATIONS):
        raw = lines[first + i]
        if i in retitle:
            a1, a2, _t, ctype, _y = row
            new_title, new_year = retitle[i]
            kept.append(f"    ({a1}, {a2}, {new_title!r}, {ctype!r}, {new_year}),")
            continue
        if i not in drop:
            kept.append(raw)
            continue
        a1, a2 = row[0], row[1]
        removed.append({
            "row": list(row), "line": raw.strip(),
            "artists": [name.get(a1, ""), name.get(a2, "")],
            "pair": [name.get(a1, ""), name.get(a2, "")],
            "reason": ("live sem fonte (internacional)" if i in set(intl)
                       else "live BR nao encontrada no Deezer nem no MusicBrainz"),
            "searched": 0 if i in set(intl) else 2,
        })
    lines[first:tail] = kept
    with open(SOURCE, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))

    q = json.load(open(QUARANTINE, encoding="utf-8")) if os.path.exists(QUARANTINE) else {"removed": []}
    q["removed"].extend(removed)
    json.dump(q, open(QUARANTINE, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    json.dump(prov, open(SOURCES, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    gone_br = len(drop) - len(intl)
    print(f"\n✅ internacionais removidas: {len(intl)}")
    print(f"✅ brasileiras: {len(local) - gone_br - len(retitle)} confirmadas, "
          f"{len(retitle)} com titulo corrigido, {gone_br} removidas (dupla sem gravacao conjunta)")


if __name__ == "__main__":
    main()
