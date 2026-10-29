"""Check every seeded row against a catalogue: keep, retitle, or drop.

~13.7k rows came from the seed with no catalogue record behind them. "I Know
Alone (Remix)" with Olivia Rodrigo and Gracie Abrams is one; it does not exist.
Each row is looked up the way tools/prune_lives.py checks Brazilian lives,
Deezer first and MusicBrainz for what Deezer misses:

    the song exists with both artists        kept, catalogue id recorded
    the pair recorded together, other song   retitled to that recording
    neither catalogue has them together      removed, unless bandmates —
                                             catalogues credit "Cream",
                                             never "Eric Clapton"
    a lookup failed                          kept, retried on the next run

The exact song is looked for in BOTH catalogues before any retitle. Deezer
credits "SICKO MODE" to Travis Scott alone; asked on its own it would trade the
row for "Fair Trade". MusicBrainz has Drake on it.

Phases, in this order; each is cached, resumable, and takes --shard k/n to run
in parallel. A phase only picks up rows the previous one has answered, so it can
be rerun while that one is still going.

    --exact      Deezer, exact song
    --mb-exact   MusicBrainz, exact song, for every row: gated on Deezer having
                 it under one name, "Garota de Ipanema" became "Overture"
    --pair       Deezer, any joint recording of the pair
    --mb-pair    MusicBrainz, any joint recording of the pair
    --rescue     last look before dropping: title-first Deezer, MusicBrainz again
    --group      the song credited to one of the artists' groups (Migos for Offset)
    --apply      band check, web second opinion, then rewrite
    --restore    put back removed rows a later web check confirmed
"""
import glob
import json
import os
import random
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
sys.path.insert(0, HERE)
from prune_lives import (  # noqa: E402
    CATALOGUES, COLLABORATIONS, DZ_NAMES, NAME, QUARANTINE, SOURCE, SOURCES, check_rows, is_live, junk_title,
    on_track, plan, rewrite, row_key, save_json, song_key, verdict,
)
import repair_edges as mb  # noqa: E402
import verify_br_pairs as dz  # noqa: E402
import verify_via_works as vw  # noqa: E402

CACHE = os.path.join(ROOT, "data", "old_rows_check.json")
GROUPS = os.path.join(ROOT, "data", "artist_groups.json")
FAME = os.path.join(ROOT, "data", "artist_fame.json")
WEB = os.path.join(ROOT, "data", "web_check.json")    # second opinion from a web search
PRUNED = os.path.join(ROOT, "data", "pruned_artists.json")
VETO = os.path.join(ROOT, "data", "old_rows_veto.json")  # catalogue ids the strict name match rejected
DROP_REASON = "nao existe no Deezer nem no MusicBrainz"
WDQS = "https://query.wikidata.org/sparql"

# Deezer allows 50 requests per 5 s per IP. Three shards at this pace stay
# under it; a quota error is retried by verify_br_pairs.get, never read as
# "not found".
dz.INTERVAL = 0.13


def unsourced(prov: dict) -> list[int]:
    return [
        i for i, (a1, a2, t, _c, _y) in enumerate(COLLABORATIONS)
        if f"{a1}-{a2}-{t}" not in prov and f"{a2}-{a1}-{t}" not in prov
    ]


def usable(entry: dict) -> bool:
    """An answer we keep: the row's own song, or a real joint recording."""
    return bool(entry.get("id")) and (entry.get("exact") or not junk_title(entry.get("title", "")))


def normalize(entry: dict) -> dict:
    """Send answers from the first pair search back for another look.

    It took the first joint song in the hits, so "Baby" became "Peaches (Remix)"
    while "Baby" sat further down, and it took DJ mashups for duets. What
    MusicBrainz already said about a pair is kept.
    """
    tried = entry.get("tried", [])
    if entry.get("id"):
        stale = (entry.get("source") == "deezer" and not entry.get("exact")
                 and entry.get("via") != "deezer-pair-v2")
        return {"tried": ["deezer-exact", "musicbrainz-exact"]} if stale or not usable(entry) else entry
    if "deezer-pair" in tried:
        return {**entry, "tried": [t for t in tried if t != "deezer-pair"]}
    return entry


