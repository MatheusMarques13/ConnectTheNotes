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

## Architecture

The entire game runs **client-side** — the dataset and the BFS pathfinding live
in the browser (`frontend/src/data/dataset.js` + `frontend/src/services/api.js`).
There is **no backend and no database at runtime**, so it deploys as a plain
static site.

The `backend/` folder is optional tooling: the canonical dataset
(`seed_data.py`), the pure graph logic, and Python tests that prove the
"every pair is solvable" invariant. `scripts/gen_dataset_js.py` regenerates the
browser dataset from it.

## Run it locally

```bash
cd frontend
yarn install        # if you hit a node-engine error: yarn install --ignore-engines
yarn start          # opens http://localhost:3000 — that's it, no backend needed
```

## Deploy

Push to your default branch — Vercel builds the static React app
(`frontend/`). No environment variables, database, or serverless functions
required.

## Tests / data tooling (optional, Python)

```bash
python backend/tests/test_game_logic.py   # proves the dataset is one component
python scripts/gen_dataset_js.py          # regenerate frontend/src/data/dataset.js
python scripts/gen_seed_data.py           # regenerate backend/seed_data.py from source
```
