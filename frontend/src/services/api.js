import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const api = axios.create({
  baseURL: API,
  timeout: 15000,
  withCredentials: true, // Send cookies with requests
});

// ── Auth API ──────────────────────────────────────────

// Exchange session_id for user data
export async function exchangeSessionId(sessionId) {
  try {
    const res = await api.post('/auth/session', { session_id: sessionId });
    return res.data;
  } catch (err) {
    console.error('exchangeSessionId error:', err);
    return null;
  }
}

// Get current authenticated user
export async function getCurrentUser() {
  try {
    const res = await api.get('/auth/me');
    return res.data;
  } catch (err) {
    if (err.response?.status === 401) {
      return null; // Not authenticated
    }
    console.error('getCurrentUser error:', err);
    return null;
  }
}

// Logout
export async function logout() {
  try {
    await api.post('/auth/logout');
    return true;
  } catch (err) {
    console.error('logout error:', err);
    return false;
  }
}

// ── Game Results & Leaderboard API ──────────────────────

// Submit game result
export async function submitGameResult(result) {
  try {
    const res = await api.post('/game/submit-result', result);
    return res.data;
  } catch (err) {
    console.error('submitGameResult error:', err);
    return null;
  }
}

// Get leaderboard
export async function getLeaderboard(period = 'all', sortBy = 'wins', limit = 20) {
  try {
    const res = await api.get('/leaderboard', { 
      params: { period, sort_by: sortBy, limit } 
    });
    return res.data;
  } catch (err) {
    console.error('getLeaderboard error:', err);
    return { leaderboard: [] };
  }
}

// Get user rank
export async function getUserRank(userId, period = 'all') {
  try {
    const res = await api.get(`/leaderboard/user/${userId}`, { params: { period } });
    return res.data;
  } catch (err) {
    console.error('getUserRank error:', err);
    return null;
  }
}

// Get user game history
export async function getUserGameHistory(userId, limit = 20) {
  try {
    const res = await api.get(`/user/${userId}/history`, { params: { limit } });
    return res.data;
  } catch (err) {
    console.error('getUserGameHistory error:', err);
    return { history: [] };
  }
}

// ── Artist API ──────────────────────────────────────────

// Search artists by name
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

// Get random artist (exclude certain IDs)
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

// Get artist by ID
export async function getArtistById(id) {
  try {
    const res = await api.get(`/artists/${id}`);
    return res.data || null;
  } catch (err) {
    console.error('getArtistById error:', err);
    return null;
  }
}

// Get collaborations for an artist
export async function getCollaborationsForArtist(artistId) {
  try {
    const res = await api.get(`/artists/${artistId}/collaborations`);
    return res.data.collaborations || [];
  } catch (err) {
    console.error('getCollaborationsForArtist error:', err);
    return [];
  }
}

// Get connected artists
export async function getConnectedArtists(artistId) {
  try {
    const res = await api.get(`/artists/${artistId}/connected`);
    return res.data.artists || [];
  } catch (err) {
    console.error('getConnectedArtists error:', err);
    return [];
  }
}

// Get collaborations between two specific artists
export async function getCollaborationsBetween(id1, id2) {
  try {
    const res = await api.get(`/collaborations/between/${id1}/${id2}`);
    return res.data.collaborations || [];
  } catch (err) {
    console.error('getCollaborationsBetween error:', err);
    return [];
  }
}

// Find path between two artists (BFS)
export async function findConnection(startId, endId) {
  try {
    const res = await api.post('/game/find-path', { startId, endId });
    return res.data.path;
  } catch (err) {
    console.error('findConnection error:', err);
    return null;
  }
}

// Get stats
export async function getStats() {
  try {
    const res = await api.get('/stats');
    return res.data;
  } catch (err) {
    console.error('getStats error:', err);
    return { totalArtists: 0, totalCollaborations: 0 };
  }
}

export default api;