def load_cache() -> dict:
    """Merge the per-writer caches; a usable answer beats anything else."""
    merged: dict = {}
    veto = json.load(open(VETO, encoding="utf-8")) if os.path.exists(VETO) else {}
    for path in sorted(glob.glob(CACHE.replace(".json", "*.json"))):
        for attempt in range(3):                     # a writer from an older run may be mid-dump
            try:
                with open(path, encoding="utf-8") as fh:
                    data = json.load(fh)
                break
            except json.JSONDecodeError:
                if attempt == 2:
                    raise
                time.sleep(2)
        for key, raw in data.items():
            entry, old = normalize(raw), merged.get(key)
            if entry.get("id") in veto.get(key, ()):
                entry = {"tried": list(CATALOGUES)}    # the credit was someone else: not found
            if old is None or (usable(entry) and not usable(old)) or (
                not usable(old) and not usable(entry)
                and len(entry.get("tried", [])) > len(old.get("tried", []))
            ):
                merged[key] = entry
    return merged


def _sparql(query: str) -> list[dict]:
    req = urllib.request.Request(
        WDQS, data=urllib.parse.urlencode({"query": query, "format": "json"}).encode(),
        headers={"User-Agent": "ConnectTheNotes/0.1 ( matheusbmarques13@gmail.com )",
                 "Accept": "application/sparql-results+json"})
    for attempt in range(6):                        # WDQS rations query time: 429 means wait
        try:
            with urllib.request.urlopen(req, timeout=120, context=dz.SSL_CTX) as fh:
                return json.load(fh)["results"]["bindings"]
        except urllib.error.HTTPError as exc:
            if exc.code not in (429, 500, 502, 503, 504) or attempt == 5:
                raise
            time.sleep(int(exc.headers.get("Retry-After") or 30))
    return []


# ?g must be a music act (has a MusicBrainz id): "member of" also lists academies.
MEMBERSHIP = """{{ ?p wdt:P463 ?g . }} UNION {{ ?g wdt:P527 ?p . }}
          ?g wdt:P434 [] .
          OPTIONAL {{ ?g wdt:P2722 ?gdz . }}
          OPTIONAL {{ ?g rdfs:label ?gl . FILTER(LANG(?gl) = "en") }}"""


def wikidata_groups() -> dict[str, set[str]]:
    """Each roster artist's bands and members, from Wikidata.

    Matched by Deezer id first, then by name for the rest: Marcelo Camelo has
    no Deezer id on Wikidata, and the id we hold for Lauryn Hill is someone
    else's. A few batched queries instead of two MusicBrainz calls for each of
    ~5k artists. Raises on failure: rows are never dropped without this guard.
    """
    fame = json.load(open(FAME, encoding="utf-8"))
    by_dz: dict[str, set[str]] = {}
    for aid, v in (fame.get("artists") or fame).items():
        if isinstance(v, dict) and v.get("dz") and int(aid) in NAME:
            by_dz.setdefault(str(v["dz"]), set()).add(NAME[int(aid)])
    out: dict[str, set[str]] = {}

    def add(people: set[str], r: dict) -> None:
        v = lambda f: (r.get(f) or {}).get("value")              # noqa: E731
        qid = v("g").rsplit("/", 1)[-1]
        group = by_dz.get(v("gdz") or "") or {v("gl") or qid}
        for n in people:
            out.setdefault(n, set()).update(group | {qid})       # the id settles shared groups

    ids = sorted(by_dz)
    for k in range(0, len(ids), 1500):
        values = " ".join(f'"{x}"' for x in ids[k:k + 1500])
        for r in _sparql(f"""SELECT ?pdz ?g ?gl ?gdz WHERE {{
          VALUES ?pdz {{ {values} }}
          ?p wdt:P2722 ?pdz .
          {MEMBERSHIP}
        }}"""):
            add(by_dz[r["pdz"]["value"]], r)
    names = sorted({n for n in NAME.values() if '"' not in n and "\\" not in n})
    for k in range(0, len(names), 700):
        values = " ".join(f'"{n}"@en "{n}"@pt' for n in names[k:k + 700])
        for r in _sparql(f"""SELECT ?pl ?g ?gl ?gdz WHERE {{
          VALUES ?pl {{ {values} }}
          ?p rdfs:label ?pl .
          {MEMBERSHIP}
        }}"""):
            add({r["pl"]["value"]}, r)
    return out


