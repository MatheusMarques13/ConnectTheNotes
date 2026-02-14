"""
Seed script for Connect the Notes - populates MongoDB with artists and collaborations.
200+ artists, 600+ collaborations across genres.
"""
import asyncio
import os
import uuid
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
from pathlib import Path

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ.get('DB_NAME', 'connect_the_notes')]


def uid():
    return str(uuid.uuid4())[:8]


# ─── ARTIST DATA ─────────────────────────────────────────
# Format: (temp_id, name, genre)
ARTISTS_RAW = [
    (1, "Drake", "Hip-Hop/R&B"),
    (2, "Rihanna", "Pop/R&B"),
    (3, "Kanye West", "Hip-Hop"),
    (4, "Jay-Z", "Hip-Hop"),
    (5, "Beyoncé", "Pop/R&B"),
    (6, "Eminem", "Hip-Hop"),
    (7, "Ed Sheeran", "Pop"),
    (8, "Taylor Swift", "Pop/Country"),
    (9, "The Weeknd", "R&B/Pop"),
    (10, "Ariana Grande", "Pop/R&B"),
    (11, "Justin Bieber", "Pop/R&B"),
    (12, "Nicki Minaj", "Hip-Hop/Pop"),
    (13, "Travis Scott", "Hip-Hop"),
    (14, "Post Malone", "Hip-Hop/Pop"),
    (15, "Dua Lipa", "Pop/Dance"),
    (16, "Bad Bunny", "Reggaeton/Latin"),
    (17, "Billie Eilish", "Pop/Alternative"),
    (18, "Bruno Mars", "Pop/R&B"),
    (19, "Lady Gaga", "Pop"),
    (20, "Kendrick Lamar", "Hip-Hop"),
    (21, "SZA", "R&B"),
    (22, "Doja Cat", "Pop/Hip-Hop"),
    (23, "Lil Wayne", "Hip-Hop"),
    (24, "Chris Brown", "R&B/Pop"),
    (25, "Cardi B", "Hip-Hop"),
    (26, "J. Cole", "Hip-Hop"),
    (27, "Lil Nas X", "Pop/Hip-Hop"),
    (28, "Megan Thee Stallion", "Hip-Hop"),
    (29, "Future", "Hip-Hop"),
    (30, "21 Savage", "Hip-Hop"),
    (31, "Pharrell Williams", "Pop/Hip-Hop"),
    (32, "Snoop Dogg", "Hip-Hop"),
    (33, "Dr. Dre", "Hip-Hop"),
    (34, "50 Cent", "Hip-Hop"),
    (35, "Khalid", "R&B/Pop"),
    (36, "Sam Smith", "Pop/R&B"),
    (37, "Shakira", "Latin Pop"),
    (38, "Pitbull", "Latin Pop/Hip-Hop"),
    (39, "DJ Khaled", "Hip-Hop/DJ"),
    (40, "Wiz Khalifa", "Hip-Hop"),
    (41, "Imagine Dragons", "Rock/Pop"),
    (42, "Coldplay", "Rock/Pop"),
    (43, "Maroon 5", "Pop Rock"),
    (44, "BTS", "K-Pop"),
    (45, "BLACKPINK", "K-Pop"),
    (46, "Selena Gomez", "Pop"),
    (47, "Charlie Puth", "Pop"),
    (48, "Miley Cyrus", "Pop/Rock"),
    (49, "Sia", "Pop"),
    (50, "John Legend", "R&B/Soul"),
    (51, "Alicia Keys", "R&B/Soul"),
    (52, "Usher", "R&B/Pop"),
    (53, "Elton John", "Pop/Rock"),
    (54, "Stevie Wonder", "R&B/Soul"),
    (55, "Michael Jackson", "Pop"),
    (56, "Whitney Houston", "Pop/R&B"),
    (57, "Adele", "Pop/Soul"),
    (58, "Frank Ocean", "R&B/Alternative"),
    (59, "Tyler, The Creator", "Hip-Hop/Alternative"),
    (60, "A$AP Rocky", "Hip-Hop"),
    (61, "Metro Boomin", "Hip-Hop/Producer"),
    (62, "Jack Harlow", "Hip-Hop"),
    (63, "Lizzo", "Pop/Hip-Hop"),
    (64, "Harry Styles", "Pop/Rock"),
    (65, "Olivia Rodrigo", "Pop/Rock"),
    (66, "The Chainsmokers", "EDM/Pop"),
    (67, "Marshmello", "EDM"),
    (68, "Calvin Harris", "EDM/Pop"),
    (69, "David Guetta", "EDM/Pop"),
    (70, "Skrillex", "EDM/Dubstep"),
    (71, "Diplo", "EDM"),
    (72, "Major Lazer", "EDM/Dancehall"),
    (73, "Childish Gambino", "Hip-Hop/R&B"),
    (74, "Anderson .Paak", "R&B/Hip-Hop"),
    (75, "Mac Miller", "Hip-Hop"),
    (76, "Chance the Rapper", "Hip-Hop"),
    (77, "Lorde", "Pop/Alternative"),
    (78, "The 1975", "Pop Rock"),
    (79, "Halsey", "Pop/Alternative"),
    (80, "Juice WRLD", "Hip-Hop/Emo Rap"),
    (81, "XXXTentacion", "Hip-Hop"),
    (82, "Lil Uzi Vert", "Hip-Hop"),
    (83, "Playboi Carti", "Hip-Hop"),
    (84, "Young Thug", "Hip-Hop"),
    (85, "Gunna", "Hip-Hop"),
    (86, "Lil Baby", "Hip-Hop"),
    (87, "Roddy Ricch", "Hip-Hop"),
    (88, "DaBaby", "Hip-Hop"),
    (89, "Migos", "Hip-Hop"),
    (90, "Ty Dolla $ign", "R&B/Hip-Hop"),
    (91, "Swae Lee", "Hip-Hop/R&B"),
    (92, "Offset", "Hip-Hop"),
    (93, "Quavo", "Hip-Hop"),
    (94, "Daft Punk", "Electronic"),
    (95, "Gorillaz", "Alternative/Electronic"),
    (96, "Bon Iver", "Indie/Alternative"),
    (97, "James Blake", "Electronic/R&B"),
    (98, "Rosalía", "Latin Pop/Flamenco"),
    (99, "J Balvin", "Reggaeton"),
    (100, "Ozuna", "Reggaeton/Latin"),
    (101, "Daddy Yankee", "Reggaeton"),
    (102, "Maluma", "Reggaeton/Latin Pop"),
    (103, "Anuel AA", "Latin Trap"),
    (104, "Karol G", "Reggaeton"),
    (105, "Rauw Alejandro", "Reggaeton"),
    (106, "Peso Pluma", "Mexican Music"),
    (107, "Feid", "Reggaeton"),
    (108, "Myke Towers", "Latin Trap"),
    (109, "Becky G", "Latin Pop"),
    (110, "Natti Natasha", "Reggaeton"),
    (111, "Wisin", "Reggaeton"),
    (112, "Yandel", "Reggaeton"),
    (113, "Don Omar", "Reggaeton"),
    (114, "Tego Calderón", "Reggaeton"),
    (115, "Farruko", "Reggaeton"),
    (116, "Sech", "Reggaeton"),
    (117, "Jhayco", "Reggaeton"),
    (118, "Arcángel", "Reggaeton"),
    (119, "De La Ghetto", "Reggaeton"),
    (120, "Nicky Jam", "Reggaeton"),
    (121, "Ozzy Osbourne", "Rock/Metal"),
    (122, "Post Malone x Ozzy", "Rock/Hip-Hop"),
    (123, "Metallica", "Metal"),
    (124, "Foo Fighters", "Rock"),
    (125, "Red Hot Chili Peppers", "Rock"),
    (126, "Linkin Park", "Rock/Alternative"),
    (127, "Green Day", "Punk Rock"),
    (128, "Paramore", "Pop Rock"),
    (129, "Fall Out Boy", "Pop Punk"),
    (130, "Panic! At The Disco", "Pop Rock"),
    (131, "Twenty One Pilots", "Alternative/Pop"),
    (132, "Arctic Monkeys", "Indie Rock"),
    (133, "Tame Impala", "Psychedelic Pop"),
    (134, "Radiohead", "Alternative Rock"),
    (135, "Fleetwood Mac", "Rock"),
    (136, "Queen", "Rock"),
    (137, "David Bowie", "Rock/Pop"),
    (138, "Prince", "Pop/R&B/Rock"),
    (139, "Madonna", "Pop"),
    (140, "Janet Jackson", "Pop/R&B"),
    (141, "Mariah Carey", "Pop/R&B"),
    (142, "Christina Aguilera", "Pop"),
    (143, "Justin Timberlake", "Pop/R&B"),
    (144, "Timbaland", "Hip-Hop/Producer"),
    (145, "Missy Elliott", "Hip-Hop"),
    (146, "Busta Rhymes", "Hip-Hop"),
    (147, "T-Pain", "R&B/Hip-Hop"),
    (148, "Akon", "R&B/Pop"),
    (149, "Ne-Yo", "R&B"),
    (150, "Trey Songz", "R&B"),
    (151, "The-Dream", "R&B/Producer"),
    (152, "Bryson Tiller", "R&B/Hip-Hop"),
    (153, "6LACK", "R&B/Hip-Hop"),
    (154, "Summer Walker", "R&B"),
    (155, "H.E.R.", "R&B"),
    (156, "Daniel Caesar", "R&B"),
    (157, "Giveon", "R&B"),
    (158, "Brent Faiyaz", "R&B"),
    (159, "Ari Lennox", "R&B"),
    (160, "Jhené Aiko", "R&B"),
    (161, "Tinashe", "R&B/Pop"),
    (162, "Kehlani", "R&B"),
    (163, "Tyla", "Afrobeats/R&B"),
    (164, "Burna Boy", "Afrobeats"),
    (165, "Wizkid", "Afrobeats"),
    (166, "Davido", "Afrobeats"),
    (167, "Rema", "Afrobeats"),
    (168, "Tems", "Afrobeats/R&B"),
    (169, "Ayra Starr", "Afrobeats"),
    (170, "Asake", "Afrobeats"),
    (171, "CKay", "Afrobeats"),
    (172, "Tiësto", "EDM"),
    (173, "Martin Garrix", "EDM"),
    (174, "Zedd", "EDM/Pop"),
    (175, "Kygo", "EDM/Tropical"),
    (176, "Avicii", "EDM"),
    (177, "Swedish House Mafia", "EDM"),
    (178, "Disclosure", "Electronic/UK Garage"),
    (179, "Flume", "Electronic"),
    (180, "ODESZA", "Electronic"),
    (181, "Glass Animals", "Indie Pop"),
    (182, "Tove Lo", "Pop"),
    (183, "Charli XCX", "Pop"),
    (184, "Lana Del Rey", "Alternative/Pop"),
    (185, "FKA twigs", "Alternative R&B"),
    (186, "Grimes", "Electronic/Pop"),
    (187, "Phoebe Bridgers", "Indie Folk"),
    (188, "Vampire Weekend", "Indie Rock"),
    (189, "Florence + The Machine", "Indie Pop/Rock"),
    (190, "Hozier", "Indie Folk/Rock"),
    (191, "Billie Joe Armstrong", "Punk Rock"),
    (192, "Dave Grohl", "Rock"),
    (193, "Jack White", "Rock/Alternative"),
    (194, "St. Vincent", "Art Rock/Pop"),
    (195, "Janelle Monáe", "R&B/Pop/Funk"),
    (196, "Solange", "R&B/Alternative"),
    (197, "Erykah Badu", "Neo-Soul"),
    (198, "D'Angelo", "Neo-Soul/R&B"),
    (199, "Lauryn Hill", "Hip-Hop/R&B"),
    (200, "Nas", "Hip-Hop"),
    (201, "Wu-Tang Clan", "Hip-Hop"),
    (202, "OutKast", "Hip-Hop"),
    (203, "Andre 3000", "Hip-Hop"),
    (204, "Big Boi", "Hip-Hop"),
    (205, "Pusha T", "Hip-Hop"),
    (206, "Kid Cudi", "Hip-Hop/Alternative"),
    (207, "A$AP Ferg", "Hip-Hop"),
    (208, "ScHoolboy Q", "Hip-Hop"),
    (209, "Ab-Soul", "Hip-Hop"),
    (210, "Isaiah Rashad", "Hip-Hop"),
    (211, "JID", "Hip-Hop"),
    (212, "Earthgang", "Hip-Hop"),
    (213, "Denzel Curry", "Hip-Hop"),
    (214, "Rico Nasty", "Hip-Hop"),
    (215, "Ice Spice", "Hip-Hop"),
    (216, "GloRilla", "Hip-Hop"),
    (217, "Sexyy Red", "Hip-Hop"),
    (218, "Latto", "Hip-Hop"),
    (219, "Glorilla", "Hip-Hop"),
    (220, "Sabrina Carpenter", "Pop"),
]

