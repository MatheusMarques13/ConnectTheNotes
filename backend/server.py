from fastapi import FastAPI, APIRouter, Query, HTTPException, Header
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
import hmac
import hashlib
import random
from pathlib import Path
from pydantic import BaseModel
from typing import Optional, List, Dict
from datetime import date as date_cls

from game_logic import (
    DIFFICULTY_BANDS,
    build_adjacency,
    bfs_steps,
    bfs_distances,
    build_path,
    pick_pair_in_band,
)

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

MONGO_URL = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
DB_NAME = os.environ.get('DB_NAME', 'connect_the_notes')

# ── Lazy, cached Mongo client (serverless-friendly) ────────────────
# Created on first use instead of at import time so a single warm Vercel
# instance reuses one connection pool across requests rather than opening a
# fresh pool on every cold start.
_client: Optional[AsyncIOMotorClient] = None


def get_db():
    global _client
    if _client is None:
        _client = AsyncIOMotorClient(
            MONGO_URL,
            maxPoolSize=5,
            serverSelectionTimeoutMS=5000,
        )
    return _client[DB_NAME]


# ── Models ──────────────────────────────────────────────

class FindPathRequest(BaseModel):
    startId: str
    endId: str


# ── Graph helpers (DB-bound; pure traversal lives in game_logic.py) ─

async def load_graph(db):
    """Fetch all connections once and build an in-memory adjacency map."""
    conns = await db.artistConnections.find({}, {"_id": 0}).to_list(None)
    return build_adjacency(conns)


async def hydrate_artists(db, ids: List[str]) -> Dict[str, dict]:
    docs = await db.artists.find({"id": {"$in": list(set(ids))}}, {"_id": 0}).to_list(None)
    return {d["id"]: d for d in docs}


# ── App lifespan: ensure indexes once on startup ───────────────────

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        from seed import ensure_indexes
        await ensure_indexes(get_db())
        logger.info("Indexes ensured on startup.")
    except Exception as e:  # never block startup on index creation
        logger.warning(f"Could not ensure indexes on startup: {e}")
    yield
    if _client is not None:
        _client.close()


app = FastAPI(title="Connect the Notes API", version="3.0.0", lifespan=lifespan)
api_router = APIRouter(prefix="/api")

# ── Health & Root ──────────────────────────────────────────

@api_router.get("/")
async def root():
    return {"message": "Connect the Notes API", "version": "3.0.0"}


@api_router.get("/health")
async def health():
    try:
        await get_db().command("ping")
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return JSONResponse(status_code=503, content={"status": "unhealthy", "error": str(e)})


# ── Protected admin seed (no public reset!) ────────────────────────

@api_router.post("/admin/seed")
async def run_seed(x_seed_token: Optional[str] = Header(default=None)):
    """Reseed the database. Requires the SEED_TOKEN env var and a matching
    X-Seed-Token header. Returns 403 otherwise. There is intentionally no
    public GET/reset endpoint anymore."""
    expected = os.environ.get("SEED_TOKEN")
    if not expected or not x_seed_token or not hmac.compare_digest(x_seed_token, expected):
        raise HTTPException(status_code=403, detail="Forbidden")
    try:
        from seed import seed
        result = await seed(get_db())
        return {"message": "✅ Seed complete", **result}
    except Exception as e:
        import traceback
        return JSONResponse(status_code=500, content={"error": str(e), "traceback": traceback.format_exc()})


# ── Auth / Leaderboard stubs (not yet implemented) ─────────────────

@api_router.get("/auth/me")
async def get_me():
    return JSONResponse(status_code=401, content={"detail": "Not authenticated"})


@api_router.get("/leaderboard")
async def get_leaderboard(period: str = Query(default="all"), sort_by: str = Query(default="wins"),
                          limit: int = Query(default=20, le=100)):
    return {"leaderboard": [], "sort_by": sort_by, "period": period}


# ── Artist Routes ──────────────────────────────────────────

@api_router.get("/artists")
async def get_artists(search: Optional[str] = None, limit: int = Query(default=10, le=50)):
    db = get_db()
    if search and len(search) >= 1:
        cursor = db.artists.find({"name": {"$regex": search, "$options": "i"}}, {"_id": 0}).limit(limit)
    else:
        cursor = db.artists.find({}, {"_id": 0}).limit(limit)
    artists = await cursor.to_list(limit)
    return {"artists": artists}


@api_router.get("/artists/random")
async def get_random_artist(excludeIds: Optional[str] = None):
    db = get_db()
    pipeline = []
    if excludeIds:
        exclude_list = [e.strip() for e in excludeIds.split(",") if e.strip()]
        if exclude_list:
            pipeline.append({"$match": {"id": {"$nin": exclude_list}}})
    pipeline.append({"$sample": {"size": 1}})
    pipeline.append({"$project": {"_id": 0}})
    results = await db.artists.aggregate(pipeline).to_list(1)
    if not results:
        raise HTTPException(status_code=404, detail="No artists available")
    return {"artist": results[0]}


