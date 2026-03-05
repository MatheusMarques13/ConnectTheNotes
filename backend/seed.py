"""
EXPANDED Seed script for Connect the Notes
NEW MODE: Artists connected by SONGS, not by intermediate artists

Example: Taylor Swift → "Everything Has Changed" → Ed Sheeran
NOT: Taylor Swift → Ed Sheeran → Beyoncé
"""
import asyncio
import os
import uuid
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
from pathlib import Path
from collections import defaultdict
import urllib.parse

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ.get('DB_NAME', 'connect_the_notes')]

def uid():
    return str(uuid.uuid4())[:8]

def get_avatar_url(name: str) -> str:
    """Generate avatar URL from UI Avatars API"""
    encoded_name = urllib.parse.quote(name)
    return f"https://ui-avatars.com/api/?name={encoded_name}&size=200&background=random&bold=true"

# ─── ARTIST DATA ─────────────────────────────────────────
ARTISTS_RAW = [
    # ── HIP-HOP / RAP ──
    (1, "Drake", "Hip-Hop/R&B"),
    (3, "Kanye West", "Hip-Hop"),
    (4, "Jay-Z", "Hip-Hop"),
    (6, "Eminem", "Hip-Hop"),
    (12, "Nicki Minaj", "Hip-Hop/Pop"),
    (13, "Travis Scott", "Hip-Hop"),
    (14, "Post Malone", "Hip-Hop/Pop"),
    (20, "Kendrick Lamar", "Hip-Hop"),
    (23, "Lil Wayne", "Hip-Hop"),
    (25, "Cardi B", "Hip-Hop"),
    (26, "J. Cole", "Hip-Hop"),
    (27, "Lil Nas X", "Pop/Hip-Hop"),
    (28, "Megan Thee Stallion", "Hip-Hop"),
    (29, "Future", "Hip-Hop"),
    (30, "21 Savage", "Hip-Hop"),
    (32, "Snoop Dogg", "Hip-Hop"),
    (33, "Dr. Dre", "Hip-Hop"),
    (34, "50 Cent", "Hip-Hop"),
    (39, "DJ Khaled", "Hip-Hop/DJ"),
    (40, "Wiz Khalifa", "Hip-Hop"),
    (58, "Frank Ocean", "R&B/Alternative"),
    (59, "Tyler, The Creator", "Hip-Hop/Alternative"),
    (60, "A$AP Rocky", "Hip-Hop"),

    # ── POP ──
    (2, "Rihanna", "Pop/R&B"),
    (7, "Ed Sheeran", "Pop"),
    (8, "Taylor Swift", "Pop/Country"),
    (10, "Ariana Grande", "Pop/R&B"),
    (11, "Justin Bieber", "Pop/R&B"),
    (15, "Dua Lipa", "Pop/Dance"),
    (17, "Billie Eilish", "Pop/Alternative"),
    (19, "Lady Gaga", "Pop"),
    (22, "Doja Cat", "Pop/Hip-Hop"),
    (46, "Selena Gomez", "Pop"),
    (47, "Charlie Puth", "Pop"),
    (48, "Miley Cyrus", "Pop/Rock"),
    (57, "Adele", "Pop/Soul"),
    (63, "Lizzo", "Pop/Hip-Hop"),
    (64, "Harry Styles", "Pop/Rock"),
    (65, "Olivia Rodrigo", "Pop/Rock"),

    # ── R&B / SOUL ──
    (5, "Beyoncé", "Pop/R&B"),
    (9, "The Weeknd", "R&B/Pop"),
    (21, "SZA", "R&B"),
    (24, "Chris Brown", "R&B/Pop"),
    (35, "Khalid", "R&B/Pop"),
    (36, "Sam Smith", "Pop/R&B"),

    # ── EDM / ELECTRONIC ──
    (66, "The Chainsmokers", "EDM/Pop"),
    (67, "Marshmello", "EDM"),
    (68, "Calvin Harris", "EDM/Pop"),
    (69, "David Guetta", "EDM/Pop"),
    (94, "Daft Punk", "Electronic"),

    # ── LATIN / REGGAETON ──
    (16, "Bad Bunny", "Reggaeton/Latin"),
    (18, "Bruno Mars", "Pop/R&B"),
    (37, "Shakira", "Latin Pop"),
    (98, "Rosalía", "Latin Pop/Flamenco"),
    (99, "J Balvin", "Reggaeton"),
]

