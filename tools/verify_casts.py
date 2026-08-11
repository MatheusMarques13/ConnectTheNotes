"""Find artists credited on songs they are not actually on.

'I Like It' (2018) shipped as Bad Bunny + Cardi B + J. Balvin + Shakira. The
real track is the first three. One fabricated pairwise row — Shakira × Cardi B —
was enough, because data/build.py merges every row sharing (title, type, year)
into one song and unions the casts. So a single bad row does not add one wrong
link, it adds one per other artist on the track.

That makes multi-artist songs the place where fabrication concentrates and the
place worth checking. For each one this asks MusicBrainz for the title, keeps
the recordings that clearly ARE our song, and reports anyone we credit who
appears on none of them.

The rule is deliberately one-sided. A miss proves nothing — MusicBrainz has
thin coverage of recent Brazilian releases, as the earlier passes showed — so a
song is only judged when a matching recording was actually found and at least
two of our artists are on it. Everything else is left alone.

Nothing is written back to source_data.py; use tools/apply_cast_fixes.py.

Run:  python3 tools/verify_casts.py [max_songs]
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

STATE = os.path.join(ROOT, "data", "cast_audit.json")

BASE = "https://musicbrainz.org/ws/2/recording"
UA = "ConnectTheNotes/0.1 ( matheusbmarques13@gmail.com )"
INTERVAL = 1.15
# Below this many of our artists confirmed, we cannot tell "wrong cast" from
# "MusicBrainz found a different song with the same name".
MIN_ANCHOR = 2
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
    s = s.lower().replace("&", " and ")
    return re.sub(r"[^a-z0-9]+", " ", s).strip()


def title_key(t: str) -> str:
    """Drop the credit and variant tail so 'Work (feat. Drake)' matches 'Work'."""
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


def credited(rec: dict) -> list[str]:
    names = [
        a["artist"]["name"]
        for a in rec.get("artist-credit") or []
        if isinstance(a, dict) and "artist" in a
    ]
    # Guests are often only in the title: "Work (feat. Drake)".
    for m in re.finditer(r"[\(\[][^)\]]*\b(?:feat|ft|with)\.?\s+([^)\]]+)[\)\]]",
                         rec.get("title") or "", re.I):
        names.extend(re.split(r"\s*(?:,|&|\band\b|\bx\b)\s*", m.group(1)))
    return [n.strip() for n in names if n and n.strip()]


def songs_from_source() -> list[dict]:
    """Rebuild the merged songs exactly as data/build.py does."""
    name = {i: n for (i, n, _g) in ARTISTS}
    groups = {}
    for a1, a2, title, ctype, year in COLLABORATIONS:
        if a1 == a2:
            continue
        key = (re.sub(r"\s+", " ", title.strip()).lower(), ctype, year)
        g = groups.setdefault(key, {"title": title, "type": ctype,
                                    "year": year, "ids": set()})
        g["ids"].update((a1, a2))
    out = []
    for g in groups.values():
        if len(g["ids"]) >= 3:                          # contamination shows here
            out.append(
                {
                    "title": g["title"], "type": g["type"], "year": g["year"],
                    "ids": sorted(g["ids"]),
                    "names": [name.get(i, "") for i in sorted(g["ids"])],
                }
            )
    out.sort(key=lambda s: -len(s["ids"]))
    return out


def main() -> None:
    budget = int(sys.argv[1]) if len(sys.argv) > 1 else 0

    songs = songs_from_source()
    state = {}
    if os.path.exists(STATE):
        with open(STATE, encoding="utf-8") as fh:
            state = json.load(fh)

    todo = [s for s in songs if f"{title_key(s['title'])}|{s['year']}" not in state]
    if budget:
        todo = todo[:budget]

    print(f"musicas com 3+ artistas: {len(songs):,} | ja checadas: {len(state):,} "
          f"| nesta rodada: {len(todo):,}", flush=True)

    started = time.time()
    for n, s in enumerate(todo, 1):
        key = f"{title_key(s['title'])}|{s['year']}"
        term = LUCENE.sub(" ", s["title"]).strip()
        if not term:
            state[key] = {"verdict": "skip"}
            continue
        # Anchor the search on one of our own artists. Searching a title alone
        # fails on common ones: `recording:"I Like It"` returns 25 unrelated
        # songs and never reaches Cardi B's, so the song came back "not-found"
        # while its cast was exactly the one we needed to check.
        # Two anchors, because the first one might be the impostor: anchoring
        # 'I Like It' on Shakira would find nothing and wrongly clear the row.
        # Ids run roughly fame-first, so try the two best-known names.
        data = None
        for anchor_name in s["names"][:2]:
            anchor = LUCENE.sub(" ", anchor_name).strip()
            query = f'recording:"{term}"'
            if anchor:
                query += f' AND artist:"{anchor}"'
            qs = urllib.parse.urlencode({"query": query, "fmt": "json", "limit": 25})
            data = get(f"{BASE}?{qs}")
            time.sleep(INTERVAL)
            if data and (data.get("recordings") or []):
                break
        if not data:
            continue

        want = title_key(s["title"])
        ours = {fold(x): x for x in s["names"]}
        seen_names: set[str] = set()
        matched = 0
        for rec in data.get("recordings") or []:
            if title_key(rec.get("title") or "") != want:
                continue
            names = {fold(x) for x in credited(rec)}
            if len(names & set(ours)) >= MIN_ANCHOR:
                matched += 1
                seen_names |= names

        if not matched:
            state[key] = {"verdict": "not-found", "title": s["title"],
                          "year": s["year"]}
        else:
            missing = [
                orig for f, orig in ours.items()
                if not any(f == x or f in x or x in f for x in seen_names)
            ]
            state[key] = {
                "verdict": "extra-artists" if missing else "clean",
                "title": s["title"],
                "year": s["year"],
                "cast": s["names"],
                "ids": s["ids"],
                "not_credited": missing,
                "recordings_matched": matched,
            }
            if missing:
                print(f"  ! {s['title']!r} ({s['year']}): "
                      f"{', '.join(missing)} nao aparece nos creditos", flush=True)

        if n % 20 == 0 or n == len(todo):
            el = time.time() - started
            with open(STATE, "w", encoding="utf-8") as fh:
                json.dump(state, fh, ensure_ascii=False, indent=1)
            print(f"  [{n}/{len(todo)}  {n / max(1e-9, el) * 60:.0f}/min  "
                  f"faltam ~{(len(todo) - n) * el / max(1, n) / 60:.0f} min]", flush=True)

    with open(STATE, "w", encoding="utf-8") as fh:
        json.dump(state, fh, ensure_ascii=False, indent=1)

    bad = [v for v in state.values() if v.get("verdict") == "extra-artists"]
    tot = sum(len(v["not_credited"]) for v in bad)
    print()
    print("=" * 70)
    print(f"MUSICAS COM ELENCO CONTAMINADO: {len(bad)}  ({tot} artistas a remover)")
    print("=" * 70)
    for v in bad[:25]:
        print(f"  {v['title']!r} ({v['year']})")
        print(f"      temos : {', '.join(v['cast'])}")
        print(f"      fora  : {', '.join(v['not_credited'])}")
    print(f"\n✅ estado em data/cast_audit.json")


if __name__ == "__main__":
    main()
