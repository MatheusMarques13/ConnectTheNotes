# Connect the Notes 🎵

A musical "six degrees" puzzle: connect two artists through a chain of shared
songs. Inspired by *Connect the Stars*, but for music.

> Drake → *“Forever”* → Eminem → *“River”* → Ed Sheeran

Every puzzle is **guaranteed solvable** — the artist database is filtered to a
single connected component, so there is always a path between any two artists.

## Game modes

- **Daily Puzzle** — one curated, always-solvable pair per day (same for
  everyone), with a streak counter.
- **Free Play** — pick any two artists, or hit **Surprise Me** for a random
  solvable matchup. Difficulty is set by graph distance (number of hops).
- Win screen shows your steps vs. the **optimal (par)** and a shareable result.
- **Give up** reveals the optimal solution at any time.

## Tech stack

- **Frontend:** React (Create React App via CRACO), Tailwind, lucide-react.
- **Backend:** FastAPI + MongoDB (Motor). Shortest-path via in-memory BFS.
- **Deploy:** Vercel (frontend static build + Python serverless backend).

## Project layout

```
backend/
  server.py        # FastAPI app (the ONLY active backend)
  game_logic.py    # pure graph logic (BFS, difficulty bands) — unit-tested
  seed_data.py     # canonical dataset (95 artists, single connected component)
  seed.py          # loads seed_data into MongoDB; asserts connectivity
  tests/           # pytest-style tests, no DB required
frontend/
  src/             # React app
scripts/
  gen_seed_data.py # regenerates seed_data.py from the source dataset
```

## Local development

### Backend

```bash
cd backend
pip install -r requirements.txt
cp .env.example .env          # then edit MONGO_URL / DB_NAME / SEED_TOKEN
python seed.py                # one-time: populate the database
uvicorn server:app --reload --port 8001
```

### Frontend

```bash
cd frontend
yarn install
# REACT_APP_BACKEND_URL='' uses same-origin /api; set it for a split deploy
yarn start
```

## Environment variables

| Var | Where | Purpose |
|-----|-------|---------|
| `MONGO_URL` | backend | MongoDB connection string |
| `DB_NAME` | backend | database name (default `connect_the_notes`) |
| `ALLOWED_ORIGINS` | backend | comma-separated CORS origins (pin in prod) |
| `SEED_TOKEN` | backend | secret required to call `POST /api/admin/seed` |
| `REACT_APP_BACKEND_URL` | frontend | backend origin; empty = same-origin |

## Seeding in production

There is **no public seed/reset endpoint**. To (re)seed a deployed database,
either run `python seed.py` against the production `MONGO_URL`, or call the
protected endpoint:

```bash
curl -X POST https://<your-api>/api/admin/seed -H "X-Seed-Token: $SEED_TOKEN"
```

## Tests

```bash
python backend/tests/test_game_logic.py     # dataset + graph logic (no DB)
```

The suite verifies the core invariant: the dataset is a single connected
component and **every artist pair is solvable**.
