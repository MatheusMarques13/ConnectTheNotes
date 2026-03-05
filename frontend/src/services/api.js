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

export async function getCollaborationsForArtist(artistId) {
  try {
    const res = await api.get(`/artists/${artistId}/collaborations`);
    return res.data.collaborations || [];
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

export async function getCollaborationsBetween(id1, id2) {
  try {
    const res = await api.get(`/collaborations/between/${id1}/${id2}`);
    return res.data.collaborations || [];
  } catch (err) {
    console.error('getCollaborationsBetween error:', err);
    return [];
  }
}

export async function findConnection(startId, endId) {
  try {
    const res = await api.post('/game/find-path', { startId, endId });
    return res.data.path;
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
    return { totalArtists: 0, totalCollaborations: 0 };
  }
}

export default api;
