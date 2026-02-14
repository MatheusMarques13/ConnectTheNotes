# Connect the Notes - PRD

## Overview
A musical artist connection trivia game where players connect two artists through their collaborations (songs, albums, live performances). Inspired by Connect the Stars but for music.

## Tech Stack
- **Frontend**: React + React Router + Tailwind CSS + Lucide React icons
- **Backend**: FastAPI + MongoDB (motor async driver)
- **Auth**: Emergent Google OAuth
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

## User Authentication (December 2024)
- **Google OAuth** via Emergent Auth service
- Session management with httpOnly cookies (7-day expiry)
- User profile display with avatar and stats
- Protected game result submission

## Game Modes
### Timed Challenge Mode
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

## Leaderboard System (December 2024)
- **Period filters**: Today, This Week, All Time
- **Sort options**: Most Wins, Fewest Steps, Fastest Time
- User rank card showing personal stats
- Game history view

## Visual Features
- **DiceBear Avatars**: Unique "lorelei" style SVG avatars for each artist
- **Genre Icons**: Lucide-react icons mapped by genre
- **Genre-colored Rings**: Avatar rings colored by genre
- **Timer States**: Color-coded urgency

## Player Stats
- Games Played / Won / Lost
- Best Steps / Best Time
- Win Rate percentage
- Rank position on leaderboard

## Artist Database
### Coverage by Genre:
- **Hip-Hop/Rap**: 100+ artists
- **Pop**: 50+ artists
- **R&B/Soul**: 40+ artists
- **Rock/Alternative**: 50+ artists
- **EDM/Electronic**: 30+ artists
- **Latin/Reggaeton**: 30+ artists
- **K-Pop**: 30+ artists
- **Afrobeats**: 20+ artists
- **Country**: 30+ artists
- **Brazilian**: 130+ artists

## API Endpoints
### Auth
- `POST /api/auth/session` - Exchange session_id for user data
- `GET /api/auth/me` - Get current authenticated user
- `POST /api/auth/logout` - Logout user

### Game Results & Leaderboard
- `POST /api/game/submit-result` - Submit game result (requires auth)
- `GET /api/leaderboard` - Get leaderboard with period/sort filters
- `GET /api/leaderboard/user/{user_id}` - Get user's rank
- `GET /api/user/{user_id}/history` - Get user's game history

### Artists & Game
- `GET /api/artists?search={query}` - Search artists
- `GET /api/artists/random` - Get random artist
- `GET /api/artists/{id}/collaborations` - Get artist collaborations
- `POST /api/game/find-path` - BFS pathfinding
- `GET /api/stats` - Database statistics

## File Structure
```
/app
├── backend/
│   ├── server.py       # FastAPI routes (auth, leaderboard, game)
│   ├── seed.py         # Database seeding (590 artists, 1087 collabs)
│   └── tests/
│       └── test_auth_leaderboard.py
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── ArtistCard.jsx
│   │   │   ├── GameBoard.jsx
│   │   │   ├── AuthCallback.jsx      # OAuth callback handler
│   │   │   ├── UserMenu.jsx          # Login/profile dropdown
│   │   │   ├── LeaderboardModal.jsx  # Leaderboard with filters
│   │   │   ├── GameHistoryModal.jsx  # User game history
│   │   │   ├── OptionsModal.jsx      # Settings + difficulty
│   │   │   └── StarryBackground.jsx
│   │   ├── services/
│   │   │   └── api.js                # Auth + leaderboard API
│   │   ├── utils/
│   │   │   └── avatars.js
│   │   ├── App.js                    # BrowserRouter, auth state
│   │   └── App.css
│   └── package.json
├── auth_testing.md
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
- [x] Timed Challenge Mode with 4 difficulties
- [x] Timer display with warning/critical states
- [x] Game Lost screen ("Time's Up!")
- [x] **Google OAuth via Emergent Auth**
- [x] **Leaderboard with period/sort filters**
- [x] **User game history**
- [x] **Game result submission with stats tracking**
- [x] Comprehensive testing (100% pass rate)
- [x] **Bug Fix (Dec 2024)**: Fixed critical UI layout bug where diamond logo was too large, covering "Start Game" button and preventing artist selection. Added missing CSS classes (.logo-section, .logo-diamond, .diamond-svg, .footer-stats) and fixed prop mismatch in ArtistCard component.

## Future/Backlog Tasks
- [ ] Social sharing of completed chains
- [ ] Daily Challenge mode (same artists for all players)
- [ ] More regional artists (African, Asian beyond K-Pop)
- [ ] Music API integration (MusicBrainz/Spotify) for automated data expansion
- [ ] Sound effects implementation
- [ ] Achievement system
