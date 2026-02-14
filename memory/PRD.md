# Connect the Notes - PRD

## Overview
A musical artist connection trivia game where players connect two artists through their collaborations (songs, albums, live performances). Inspired by Connect the Stars but for music.

## Tech Stack
- **Frontend**: React + Tailwind CSS + Lucide React icons
- **Backend**: FastAPI + MongoDB (motor async driver)
- **Database**: 590 artists, 1087 collaborations across all major genres

## Core Features
- Artist search with autocomplete (backed by MongoDB text index)
- Random artist selection
- Game board with collaboration chain-building
- BFS pathfinding for connection paths and hints
- Step counter, undo, restart functionality
- Victory screen with connection chain display
- How to Play & Options modals
- Animated starry/constellation background with mouse interactivity

## Visual Features
- **DiceBear Avatars**: Unique "lorelei" style SVG avatars for each artist
- **Genre Icons**: Lucide-react icons mapped by genre (mic-2 for Hip-Hop, guitar for Rock, flame for Latin, etc.)
- **Genre-colored Rings**: Avatar rings colored by genre for visual distinction

## Design Theme
- Diamond/crystal atmosphere: icy blues, silvers, deep navy
- Fonts: Cormorant Garamond (display), Outfit (body), JetBrains Mono (mono)
- Constellation animations with shooting stars

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
- **Brazilian**: 130+ artists (see below)

### Brazilian Artists (December 2024 Update):
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
│   ├── seed.py         # Database seeding script
│   └── tests/          # Pytest test files
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── ArtistCard.jsx     # Artist selection with avatars
│   │   │   ├── GameBoard.jsx      # Main game interface
│   │   │   ├── StarryBackground.jsx
│   │   │   ├── HowToPlayModal.jsx
│   │   │   └── OptionsModal.jsx
│   │   ├── services/
│   │   │   └── api.js             # Centralized API calls
│   │   ├── utils/
│   │   │   └── avatars.js         # DiceBear & genre icon utilities
│   │   ├── App.js                 # Main app component
│   │   └── App.css                # Diamond theme styles
│   └── package.json
└── memory/
    └── PRD.md
```

## Completed Tasks (December 2024)
- [x] Full-stack scaffolding (React + FastAPI + MongoDB)
- [x] Artist search and selection
- [x] Game board with collaboration display
- [x] BFS pathfinding algorithm
- [x] Diamond/crystal theme design
- [x] DiceBear avatar integration
- [x] Genre-specific icons
- [x] Brazilian artists expansion (130+ artists)
- [x] Comprehensive testing (100% pass rate)

## Upcoming/Future Tasks
- [ ] Integrate music data API (MusicBrainz/Spotify) for scalable data sourcing
- [ ] Add more international regions (African artists, Asian pop beyond K-Pop)
- [ ] Timed challenge mode
- [ ] Difficulty settings
- [ ] User accounts with game history/stats
- [ ] Social sharing of completed chains
