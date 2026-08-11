"""Map which artists are members of which groups.

The cast verifier compares our credits against a catalogue's, and catalogues
credit the group where we credit the people. On 'Motorsport' MusicBrainz says
Migos; we say Offset and Quavo. Both are right, but the naive comparison reads
Offset and Quavo as impostors and would delete two real connections. Same for
Diplo under Major Lazer, and Steve Angello under Swedish House Mafia.

So before any cast correction runs, resolve band membership from MusicBrainz's
artist relationships and let tools/apply_cast_fixes.py refuse to strip a person
from a track their group is credited on.

Only artists the verifier actually proposes removing get looked up, so this
stays a few hundred requests rather than a crawl of the roster.

Run:  python3 tools/fetch_memberships.py
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

AUDIT = os.path.join(ROOT, "data", "cast_audit.json")
OUT = os.path.join(ROOT, "data", "artist_groups.json")

BASE = "https://musicbrainz.org/ws/2/artist"
UA = "ConnectTheNotes/0.1 ( matheusbmarques13@gmail.com )"
INTERVAL = 1.2
LUCENE = re.compile(r'[+\-&|!(){}\[\]^"~*?:\\/]')


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
    return re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()


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


def related(name: str) -> list[str]:
    """Groups this artist belongs to, and people who belong to it."""
    term = LUCENE.sub(" ", name).strip()
    if not term:
        return []
    qs = urllib.parse.urlencode({"query": f'artist:"{term}"', "fmt": "json", "limit": 1})
    found = get(f"{BASE}?{qs}")
    hits = (found or {}).get("artists") or []
    if not hits:
        return []
    mbid = hits[0]["id"]
    time.sleep(INTERVAL)

    detail = get(f"{BASE}/{mbid}?inc=artist-rels&fmt=json")
    names = []
    for rel in (detail or {}).get("relations") or []:
        if rel.get("type") in ("member of band", "collaboration", "is person"):
            other = (rel.get("artist") or {}).get("name")
            if other:
                names.append(other)
    return names


def main() -> None:
    with open(AUDIT, encoding="utf-8") as fh:
        audit = json.load(fh)

    wanted = set()
    for v in audit.values():
        if v.get("verdict") == "extra-artists":
            wanted.update(v.get("not_credited") or [])
            wanted.update(v.get("cast") or [])

    cache = {}
    if os.path.exists(OUT):
        with open(OUT, encoding="utf-8") as fh:
            cache = json.load(fh)

    todo = sorted(n for n in wanted if n and n not in cache)
    print(f"artistas a resolver: {len(todo)} ({len(cache)} em cache)", flush=True)

    started = time.time()
    for n, name in enumerate(todo, 1):
        cache[name] = related(name)
        time.sleep(INTERVAL)
        if n % 20 == 0 or n == len(todo):
            el = time.time() - started
            with open(OUT, "w", encoding="utf-8") as fh:
                json.dump(cache, fh, ensure_ascii=False, indent=1)
            print(f"  {n}/{len(todo)}  "
                  f"faltam ~{(len(todo) - n) * el / max(1, n) / 60:.0f} min", flush=True)

    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(cache, fh, ensure_ascii=False, indent=1)

    withrel = {k: v for k, v in cache.items() if v}
    print(f"\n✅ {len(withrel)} artistas com vinculo de grupo/pessoa")
    for k, v in list(withrel.items())[:12]:
        print(f"   {k} <-> {', '.join(v[:5])}")


if __name__ == "__main__":
    main()
