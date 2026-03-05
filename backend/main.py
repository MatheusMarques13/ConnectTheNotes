from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from pathlib import Path
import httpx
import asyncio

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

app = FastAPI(title="Connect The Notes API")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MongoDB connection
mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ.get('DB_NAME', 'connect_the_notes')]

@app.get("/")
async def root():
    return {"message": "Connect The Notes API is running"}

@app.get("/api/artists")
async def get_artists(genre: str | None = None):
    """Get all artists, optionally filtered by genre"""
    query = {}
    if genre:
        query["genre"] = {"$regex": genre, "$options": "i"}
    
    artists = await db.artists.find(query, {"_id": 0}).to_list(1000)
    return {"artists": artists, "count": len(artists)}

@app.get("/api/artists/random")
async def get_random_artists(count: int = 9, genre: str | None = None):
    """Get random artists for the game"""
    match_stage = {}
    if genre:
        match_stage = {"genre": {"$regex": genre, "$options": "i"}}
    
    pipeline = [
        {"$match": match_stage} if match_stage else {"$match": {}},
        {"$sample": {"size": count}},
        {"$project": {"_id": 0}}
    ]
    
    artists = await db.artists.aggregate(pipeline).to_list(count)
    return {"artists": artists}

@app.get("/api/genres")
async def get_genres():
    """Get all unique genres"""
    genres = await db.artists.distinct("genre")
    return {"genres": sorted(genres)}

async def fetch_artist_image_from_deezer(artist_name: str) -> str | None:
    """Fetch artist image from Deezer API"""
    try:
        async with httpx.AsyncClient(timeout=10.0) as http_client:
            response = await http_client.get(
                'https://api.deezer.com/search/artist',
                params={'q': artist_name, 'limit': 1}
            )
            if response.status_code == 200:
                data = response.json()
                if data.get('data') and len(data['data']) > 0:
                    return data['data'][0].get('picture_medium')
    except Exception as e:
        print(f"Error fetching image for {artist_name}: {e}")
    return None

@app.post("/api/fetch-images")
async def fetch_images():
    """Populate all artists with real images from Deezer API"""
    artists = await db.artists.find({}, {'_id': 0, 'id': 1, 'name': 1, 'imageUrl': 1}).to_list(None)
    total = len(artists)
    updated = 0
    skipped = 0
    failed = 0
    
    results = []
    
    for i, artist in enumerate(artists, 1):
        # Skip if already has imageUrl
        if artist.get('imageUrl'):
            skipped += 1
            results.append(f"[{i}/{total}] ⏭️  {artist['name']} - already has image")
            continue
        
        results.append(f"[{i}/{total}] 🔍 Fetching {artist['name']}...")
        image_url = await fetch_artist_image_from_deezer(artist['name'])
        
        if image_url:
            await db.artists.update_one(
                {'id': artist['id']},
                {'$set': {'imageUrl': image_url}}
            )
            updated += 1
            results.append(f"[{i}/{total}] ✅ {artist['name']} - {image_url}")
        else:
            failed += 1
            results.append(f"[{i}/{total}] ❌ {artist['name']} - no image found")
        
        # Rate limit: 50 requests per second max (Deezer)
        await asyncio.sleep(0.1)
    
    summary = f"✨ Done! Updated: {updated}, Skipped: {skipped}, Failed: {failed}"
    results.append(summary)
    
    return {
        "summary": summary,
        "updated": updated,
        "skipped": skipped,
        "failed": failed,
        "total": total,
        "log": results
    }

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
