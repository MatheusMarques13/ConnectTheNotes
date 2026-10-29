"""Remove live rows no catalogue backs: all of them abroad, and in Brazil only
the ones neither Deezer nor MusicBrainz can find.

A live row is doubtful when nothing in data/edge_sources.json backs it. The
seeded data wrote stage appearances down as songs — "Cruel Summer (tribute)"
with Olivia Rodrigo and Taylor Swift never existed. Abroad, doubtful is enough
to drop it. In Brazil the live DVD is the main release format, so each row is
looked up. Most seeded Brazilian rows pair the right artists under the wrong
song — Bruno & Marrone and Leonardo never recorded "Sentimental Demais", but
they did record "A Rotina (Ao Vivo)" — so when the exact song is missing but the
pair has a real joint recording, the row is retitled to it and the connection
survives. Only pairs with no joint recording anywhere are removed.

A lookup that fails (network, quota) is never read as "not found": the row is
kept and retried on the next run. tools/verify_old_rows.py reuses this machinery
for every seeded row.

Brazilian means either artist is, or the title is in Portuguese. The genre tag
alone misses Anitta ("Latin Pop") and Iza ("R&B/Pop"), so an artist also counts
when at least 30% of their collaborators carry a Brazilian tag.

Removed rows go to data/quarantine.json; confirmed ones get their catalogue id
in data/edge_sources.json. Lookups are cached in data/live_check.json.

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
from harvest_recent import classify  # noqa: E402
import verify_br_pairs as dz  # noqa: E402

SOURCE = os.path.join(ROOT, "data", "source_data.py")
SOURCES = os.path.join(ROOT, "data", "edge_sources.json")
QUARANTINE = os.path.join(ROOT, "data", "quarantine.json")
CACHE = os.path.join(ROOT, "data", "live_check.json")

BR_PARTNER_SHARE = 0.3
NAME = {i: n for (i, n, _g) in ARTISTS}


def _deezer_ids() -> tuple[dict[str, set[int]], dict[str, str]]:
    """Roster name -> Deezer artist ids, and -> Deezer's own spelling when it
    differs ("Tom Jobim" is "Antônio Carlos Jobim" there). From artist_fame.json."""
    path = os.path.join(ROOT, "data", "artist_fame.json")
    if not os.path.exists(path):
        return {}, {}
    fame = json.load(open(path, encoding="utf-8"))
    ids: dict[str, set[int]] = {}
    names: dict[str, str] = {}
    for aid, v in (fame.get("artists") or fame).items():
        if isinstance(v, dict) and v.get("dz") and int(aid) in NAME:
            ours = NAME[int(aid)]
            ids.setdefault(ours, set()).add(int(v["dz"]))
            if v.get("name") and dz.fold(v["name"]) != dz.fold(ours):
                names[ours] = v["name"]
    return ids, names


DZ_IDS, DZ_NAMES = _deezer_ids()

# Positional, so "Runnin' (Dying to Live)" and "Long Live" stay songs.
LIVE = re.compile(
    r"[\(\[]\s*(?:live|ao vivo|en vivo)\b"
    r"|[\(\[][^)\]]*\b(?:ao vivo|en vivo|unplugged|tribute|tributo|homenagem|performance"
    r"|live (?:at|from|in|duet|version|session|tribute))\b"
    r"|[-–—]\s*(?:ao vivo|en vivo|live)\b"
    r"|\b(?:ao vivo|en vivo)\s*$",
    re.I,
)


# Compilations credit every singer whose song is spliced in: Deezer lists Yo Yo
# Honey Singh and Badshah on "Punjabi Mashup", which neither sang with the other.
COMPILATION = re.compile(
    r"\bmash-?up\b|\bnon[- ]?stop\b|\b(?:party|dance|lo-?fi|chart|hit) ?mix\b|\blo-?fi\b|\bmedley of\b"
    r"|\bmix\s*(?::|\d)|[-–]\s*dj\b|\bmix\s*$|\b(?:chart|greatest|top) hits\b",   # "Reggae Mix 1", "Chart Hits: Extended"
    re.I,
)
# Several songs in one title ("Bad Blood / Royals / Hold Up") is a DJ splice,
# unless it is a live pot-pourri or a session: the DVD format of pagode and
# sertanejo, where both did sing it together.
SONG_LIST = re.compile(r"\s/\s.*\s/\s")
SESSION = re.compile(r"\bsessions?\b", re.I)
GENERIC = re.compile(r"^(?:intro|outro|interlude|skit)(?: \d+)?$")     # a bare "Intro" names no song
BRACKET = re.compile(r"[\(\[]([^)\]]*)[\)\]]")
MIX_WORD = re.compile(r"\b(?:re)?mix\b", re.I)


def remixer_credit(title: str) -> bool:
    """"(Marshmello Remix)", "(Club Mix)", "- Sounds Right Mix": a remixer or a
    version, not a guest. A bare "(Remix)" is the posse remix the guests sing
    on, and stays."""
    tail = re.split(r"\s[-–—]\s", title or "")[1:]          # "Get Real - Sounds Right Mix"
    for group in BRACKET.findall(title or "") + tail[-1:]:
        m = MIX_WORD.search(group)
        if m and set(dz.fold(group[:m.start()]).split()) - {"official", "the", "a"}:
            return True
    return False


def junk_title(title: str) -> bool:
    """Not a recording two artists made together, whatever the credits say."""
    t = title or ""
    return (not re.search(r"\w", BRACKET.sub("", t))   # "♡", "$$$ (feat. Gunna)": no song name
            or classify(t) is None or remixer_credit(t)
            or bool(COMPILATION.search(t) or COMPILATION.search(BRACKET.sub(" ", t).strip()))
            or (bool(SONG_LIST.search(BRACKET.sub(" ", t))) and not (LIVE.search(t) or SESSION.search(t)))
            or bool(GENERIC.match(song_key(t))))


class LookupFailed(Exception):
    """A catalogue did not answer. Never the same thing as "not found"."""


def save_json(path: str, obj) -> None:
    """Temp file + rename: a parallel reader never sees a half-written file."""
    with open(path + ".tmp", "w", encoding="utf-8") as fh:
        json.dump(obj, fh, ensure_ascii=False, indent=1)
    os.replace(path + ".tmp", path)


def is_live(title: str, ctype: str) -> bool:
    return ctype in ("live", "dvd") or bool(LIVE.search(title))


def base(title: str) -> str:
    """Song title with the live tail and any parenthetical stripped."""
    t = re.sub(r"['’`´]", "", title or "")            # "What's Poppin" is "WHATS POPPIN"
    t = re.sub(r"\s*[\(\[][^)\]]*[\)\]]", " ", t)
    t = re.sub(r"\s*[-–—]\s*(?:ao vivo|en vivo|live)\b.*$", "", t, flags=re.I)
    return dz.fold(t)


# "Savage (Remix)" on our side is "Savage Remix (feat. Beyoncé)" on Deezer.
VARIANT_TAIL = re.compile(r"(?:\s+(?:remix|mix|version|edit|live|ao vivo|en vivo|acustico|acoustic))+$")


def song_key(title: str) -> str:
    """base() without a trailing version word, so a remix row meets its remix."""
    return VARIANT_TAIL.sub("", base(title))


def row_key(i: int) -> str:
    a1, a2, title, _c, year = COLLABORATIONS[i]
    return f"{a1}|{a2}|{title}|{year}"


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


def _norm(x: str) -> str:
    return f" {dz.fold(x)} ".replace(" e ", " ").replace(" and ", " ").strip()


ROSTER = {_norm(n) for n in NAME.values()}


DESCRIPTOR = re.compile(r"\s+(?:of|from)\s+.*$|\s*\((?:of\s+)?[^)]*\)\s*$", re.I)
JOINER = re.compile(r"\s*(?:&|,|\+|/|\bvs\.?|\band\b|\be\b|\bx\b)\s*", re.I)


def contains_act(want: str, credit: str, roster: set[str], norm) -> bool:
    """Is the act `want` (normalized) inside the longer `credit`?

    Whole words only: "m" (MØ) is in every credit, "tini" in "Tinie Tempah",
    "mora" in "Morad". And when the credit is another act we know, only as one
    of its joined parts: "Wisin & Yandel" holds Wisin, "Luan Santana" does not
    hold Santana, "Camila Cabello" is not the band Camila.
    """
    credit = DESCRIPTOR.sub("", credit)          # "Jimin of BTS" credits Jimin, not BTS
    got = norm(credit)
    if len(want) <= 3 or f" {want} " not in f" {got} ":
        return False
    return got not in roster or want in {norm(p) for p in JOINER.split(credit)}


def credited_on(n: str, names: list[str]) -> bool:
    """Is `n` among `names`? "Henrique & Juliano" must match "Henrique e Juliano"."""
    want = _norm(n)
    return any(want == _norm(x) or contains_act(want, x, ROSTER, _norm) for x in names)


def on_track(n: str, contributors: list[dict]) -> bool:
    """By name, or by Deezer id when the names differ ("mo" is "MØ")."""
    return (credited_on(n, [c.get("name", "") for c in contributors])
            or bool(DZ_IDS.get(n, set()) & {c.get("id") for c in contributors}))


_TRACKS: dict[str, dict] = {}
_PAIRS: dict[tuple, list | dict] = {}       # one pair search serves all of the pair's rows


def deezer_track(track_id) -> dict:
    tid = str(track_id)
    if tid not in _TRACKS:
        track = dz.get(f"{dz.TRACK}{tid}")
        time.sleep(dz.INTERVAL)
        if track is None:
            raise LookupFailed(f"deezer track {tid}")
        _TRACKS[tid] = track
    return _TRACKS[tid]


def _found(source: str, rid: str, exact: bool, title: str, year: int | None) -> dict:
    return {"source": source, "id": rid, "exact": exact, "title": title, "year": year}


def deezer_exact(n1: str, n2: str, title: str, taken: set[str]) -> dict:
    """The row's own song on Deezer, crediting both.

    On a miss, records whether Deezer has the song under one of them. That case
    is ambiguous — "SICKO MODE" is credited to Travis Scott alone on Deezer,
    Drake's verse and all — so it earns a MusicBrainz look before any retitle.
    """
    want = song_key(title)
    hits = dz.search(n1, f"{n2} {base(title)}")
    time.sleep(dz.INTERVAL)
    if hits is None:
        raise LookupFailed(f"deezer search {n1} / {n2} {want}")
    by_one = False
    for hit in hits:
        if song_key(hit.get("title") or "") != want:
            continue
        people = deezer_track(hit["id"]).get("contributors") or []
        a, b = on_track(n1, people), on_track(n2, people)
        if a and b:
            return _found("deezer", str(hit["id"]), True, title, None)
        by_one = by_one or a or b
    return {"title_by_one": by_one}


def deezer_pair(n1: str, n2: str, title: str, taken: set[str]) -> dict | None:
    """Any joint recording of the pair on Deezer the dataset does not have yet."""
    want = song_key(title)
    hits = _PAIRS.get(("deezer", n1, n2))
    if hits is None:
        hits = dz.search(n1, n2)
        time.sleep(dz.INTERVAL)
        if hits is None:
            raise LookupFailed(f"deezer search {n1} / {n2}")
        _PAIRS[("deezer", n1, n2)] = hits
    for hit in sorted(hits, key=lambda h: song_key(h.get("title") or "") != want):
        got = song_key(hit.get("title") or "")
        if got != want and (got in taken or junk_title(hit.get("title") or "")):
            continue
        track = deezer_track(hit["id"])
        people = track.get("contributors") or []
        if on_track(n1, people) and on_track(n2, people):
            year = (track.get("release_date") or "")[:4]
            exact = got == want
            found = _found("deezer", str(hit["id"]), exact,
                           title if exact else clean_title(hit.get("title") or title),
                           int(year) if year.isdigit() else None)
            return {**found, "via": "deezer-pair-v2"}
    return None


def musicbrainz_exact(n1: str, n2: str, title: str, taken: set[str]) -> dict | None:
    want = song_key(title)
    term = mb.LUCENE.sub(" ", base(title)).strip()
    if not term or not mb.term(n1) or not mb.term(n2):
        return None
    # Both names in one query: the artist field holds every credited act, so
    # this finds guests too, in one request instead of one per anchor.
    qs = urllib.parse.urlencode({
        "query": f'recording:"{term}" AND artist:"{mb.term(n1)}" AND artist:"{mb.term(n2)}"',
        "fmt": "json", "limit": 10,
    })
    data = mb.get(f"{mb.BASE}?{qs}")
    time.sleep(mb.INTERVAL)
    if data is None:
        raise LookupFailed(f"musicbrainz search {term} / {n1} / {n2}")
    for rec in data.get("recordings") or []:
        if song_key(rec.get("title") or "") == want and mb.credits_both(rec, n1, n2):
            return _found("musicbrainz", rec["id"], True, title, None)
    return None


def musicbrainz_pair(n1: str, n2: str, title: str, taken: set[str]) -> dict | None:
    if not mb.term(n1) or not mb.term(n2):
        return None
    want = song_key(title)
    data = _PAIRS.get(("musicbrainz", n1, n2))
    if data is None:
        data = mb.query_pair(n1, n2)
        time.sleep(mb.INTERVAL)
        if data is None:
            raise LookupFailed(f"musicbrainz pair {n1} / {n2}")
        _PAIRS[("musicbrainz", n1, n2)] = data
    recs = data.get("recordings") or []
    for rec in sorted(recs, key=lambda r: song_key(r.get("title") or "") != want):
        got = song_key(rec.get("title") or "")
        if got != want and (got in taken or junk_title(rec.get("title") or "")):
            continue
        if mb.credits_both(rec, n1, n2):
            exact = got == want
            return _found("musicbrainz", rec["id"], exact,
                          title if exact else clean_title(rec["title"]), mb.year_of(rec))
    return None


def deezer_title_first(n1: str, n2: str, title: str, taken: set[str]) -> dict:
    """The row's own song searched as "<title> <artist>", once per artist.

    "<a> <b> <title>" puts karaoke and tribute uploads first ("Pitbull feat.
    Chris Brown - International Love (Vocal Version)"), and returns nothing at
    all when the guest is uncredited ("Highlights" by Kanye West).
    """
    want = song_key(title)
    for anchor in (n1, n2):
        hits = dz.search(base(title), anchor)
        time.sleep(dz.INTERVAL)
        if hits is None:
            raise LookupFailed(f"deezer search {title} / {anchor}")
        for hit in hits:
            if song_key(hit.get("title") or "") != want:
                continue
            people = deezer_track(hit["id"]).get("contributors") or []
            if on_track(n1, people) and on_track(n2, people):
                return _found("deezer", str(hit["id"]), True, title, None)
    return {}


def musicbrainz_song(n1: str, n2: str, title: str, taken: set[str]) -> dict | None:
    """The row's own song among the pair's joint recordings: one request, shared
    by all of the pair's rows. The song-by-title query only runs when the pair has
    more recordings than one page holds."""
    found = musicbrainz_pair(n1, n2, title, taken)
    if found and found["exact"]:
        return found
    data = _PAIRS.get(("musicbrainz", n1, n2)) or {}
    if (data.get("count") or 0) > len(data.get("recordings") or []):
        return musicbrainz_exact(n1, n2, title, taken)
    return None


def rescue(n1: str, n2: str, title: str, taken: set[str]) -> dict:
    """Last look before a row is dropped. The row's own song first -- by title on
    Deezer, then MusicBrainz with every name a credit can carry ("Ye") -- also
    under the catalogue's spelling of a name ("Antônio Carlos Jobim" for Tom
    Jobim). Only then any other joint recording."""
    names = [(n1, n2)]
    alt = (DZ_NAMES.get(n1, n1), DZ_NAMES.get(n2, n2))
    if alt != (n1, n2):
        names.append(alt)
    for a, b in names:
        found = deezer_title_first(a, b, title, taken) or musicbrainz_song(a, b, title, taken)
        if found:
            return found
    for a, b in names:                          # Deezer's pair search already ran on ours
        found = musicbrainz_pair(a, b, title, taken) or (
            deezer_pair(a, b, title, taken) if (a, b) != (n1, n2) else None)
        if found:
            return found
    return {}


def _groups_of() -> dict[str, list[str]]:
    """Each act's bands and members by name, from data/artist_groups.json."""
    path = os.path.join(ROOT, "data", "artist_groups.json")
    raw = json.load(open(path, encoding="utf-8")) if os.path.exists(path) else {}
    out = {}
    for name, related in raw.items():
        seen, keep = {_norm(name)}, []
        for r in sorted(related, key=lambda r: "*" in r):   # Deezer search cannot find "N*E*R*D"
            if not re.fullmatch(r"Q\d+", r) and _norm(r) not in seen:   # Wikidata ids carry no name
                seen.add(_norm(r))
                keep.append(r)
        out[name] = keep
    return out