def web_title(w: dict, title: str) -> str:
    """The recording a web verdict vouches for. A remixer's remix ("Move Your
    Body (Alan Walker Remix)") is not a collaboration, however it is credited."""
    return w["title"] if w.get("verdict") == "other" and w.get("title") else title


def rescue_from_web(drop: dict[int, str], retitle: dict, prov: dict) -> int:
    """Rows both catalogues missed but a web search found, re-checked by a second
    search: kept, or retitled to the joint recording that was found."""
    web = json.load(open(WEB, encoding="utf-8")) if os.path.exists(WEB) else {}
    taken = {}
    for a1, a2, t, _c, _y in COLLABORATIONS:
        taken.setdefault((min(a1, a2), max(a1, a2)), set()).add(song_key(t))
    rescued = 0
    for i in list(drop):
        w = web.get(row_key(i)) or {}
        if not w.get("confirmed") or junk_title(web_title(w, COLLABORATIONS[i][2])):
            continue
        a1, a2, title, _c, year = COLLABORATIONS[i]
        new_title = title
        if w["verdict"] == "other" and w.get("title"):
            own = taken[(min(a1, a2), max(a1, a2))]
            if song_key(w["title"]) in own:        # the pair already has that song
                continue
            new_title = w["title"]
            own.add(song_key(new_title))
            retitle[i] = (new_title, w.get("year") or year)
        prov[f"{a1}-{a2}-{new_title}"] = {"source": "web", "id": w.get("check_url") or w.get("url"),
                                          "was": title}
        del drop[i]
        rescued += 1
    return rescued


def restore_from_web() -> int:
    """Put back removed rows a later web check confirmed, and their artists."""
    web = json.load(open(WEB, encoding="utf-8")) if os.path.exists(WEB) else {}
    q = json.load(open(QUARANTINE, encoding="utf-8"))
    pruned = json.load(open(PRUNED, encoding="utf-8")) if os.path.exists(PRUNED) else {"removed": []}
    prov = json.load(open(SOURCES, encoding="utf-8"))
    taken = {}
    for a1, a2, t, _c, _y in COLLABORATIONS:
        taken.setdefault((min(a1, a2), max(a1, a2)), set()).add(song_key(t))
    rows, kept = [], []
    for item in q["removed"]:
        a1, a2, title, ctype, year = item["row"]
        w = web.get(f"{a1}|{a2}|{title}|{year}") or {}
        if item.get("reason") != DROP_REASON or not w.get("confirmed") or junk_title(web_title(w, title)):
            kept.append(item)
            continue
        if w["verdict"] == "other" and w.get("title"):
            title, year, ctype = w["title"], w.get("year") or year, "live" if is_live(w["title"], "") else "song"
        own = taken.setdefault((min(a1, a2), max(a1, a2)), set())
        if song_key(title) not in own:              # else the pair already has that song
            own.add(song_key(title))
            rows.append(f"    ({a1}, {a2}, {title!r}, {ctype!r}, {year}),")
            prov[f"{a1}-{a2}-{title}"] = {"source": "web", "id": w.get("check_url") or w.get("url"),
                                          "was": item["row"][2]}
    need = {int(x) for line in rows for x in line.strip(" (),").split(",")[:2]} - set(NAME)
    artists = [a for a in pruned["removed"] if a["id"] in need]
    pruned["removed"] = [a for a in pruned["removed"] if a["id"] not in need]
    with open(SOURCE, encoding="utf-8") as fh:
        lines = fh.read().split("\n")
    a_end = next(k for k, l in enumerate(lines) if l.startswith("ARTISTS")) + len(NAME) + 1
    c_end = next(k for k, l in enumerate(lines) if l.startswith("COLLABORATIONS")) + len(COLLABORATIONS) + 1
    if lines[a_end] != "]" or lines[c_end] != "]":
        sys.exit("❌ layout inesperado em source_data.py. Abortando.")
    lines[c_end:c_end] = rows                      # the later block first, so a_end stays valid
    lines[a_end:a_end] = ["    " + a["line"] for a in artists]
    with open(SOURCE, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))
    q["removed"] = kept
    save_json(QUARANTINE, q)
    save_json(PRUNED, pruned)
    save_json(SOURCES, prov)
    print(f"✅ de volta: {len(rows)} linhas, {len(artists)} artistas")
    return len(rows)


