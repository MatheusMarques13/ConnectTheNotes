"""Connect the Notes API — fully in-memory, no database required.

The dataset is a small static read-only graph (see store.py / seed_data.py), so
every request is answered from memory. This makes the app dependency-light and
deployable to serverless with zero configuration.
"""
from fastapi import FastAPI, APIRouter, Query, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from datetime import date as date_cls
import os
import random
import hashlib

import store
from game_logic import (
    DIFFICULTY_BANDS,
    bfs_steps,
    bfs_distances,
    build_path,
    pick_pair_in_band,
)


class FindPathRequest(BaseModel):
    startId: str
    endId: str


app = FastAPI(title="Connect the Notes API", version="3.1.0")
api_router = APIRouter(prefix="/api")


# ── Health & Root ──────────────────────────────────────────

@api_router.get("/")
async def root():
    return {"message": "Connect the Notes API", "version": "3.1.0"}


@api_router.get("/health")
async def health():
    s = store.stats()
    return {"status": "healthy", **s}


# ── Artist Routes ──────────────────────────────────────────

@api_router.get("/artists")
async def get_artists(search: Optional[str] = None, limit: int = Query(default=10, le=50)):
    return {"artists": store.search_artists(search, limit)}


@api_router.get("/artists/random")
async def get_random_artist(excludeIds: Optional[str] = None):
    exclude = [e.strip() for e in excludeIds.split(",")] if excludeIds else []
    artist = store.random_artist(exclude_ids=set(exclude))
    if not artist:
        raise HTTPException(status_code=404, detail="No artists available")
    return {"artist": artist}


@api_router.get("/artists/{artist_id}")
async def get_artist(artist_id: str):
    artist = store.get_artist(artist_id)
    if not artist:
        raise HTTPException(status_code=404, detail="Artist not found")
    return artist


@api_router.get("/artists/{artist_id}/connections")
async def get_artist_connections(artist_id: str):
    return {"connections": store.connections_for(artist_id)}


@api_router.get("/artists/{artist_id}/connected")
async def get_connected_artists(artist_id: str):
    return {"artists": store.connected_artists(artist_id)}


# ── Connection Routes ──────────────────────────────────────

@api_router.get("/connections/between/{id1}/{id2}")
async def get_connections_between(id1: str, id2: str):
    return {"connections": store.connections_between(id1, id2)}


# ── Game Logic ─────────────────────────────────────────────

@api_router.post("/game/find-path")
async def find_path(request: FindPathRequest):
    """Shortest path between two artists via shared songs.
    Path is a list of alternating {kind:'artist'} / {kind:'song'} nodes."""
    if request.startId == request.endId:
        return {"path": [], "optimalSteps": 0}
    steps = bfs_steps(store.ADJACENCY, request.startId, request.endId)
    if steps is None:
        return {"path": None, "optimalSteps": None}
    ids = [request.startId] + [s[2] for s in steps]
    artists = store.get_artists(ids)
    return {"path": build_path(request.startId, steps, artists), "optimalSteps": len(steps)}


@api_router.get("/game/random-pair")
async def random_pair(difficulty: str = Query(default="any")):
    """Two artists guaranteed connected, within a difficulty (distance) band."""
    lo, hi = DIFFICULTY_BANDS.get(difficulty, DIFFICULTY_BANDS["any"])
    picked = pick_pair_in_band(store.ADJACENCY, random.Random(), lo, hi)
    if not picked:
        raise HTTPException(status_code=503, detail="No data")
    start, end, dist = picked
    artists = store.get_artists([start, end])
    return {"artist1": artists.get(start), "artist2": artists.get(end), "optimalSteps": dist}


@api_router.get("/game/daily")
async def daily_puzzle(date: Optional[str] = Query(default=None)):
    """Deterministic, always-solvable puzzle for the given date (default today)."""
    day = date or date_cls.today().isoformat()
    seed_int = int(hashlib.sha256(day.encode()).hexdigest(), 16) % (2 ** 32)
    lo, hi = DIFFICULTY_BANDS["medium"]
    picked = pick_pair_in_band(store.ADJACENCY, random.Random(seed_int), lo, hi)
    if not picked:
        raise HTTPException(status_code=503, detail="No data")
    start, end, dist = picked
    artists = store.get_artists([start, end])
    return {"date": day, "artist1": artists.get(start), "artist2": artists.get(end), "optimalSteps": dist}


# ── Stats ──────────────────────────────────────────────────

@api_router.get("/stats")
async def get_stats():
    return {**store.stats(), "mode": "song-based"}


# ── Setup ──────────────────────────────────────────────────

app.include_router(api_router)

allowed_origins = [o.strip() for o in os.environ.get('ALLOWED_ORIGINS', '*').split(',') if o.strip()]
allow_credentials = allowed_origins != ['*']

app.add_middleware(
    CORSMiddleware,
    allow_credentials=allow_credentials,
    allow_origins=allowed_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)
