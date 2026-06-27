# Connect the Notes — API Contract

The active backend is **`backend/server.py`** (FastAPI). All routes are prefixed
with `/api`. Data lives in two MongoDB collections:

- `artists` — `{ id, name, genre, imageUrl }`
- `artistConnections` — `{ id, artist1, artist2, song: { title, type, year, coverUrl } }`

`type` is one of `song | album | live | feature`.

## Artists

- `GET /api/artists?search=<q>&limit=10` → `{ artists: [...] }`
- `GET /api/artists/random?excludeIds=a,b` → `{ artist }`
- `GET /api/artists/:id` → artist object
- `GET /api/artists/:id/connections` → `{ connections: [...] }`
- `GET /api/artists/:id/connected` → `{ artists: [...] }`
- `GET /api/connections/between/:id1/:id2` → `{ connections: [...] }`

## Game

- `POST /api/game/find-path` — body `{ startId, endId }` →
  `{ path: [ {kind:'artist', artist}, {kind:'song', song}, ... ] | null, optimalSteps }`.
  `path === null` means unreachable (cannot happen within the seeded dataset,
  which is a single connected component). The structural marker is `kind`, so a
  song's own `type` (`album`/`live`/…) is never overwritten.
- `GET /api/game/random-pair?difficulty=easy|medium|hard|any` →
  `{ artist1, artist2, optimalSteps }` — guaranteed connected, distance within
  the difficulty band.
- `GET /api/game/daily?date=YYYY-MM-DD` →
  `{ date, artist1, artist2, optimalSteps }` — deterministic per date.

## Stats & ops

- `GET /api/stats` → `{ totalArtists, totalConnections, mode }`
- `GET /api/health` → `{ status, database }`
- `POST /api/admin/seed` (requires `X-Seed-Token`) → reseeds the database.
  There is intentionally **no public seed/reset endpoint**.

## Notes

- Shortest paths are computed by an in-memory BFS (`backend/game_logic.py`): the
  whole graph is loaded once per request, then traversed in memory.
- The dataset (`backend/seed_data.py`) is filtered to a single connected
  component, so **every artist pair is solvable**. `seed.py` re-asserts this
  invariant before inserting.