# ─── COLLABORATIONS (Song-based) ─────────────────────────────────────
# Format: (artist1_id, artist2_id, song_title, song_type, year)
COLLABS_RAW = [
    # Drake connections
    (1, 2, "Work", "song", 2016),
    (1, 2, "Take Care", "song", 2011),
    (1, 3, "Forever", "song", 2009),
    (1, 29, "What a Time to Be Alive", "album", 2015),
    (1, 30, "Her Loss", "album", 2022),
    (1, 21, "Slime You Out", "song", 2023),
    
    # Rihanna connections
    (2, 3, "All of the Lights", "song", 2010),
    (2, 6, "Love the Way You Lie", "song", 2010),
    (2, 68, "We Found Love", "song", 2011),
    
    # Kanye West connections
    (3, 4, "Watch the Throne", "album", 2011),
    (3, 20, "No More Parties in LA", "song", 2016),
    (3, 94, "Stronger", "song", 2007),
    
    # Jay-Z connections
    (4, 5, "Everything Is Love", "album", 2018),
    (4, 5, "Crazy in Love", "song", 2003),
    (4, 6, "Renegade", "song", 2001),
    
    # Beyoncé connections
    (5, 7, "Perfect Duet", "song", 2017),
    (5, 37, "Beautiful Liar", "song", 2007),
    (5, 19, "Telephone", "song", 2010),
    
    # Ed Sheeran massive web
    (7, 8, "Everything Has Changed", "song", 2012),
    (7, 11, "I Don't Care", "song", 2019),
    (7, 15, "Beautiful People", "song", 2019),
    (7, 18, "Blow", "song", 2019),
    (7, 47, "Cross Me", "song", 2019),
    
    # Taylor Swift connections
    (8, 7, "Everything Has Changed", "song", 2012),
    (8, 29, "End Game", "song", 2017),
    (8, 14, "Fortnight", "song", 2024),
    (8, 65, "Nothing New", "song", 2021),
    
    # The Weeknd
    (9, 10, "Love Me Harder", "song", 2014),
    (9, 1, "Crew Love", "song", 2011),
    (9, 15, "Levitating (Remix)", "song", 2020),
    (9, 94, "Starboy", "song", 2016),
    (9, 94, "I Feel It Coming", "song", 2016),
    
    # Ariana Grande
    (10, 12, "Side to Side", "song", 2016),
    (10, 19, "Rain on Me", "song", 2020),
    (10, 11, "Stuck with U", "song", 2020),
    (10, 9, "Save Your Tears (Remix)", "song", 2021),
    
    # Justin Bieber
    (11, 39, "I'm the One", "song", 2017),
    (11, 7, "I Don't Care", "song", 2019),
    (11, 67, "Set Me Free", "song", 2023),
    
    # Post Malone
    (14, 8, "Fortnight", "song", 2024),
    (14, 30, "Rockstar", "song", 2017),
    (14, 22, "I Like You", "song", 2022),
    
    # Dua Lipa
    (15, 16, "Levitating (Remix)", "song", 2020),
    (15, 68, "One Kiss", "song", 2018),
    (15, 7, "Beautiful People", "song", 2019),
    (15, 9, "Levitating (Remix)", "song", 2020),
    
    # Bad Bunny Latin web
    (16, 99, "OASIS", "album", 2019),
    (16, 25, "I Like It", "song", 2018),
    (16, 98, "La Noche de Anoche", "song", 2020),
    (16, 37, "TQG", "song", 2023),
    (16, 1, "MIA", "song", 2018),
    
    # Bruno Mars
    (18, 7, "Blow", "song", 2019),
    (18, 25, "Finesse (Remix)", "song", 2018),
    (18, 19, "Die With a Smile", "song", 2024),
    
    # Lady Gaga
    (19, 5, "Telephone", "song", 2010),
    (19, 10, "Rain on Me", "song", 2020),
    (19, 18, "Die With a Smile", "song", 2024),
    
    # Kendrick Lamar
    (20, 21, "All the Stars", "song", 2018),
    (20, 3, "No More Parties in LA", "song", 2016),
    
    # SZA
    (21, 22, "Kiss Me More", "song", 2021),
    (21, 1, "Slime You Out", "song", 2023),
    (21, 20, "All the Stars", "song", 2018),
    
    # Doja Cat
    (22, 21, "Kiss Me More", "song", 2021),
    (22, 14, "I Like You", "song", 2022),
    (22, 68, "Potion", "song", 2022),
    
    # Calvin Harris
    (68, 2, "We Found Love", "song", 2011),
    (68, 15, "One Kiss", "song", 2018),
    (68, 22, "Potion", "song", 2022),
    
    # Chainsmokers
    (66, 8, "Lover (Remix)", "song", 2019),
    (66, 67, "Takeaway", "song", 2019),
    
    # More connections for network density
    (29, 1, "What a Time to Be Alive", "album", 2015),
    (29, 8, "End Game", "song", 2017),
    (30, 1, "Her Loss", "album", 2022),
    (30, 14, "Rockstar", "song", 2017),
    (37, 5, "Beautiful Liar", "song", 2007),
    (37, 16, "TQG", "song", 2023),
    (39, 11, "I'm the One", "song", 2017),
    (47, 7, "Cross Me", "song", 2019),
    (65, 8, "Nothing New", "song", 2021),
    (67, 11, "Set Me Free", "song", 2023),
    (67, 66, "Takeaway", "song", 2019),
    (94, 9, "Starboy", "song", 2016),
    (94, 9, "I Feel It Coming", "song", 2016),
    (94, 3, "Stronger", "song", 2007),
    (98, 16, "La Noche de Anoche", "song", 2020),
    (99, 16, "OASIS", "album", 2019),
]


