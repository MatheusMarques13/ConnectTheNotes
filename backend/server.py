from fastapi import FastAPI, APIRouter, Query, HTTPException
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List, Optional
import uuid
import random
from collections import deque

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ.get('DB_NAME', 'connect_the_notes')]

app = FastAPI(title="Connect the Notes API", version="2.0.1")
api_router = APIRouter(prefix="/api")

# ── Models ──────────────────────────────────────────────

class FindPathRequest(BaseModel):
    startId: str
    endId: str

# ── Health & Root ──────────────────────────────────────────

@api_router.get("/")
async def root():
    return {"message": "Connect the Notes API - Song Mode", "version": "2.0.1"}

@api_router.get("/health")
async def health():
    try:
        await db.command("ping")
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return JSONResponse(status_code=503, content={"status": "unhealthy", "error": str(e)})

# ── SEED & RESET ENDPOINTS ──

@api_router.get("/seed")
async def run_seed():
    """Open this URL in any browser to seed the database."""
    try:
        from seed import seed
        await seed()
        artist_count = await db.artists.count_documents({})
        connection_count = await db.artistConnections.count_documents({})
        
        # Verify data
        sample_connection = await db.artistConnections.find_one({}, {"_id": 0})
        
        return {
            "message": "✅ Seed complete! Database populated with song-based connections.",
            "artists": artist_count,
            "connections": connection_count,
            "mode": "Artists connected by SHARED SONGS",
            "sample_connection": sample_connection
        }
    except Exception as e:
        import traceback
        return JSONResponse(status_code=500, content={
            "error": str(e),
            "traceback": traceback.format_exc()
        })

@api_router.get("/reset")
async def force_reset():
    """⚠️ DANGER: Drops ALL collections and reseeds. Use this if seed fails."""
    try:
        # Drop ALL collections
        collections = await db.list_collection_names()
        for coll in collections:
            await db.drop_collection(coll)
        
        # Run seed
        from seed import seed
        await seed()
        
        artist_count = await db.artists.count_documents({})
        connection_count = await db.artistConnections.count_documents({})
        sample_artist = await db.artists.find_one({}, {"_id": 0})
        sample_connection = await db.artistConnections.find_one({}, {"_id": 0})
        
        return {
            "message": "🔥 HARD RESET COMPLETE!",
            "artists": artist_count,
            "connections": connection_count,
            "collections_dropped": collections,
            "sample_artist": sample_artist,
            "sample_connection": sample_connection
        }
    except Exception as e:
        import traceback
        return JSONResponse(status_code=500, content={
            "error": str(e),
            "traceback": traceback.format_exc()
        })

# ── Auth Stubs (Coming Soon) ──────────────────────────────

@api_router.get("/auth/me")
async def get_me():
    return JSONResponse(status_code=401, content={"detail": "Auth coming soon"})

@api_router.post("/auth/session")
async def create_session():
    return JSONResponse(status_code=501, content={"detail": "Auth coming soon"})

@api_router.post("/auth/logout")
async def logout_stub():
    return {"message": "Logged out"}

# ── Game Results Stubs (Coming Soon) ──────────────────────

@api_router.post("/game/submit-result")
async def submit_game_result():
    return JSONResponse(status_code=401, content={"detail": "Login required - coming soon"})

@api_router.get("/leaderboard")
async def get_leaderboard(
    period: str = Query(default="all"),
    sort_by: str = Query(default="wins"),
    limit: int = Query(default=20, le=100)
):
    return {"leaderboard": [], "sort_by": sort_by, "period": period, "message": "Coming soon"}

@api_router.get("/leaderboard/user/{user_id}")
async def get_user_rank(user_id: str):
    return {"user_id": user_id, "rank": None, "message": "Coming soon"}

@api_router.get("/user/{user_id}/history")
async def get_user_history(user_id: str):
    return {"history": [], "message": "Coming soon"}

# ── Artist Routes ──────────────────────────────────────────

@api_router.get("/artists")
async def get_artists(search: Optional[str] = None, limit: int = Query(default=10, le=50)):
    if search and len(search) >= 1:
        cursor = db.artists.find(
            {"name": {"$regex": search, "$options": "i"}},
            {"_id": 0}
        ).limit(limit)
    else:
        cursor = db.artists.find({}, {"_id": 0}).limit(limit)
    artists = await cursor.to_list(limit)
    return {"artists": artists}

@api_router.get("/artists/random")
async def get_random_artist(excludeIds: Optional[str] = None):
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
    artist = await db.artists.find_one({"id": artist_id}, {"_id": 0})
    if not artist:
        raise HTTPException(status_code=404, detail="Artist not found")
    return artist

