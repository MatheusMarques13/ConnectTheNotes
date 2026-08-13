"""Tell a cover from a collaboration using the WORK, not the recording.

Every earlier attempt asked the wrong question. "Does one recording credit both
artists?" cannot separate these two:

    Life on Mars?   Seu Jorge recorded it; David Bowie wrote it and is not on it
    Under Pressure  Bowie and all four of Queen wrote it, together, and played it

Both look identical at the recording level — MusicBrainz has 135 "Under
Pressure" recordings and the top ones credit Queen alone. The difference is one
layer up, in the work:

    Life on Mars?   writers = David Bowie                    (only him)
    Under Pressure  writers = Bowie, Deacon, May, Mercury, Taylor  (both sides)

So the rule is:

    both perform                      -> collaboration    keep
    both write                        -> collaboration    keep
    B only writes, A only performs    -> cover or composition credit   remove
    neither resolves                  -> inconclusive     keep

That last line matters. Three separate passes in this project were wrecked by
treating a catalogue miss as proof; here a miss returns `inconclusive` and the
row survives.

Three requests per pair: find the recording, follow it to its work, read the
work's writers. Resumable.

Run:  python3 tools/verify_via_works.py [max_pairs] [--from-risk]
"""
import json
import os
import re
import ssl
import sys
import time
import unicodedata
import urllib.parse
import urllib.request
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
sys.path.insert(0, os.path.join(ROOT, "data"))
from source_data import ARTISTS, COLLABORATIONS  # noqa: E402

SOURCES = os.path.join(ROOT, "data", "edge_sources.json")
COVER_RISK = os.path.join(ROOT, "data", "cover_risk.json")
GROUPS = os.path.join(ROOT, "data", "artist_groups.json")
STATE = os.path.join(ROOT, "data", "work_audit.json")

MB = "https://musicbrainz.org/ws/2"
UA = "ConnectTheNotes/0.1 ( matheusbmarques13@gmail.com )"
INTERVAL = 1.15
LUCENE = re.compile(r'[+\-&|!(){}\[\]^"~*?:\\/]')

WRITES = {"composer", "lyricist", "writer", "arranger", "librettist"}
# A writer with this few recording credits is a writer, not a performer.
# Measured: Bernie Taupin 45, Desmond Child 84, John Lennon 8,630. Two orders of
# magnitude apart, and the gap is what keeps Lennon from being deleted off
# "Hey Jude" — MusicBrainz credits The Beatles, never him, so he otherwise looks
# exactly like a lyricist who never played.
NON_PERFORMER_MAX = 200
PERFORMS = {"performer", "vocal", "instrument", "conductor", "performing orchestra"}


def _ssl_context() -> ssl.SSLContext:
    try:
        import certifi

        return ssl.create_default_context(cafile=certifi.where())
    except ImportError:
        return ssl.create_default_context()


SSL_CTX = _ssl_context()


def fold(s: str) -> str:
    s = unicodedata.normalize("NFKD", s or "")
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = s.lower().replace("&", " and ")
    return re.sub(r"[^a-z0-9]+", " ", s).strip()


def title_key(t: str) -> str:
    return fold(re.sub(r"\s*[\(\[][^)\]]*[\)\]]", " ", t or ""))


def get(url: str, tries: int = 4) -> dict | None:
    delay = 2.0
    for attempt in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=30, context=SSL_CTX) as fh:
                return json.load(fh)
        except Exception as exc:                        # noqa: BLE001
            if getattr(exc, "code", None) == 404:
                return None
            if attempt == tries - 1:
                return None
            time.sleep(1.5 if getattr(exc, "code", None) == 503 else delay)
            delay *= 2
    return None


def performers(rec: dict) -> set[str]:
    names = {
        fold(a["artist"]["name"])
        for a in rec.get("artist-credit") or []
        if isinstance(a, dict) and "artist" in a
    }
    for rel in rec.get("relations") or []:
        if rel.get("type") in PERFORMS:
            other = (rel.get("artist") or {}).get("name")
            if other:
                names.add(fold(other))
    for m in re.finditer(r"[\(\[][^)\]]*\b(?:feat|ft|with)\.?\s+([^)\]]+)[\)\]]",
                         rec.get("title") or "", re.I):
        for part in re.split(r"\s*(?:,|&|\band\b)\s*", m.group(1)):
            if part.strip():
                names.add(fold(part))
    return names


def writers(work: dict) -> set[str]:
    return {
        fold((rel.get("artist") or {}).get("name", ""))
        for rel in work.get("relations") or []
        if rel.get("type") in WRITES and (rel.get("artist") or {}).get("name")
    }


_REC_COUNT: dict[str, int] = {}