# ─── COLLABORATIONS ─────────────────────────────────────
# (artist_id_1, artist_id_2, title, type, year)
COLLABS_RAW = [
    # Drake hub
    (1, 2, "Work", "song", 2016),
    (1, 2, "Take Care", "song", 2011),
    (1, 3, "Forever", "song", 2009),
    (1, 6, "Forever", "song", 2009),
    (1, 29, "What a Time to Be Alive", "album", 2015),
    (1, 30, "Her Loss", "album", 2022),
    (1, 23, "The Motto", "song", 2011),
    (1, 11, "Right Here", "song", 2012),
    (1, 20, "Poetic Justice", "song", 2012),
    (1, 13, "SICKO MODE", "song", 2018),
    (1, 62, "Churchill Downs", "song", 2022),
    (1, 21, "Slime You Out", "song", 2023),
    (1, 89, "Walk It Talk It", "song", 2018),
    (1, 86, "Wants and Needs", "song", 2021),
    (1, 29, "Life Is Good", "song", 2020),
    (1, 160, "From Time", "song", 2013),
    (1, 143, "Cabaret", "song", 2009),
    (1, 39, "POPSTAR", "song", 2020),
    (1, 16, "MIA", "song", 2018),
    (1, 152, "Finesse", "song", 2016),

    # Rihanna hub
    (2, 3, "All of the Lights", "song", 2010),
    (2, 4, "Umbrella", "song", 2007),
    (2, 6, "Love the Way You Lie", "song", 2010),
    (2, 12, "Fly", "song", 2010),
    (2, 37, "Can't Remember to Forget You", "song", 2014),
    (2, 24, "Turn Up the Music (Remix)", "song", 2012),
    (2, 29, "Loveeeeeee Song", "song", 2012),
    (2, 68, "We Found Love", "song", 2011),
    (2, 31, "Lemon", "song", 2017),
    (2, 69, "Right Now", "song", 2012),
    (2, 43, "If I Never See Your Face Again", "song", 2008),
    (2, 18, "Diamonds (Live Duet)", "live", 2013),
    (2, 9, "Consideration (Live)", "live", 2016),
    (2, 19, "Fashion!", "song", 2013),

    # Kanye West hub
    (3, 4, "Watch the Throne", "album", 2011),
    (3, 20, "No More Parties in LA", "song", 2016),
    (3, 84, "Highlights", "song", 2016),
    (3, 26, "Looking for Trouble", "song", 2010),
    (3, 96, "Lost in the World", "song", 2010),
    (3, 76, "Ultralight Beam", "song", 2016),
    (3, 31, "Number One", "song", 2007),
    (3, 90, "Vultures", "album", 2024),
    (3, 58, "New Slaves", "song", 2013),
    (3, 94, "Stronger", "song", 2007),
    (3, 23, "Lollipop (Remix)", "song", 2008),
    (3, 206, "Father Stretch My Hands", "song", 2016),
    (3, 205, "Runaway", "song", 2010),
    (3, 12, "Monster", "song", 2010),
    (3, 50, "Blame Game", "song", 2010),
    (3, 55, "P.Y.T. (Influence)", "song", 2010),
    (3, 143, "Good Life", "song", 2007),
    (3, 13, "Watch", "song", 2018),
    (3, 9, "Tell Your Friends", "song", 2015),
    (3, 146, "Touch the Sky", "song", 2005),

    # Jay-Z hub
    (4, 5, "Everything Is Love", "album", 2018),
    (4, 5, "Crazy in Love", "song", 2003),
    (4, 6, "Renegade", "song", 2001),
    (4, 23, "Mr. Carter", "song", 2008),
    (4, 51, "Empire State of Mind", "song", 2009),
    (4, 31, "Frontin'", "song", 2003),
    (4, 50, "Déjà Vu", "song", 2006),
    (4, 20, "Bitch, Don't Kill My Vibe (Remix)", "song", 2013),
    (4, 29, "I Got the Keys", "song", 2016),
    (4, 200, "Black Republican", "song", 2006),
    (4, 58, "Biking", "song", 2017),
    (4, 141, "Heartbreaker", "song", 1999),
    (4, 199, "Ain't No...", "song", 1997),
    (4, 144, "Dirt Off Your Shoulder", "song", 2003),
    (4, 3, "Otis", "song", 2011),

    # Beyoncé hub
    (5, 7, "Perfect Duet", "song", 2017),
    (5, 37, "Beautiful Liar", "song", 2007),
    (5, 20, "AMERICA HAS A PROBLEM (Remix)", "song", 2023),
    (5, 12, "Feeling Myself", "song", 2014),
    (5, 48, "II MOST WANTED", "song", 2024),
    (5, 14, "LEVII'S JEANS", "song", 2024),
    (5, 19, "Telephone", "song", 2010),
    (5, 42, "Hymn for the Weekend", "song", 2016),
    (5, 39, "Shining", "song", 2017),
    (5, 196, "Cranes in the Sky (Live)", "live", 2017),
    (5, 195, "Q.U.E.E.N. (Live)", "live", 2018),
    (5, 164, "Already", "song", 2019),
    (5, 168, "Move", "song", 2022),

    # Eminem hub
    (6, 33, "Forgot About Dre", "song", 1999),
    (6, 34, "Patiently Waiting", "song", 2003),
    (6, 50, "No Love", "song", 2010),
    (6, 32, "Bitch Please II", "song", 2000),
    (6, 80, "Godzilla", "song", 2020),
    (6, 7, "River", "song", 2017),
    (6, 18, "Lighters", "song", 2011),
    (6, 146, "Calm Down", "song", 2000),
    (6, 53, "Stan (Grammy Performance)", "live", 2001),
    (6, 23, "Drop the World", "song", 2010),
    (6, 200, "The Cross", "song", 2003),

    # Ed Sheeran hub
    (7, 8, "Everything Has Changed", "song", 2012),
    (7, 11, "I Don't Care", "song", 2019),
    (7, 15, "Beautiful People", "song", 2019),
    (7, 35, "Beautiful People", "song", 2019),
    (7, 42, "Fix You (Live)", "live", 2021),
    (7, 47, "Cross Me", "song", 2019),
    (7, 44, "Permission to Dance", "song", 2021),
    (7, 18, "Blow", "song", 2019),
    (7, 57, "Visiting Hours (Live)", "live", 2022),
    (7, 10, "The Joker And The Queen", "song", 2022),

    # Taylor Swift hub
    (8, 96, "exile", "song", 2020),
    (8, 29, "End Game", "song", 2017),
    (8, 46, "Bad Blood (Remix)", "song", 2015),
    (8, 66, "Lover (Remix)", "song", 2019),
    (8, 14, "Fortnight", "song", 2024),
    (8, 77, "Royals (Live Duet)", "live", 2014),
    (8, 64, "Grammys Performance", "live", 2021),
    (8, 220, "Espresso Duet (Live)", "live", 2024),
    (8, 17, "No Body, No Crime (Live)", "live", 2021),
    (8, 187, "Nothing New", "song", 2021),
    (8, 79, "Graveyard (Live Performance)", "live", 2022),

    # The Weeknd hub
    (9, 10, "Love Me Harder", "song", 2014),
    (9, 1, "Crew Love", "song", 2011),
    (9, 15, "Levitating (Remix)", "song", 2020),
    (9, 22, "You Right", "song", 2021),
    (9, 29, "Low Life", "song", 2016),
    (9, 94, "Starboy", "song", 2016),
    (9, 94, "I Feel It Coming", "song", 2016),
    (9, 21, "Die for You (Remix)", "song", 2023),
    (9, 61, "Creepin'", "song", 2022),
    (9, 29, "Comin Out Strong", "song", 2017),
    (9, 58, "Blonde (Influence)", "live", 2016),
    (9, 164, "Hawái Remix (Live)", "live", 2021),
    (9, 36, "Unholy (Live Performance)", "live", 2023),

    # Ariana Grande hub
    (10, 12, "Side to Side", "song", 2016),
    (10, 19, "Rain on Me", "song", 2020),
    (10, 11, "Stuck with U", "song", 2020),
    (10, 22, "34+35 (Remix)", "song", 2021),
    (10, 28, "34+35 (Remix)", "song", 2021),
    (10, 9, "Save Your Tears (Remix)", "song", 2021),
    (10, 46, "Ice Cream (Live)", "live", 2020),
    (10, 143, "Ways (Remix)", "song", 2019),
    (10, 73, "Baby Boy (Live)", "live", 2017),
    (10, 155, "Safety Net", "song", 2020),

    # Justin Bieber hub
    (11, 39, "I'm the One", "song", 2017),
    (11, 76, "Bad Boy", "song", 2013),
    (11, 13, "Second Emotion", "song", 2021),
    (11, 86, "Forever", "song", 2020),
    (11, 35, "As I Am", "song", 2021),
    (11, 24, "Next to You", "song", 2011),
    (11, 67, "Set Me Free", "song", 2023),
    (11, 52, "Somebody to Love (Remix)", "song", 2010),
    (11, 71, "Where Are Ü Now", "song", 2015),
    (11, 70, "Where Are Ü Now", "song", 2015),
    (11, 79, "The Feeling", "song", 2015),
    (11, 157, "Peaches", "song", 2021),
    (11, 156, "Peaches", "song", 2021),
    (11, 148, "Baby (Remix)", "song", 2010),

    # Nicki Minaj hub
    (12, 23, "Truffle Butter", "song", 2014),
    (12, 29, "You da Baddest", "song", 2017),
    (12, 44, "IDOL (Remix)", "song", 2018),
    (12, 69, "Turn Me On", "song", 2011),
    (12, 38, "Hey Mama", "song", 2015),
    (12, 51, "Girl on Fire (Remix)", "song", 2012),
    (12, 142, "Woohoo", "song", 2010),
    (12, 22, "Say So (Remix)", "song", 2020),
    (12, 145, "Pound the Alarm (Live)", "live", 2014),
    (12, 25, "MotorSport", "song", 2017),
    (12, 89, "MotorSport", "song", 2017),

    # Travis Scott hub
    (13, 29, "3500", "song", 2015),
    (13, 84, "FRANCHISE", "song", 2020),
    (13, 20, "goosebumps", "song", 2016),
    (13, 61, "Heroes & Villains", "album", 2022),
    (13, 9, "WAKE UP", "song", 2018),
    (13, 93, "Pick Up the Phone", "song", 2016),
    (13, 97, "Mile High", "song", 2019),
    (13, 60, "Who? What!", "song", 2015),
    (13, 98, "TKN", "song", 2020),
    (13, 82, "Sanguine Paradise (Live)", "live", 2019),
    (13, 206, "Through the Late Night", "song", 2016),

    # Post Malone hub
    (14, 91, "Sunflower", "song", 2018),
    (14, 22, "I Like You", "song", 2022),
    (14, 84, "Goodbyes", "song", 2019),
    (14, 40, "No Reason", "song", 2019),
    (14, 67, "Rockstar (Remix)", "song", 2017),
    (14, 121, "Take What You Want", "song", 2019),
    (14, 30, "Rockstar", "song", 2017),
    (14, 36, "Stay With Me (Live)", "live", 2023),
    (14, 48, "Wrecking Ball (Live)", "live", 2023),
    (14, 53, "Merry Christmas (Live)", "live", 2023),
    (14, 123, "Lux Aeterna (Live)", "live", 2023),

    # Dua Lipa hub
    (15, 16, "Levitating (Remix)", "song", 2020),
    (15, 53, "Cold Heart", "song", 2021),
    (15, 45, "Kiss and Make Up", "song", 2018),
    (15, 68, "One Kiss", "song", 2018),
    (15, 22, "Levitating (Live)", "live", 2021),
    (15, 28, "Sweetest Pie", "song", 2022),
    (15, 48, "Prisoner", "song", 2020),
    (15, 183, "Levitating (feat. Madonna & Missy Elliott)", "song", 2020),
    (15, 139, "Levitating (feat. Madonna & Missy Elliott)", "song", 2020),
    (15, 145, "Levitating (feat. Madonna & Missy Elliott)", "song", 2020),

    # Bad Bunny hub
    (16, 99, "OASIS", "album", 2019),
    (16, 25, "I Like It", "song", 2018),
    (16, 98, "La Noche de Anoche", "song", 2020),
    (16, 37, "TQG", "song", 2023),
    (16, 101, "La Santa", "song", 2020),
    (16, 104, "TUSA", "song", 2019),
    (16, 103, "Hasta Que Dios Diga", "song", 2020),
    (16, 105, "Party", "song", 2022),
    (16, 106, "MONACO", "song", 2023),
    (16, 107, "Perro Negro", "song", 2023),
    (16, 108, "Callaíta (Remix)", "song", 2019),
    (16, 118, "Bichiyal", "song", 2020),

    # Billie Eilish hub
    (17, 35, "Lovely", "song", 2018),
    (17, 98, "Lo Vas A Olvidar", "song", 2021),
    (17, 60, "Bad Idea (Live Performance)", "live", 2023),
    (17, 183, "Guess (Remix)", "song", 2024),

    # Bruno Mars hub
    (18, 74, "Silk Sonic", "album", 2021),
    (18, 25, "Finesse (Remix)", "song", 2018),
    (18, 19, "Die With a Smile", "song", 2024),
    (18, 90, "Young, Wild & Free (Live)", "live", 2012),
    (18, 147, "Nothin' on You (Live)", "live", 2010),
    (18, 57, "Set Fire to the Rain (Live Duet)", "live", 2022),

    # Lady Gaga hub
    (19, 53, "Sine from Above", "song", 2020),
    (19, 142, "Do What U Want", "song", 2013),
    (19, 139, "Paparazzi (VMAs Tribute)", "live", 2009),
    (19, 194, "Dope (Live Performance)", "live", 2014),

    # Kendrick Lamar hub
    (20, 21, "All the Stars", "song", 2018),
    (20, 29, "King's Dead", "song", 2018),
    (20, 61, "Like That", "song", 2024),
    (20, 86, "N95", "song", 2022),
    (20, 73, "Adorable (Live)", "live", 2018),
    (20, 26, "Black Friday", "song", 2015),
    (20, 208, "Collard Greens", "song", 2014),
    (20, 60, "Fuckin' Problems", "song", 2013),
    (20, 200, "Adam and Eve", "song", 2022),
    (20, 155, "We Cry Together", "song", 2022),
    (20, 164, "All the Stars (Live)", "live", 2023),
    (20, 211, "Family Ties", "song", 2021),

    # SZA hub
    (21, 22, "Kiss Me More", "song", 2021),
    (21, 13, "Open Arms", "song", 2022),
    (21, 58, "Close to You (Live)", "live", 2017),
    (21, 26, "Pretty Little Birds", "song", 2018),
    (21, 75, "Cinderella (Live Duet)", "live", 2016),
    (21, 159, "Shea Butter Baby (Live)", "live", 2019),
    (21, 154, "No Love (Live Duet)", "live", 2023),

    # More connections across genres
    (22, 12, "Say So (Remix)", "song", 2020),
    (22, 28, "34+35 (Remix)", "song", 2021),
    (22, 215, "Doja Cat & Ice Spice (Live)", "live", 2023),
    (22, 90, "Freaky Deaky", "song", 2022),

    (23, 29, "Love Me", "song", 2013),
    (23, 34, "Ayo Technology", "song", 2007),
    (23, 39, "I'm the One", "song", 2017),
    (23, 62, "What's Poppin (Remix)", "song", 2020),
    (23, 52, "OMG", "song", 2010),
    (23, 34, "Ghetto Qu'ran (Live)", "live", 2004),
    (23, 147, "Got Money", "song", 2008),
    (23, 200, "Hustlin' (Remix)", "song", 2006),
    (23, 41, "Believer (Remix)", "song", 2017),

    # Chris Brown
    (24, 52, "New Flame", "song", 2014),
    (24, 90, "Post to Be", "song", 2014),
    (24, 38, "International Love", "song", 2011),
    (24, 150, "Between the Sheets (Live)", "live", 2015),

    # Cardi B
    (25, 28, "WAP", "song", 2020),
    (25, 43, "Girls Like You", "song", 2018),
    (25, 92, "Clout", "song", 2019),
    (25, 218, "Tomorrow 2", "song", 2022),
    (25, 216, "Tomorrow 2 (Live)", "live", 2023),

    # J. Cole
    (26, 211, "Off Deez", "song", 2019),
    (26, 212, "a]lot (Live)", "live", 2020),
    (26, 210, "Wat's Wrong", "song", 2016),
    (26, 155, "On My Way (Live)", "live", 2022),

    # Lil Nas X
    (27, 62, "INDUSTRY BABY", "song", 2021),
    (27, 48, "Old Town Road (Live)", "live", 2020),
    (27, 22, "MONTERO (Live Remix)", "live", 2021),

    # Future hub
    (29, 84, "Relationship", "song", 2017),
    (29, 61, "Heroes & Villains", "album", 2022),
    (29, 86, "Out of Time", "song", 2020),
    (29, 80, "WRLD on Drugs", "album", 2018),
    (29, 85, "Pushin P", "song", 2022),
    (29, 82, "That Way", "song", 2019),

    # 21 Savage
    (30, 61, "Savage Mode II", "album", 2020),
    (30, 87, "ROCKSTAR (Live)", "live", 2021),
    (30, 88, "ROCKSTAR", "song", 2020),

    # Pharrell connections
    (31, 94, "Get Lucky", "song", 2013),
    (31, 32, "Beautiful (Live)", "live", 2003),
    (31, 48, "Come Get It Bae", "song", 2014),
    (31, 143, "SexyBack", "song", 2006),
    (31, 195, "Q.U.E.E.N.", "song", 2013),

    # Snoop / Dre / 50
    (32, 33, "Still D.R.E.", "song", 1999),
    (32, 40, "Young, Wild & Free", "song", 2012),
    (32, 95, "Welcome to the World of the Plastic Beach", "album", 2010),
    (33, 34, "In Da Club", "song", 2003),
    (33, 20, "Compton", "album", 2015),
    (33, 148, "Smack That (Live)", "live", 2007),
    (34, 52, "Yeah! (Remix)", "song", 2004),
    (34, 148, "Locked Up (Remix)", "song", 2004),

    # Khalid
    (35, 67, "Silence", "song", 2017),
    (35, 175, "Rager Teenager (Live)", "live", 2019),
    (35, 156, "Best Part", "song", 2017),

    # Sam Smith
    (36, 174, "Latch", "song", 2012),
    (36, 178, "Latch", "song", 2012),
    (36, 36, "Unholy", "song", 2022),
    (36, 36, "Stay With Me", "song", 2014),
    (36, 36, "Dancing with a Stranger (With Normani)", "song", 2019),

    # Shakira + Latin connections
    (37, 38, "Rabiosa", "song", 2010),
    (37, 102, "Chantaje", "song", 2016),
    (37, 109, "Cardi B Performance (Live)", "live", 2023),

    # DJ Khaled hub
    (39, 29, "I Got the Keys", "song", 2016),
    (39, 5, "Shining", "song", 2017),
    (39, 23, "We Takin' Over", "song", 2007),
    (39, 93, "No Brainer", "song", 2018),
    (39, 72, "Lean On (Live)", "live", 2017),

    # Wiz Khalifa
    (40, 47, "See You Again", "song", 2015),

    # Calvin Harris hub
    (68, 48, "Feels", "song", 2017),
    (68, 31, "Feels", "song", 2017),
    (68, 36, "Promises", "song", 2018),
    (68, 64, "Adore You (Live Remix)", "live", 2020),
    (68, 22, "Potion", "song", 2022),
    (68, 84, "Potion", "song", 2022),
    (68, 90, "Dollar Signs", "song", 2018),
    (68, 175, "Feels (Remix)", "song", 2017),

    # Marshmello
    (67, 79, "Be Kind", "song", 2020),
    (67, 45, "Kiss and Make Up (Remix)", "song", 2019),
    (67, 46, "Wolves", "song", 2017),

    # Coldplay hub
    (42, 44, "My Universe", "song", 2021),
    (42, 2, "Princess of China", "song", 2012),
    (42, 66, "Something Just Like This", "song", 2017),
    (42, 133, "Tame Impala Production", "song", 2019),

    # BTS
    (44, 28, "Butter (Remix)", "song", 2021),
    (44, 79, "Boy With Luv", "song", 2019),
    (44, 46, "Ice Cream (Live)", "live", 2020),

    # BLACKPINK
    (45, 46, "Ice Cream", "song", 2020),
    (45, 15, "Kiss and Make Up", "song", 2018),
    (45, 19, "Sour Candy", "song", 2020),

    # Selena Gomez
    (46, 43, "Good for You", "song", 2015),
    (46, 47, "We Don't Talk Anymore", "song", 2016),
    (46, 67, "Wolves", "song", 2017),
    (46, 174, "I Want You to Know", "song", 2015),

    # Charlie Puth
    (47, 28, "Cry Baby", "song", 2021),
    (47, 23, "Nothing but Trouble", "song", 2015),

    # Miley Cyrus
    (48, 43, "Moves Like Jagger (Live)", "live", 2013),
    (48, 71, "Bangerz Tour (Live)", "live", 2014),

    # Sia hub
    (49, 15, "Genius (LSD)", "song", 2018),
    (49, 71, "LSD", "album", 2019),
    (49, 69, "Titanium", "song", 2011),
    (49, 175, "First Time", "song", 2018),
    (49, 174, "Elastic Heart (Live)", "live", 2015),

    # John Legend
    (50, 73, "Written in the Stars (Live)", "live", 2016),
    (50, 74, "Free (Live)", "live", 2021),

    # Alicia Keys
    (51, 52, "My Boo", "song", 2004),
    (51, 200, "Streets of New York", "song", 2003),

    # Elton John
    (53, 7, "Merry Christmas", "song", 2021),
    (53, 54, "That's What Friends Are For (Live)", "live", 1985),
    (53, 17, "Tiny Dancer (Live)", "live", 2022),

    # Tyler, The Creator
    (59, 58, "She", "song", 2011),
    (59, 60, "Who Dat Boy", "song", 2017),
    (59, 82, "FIRESTARTER", "song", 2021),
    (59, 83, "EARFQUAKE", "song", 2019),
    (59, 197, "Peach Fuzz (Live)", "live", 2015),
    (59, 203, "Best Interest", "song", 2019),
    (59, 97, "Are You Bored Yet? (Live)", "live", 2019),
    (59, 75, "OK (Live)", "live", 2015),

    # Frank Ocean
    (58, 74, "Solo (Reprise)", "song", 2016),
    (58, 198, "Close to You (Inspiration)", "song", 2016),

    # A$AP Rocky
    (60, 70, "Wild for the Night", "song", 2013),
    (60, 207, "Shabba", "song", 2013),
    (60, 206, "Ride (Live)", "live", 2013),

    # Metro Boomin
    (61, 9, "Creepin'", "song", 2022),
    (61, 30, "Savage Mode II", "album", 2020),
    (61, 85, "Space Cadet", "song", 2019),

    # Young Thug hub
    (84, 85, "Drip or Drown 2", "album", 2019),
    (84, 82, "Got the Guap", "song", 2018),
    (84, 52, "No Limit", "song", 2016),
    (84, 86, "Bad Boy", "song", 2020),

    # Lil Baby hub
    (86, 85, "Drip Too Hard", "song", 2018),
    (86, 62, "What's Poppin (Remix)", "song", 2020),
    (86, 88, "Baby", "song", 2020),

    # Roddy Ricch + DaBaby
    (87, 88, "ROCKSTAR", "song", 2020),
    (88, 86, "Baby", "song", 2020),

    # Migos / Offset / Quavo
    (89, 92, "Culture III", "album", 2021),
    (89, 93, "Culture III", "album", 2021),
    (92, 93, "Culture", "album", 2017),

    # Daft Punk
    (94, 31, "Get Lucky", "song", 2013),
    (94, 95, "Homework (Live)", "live", 2007),
    (94, 55, "Something About Us (Live)", "live", 2001),

    # Gorillaz
    (95, 74, "Humility (Live)", "live", 2018),
    (95, 32, "Plastic Beach", "album", 2010),
    (95, 137, "Music Is My Radar (Live)", "live", 2000),
    (95, 203, "Do Ya Thing", "song", 2012),

    # Bon Iver
    (96, 97, "Fall Creek Boys Choir", "song", 2011),
    (96, 97, "I Need a Forest Fire", "song", 2016),

    # James Blake
    (97, 60, "Hindsight", "song", 2016),
    (97, 185, "Take Me (Live)", "live", 2016),

    # Rosalía hub
    (98, 99, "Con Altura", "song", 2019),
    (98, 100, "Yo x Ti, Tu x Mi", "song", 2019),
    (98, 104, "Linda (Live)", "live", 2023),
    (98, 105, "Beso", "song", 2023),

    # J Balvin
    (99, 100, "Reggaeton Lento (Remix)", "song", 2017),
    (99, 101, "Machika", "song", 2018),
    (99, 102, "Que Pena", "song", 2019),

    # Latin connections
    (100, 101, "La Rompe Corazones", "song", 2017),
    (100, 103, "China", "song", 2019),
    (101, 120, "Con Calma (Remix)", "song", 2019),
    (101, 32, "Gangnam Style (Live Remix)", "live", 2017),
    (102, 37, "Clandestino", "song", 2018),
    (102, 139, "Medellín (Concept)", "live", 2019),
    (103, 108, "Bubble Gum", "song", 2018),
    (104, 108, "2 AM (Live)", "live", 2023),
    (105, 107, "Feliz Cumpleaños Ferxxo", "song", 2022),
    (106, 16, "MONACO", "song", 2023),
    (107, 108, "Polaris", "song", 2023),
    (109, 120, "Sin Pijama", "song", 2018),
    (109, 38, "Superhéroe", "song", 2019),
    (110, 101, "Dura (Remix)", "song", 2018),
    (110, 100, "Criminal", "song", 2017),
    (111, 112, "Wisin & Yandel", "album", 2004),
    (111, 113, "Salio el Sol", "song", 2009),
    (112, 113, "Reggaeton (Live)", "live", 2005),
    (113, 101, "Taboo", "song", 2007),
    (114, 113, "Los Bandoleros", "song", 2005),
    (115, 120, "Si Me Dices Que Sí", "song", 2020),
    (116, 100, "Otro Trago", "song", 2019),
    (117, 16, "Dákiti", "song", 2020),
    (118, 119, "La Movie", "song", 2018),
    (118, 103, "Me ArrepentÍ", "song", 2019),
    (119, 120, "La Formula (Live)", "live", 2012),
    (120, 113, "Travesuras (Remix)", "song", 2014),

    # Rock connections
    (121, 14, "Take What You Want", "song", 2019),
    (123, 14, "Lux Aeterna (Live)", "live", 2023),
    (124, 192, "Foo Fighters Band", "album", 2011),
    (126, 4, "Numb/Encore", "song", 2004),
    (126, 127, "Rock the Rhine (Live)", "live", 2005),
    (127, 191, "Green Day Band", "album", 1994),
    (128, 64, "Tour Performance (Live)", "live", 2023),
    (128, 79, "Nightmare (Live)", "live", 2018),
    (129, 130, "Emo Nite (Live)", "live", 2016),
    (129, 128, "Tour (Live)", "live", 2014),
    (130, 129, "Sugar We're Goin Down (Live)", "live", 2017),
    (131, 78, "Festival Performance (Live)", "live", 2019),
    (131, 41, "Radioactive (Live)", "live", 2018),
    (132, 133, "Currents (Influenced)", "song", 2015),
    (133, 175, "Higher Ground (Live)", "live", 2019),
    (133, 13, "Skeletons", "song", 2018),
    (134, 188, "Oxford Bands (Live)", "live", 2010),

    # Pop/R&B connections
    (139, 12, "Bitch I'm Madonna", "song", 2015),
    (139, 142, "Lady Marmalade", "song", 2001),
    (140, 55, "Scream", "song", 1995),
    (141, 4, "Heartbreaker", "song", 1999),
    (141, 142, "Lady Marmalade", "song", 2001),
    (141, 199, "Killing Me Softly (Live)", "live", 1998),
    (142, 11, "Fall in Line", "song", 2018),
    (142, 149, "Just a Fool", "song", 2012),
    (143, 90, "After Party (Live)", "live", 2018),
    (143, 144, "Cry Me a River", "song", 2002),
    (143, 79, "Grammys Performance", "live", 2022),
    (144, 145, "One Minute Man", "song", 2001),
    (144, 200, "If I Ruled the World (Remix)", "song", 2001),
    (144, 4, "Dirt Off Your Shoulder", "song", 2003),
    (145, 146, "Why You Treat Me So Bad (Live)", "live", 2003),
    (145, 12, "Pound the Alarm (Live)", "live", 2014),
    (146, 6, "Calm Down", "song", 2000),
    (147, 23, "Got Money", "song", 2008),
    (147, 43, "Moves Like Jagger (Live)", "live", 2012),
    (147, 52, "My Place (Live)", "live", 2008),
    (148, 34, "Locked Up (Remix)", "song", 2004),
    (148, 11, "Baby (Remix)", "song", 2010),
    (149, 12, "Miss Independent (Live)", "live", 2010),
    (149, 142, "Just a Fool", "song", 2012),
    (150, 12, "Bottoms Up", "song", 2010),
    (151, 5, "Single Ladies (Writer)", "song", 2008),
    (152, 1, "Finesse", "song", 2016),
    (152, 9, "Rambo (Remix)", "song", 2015),
    (153, 29, "East Atlanta Love Letter", "song", 2018),
    (153, 35, "Better", "song", 2018),
    (154, 21, "No Love (Live Duet)", "live", 2023),
    (154, 52, "Come Thru", "song", 2019),
    (155, 10, "Safety Net", "song", 2020),
    (155, 26, "On My Way (Live)", "live", 2022),
    (155, 156, "Best Part", "song", 2017),
    (156, 35, "Best Part", "song", 2017),
    (156, 157, "Love Again (Live)", "live", 2021),
    (157, 11, "Peaches", "song", 2021),
    (157, 1, "Chicago Freestyle", "song", 2020),
    (158, 13, "Crew (Live)", "live", 2020),
    (158, 59, "Running Man (Live)", "live", 2020),
    (159, 26, "Pretty Little Birds", "song", 2018),
    (160, 1, "From Time", "song", 2013),
    (160, 75, "Wedding (Live)", "live", 2016),
    (161, 29, "Jealous (Live)", "live", 2017),
    (162, 90, "Nights Like This", "song", 2019),
    (162, 11, "Get Me (Live)", "live", 2020),

    # Afrobeats connections
    (163, 164, "Water", "song", 2023),
    (163, 13, "Water (Remix)", "song", 2023),
    (164, 165, "Ginger", "song", 2020),
    (164, 7, "For My Hand", "song", 2022),
    (164, 21, "Onyeka (Live)", "live", 2023),
    (164, 42, "Hymn for the Weekend (Live)", "live", 2022),
    (165, 1, "Come Closer", "song", 2017),
    (165, 168, "Essence", "song", 2020),
    (165, 11, "Essence (Remix)", "song", 2021),
    (166, 24, "Blow My Mind", "song", 2019),
    (166, 48, "Wrecking Ball (Live Remix)", "live", 2020),
    (167, 46, "Calm Down (Remix)", "song", 2022),
    (167, 166, "E Choke (Live)", "live", 2021),
    (168, 165, "Essence", "song", 2020),
    (168, 1, "Fountains", "song", 2021),
    (168, 164, "Coming Home (Live)", "live", 2022),
    (169, 170, "Sability (Live)", "live", 2023),
    (170, 164, "Yoga (Live)", "live", 2023),
    (171, 46, "Love Nwantiti (Live Remix)", "live", 2021),

    # EDM connections
    (172, 43, "Way to Go (Live)", "live", 2015),
    (172, 147, "Neon (Live)", "live", 2020),
    (173, 44, "Boy With Luv (Remix)", "song", 2019),
    (173, 15, "Scared to Be Lonely", "song", 2017),
    (173, 64, "Watermelon Sugar (Remix)", "song", 2020),
    (174, 46, "I Want You to Know", "song", 2015),
    (174, 36, "Latch", "song", 2012),
    (174, 57, "Hello (Remix Live)", "live", 2016),
    (175, 143, "Suit & Tie (Live)", "live", 2016),
    (175, 49, "First Time", "song", 2018),
    (175, 133, "Higher Ground (Live)", "live", 2019),
    (176, 142, "Levels (Live)", "live", 2012),
    (176, 48, "Party in the USA (Live Remix)", "live", 2014),
    (177, 42, "Summer (Live)", "live", 2014),
    (177, 9, "Moth to a Flame", "song", 2021),
    (178, 36, "Latch", "song", 2012),
    (178, 182, "Magnets", "song", 2015),
    (179, 182, "Say It", "song", 2016),
    (180, 173, "Festival Set (Live)", "live", 2019),
    (180, 175, "Light (Live)", "live", 2018),

    # Indie/Alt connections
    (181, 78, "Festival (Live)", "live", 2021),
    (182, 178, "Magnets", "song", 2015),
    (183, 17, "Guess (Remix)", "song", 2024),
    (183, 90, "Babygirl", "song", 2017),
    (183, 15, "Levitating (feat. Madonna & Missy Elliott)", "song", 2020),
    (184, 9, "Lust for Life", "song", 2017),
    (184, 189, "Big God (Live Performance)", "live", 2019),
    (184, 220, "Bad Habit (Live Mashup)", "live", 2024),
    (185, 97, "Take Me (Live)", "live", 2016),
    (186, 60, "Venus Fly", "song", 2015),
    (187, 8, "Nothing New", "song", 2021),
    (187, 194, "Punisher (Live)", "live", 2021),
    (188, 134, "In Rainbows (Live Crossover)", "live", 2012),
    (189, 184, "Big God (Live Performance)", "live", 2019),
    (189, 42, "Fix You (Live)", "live", 2016),
    (190, 64, "Cherry (Live)", "live", 2023),
    (190, 57, "Rolling in the Deep (Live Duet)", "live", 2023),

    # Classic R&B/Hip-Hop
    (195, 31, "Q.U.E.E.N.", "song", 2013),
    (195, 203, "Pink Matter (Live)", "live", 2015),
    (196, 5, "Cranes in the Sky (Live)", "live", 2017),
    (196, 197, "All I Could Do Was Cry (Live)", "live", 2017),
    (197, 74, "Come Down (Live)", "live", 2016),
    (197, 203, "Andre 3000 & Erykah Badu Duet (Live)", "live", 2000),
    (198, 199, "Nothing Even Matters", "song", 1998),
    (198, 74, "Silk Sonic Tribute (Live)", "live", 2022),
    (199, 3, "All Falls Down (Influence)", "song", 2004),
    (199, 200, "If I Ruled the World", "song", 1996),
    (200, 201, "Verbal Intercourse", "song", 1995),
    (200, 26, "Let Nas Down", "song", 2013),
    (200, 6, "The Cross", "song", 2003),
    (201, 200, "Verbal Intercourse", "song", 1995),
    (202, 203, "OutKast", "album", 1994),
    (202, 204, "OutKast", "album", 1994),
    (203, 204, "OutKast", "album", 1994),
    (203, 3, "Flashing Lights (Live)", "live", 2008),
    (203, 13, "Caroline (Live)", "live", 2019),
    (203, 195, "Pink Matter (Live)", "live", 2015),
    (204, 202, "Speakerboxxx / The Love Below", "album", 2003),

    # Pusha T / Kid Cudi
    (205, 3, "Runaway", "song", 2010),
    (205, 20, "Nosetalgia", "song", 2013),
    (206, 3, "Father Stretch My Hands", "song", 2016),
    (206, 13, "Through the Late Night", "song", 2016),
    (206, 60, "Ride (Live)", "live", 2013),

    # Newer Hip-Hop
    (207, 60, "Shabba", "song", 2013),
    (208, 20, "Collard Greens", "song", 2014),
    (208, 13, "Studio (Live)", "live", 2014),
    (209, 20, "Terrorist Threats", "song", 2012),
    (210, 26, "Wat's Wrong", "song", 2016),
    (210, 21, "Headshots (Live)", "live", 2021),
    (211, 20, "Family Ties", "song", 2021),
    (211, 26, "Off Deez", "song", 2019),
    (211, 212, "JID & Earthgang (Spillage Village)", "album", 2016),
    (212, 26, "a lot (Live)", "live", 2020),
    (213, 211, "Bruuuh", "song", 2019),
    (213, 59, "RICKY (Live)", "live", 2019),
    (213, 83, "Ultimate (Remix)", "song", 2016),
    (214, 28, "ARM & LEG (Live)", "live", 2022),
    (215, 22, "Doja Cat & Ice Spice (Live)", "live", 2023),
    (215, 8, "Karma (Live Remix)", "live", 2024),
    (215, 25, "TMZ (Live)", "live", 2024),
    (216, 25, "Tomorrow 2 (Live)", "live", 2023),
    (216, 28, "WAP (Live Mashup)", "live", 2023),
    (218, 43, "Big Energy (Remix)", "song", 2022),
    (218, 25, "Tomorrow 2", "song", 2022),

    # Pop connections
    (220, 62, "Lie to Girls (Live)", "live", 2024),
    (220, 8, "Espresso Duet (Live)", "live", 2024),
    (220, 64, "Grammys Duet (Live)", "live", 2024),

    # Diplo / Major Lazer / Skrillex
    (71, 72, "Major Lazer Project", "album", 2015),
    (71, 70, "Jack Ü", "album", 2015),
    (72, 39, "Lean On", "song", 2015),
    (70, 60, "Wild for the Night", "song", 2013),

    # David Guetta
    (69, 12, "Turn Me On", "song", 2011),
    (69, 49, "Titanium", "song", 2011),
    (69, 51, "Blinding Lights (Remix)", "song", 2020),
    (69, 6, "Not Afraid of the Dark", "song", 2011),

    # Extra cross-genre links
    (63, 64, "Juice (Live Duet)", "live", 2020),
    (63, 48, "Flowers (Live Duet)", "live", 2023),
    (64, 190, "Cherry (Live)", "live", 2023),
    (64, 128, "Tour Performance (Live)", "live", 2023),
    (64, 220, "Grammys Duet (Live)", "live", 2024),
    (64, 63, "Juice (Live Duet)", "live", 2020),
    (65, 8, "Déjà Vu (Influence)", "song", 2021),
    (65, 42, "Band Aid (Live)", "live", 2022),
    (65, 17, "Happier Than Ever (Live Mashup)", "live", 2022),

    # Anderson .Paak / Mac Miller
    (74, 75, "Dang!", "song", 2016),
    (74, 95, "Humility (Live)", "live", 2018),
    (75, 21, "Cinderella (Live Duet)", "live", 2016),
    (75, 59, "OK (Live)", "live", 2015),
    (75, 1, "Congratulations (Live)", "live", 2018),
    (75, 160, "Wedding (Live)", "live", 2016),

    # Halsey / Juice WRLD / Chainsmokers
    (79, 66, "Closer", "song", 2016),
    (79, 80, "Life's a Mess", "song", 2020),
    (80, 29, "WRLD on Drugs", "album", 2018),
    (80, 13, "No Bystanders", "song", 2018),

    # Chance the Rapper
    (76, 11, "Confident (Remix)", "song", 2017),
    (76, 73, "They Don't Like Me", "song", 2013),

    # Ty Dolla $ign
    (90, 3, "Vultures", "album", 2024),
    (90, 14, "Psycho", "song", 2018),
    (90, 84, "Expensive (Live)", "live", 2018),

    # Swae Lee
    (91, 14, "Sunflower", "song", 2018),
    (91, 89, "Culture III", "album", 2021),
    (91, 175, "Arms Around You (Live)", "live", 2019),

    # Lorde / The 1975
    (77, 42, "Yellow (Live Tribute)", "live", 2017),
    (77, 178, "Disclosure (Live)", "live", 2017),
    (78, 131, "Festival Performance (Live)", "live", 2019),
    (78, 182, "Give Yourself a Try (Remix)", "song", 2018),
    (78, 132, "505 (Live Cover)", "live", 2019),
]


