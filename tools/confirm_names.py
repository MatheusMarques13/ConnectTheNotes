"""Re-check the artist names iTunes refused to confirm the first time.

The first pass called the iTunes Search API every 0.35s and got HTTP 403 partway
through: Apple caps it near 20 requests per minute. So "88 names unconfirmed"
was mostly throttling, not obscurity — those artists were never really looked up.

This retries only the unconfirmed ones at a pace Apple tolerates, and rewrites
source_data.py wherever the store's own spelling differs from the mechanical
de-slug. Resumable, because a run this slow will get interrupted.

Run:  python3 tools/confirm_names.py [--dry-run]
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

SOURCE = os.path.join(ROOT, "data", "source_data.py")
REPORT = os.path.join(ROOT, "data", "name_fixes.json")

SEARCH = "https://itunes.apple.com/search"
# Apple returns a bodiless 403 above roughly 20 requests/minute. 3.4s keeps us
# just under it; going faster does not fail loudly, it silently returns nothing.
INTERVAL = 3.4
COOLDOWN = 45.0


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
    return re.sub(r"[^a-z0-9]+", "", s.lower())


def lookup(term: str) -> list[str] | None:
    """Return candidate artist names, or None when throttled."""
    qs = urllib.parse.urlencode(
        {"term": term, "entity": "musicArtist", "limit": 5, "country": "US"}
    )
    req = urllib.request.Request(
        f"{SEARCH}?{qs}", headers={"User-Agent": "ConnectTheNotes/0.1"}
    )
    try:
        with urllib.request.urlopen(req, timeout=20, context=SSL_CTX) as fh:
            body = fh.read()
    except Exception as exc:                            # noqa: BLE001
        if getattr(exc, "code", None) == 403:
            return None
        return []
    if not body.strip():
        return None
    try:
        return [r.get("artistName") or "" for r in json.loads(body).get("results") or []]
    except json.JSONDecodeError:
        return None


def main() -> None:
    dry = "--dry-run" in sys.argv
    with open(REPORT, encoding="utf-8") as fh:
        fixes = json.load(fh)

    todo = [(k, v) for k, v in fixes.items() if not v.get("confirmed")]
    print(f"nomes a reconfirmar: {len(todo)} "
          f"(~{len(todo) * INTERVAL / 60:.0f} min a {INTERVAL}s cada)", flush=True)

    changed, confirmed, throttled = {}, 0, 0
    for n, (aid, v) in enumerate(todo, 1):
        guess = v["now"]
        names = lookup(guess)
        if names is None:                               # throttled — back off
            throttled += 1
            print(f"  ...403, esperando {COOLDOWN:.0f}s", flush=True)
            time.sleep(COOLDOWN)
            names = lookup(guess)
        time.sleep(INTERVAL)

        if not names:
            continue
        for got in names:
            if fold(got) == fold(guess):
                v["confirmed"] = True
                confirmed += 1
                if got != guess:
                    changed[aid] = (guess, got)
                    v["now"] = got
                break

        if n % 10 == 0 or n == len(todo):
            print(f"  {n}/{len(todo)}  confirmados {confirmed}  "
                  f"grafia corrigida {len(changed)}", flush=True)
            with open(REPORT, "w", encoding="utf-8") as fh:
                json.dump(fixes, fh, ensure_ascii=False, indent=1)

    with open(REPORT, "w", encoding="utf-8") as fh:
        json.dump(fixes, fh, ensure_ascii=False, indent=1)

    print(f"\n  confirmados nesta rodada : {confirmed}/{len(todo)}")
    print(f"  grafia corrigida         : {len(changed)}")
    for aid, (old, new) in list(changed.items())[:15]:
        print(f"    {old!r} -> {new!r}")
    print(f"  ainda sem confirmacao    : {len(todo) - confirmed}")

    if dry or not changed:
        print("\n(nada reescrito)" if not changed else "\n(dry-run)")
        return

    with open(SOURCE, encoding="utf-8") as fh:
        text = fh.read()
    applied = 0
    for aid, (old, new) in changed.items():
        needle = f"({aid}, {old!r}, "
        if needle in text:
            text = text.replace(needle, f"({aid}, {new!r}, ", 1)
            applied += 1
    with open(SOURCE, "w", encoding="utf-8") as fh:
        fh.write(text)
    print(f"\n✅ {applied} grafias corrigidas em source_data.py")


if __name__ == "__main__":
    main()