def recording_count(name: str) -> int | None:
    """How many recordings this artist is credited on, anywhere."""
    if name in _REC_COUNT:
        return _REC_COUNT[name]
    term = LUCENE.sub(" ", name).strip()
    if not term:
        return None
    qs = urllib.parse.urlencode({"query": f'artist:"{term}"', "fmt": "json", "limit": 1})
    found = get(f"{MB}/artist?{qs}")
    time.sleep(INTERVAL)
    hits = (found or {}).get("artists") or []
    if not hits:
        return None
    data = get(f"{MB}/recording?artist={hits[0]['id']}&limit=1&fmt=json")
    time.sleep(INTERVAL)
    if not data:
        return None
    n = data.get("recording-count")
    if isinstance(n, int):
        _REC_COUNT[name] = n
    return n if isinstance(n, int) else None


def work_recordings(work_id: str, pages: int = 3) -> tuple[list[set[str]], int]:
    """Every artist credit across the recordings of a work.

    This is the query the earlier passes were missing. Searching recordings by
    title finds whichever ones rank first — for "Under Pressure" that is a wall
    of Queen-only entries. Browsing by WORK reaches all 261 of them, including
    the ones credited to Queen AND David Bowie, which is what settles the case.
    """
    casts, total = [], 0
    for page in range(pages):
        qs = urllib.parse.urlencode(
            {"work": work_id, "inc": "artist-credits", "limit": 100,
             "offset": page * 100, "fmt": "json"}
        )
        data = get(f"{MB}/recording?{qs}")
        time.sleep(INTERVAL)
        if not data:
            break
        recs = data.get("recordings") or []
        total = data.get("recording-count", total)
        for r in recs:
            casts.append({
                fold(a["artist"]["name"])
                for a in r.get("artist-credit") or []
                if isinstance(a, dict) and "artist" in a
            })
        if (page + 1) * 100 >= total:
            break
    return casts, total


_LINKED = None


def bandmates(a: str, b: str) -> bool:
    """Are these two the same act named at different levels?

    A catalogue credits "The Beatles", never "John Lennon", so Lennon appears in
    zero of the 855 recordings of "Hey Jude" — which reads as a composition
    credit and would delete him from McCartney. Bandmates are settled before any
    of the cover logic runs.
    """
    global _LINKED
    if _LINKED is None:
        raw = {}
        if os.path.exists(GROUPS):
            with open(GROUPS, encoding="utf-8") as fh:
                raw = json.load(fh)
        _LINKED = {fold(k): {fold(x) for x in v} for k, v in raw.items()}
    fa, fb = fold(a), fold(b)
    if fb in _LINKED.get(fa, set()) or fa in _LINKED.get(fb, set()):
        return True
    # A shared group, not a direct link. Eric Clapton points at "Cream" and so
    # does Jack Bruce; neither points at the other, so a direct check misses
    # every pair of bandmates who are not each other's listed relation.
    if _LINKED.get(fa, set()) & _LINKED.get(fb, set()):
        return True
    # One name inside the other: "Tom Petty" and "Tom Petty and the
    # Heartbreakers" are the same act.
    return bool(fa and fb and (fa in fb or fb in fa))


def judge(a: str, b: str, title: str) -> dict:
    """Classify one pair. Never guesses: unresolved returns `inconclusive`."""
    if bandmates(a, b):
        return {"verdict": "collaboration", "why": "sao a mesma banda"}
    fa, fb = fold(a), fold(b)
    want = title_key(title)
    term = LUCENE.sub(" ", title).strip()

    rec_id = None
    for who in (a, b):
        anchor = LUCENE.sub(" ", who).strip()
        qs = urllib.parse.urlencode(
            {
                "query": f'recording:"{term}" AND artist:"{anchor}"',
                "fmt": "json", "limit": 10,
            }
        )
        found = get(f"{MB}/recording?{qs}")
        time.sleep(INTERVAL)
        for r in (found or {}).get("recordings") or []:
            if title_key(r.get("title") or "") == want:
                rec_id = r["id"]
                break
        if rec_id:
            break
    if not rec_id:
        return {"verdict": "inconclusive", "why": "gravacao nao encontrada"}

    detail = get(f"{MB}/recording/{rec_id}?inc=artist-rels%2Bwork-rels%2Bartist-credits&fmt=json")
    time.sleep(INTERVAL)
    if not detail:
        return {"verdict": "inconclusive", "why": "detalhe indisponivel"}

    on_rec = performers(detail)
    if {fa, fb} <= on_rec:
        return {"verdict": "collaboration", "why": "os dois tocam na gravacao",
                "recording": rec_id}

    work_rel = next(
        (r for r in detail.get("relations") or [] if r.get("target-type") == "work"),
        None,
    )
    if not work_rel:
        return {"verdict": "inconclusive", "why": "gravacao sem obra ligada",
                "recording": rec_id}

    work_id = (work_rel.get("work") or {}).get("id")
    work = get(f"{MB}/work/{work_id}?inc=artist-rels&fmt=json") if work_id else None
    time.sleep(INTERVAL)
    if not work:
        return {"verdict": "inconclusive", "why": "obra indisponivel",
                "recording": rec_id}

    wrote = writers(work)

    # Does ANY recording of this work credit both? One hit settles it.
    casts, total = work_recordings(work_id)
    for cast in casts:
        if {fa, fb} <= cast:
            return {"verdict": "collaboration",
                    "why": f"gravacao da obra credita os dois ({total} gravacoes)",
                    "recording": rec_id, "work": work_id}

    ever = set().union(*casts) if casts else set()
    solo_a = any(fa in c and fb not in c for c in casts)
    solo_b = any(fb in c and fa not in c for c in casts)

    # Each recorded the work, separately, and never once together. That is the
    # exact shape of a cover: Bowie's "Life on Mars?" and Seu Jorge's, side by
    # side in the same work, sharing no session.
    if solo_a and solo_b:
        return {
            "verdict": "cover-or-composition",
            "why": (f"cada um gravou a obra separadamente, nunca juntos "
                    f"({total} gravacoes)"),
            "recording": rec_id, "work": work_id,
        }

    # Or one of them only ever signs it — never a single credit across every
    # recording. That is a songwriting credit, not a session.
    for (perf, pn), (comp, cn) in (((fa, a), (fb, b)), ((fb, b), (fa, a))):
        if perf in ever and comp in wrote and comp not in ever:
            # Only if the writer really is a non-performer. A performing artist
            # missing from the credits usually means the catalogue names their
            # band instead, not that they were absent.
            n = recording_count(cn)
            if n is None or n > NON_PERFORMER_MAX:
                return {
                    "verdict": "inconclusive",
                    "why": (f"{cn} assina a obra mas tem "
                            f"{'?' if n is None else n} gravacoes proprias — "
                            f"pode estar creditado como banda"),
                    "recording": rec_id, "work": work_id,
                }
            return {
                "verdict": "cover-or-composition",
                "why": (f"{cn} assina a obra, tem so {n} gravacoes proprias e "
                        f"nao aparece em nenhuma das {total}; {pn} gravou"),
                "recording": rec_id, "work": work_id,
            }

    return {"verdict": "inconclusive",
            "why": f"nenhuma das {total} gravacoes resolve",
            "recording": rec_id, "work": work_id}