def spare_bandmates(drop: dict[int, str]) -> int:
    """Rows between bandmates stay: catalogues credit "Cream", never "Eric Clapton"."""
    groups = json.load(open(GROUPS, encoding="utf-8")) if os.path.exists(GROUPS) else {}
    for name, related in wikidata_groups().items():
        groups[name] = sorted(set(groups.get(name, [])) | related)
    json.dump(groups, open(GROUPS, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    vw._LINKED = None                                  # reload with the new memberships
    spared = [i for i in drop
              if vw.bandmates(NAME[COLLABORATIONS[i][0]], NAME[COLLABORATIONS[i][1]])]
    for i in spared:
        del drop[i]
    return len(spared)


def recheck(prov: dict, cache: dict) -> None:
    """Re-read the evidence behind accepted rows with the strict name match.

    Earlier passes let a name match inside a longer one: "Luan Santana" stood
    for Santana, and on MusicBrainz "MØ" (folded "m") matched any credit with an
    m in it. Only rows with a short name, or one inside another roster name, can
    have matched that way. A rejected id is vetoed for seeded rows; rows confirmed
    by earlier tools lose their source and are looked up again. Review the
    rejections by hand before applying: two roster nodes can be one person
    ("Pharrell" and "Pharrell Williams"), and then the match was right.
    """
    folded = {i: mb.fold(n) for i, n in NAME.items()}
    every = set(folded.values())
    risky = {i for i, f in folded.items() if len(f) <= 4 or any(g != f and f in g for g in every)}
    todo = []                                         # (where, key, a1, a2, source, id)
    for i in unsourced(prov):
        e = cache.get(row_key(i)) or {}
        if e.get("id") and {*COLLABORATIONS[i][:2]} & risky:
            todo.append(("cache", row_key(i), *COLLABORATIONS[i][:2], e["source"], e["id"]))
    for k, x in prov.items():
        a1, a2 = (int(t) for t in k.split("-", 2)[:2])
        if x.get("source") in ("deezer", "musicbrainz") and x.get("id") and {a1, a2} & risky:
            todo.append(("prov", k, a1, a2, x["source"], x["id"]))

    def names(a1: int, a2: int) -> list[tuple[str, str]]:
        n1, n2 = NAME[a1], NAME[a2]
        return [(n1, n2), (DZ_NAMES.get(n1, n1), DZ_NAMES.get(n2, n2))]

    recs: dict[str, dict] = {}
    mbids = sorted({t[5] for t in todo if t[4] == "musicbrainz"})
    for k in range(0, len(mbids), 50):                # one search answers 50 recording ids
        q = " OR ".join(f'rid:"{x}"' for x in mbids[k:k + 50])
        data = mb.get(f"{mb.BASE}?{urllib.parse.urlencode({'query': q, 'fmt': 'json', 'limit': 100})}")
        time.sleep(mb.INTERVAL)
        for rec in (data or {}).get("recordings") or []:
            recs[rec["id"]] = rec
    veto = json.load(open(VETO, encoding="utf-8")) if os.path.exists(VETO) else {}
    rejected = []
    for n, (where, key, a1, a2, source, rid) in enumerate(todo, 1):
        if source == "deezer":
            track = dz.get(f"{dz.TRACK}{rid}")
            time.sleep(dz.INTERVAL)
            if track is None:
                continue                              # lookup failed: keep, never guess
            people = track.get("contributors") or []
            ok = any(on_track(x, people) and on_track(y, people) for x, y in names(a1, a2))
        else:
            if rid not in recs:
                continue
            ok = any(mb.credits_both(recs[rid], x, y) for x, y in names(a1, a2))
        if not ok:
            rejected.append((where, key, a1, a2))
            if where == "cache":
                veto.setdefault(key, []).append(rid)
            else:
                prov.pop(key, None)
        if n % 200 == 0 or n == len(todo):
            print(f"  {n}/{len(todo)}  rejeitadas {len(rejected)}", flush=True)
    save_json(VETO, veto)
    save_json(SOURCES, prov)
    print(f"\n✅ reconferidas {len(todo):,} provas | rejeitadas {len(rejected):,} "
          f"(linhas do seed {sum(r[0] == 'cache' for r in rejected):,}, "
          f"ja publicadas {sum(r[0] == 'prov' for r in rejected):,})")
    for where, key, a1, a2 in rejected[:40]:
        print(f"  {where:5s} {NAME[a1]} × {NAME[a2]} — {key}")


def shard_of(i: int, n: int) -> int:
    a, b = sorted(COLLABORATIONS[i][:2])           # by pair: one retitle owner per pair
    return (a * 1_000_003 + b) % n


PHASES = {                        # flag -> (lookup, lookups that must have answered first)
    "--exact": ("deezer-exact", set()),
    "--mb-exact": ("musicbrainz-exact", {"deezer-exact"}),
    "--pair": ("deezer-pair-v2", {"deezer-exact", "musicbrainz-exact"}),
    "--mb-pair": ("musicbrainz-pair", {"deezer-exact", "musicbrainz-exact", "deezer-pair-v2"}),
    "--rescue": ("rescue", {"deezer-exact", "musicbrainz-exact", "deezer-pair-v2", "musicbrainz-pair"}),
    "--group": ("group-credit", {"deezer-exact", "musicbrainz-exact", "deezer-pair-v2", "musicbrainz-pair",
                                 "rescue"}),
}


def main() -> None:
    prov = json.load(open(SOURCES, encoding="utf-8"))
    rows = unsourced(prov)
    cache = load_cache()

    if "--restore" in sys.argv:
        restore_from_web()
        return

    if "--recheck" in sys.argv:
        recheck(prov, cache)
        return

    if "--apply" in sys.argv:
        drop, retitle = plan(rows, cache, prov, DROP_REASON)
        rescued = rescue_from_web(drop, retitle, prov)
        spared = spare_bandmates(drop)
        print(f"achadas na web e conferidas: {rescued:,}")
        unknown = sum(verdict(cache.get(row_key(i))) == "unknown" for i in rows)
        if "--dry-run" in sys.argv:
            show = lambda i: "{} × {} — {!r}".format(NAME[COLLABORATIONS[i][0]], NAME[COLLABORATIONS[i][1]], COLLABORATIONS[i][2])  # noqa: E731
            print(f"sairiam {len(drop):,}, titulo trocado {len(retitle):,}, banda {spared:,}, sem resposta {unknown:,}")
            for i in random.Random(1).sample(sorted(drop), min(25, len(drop))):
                print("  sai  ", show(i))
            for i in random.Random(1).sample(sorted(retitle), min(25, len(retitle))):
                print("  troca", show(i), "->", repr(retitle[i][0]))
            return
        rewrite(drop, retitle, prov)
        save_json(CACHE, cache)                       # one audit file instead of one per writer
        for path in glob.glob(CACHE.replace(".json", ".*.json")):
            os.remove(path)
        print(f"\n✅ conferidas: {len(rows):,} | mantidas como estavam: "
              f"{len(rows) - len(drop) - len(retitle) - spared - unknown:,}")
        print(f"✅ titulo corrigido: {len(retitle):,} | removidas: {len(drop):,} | "
              f"poupadas por serem da mesma banda: {spared:,} | sem resposta (ficam): {unknown:,}")
        return

    flag = next((f for f in PHASES if f in sys.argv), "--exact")
    src, needs = PHASES[flag]
    tag = flag.strip("-")
    if "--shard" in sys.argv:
        k, n = (int(x) for x in sys.argv[sys.argv.index("--shard") + 1].split("/"))
        rows = [i for i in rows if shard_of(i, n) == k]   # by pair: one retitle owner per pair
        tag += f".{k}"
    path = CACHE.replace(".json", f".{tag}.json")         # one file per writer
    todo = []
    for i in rows:
        e = cache.get(row_key(i)) or {}
        if e.get("id") or not needs <= set(e.get("tried", [])) or src in e.get("tried", []):
            continue
        todo.append(i)
    fame = json.load(open(FAME, encoding="utf-8"))
    fans = {int(k): x.get("fans") or 0 for k, x in (fame.get("artists") or fame).items() if isinstance(x, dict)}
    # Famous pairs first: a run cut short has still covered what players see.
    todo.sort(key=lambda i: -min(fans.get(COLLABORATIONS[i][0], 0), fans.get(COLLABORATIONS[i][1], 0)))
    save_json(path, cache)                                # skips visible to the next phase now
    check_rows(todo, cache, path, (src,))


if __name__ == "__main__":
    main()
