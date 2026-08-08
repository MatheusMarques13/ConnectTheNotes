"""Fetch a real popularity signal (Deezer fan count) for every roster artist.

The random-puzzle picker needs to favour artists players actually recognise.
Graph centrality alone can't do that: it measures "does lots of features", which
buries legacy/rock acts (Linkin Park, Ozzy Osbourne, The Notorious B.I.G.) and
over-rates regional collab hubs. Deezer's `nb_fan` is a real audience number, so
we fetch it once per artist and bake it into the dataset at build time.

Matching is deliberately strict: we only accept a Deezer artist whose normalized
name equals ours, so "Air"/"Cream"/"Woods"-style ambiguity fails closed
(match:"none") instead of importing a stranger's fan count. Among several exact
matches we keep the most-followed one, which is the well-known act.

Env: SHARD_INDEX, SHARD_TOTAL, FAME_OUT (dir), FAME_PRIOR (jsonl to resume from).
Writes JSONL: {id, name, dz_id, dz_name, fans, match}
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "data"))

from deezer_verify import norm_name, get, q, GAVE_UP  # noqa: E402
from source_data import ARTISTS  # noqa: E402

API = "https://api.deezer.com"
SHARD_INDEX = int(os.environ.get("SHARD_INDEX", "0"))
SHARD_TOTAL = int(os.environ.get("SHARD_TOTAL", "1"))
OUT_DIR = os.environ.get("FAME_OUT", "out")
PRIOR = os.environ.get("FAME_PRIOR", "")


def lookup(name):
    """-> (dz_id, dz_name, fans, match) ; match in exact|none|error."""
    d = get(f"{API}/search/artist?q={q(name)}&limit=10")
    if d is GAVE_UP:
        return None, None, None, "error"
    if not d or not d.get("data"):
        return None, None, None, "none"
    target = norm_name(name)
    exact = [a for a in d["data"] if norm_name(a.get("name")) == target]
    if not exact:
        return None, None, None, "none"
    best = max(exact, key=lambda a: a.get("nb_fan") or 0)
    return best.get("id"), best.get("name"), best.get("nb_fan") or 0, "exact"


def main():
    done = set()
    if PRIOR and os.path.exists(PRIOR):
        with open(PRIOR, encoding="utf-8") as fh:
            for line in fh:
                try:
                    r = json.loads(line)
                except Exception:
                    continue
                # Only treat a row as settled if it actually resolved; transient
                # errors get retried on the next run.
                if r.get("match") in ("exact", "none"):
                    done.add(r["id"])

    mine = [(i, n) for (i, n, _g) in ARTISTS
            if i % SHARD_TOTAL == SHARD_INDEX and i not in done]
    os.makedirs(OUT_DIR, exist_ok=True)
    path = os.path.join(OUT_DIR, "artist_fame.jsonl")
    written = errors = 0
    with open(path, "w", encoding="utf-8") as out:
        for k, (aid, name) in enumerate(mine):
            dz_id, dz_name, fans, match = lookup(name)
            if match == "error":
                errors += 1
                continue
            out.write(json.dumps({"id": aid, "name": name, "dz_id": dz_id,
                                  "dz_name": dz_name, "fans": fans,
                                  "match": match}, ensure_ascii=False) + "\n")
            out.flush()
            written += 1
            if k % 25 == 0:
                print(f"[{SHARD_INDEX}] {k}/{len(mine)} written={written}", flush=True)
    print(f"SHARD DONE written={written} errors={errors}", flush=True)


if __name__ == "__main__":
    main()