def main() -> None:
    numeric = [x for x in sys.argv[1:] if x.isdigit()]
    budget = int(numeric[0]) if numeric else 0

    name = {i: n for (i, n, _g) in ARTISTS}
    prov = {}
    if os.path.exists(SOURCES):
        with open(SOURCES, encoding="utf-8") as fh:
            prov = json.load(fh)

    pairs = defaultdict(list)
    for a1, a2, title, ctype, year in COLLABORATIONS:
        if a1 != a2:
            pairs[(min(a1, a2), max(a1, a2))].append((title, ctype, year))

    # Only single-song, unsourced pairs can hide a cover: a duo with several
    # tracks together is a real working relationship.
    cands = []
    for (a, b), songs in pairs.items():
        if len(songs) != 1:
            continue
        title, ctype, year = songs[0]
        if f"{a}-{b}-{title}" in prov or f"{b}-{a}-{title}" in prov:
            continue
        cands.append({"a1": a, "a2": b, "names": [name.get(a, ""), name.get(b, "")],
                      "title": title, "type": ctype, "year": year})

    if "--from-risk" in sys.argv and os.path.exists(COVER_RISK):
        with open(COVER_RISK, encoding="utf-8") as fh:
            risky = {(r["a1"], r["a2"]) for r in json.load(fh)}
        cands = [c for c in cands if (c["a1"], c["a2"]) in risky]

    state = {}
    if os.path.exists(STATE):
        with open(STATE, encoding="utf-8") as fh:
            state = json.load(fh)

    todo = [c for c in cands if f"{c['a1']}-{c['a2']}" not in state]
    if budget:
        todo = todo[:budget]

    print(f"pares candidatos: {len(cands):,} | ja julgados: {len(state):,} | "
          f"nesta rodada: {len(todo):,} (~{len(todo) * 3 * INTERVAL / 60:.0f} min)",
          flush=True)

    started = time.time()
    for n, c in enumerate(todo, 1):
        out = judge(c["names"][0], c["names"][1], c["title"])
        out.update({"names": c["names"], "title": c["title"], "year": c["year"],
                    "ids": [c["a1"], c["a2"]]})
        state[f"{c['a1']}-{c['a2']}"] = out

        if out["verdict"] == "cover-or-composition":
            print(f"  x {c['title']!r} — {c['names'][0]} x {c['names'][1]}: "
                  f"{out['why']}", flush=True)
        if n % 10 == 0 or n == len(todo):
            with open(STATE, "w", encoding="utf-8") as fh:
                json.dump(state, fh, ensure_ascii=False, indent=1)
            el = time.time() - started
            print(f"  [{n}/{len(todo)}  faltam ~"
                  f"{(len(todo) - n) * el / max(1, n) / 60:.0f} min]", flush=True)

    with open(STATE, "w", encoding="utf-8") as fh:
        json.dump(state, fh, ensure_ascii=False, indent=1)

    from collections import Counter
    tally = Counter(v["verdict"] for v in state.values())
    print(f"\n✅ {dict(tally)}")


if __name__ == "__main__":
    main()
