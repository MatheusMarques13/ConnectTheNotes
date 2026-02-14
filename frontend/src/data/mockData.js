// Massive archive of musical artists and their collaborations
// Each artist has: id, name, image (placeholder), genre
// Each collaboration has: artists involved, title, type (song/album/live/feature), year

const ARTISTS = [
  { id: 1, name: "Drake", genre: "Hip-Hop/R&B", image: "https://i.scdn.co/image/ab6761610000e5eb4293385d429161f6a1b532a2" },
  { id: 2, name: "Rihanna", genre: "Pop/R&B", image: "https://i.scdn.co/image/ab6761610000e5eb99e4fca7c0b7cb166d915789" },
  { id: 3, name: "Kanye West", genre: "Hip-Hop", image: "https://i.scdn.co/image/ab6761610000e5eb6e835a500e791bf9c27f4ef4" },
  { id: 4, name: "Jay-Z", genre: "Hip-Hop", image: "https://i.scdn.co/image/ab6761610000e5eb05079e11031490e824aecc52" },
  { id: 5, name: "Beyoncé", genre: "Pop/R&B", image: "https://i.scdn.co/image/ab6761610000e5eb12e3f20d05a8d838de5b5e4c" },
  { id: 6, name: "Eminem", genre: "Hip-Hop", image: "https://i.scdn.co/image/ab6761610000e5eba00b11c129f27a88fc72f36b" },
  { id: 7, name: "Ed Sheeran", genre: "Pop", image: "https://i.scdn.co/image/ab6761610000e5eb3bcef85e105dfc42399ef0ba" },
  { id: 8, name: "Taylor Swift", genre: "Pop/Country", image: "https://i.scdn.co/image/ab6761610000e5eb859e4c14fa59296c8649e0e4" },
  { id: 9, name: "The Weeknd", genre: "R&B/Pop", image: "https://i.scdn.co/image/ab6761610000e5eb214f3cf1cbe7139c1e26571c" },
  { id: 10, name: "Ariana Grande", genre: "Pop/R&B", image: "https://i.scdn.co/image/ab6761610000e5ebcdce7620dc940db079c4e508" },
  { id: 11, name: "Justin Bieber", genre: "Pop/R&B", image: "https://i.scdn.co/image/ab6761610000e5eb8ae7f2aaa9817a704a87ea36" },
  { id: 12, name: "Nicki Minaj", genre: "Hip-Hop/Pop", image: "https://i.scdn.co/image/ab6761610000e5eb42cba4858e42tried28bc0e05" },
  { id: 13, name: "Travis Scott", genre: "Hip-Hop", image: "https://i.scdn.co/image/ab6761610000e5eb19c2790744c792d05570bb71" },
  { id: 14, name: "Post Malone", genre: "Hip-Hop/Pop", image: "https://i.scdn.co/image/ab6761610000e5ebf1be22786da29b0a1284c0a5" },
  { id: 15, name: "Dua Lipa", genre: "Pop/Dance", image: "https://i.scdn.co/image/ab6761610000e5eb1bbee4a01dbd58ab4a4ee692" },
  { id: 16, name: "Bad Bunny", genre: "Reggaeton/Latin", image: "https://i.scdn.co/image/ab6761610000e5eb81845df0cffd53bcfa973767" },
  { id: 17, name: "Billie Eilish", genre: "Pop/Alternative", image: "https://i.scdn.co/image/ab6761610000e5ebd8b9980db67272cb4d2c3daf" },
  { id: 18, name: "Bruno Mars", genre: "Pop/R&B", image: "https://i.scdn.co/image/ab6761610000e5ebc36dd9eb55fb0db4911f25dd" },
  { id: 19, name: "Lady Gaga", genre: "Pop", image: "https://i.scdn.co/image/ab6761610000e5ebc8d3d98a1bccbe71393dbfbf" },
  { id: 20, name: "Kendrick Lamar", genre: "Hip-Hop", image: "https://i.scdn.co/image/ab6761610000e5eb437b9e2a82505b3d93ff1022" },
  { id: 21, name: "SZA", genre: "R&B", image: "https://i.scdn.co/image/ab6761610000e5eb7eb79c1386d798f29b13496f" },
  { id: 22, name: "Doja Cat", genre: "Pop/Hip-Hop", image: "https://i.scdn.co/image/ab6761610000e5ebe94f88ff74ae4ef2b6eb394b" },
  { id: 23, name: "Lil Wayne", genre: "Hip-Hop", image: "https://i.scdn.co/image/ab6761610000e5eb9a398209a4ef3360dce2dec4" },
  { id: 24, name: "Chris Brown", genre: "R&B/Pop", image: "https://i.scdn.co/image/ab6761610000e5eb1d97a3c3f2694a3c1cf4e4b8" },
  { id: 25, name: "Cardi B", genre: "Hip-Hop", image: "https://i.scdn.co/image/ab6761610000e5eb4d3259823e4a2ff6tried7fd8" },
  { id: 26, name: "J. Cole", genre: "Hip-Hop", image: "https://i.scdn.co/image/ab6761610000e5ebadd503b411a712e277895c8a" },
  { id: 27, name: "Lil Nas X", genre: "Pop/Hip-Hop", image: "https://i.scdn.co/image/ab6761610000e5eb989ed05e1f0570cc4726c2d3" },
  { id: 28, name: "Megan Thee Stallion", genre: "Hip-Hop", image: "https://i.scdn.co/image/ab6761610000e5eb4521e58e39a6a4b4e7e1f8de" },
  { id: 29, name: "Future", genre: "Hip-Hop", image: "https://i.scdn.co/image/ab6761610000e5eb5cf37b9a6b4f9a2b2d5a8c11" },
  { id: 30, name: "21 Savage", genre: "Hip-Hop", image: "https://i.scdn.co/image/ab6761610000e5eb4f8b618c4325c55aaedbc3df" },
  { id: 31, name: "Pharrell Williams", genre: "Pop/Hip-Hop", image: "https://i.scdn.co/image/ab6761610000e5eb07a50f0a9a8f6ccf7ada94ab" },
  { id: 32, name: "Snoop Dogg", genre: "Hip-Hop", image: "https://i.scdn.co/image/ab6761610000e5eb9a1e9e3a2b7a8f46e1e0f2da" },
  { id: 33, name: "Dr. Dre", genre: "Hip-Hop", image: "https://i.scdn.co/image/ab6761610000e5eb41632c81876dc4a1e6c7b66a" },
  { id: 34, name: "50 Cent", genre: "Hip-Hop", image: "https://i.scdn.co/image/ab6761610000e5ebfb97f168bf40d7268df2a99c" },
  { id: 35, name: "Khalid", genre: "R&B/Pop", image: "https://i.scdn.co/image/ab6761610000e5eb31072db9da0311ecb4e4b5c7" },
  { id: 36, name: "Sam Smith", genre: "Pop/R&B", image: "https://i.scdn.co/image/ab6761610000e5eb0d35db tried7d4b9f4b8e6c3bd" },
  { id: 37, name: "Shakira", genre: "Latin Pop", image: "https://i.scdn.co/image/ab6761610000e5eb284894d68fe2f80cad555110" },
  { id: 38, name: "Pitbull", genre: "Latin Pop/Hip-Hop", image: "https://i.scdn.co/image/ab6761610000e5eb0e2a618e8c6d09a7ed5a9c6f" },
  { id: 39, name: "DJ Khaled", genre: "Hip-Hop/DJ", image: "https://i.scdn.co/image/ab6761610000e5eb42c9c7ab3e92b7b1a73d3b05" },
  { id: 40, name: "Wiz Khalifa", genre: "Hip-Hop", image: "https://i.scdn.co/image/ab6761610000e5eb5e4698a0547fbed9e8f5e0b4" },
  { id: 41, name: "Imagine Dragons", genre: "Rock/Pop", image: "https://i.scdn.co/image/ab6761610000e5eb920dc1f617550de8388f368e" },
  { id: 42, name: "Coldplay", genre: "Rock/Pop", image: "https://i.scdn.co/image/ab6761610000e5eb989ed05e1f0570cc4726c2d3" },
  { id: 43, name: "Maroon 5", genre: "Pop Rock", image: "https://i.scdn.co/image/ab6761610000e5ebf8349dfb6a264e88d697b37e" },
  { id: 44, name: "BTS", genre: "K-Pop", image: "https://i.scdn.co/image/ab6761610000e5ebd642648235ebf3460d2d1f34" },
  { id: 45, name: "BLACKPINK", genre: "K-Pop", image: "https://i.scdn.co/image/ab6761610000e5ebc9690bc711d04b3d4fd4b87c" },
  { id: 46, name: "Selena Gomez", genre: "Pop", image: "https://i.scdn.co/image/ab6761610000e5eb53c3bbb2789b6e02ae0c868e" },
  { id: 47, name: "Charlie Puth", genre: "Pop", image: "https://i.scdn.co/image/ab6761610000e5ebbcb32e18e2e6b9f2a1ea4ff7" },
  { id: 48, name: "Miley Cyrus", genre: "Pop/Rock", image: "https://i.scdn.co/image/ab6761610000e5eb55e8a6235c3945e12e2141bb" },
  { id: 49, name: "Sia", genre: "Pop", image: "https://i.scdn.co/image/ab6761610000e5ebb8a83dd1aa78a06tried7b4a8" },
  { id: 50, name: "John Legend", genre: "R&B/Soul", image: "https://i.scdn.co/image/ab6761610000e5eb94d2750eee2e66b2dad3f3d7" },
  { id: 51, name: "Alicia Keys", genre: "R&B/Soul", image: "https://i.scdn.co/image/ab6761610000e5eb7e8ddeb13fe6c45e2f3a9eb5" },
  { id: 52, name: "Usher", genre: "R&B/Pop", image: "https://i.scdn.co/image/ab6761610000e5eb625a32e6c5a6d87tried4e5a8" },
  { id: 53, name: "Elton John", genre: "Pop/Rock", image: "https://i.scdn.co/image/ab6761610000e5eb0a7388b95df960b5c0da8970" },
  { id: 54, name: "Stevie Wonder", genre: "R&B/Soul", image: "https://i.scdn.co/image/ab6761610000e5eb97b05e47eb0f2d4b4c3f7e8a" },
  { id: 55, name: "Michael Jackson", genre: "Pop", image: "https://i.scdn.co/image/ab6761610000e5eb5ef4b0c5b8bbe788d8d0a3f8" },
  { id: 56, name: "Whitney Houston", genre: "Pop/R&B", image: "https://i.scdn.co/image/ab6761610000e5eb7f8b74b3b0e6a2c1d8f4e6a2" },
  { id: 57, name: "Adele", genre: "Pop/Soul", image: "https://i.scdn.co/image/ab6761610000e5eb68f6e5892075d7f22615bd17" },
  { id: 58, name: "Frank Ocean", genre: "R&B/Alternative", image: "https://i.scdn.co/image/ab6761610000e5eb5ef4b0c5b8bbe788d8d0a3f8" },
  { id: 59, name: "Tyler, The Creator", genre: "Hip-Hop/Alternative", image: "https://i.scdn.co/image/ab6761610000e5eb8278b782cbb5a3963db88ada" },
  { id: 60, name: "A$AP Rocky", genre: "Hip-Hop", image: "https://i.scdn.co/image/ab6761610000e5eb5ea029d1f3b7e4d52de tried05" },
  { id: 61, name: "Metro Boomin", genre: "Hip-Hop/Producer", image: "https://i.scdn.co/image/ab6761610000e5eb5ef4b0c5b8bbe788d8d0a3f8" },
  { id: 62, name: "Jack Harlow", genre: "Hip-Hop", image: "https://i.scdn.co/image/ab6761610000e5eb625a32e6c5a6d874d4e5a823" },
  { id: 63, name: "Lizzo", genre: "Pop/Hip-Hop", image: "https://i.scdn.co/image/ab6761610000e5eb0c68f0e7155b4f8c3a3d70dc" },
  { id: 64, name: "Harry Styles", genre: "Pop/Rock", image: "https://i.scdn.co/image/ab6761610000e5ebf7db7c8eded1ffa37da8b2c1" },
  { id: 65, name: "Olivia Rodrigo", genre: "Pop/Rock", image: "https://i.scdn.co/image/ab6761610000e5ebe03a98785f3658f0b6461ec4" },
  { id: 66, name: "The Chainsmokers", genre: "EDM/Pop", image: "https://i.scdn.co/image/ab6761610000e5eb1ba8fc5f5c73e7e9313cc6eb" },
  { id: 67, name: "Marshmello", genre: "EDM", image: "https://i.scdn.co/image/ab6761610000e5ebb00fbf613ee5a7998a2af7e8" },
  { id: 68, name: "Calvin Harris", genre: "EDM/Pop", image: "https://i.scdn.co/image/ab6761610000e5eb1be22886b0b9e1c5e6e73eba" },
  { id: 69, name: "David Guetta", genre: "EDM/Pop", image: "https://i.scdn.co/image/ab6761610000e5eba5579a06da6b7c63e7b48b41" },
  { id: 70, name: "Skrillex", genre: "EDM/Dubstep", image: "https://i.scdn.co/image/ab6761610000e5eb625a32e6c5a6d874d4e5a823" },
  { id: 71, name: "Diplo", genre: "EDM", image: "https://i.scdn.co/image/ab6761610000e5eb625a32e6c5a6d874d4e5a823" },
  { id: 72, name: "Major Lazer", genre: "EDM/Dancehall", image: "https://i.scdn.co/image/ab6761610000e5eb625a32e6c5a6d874d4e5a823" },
  { id: 73, name: "Childish Gambino", genre: "Hip-Hop/R&B", image: "https://i.scdn.co/image/ab6761610000e5eb3ef786b1a1e01665e13b1cae" },
  { id: 74, name: "Anderson .Paak", genre: "R&B/Hip-Hop", image: "https://i.scdn.co/image/ab6761610000e5eb2c78d93ee5b3f1b3e4c1d3f8" },
  { id: 75, name: "Mac Miller", genre: "Hip-Hop", image: "https://i.scdn.co/image/ab6761610000e5eb625a32e6c5a6d874d4e5a823" },
  { id: 76, name: "Chance the Rapper", genre: "Hip-Hop", image: "https://i.scdn.co/image/ab6761610000e5eb5ef4b0c5b8bbe788d8d0a3f8" },
  { id: 77, name: "Lorde", genre: "Pop/Alternative", image: "https://i.scdn.co/image/ab6761610000e5eb625a32e6c5a6d874d4e5a823" },
  { id: 78, name: "The 1975", genre: "Pop Rock", image: "https://i.scdn.co/image/ab6761610000e5eb625a32e6c5a6d874d4e5a823" },
  { id: 79, name: "Halsey", genre: "Pop/Alternative", image: "https://i.scdn.co/image/ab6761610000e5eb625a32e6c5a6d874d4e5a823" },
  { id: 80, name: "Juice WRLD", genre: "Hip-Hop/Emo Rap", image: "https://i.scdn.co/image/ab6761610000e5eb625a32e6c5a6d874d4e5a823" },
  { id: 81, name: "XXXTentacion", genre: "Hip-Hop", image: "https://i.scdn.co/image/ab6761610000e5eb625a32e6c5a6d874d4e5a823" },
  { id: 82, name: "Lil Uzi Vert", genre: "Hip-Hop", image: "https://i.scdn.co/image/ab6761610000e5eb625a32e6c5a6d874d4e5a823" },
  { id: 83, name: "Playboi Carti", genre: "Hip-Hop", image: "https://i.scdn.co/image/ab6761610000e5eb625a32e6c5a6d874d4e5a823" },
  { id: 84, name: "Young Thug", genre: "Hip-Hop", image: "https://i.scdn.co/image/ab6761610000e5eb625a32e6c5a6d874d4e5a823" },
  { id: 85, name: "Gunna", genre: "Hip-Hop", image: "https://i.scdn.co/image/ab6761610000e5eb625a32e6c5a6d874d4e5a823" },
  { id: 86, name: "Lil Baby", genre: "Hip-Hop", image: "https://i.scdn.co/image/ab6761610000e5eb625a32e6c5a6d874d4e5a823" },
  { id: 87, name: "Roddy Ricch", genre: "Hip-Hop", image: "https://i.scdn.co/image/ab6761610000e5eb625a32e6c5a6d874d4e5a823" },
  { id: 88, name: "DaBaby", genre: "Hip-Hop", image: "https://i.scdn.co/image/ab6761610000e5eb625a32e6c5a6d874d4e5a823" },
  { id: 89, name: "Migos", genre: "Hip-Hop", image: "https://i.scdn.co/image/ab6761610000e5eb625a32e6c5a6d874d4e5a823" },
  { id: 90, name: "Ty Dolla $ign", genre: "R&B/Hip-Hop", image: "https://i.scdn.co/image/ab6761610000e5eb625a32e6c5a6d874d4e5a823" },
  { id: 91, name: "Swae Lee", genre: "Hip-Hop/R&B", image: "https://i.scdn.co/image/ab6761610000e5eb625a32e6c5a6d874d4e5a823" },
  { id: 92, name: "Offset", genre: "Hip-Hop", image: "https://i.scdn.co/image/ab6761610000e5eb625a32e6c5a6d874d4e5a823" },
  { id: 93, name: "Quavo", genre: "Hip-Hop", image: "https://i.scdn.co/image/ab6761610000e5eb625a32e6c5a6d874d4e5a823" },
  { id: 94, name: "Daft Punk", genre: "Electronic", image: "https://i.scdn.co/image/ab6761610000e5eb625a32e6c5a6d874d4e5a823" },
  { id: 95, name: "Gorillaz", genre: "Alternative/Electronic", image: "https://i.scdn.co/image/ab6761610000e5eb625a32e6c5a6d874d4e5a823" },
  { id: 96, name: "Bon Iver", genre: "Indie/Alternative", image: "https://i.scdn.co/image/ab6761610000e5eb625a32e6c5a6d874d4e5a823" },
  { id: 97, name: "James Blake", genre: "Electronic/R&B", image: "https://i.scdn.co/image/ab6761610000e5eb625a32e6c5a6d874d4e5a823" },
  { id: 98, name: "Rosalía", genre: "Latin Pop/Flamenco", image: "https://i.scdn.co/image/ab6761610000e5eb625a32e6c5a6d874d4e5a823" },
  { id: 99, name: "J Balvin", genre: "Reggaeton", image: "https://i.scdn.co/image/ab6761610000e5eb625a32e6c5a6d874d4e5a823" },
  { id: 100, name: "Ozuna", genre: "Reggaeton/Latin", image: "https://i.scdn.co/image/ab6761610000e5eb625a32e6c5a6d874d4e5a823" },
];