async def seed():
    print("Dropping existing collections...")
    await db.artists.drop()
    await db.collaborations.drop()

    # Map temp IDs to real UUIDs
    id_map = {}
    artist_docs = []
    for temp_id, name, genre in ARTISTS_RAW:
        real_id = uid()
        id_map[temp_id] = real_id
        artist_docs.append({
            "id": real_id,
            "name": name,
            "genre": genre,
            "imageUrl": "",
        })

    print(f"Inserting {len(artist_docs)} artists...")
    if artist_docs:
        await db.artists.insert_many(artist_docs)

    # Create collaborations
    collab_docs = []
    seen = set()
    for a1, a2, title, ctype, year in COLLABS_RAW:
        if a1 not in id_map or a2 not in id_map:
            continue
        key = (min(a1, a2), max(a1, a2), title, year)
        if key in seen:
            continue
        seen.add(key)
        collab_docs.append({
            "id": uid(),
            "artistIds": [id_map[a1], id_map[a2]],
            "title": title,
            "type": ctype,
            "year": year,
        })

    print(f"Inserting {len(collab_docs)} collaborations...")
    if collab_docs:
        await db.collaborations.insert_many(collab_docs)

    # Create indexes
    print("Creating indexes...")
    await db.artists.create_index("id", unique=True)
    await db.artists.create_index([("name", "text")])
    await db.collaborations.create_index("id", unique=True)
    await db.collaborations.create_index("artistIds")

    print("Seed complete!")
    print(f"  Artists: {len(artist_docs)}")
    print(f"  Collaborations: {len(collab_docs)}")


if __name__ == "__main__":
    asyncio.run(seed())
