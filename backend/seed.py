"""
Seed script for Connect the Notes.

Game mode: artists are connected by SHARED SONGS.
  Example path: Taylor Swift -> "Everything Has Changed" -> Ed Sheeran

The canonical dataset lives in seed_data.py and is already filtered to a single
connected component, so EVERY artist pair is solvable. This script re-verifies
that invariant before inserting and fails loudly if it is ever broken.

Run standalone:   python seed.py
Or via the protected admin endpoint (POST /api/admin/seed with the seed token).
"""
import asyncio
import os
import uuid
from collections import deque

from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
from pathlib import Path

from seed_data import ARTISTS, COLLABORATIONS

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')


def uid():
    return str(uuid.uuid4())[:8]


def _assert_single_component(artist_ids, edges):
    """Fail loudly unless every artist is reachable from every other one."""
    adj = {a: set() for a in artist_ids}
    for a1, a2 in edges:
        adj[a1].add(a2)
        adj[a2].add(a1)
    start = next(iter(artist_ids))
    seen = {start}
    queue = deque([start])
    while queue:
        node = queue.popleft()
        for nb in adj[node]:
            if nb not in seen:
                seen.add(nb)
                queue.append(nb)
    if len(seen) != len(artist_ids):
        unreachable = set(artist_ids) - seen
        raise RuntimeError(
            f"Dataset is NOT a single connected component: "
            f"{len(unreachable)} artist(s) unreachable -> {sorted(unreachable)}. "
            f"Every pair must be solvable; regenerate seed_data.py."
        )


async def seed(db=None):
    """Populate the database. Accepts an optional db handle (reused by the API);
    builds its own client when run standalone."""
    own_client = None
    if db is None:
        mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
        own_client = AsyncIOMotorClient(mongo_url)
        db = own_client[os.environ.get('DB_NAME', 'connect_the_notes')]

    try:
        # ── 0. Verify connectivity invariant BEFORE touching the DB ──
        artist_ids = [a[0] for a in ARTISTS]
        edges = [(c[0], c[1]) for c in COLLABORATIONS]
        _assert_single_component(artist_ids, edges)

        print("🔥 Dropping existing collections...")
        await db.artists.drop()
        await db.artistConnections.drop()

        # ── 1. Insert artists (real uuid ids, deterministic avatar via frontend) ──
        id_map = {}
        artist_docs = []
        for temp_id, name, genre in ARTISTS:
            real_id = uid()
            id_map[temp_id] = real_id
            artist_docs.append({
                "id": real_id,
                "name": name,
                "genre": genre,
                # Left empty on purpose: the frontend renders a deterministic,
                # styled initials avatar (utils/avatars.js) when imageUrl is blank.
                # Real artist photos can be backfilled here later.
                "imageUrl": "",
            })

        print(f"✅ Inserting {len(artist_docs)} artists...")
        await db.artists.insert_many(artist_docs)

        # ── 2. Build song-based connections (dedup parallel duplicates) ──
        connection_docs = []
        seen = set()
        for a1, a2, title, ctype, year in COLLABORATIONS:
            if a1 not in id_map or a2 not in id_map or a1 == a2:
                continue
            key = (min(a1, a2), max(a1, a2), title)
            if key in seen:
                continue
            seen.add(key)
            connection_docs.append({
                "id": uid(),
                "artist1": id_map[a1],
                "artist2": id_map[a2],
                "song": {
                    "title": title,
                    "type": ctype,
                    "year": year,
                    "coverUrl": "",
                },
            })

        print(f"✅ Inserting {len(connection_docs)} connections (song-based)...")
        await db.artistConnections.insert_many(connection_docs)

        # ── 3. Indexes ──
        await ensure_indexes(db)

        print("\n🎉 Seed complete!")
        print(f"  Artists: {len(artist_docs)}")
        print(f"  Connections: {len(connection_docs)}")
        print("  Invariant: single connected component → 100% of pairs solvable")
        return {"artists": len(artist_docs), "connections": len(connection_docs)}
    finally:
        if own_client is not None:
            own_client.close()


async def ensure_indexes(db):
    """Idempotent; safe to call on every app startup."""
    await db.artists.create_index("id", unique=True)
    await db.artists.create_index([("name", "text")])
    await db.artistConnections.create_index("id", unique=True)
    await db.artistConnections.create_index("artist1")
    await db.artistConnections.create_index("artist2")
    await db.artistConnections.create_index([("artist1", 1), ("artist2", 1)])


if __name__ == "__main__":
    asyncio.run(seed())
