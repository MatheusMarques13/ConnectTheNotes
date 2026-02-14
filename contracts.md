# Connect the Notes - API Contracts

## A. API Endpoints

### GET /api/artists
- Query params: `?search=<query>&limit=10`
- Returns: `{ artists: [{ id, name, genre, imageUrl }] }`

### GET /api/artists/random
- Query params: `?excludeIds=1,2`
- Returns: `{ artist: { id, name, genre, imageUrl } }`

### GET /api/artists/:id
- Returns: `{ id, name, genre, imageUrl }`

### GET /api/artists/:id/collaborations
- Returns: `{ collaborations: [{ id, artistIds, title, type, year }] }`

### GET /api/collaborations/between/:id1/:id2
- Returns: `{ collaborations: [{ id, artistIds, title, type, year }] }`

### GET /api/artists/:id/connected
- Returns: `{ artists: [{ id, name, genre, imageUrl }] }`

### POST /api/game/find-path
- Body: `{ startId: string, endId: string }`
- Returns: `{ path: [{ collab, fromArtist, toArtist }] | null }`

## B. Mocked Data to Replace
- `ARTISTS` array in mockData.js → MongoDB `artists` collection
- `COLLABORATIONS` array → MongoDB `collaborations` collection
- `findConnection()` → Backend BFS via `/api/game/find-path`
- `searchArtists()` → Backend text search via `/api/artists?search=`
- `getRandomArtist()` → Backend random via `/api/artists/random`
- `getCollaborationsForArtist()` → Backend via `/api/artists/:id/collaborations`
- `getCollaborationsBetween()` → Backend via `/api/collaborations/between/:id1/:id2`
- `getConnectedArtists()` → Backend via `/api/artists/:id/connected`

## C. Backend Implementation
1. MongoDB models: `artists`, `collaborations` collections
2. Seed script with 200+ artists and 500+ collaborations
3. BFS pathfinding endpoint
4. Text search index on artist names

## D. Frontend Integration
- Create `api.js` service layer that calls backend
- Replace all mockData imports in components with api calls
- Add loading states and error handling
- Components to update: ArtistCard, GameBoard, App.js