@api_router.get("/artists/{artist_id}/connections")
async def get_artist_connections(artist_id: str):
    """Get all songs that connect this artist to others"""
    connections = await db.artistConnections.find(
        {"$or": [{"artist1": artist_id}, {"artist2": artist_id}]},
        {"_id": 0}
    ).to_list(500)
    return {"connections": connections}

@api_router.get("/artists/{artist_id}/connected")
async def get_connected_artists(artist_id: str):
    """Get all artists directly connected via songs"""
    connections = await db.artistConnections.find(
        {"$or": [{"artist1": artist_id}, {"artist2": artist_id}]},
        {"_id": 0}
    ).to_list(500)
    
    connected_ids = set()
    for conn in connections:
        other_id = conn["artist2"] if conn["artist1"] == artist_id else conn["artist1"]
        connected_ids.add(other_id)
    
    if not connected_ids:
        return {"artists": []}
    
    artists = await db.artists.find(
        {"id": {"$in": list(connected_ids)}},
        {"_id": 0}
    ).to_list(200)
    return {"artists": artists}

# ── Connection Routes ──────────────────────────────────────

@api_router.get("/connections/between/{id1}/{id2}")
async def get_connections_between(id1: str, id2: str):
    """Get songs connecting two artists directly"""
    connections = await db.artistConnections.find(
        {"$or": [
            {"artist1": id1, "artist2": id2},
            {"artist1": id2, "artist2": id1}
        ]},
        {"_id": 0}
    ).to_list(100)
    return {"connections": connections}

# ── Game Logic (NEW: Song-based BFS) ──────────────────────────────────

@api_router.post("/game/find-path")
async def find_path(request: FindPathRequest):
    """
    NEW ALGORITHM: Find shortest path between artists via SHARED SONGS
    Path format: [Artist A, Song X, Artist B, Song Y, Artist C]
    """
    start_id = request.startId
    end_id = request.endId
    
    if start_id == end_id:
        return {"path": []}
    
    # Check if direct connection exists
    direct = await db.artistConnections.find_one(
        {"$or": [
            {"artist1": start_id, "artist2": end_id},
            {"artist1": end_id, "artist2": start_id}
        ]},
        {"_id": 0}
    )
    
    if direct:
        # Direct connection found!
        start_artist = await db.artists.find_one({"id": start_id}, {"_id": 0})
        end_artist = await db.artists.find_one({"id": end_id}, {"_id": 0})
        
        return {
            "path": [
                {"type": "artist", **start_artist},
                {"type": "song", **direct["song"]},
                {"type": "artist", **end_artist}
            ]
        }
    
    # BFS to find shortest path
    visited = {start_id}
    queue = deque([(start_id, [])])
    
    while queue:
        current_id, path = queue.popleft()
        
        # Find all songs connecting current artist to others
        connections = await db.artistConnections.find(
            {"$or": [{"artist1": current_id}, {"artist2": current_id}]},
            {"_id": 0}
        ).to_list(500)
        
        for conn in connections:
            # Determine the next artist
            next_id = conn["artist2"] if conn["artist1"] == current_id else conn["artist1"]
            
            if next_id == end_id:
                # Found the target!
                full_path = []
                
                # Start artist
                start_artist = await db.artists.find_one({"id": start_id}, {"_id": 0})
                full_path.append({"type": "artist", **start_artist})
                
                # Add intermediate steps
                for step in path:
                    full_path.append({"type": "song", **step["song"]})
                    artist = await db.artists.find_one({"id": step["toArtist"]}, {"_id": 0})
                    full_path.append({"type": "artist", **artist})
                
                # Add final song and end artist
                full_path.append({"type": "song", **conn["song"]})
                end_artist = await db.artists.find_one({"id": end_id}, {"_id": 0})
                full_path.append({"type": "artist", **end_artist})
                
                return {"path": full_path}
            
            if next_id not in visited:
                visited.add(next_id)
                queue.append((next_id, path + [{
                    "song": conn["song"],
                    "fromArtist": current_id,
                    "toArtist": next_id
                }]))
    
    # No path found
    return {"path": None}

# ── Stats ──────────────────────────────────────────────────

@api_router.get("/stats")
async def get_stats():
    artist_count = await db.artists.count_documents({})
    connection_count = await db.artistConnections.count_documents({})
    return {
        "totalArtists": artist_count,
        "totalConnections": connection_count,
        "mode": "song-based"
    }

# ── Setup ──────────────────────────────────────────────────

app.include_router(api_router)

# CORS
allowed_origins = os.environ.get('ALLOWED_ORIGINS', '*').split(',')

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=allowed_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
