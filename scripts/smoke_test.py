"""End-to-end smoke test of the (in-memory) backend.
Exercises server.py's actual route handlers + a full simulated playthrough.
No database needed.

Run from repo root:  python scripts/smoke_test.py
"""
import asyncio
import os
import sys
import random

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "backend"))

import server
import store
from server import FindPathRequest


def line(c="─"):
    print(c * 60)


async def main():
    line("=")
    print("1) DATA (loaded in memory at import — no DB)")
    stats = await server.get_stats()
    print(f"   GET /api/stats -> {stats}")
    assert stats["totalArtists"] == 95, stats

    line("=")
    print("2) DAILY PUZZLE (deterministic per date)")
    d1 = await server.daily_puzzle(date="2026-06-27")
    d1b = await server.daily_puzzle(date="2026-06-27")
    d2 = await server.daily_puzzle(date="2026-06-28")
    print(f"   2026-06-27 -> {d1['artist1']['name']} → {d1['artist2']['name']} (par {d1['optimalSteps']})")
    print(f"   2026-06-28 -> {d2['artist1']['name']} → {d2['artist2']['name']} (par {d2['optimalSteps']})")
    assert (d1["artist1"]["id"], d1["artist2"]["id"]) == (d1b["artist1"]["id"], d1b["artist2"]["id"])
    print("   ✅ same date => same puzzle")

    line("=")
    print("3) RANDOM PAIR by difficulty (graph distance)")
    for diff in ["easy", "medium", "hard"]:
        p = await server.random_pair(difficulty=diff)
        print(f"   {diff:6} -> {p['artist1']['name']} → {p['artist2']['name']} (par {p['optimalSteps']})")

    line("=")
    print("4) FIND-PATH + 'kind' marker / album type preserved")
    fp = await server.find_path(FindPathRequest(startId=d1["artist1"]["id"], endId=d1["artist2"]["id"]))
    path = fp["path"]
    pretty = []
    for node in path:
        if node["kind"] == "artist":
            pretty.append(node["artist"]["name"])
        else:
            s = node["song"]
            pretty.append(f'“{s["title"]}” [{s["type"]}]')
    print("   " + "  →  ".join(pretty))
    assert path[0]["kind"] == "artist" and path[1]["kind"] == "song"
    print(f"   optimalSteps = {fp['optimalSteps']}  ✅ alternating artist/song, song type intact")

    line("=")
    print("5) SIMULATED PLAYTHROUGH (follow the optimal chain to a WIN)")
    target = d1["artist2"]
    cur = d1["artist1"]
    print(f"   Goal: connect {cur['name']} → {target['name']}")
    steps_taken = 0
    i = 0
    while i < len(path) - 1:
        song = path[i + 1]["song"]
        nxt = path[i + 2]["artist"]
        between = await server.get_connections_between(cur["id"], nxt["id"])
        legal = song["title"] in [c["song"]["title"] for c in between["connections"]]
        steps_taken += 1
        print(f"   step {steps_taken}: {cur['name']} --“{song['title']}”--> {nxt['name']}   {'✓' if legal else '✗ ILLEGAL'}")
        assert legal
        cur = nxt
        i += 2
    print(f"   reached {cur['name']} -> {'🎉 WIN' if cur['id'] == target['id'] else 'NOT TARGET'} in {steps_taken} steps (par {d1['optimalSteps']})")
    assert cur["id"] == target["id"]

    line("=")
    print("6) SOLVABILITY GUARANTEE — 300 random pairs, expect 0 unsolvable")
    rng = random.Random(7)
    unsolvable = 0
    for _ in range(300):
        a, b = rng.sample(store.ARTIST_LIST, 2)
        r = await server.find_path(FindPathRequest(startId=a["id"], endId=b["id"]))
        if r["path"] is None:
            unsolvable += 1
    print(f"   unsolvable pairs: {unsolvable} / 300")
    assert unsolvable == 0

    line("=")
    print("✅ ALL SMOKE CHECKS PASSED — in-memory backend behaves correctly")


if __name__ == "__main__":
    asyncio.run(main())
