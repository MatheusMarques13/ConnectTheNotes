"""Resolve a real photo URL for every artist that has a Deezer id.

Why this exists: frontend/scripts/fetch-images.mjs looks photos up by NAME on
every build, under an 18-minute deadline shared with ~13k song covers. With
5.6k artists it never gets through the list, so whoever sits late in the queue
ships with no photo — and a name search can also land on the wrong artist.

We already know each artist's exact Deezer id (data/artist_fame.json), so this
fetches the picture by id, once, and the result is committed as
data/artist_images.json. The build then just reads that file: no lookup, no
deadline, no wrong-artist matches.

Env: SHARD_INDEX, SHARD_TOTAL, IMG_OUT (dir), IMG_PRIOR (jsonl to resume from).
Writes JSONL: {id, dz, url}
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "data"))

from deezer_verify import get, GAVE_UP  # noqa: E402

API = "https://api.deezer.com"
FAME = os.path.join(HERE, "..", "data", "artist_fame.json")
SHARD_INDEX = int(os.environ.get("SHARD_INDEX", "0"))
SHARD_TOTAL = int(os.environ.get("SHARD_TOTAL", "1"))
OUT_DIR = os.environ.get("IMG_OUT", "out")
PRIOR = os.environ.get("IMG_PRIOR", "")


def main():
    from source_data import ARTISTS  # imported late so the path insert applies
    live = {i for (i, _n, _g) in ARTISTS}

    with open(FAME, encoding="utf-8") as fh:
        fame = json.load(fh)
    targets = []
    for k, v in fame.items():
        i = int(k)
        if i not in live or not isinstance(v, dict) or v.get("dz") is None:
            continue
        targets.append((i, v["dz"]))

    done = set()
    if PRIOR and os.path.exists(PRIOR):
        with open(PRIOR, encoding="utf-8") as fh:
            for line in fh:
                try:
                    r = json.loads(line)
                except Exception:
                    continue
                if r.get("url"):
                    done.add(r["id"])

    mine = [(i, d) for (i, d) in targets
            if i % SHARD_TOTAL == SHARD_INDEX and i not in done]
    os.makedirs(OUT_DIR, exist_ok=True)
    path = os.path.join(OUT_DIR, "artist_images.jsonl")
    got = 0
    with open(path, "w", encoding="utf-8") as out:
        for k, (aid, dz_id) in enumerate(mine):
            d = get(f"{API}/artist/{dz_id}")
            if d is GAVE_UP or not d:
                continue
            url = d.get("picture_xl") or d.get("picture_big") or d.get("picture_medium") or ""
            # Deezer returns a placeholder path for artists with no photo.
            if not url or "/artist//" in url:
                continue
            out.write(json.dumps({"id": aid, "dz": dz_id, "url": url}) + "\n")
            out.flush()
            got += 1
            if k % 50 == 0:
                print(f"[{SHARD_INDEX}] {k}/{len(mine)} got={got}", flush=True)
    print(f"SHARD DONE checked={len(mine)} got={got}", flush=True)


if __name__ == "__main__":
    main()
