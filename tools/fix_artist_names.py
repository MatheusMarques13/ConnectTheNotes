"""Turn scraped social handles back into artist names.

143 roster entries are handles rather than names — `ricky_van_shelton`,
`brooks_and_dunn_official`, `hank_williams_sr`. They render as-is in the game
and break every catalogue lookup that takes a name.

Mechanical de-slugging gets the shape right but not the spelling, so each
candidate is confirmed against the iTunes Search API, which needs no key and
returns the label's own capitalisation. Unconfirmed names still get the
mechanical fix — a handle is never the better option — but are reported so
they can be eyeballed.

Genuinely stylised names are left alone: Coma_Cose, Go_A, mxmtoon and 88rising
are spelled that way by their owners, so only all-lowercase snake_case and an
explicit `_official` suffix count as handles.

Run:  python3 tools/fix_artist_names.py [--dry-run]
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
from source_data import ARTISTS  # noqa: E402

SOURCE = os.path.join(ROOT, "data", "source_data.py")
REPORT = os.path.join(ROOT, "data", "name_fixes.json")

SEARCH = "https://itunes.apple.com/search"
INTERVAL = 0.35

HANDLE = re.compile(r"^[a-z0-9]+(?:_[a-z0-9]+)+$|_official$")
# Particles that stay lowercase inside a name unless they lead it.
PARTICLES = {"de", "da", "do", "dos", "das", "del", "la", "le", "van", "von", "e"}
SUFFIXES = {"sr": "Sr.", "jr": "Jr.", "ii": "II", "iii": "III", "iv": "IV"}


def _ssl_context() -> ssl.SSLContext:
    try:
        import certifi

        return ssl.create_default_context(cafile=certifi.where())
    except ImportError:
        return ssl.create_default_context()


SSL_CTX = _ssl_context()


def deslug(raw: str) -> str:
    body = re.sub(r"_official$", "", raw)
    # Handles flatten the punctuation out of Irish and Scottish names:
    # cole_o_dea is Cole O'Dea, not Cole O Dea.
    body = re.sub(r"_o_([a-z])", lambda m: f"_o'{m.group(1)}", body)
    body = re.sub(r"_mc_([a-z])", lambda m: f"_mc{m.group(1)}", body)
    words = body.split("_")
    out = []
    for pos, w in enumerate(words):
        if w == "and":
            out.append("&")
        elif w in SUFFIXES:
            out.append(SUFFIXES[w])
        elif w in PARTICLES and pos > 0:
            out.append(w)
        elif w.startswith("o'") and len(w) > 2:
            out.append("O'" + w[2:].capitalize())
        elif w.startswith("mc") and len(w) > 2:
            out.append("Mc" + w[2:].capitalize())
        else:
            out.append(w.capitalize())
    return " ".join(out)


def fold(s: str) -> str:
    s = unicodedata.normalize("NFKD", s or "")
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]+", "", s.lower())


def itunes_name(guess: str) -> str | None:
    qs = urllib.parse.urlencode(
        {"term": guess, "entity": "musicArtist", "limit": 3, "country": "US"}
    )
    try:
        req = urllib.request.Request(
            f"{SEARCH}?{qs}", headers={"User-Agent": "ConnectTheNotes/0.1"}
        )
        with urllib.request.urlopen(req, timeout=20, context=SSL_CTX) as fh:
            data = json.load(fh)
    except Exception:                                   # noqa: BLE001
        return None
    want = fold(guess)
    results = [(r.get("artistName") or "") for r in data.get("results") or []]

    # Exact match modulo case and punctuation — the common case.
    for got in results:
        if fold(got) == want:
            return got

    # Handles also truncate and tack on disambiguators: `rhodes_uk` is RHODES,
    # `lilly_wood` is Lilly Wood and the Prick. Accept a prefix relationship in
    # either direction, but only a tight one — a loose match here would rename
    # an artist into someone else entirely.
    for got in results:
        g = fold(got)
        if not g or not want:
            continue
        short, long = (g, want) if len(g) < len(want) else (want, g)
        if long.startswith(short) and len(short) >= 4 and len(long) - len(short) <= 12:
            return got
    return None


def main() -> None:
    dry = "--dry-run" in sys.argv
    handles = [(i, n) for (i, n, _g) in ARTISTS if HANDLE.search(n)]
    print(f"handles a corrigir: {len(handles)}", flush=True)

    fixes, unconfirmed = {}, []
    for n, (aid, raw) in enumerate(handles, 1):
        guess = deslug(raw)
        canon = itunes_name(guess)
        time.sleep(INTERVAL)
        final = canon or guess
        fixes[str(aid)] = {
            "was": raw,
            "now": final,
            "confirmed": bool(canon),
        }
        if not canon:
            unconfirmed.append((raw, guess))
        if n % 25 == 0 or n == len(handles):
            print(f"  {n}/{len(handles)}  confirmados "
                  f"{sum(1 for v in fixes.values() if v['confirmed'])}", flush=True)

    print(f"\n  confirmados pelo iTunes : {sum(1 for v in fixes.values() if v['confirmed'])}")
    print(f"  so mecanico (revisar)   : {len(unconfirmed)}")
    for raw, guess in unconfirmed[:12]:
        print(f"    {raw}  ->  {guess}")

    with open(REPORT, "w", encoding="utf-8") as fh:
        json.dump(fixes, fh, ensure_ascii=False, indent=1)

    if dry:
        print("\n(dry-run: source_data.py intacto)")
        return

    with open(SOURCE, encoding="utf-8") as fh:
        text = fh.read()

    applied = 0
    for aid, fx in fixes.items():
        old = f"({aid}, {fx['was']!r}, "
        new = f"({aid}, {fx['now']!r}, "
        if old in text:
            text = text.replace(old, new, 1)
            applied += 1

    with open(SOURCE, "w", encoding="utf-8") as fh:
        fh.write(text)
    print(f"\n✅ {applied} nomes reescritos em source_data.py")
    print(f"✅ relatorio em data/name_fixes.json")


if __name__ == "__main__":
    main()
