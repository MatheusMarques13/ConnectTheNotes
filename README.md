# Connect the Notes 🎵

A musical "six degrees" puzzle: connect two artists through a chain of shared
songs. Inspired by *Connect the Stars*, but for music.

> Drake → *“Forever”* → Eminem → *“River”* → Ed Sheeran

Every puzzle is **guaranteed solvable** — the artist dataset is a single
connected component, so there is always a path between any two artists.

## Game modes

- **Daily Puzzle** — one curated, always-solvable pair per day (same for
  everyone), with a streak counter.
- **Free Play** — pick any two artists, or hit **Surprise Me** for a random
  solvable matchup. Difficulty is set by graph distance (number of hops).
- Win screen shows your steps vs. the **optimal (par)** and a shareable result.
- **Give up** reveals the optimal solution at any time.

## Tech stack

- **Frontend:** React (Create React App via CRACO), Tailwind, lucide-react.
- **Backend:** FastAPI. The dataset is a small static read-only graph served
  **entirely in memory — no database required.** Shortest paths via BFS.
- **Deploy:** Vercel (frontend static build + Python serverless backend).

## Project layout

```
backend/
  server.py        # FastAPI app (all endpoints)
  store.py         # in-memory data store, built from seed_data.py
  game_logic.py    # pure graph logic (BFS, difficulty bands) — unit-tested
  seed_data.py     # canonical dataset (95 artists, single connected component)
  tests/           # pytest-style tests, no DB required
frontend/
  src/             # React app
scripts/
  smoke_test.py    # end-to-end backend test (no DB)
  gen_seed_data.py # regenerates seed_data.py from the source dataset
```

## Run it locally

### Backend (no database!)

```bash
cd backend
pip install -r requirements.txt
uvicorn server:app --reload --port 8001
```

That's it — the data loads in memory at startup.

### Frontend

```bash
cd frontend
echo "REACT_APP_BACKEND_URL=http://localhost:8001" >> .env   # dev is cross-origin
yarn install        # if you hit a node-engine error: yarn install --ignore-engines
yarn start          # opens http://localhost:3000
```

## Quick checks (no UI)

```bash
python backend/tests/test_game_logic.py   # dataset + graph logic
python scripts/smoke_test.py              # full backend e2e + simulated playthrough
```

Both verify the core invariant: the dataset is a single connected component and
**every artist pair is solvable**.

## Environment variables

| Var | Where | Purpose |
|-----|-------|---------|
| `ALLOWED_ORIGINS` | backend | comma-separated CORS origins (pin in prod) |
| `REACT_APP_BACKEND_URL` | frontend | backend origin; empty = same-origin |

## Updating the dataset

Edit the source data and regenerate:

```bash
python scripts/gen_seed_data.py   # rewrites backend/seed_data.py, keeping only
                                  # the largest connected component (100% solvable)
```
