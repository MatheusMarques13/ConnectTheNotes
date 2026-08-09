"""Check proposed collaborations against the Deezer catalog before they are added.

New rows must clear the same bar as the rest of the dataset: the recording has
to exist and BOTH claimed artists have to be credited on it. This runs over a
candidate file instead of data/source_data.py, so nothing unverified is ever
committed to the game data.

Env: CAND_IN (json list of [a, b, title, type, year]), CAND_OUT (dir),
     SHARD_INDEX, SHARD_TOTAL.
Writes JSONL: {a, b, title, type, year, verdict, credited, link}
  verdict "ok"       -> both artists credited; safe to add
          "partial"  -> track found, the pair is not both on it; reject
          "notfound" -> no such recording surfaced; reject
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from deezer_verify import norm_name, verify_song  # noqa: E402

CAND_IN = os.environ.get("CAND_IN", "audit_data/candidates.json")
OUT_DIR = os.environ.get("CAND_OUT", "out")
SHARD_INDEX = int(os.environ.get("SHARD_INDEX", "0"))
SHARD_TOTAL = int(os.environ.get("SHARD_TOTAL", "1"))


def main():
    with open(CAND_IN, encoding="utf-8") as fh:
        rows = json.load(fh)
    mine = [r for k, r in enumerate(rows) if k % SHARD_TOTAL == SHARD_INDEX]
    os.makedirs(OUT_DIR, exist_ok=True)
    path = os.path.join(OUT_DIR, "candidates_done.jsonl")
    ok = 0
    with open(path, "w", encoding="utf-8") as out:
        for k, (a, b, title, ctype, year) in enumerate(mine):
            needed = {norm_name(a), norm_name(b)}
            credited, link, complete = verify_song(title, ctype, [a, b], needed)
            if not credited:
                verdict = "notfound" if complete else "unknown"
            elif needed <= credited:
                verdict = "ok"
            else:
                verdict = "partial"
            if verdict == "ok":
                ok += 1
            out.write(json.dumps({
                "a": a, "b": b, "title": title, "type": ctype, "year": year,
                "verdict": verdict, "link": link,
                "credited": sorted(credited)[:12],
            }, ensure_ascii=False) + "\n")
            out.flush()
            if k % 10 == 0:
                print(f"[{SHARD_INDEX}] {k}/{len(mine)} ok={ok}", flush=True)
    print(f"SHARD DONE checked={len(mine)} ok={ok}", flush=True)


if __name__ == "__main__":
    main()