async def seed():
    print("🔥 Dropping existing collections...")
    await db.artists.drop()
    await db.artistConnections.drop()
    
    # ─── 1. INSERT ARTISTS ─────────────────────────────────
    id_map = {}
    artist_docs = []
    seen_ids = set()
    
    for temp_id, name, genre in ARTISTS_RAW:
        if temp_id in seen_ids:
            continue
        seen_ids.add(temp_id)
        real_id = uid()
        id_map[temp_id] = real_id
        artist_docs.append({
            "id": real_id,
            "name": name,
            "genre": genre,
            "imageUrl": get_avatar_url(name),
        })
    
    print(f"✅ Inserting {len(artist_docs)} artists with avatars...")
    if artist_docs:
        await db.artists.insert_many(artist_docs)
    
    # ─── 2. BUILD SONG-BASED CONNECTIONS ─────────────────────
    connection_docs = []
    seen = set()
    
    for a1, a2, title, ctype, year in COLLABS_RAW:
        if a1 not in id_map or a2 not in id_map:
            continue
        if a1 == a2:
            continue
        
        key_forward = (a1, a2, title)
        key_backward = (a2, a1, title)
        
        if key_forward not in seen:
            seen.add(key_forward)
            seen.add(key_backward)
            
            connection_docs.append({
                "id": uid(),
                "artist1": id_map[a1],
                "artist2": id_map[a2],
                "song": {
                    "title": title,
                    "type": ctype,
                    "year": year,
                    "coverUrl": ""
                }
            })
    
    print(f"✅ Inserting {len(connection_docs)} artist connections (song-based)...")
    if connection_docs:
        await db.artistConnections.insert_many(connection_docs)
    
    # ─── 3. CREATE INDEXES ─────────────────────────────────
    await db.artists.create_index("id", unique=True)
    await db.artists.create_index([("name", "text")])
    await db.artistConnections.create_index("id", unique=True)
    await db.artistConnections.create_index("artist1")
    await db.artistConnections.create_index("artist2")
    await db.artistConnections.create_index(["artist1", "artist2"])
    
    print("\n🎉 Seed complete!")
    print(f"  Artists: {len(artist_docs)}")
    print(f"  Direct Connections (Songs): {len(connection_docs)}")
    print("\n🎵 Game mode: Artists connected by SHARED SONGS")
    print("   Example path: Taylor Swift → 'Everything Has Changed' → Ed Sheeran")


if __name__ == "__main__":
    asyncio.run(seed())
