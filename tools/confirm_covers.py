"""Second pass on the pairs flagged as cover or tribute.

tools/verify_casts.py --duos asks whether one recording credits both artists.
That question has a blind spot: a catalogue often credits only the lead and
files the guest as a relationship. "Just Good Friends" is a genuine Michael
Jackson and Stevie Wonder duet from Bad, but MusicBrainz credits Michael alone
and lists Stevie as a performer relation — so the first pass reads it as a
cover and would delete a real collaboration. Same for Slash's guitar on
"Give In to Me".

This re-opens every flagged recording with inc=artist-rels and looks for the
partner among the performers, vocalists and instrumentalists. Only pairs absent
from the credits AND from the relationships stay flagged.

Writes the verdict back into data/cast_audit.json, so tools/apply_cast_fixes.py
picks up the corrected set.

Run:  python3 tools/confirm_covers.py [max_pairs]
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

STATE = os.path.join(ROOT, "data", "cast_audit.json")

BASE = "https://musicbrainz.org/ws/2/recording"
UA = "ConnectTheNotes/0.1 ( matheusbmarques13@gmail.com )"
INTERVAL = 1.15
LUCENE = re.compile(r'[+\-&|!(){}\[\]^"~*?:\\/]')

# Relationship types that mean "this person is ON the track".
PERFORMS = {"performer", "vocal", "instrument", "performing orchestra", "conductor"}


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
    t = re.sub(r"\s*[\(\[][^)\]]*[\)\]]", " ", t or "")
    return fold(t)


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


def everyone_on(rec: dict) -> set[str]:
    """Credited artists plus anyone related to the recording as a performer."""
    names = {
        fold(a["artist"]["name"])
        for a in rec.get("artist-credit") or []
        if isinstance(a, dict) and "artist" in a
    }
    for rel in rec.get("relations") or []:
        if rel.get("type") in PERFORMS or rel.get("target-type") == "artist":
            other = (rel.get("artist") or {}).get("name")
            if other:
                names.add(fold(other))
    for m in re.finditer(r"[\(\[][^)\]]*\b(?:feat|ft|with)\.?\s+([^)\]]+)[\)\]]",
                         rec.get("title") or "", re.I):
        for part in re.split(r"\s*(?:,|&|\band\b)\s*", m.group(1)):
            if part.strip():
                names.add(fold(part))
    return names


def main() -> None:
    budget = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 0

    with open(STATE, encoding="utf-8") as fh:
        state = json.load(fh)

    todo = [
        (k, v) for k, v in state.items()
        if v.get("verdict") == "no-joint-recording" and not v.get("rechecked")
    ]
    if budget:
        todo = todo[:budget]

    print(f"pares a reconferir: {len(todo)} (~{len(todo) * 2 * INTERVAL / 60:.0f} min)",
          flush=True)

    rescued = 0
    started = time.time()
    for n, (key, v) in enumerate(todo, 1):
        cast = v.get("cast") or []
        if len(cast) != 2:
            v["rechecked"] = True
            continue

        term = LUCENE.sub(" ", v["title"]).strip()
        # Anchor on both names. The catalogue credits only the lead, so
        # anchoring on the guest returns nothing: "Just Good Friends" searched
        # under Stevie Wonder gives count=0, while under Michael Jackson it is
        # right there with Stevie in the relationships.
        found = None
        for who in cast:
            anchor = LUCENE.sub(" ", who).strip()
            qs = urllib.parse.urlencode(
                {
                    "query": f'recording:"{term}" AND artist:"{anchor}"',
                    "fmt": "json", "limit": 10,
                }
            )
            found = get(f"{BASE}?{qs}")
            time.sleep(INTERVAL)
            if found and (found.get("recordings") or []):
                break

        want = title_key(v["title"])
        wanted = {fold(cast[0]), fold(cast[1])}
        joint = None
        for rec in (found or {}).get("recordings") or []:
            if title_key(rec.get("title") or "") != want:
                continue
            # A literal "+" in a query string is decoded as a space, which
            # makes the whole inc parameter invalid and the response arrive with
            # no relations at all — silently, looking exactly like "no guest".
            detail = get(
                f"{BASE}/{rec['id']}?inc=artist-rels%2Bartist-credits&fmt=json"
            )
            time.sleep(INTERVAL)
            if not detail:
                continue
            if wanted <= everyone_on(detail):
                joint = rec["id"]
                break

        v["rechecked"] = True
        if joint:
            rescued += 1
            v["verdict"] = "clean"
            v["rescued_by"] = joint
            print(f"  ✓ RESGATADO {v['title']!r} — {cast[0]} x {cast[1]} "
                  f"(creditado via relacionamento)", flush=True)
        else:
            print(f"  x confirmado cover/tributo: {v['title']!r} — "
                  f"{cast[0]} x {cast[1]}", flush=True)

        if n % 5 == 0 or n == len(todo):
            with open(STATE, "w", encoding="utf-8") as fh:
                json.dump(state, fh, ensure_ascii=False, indent=1)
            el = time.time() - started
            print(f"  [{n}/{len(todo)}  faltam ~"
                  f"{(len(todo) - n) * el / max(1, n) / 60:.0f} min]", flush=True)

    with open(STATE, "w", encoding="utf-8") as fh:
        json.dump(state, fh, ensure_ascii=False, indent=1)

    still = sum(1 for v in state.values() if v.get("verdict") == "no-joint-recording")
    print(f"\n✅ {rescued} resgatados | {still} confirmados como cover/tributo")


if __name__ == "__main__":
    main()
