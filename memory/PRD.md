# Connect the Notes - PRD

## Overview
A musical artist connection trivia game where players connect two artists through their collaborations (songs, albums, live performances). Inspired by Connect the Stars but for music.

## Tech Stack
- **Frontend**: React + Tailwind CSS + Lucide React icons
- **Backend**: FastAPI + MongoDB (motor async driver)
- **Database**: 590 artists, 1087 collaborations across all major genres

## Core Features
- Artist search with autocomplete (backed by MongoDB text index)
- Random artist selection ("Choose for Me")
- Game board with collaboration chain-building
- BFS pathfinding for connection paths and hints
- Step counter, undo, restart functionality
- Victory screen with connection chain display
- How to Play & Options modals
- Animated starry/constellation background with mouse interactivity

## Game Modes (December 2024)
### Timed Challenge Mode
- Toggle on/off in Options
- Four difficulty levels:
  - **Easy**: 5 minutes, hints enabled
  - **Medium**: 3 minutes, hints enabled
  - **Hard**: 90 seconds, hints disabled
  - **Expert**: 60 seconds, hints disabled
- Visual timer with progress bar
- Warning states: Yellow at 30s, Red pulse at 10s
- "Time's Up!" game lost screen on timeout

### Classic Mode (Default)
- No time limit
- Hints toggleable in Options
- Relaxed exploration of connections

## Visual Features
- **DiceBear Avatars**: Unique "lorelei" style SVG avatars for each artist
- **Genre Icons**: Lucide-react icons mapped by genre (mic-2 for Hip-Hop, guitar for Rock, flame for Latin, etc.)
- **Genre-colored Rings**: Avatar rings colored by genre for visual distinction
- **Timer States**: Color-coded urgency (normal → yellow → red)

## Design Theme
- Diamond/crystal atmosphere: icy blues, silvers, deep navy
- Fonts: Cormorant Garamond (display), Outfit (body), JetBrains Mono (mono)
- Constellation animations with shooting stars

## Player Stats
- Games Played
- Games Won
- Games Lost
- Best Steps (fewest steps to win)
- Best Time (fastest win in timed mode)
- Win Rate percentage

## Artist Database
### Coverage by Genre:
- **Hip-Hop/Rap**: 100+ artists (Drake, Kendrick, Travis Scott, UK Rap, etc.)
- **Pop**: 50+ artists (Taylor Swift, Ariana Grande, Dua Lipa, etc.)
- **R&B/Soul**: 40+ artists (The Weeknd, SZA, Frank Ocean, etc.)
- **Rock/Alternative**: 50+ artists (Coldplay, Arctic Monkeys, etc.)
- **EDM/Electronic**: 30+ artists (Calvin Harris, Marshmello, Fred again.., etc.)
- **Latin/Reggaeton**: 30+ artists (Bad Bunny, Rosalía, J Balvin, etc.)
- **K-Pop**: 30+ artists (BTS, BLACKPINK, NewJeans, etc.)
- **Afrobeats**: 20+ artists (Burna Boy, Wizkid, Tems, etc.)
- **Country**: 30+ artists (Morgan Wallen, Chris Stapleton, etc.)
- **Brazilian**: 130+ artists

### Brazilian Artists (December 2024):
- **Funk/Pop**: Anitta, Ludmilla, MC Kevinho, Pabllo Vittar, Gloria Groove, Luísa Sonza
- **Sertanejo**: Marília Mendonça, Gusttavo Lima, Luan Santana, Maiara & Maraisa, Henrique & Juliano
- **MPB Legends**: Caetano Veloso, Gilberto Gil, Tom Jobim, Elis Regina, Milton Nascimento
- **EDM**: Alok, Vintage Culture, Cat Dealers, Dubdogz, KVSH
- **Hip-Hop**: Racionais MC's, Emicida, Criolo, Djonga
- **Pagode**: Thiaguinho, Zeca Pagodinho, Sorriso Maroto, Dilsinho
- **Rock**: Legião Urbana, Titãs, Charlie Brown Jr, Fresno

## API Endpoints
- `GET /api/artists?search={query}&limit={n}` - Search artists
- `GET /api/artists/random` - Get random artist
- `GET /api/artists/{id}` - Get artist by ID
- `GET /api/artists/{id}/collaborations` - Get artist collaborations
- `GET /api/artists/{id}/connected` - Get connected artists
- `POST /api/game/find-path` - BFS pathfinding between two artists
- `GET /api/stats` - Database statistics

## File Structure
```
/app
├── backend/
│   ├── server.py       # FastAPI routes and DB connection
│   ├── seed.py         # Database seeding script (590 artists, 1087 collabs)
│   └── tests/          # Pytest test files
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── ArtistCard.jsx     # Artist selection with avatars
│   │   │   ├── GameBoard.jsx      # Game interface + timer + game lost screen
│   │   │   ├── StarryBackground.jsx
│   │   │   ├── HowToPlayModal.jsx
│   │   │   └── OptionsModal.jsx   # Timed mode + difficulty selector
│   │   ├── services/
│   │   │   └── api.js             # Centralized API calls
│   │   ├── utils/
│   │   │   └── avatars.js         # DiceBear & genre icon utilities
│   │   ├── App.js                 # DIFFICULTY_CONFIG, game state
│   │   └── App.css                # Diamond theme + timer + game lost styles
│   └── package.json
└── memory/
    └── PRD.md
```

## Completed Tasks
- [x] Full-stack scaffolding (React + FastAPI + MongoDB)
- [x] Artist search and selection
- [x] Game board with collaboration display
- [x] BFS pathfinding algorithm
- [x] Diamond/crystal theme design
- [x] DiceBear avatar integration
- [x] Genre-specific icons
- [x] Brazilian artists expansion (130+ artists)
- [x] **Timed Challenge Mode** with 4 difficulty levels
- [x] **Timer display** with warning/critical states
- [x] **Game Lost screen** ("Time's Up!")
- [x] **Stats tracking** (played, won, lost, best time, win rate)
- [x] Comprehensive testing (100% pass rate)

## Future/Backlog Tasks
- [ ] User accounts for persistent game history/stats
- [ ] Social sharing of completed chains
- [ ] Leaderboards (daily/weekly/all-time)
- [ ] More regional artists (African, Asian beyond K-Pop)
- [ ] Music API integration (MusicBrainz/Spotify) for automated data expansion
- [ ] Sound effects implementation
- [ ] Achievement system
