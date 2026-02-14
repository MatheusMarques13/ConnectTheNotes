from fastapi import FastAPI, APIRouter, Query, HTTPException, Request, Response
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
import httpx
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List, Optional
import uuid
import random
from datetime import datetime, timezone, timedelta
from collections import deque

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ.get('DB_NAME', 'connect_the_notes')]

app = FastAPI()
api_router = APIRouter(prefix="/api")

# ── Models ──────────────────────────────────────────────

class Artist(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    genre: str
    imageUrl: str = ""

class ArtistCreate(BaseModel):
    name: str
    genre: str
    imageUrl: str = ""

class Collaboration(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    artistIds: List[str]
    title: str
    type: str  # song, album, live, feature
    year: int

class CollaborationCreate(BaseModel):
    artistIds: List[str]
    title: str
    type: str
    year: int

class PathStep(BaseModel):
    collab: dict
    fromArtist: str
    toArtist: str

class FindPathRequest(BaseModel):
    startId: str
    endId: str

class User(BaseModel):
    user_id: str
    email: str
    name: str
    picture: Optional[str] = None
    created_at: datetime

class GameResultSubmit(BaseModel):
    artist1_name: str
    artist2_name: str
    steps: int
    time_seconds: Optional[int] = None
    difficulty: Optional[str] = None
    timed_mode: bool = False
    won: bool = True

class GameResult(BaseModel):
    result_id: str
    user_id: str
    user_name: str
    user_picture: Optional[str] = None
    artist1_name: str
    artist2_name: str
    steps: int
    time_seconds: Optional[int] = None
    difficulty: Optional[str] = None
    timed_mode: bool = False
    won: bool = True
    created_at: datetime

# ── Auth Helper ──────────────────────────────────────────

async def get_current_user(request: Request) -> Optional[dict]:
    """Get current user from session token in cookie or Authorization header"""
    # Check cookie first
    session_token = request.cookies.get("session_token")
    
    # Fallback to Authorization header
    if not session_token:
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            session_token = auth_header.split(" ")[1]
    
    if not session_token:
        return None
    
    # Find session in database
    session_doc = await db.user_sessions.find_one(
        {"session_token": session_token},
        {"_id": 0}
    )
    
    if not session_doc:
        return None
    
    # Check expiry with timezone awareness
    expires_at = session_doc.get("expires_at")
    if isinstance(expires_at, str):
        expires_at = datetime.fromisoformat(expires_at)
    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=timezone.utc)
    if expires_at < datetime.now(timezone.utc):
        return None
    
    # Get user data
    user_doc = await db.users.find_one(
        {"user_id": session_doc["user_id"]},
        {"_id": 0}
    )
    
    return user_doc

async def require_auth(request: Request) -> dict:
    """Require authentication - raises 401 if not authenticated"""
    user = await get_current_user(request)
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return user

# ── Auth Routes ──────────────────────────────────────────

@api_router.post("/auth/session")
async def create_session(request: Request, response: Response):
    """Exchange session_id for session_token and user data"""
    body = await request.json()
    session_id = body.get("session_id")
    
    if not session_id:
        raise HTTPException(status_code=400, detail="session_id required")
    
    # Call Emergent Auth to get user data
    # REMINDER: DO NOT HARDCODE THE URL, OR ADD ANY FALLBACKS OR REDIRECT URLS, THIS BREAKS THE AUTH
    async with httpx.AsyncClient() as client_http:
        try:
            resp = await client_http.get(
                "https://demobackend.emergentagent.com/auth/v1/env/oauth/session-data",
                headers={"X-Session-ID": session_id},
                timeout=10.0
            )
            if resp.status_code != 200:
                raise HTTPException(status_code=401, detail="Invalid session_id")
            auth_data = resp.json()
        except httpx.RequestError as e:
            raise HTTPException(status_code=500, detail=f"Auth service error: {str(e)}")
    
    user_email = auth_data.get("email")
    user_name = auth_data.get("name")
    user_picture = auth_data.get("picture")
    emergent_session_token = auth_data.get("session_token")
    
    # Check if user exists
    existing_user = await db.users.find_one({"email": user_email}, {"_id": 0})
    
    if existing_user:
        user_id = existing_user["user_id"]
        # Update user data if changed
        await db.users.update_one(
            {"user_id": user_id},
            {"$set": {"name": user_name, "picture": user_picture}}
        )
    else:
        # Create new user
        user_id = f"user_{uuid.uuid4().hex[:12]}"
        await db.users.insert_one({
            "user_id": user_id,
            "email": user_email,
            "name": user_name,
            "picture": user_picture,
            "created_at": datetime.now(timezone.utc),
            "stats": {
                "games_played": 0,
                "games_won": 0,
                "games_lost": 0,
                "best_steps": None,
                "best_time": None
            }
        })
    
    # Create session
    session_token = f"sess_{uuid.uuid4().hex}"
    expires_at = datetime.now(timezone.utc) + timedelta(days=7)
    
    await db.user_sessions.insert_one({
        "user_id": user_id,
        "session_token": session_token,
        "expires_at": expires_at,
        "created_at": datetime.now(timezone.utc)
    })
    
    # Set httpOnly cookie
    response.set_cookie(
        key="session_token",
        value=session_token,
        httponly=True,
        secure=True,
        samesite="none",
        path="/",
        max_age=7 * 24 * 60 * 60  # 7 days
    )
    
    # Get updated user
    user_doc = await db.users.find_one({"user_id": user_id}, {"_id": 0})
    
    return {
        "user": user_doc,
        "session_token": session_token
    }

@api_router.get("/auth/me")
async def get_me(request: Request):
    """Get current authenticated user"""
    user = await get_current_user(request)
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return user

@api_router.post("/auth/logout")
async def logout(request: Request, response: Response):
    """Logout user - clear session"""
    session_token = request.cookies.get("session_token")
    
    if session_token:
        await db.user_sessions.delete_one({"session_token": session_token})
    
    response.delete_cookie(
        key="session_token",
        path="/",
        secure=True,
        samesite="none"
    )
    
    return {"message": "Logged out successfully"}

# ── Game Results & Leaderboard Routes ──────────────────────

@api_router.post("/game/submit-result")
async def submit_game_result(result: GameResultSubmit, request: Request):
    """Submit a game result (requires auth)"""
    user = await require_auth(request)
    
    # Create game result
    result_id = f"result_{uuid.uuid4().hex[:12]}"
    game_result = {
        "result_id": result_id,
        "user_id": user["user_id"],
        "user_name": user["name"],
        "user_picture": user.get("picture"),
        "artist1_name": result.artist1_name,
        "artist2_name": result.artist2_name,
        "steps": result.steps,
        "time_seconds": result.time_seconds,
        "difficulty": result.difficulty,
        "timed_mode": result.timed_mode,
        "won": result.won,
        "created_at": datetime.now(timezone.utc)
    }
    
    await db.game_results.insert_one(game_result)
    
    # Update user stats
    stats_update = {"$inc": {"stats.games_played": 1}}
    if result.won:
        stats_update["$inc"]["stats.games_won"] = 1
        # Update best steps
        if user.get("stats", {}).get("best_steps") is None or result.steps < user["stats"]["best_steps"]:
            stats_update["$set"] = {"stats.best_steps": result.steps}
        # Update best time (only for timed mode wins)
        if result.timed_mode and result.time_seconds:
            current_best = user.get("stats", {}).get("best_time")
            if current_best is None or result.time_seconds < current_best:
                if "$set" not in stats_update:
                    stats_update["$set"] = {}
                stats_update["$set"]["stats.best_time"] = result.time_seconds
    else:
        stats_update["$inc"]["stats.games_lost"] = 1
    
    await db.users.update_one({"user_id": user["user_id"]}, stats_update)
    
    # Return updated user
    updated_user = await db.users.find_one({"user_id": user["user_id"]}, {"_id": 0})
    
    return {
        "result_id": result_id,
        "user": updated_user
    }

@api_router.get("/leaderboard")
async def get_leaderboard(
    period: str = Query(default="all", regex="^(daily|weekly|all)$"),
    sort_by: str = Query(default="steps", regex="^(steps|time|wins)$"),
    limit: int = Query(default=20, le=100)
):
    """Get leaderboard data"""
    # Calculate time filter
    now = datetime.now(timezone.utc)
    time_filter = {}
    
    if period == "daily":
        start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
        time_filter = {"created_at": {"$gte": start_of_day}}
    elif period == "weekly":
        start_of_week = now - timedelta(days=now.weekday())
        start_of_week = start_of_week.replace(hour=0, minute=0, second=0, microsecond=0)
        time_filter = {"created_at": {"$gte": start_of_week}}
    
    if sort_by == "wins":
        # Aggregate wins by user
        pipeline = [
            {"$match": {**time_filter, "won": True}},
            {"$group": {
                "_id": "$user_id",
                "user_name": {"$first": "$user_name"},
                "user_picture": {"$first": "$user_picture"},
                "wins": {"$sum": 1},
                "best_steps": {"$min": "$steps"},
                "best_time": {"$min": "$time_seconds"},
                "latest_game": {"$max": "$created_at"}
            }},
            {"$sort": {"wins": -1, "best_steps": 1}},
            {"$limit": limit},
            {"$project": {"_id": 0, "user_id": "$_id", "user_name": 1, "user_picture": 1, "wins": 1, "best_steps": 1, "best_time": 1}}
        ]
        results = await db.game_results.aggregate(pipeline).to_list(limit)
        return {"leaderboard": results, "sort_by": "wins", "period": period}
    
    elif sort_by == "steps":
        # Best single game by fewest steps
        pipeline = [
            {"$match": {**time_filter, "won": True}},
            {"$sort": {"steps": 1, "time_seconds": 1}},
            {"$group": {
                "_id": "$user_id",
                "user_name": {"$first": "$user_name"},
                "user_picture": {"$first": "$user_picture"},
                "best_steps": {"$first": "$steps"},
                "best_time": {"$first": "$time_seconds"},
                "artist1_name": {"$first": "$artist1_name"},
                "artist2_name": {"$first": "$artist2_name"}
            }},
            {"$sort": {"best_steps": 1}},
            {"$limit": limit},
            {"$project": {"_id": 0, "user_id": "$_id", "user_name": 1, "user_picture": 1, "best_steps": 1, "best_time": 1, "artist1_name": 1, "artist2_name": 1}}
        ]
        results = await db.game_results.aggregate(pipeline).to_list(limit)
        return {"leaderboard": results, "sort_by": "steps", "period": period}
    
    elif sort_by == "time":
        # Fastest timed games
        pipeline = [
            {"$match": {**time_filter, "won": True, "timed_mode": True, "time_seconds": {"$exists": True, "$ne": None}}},
            {"$sort": {"time_seconds": 1}},
            {"$group": {
                "_id": "$user_id",
                "user_name": {"$first": "$user_name"},
                "user_picture": {"$first": "$user_picture"},
                "best_time": {"$first": "$time_seconds"},
                "best_steps": {"$first": "$steps"},
                "difficulty": {"$first": "$difficulty"},
                "artist1_name": {"$first": "$artist1_name"},
                "artist2_name": {"$first": "$artist2_name"}
            }},
            {"$sort": {"best_time": 1}},
            {"$limit": limit},
            {"$project": {"_id": 0, "user_id": "$_id", "user_name": 1, "user_picture": 1, "best_time": 1, "best_steps": 1, "difficulty": 1, "artist1_name": 1, "artist2_name": 1}}
        ]
        results = await db.game_results.aggregate(pipeline).to_list(limit)
        return {"leaderboard": results, "sort_by": "time", "period": period}

@api_router.get("/leaderboard/user/{user_id}")
async def get_user_rank(user_id: str, period: str = Query(default="all", regex="^(daily|weekly|all)$")):
    """Get a specific user's rank and stats"""
    # Calculate time filter
    now = datetime.now(timezone.utc)
    time_filter = {}
    
    if period == "daily":
        start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
        time_filter = {"created_at": {"$gte": start_of_day}}
    elif period == "weekly":
        start_of_week = now - timedelta(days=now.weekday())
        start_of_week = start_of_week.replace(hour=0, minute=0, second=0, microsecond=0)
        time_filter = {"created_at": {"$gte": start_of_week}}
    
    # Get user's stats for the period
    user_results = await db.game_results.find(
        {"user_id": user_id, **time_filter},
        {"_id": 0}
    ).to_list(1000)
    
    wins = sum(1 for r in user_results if r.get("won"))
    games_played = len(user_results)
    best_steps = min((r["steps"] for r in user_results if r.get("won")), default=None)
    timed_results = [r for r in user_results if r.get("won") and r.get("timed_mode") and r.get("time_seconds")]
    best_time = min((r["time_seconds"] for r in timed_results), default=None)
    
    # Get rank by wins
    pipeline = [
        {"$match": {**time_filter, "won": True}},
        {"$group": {"_id": "$user_id", "wins": {"$sum": 1}}},
        {"$sort": {"wins": -1}},
    ]
    all_users = await db.game_results.aggregate(pipeline).to_list(1000)
    
    rank = None
    for i, u in enumerate(all_users):
        if u["_id"] == user_id:
            rank = i + 1
            break
    
    return {
        "user_id": user_id,
        "period": period,
        "rank": rank,
        "wins": wins,
        "games_played": games_played,
        "best_steps": best_steps,
        "best_time": best_time
    }

@api_router.get("/user/{user_id}/history")
async def get_user_game_history(user_id: str, limit: int = Query(default=20, le=100)):
    """Get user's recent game history"""
    results = await db.game_results.find(
        {"user_id": user_id},
        {"_id": 0}
    ).sort("created_at", -1).limit(limit).to_list(limit)
    
    return {"history": results}

# ── Artist Routes ──────────────────────────────────────────────

@api_router.get("/")
async def root():
    return {"message": "Connect the Notes API"}

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

@api_router.get("/collaborations/between/{id1}/{id2}")
async def get_collaborations_between(id1: str, id2: str):
    collabs = await db.collaborations.find(
        {"artistIds": {"$all": [id1, id2]}},
        {"_id": 0}
    ).to_list(100)
    return {"collaborations": collabs}

@api_router.post("/game/find-path")
async def find_path(request: FindPathRequest):
    start_id = request.startId
    end_id = request.endId
    
    if start_id == end_id:
        return {"path": []}
    
    # BFS
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

@api_router.get("/stats")
async def get_stats():
    artist_count = await db.artists.count_documents({})
    collab_count = await db.collaborations.count_documents({})
    return {
        "totalArtists": artist_count,
        "totalCollaborations": collab_count
    }

# Include router
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
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
