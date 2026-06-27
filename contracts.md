# Connect the Notes — API Contract

The active backend is **`backend/server.py`** (FastAPI). All routes are prefixed
with `/api`. There is **no database**: data is served in memory from
`backend/store.py` (built from `seed_data.py`). Shapes:

- artist — `{ id, name, genre, imageUrl }`
- connection — `{ id, artist1, artist2, song: { title, type, year, coverUrl } }`

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
- `GET /api/health` → `{ status, totalArtists, totalConnections }`

## Notes

- Shortest paths are computed by BFS over the in-memory graph
  (`backend/game_logic.py` + `backend/store.py`).
- The dataset (`backend/seed_data.py`) is filtered to a single connected
  component, so **every artist pair is solvable**.
