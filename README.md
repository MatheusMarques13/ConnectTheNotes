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
There is **no backend and no database**, so it deploys as a plain static site.

```
frontend/        the React app (this is the whole product)
  src/data/dataset.js     generated graph (do not edit by hand)
  src/services/api.js     client-side engine (BFS, daily, difficulty)
data/            data source + build tool (Python, optional — only to edit data)
  source_data.py          human-editable artists & collaborations
  build.py                regenerates dataset.js + asserts it's solvable
```

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

## Editing the artist data (optional, Python)

Edit `data/source_data.py`, then regenerate and validate the shipped dataset:

```bash
python data/build.py   # rewrites frontend/src/data/dataset.js;
                       # fails loudly if any artist pair becomes unsolvable
```