GROUPS_OF = _groups_of()


def group_credit(n1: str, n2: str, title: str, taken: set[str]) -> dict:
    """The row's own song credited to one of the artists' groups: catalogues
    credit "Black Eyed Peas" on RITMO, where we credit will.i.am, and "N.E.R.D"
    on Lemon, where we credit Pharrell. Exact song only, never a retitle: the
    band file lists members as well as bands, and a member's solo song is not
    the band's."""
    want = song_key(title)
    for a, b in ((n1, n2), (n2, n1)):
        for g in GROUPS_OF.get(a, [])[:8]:
            if _norm(g) == _norm(b):
                continue
            hits = dz.search(base(title), g)
            time.sleep(dz.INTERVAL)
            if hits is None:
                raise LookupFailed(f"deezer search {title} / {g}")
            for hit in hits:
                if song_key(hit.get("title") or "") != want:
                    continue
                people = deezer_track(hit["id"]).get("contributors") or []
                if on_track(g, people) and on_track(b, people):
                    return {**_found("deezer", str(hit["id"]), True, title, None), "via": f"group:{g}"}
    return {}


# Exact song in both catalogues before any retitle: Deezer alone would trade
# "SICKO MODE" for "Fair Trade" because it leaves Drake off the credit.
LOOKUPS = {
    "deezer-exact": deezer_exact,
    "musicbrainz-exact": musicbrainz_song,  # one pair query serves all of the pair's rows
    "deezer-pair-v2": deezer_pair,       # v2: prefers the row's own song, skips mashups
    "musicbrainz-pair": musicbrainz_pair,
    "rescue": rescue,
    "group-credit": group_credit,
}
CATALOGUES = tuple(LOOKUPS)


