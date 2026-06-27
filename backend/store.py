"""In-memory data store for Connect the Notes.

The game data is a small, static, read-only graph, so there is no need for a
database: everything is loaded from seed_data.py into memory once at import.
This keeps the app dependency-free (no MongoDB), trivially testable, and
deployable to serverless with zero configuration.
"""
from typing import List, Optional, Dict

from seed_data import ARTISTS, COLLABORATIONS
from game_logic import build_adjacency


def _slug(n: int) -> str:
    return f"a{n}"


# ── Build artists ──────────────────────────────────────────
ARTISTS_BY_ID: Dict[str, dict] = {}
ARTIST_LIST: List[dict] = []
for _id, _name, _genre in ARTISTS:
    doc = {"id": _slug(_id), "name": _name, "genre": _genre, "imageUrl": ""}
    ARTISTS_BY_ID[doc["id"]] = doc
    ARTIST_LIST.append(doc)

# ── Build connections (dedupe parallel duplicates: same pair + title) ──
CONNECTIONS: List[dict] = []
_seen = set()
for _a1, _a2, _title, _type, _year in COLLABORATIONS:
    s1, s2 = _slug(_a1), _slug(_a2)
    if s1 not in ARTISTS_BY_ID or s2 not in ARTISTS_BY_ID or s1 == s2:
        continue
    key = (min(_a1, _a2), max(_a1, _a2), _title)
    if key in _seen:
        continue
    _seen.add(key)
    CONNECTIONS.append({
        "id": f"c{len(CONNECTIONS)}",
        "artist1": s1,
        "artist2": s2,
        "song": {"title": _title, "type": _type, "year": _year, "coverUrl": ""},
    })

# ── Adjacency for BFS (reuses the pure graph helper) ──
ADJACENCY = build_adjacency(CONNECTIONS)


# ── Query API (mirrors what the endpoints need) ────────────

def search_artists(query: Optional[str], limit: int = 10) -> List[dict]:
    if query and len(query) >= 1:
        q = query.lower()
        out = [a for a in ARTIST_LIST if q in a["name"].lower()]
    else:
        out = ARTIST_LIST
    return out[:limit]


def random_artist(exclude_ids=None, rng=None):
    import random as _random
    rng = rng or _random
    pool = [a for a in ARTIST_LIST if not exclude_ids or a["id"] not in exclude_ids]
    return rng.choice(pool) if pool else None


def get_artist(artist_id: str) -> Optional[dict]:
    return ARTISTS_BY_ID.get(artist_id)


def get_artists(ids) -> Dict[str, dict]:
    return {i: ARTISTS_BY_ID[i] for i in set(ids) if i in ARTISTS_BY_ID}


def connections_for(artist_id: str) -> List[dict]:
    return [c for c in CONNECTIONS if c["artist1"] == artist_id or c["artist2"] == artist_id]


def connected_artists(artist_id: str) -> List[dict]:
    ids = set()
    for c in connections_for(artist_id):
        ids.add(c["artist2"] if c["artist1"] == artist_id else c["artist1"])
    return [ARTISTS_BY_ID[i] for i in ids if i in ARTISTS_BY_ID]


def connections_between(id1: str, id2: str) -> List[dict]:
    return [c for c in CONNECTIONS
            if {c["artist1"], c["artist2"]} == {id1, id2}]


def stats() -> dict:
    return {"totalArtists": len(ARTIST_LIST), "totalConnections": len(CONNECTIONS)}
