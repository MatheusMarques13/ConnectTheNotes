"""Merge Deezer verification shard outputs with prior combined results.

Usage: python3 tools/deezer_merge.py OUT_FILE INPUT1 [INPUT2 ...]
Each input is a songs_done.jsonl (prior combined file and/or per-shard files).
Dedupes by song key; a row with a non-null link always beats one without.
"""
import sys, json

out_path, inputs = sys.argv[1], sys.argv[2:]
best = {}
for path in inputs:
    try:
        fh = open(path, encoding="utf-8")
    except FileNotFoundError:
        continue
    with fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                r = json.loads(line)
                k = tuple(r["key"])
            except Exception:
                continue
            cur = best.get(k)
            if cur is None or (r.get("link") and not cur.get("link")):
                best[k] = r

with open(out_path, "w", encoding="utf-8") as fh:
    for r in best.values():
        fh.write(json.dumps(r, ensure_ascii=False) + "\n")
print(f"merged {len(inputs)} inputs -> {len(best)} unique songs "
      f"({sum(1 for r in best.values() if r.get('link'))} with link)")