def verdict(entry: dict | None) -> str:
    """found / missing (every lookup answered no) / unknown (keep the row)."""
    if entry is None:
        return "unknown"
    if entry.get("id"):
        return "found"
    tried = set(entry.get("tried", []))
    if entry == {} or {"deezer", "musicbrainz"} <= tried:   # prune_lives' first run
        return "missing"
    return "missing" if set(CATALOGUES) <= tried else "unknown"


def check_rows(indices: list[int], cache: dict, path: str,
               sources: tuple[str, ...] = CATALOGUES) -> None:
    """Run `sources`, in order, for each unresolved row and cache what each said."""
    taken = defaultdict(set)
    for a1, a2, title, _c, _y in COLLABORATIONS:
        taken[(min(a1, a2), max(a1, a2))].add(song_key(title))
    for key, e in cache.items():                 # retitles made by earlier phases
        if e.get("id") and not e.get("exact"):
            a1, a2 = (int(x) for x in key.split("|")[:2])
            taken[(min(a1, a2), max(a1, a2))].add(song_key(e["title"]))
    todo = [
        i for i in indices
        if verdict(cache.get(row_key(i))) == "unknown"
        and not set(sources) <= set((cache.get(row_key(i)) or {}).get("tried", []))
    ]
    started, failed = time.time(), 0
    print(f"a consultar: {len(todo):,} linhas em {', '.join(sources)}", flush=True)
    for n, i in enumerate(todo, 1):
        a1, a2, title, _c, _y = COLLABORATIONS[i]
        n1, n2 = NAME[a1], NAME[a2]
        own = taken[(min(a1, a2), max(a1, a2))]
        entry = dict(cache.get(row_key(i)) or {"tried": []})
        try:
            for src in sources:
                if src in entry.get("tried", []):
                    continue
                res = LOOKUPS[src](n1, n2, title, own) or {}
                if res.get("id"):
                    entry = res
                    break
                entry.update(res)
                entry["tried"] = entry.get("tried", []) + [src]
        except LookupFailed as exc:
            failed += 1
            print(f"  !! {n}/{len(todo)}  {n1} × {n2} — {title!r}: {exc}", flush=True)
        cache[row_key(i)] = entry
        if entry.get("id") and not entry["exact"]:
            own.add(song_key(entry["title"]))
        state = verdict(entry)
        tag = {"found": "OK" if entry.get("exact") else "->", "missing": "--"}.get(state, "..")
        extra = f"  ->  {entry['title']!r}" if state == "found" and not entry["exact"] else ""
        print(f"  {tag} {n}/{len(todo)}  {n1} × {n2} — {title!r}{extra}", flush=True)
        if n % 25 == 0 or n == len(todo):
            save_json(path, cache)
            el = time.time() - started
            print(f"     [{n / el * 60:.0f}/min, falhas {failed}, "
                  f"faltam ~{(len(todo) - n) * el / n / 60:.0f} min]", flush=True)