// Collaborations - the connections between artists
// Each collaboration links artists by IDs
const COLLABORATIONS = [
  // Drake connections
  { id: 1, artistIds: [1, 2], title: "Work", type: "song", year: 2016 },
  { id: 2, artistIds: [1, 2], title: "Take Care", type: "song", year: 2011 },
  { id: 3, artistIds: [1, 3], title: "Forever", type: "song", year: 2009 },
  { id: 4, artistIds: [1, 6], title: "Forever", type: "song", year: 2009 },
  { id: 5, artistIds: [1, 29], title: "What a Time to Be Alive", type: "album", year: 2015 },
  { id: 6, artistIds: [1, 30], title: "Her Loss", type: "album", year: 2022 },
  { id: 7, artistIds: [1, 23], title: "The Motto", type: "song", year: 2011 },
  { id: 8, artistIds: [1, 11], title: "Right Here", type: "song", year: 2012 },
  { id: 9, artistIds: [1, 20], title: "Poetic Justice", type: "song", year: 2012 },
  { id: 10, artistIds: [1, 13], title: "SICKO MODE", type: "song", year: 2018 },
  { id: 11, artistIds: [1, 62], title: "Churchill Downs", type: "song", year: 2022 },
  { id: 12, artistIds: [1, 21], title: "Slime You Out", type: "song", year: 2023 },
  
  // Rihanna connections
  { id: 13, artistIds: [2, 3], title: "All of the Lights", type: "song", year: 2010 },
  { id: 14, artistIds: [2, 4], title: "Umbrella", type: "song", year: 2007 },
  { id: 15, artistIds: [2, 6], title: "Love the Way You Lie", type: "song", year: 2010 },
  { id: 16, artistIds: [2, 12], title: "Fly", type: "song", year: 2010 },
  { id: 17, artistIds: [2, 37], title: "Can't Remember to Forget You", type: "song", year: 2014 },
  { id: 18, artistIds: [2, 24], title: "Turn Up the Music (Remix)", type: "song", year: 2012 },
  { id: 19, artistIds: [2, 29], title: "Loveeeeeee Song", type: "song", year: 2012 },
  
  // Kanye West connections
  { id: 20, artistIds: [3, 4], title: "Watch the Throne", type: "album", year: 2011 },
  { id: 21, artistIds: [3, 20], title: "No More Parties in LA", type: "song", year: 2016 },
  { id: 22, artistIds: [3, 84], title: "Highlights", type: "song", year: 2016 },
  { id: 23, artistIds: [3, 26], title: "Looking for Trouble", type: "song", year: 2010 },
  { id: 24, artistIds: [3, 96], title: "Monster", type: "song", year: 2010 },
  { id: 25, artistIds: [3, 76], title: "Ultralight Beam", type: "song", year: 2016 },
  { id: 26, artistIds: [3, 31], title: "Number One", type: "song", year: 2007 },
  { id: 27, artistIds: [3, 90], title: "Vultures", type: "album", year: 2024 },
  { id: 28, artistIds: [3, 58], title: "New Slaves", type: "song", year: 2013 },
  { id: 29, artistIds: [3, 55], title: "Black Skinhead (Inspiration)", type: "song", year: 2013 },
  { id: 30, artistIds: [3, 23], title: "Lollipop (Remix)", type: "song", year: 2008 },
  
  // Jay-Z connections
  { id: 31, artistIds: [4, 5], title: "Everything Is Love", type: "album", year: 2018 },
  { id: 32, artistIds: [4, 5], title: "Crazy in Love", type: "song", year: 2003 },
  { id: 33, artistIds: [4, 6], title: "Renegade", type: "song", year: 2001 },
  { id: 34, artistIds: [4, 23], title: "Mr. Carter", type: "song", year: 2008 },
  { id: 35, artistIds: [4, 51], title: "Empire State of Mind", type: "song", year: 2009 },
  { id: 36, artistIds: [4, 31], title: "Frontin'", type: "song", year: 2003 },
  { id: 37, artistIds: [4, 50], title: "Déjà Vu", type: "song", year: 2006 },
  { id: 38, artistIds: [4, 20], title: "Bitch, Don't Kill My Vibe (Remix)", type: "song", year: 2013 },
  { id: 39, artistIds: [4, 29], title: "I Got the Keys", type: "song", year: 2016 },
  
  // Beyoncé connections
  { id: 40, artistIds: [5, 7], title: "Perfect Duet", type: "song", year: 2017 },
  { id: 41, artistIds: [5, 37], title: "Beautiful Liar", type: "song", year: 2007 },
  { id: 42, artistIds: [5, 20], title: "AMERICA HAS A PROBLEM (Remix)", type: "song", year: 2023 },
  { id: 43, artistIds: [5, 12], title: "Feeling Myself", type: "song", year: 2014 },
  { id: 44, artistIds: [5, 48], title: "II MOST WANTED", type: "song", year: 2024 },
  { id: 45, artistIds: [5, 14], title: "LEVII'S JEANS", type: "song", year: 2024 },
  
  // Eminem connections
  { id: 46, artistIds: [6, 33], title: "Forgot About Dre", type: "song", year: 1999 },
  { id: 47, artistIds: [6, 34], title: "Patiently Waiting", type: "song", year: 2003 },
  { id: 48, artistIds: [6, 50], title: "No Love", type: "song", year: 2010 },
  { id: 49, artistIds: [6, 32], title: "Bitch Please II", type: "song", year: 2000 },
  { id: 50, artistIds: [6, 80], title: "Godzilla", type: "song", year: 2020 },
  { id: 51, artistIds: [6, 7], title: "River", type: "song", year: 2017 },
  
  // Ed Sheeran connections
  { id: 52, artistIds: [7, 8], title: "Everything Has Changed", type: "song", year: 2012 },
  { id: 53, artistIds: [7, 11], title: "I Don't Care", type: "song", year: 2019 },
  { id: 54, artistIds: [7, 15], title: "Beautiful People", type: "song", year: 2019 },
  { id: 55, artistIds: [7, 35], title: "Beautiful People", type: "song", year: 2019 },
  { id: 56, artistIds: [7, 42], title: "Fix You (Live)", type: "live", year: 2021 },
  { id: 57, artistIds: [7, 47], title: "Cross Me", type: "song", year: 2019 },
  { id: 58, artistIds: [7, 44], title: "Permission to Dance", type: "song", year: 2021 },
  { id: 59, artistIds: [7, 18], title: "Blow", type: "song", year: 2019 },
  
  // Taylor Swift connections
  { id: 60, artistIds: [8, 96], title: "exile", type: "song", year: 2020 },
  { id: 61, artistIds: [8, 29], title: "End Game", type: "song", year: 2017 },
  { id: 62, artistIds: [8, 46], title: "Bad Blood (Remix)", type: "song", year: 2015 },
  { id: 63, artistIds: [8, 66], title: "Lover (Remix)", type: "song", year: 2019 },
  { id: 64, artistIds: [8, 77], title: "Royals (Live Duet)", type: "live", year: 2014 },
  { id: 65, artistIds: [8, 14], title: "Fortnight", type: "song", year: 2024 },
  { id: 66, artistIds: [8, 64], title: "Grammys Performance", type: "live", year: 2021 },
  
  // The Weeknd connections
  { id: 67, artistIds: [9, 10], title: "Love Me Harder", type: "song", year: 2014 },
  { id: 68, artistIds: [9, 1], title: "Crew Love", type: "song", year: 2011 },
  { id: 69, artistIds: [9, 3], title: "Tell Your Friends", type: "song", year: 2015 },
  { id: 70, artistIds: [9, 15], title: "Levitating (Remix)", type: "song", year: 2020 },
  { id: 71, artistIds: [9, 22], title: "You Right", type: "song", year: 2021 },
  { id: 72, artistIds: [9, 29], title: "Low Life", type: "song", year: 2016 },
  { id: 73, artistIds: [9, 94], title: "Starboy", type: "song", year: 2016 },
  { id: 74, artistIds: [9, 21], title: "Kiss Me More (Live)", type: "live", year: 2021 },
  
  // Ariana Grande connections
  { id: 75, artistIds: [10, 12], title: "Side to Side", type: "song", year: 2016 },
  { id: 76, artistIds: [10, 19], title: "Rain on Me", type: "song", year: 2020 },
  { id: 77, artistIds: [10, 11], title: "Stuck with U", type: "song", year: 2020 },
  { id: 78, artistIds: [10, 22], title: "34+35 (Remix)", type: "song", year: 2021 },
  { id: 79, artistIds: [10, 28], title: "34+35 (Remix)", type: "song", year: 2021 },
  { id: 80, artistIds: [10, 46], title: "Ice Cream (Live)", type: "live", year: 2020 },
  { id: 81, artistIds: [10, 9], title: "Save Your Tears (Remix)", type: "song", year: 2021 },
  
  // Justin Bieber connections
  { id: 82, artistIds: [11, 39], title: "I'm the One", type: "song", year: 2017 },
  { id: 83, artistIds: [11, 76], title: "Bad Boy", type: "song", year: 2013 },
  { id: 84, artistIds: [11, 13], title: "Second Emotion", type: "song", year: 2021 },
  { id: 85, artistIds: [11, 86], title: "Forever", type: "song", year: 2020 },
  { id: 86, artistIds: [11, 15], title: "One Kiss (Live)", type: "live", year: 2021 },
  { id: 87, artistIds: [11, 35], title: "As I Am", type: "song", year: 2021 },
  { id: 88, artistIds: [11, 24], title: "Next to You", type: "song", year: 2011 },
  
  // Nicki Minaj connections
  { id: 89, artistIds: [12, 23], title: "Truffle Butter", type: "song", year: 2014 },
  { id: 90, artistIds: [12, 29], title: "You da Baddest", type: "song", year: 2017 },
  { id: 91, artistIds: [12, 3], title: "Monster", type: "song", year: 2010 },
  
  // Travis Scott connections
  { id: 92, artistIds: [13, 3], title: "Watch", type: "song", year: 2018 },
  { id: 93, artistIds: [13, 29], title: "3500", type: "song", year: 2015 },
  { id: 94, artistIds: [13, 84], title: "FRANCHISE", type: "song", year: 2020 },
  { id: 95, artistIds: [13, 20], title: "goosebumps", type: "song", year: 2016 },
  { id: 96, artistIds: [13, 61], title: "Heroes & Villains", type: "album", year: 2022 },
  { id: 97, artistIds: [13, 9], title: "WAKE UP", type: "song", year: 2018 },
  
  // Post Malone connections
  { id: 98, artistIds: [14, 91], title: "Sunflower", type: "song", year: 2018 },
  { id: 99, artistIds: [14, 21], title: "Love Galore (Remix)", type: "song", year: 2017 },
  { id: 100, artistIds: [14, 22], title: "I Like You", type: "song", year: 2022 },
  { id: 101, artistIds: [14, 84], title: "Goodbyes", type: "song", year: 2019 },
  { id: 102, artistIds: [14, 40], title: "No Reason", type: "song", year: 2019 },
  { id: 103, artistIds: [14, 67], title: "Rockstar (Remix)", type: "song", year: 2017 },
  
  // Dua Lipa connections
  { id: 104, artistIds: [15, 16], title: "Levitating (Remix)", type: "song", year: 2020 },
  { id: 105, artistIds: [15, 53], title: "Cold Heart", type: "song", year: 2021 },
  { id: 106, artistIds: [15, 45], title: "Kiss and Make Up", type: "song", year: 2018 },
  { id: 107, artistIds: [15, 68], title: "One Kiss", type: "song", year: 2018 },
  { id: 108, artistIds: [15, 22], title: "Levitating (Live)", type: "live", year: 2021 },
  { id: 109, artistIds: [15, 28], title: "Sweetest Pie", type: "song", year: 2022 },
  { id: 110, artistIds: [15, 48], title: "Prisoner", type: "song", year: 2020 },
  
  // Bad Bunny connections
  { id: 111, artistIds: [16, 1], title: "MIA", type: "song", year: 2018 },
  { id: 112, artistIds: [16, 99], title: "OASIS", type: "album", year: 2019 },
  { id: 113, artistIds: [16, 25], title: "I Like It", type: "song", year: 2018 },
  { id: 114, artistIds: [16, 98], title: "La Noche de Anoche", type: "song", year: 2020 },
  { id: 115, artistIds: [16, 37], title: "TQG", type: "song", year: 2023 },
  
  // Bruno Mars connections
  { id: 116, artistIds: [18, 74], title: "Silk Sonic", type: "album", year: 2021 },
  { id: 117, artistIds: [18, 25], title: "Finesse (Remix)", type: "song", year: 2018 },
  { id: 118, artistIds: [18, 15], title: "Levitating (Remix Live)", type: "live", year: 2021 },
  { id: 119, artistIds: [18, 19], title: "Die With a Smile", type: "song", year: 2024 },
  { id: 120, artistIds: [18, 6], title: "Lighters", type: "song", year: 2011 },
  { id: 121, artistIds: [18, 22], title: "Kiss Me More (Live Performance)", type: "live", year: 2022 },
  
  // Lady Gaga connections
  { id: 122, artistIds: [19, 5], title: "Telephone", type: "song", year: 2010 },
  { id: 123, artistIds: [19, 53], title: "Sine from Above", type: "song", year: 2020 },
  { id: 124, artistIds: [19, 2], title: "Fashion!", type: "song", year: 2013 },
  
  // Kendrick Lamar connections
  { id: 125, artistIds: [20, 21], title: "All the Stars", type: "song", year: 2018 },
  { id: 126, artistIds: [20, 29], title: "King's Dead", type: "song", year: 2018 },
  { id: 127, artistIds: [20, 59], title: "HUMBLE (Live)", type: "live", year: 2017 },
  { id: 128, artistIds: [20, 61], title: "Like That", type: "song", year: 2024 },
  { id: 129, artistIds: [20, 86], title: "N95", type: "song", year: 2022 },
  { id: 130, artistIds: [20, 73], title: "Adorable (Live)", type: "live", year: 2018 },
  
  // SZA connections
  { id: 131, artistIds: [21, 1], title: "Slime You Out", type: "song", year: 2023 },
  { id: 132, artistIds: [21, 22], title: "Kiss Me More", type: "song", year: 2021 },
  { id: 133, artistIds: [21, 13], title: "Open Arms (feat. Travis Scott)", type: "song", year: 2022 },
  
  // Doja Cat connections
  { id: 134, artistIds: [22, 12], title: "Say So (Remix)", type: "song", year: 2020 },
  { id: 135, artistIds: [22, 28], title: "34+35 (Remix)", type: "song", year: 2021 },
  
  // Lil Wayne connections
  { id: 136, artistIds: [23, 29], title: "Love Me", type: "song", year: 2013 },
  { id: 137, artistIds: [23, 34], title: "Ayo Technology", type: "song", year: 2007 },
  { id: 138, artistIds: [23, 39], title: "I'm the One", type: "song", year: 2017 },
  
  // DJ Khaled connections
  { id: 139, artistIds: [39, 29], title: "I Got the Keys", type: "song", year: 2016 },
  { id: 140, artistIds: [39, 1], title: "POPSTAR", type: "song", year: 2020 },
  { id: 141, artistIds: [39, 5], title: "Shining", type: "song", year: 2017 },
  { id: 142, artistIds: [39, 23], title: "We Takin' Over", type: "song", year: 2007 },
  
  // Dr. Dre connections
  { id: 143, artistIds: [33, 32], title: "Still D.R.E.", type: "song", year: 1999 },
  { id: 144, artistIds: [33, 34], title: "In Da Club", type: "song", year: 2003 },
  { id: 145, artistIds: [33, 20], title: "Compton", type: "album", year: 2015 },
  
  // Calvin Harris connections
  { id: 146, artistIds: [68, 2], title: "We Found Love", type: "song", year: 2011 },
  { id: 147, artistIds: [68, 48], title: "Feels", type: "song", year: 2017 },
  { id: 148, artistIds: [68, 31], title: "Feels", type: "song", year: 2017 },
  { id: 149, artistIds: [68, 18], title: "Feels (Live)", type: "live", year: 2017 },
  
  // Marshmello connections
  { id: 150, artistIds: [67, 35], title: "Silence", type: "song", year: 2017 },
  { id: 151, artistIds: [67, 79], title: "Be Kind", type: "song", year: 2020 },
  { id: 152, artistIds: [67, 45], title: "Kiss and Make Up (Remix)", type: "song", year: 2019 },
  { id: 153, artistIds: [67, 11], title: "Set Me Free", type: "song", year: 2023 },
  
  // Coldplay connections
  { id: 154, artistIds: [42, 44], title: "My Universe", type: "song", year: 2021 },
  { id: 155, artistIds: [42, 2], title: "Princess of China", type: "song", year: 2012 },
  { id: 156, artistIds: [42, 5], title: "Hymn for the Weekend", type: "song", year: 2016 },
  { id: 157, artistIds: [42, 66], title: "Something Just Like This", type: "song", year: 2017 },
  
  // BTS connections
  { id: 158, artistIds: [44, 28], title: "Butter (Remix)", type: "song", year: 2021 },
  { id: 159, artistIds: [44, 79], title: "Boy With Luv", type: "song", year: 2019 },
  { id: 160, artistIds: [44, 12], title: "IDOL (Remix)", type: "song", year: 2018 },
  { id: 161, artistIds: [44, 46], title: "Ice Cream (Live)", type: "live", year: 2020 },
  
  // Future connections
  { id: 162, artistIds: [29, 84], title: "Relationship", type: "song", year: 2017 },
  { id: 163, artistIds: [29, 61], title: "Heroes & Villains", type: "album", year: 2022 },
  { id: 164, artistIds: [29, 86], title: "Out of Time", type: "song", year: 2020 },
  
  // Metro Boomin connections
  { id: 165, artistIds: [61, 29], title: "Heroes & Villains", type: "album", year: 2022 },
  { id: 166, artistIds: [61, 9], title: "Creepin'", type: "song", year: 2022 },
  { id: 167, artistIds: [61, 30], title: "Savage Mode II", type: "album", year: 2020 },
  
  // Anderson .Paak / Silk Sonic
  { id: 168, artistIds: [74, 75], title: "Dang!", type: "song", year: 2016 },
  
  // Pharrell connections
  { id: 169, artistIds: [31, 2], title: "Lemon", type: "song", year: 2017 },
  { id: 170, artistIds: [31, 94], title: "Get Lucky", type: "song", year: 2013 },
  { id: 171, artistIds: [31, 32], title: "Beautiful (Live)", type: "live", year: 2003 },
  { id: 172, artistIds: [31, 48], title: "Come Get It Bae", type: "song", year: 2014 },
  
  // Daft Punk connections
  { id: 173, artistIds: [94, 3], title: "Stronger", type: "song", year: 2007 },
  { id: 174, artistIds: [94, 9], title: "I Feel It Coming", type: "song", year: 2016 },
  
  // Tyler, The Creator connections
  { id: 175, artistIds: [59, 58], title: "She", type: "song", year: 2011 },
  { id: 176, artistIds: [59, 60], title: "Who Dat Boy", type: "song", year: 2017 },
  { id: 177, artistIds: [59, 82], title: "FIRESTARTER", type: "song", year: 2021 },
  { id: 178, artistIds: [59, 83], title: "EARFQUAKE", type: "song", year: 2019 },
  
  // Frank Ocean connections
  { id: 179, artistIds: [58, 4], title: "Biking", type: "song", year: 2017 },
  { id: 180, artistIds: [58, 74], title: "Solo (Reprise)", type: "song", year: 2016 },
  
  // Young Thug connections
  { id: 181, artistIds: [84, 85], title: "Drip or Drown 2", type: "album", year: 2019 },
  { id: 182, artistIds: [84, 13], title: "Pick Up the Phone", type: "song", year: 2016 },
  { id: 183, artistIds: [84, 82], title: "Got the Guap", type: "song", year: 2018 },
  
  // Halsey connections
  { id: 184, artistIds: [79, 66], title: "Closer", type: "song", year: 2016 },
  { id: 185, artistIds: [79, 11], title: "The Feeling", type: "song", year: 2015 },
  { id: 186, artistIds: [79, 80], title: "Life's a Mess", type: "song", year: 2020 },
  
  // Juice WRLD connections
  { id: 187, artistIds: [80, 29], title: "WRLD on Drugs", type: "album", year: 2018 },
  { id: 188, artistIds: [80, 13], title: "No Bystanders", type: "song", year: 2018 },
  
  // Childish Gambino connections
  { id: 189, artistIds: [73, 76], title: "They Don't Like Me", type: "song", year: 2013 },
  { id: 190, artistIds: [73, 21], title: "Summertime Magic (Live)", type: "live", year: 2018 },
  
  // Cardi B connections
  { id: 191, artistIds: [25, 28], title: "WAP", type: "song", year: 2020 },
  { id: 192, artistIds: [25, 43], title: "Girls Like You", type: "song", year: 2018 },
  { id: 193, artistIds: [25, 18], title: "Finesse (Remix)", type: "song", year: 2018 },
  { id: 194, artistIds: [25, 92], title: "Clout", type: "song", year: 2019 },
  
  // Selena Gomez connections
  { id: 195, artistIds: [46, 43], title: "Good for You", type: "song", year: 2015 },
  { id: 196, artistIds: [46, 67], title: "Wolves", type: "song", year: 2017 },
  { id: 197, artistIds: [46, 3], title: "All Mine (Remix)", type: "song", year: 2018 },
  
  // Charlie Puth connections
  { id: 198, artistIds: [47, 46], title: "We Don't Talk Anymore", type: "song", year: 2016 },
  { id: 199, artistIds: [47, 28], title: "Cry Baby", type: "song", year: 2021 },
  { id: 200, artistIds: [47, 23], title: "Nothing but Trouble", type: "song", year: 2015 },
  
  // Miley Cyrus / Collaboration
  { id: 201, artistIds: [48, 43], title: "Moves Like Jagger", type: "live", year: 2013 },
  
  // Rosalia connections
  { id: 202, artistIds: [98, 13], title: "TKN", type: "song", year: 2020 },
  { id: 203, artistIds: [98, 99], title: "Con Altura", type: "song", year: 2019 },
  { id: 204, artistIds: [98, 100], title: "Yo x Ti, Tu x Mi", type: "song", year: 2019 },
  
  // Swae Lee / Offset / Quavo (Migos)
  { id: 205, artistIds: [89, 92], title: "Culture III", type: "album", year: 2021 },
  { id: 206, artistIds: [89, 93], title: "Culture III", type: "album", year: 2021 },
  { id: 207, artistIds: [92, 93], title: "Culture", type: "album", year: 2017 },
  { id: 208, artistIds: [89, 1], title: "Walk It Talk It", type: "song", year: 2018 },
  { id: 209, artistIds: [93, 13], title: "Pick Up the Phone", type: "song", year: 2016 },
  
  // Lil Baby connections
  { id: 210, artistIds: [86, 85], title: "Drip Too Hard", type: "song", year: 2018 },
  { id: 211, artistIds: [86, 1], title: "Wants and Needs", type: "song", year: 2021 },
  { id: 212, artistIds: [86, 84], title: "Bad Boy", type: "song", year: 2020 },
  
  // Gorillaz connections
  { id: 213, artistIds: [95, 32], title: "Welcome to the World of the Plastic Beach", type: "album", year: 2010 },
  { id: 214, artistIds: [95, 74], title: "Humility (Live)", type: "live", year: 2018 },
  
  // Elton John connections
  { id: 215, artistIds: [53, 7], title: "Merry Christmas", type: "song", year: 2021 },
  { id: 216, artistIds: [53, 54], title: "That's What Friends Are For (Live)", type: "live", year: 1985 },
  { id: 217, artistIds: [53, 6], title: "Stan (Grammy Performance)", type: "live", year: 2001 },
  
  // Jack Harlow connections
  { id: 218, artistIds: [62, 23], title: "What's Poppin (Remix)", type: "song", year: 2020 },
  { id: 219, artistIds: [62, 86], title: "What's Poppin (Remix)", type: "song", year: 2020 },
  
  // Maroon 5 connections
  { id: 220, artistIds: [43, 47], title: "Moves Like Jagger (Live)", type: "live", year: 2016 },
  { id: 221, artistIds: [43, 2], title: "If I Never See Your Face Again", type: "song", year: 2008 },
  
  // Diplo / Major Lazer
  { id: 222, artistIds: [71, 72], title: "Major Lazer Project", type: "album", year: 2015 },
  { id: 223, artistIds: [71, 70], title: "Jack Ü", type: "album", year: 2015 },
  { id: 224, artistIds: [72, 39], title: "Lean On", type: "song", year: 2015 },
  { id: 225, artistIds: [71, 11], title: "Where Are Ü Now", type: "song", year: 2015 },
  { id: 226, artistIds: [70, 11], title: "Where Are Ü Now", type: "song", year: 2015 },
  
  // David Guetta connections
  { id: 227, artistIds: [69, 2], title: "Right Now", type: "song", year: 2012 },
  { id: 228, artistIds: [69, 12], title: "Turn Me On", type: "song", year: 2011 },
  { id: 229, artistIds: [69, 6], title: "Not Afraid of the Dark", type: "song", year: 2011 },
  { id: 230, artistIds: [69, 49], title: "Titanium", type: "song", year: 2011 },
  { id: 231, artistIds: [69, 51], title: "Blinding Lights (Remix)", type: "song", year: 2020 },
  
  // James Blake connections
  { id: 232, artistIds: [97, 96], title: "I Need a Forest Fire", type: "song", year: 2016 },
  { id: 233, artistIds: [97, 13], title: "Mile High", type: "song", year: 2019 },
  { id: 234, artistIds: [97, 60], title: "Hindsight", type: "song", year: 2016 },
  
  // Bon Iver connections
  { id: 235, artistIds: [96, 3], title: "Lost in the World", type: "song", year: 2010 },
  { id: 236, artistIds: [96, 97], title: "Fall Creek Boys Choir", type: "song", year: 2011 },
  
  // Wiz Khalifa connections
  { id: 237, artistIds: [40, 47], title: "See You Again", type: "song", year: 2015 },
  { id: 238, artistIds: [40, 32], title: "Young, Wild & Free", type: "song", year: 2012 },
  
  // 50 Cent connections
  { id: 239, artistIds: [34, 11], title: "Ayo Technology", type: "song", year: 2007 },
  { id: 240, artistIds: [34, 52], title: "Yeah! (Remix)", type: "song", year: 2004 },
  
  // Usher connections  
  { id: 241, artistIds: [52, 11], title: "Somebody to Love (Remix)", type: "song", year: 2010 },
  { id: 242, artistIds: [52, 23], title: "OMG", type: "song", year: 2010 },
  { id: 243, artistIds: [52, 84], title: "No Limit", type: "song", year: 2016 },
  
  // John Legend connections
  { id: 244, artistIds: [50, 3], title: "Blame Game", type: "song", year: 2010 },
  { id: 245, artistIds: [50, 73], title: "Written in the Stars (Live)", type: "live", year: 2016 },
  
  // Alicia Keys connections
  { id: 246, artistIds: [51, 52], title: "My Boo", type: "song", year: 2004 },
  { id: 247, artistIds: [51, 12], title: "Girl on Fire (Remix)", type: "song", year: 2012 },
  
  // Sia connections
  { id: 248, artistIds: [49, 15], title: "Genius (LSD)", type: "song", year: 2018 },
  { id: 249, artistIds: [49, 71], title: "LSD", type: "album", year: 2019 },
  { id: 250, artistIds: [49, 69], title: "Titanium", type: "song", year: 2011 },
  
  // Lil Nas X connections
  { id: 251, artistIds: [27, 62], title: "INDUSTRY BABY", type: "song", year: 2021 },
  { id: 252, artistIds: [27, 22], title: "MONTERO (Live Remix)", type: "live", year: 2021 },
  { id: 253, artistIds: [27, 48], title: "Old Town Road (Live)", type: "live", year: 2020 },
  
  // Shakira connections
  { id: 254, artistIds: [37, 38], title: "Rabiosa", type: "song", year: 2010 },
  { id: 255, artistIds: [37, 18], title: "Hips Don't Lie (Live)", type: "live", year: 2011 },
  
  // Pitbull connections
  { id: 256, artistIds: [38, 12], title: "Hey Mama", type: "song", year: 2015 },
  { id: 257, artistIds: [38, 24], title: "International Love", type: "song", year: 2011 },
  
  // Additional cross-genre connections
  { id: 258, artistIds: [64, 63], title: "Juice (Live Duet)", type: "live", year: 2020 },
  { id: 259, artistIds: [17, 35], title: "Lovely", type: "song", year: 2018 },
  { id: 260, artistIds: [17, 98], title: "Lo Vas A Olvidar", type: "song", year: 2021 },
  { id: 261, artistIds: [57, 19], title: "Shallow-like Performance (Live)", type: "live", year: 2022 },
  { id: 262, artistIds: [41, 23], title: "Believer (Remix)", type: "song", year: 2017 },
  { id: 263, artistIds: [88, 87], title: "ROCKSTAR", type: "song", year: 2020 },
  { id: 264, artistIds: [88, 86], title: "Baby", type: "song", year: 2020 },
  { id: 265, artistIds: [91, 14], title: "Sunflower", type: "song", year: 2018 },
  { id: 266, artistIds: [85, 29], title: "Pushin P", type: "song", year: 2022 },
  { id: 267, artistIds: [82, 29], title: "That Way", type: "song", year: 2019 },
  { id: 268, artistIds: [83, 82], title: "Shoota", type: "song", year: 2018 },
  { id: 269, artistIds: [75, 74], title: "Dang!", type: "song", year: 2016 },
  { id: 270, artistIds: [75, 21], title: "Cinderella (Live Duet)", type: "live", year: 2016 },
  { id: 271, artistIds: [76, 3], title: "Ultralight Beam", type: "song", year: 2016 },
  { id: 272, artistIds: [76, 11], title: "Confident (Remix)", type: "song", year: 2017 },
  { id: 273, artistIds: [99, 100], title: "Reggaeton Lento (Remix)", type: "song", year: 2017 },
  { id: 274, artistIds: [60, 70], title: "Wild for the Night", type: "song", year: 2013 },
  { id: 275, artistIds: [60, 59], title: "POTATO SALAD", type: "song", year: 2018 },
  { id: 276, artistIds: [74, 95], title: "Humility (Live Performance)", type: "live", year: 2018 },
  { id: 277, artistIds: [21, 58], title: "Close to You (Live)", type: "live", year: 2017 },
  { id: 278, artistIds: [26, 20], title: "Black Friday", type: "song", year: 2015 },
  { id: 279, artistIds: [26, 21], title: "Pretty Little Birds", type: "song", year: 2018 },
  { id: 280, artistIds: [64, 46], title: "Grammys Performers (Live)", type: "live", year: 2023 },
];

