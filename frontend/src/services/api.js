import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || '';
const API = `${BACKEND_URL}/api`;

const api = axios.create({
  baseURL: API,
  timeout: 15000,
});

// ── Auth API (stubs - coming soon) ────────────────────

export async function getCurrentUser() {
  return null;
}

export async function exchangeSessionId() {
  return null;
}

export async function logout() {
  return true;
}

export async function submitGameResult() {
  return null;
}

export async function getLeaderboard(period = 'all', sortBy = 'wins', limit = 20) {
  try {
    const res = await api.get('/leaderboard', { params: { period, sort_by: sortBy, limit } });
    return res.data;
  } catch (err) {
    return { leaderboard: [] };
  }
}

export async function getUserRank(userId, period = 'all') {
  return null;
}

export async function getUserGameHistory(userId, limit = 20) {
  return { history: [] };
}

// ── Artist API ──────────────────────────────────────────

export async function searchArtists(query, limit = 8) {
  if (!query || query.length < 1) return [];
  try {
    const res = await api.get('/artists', { params: { search: query, limit } });
    return res.data.artists || [];
  } catch (err) {
    console.error('searchArtists error:', err);
    return [];
  }
}

export async function getRandomArtist(excludeIds = []) {
  try {
    const params = {};
    if (excludeIds.length > 0) {
      params.excludeIds = excludeIds.join(',');
    }
    const res = await api.get('/artists/random', { params });
    return res.data.artist || null;
  } catch (err) {
    console.error('getRandomArtist error:', err);
    return null;
  }
}

export async function getArtistById(id) {
  try {
    const res = await api.get(`/artists/${id}`);
    return res.data || null;
  } catch (err) {
    console.error('getArtistById error:', err);
    return null;
  }
}

// UPDATED: Now uses /connections endpoint with song data
export async function getCollaborationsForArtist(artistId) {
  try {
    const res = await api.get(`/artists/${artistId}/connections`);
    // Backend returns connections with song data
    // Map to collab format for UI compatibility
    const connections = res.data.connections || [];
    return connections.map(conn => ({
      id: conn.id,
      title: conn.song.title,
      type: conn.song.type,
      year: conn.song.year,
      artistIds: [conn.artist1, conn.artist2],
      coverUrl: conn.song.coverUrl
    }));
  } catch (err) {
    console.error('getCollaborationsForArtist error:', err);
    return [];
  }
}

export async function getConnectedArtists(artistId) {
  try {
    const res = await api.get(`/artists/${artistId}/connected`);
    return res.data.artists || [];
  } catch (err) {
    console.error('getConnectedArtists error:', err);
    return [];
  }
}

// UPDATED: Now uses /connections/between endpoint
export async function getCollaborationsBetween(id1, id2) {
  try {
    const res = await api.get(`/connections/between/${id1}/${id2}`);
    // Map connections to collab format
    const connections = res.data.connections || [];
    return connections.map(conn => ({
      id: conn.id,
      title: conn.song.title,
      type: conn.song.type,
      year: conn.song.year,
      artistIds: [conn.artist1, conn.artist2],
      coverUrl: conn.song.coverUrl
    }));
  } catch (err) {
    console.error('getCollaborationsBetween error:', err);
    return [];
  }
}

// UPDATED: Backend now returns path with type: artist/song alternating
export async function findConnection(startId, endId) {
  try {
    const res = await api.post('/game/find-path', { startId, endId });
    const rawPath = res.data.path;
    
    if (!rawPath || rawPath.length === 0) return null;
    
    // New backend format: [{type: 'artist', ...}, {type: 'song', ...}, {type: 'artist', ...}]
    // Convert to old format for GameBoard compatibility
    // Old format: [{fromArtist, toArtist, collab}]
    
    const convertedPath = [];
    
    for (let i = 0; i < rawPath.length; i++) {
      const item = rawPath[i];
      
      // Skip if not an artist (we only track artist-to-artist steps)
      if (item.type !== 'artist') continue;
      
      // Find next artist in path
      let nextArtistIndex = i + 1;
      while (nextArtistIndex < rawPath.length && rawPath[nextArtistIndex].type !== 'artist') {
        nextArtistIndex++;
      }
      
      if (nextArtistIndex >= rawPath.length) break;
      
      // Find song between current and next artist
      const songIndex = i + 1;
      if (songIndex < rawPath.length && rawPath[songIndex].type === 'song') {
        const song = rawPath[songIndex];
        const nextArtist = rawPath[nextArtistIndex];
        
        convertedPath.push({
          fromArtist: item.id,
          toArtist: nextArtist.id,
          collab: {
            title: song.title,
            type: song.type,
            year: song.year,
            coverUrl: song.coverUrl
          }
        });
      }
      
      i = nextArtistIndex - 1; // Skip to next artist
    }
    
    return convertedPath;
  } catch (err) {
    console.error('findConnection error:', err);
    return null;
  }
}

export async function getStats() {
  try {
    const res = await api.get('/stats');
    return res.data;
  } catch (err) {
    console.error('getStats error:', err);
    return { totalArtists: 0, totalConnections: 0 };
  }
}

export default api;