@api_router.get("/artists/{artist_id}")
async def get_artist(artist_id: str):
    artist = await get_db().artists.find_one({"id": artist_id}, {"_id": 0})
    if not artist:
        raise HTTPException(status_code=404, detail="Artist not found")
    return artist


@api_router.get("/artists/{artist_id}/connections")
async def get_artist_connections(artist_id: str):
    connections = await get_db().artistConnections.find(
        {"$or": [{"artist1": artist_id}, {"artist2": artist_id}]}, {"_id": 0}
    ).to_list(500)
    return {"connections": connections}


@api_router.get("/artists/{artist_id}/connected")
async def get_connected_artists(artist_id: str):
    db = get_db()
    connections = await db.artistConnections.find(
        {"$or": [{"artist1": artist_id}, {"artist2": artist_id}]}, {"_id": 0}
    ).to_list(500)
    connected_ids = set()
    for conn in connections:
        other = conn["artist2"] if conn["artist1"] == artist_id else conn["artist1"]
        connected_ids.add(other)
    if not connected_ids:
        return {"artists": []}
    artists = await db.artists.find({"id": {"$in": list(connected_ids)}}, {"_id": 0}).to_list(200)
    return {"artists": artists}


# ── Connection Routes ──────────────────────────────────────

@api_router.get("/connections/between/{id1}/{id2}")
async def get_connections_between(id1: str, id2: str):
    connections = await get_db().artistConnections.find(
        {"$or": [{"artist1": id1, "artist2": id2}, {"artist1": id2, "artist2": id1}]}, {"_id": 0}
    ).to_list(100)
    return {"connections": connections}


# ── Game Logic ─────────────────────────────────────────────

@api_router.post("/game/find-path")
async def find_path(request: FindPathRequest):
    """Shortest path between two artists via shared songs.
    Path is a list of alternating {kind:'artist'} / {kind:'song'} nodes."""
    db = get_db()
    if request.startId == request.endId:
        return {"path": []}
    adj = await load_graph(db)
    steps = bfs_steps(adj, request.startId, request.endId)
    if steps is None:
        return {"path": None}
    ids = [request.startId] + [s[2] for s in steps]
    artists = await hydrate_artists(db, ids)
    return {"path": build_path(request.startId, steps, artists), "optimalSteps": len(steps)}


@api_router.get("/game/random-pair")
async def random_pair(difficulty: str = Query(default="any")):
    """Return two artists guaranteed to be connected, with their optimal
    step count, optionally constrained to a difficulty (graph-distance) band."""
    db = get_db()
    adj = await load_graph(db)
    lo, hi = DIFFICULTY_BANDS.get(difficulty, DIFFICULTY_BANDS["any"])
    picked = pick_pair_in_band(adj, random.Random(), lo, hi)
    if not picked:
        raise HTTPException(status_code=503, detail="Graph not seeded")
    start, end, dist = picked
    artists = await hydrate_artists(db, [start, end])
    return {"artist1": artists.get(start), "artist2": artists.get(end), "optimalSteps": dist}


@api_router.get("/game/daily")
async def daily_puzzle(date: Optional[str] = Query(default=None)):
    """A deterministic, always-solvable puzzle for the given date (defaults to
    today). Everyone playing on the same date gets the same pair."""
    db = get_db()
    day = date or date_cls.today().isoformat()
    adj = await load_graph(db)
    if not adj:
        raise HTTPException(status_code=503, detail="Graph not seeded")
    seed_int = int(hashlib.sha256(day.encode()).hexdigest(), 16) % (2 ** 32)
    rng = random.Random(seed_int)
    lo, hi = DIFFICULTY_BANDS["medium"]
    picked = pick_pair_in_band(adj, rng, lo, hi)
    start, end, dist = picked
    artists = await hydrate_artists(db, [start, end])
    return {
        "date": day,
        "artist1": artists.get(start),
        "artist2": artists.get(end),
        "optimalSteps": dist,
    }


# ── Stats ──────────────────────────────────────────────────

@api_router.get("/stats")
async def get_stats():
    db = get_db()
    artist_count = await db.artists.count_documents({})
    connection_count = await db.artistConnections.count_documents({})
    return {"totalArtists": artist_count, "totalConnections": connection_count, "mode": "song-based"}


# ── Setup ──────────────────────────────────────────────────

app.include_router(api_router)

# CORS: with credentials, the wildcard origin is invalid, so only enable
# credentials when explicit origins are configured.
allowed_origins = [o.strip() for o in os.environ.get('ALLOWED_ORIGINS', '*').split(',') if o.strip()]
allow_credentials = allowed_origins != ['*']

app.add_middleware(
    CORSMiddleware,
    allow_credentials=allow_credentials,
    allow_origins=allowed_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)
