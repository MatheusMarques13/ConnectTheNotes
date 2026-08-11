"""Find edges that cannot be true, using only the dataset and artist lifespans.

tools/audit_edges.py catches rows whose title is not a song. It cannot catch a
row whose title is a perfectly good song attributed to the wrong people, and
that turns out to be its own failure mode:

    'Scream & Shout'   [2012]  will.i.am × Britney Spears     <- real
    'Scream and Shout' [2012]  Michael Jackson × will.i.am    <- invented

The second is a hallucination built by welding "Scream" (1995, Michael and
Janet Jackson) onto "Scream & Shout" (2012). Michael Jackson died in 2009.

Two detectors, both cheap:

  twin-title  Two rows share a title once punctuation and "&"/"and" are
              normalised, and a year, but credit different artists. Real songs
              do not do this; one of the pair is usually invented.
  posthumous  DOES NOT WORK — kept only so nobody tries it again. The idea was
              that an artist credited after their death marks a fabrication.
              It does not, in music: posthumous features and remixes are an
              ordinary product category. Of the first 30 hits, essentially all
              were real releases — Kygo × Whitney Houston "Higher Love",
              Drake × Michael Jackson "Don't Matter to Me", Justin Timberlake ×
              Michael Jackson "Love Never Felt So Good". The lifespan cache is
              still written because it is cheap and useful elsewhere, but the
              flags it produces must not be treated as findings.

Neither deletes anything — both write candidates for review.

Run:  python3 tools/find_impossible.py [max_lookups]
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

LIFESPANS = os.path.join(ROOT, "data", "artist_lifespans.json")
REPORT = os.path.join(ROOT, "data", "impossible_edges.json")

BASE = "https://musicbrainz.org/ws/2/artist"
UA = "ConnectTheNotes/0.1 ( matheusbmarques13@gmail.com )"
INTERVAL = 1.15
# A posthumous release is normal; a brand-new duet recorded years after a death
# is not. Allow a window for material finished from existing sessions.
POSTHUMOUS_GRACE = 3
LUCENE = re.compile(r'[+\-&|!(){}\[\]^"~*?:\\/]')


def _ssl_context() -> ssl.SSLContext:
    try:
        import certifi

        return ssl.create_default_context(cafile=certifi.where())
    except ImportError:
        return ssl.create_default_context()


SSL_CTX = _ssl_context()


def twin_key(title: str) -> str:
    """Collapse the spellings a fabricated twin hides behind."""
    s = unicodedata.normalize("NFKD", title or "")
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = s.lower().replace("&", " and ")
    s = re.sub(r"\b(feat|ft|featuring|com|with)\b.*$", "", s)
    return re.sub(r"[^a-z0-9]+", " ", s).strip()


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


def lifespan(name: str) -> dict | None:
    term = LUCENE.sub(" ", name).strip()
    if not term:
        return None
    qs = urllib.parse.urlencode(
        {"query": f'artist:"{term}"', "fmt": "json", "limit": 1}
    )
    data = get(f"{BASE}?{qs}")
    hit = (data or {}).get("artists") or []
    if not hit:
        return None
    a = hit[0]
    span = a.get("life-span") or {}
    return {
        "mb_name": a.get("name"),
        "begin": (span.get("begin") or "")[:4],
        "end": (span.get("end") or "")[:4],
        "ended": bool(span.get("ended")),
    }


def build_key(title: str) -> str:
    """What data/build.py groups on — spacing and case only."""
    return re.sub(r"\s+", " ", (title or "").strip()).lower()


def find_twins() -> list[dict]:
    """Rows that are the same song to a human but two songs to the build.

    build.py groups on (title, type, year), so "Lady Marmalade" credited across
    six rows merges into one song with all six artists — normal, not a twin.
    The dangerous case is a title the build keeps SEPARATE because a character
    differs, while a reader would call them the same track:

        'Scream & Shout'   -> will.i.am, Britney Spears
        'Scream and Shout' -> Michael Jackson, will.i.am

    Same song name, same year, disjoint casts, two separate nodes. One of them
    is invented, and merging them would be worse than leaving it — so these are
    reported for a human, never auto-resolved.
    """
    name = {i: n for (i, n, _g) in ARTISTS}
    groups = defaultdict(list)
    for idx, (a1, a2, title, ctype, year) in enumerate(COLLABORATIONS):
        groups[(twin_key(title), year)].append((idx, a1, a2, title, ctype))

    twins = []
    for (key, year), rows in groups.items():
        if len(rows) < 2 or not key:
            continue
        # If the build already merges them, there is nothing hidden here.
        if len({build_key(r[3]) for r in rows}) < 2:
            continue
        casts = defaultdict(set)
        for r in rows:
            casts[build_key(r[3])].update((r[1], r[2]))
        variants = list(casts.items())
        disjoint = any(
            not (casts[a] & casts[b])
            for i, (a, _) in enumerate(variants)
            for b, _ in variants[i + 1:]
        )
        if not disjoint and len(variants) < 2:
            continue
        twins.append(
            {
                "title_key": key,
                "year": year,
                "disjoint_casts": disjoint,
                "rows": [
                    {
                        "i": r[0],
                        "title": r[3],
                        "type": r[4],
                        "artists": [name.get(r[1], ""), name.get(r[2], "")],
                    }
                    for r in rows
                ],
            }
        )
    # Disjoint casts first — those are the likely fabrications.
    twins.sort(key=lambda t: (not t["disjoint_casts"], -len(t["rows"])))
    return twins


def main() -> None:
    budget = int(sys.argv[1]) if len(sys.argv) > 1 else 250
    name = {i: n for (i, n, _g) in ARTISTS}

    twins = find_twins()
    print("=" * 70)
    print(f"TITULOS GEMEOS: {len(twins)} grupos")
    print("=" * 70)
    for t in twins[:15]:
        print(f"  [{t['year']}] {t['title_key']!r}")
        for r in t["rows"]:
            print(f"      {r['title']!r} — {r['artists'][0]} × {r['artists'][1]}")

    # ---------------------------------------------------- posthumous check
    cache = {}
    if os.path.exists(LIFESPANS):
        with open(LIFESPANS, encoding="utf-8") as fh:
            cache = json.load(fh)

    # Only look up artists that actually appear on a suspicious-looking row:
    # someone credited on a track dated well after their other work.
    latest = defaultdict(int)
    earliest = defaultdict(lambda: 9999)
    for a1, a2, _t, _c, y in COLLABORATIONS:
        for a in (a1, a2):
            latest[a] = max(latest[a], y)
            earliest[a] = min(earliest[a], y)

    span = sorted(
        (a for a in latest if latest[a] - earliest[a] > 25),
        key=lambda a: -(latest[a] - earliest[a]),
    )
    todo = [a for a in span if str(a) not in cache][:budget]
    print(f"\nconsultando lifespan de {len(todo)} artistas de carreira longa "
          f"({len(cache)} em cache)", flush=True)

    for n, aid in enumerate(todo, 1):
        info = lifespan(name.get(aid, ""))
        time.sleep(INTERVAL)
        cache[str(aid)] = info or {}
        if n % 25 == 0 or n == len(todo):
            with open(LIFESPANS, "w", encoding="utf-8") as fh:
                json.dump(cache, fh, ensure_ascii=False, indent=1)
            print(f"  {n}/{len(todo)}", flush=True)

    with open(LIFESPANS, "w", encoding="utf-8") as fh:
        json.dump(cache, fh, ensure_ascii=False, indent=1)

    impossible = []
    for idx, (a1, a2, title, ctype, year) in enumerate(COLLABORATIONS):
        for aid in (a1, a2):
            info = cache.get(str(aid)) or {}
            end = info.get("end")
            if end and end.isdigit() and year > int(end) + POSTHUMOUS_GRACE:
                impossible.append(
                    {
                        "i": idx,
                        "title": title,
                        "year": year,
                        "artists": [name.get(a1, ""), name.get(a2, "")],
                        "who": name.get(aid, ""),
                        "died": end,
                    }
                )
                break

    print()
    print("=" * 70)
    print(f"ARESTAS ANACRONICAS: {len(impossible)}")
    print("=" * 70)
    for e in impossible[:25]:
        print(f"  {e['title']!r} ({e['year']}) — {e['artists'][0]} × "
              f"{e['artists'][1]}  [{e['who']} ate {e['died']}]")

    with open(REPORT, "w", encoding="utf-8") as fh:
        json.dump({"twins": twins, "anachronistic": impossible}, fh,
                  ensure_ascii=False, indent=1)
    print(f"\n✅ relatorio em data/impossible_edges.json")


if __name__ == "__main__":
    main()