// BFS pathfinding algorithm to find connection between two artists
function findConnection(startId, endId) {
  if (startId === endId) return [];
  
  const visited = new Set();
  const queue = [[startId, []]];
  visited.add(startId);
  
  while (queue.length > 0) {
    const [currentId, path] = queue.shift();
    
    // Find all collaborations involving this artist
    const collabs = COLLABORATIONS.filter(c => c.artistIds.includes(currentId));
    
    for (const collab of collabs) {
      const nextArtistId = collab.artistIds.find(id => id !== currentId);
      
      if (nextArtistId === endId) {
        return [...path, { collab, fromArtist: currentId, toArtist: nextArtistId }];
      }
      
      if (!visited.has(nextArtistId)) {
        visited.add(nextArtistId);
        queue.push([nextArtistId, [...path, { collab, fromArtist: currentId, toArtist: nextArtistId }]]);
      }
    }
  }
  
  return null; // No connection found
}

// Get artist by ID
function getArtistById(id) {
  return ARTISTS.find(a => a.id === id);
}

// Get all collaborations for an artist
function getCollaborationsForArtist(artistId) {
  return COLLABORATIONS.filter(c => c.artistIds.includes(artistId));
}

// Get random artist
function getRandomArtist(excludeIds = []) {
  const available = ARTISTS.filter(a => !excludeIds.includes(a.id));
  return available[Math.floor(Math.random() * available.length)];
}

// Search artists by name
function searchArtists(query) {
  if (!query || query.length < 1) return [];
  const lowerQuery = query.toLowerCase();
  return ARTISTS.filter(a => a.name.toLowerCase().includes(lowerQuery)).slice(0, 8);
}

// Get connected artists (all artists directly connected to given artist)
function getConnectedArtists(artistId) {
  const collabs = getCollaborationsForArtist(artistId);
  const connectedIds = new Set();
  collabs.forEach(c => {
    c.artistIds.forEach(id => {
      if (id !== artistId) connectedIds.add(id);
    });
  });
  return Array.from(connectedIds).map(id => getArtistById(id));
}

// Get collaborations between two specific artists
function getCollaborationsBetween(artistId1, artistId2) {
  return COLLABORATIONS.filter(c => 
    c.artistIds.includes(artistId1) && c.artistIds.includes(artistId2)
  );
}

export {
  ARTISTS,
  COLLABORATIONS,
  findConnection,
  getArtistById,
  getCollaborationsForArtist,
  getRandomArtist,
  searchArtists,
  getConnectedArtists,
  getCollaborationsBetween,
};
