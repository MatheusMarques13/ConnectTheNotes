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

app = FastAPI(title="Connect the Notes API", version="1.0.0")
api_router = APIRouter(prefix="/api")

# ── Models ──────────────────────────────────────────────

class FindPathRequest(BaseModel):
    startId: str
    endId: str

# ── Health & Root ──────────────────────────────────────────

@api_router.get("/")
async def root():
    return {"message": "Connect the Notes API", "version": "1.0.0"}

@api_router.get("/health")
async def health():
    try:
        await db.command("ping")
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return JSONResponse(status_code=503, content={"status": "unhealthy", "error": str(e)})

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

@api_router.get("/artists/{artist_id}/collaborations")
async def get_artist_collaborations(artist_id: str):
    collabs = await db.collaborations.find(
        {"artistIds": artist_id},
        {"_id": 0}
    ).to_list(500)
    return {"collaborations": collabs}

@api_router.get("/artists/{artist_id}/connected")
async def get_connected_artists(artist_id: str):
    collabs = await db.collaborations.find(
        {"artistIds": artist_id},
        {"_id": 0}
    ).to_list(500)
    
    connected_ids = set()
    for c in collabs:
        for aid in c["artistIds"]:
            if aid != artist_id:
                connected_ids.add(aid)
    
    if not connected_ids:
        return {"artists": []}
    
    artists = await db.artists.find(
        {"id": {"$in": list(connected_ids)}},
        {"_id": 0}
    ).to_list(200)
    return {"artists": artists}

# ── Collaboration Routes ──────────────────────────────────

@api_router.get("/collaborations/between/{id1}/{id2}")
async def get_collaborations_between(id1: str, id2: str):
    collabs = await db.collaborations.find(
        {"artistIds": {"$all": [id1, id2]}},
        {"_id": 0}
    ).to_list(100)
    return {"collaborations": collabs}

# ── Game Logic ──────────────────────────────────────────────

@api_router.post("/game/find-path")
async def find_path(request: FindPathRequest):
    start_id = request.startId
    end_id = request.endId
    
    if start_id == end_id:
        return {"path": []}
    
    visited = {start_id}
    queue = deque([(start_id, [])])
    
    while queue:
        current_id, path = queue.popleft()
        
        collabs = await db.collaborations.find(
            {"artistIds": current_id},
            {"_id": 0}
        ).to_list(500)
        
        for collab in collabs:
            for next_id in collab["artistIds"]:
                if next_id == current_id:
                    continue
                if next_id == end_id:
                    return {
                        "path": path + [{
                            "collab": collab,
                            "fromArtist": current_id,
                            "toArtist": next_id
                        }]
                    }
                if next_id not in visited:
                    visited.add(next_id)
                    queue.append((next_id, path + [{
                        "collab": collab,
                        "fromArtist": current_id,
                        "toArtist": next_id
                    }]))
    
    return {"path": None}

# ── Stats ──────────────────────────────────────────────────

@api_router.get("/stats")
async def get_stats():
    artist_count = await db.artists.count_documents({})
    collab_count = await db.collaborations.count_documents({})
    return {
        "totalArtists": artist_count,
        "totalCollaborations": collab_count
    }

# ── Setup ──────────────────────────────────────────────────

app.include_router(api_router)

# CORS - allow frontend origins
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
