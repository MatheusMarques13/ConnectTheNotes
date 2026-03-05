import asyncio
import httpx
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from pathlib import Path

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ.get('DB_NAME', 'connect_the_notes')]

async def fetch_artist_image(artist_name: str) -> str | None:
    """Fetch artist image from Deezer API"""
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(
                'https://api.deezer.com/search/artist',
                params={'q': artist_name, 'limit': 1}
            )
            if response.status_code == 200:
                data = response.json()
                if data.get('data') and len(data['data']) > 0:
                    # Get medium size image (250x250)
                    return data['data'][0].get('picture_medium')
    except Exception as e:
        print(f"Error fetching image for {artist_name}: {e}")
    return None

async def update_artist_images():
    """Update all artists with real images from Deezer"""
    print("Starting image fetch...")
    
    artists = await db.artists.find({}, {'_id': 0, 'id': 1, 'name': 1, 'imageUrl': 1}).to_list(None)
    total = len(artists)
    updated = 0
    skipped = 0
    failed = 0
    
    for i, artist in enumerate(artists, 1):
        # Skip if already has imageUrl
        if artist.get('imageUrl'):
            skipped += 1
            print(f"[{i}/{total}] ⏭️  {artist['name']} - already has image")
            continue
        
        print(f"[{i}/{total}] 🔍 Fetching {artist['name']}...")
        image_url = await fetch_artist_image(artist['name'])
        
        if image_url:
            await db.artists.update_one(
                {'id': artist['id']},
                {'$set': {'imageUrl': image_url}}
            )
            updated += 1
            print(f"[{i}/{total}] ✅ {artist['name']} - {image_url}")
        else:
            failed += 1
            print(f"[{i}/{total}] ❌ {artist['name']} - no image found")
        
        # Rate limit: 50 requests per second max (Deezer)
        await asyncio.sleep(0.1)
    
    print(f"\n✨ Done! Updated: {updated}, Skipped: {skipped}, Failed: {failed}")
    client.close()

if __name__ == '__main__':
    asyncio.run(update_artist_images())
