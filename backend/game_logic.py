"""Pure graph logic for Connect the Notes — no database dependency, so it can
be unit-tested directly against the seed data."""
from collections import deque
from typing import Dict, List, Tuple

# Difficulty expressed as a band of shortest-path distance (hops) between the
# two artists — the real source of difficulty in a connection game.
DIFFICULTY_BANDS: Dict[str, Tuple[int, int]] = {
    "easy": (2, 3),
    "medium": (3, 4),
    "hard": (4, 7),
    "any": (2, 7),
}

Adjacency = Dict[str, List[Tuple[str, dict]]]


def build_adjacency(connections) -> Adjacency:
    """connections: iterable of {artist1, artist2, song} -> adjacency map
    artist_id -> list of (neighbor_id, song)."""
    adj: Adjacency = {}
    for c in connections:
        a1, a2, song = c["artist1"], c["artist2"], c["song"]
        adj.setdefault(a1, []).append((a2, song))
        adj.setdefault(a2, []).append((a1, song))
    return adj


def bfs_steps(adj: Adjacency, start, end):
    """Shortest path as a list of (from_id, song, to_id) steps.
    Returns [] if start == end, or None if unreachable."""
    if start == end:
        return []
    visited = {start}
    queue = deque([(start, [])])
    while queue:
        cur, path = queue.popleft()
        for nb, song in adj.get(cur, []):
            if nb == end:
                return path + [(cur, song, nb)]
            if nb not in visited:
                visited.add(nb)
                queue.append((nb, path + [(cur, song, nb)]))
    return None


def bfs_distances(adj: Adjacency, start) -> Dict[str, int]:
    dist = {start: 0}
    queue = deque([start])
    while queue:
        cur = queue.popleft()
        for nb, _ in adj.get(cur, []):
            if nb not in dist:
                dist[nb] = dist[cur] + 1
                queue.append(nb)
    return dist


def build_path(start_id, steps, artists: Dict[str, dict]):
    """Build the alternating artist/song path the frontend consumes.
    Uses 'kind' as the structural marker so the song's own 'type'
    (song/album/live/feature) is never overwritten."""
    path = [{"kind": "artist", "artist": artists.get(start_id)}]
    for _frm, song, to in steps:
        path.append({"kind": "song", "song": song})
        path.append({"kind": "artist", "artist": artists.get(to)})
    return path


def pick_pair_in_band(adj: Adjacency, rng, lo: int, hi: int):
    """Pick a (start, end, distance) whose shortest path is within [lo, hi].
    Falls back to any reachable pair at distance >= 2."""
    ids = list(adj.keys())
    if not ids:
        return None
    for _ in range(60):
        start = rng.choice(ids)
        dist = bfs_distances(adj, start)
        candidates = [a for a, d in dist.items() if lo <= d <= hi]
        if candidates:
            end = rng.choice(candidates)
            return start, end, dist[end]
    start = rng.choice(ids)
    dist = bfs_distances(adj, start)
    far = [(a, d) for a, d in dist.items() if d >= 2]
    if far:
        end, d = rng.choice(far)
        return start, end, d
    return None
