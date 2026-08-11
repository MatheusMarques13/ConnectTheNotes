"""Second opinion on the Brazilian pairs MusicBrainz could not confirm.

MusicBrainz misses Brazilian releases in a specific way: joint projects are
catalogued under the project name, not as two credited artists. Raça Negra and
Só Pra Contrariar return nothing there, yet they recorded "Gigantes do Samba"
(2015) together. Deleting on a MusicBrainz miss alone would erase real work.

Deezer has the coverage MusicBrainz lacks here, so this pass gathers evidence
instead of issuing verdicts:

    confirmed — a track credits both artists in its contributors list
    evidence  — searching both names returns releases worth a human look
                (the joint-project case)
    none      — nothing found in either source

Only `none` is a safe deletion. Everything else goes to review.

Run:  python3 tools/verify_br_pairs.py [max_pairs]
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

REPAIR = os.path.join(ROOT, "data", "edge_repair.json")
STATE = os.path.join(ROOT, "data", "br_evidence.json")

SEARCH = "https://api.deezer.com/search"
TRACK = "https://api.deezer.com/track/"
INTERVAL = 0.55            # Deezer tolerates ~50 req/5s; stay well under
TOP_TRACKS = 3             # how many hits to open for a contributors check

BR_TAGS = (
    "Sertanejo", "Pagode", "Axé", "Forró", "MPB", "Samba", "Brazilian",
    "Funk Carioca", "Tropicália",
)


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
    delay = 1.0
    for attempt in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "ConnectTheNotes/0.1"})
            with urllib.request.urlopen(req, timeout=25, context=SSL_CTX) as fh:
                return json.load(fh)
        except Exception as exc:                        # noqa: BLE001
            if attempt == tries - 1:
                print(f"    ! {exc}", flush=True)
                return None
            time.sleep(delay)
            delay *= 2
    return None


def search(n1: str, n2: str) -> list[dict]:
    qs = urllib.parse.urlencode({"q": f"{n1} {n2}", "limit": 8})
    data = get(f"{SEARCH}?{qs}") or {}
    return data.get("data") or []


def contributors(track_id: int) -> list[str]:
    data = get(f"{TRACK}{track_id}") or {}
    return [c.get("name", "") for c in data.get("contributors") or []]


def is_br(genre: str) -> bool:
    return any(t in (genre or "") for t in BR_TAGS)


def main() -> None:
    limit = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    genre = {i: g for (i, _n, g) in ARTISTS}

    with open(REPAIR, encoding="utf-8") as fh:
        repair = json.load(fh)

    todo_all = [
        (k, v)
        for k, v in repair.items()
        if v["verdict"] == "drop" and (is_br(genre.get(v["a1"])) or is_br(genre.get(v["a2"])))
    ]

    state = {}
    if os.path.exists(STATE):
        with open(STATE, encoding="utf-8") as fh:
            state = json.load(fh)

    todo = [(k, v) for k, v in todo_all if k not in state]
    if limit:
        todo = todo[:limit]

    print(f"pares BR a checar: {len(todo_all)} | ja feitos: {len(state)} | "
          f"nesta rodada: {len(todo)}", flush=True)

    started = time.time()
    for n, (key, v) in enumerate(todo, 1):
        n1, n2 = v["names"]
        hits = search(n1, n2)
        time.sleep(INTERVAL)

        found, evidence = [], []
        for t in hits[:TOP_TRACKS]:
            names = contributors(t["id"])
            time.sleep(INTERVAL)
            folded = " | ".join(fold(x) for x in names)
            both = all(fold(x) in folded for x in (n1, n2))
            item = {
                "title": t.get("title"),
                "album": (t.get("album") or {}).get("title"),
                "artist": (t.get("artist") or {}).get("name"),
                "contributors": names,
                "deezer_id": t["id"],
            }
            (found if both else evidence).append(item)

        verdict = "confirmed" if found else ("evidence" if evidence else "none")
        state[key] = {
            "a1": v["a1"], "a2": v["a2"], "names": [n1, n2],
            "placeholders": v["placeholders"],
            "verdict": verdict,
            "confirmed": found[:3],
            "evidence": evidence[:3],
        }

        tag = {"confirmed": "OK  ", "evidence": "?   ", "none": "--  "}[verdict]
        print(f"  {tag}{n}/{len(todo)}  {n1} × {n2} -> {verdict}", flush=True)
        if n % 5 == 0 or n == len(todo):
            el = time.time() - started
            print(f"     [{n / max(1e-9, el) * 60:.1f}/min, "
                  f"faltam ~{(len(todo) - n) * el / max(1, n) / 60:.0f} min]", flush=True)
            with open(STATE, "w", encoding="utf-8") as fh:
                json.dump(state, fh, ensure_ascii=False, indent=1)

    with open(STATE, "w", encoding="utf-8") as fh:
        json.dump(state, fh, ensure_ascii=False, indent=1)

    tot = {"confirmed": 0, "evidence": 0, "none": 0}
    for v in state.values():
        tot[v["verdict"]] += 1
    print()
    print("=" * 68)
    print(f"CONFIRMADOS {tot['confirmed']}  |  COM INDICIO {tot['evidence']}  |  "
          f"NADA {tot['none']}")
    print("=" * 68)
    for v in list(state.values()):
        if v["verdict"] == "confirmed":
            c = v["confirmed"][0]
            print(f"  OK {v['names'][0]} × {v['names'][1]}")
            print(f"       {c['title']!r} — {', '.join(c['contributors'][:4])}")
    print()
    for v in list(state.values()):
        if v["verdict"] == "evidence":
            c = v["evidence"][0]
            print(f"  ?  {v['names'][0]} × {v['names'][1]}")
            print(f"       {c['title']!r} [{c['album']}] — {c['artist']}")
    print(f"\n✅ evidencias em data/br_evidence.json")


if __name__ == "__main__":
    main()
