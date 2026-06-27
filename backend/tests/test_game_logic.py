"""Tests for the dataset invariant and pure graph logic.
No database required — runs against seed_data.py directly.

Run:  python -m pytest backend/tests/  (or)  python backend/tests/test_game_logic.py
"""
import os
import sys
import random

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from seed_data import ARTISTS, COLLABORATIONS  # noqa: E402
from game_logic import (  # noqa: E402
    DIFFICULTY_BANDS,
    build_adjacency,
    bfs_steps,
    bfs_distances,
    build_path,
    pick_pair_in_band,
)


def _adjacency():
    conns = [
        {"artist1": a1, "artist2": a2, "song": {"title": title, "type": ctype, "year": year}}
        for (a1, a2, title, ctype, year) in COLLABORATIONS
    ]
    return build_adjacency(conns)


def test_dataset_is_single_connected_component():
    """The whole point of the revival: every artist pair must be solvable."""
    adj = _adjacency()
    ids = [a[0] for a in ARTISTS]
    dist = bfs_distances(adj, ids[0])
    unreachable = [i for i in ids if i not in dist]
    assert not unreachable, f"Unreachable artists -> {unreachable}"
    assert len(dist) == len(ids)


def test_every_pair_is_solvable():
    adj = _adjacency()
    ids = [a[0] for a in ARTISTS]
    # All-pairs reachability via per-source BFS distances.
    for s in ids:
        dist = bfs_distances(adj, s)
        assert len(dist) == len(ids), f"{s} cannot reach everyone"


def test_bfs_steps_finds_path_and_marks_kind():
    adj = _adjacency()
    ids = [a[0] for a in ARTISTS]
    steps = bfs_steps(adj, ids[0], ids[-1])
    assert steps, "Expected a path between two artists"
    artists = {a[0]: {"id": a[0], "name": a[1], "genre": a[2]} for a in ARTISTS}
    path = build_path(ids[0], steps, artists)
    # Alternating artist/song/artist...
    assert path[0]["kind"] == "artist"
    assert path[1]["kind"] == "song"
    # Album/live songs keep their own type (no collision with the 'kind' marker).
    for node in path:
        if node["kind"] == "song":
            assert node["song"]["type"] in {"song", "album", "live", "feature"}


def test_same_artist_returns_empty_path():
    adj = _adjacency()
    ids = [a[0] for a in ARTISTS]
    assert bfs_steps(adj, ids[0], ids[0]) == []


def test_pick_pair_respects_difficulty_band():
    adj = _adjacency()
    rng = random.Random(42)
    for diff, (lo, hi) in DIFFICULTY_BANDS.items():
        picked = pick_pair_in_band(adj, rng, lo, hi)
        assert picked is not None
        start, end, dist = picked
        assert start != end
        assert lo <= dist <= hi, f"{diff}: distance {dist} outside [{lo},{hi}]"


def test_daily_is_deterministic_per_date():
    """Same date -> same puzzle (seeded RNG)."""
    import hashlib
    adj = _adjacency()
    lo, hi = DIFFICULTY_BANDS["medium"]

    def daily_for(day):
        seed_int = int(hashlib.sha256(day.encode()).hexdigest(), 16) % (2 ** 32)
        return pick_pair_in_band(adj, random.Random(seed_int), lo, hi)

    assert daily_for("2026-06-27") == daily_for("2026-06-27")
    # Extremely unlikely to collide across two different dates.
    assert daily_for("2026-06-27") != daily_for("2026-06-28")


if __name__ == "__main__":
    funcs = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    failed = 0
    for fn in funcs:
        try:
            fn()
            print(f"  ✅ {fn.__name__}")
        except AssertionError as e:
            failed += 1
            print(f"  ❌ {fn.__name__}: {e}")
    print(f"\n{len(funcs) - failed}/{len(funcs)} passed")
    sys.exit(1 if failed else 0)
