"""Measure what the random puzzle picker actually serves up.

Mirrors the selection logic in frontend/src/services/api.js against the shipped
dataset.js, so we can compare the old uniform picker with the fame-weighted one
instead of eyeballing a few rolls.

Run:  python tools/sim_random.py [trials]
"""
import json
import os
import random
import re
import sys
from collections import Counter, deque

HERE = os.path.dirname(os.path.abspath(__file__))
DATASET = os.path.join(HERE, "..", "frontend", "src", "data", "dataset.js")
BANDS = {"easy": (2, 3), "medium": (3, 4), "hard": (4, 7), "any": (2, 7)}


def load():
    src = open(DATASET, encoding="utf-8").read()

    def grab(name):
        m = re.search(r"export const %s = (\[.*?\]);\n" % name, src, re.S)
        return json.loads(m.group(1)) if m else []

    return grab("ARTISTS"), grab("SONGS"), grab("FAMOUS_IDS")


def adjacency(songs):
    adj = {}
    for s in songs:
        for a in s["artists"]:
            for b in s["artists"]:
                if a != b:
                    adj.setdefault(a, set()).add(b)
    return adj


def bfs(adj, start):
    dist = {start: 0}
    q = deque([start])
    while q:
        cur = q.popleft()
        for nxt in adj.get(cur, ()):
            if nxt not in dist:
                dist[nxt] = dist[cur] + 1
                q.append(nxt)
    return dist


def weighted(rng, ids, fame):
    tot = sum((fame.get(i, 1) or 1) ** 2 for i in ids)
    r = rng.random() * tot
    for i in ids:
        r -= (fame.get(i, 1) or 1) ** 2
        if r <= 0:
            return i
    return ids[-1]


def pick(rng, adj, ids, fame, pool, lo, hi, weighted_mode):
    for _ in range(60):
        start = weighted(rng, pool, fame) if weighted_mode else rng.choice(ids)
        dist = bfs(adj, start)
        if weighted_mode:
            cands = [i for i in pool if lo <= dist.get(i, -1) <= hi]
        else:
            cands = [i for i, d in dist.items() if lo <= d <= hi]
        if cands:
            end = weighted(rng, cands, fame) if weighted_mode else rng.choice(cands)
            return start, end
    return None, None


def main():
    trials = int(sys.argv[1]) if len(sys.argv) > 1 else 300
    artists, songs, pool = load()
    by_id = {a["id"]: a for a in artists}
    fame = {a["id"]: a.get("fame", 1) for a in artists}
    adj = adjacency(songs)
    ids = [a["id"] for a in artists]
    lo, hi = BANDS["any"]

    for mode, label in ((False, "ANTES (uniforme)"), (True, "DEPOIS (ponderado)")):
        rng = random.Random(20260808)
        names = Counter()
        fames = []
        for _ in range(trials):
            a, b = pick(rng, adj, ids, fame, pool, lo, hi, mode)
            if not a:
                continue
            for x in (a, b):
                names[by_id[x]["name"]] += 1
                fames.append(fame[x])
        fames.sort()
        med = fames[len(fames) // 2] if fames else 0
        in_pool = sum(1 for f in fames if f >= min(fame[i] for i in pool))
        print(f"\n=== {label} — {trials} sorteios ===")
        print(f"fama mediana do artista sorteado: {med}/1000 | "
              f"dentro do pool famoso: {100 * in_pool // max(1, len(fames))}%")
        print("mais sorteados: " + ", ".join(f"{n}" for n, _ in names.most_common(18)))
        rare = [n for n, c in names.items() if c == 1]
        print(f"exemplos da cauda: {', '.join(rare[:12])}")


if __name__ == "__main__":
    main()
