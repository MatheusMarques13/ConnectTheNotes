"""Ask MusicBrainz whether each flagged pair actually recorded together.

tools/audit_edges.py proves a title is not a song name. It cannot prove the two
artists never collaborated — "Ao Vivo" is a placeholder, but Almir Sater and
Renato Teixeira really did record together. Those are opposite outcomes:

    repair  — the pair exists in the catalog. Swap the placeholder for the real
              title and keep the edge, with the MBID as its source.
    drop    — no shared recording found. Likely two acts on the same festival
              bill, which is not a collaboration.

"Not found" is a weak signal, never proof: MusicBrainz coverage of recent
Brazilian releases is thin, so drops are proposals for review, not deletions.
Nothing is written back to source_data.py here.

Resumable: re-running skips pairs already settled, same as tools/deezer_verify.py.
Rate limited to MusicBrainz's documented 1 req/s.

Run:  python3 tools/repair_edges.py [max_pairs]
"""
import json
import os
import re
import ssl
import sys
import unicodedata
import time
import urllib.parse
import urllib.request
from collections import OrderedDict

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
sys.path.insert(0, os.path.join(ROOT, "data"))
from source_data import ARTISTS  # noqa: E402

AUDIT = os.path.join(ROOT, "data", "edge_audit.json")
STATE = os.path.join(ROOT, "data", "edge_repair.json")

UA = "ConnectTheNotes/0.1 ( matheusbmarques13@gmail.com )"
BASE = "https://musicbrainz.org/ws/2/recording"
INTERVAL = 1.3            # MusicBrainz allows 1 req/s; stay comfortably under
THROTTLE_WAIT = 1.5       # pause after a 503 before trying the same query again
THROTTLED_LATENCY = 8.0   # measured: response time under sustained load
BACKOFF_MAX = 30.0

# Lucene syntax that would break a quoted query term.
LUCENE = re.compile(r'[+\-&|!(){}\[\]^"~*?:\\/]')


def _ssl_context() -> ssl.SSLContext:
    """python.org builds on macOS ship without a usable CA bundle.

    ssl.get_default_verify_paths().cafile is None there, so every HTTPS call
    dies with CERTIFICATE_VERIFY_FAILED even though curl works fine. certifi
    carries its own bundle; fall back to the default only if it is absent.
    """
    try:
        import certifi

        return ssl.create_default_context(cafile=certifi.where())
    except ImportError:
        return ssl.create_default_context()


SSL_CTX = _ssl_context()


def display_name(raw: str) -> str:
    """Turn a scraped handle back into something searchable.

    ricky_van_shelton -> Ricky Van Shelton. Stylised names that are genuinely
    written that way (Coma_Cose, Go_A, mxmtoon) keep their capitals or are a
    single token, so they are left alone.
    """
    if re.fullmatch(r"[a-z0-9]+(?:_[a-z0-9]+)+", raw):
        cleaned = re.sub(r"_official$", "", raw)
        return " ".join(w.capitalize() for w in cleaned.split("_"))
    return raw


def term(name: str) -> str:
    return LUCENE.sub(" ", display_name(name)).strip()


def get(url: str, tries: int = 6) -> dict | None:
    """MusicBrainz throttles with a bare 503 rather than a 429.

    A 503 here means "you were early", not "the server is down", so it costs a
    short fixed wait and a retry. Only genuine transport errors escalate — an
    exponential backoff on throttling would turn a 1s pause into a minute.
    """
    delay = 2.0
    for attempt in range(tries):
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        try:
            with urllib.request.urlopen(req, timeout=30, context=SSL_CTX) as fh:
                return json.load(fh)
        except Exception as exc:                       # noqa: BLE001
            code = getattr(exc, "code", None)
            if code == 404:
                return None
            if attempt == tries - 1:
                print(f"    ! desisti: {exc}", flush=True)
                return None
            if code == 503:
                retry_after = 0.0
                hdrs = getattr(exc, "headers", None)
                if hdrs and str(hdrs.get("Retry-After", "")).isdigit():
                    retry_after = float(hdrs.get("Retry-After"))
                time.sleep(max(THROTTLE_WAIT, min(10.0, retry_after)))
                continue
            time.sleep(min(BACKOFF_MAX, delay))
            delay *= 2
    return None


def query_pair(n1: str, n2: str) -> dict | None:
    t1, t2 = term(n1), term(n2)
    if not t1 or not t2:
        return None
    qs = urllib.parse.urlencode(
        {
            "query": f'artist:"{t1}" AND artist:"{t2}"',
            "fmt": "json",
            "limit": 8,
        }
    )
    return get(f"{BASE}?{qs}")


def year_of(rec: dict) -> int | None:
    for rel in rec.get("releases") or []:
        d = rel.get("date") or ""
        if d[:4].isdigit():
            return int(d[:4])
    return None


def credited(rec: dict) -> list[str]:
    return [
        a["artist"]["name"]
        for a in rec.get("artist-credit") or []
        if isinstance(a, dict) and "artist" in a
    ]


