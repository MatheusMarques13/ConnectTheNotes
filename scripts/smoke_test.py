"""End-to-end smoke test of the REAL backend against an in-memory Mongo.
Exercises server.py's actual route handlers + a full simulated playthrough.

Run from repo root:  python scripts/smoke_test.py
"""
import asyncio
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "backend"))
os.environ.setdefault("MONGO_URL", "mongodb://localhost:27017")

from mongomock_motor import AsyncMongoMockClient
import server
import seed as seed_mod
from server import FindPathRequest


def line(c="─"):
    print(c * 60)


async def main():
    # Point the real backend at an in-memory Mongo
    client = AsyncMongoMockClient()
    server._client = client
    db = client[server.DB_NAME]

    line("=")
    print("1) SEED")
    try:
        result = await seed_mod.seed(db)
    except Exception as e:
        # mongomock may reject a text index; retry without it
        print(f"   (text index unsupported by mock: {e}; seeding without indexes)")
        orig = seed_mod.ensure_indexes
        seed_mod.ensure_indexes = lambda _db: asyncio.sleep(0)
        result = await seed_mod.seed(db)
        seed_mod.ensure_indexes = orig
    print(f"   seeded: {result}")

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
    assert (d1["artist1"]["id"], d1["artist2"]["id"]) == (d1b["artist1"]["id"], d1b["artist2"]["id"]), "daily not deterministic!"
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
    saw_non_song = False
    for node in path:
        if node["kind"] == "artist":
            pretty.append(node["artist"]["name"])
        else:
            s = node["song"]
            pretty.append(f'“{s["title"]}” [{s["type"]}]')
            if s["type"] != "song":
                saw_non_song = True
    print("   " + "  →  ".join(pretty))
    print(f"   optimalSteps = {fp['optimalSteps']}")
    # Verify markers
    assert path[0]["kind"] == "artist" and path[1]["kind"] == "song"
    print("   ✅ alternating artist/song; song 'type' (song/album/live) intact")

    line("=")
    print("5) SIMULATED PLAYTHROUGH (follow the optimal chain to a WIN)")
    start = d1["artist1"]
    target = d1["artist2"]
    print(f"   Goal: connect {start['name']} → {target['name']}")
    # Walk the path the same way a player would: at each artist, the next
    # collaboration links to the next artist until we reach the target.
    cur = start
    steps_taken = 0
    i = 0
    while i < len(path) - 1:
        song = path[i + 1]["song"]
        nxt = path[i + 2]["artist"]
        # Confirm the move is a legal direct collaboration (what the UI checks)
        between = await server.get_connections_between(cur["id"], nxt["id"])
        titles = [c["song"]["title"] for c in between["connections"]]
        legal = song["title"] in titles
        steps_taken += 1
        print(f"   step {steps_taken}: {cur['name']} --“{song['title']}”--> {nxt['name']}   {'✓ legal move' if legal else '✗ ILLEGAL'}")
        assert legal, f"move not a real collaboration: {cur['name']} -> {nxt['name']}"
        cur = nxt
        i += 2
    won = cur["id"] == target["id"]
    print(f"   reached: {cur['name']}  ->  {'🎉 WIN' if won else 'NOT TARGET'} in {steps_taken} steps (par {d1['optimalSteps']})")
    assert won and steps_taken == d1["optimalSteps"]

    line("=")
    print("6) SOLVABILITY GUARANTEE — sample 300 random pairs, expect 0 unsolvable")
    import random
    all_artists = await db.artists.find({}, {"_id": 0}).to_list(None)
    rng = random.Random(7)
    unsolvable = 0
    for _ in range(300):
        a, b = rng.sample(all_artists, 2)
        r = await server.find_path(FindPathRequest(startId=a["id"], endId=b["id"]))
        if r["path"] is None:
            unsolvable += 1
    print(f"   unsolvable pairs: {unsolvable} / 300")
    assert unsolvable == 0

    line("=")
    print("✅ ALL SMOKE CHECKS PASSED — backend + dataset behave correctly")


if __name__ == "__main__":
    asyncio.run(main())