def rewrite(drop: dict[int, str], retitle: dict[int, tuple[str, int]], prov: dict) -> None:
    """Drop rows (index -> reason) and retitle rows (index -> (title, year))."""
    with open(SOURCE, encoding="utf-8") as fh:
        lines = fh.read().split("\n")
    start = next(k for k, l in enumerate(lines) if l.startswith("COLLABORATIONS"))
    first = start + 1
    tail = next(k for k, l in enumerate(lines[first:], first) if l.strip() == "]")
    if tail - first != len(COLLABORATIONS):
        sys.exit("❌ layout inesperado em source_data.py. Abortando.")
    kept, removed = [], []
    for i, row in enumerate(COLLABORATIONS):
        a1, a2, _t, ctype, _y = row
        if i in retitle:
            new_title, new_year = retitle[i]
            # The real recording decides the type: an album row retitled to a
            # track is a song, a live recording stays live.
            new_type = "live" if is_live(new_title, "") else "song"
            kept.append(f"    ({a1}, {a2}, {new_title!r}, {new_type!r}, {new_year}),")
        elif i in drop:
            removed.append({
                "row": list(row), "line": lines[first + i].strip(),
                "artists": [NAME.get(a1, ""), NAME.get(a2, "")],
                "pair": [NAME.get(a1, ""), NAME.get(a2, "")],
                "reason": drop[i], "searched": 2,
            })
        else:
            kept.append(lines[first + i])
    lines[first:tail] = kept
    with open(SOURCE, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))
    q = json.load(open(QUARANTINE, encoding="utf-8")) if os.path.exists(QUARANTINE) else {"removed": []}
    q["removed"].extend(removed)
    json.dump(q, open(QUARANTINE, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    json.dump(prov, open(SOURCES, "w", encoding="utf-8"), ensure_ascii=False, indent=1)


def plan(indices: list[int], cache: dict, prov: dict, reason: str) -> tuple[dict, dict]:
    """Turn cached verdicts into drops and retitles; unknown rows are left alone."""
    drop, retitle = {}, {}
    for i in indices:
        a1, a2, title, _c, year = COLLABORATIONS[i]
        entry = cache.get(row_key(i))
        state = verdict(entry)
        if state == "missing":
            drop[i] = reason
        elif state == "found":
            new_title = title if entry["exact"] else clean_title(entry["title"])
            if not entry["exact"]:
                retitle[i] = (new_title, entry.get("year") or year)
            prov[f"{a1}-{a2}-{new_title}"] = {"source": entry["source"], "id": entry["id"],
                                              "was": title}
    return drop, retitle


def _selfcheck() -> None:
    for t in ("Royals (Live Duet)", "Cruel Summer (tribute)", "Stan (Grammy Performance)",
              "Evidências - Ao Vivo", "Sozinho (Ao Vivo em Goiânia)"):
        assert is_live(t, "song"), t
    for t in ("Runnin' (Dying to Live)", "Long Live", "Live and Let Die",
              "Ao Vivo e a Cores", "I Don't Wanna Live Forever"):
        assert not is_live(t, "song"), t
    assert base("Evidências (Ao Vivo)") == base("Evidências - Ao Vivo") == "evidencias"
    assert song_key("Savage Remix (feat. Beyoncé)") == song_key("Savage (Remix)") == "savage"
    assert song_key("Comunicação Falhou Ao Vivo") == "comunicacao falhou"
    assert song_key("What's Poppin (Remix)") == song_key("WHATS POPPIN (Remix)")
    assert verdict(None) == verdict({"tried": ["deezer-exact"]}) == "unknown"
    assert verdict({}) == verdict({"tried": list(CATALOGUES)}) == "missing"
    assert verdict({"tried": ["deezer", "musicbrainz"]}) == "missing"
    assert on_track("Henrique & Juliano", [{"name": "Henrique e Juliano", "id": 0}])
    assert not credited_on("Santana", ["Luan Santana"]) and not credited_on("Rita", ["Margarita"])
    assert credited_on("Ludmilla", ["Ludmilla Oficial"]) and not credited_on("IU", ["IU Band"])
    assert not credited_on("Camila", ["Camila Cabello"]) and not credited_on("TINI", ["Tinie Tempah"])
    assert credited_on("Wisin", ["Wisin & Yandel"]) and credited_on("Lauryn Hill", ["Ms. Lauryn Hill"])
    assert credited_on("Spice", ["Vybz Kartel, Spice"]) and credited_on("Raisa", ["Afgan,Raisa"])
    assert credited_on("The Supremes", ["Diana Ross & The Supremes"]) and not credited_on("Mora", ["Morad"])
    assert not credited_on("Sistar", ["Hyorin of Sistar"]) and credited_on("Hyorin", ["Hyorin of Sistar"])
    assert not credited_on("MAMAMOO", ["Solar (MAMAMOO)"]) and junk_title("♡")
    assert junk_title("$$$ (feat. Gunna)") and junk_title("♡ (Infinity Station Sessions)")
    for t in ("Punjabi Mashup", "Garmi Non Stop Dance Mix", "Crazy (Tiësto's Big Room Mix)",
              "Reggae Dancehall Lovers Rock - Continuous Mix", "Ultimate Party Mashup - Desi Club Edition",
              "Pal Pal Dil Ke Paas Lofi Mix by L3AD", "Let Me Love You (Marshmello Remix)",
              "Dirty Vibe (DJ Snake & Aazar Remix)", "Tere Liye (Lofi Mix)", "Ke Star (Club Mix)",
              "Just Massive Dance: S & M (Dave Aude remix) / On the Floor (Ccw club mix)",
              "Anne Marie Hitmix: Perfect to Me / Some People / Friends", "Jet Star Reggae Mix 1",
              "Chart Mix: November 2016: All We Know / Starboy / The Greatest", "New Year Mix 2023",
              "9Xm House of Dance-Dj Shilpi Sharma-Vol.1", "Bad Blood / Royals / Hold Up", "Intro 2",
              "Ultimate Bollywood Dance Celebration Mix", "Chart Hits: Extended",
              "Autumn Rai Mix (feat. Cheb Mami)", "Get Real - Sounds Right Mix",
              "Come Dancing / And That Says a Lot (Panned, Right) / Prove Your Love"):
        assert junk_title(t), t
    for t in ("Pot-Pourri: Miudinho / Casa de bamba (Ao vivo)", "THE BOX MEDLEY 12", "Lean On",
              "Poesia Acústica #9: Melhor Forma", "Mix It Up", "Savage Remix (feat. Beyoncé)",
              "Mi Cubana (Remix)", "Peaches (Remix)", "Dance (A$$) Remix (Remix)", "X (Official Remix)",
              "Pra Mim Não É / Se Eu Te Pego Te Envergo / Instigante (Ao Vivo)", "Silk Sonic Intro",
              "Lud Session #2: Modo Avião / A Tua Voz / 700 Por Hora", "DJ Got Us Fallin' in Love",
              "Villano Antillano: Bzrp Music Sessions, Vol. 51/66", "I Can't Save You (Interlude)",
              "Mi Persona Favorita (En Directo En El Wanda Metropolitano / Madrid / 2019)",
              "Ela É do Tipo - Remix", "Evidências - Ao Vivo", "Gimme the power"):
        assert not junk_title(t), t
    assert clean_title("O Show Tem que Continuar (feat. Martinho Da Vila, Maria Rita, Ao Vivo") \
        == "O Show Tem que Continuar"
    drake = next(iter(DZ_IDS.get("Drake", {246791})))
    assert on_track("Drake", [{"name": "Aubrey Graham", "id": drake}])


def main() -> None:
    _selfcheck()
    dry = "--dry-run" in sys.argv
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
    check_rows(local, cache, CACHE)
    drop, retitle = plan(local, cache, prov, "live BR nao encontrada no Deezer nem no MusicBrainz")
    drop.update({i: "live sem fonte (internacional)" for i in intl})
    rewrite(drop, retitle, prov)
    gone_br = len(drop) - len(intl)
    print(f"\n✅ internacionais removidas: {len(intl)}")
    print(f"✅ brasileiras: {len(local) - gone_br - len(retitle)} mantidas, "
          f"{len(retitle)} com titulo corrigido, {gone_br} removidas")


if __name__ == "__main__":
    main()
