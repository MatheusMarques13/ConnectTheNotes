"""Harvest 2023+ collaborations the seeded dataset never had.

The dataset was written from model knowledge, so it thins out at the training
cutoff: 1,296 edges for 2022, 175 for 2024, 29 for 2025, none for 2026. No
amount of cleaning fixes that — the rows simply were never there.

This asks MusicBrainz for recent recordings crediting artists already on the
roster, and proposes an edge only when EVERY credited artist is someone we
already know. New artists are never invented here: unconstrained growth is how
the fabricated rows got in, and a wrong edge costs more than a missing one.

Artists are visited fame-first, so an interrupted run still covers the acts the
game actually draws from. Resumable — rerun to continue.

Run:  python3 tools/harvest_recent.py [max_artists]
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

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
sys.path.insert(0, os.path.join(ROOT, "data"))
from source_data import ARTISTS, COLLABORATIONS  # noqa: E402

FAME = os.path.join(ROOT, "data", "artist_fame.json")
STATE = os.path.join(ROOT, "data", "recent_harvest.json")

BASE = "https://musicbrainz.org/ws/2/recording"
UA = "ConnectTheNotes/0.1 ( matheusbmarques13@gmail.com )"
INTERVAL = 1.15
FROM_YEAR = 2023
PAGE = 100

LUCENE = re.compile(r'[+\-&|!(){}\[\]^"~*?:\\/]')

# A catalogue lookup returns every variant of a track, and most of them are not
# collaborations. Three classes need different handling:
#
#   technical — "(instrumental)", "(sped up)", "(radio edit)". Same people, no
#               new information. Dropped.
#   remix     — "Atomic City (David Guetta remix)". Guetta remixed U2; they
#               never worked together. Real in a catalogue, false as an edge,
#               so it is kept but typed `remix` rather than passed off as a song.
#   variant   — "(piano version)", "(Elyanna version)". The suffix is stripped
#               to find the base title so six variants collapse into one row.
#
# Guest versions stay distinct on purpose: WE PRAY (Elyanna version) and
# WE PRAY (TWICE version) have different personnel, and merging them would
# claim TWICE and Elyanna recorded together.
VARIANT_SUFFIX = re.compile(
    r"\s*[\(\[][^)\]]*\b(?:remix|re-?edit|edit|mix|mashup|bootleg|instrumental"
    r"|a\s?cappella|acapella|sped\s?up|slowed|radio|extended|version|reprise"
    r"|demo|clean|explicit|karaoke|edit[ae]d)\b[^)\]]*[\)\]]",
    re.I,
)
TECHNICAL = re.compile(
    r"\b(?:instrumental|a\s?cappella|acapella|sped\s?up|slowed|karaoke"
    r"|radio\s?edit|extended\s?(?:mix|version)|clean\s?version|censored)\b",
    re.I,
)
REMIXY = re.compile(r"\b(?:remix|mashup|bootleg|dub\s?mix|club\s?mix|vip\s?mix|re-?edit)\b", re.I)
LIVEY = re.compile(r"\b(?:ao\s?vivo|live|en\s?vivo|unplugged|ac[uú]stico)\b", re.I)


# DJ record pools flood MusicBrainz with service edits: transitions, blends,
# mashups, drumless cuts. They credit both source artists, so they look exactly
# like a collaboration and are the fastest way to reintroduce the fabrications
# this whole cleanup removed — "Somebody to Crush On (Gaszia Love Mash)" would
# assert that Justin Bieber and AJ Tracey worked together. Never harvested.
DJ_EDIT = re.compile(
    r"\b(?:transition|drumless|mash(?:up)?|blend|bootleg|flip|segue|redrum"
    r"|quick\s?hit|short\s?edit|hype\s?edit|intro\s?edit|outro|acap"
    r"|dirty|clean|edition|super\s?cut|megamix|throwback\s?mix|continuous\s?mix|in\s?the\s?mix)\b"
    r"|\b\d{2,3}\s*-\s*\d{2,3}\b",                      # 95-78 BPM transition
    re.I,
)


# A DJ mix lists adjacent tracks: "Tears / I Just Might / bye (Mixed)"
# credits Bruno Mars and Sabrina Carpenter, who never worked together.
MIXED_TAG = re.compile(r"[\(\[]\s*(?:mixed|dj\s?mix)\s*[\)\]]", re.I)

def classify(title: str) -> tuple[str, str] | None:
    """Return (base_title, type) or None when the variant carries no signal."""
    if DJ_EDIT.search(title) or MIXED_TAG.search(title):
        return None
    if TECHNICAL.search(title):
        return None
    base = re.sub(r"\s{2,}", " ", VARIANT_SUFFIX.sub("", title)).strip(" -–—")
    if not base:
        return None
    if REMIXY.search(title):
        return base, "remix"
    if LIVEY.search(title):
        return base, "live"
    return base, "song"


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
    s = re.sub(r"^(?:the|os|as)\s+", "", s.lower())
    return re.sub(r"[^a-z0-9]+", " ", s).strip()


def get(url: str, tries: int = 5) -> dict | None:
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


def save(state: dict) -> None:
    """Write via a temp file + rename.

    A reader that opens this mid-write gets a truncated document and a
    JSONDecodeError; rename is atomic, so a reader sees either the old file or
    the new one and never a half-written one.
    """
    tmp = STATE + ".tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump(state, fh, ensure_ascii=False, indent=1)
    os.replace(tmp, STATE)


def credited(rec: dict) -> list[str]:
    return [
        a["artist"]["name"]
        for a in rec.get("artist-credit") or []
        if isinstance(a, dict) and "artist" in a
    ]


def first_year(rec: dict) -> int | None:
    best = None
    for rel in rec.get("releases") or []:
        d = (rel.get("date") or "")[:4]
        if d.isdigit():
            y = int(d)
            best = y if best is None else min(best, y)
    return best


def main() -> None:
    limit = int(sys.argv[1]) if len(sys.argv) > 1 else 0

    roster = {fold(n): i for (i, n, _g) in ARTISTS}
    name = {i: n for (i, n, _g) in ARTISTS}
    known = {
        (min(a1, a2), max(a1, a2), fold(t))
        for a1, a2, t, _c, _y in COLLABORATIONS
    }
    known_pairs = {(min(a1, a2), max(a1, a2)) for a1, a2, *_ in COLLABORATIONS}

    fame = {}
    if os.path.exists(FAME):
        with open(FAME, encoding="utf-8") as fh:
            raw = json.load(fh)
        for k, v in (raw.get("artists") or raw).items():
            if isinstance(v, dict):
                fame[k] = v.get("fans", 0)

    def rank(entry: tuple) -> int:
        i, n, _g = entry
        return -int(fame.get(str(i), fame.get(n, 0)) or 0)

    ordered = sorted(ARTISTS, key=rank)

    state = {"done": [], "found": []}
    if os.path.exists(STATE):
        with open(STATE, encoding="utf-8") as fh:
            state = json.load(fh)
    done = set(state["done"])

    seen_new = {
        (f["a1"], f["a2"], fold(f["title"]))
        for f in state["found"]
    }

    todo = [a for a in ordered if str(a[0]) not in done]
    if limit:
        todo = todo[:limit]

    print(f"artistas no roster: {len(ARTISTS):,} | ja varridos: {len(done):,} | "
          f"nesta rodada: {len(todo):,}", flush=True)

    started = time.time()
    for n, (aid, aname, _g) in enumerate(todo, 1):
        term = LUCENE.sub(" ", aname).strip()
        if not term:
            done.add(str(aid))
            continue
        qs = urllib.parse.urlencode(
            {
                "query": f'artist:"{term}" AND firstreleasedate:[{FROM_YEAR} TO 2030]',
                "fmt": "json",
                "limit": PAGE,
            }
        )
        data = get(f"{BASE}?{qs}")
        time.sleep(INTERVAL)
        done.add(str(aid))

        if not data:
            continue

        hits = 0
        for rec in data.get("recordings") or []:
            names = credited(rec)
            if len(names) < 2:
                continue
            ids = [roster.get(fold(x)) for x in names]
            # Every credited act must already be on the roster. A partial match
            # means we would be guessing at who the stranger is.
            if any(i is None for i in ids) or aid not in ids:
                continue
            year = first_year(rec) or FROM_YEAR
            if year < FROM_YEAR:
                continue
            shaped = classify(rec["title"])
            if not shaped:
                continue
            title, ctype = shaped
            uniq = sorted(set(ids))
            for x in range(len(uniq)):
                for y in range(x + 1, len(uniq)):
                    p = (uniq[x], uniq[y])
                    dedup = (p[0], p[1], fold(title))
                    if dedup in known or dedup in seen_new:
                        continue
                    seen_new.add(dedup)
                    state["found"].append(
                        {
                            "a1": p[0], "a2": p[1],
                            "names": [name[p[0]], name[p[1]]],
                            "title": title,
                            "type": ctype,
                            "year": year,
                            "mbid": rec["id"],
                            "new_pair": p not in known_pairs,
                        }
                    )
                    hits += 1

        if hits:
            print(f"  + {aname}: {hits} arestas novas", flush=True)
        if n % 25 == 0 or n == len(todo):
            el = time.time() - started
            state["done"] = sorted(done)
            save(state)
            print(f"  [{n}/{len(todo)}  {n / max(1e-9, el) * 60:.0f}/min  "
                  f"achadas {len(state['found']):,}  "
                  f"faltam ~{(len(todo) - n) * el / max(1, n) / 3600:.1f}h]", flush=True)

    state["done"] = sorted(done)
    save(state)

    novos = [f for f in state["found"] if f["new_pair"]]
    print(f"\n✅ {len(state['found']):,} arestas candidatas "
          f"({len(novos):,} entre pares que nunca colaboraram no dataset)")


if __name__ == "__main__":
    main()