def fold(s: str) -> str:
    """Accent- and punctuation-insensitive key for comparing artist names."""
    s = unicodedata.normalize("NFKD", display_name(s))
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()


def credits_both(rec: dict, n1: str, n2: str) -> bool:
    """Does this recording actually credit BOTH artists?

    Lucene scores loosely: `artist:"Jack White" AND artist:"Beck"` happily
    returns a recording that credits neither in full. Without this check the
    tool would swap a fabricated title for an unrelated real one, which is
    worse than leaving the placeholder in place.
    """
    names = [fold(a) for a in credited(rec)]
    joined = " | ".join(names)
    return all(
        any(f == fold(n) for f in names) or fold(n) in joined
        for n in (n1, n2)
    )


def main() -> None:
    limit = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    name = {i: n for (i, n, _g) in ARTISTS}

    with open(AUDIT, encoding="utf-8") as fh:
        audit = json.load(fh)

    # One lookup per artist pair, not per edge — the same two acts often carry
    # several placeholder rows.
    pairs = OrderedDict()
    for e in audit["edges"]:
        if e["verdict"] != "fabricated":
            continue
        key = f"{min(e['a1'], e['a2'])}-{max(e['a1'], e['a2'])}"
        pairs.setdefault(key, []).append(e)

    state = {}
    if os.path.exists(STATE):
        with open(STATE, encoding="utf-8") as fh:
            state = json.load(fh)

    todo = [k for k in pairs if k not in state]
    if limit:
        todo = todo[:limit]

    print(f"pares no total: {len(pairs):,} | ja resolvidos: {len(state):,} | "
          f"nesta rodada: {len(todo):,}", flush=True)
    if not todo:
        print("nada a fazer.")
    else:
        # MusicBrainz throttles by delaying responses rather than rejecting
        # them: latency climbs from ~0.5s to ~8s under sustained load, so
        # budget for the throttled rate, not the polite interval.
        est = len(todo) * (INTERVAL + THROTTLED_LATENCY) / 60
        print(f"estimativa: ~{est:.0f} min (a MusicBrainz atrasa as respostas "
              f"ate ~{THROTTLED_LATENCY:.0f}s sob carga)\n", flush=True)

    started = time.time()
    for n, key in enumerate(todo, 1):
        a1, a2 = (int(x) for x in key.split("-"))
        n1, n2 = name.get(a1, ""), name.get(a2, "")
        data = query_pair(n1, n2)
        time.sleep(INTERVAL)

        if data is None:
            continue                                   # retry on a later run

        # Keep only recordings that credit both acts — a loose Lucene hit is
        # not evidence the pair ever worked together.
        recs = [r for r in (data.get("recordings") or []) if credits_both(r, n1, n2)]
        cands = [
            {
                "title": r["title"],
                "mbid": r["id"],
                "artists": credited(r),
                "year": year_of(r),
                "disambiguation": r.get("disambiguation") or "",
            }
            for r in recs
        ]
        state[key] = {
            "a1": a1,
            "a2": a2,
            "names": [n1, n2],
            "count": data.get("count", 0),
            "confirmed": len(cands),
            "verdict": "repair" if cands else "drop",
            "candidates": cands[:5],
            "placeholders": sorted({e["title"] for e in pairs[key]}),
        }

        mark = "OK " if cands else "-- "
        print(f"  {mark}{n}/{len(todo)}  {n1} × {n2} -> "
              f"{state[key]['verdict']} "
              f"({state[key]['confirmed']}/{state[key]['count']})", flush=True)
        if n % 5 == 0 or n == len(todo):
            elapsed = time.time() - started
            left = (len(todo) - n) * elapsed / max(1, n) / 60
            print(f"     [{n / max(1e-9, elapsed) * 60:.1f}/min, "
                  f"faltam ~{left:.0f} min]", flush=True)
            with open(STATE, "w", encoding="utf-8") as fh:
                json.dump(state, fh, ensure_ascii=False, indent=1)

    with open(STATE, "w", encoding="utf-8") as fh:
        json.dump(state, fh, ensure_ascii=False, indent=1)

    done = [v for v in state.values()]
    rep = [v for v in done if v["verdict"] == "repair"]
    drop = [v for v in done if v["verdict"] == "drop"]
    print()
    print("=" * 70)
    print(f"RESOLVIDOS {len(done):,} pares  |  reparar {len(rep):,}  |  "
          f"remover {len(drop):,}")
    print("=" * 70)
    print("\n  colaboracoes REAIS com titulo placeholder (amostra):")
    for v in rep[:12]:
        best = v["candidates"][0]
        ph = ", ".join(v["placeholders"][:2])
        print(f"    {v['names'][0]} × {v['names'][1]}")
        print(f"      era: {ph!r}  ->  {best['title']!r} ({best['year'] or '?'})")
    print("\n  pares SEM gravacao em comum (propostas de remocao):")
    for v in drop[:12]:
        print(f"    {v['names'][0]} × {v['names'][1]}  "
              f"({', '.join(v['placeholders'][:2])})")
    print(f"\n✅ estado em data/edge_repair.json")


if __name__ == "__main__":
    main()
