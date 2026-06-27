import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || '';
const API = `${BACKEND_URL}/api`;

const api = axios.create({
  baseURL: API,
  timeout: 15000,
});

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
    const connections = res.data.connections || [];
    
    console.log(`[API] Got ${connections.length} connections between ${id1} and ${id2}`);
    console.log('[API] Sample connection:', connections[0]);
    
    // Map connections to collab format
    return connections.map(conn => {
      if (!conn.song) {
        console.warn('[API] Connection missing song data:', conn);
        return null;
      }
      return {
        id: conn.id,
        title: conn.song.title || 'Unknown',
        type: conn.song.type || 'song',
        year: conn.song.year || 2024,
        artistIds: [conn.artist1, conn.artist2],
        coverUrl: conn.song.coverUrl || ''
      };
    }).filter(Boolean);
  } catch (err) {
    console.error('getCollaborationsBetween error:', err);
    return [];
  }
}

// Backend returns { path: [{kind:'artist', artist}, {kind:'song', song}, ...], optimalSteps }
// Returns { steps: [{fromArtist, toArtist, collab}] | null, optimalSteps: number | null }.
// steps === null means the two artists are NOT connected.
export async function findConnection(startId, endId) {
  try {
    const res = await api.post('/game/find-path', { startId, endId });
    const rawPath = res.data.path;

    // null => unreachable; [] => same artist
    if (rawPath === null || rawPath === undefined) return { steps: null, chain: null, optimalSteps: null };
    if (rawPath.length === 0) return { steps: [], chain: [], optimalSteps: 0 };

    const normSong = (song = {}) => ({
      title: song.title || 'Unknown',
      type: song.type || 'song',
      year: song.year || 2024,
      coverUrl: song.coverUrl || '',
    });

    // steps: [{fromArtist:id, toArtist:id, collab}] for hints/logic
    const steps = [];
    for (let i = 0; i < rawPath.length; i++) {
      const node = rawPath[i];
      if (node.kind !== 'artist') continue;
      const songNode = rawPath[i + 1];
      const nextArtistNode = rawPath[i + 2];
      if (!songNode || songNode.kind !== 'song' || !nextArtistNode || nextArtistNode.kind !== 'artist') break;
      steps.push({
        fromArtist: node.artist?.id,
        toArtist: nextArtistNode.artist?.id,
        collab: normSong(songNode.song),
      });
    }

    // chain: [{artist:obj, collab}] ready for <ConstellationGraph />
    const chain = [];
    let pendingSong = null;
    for (const node of rawPath) {
      if (node.kind === 'artist') {
        chain.push({ artist: node.artist, collab: pendingSong });
        pendingSong = null;
      } else if (node.kind === 'song') {
        pendingSong = normSong(node.song);
      }
    }

    return { steps, chain, optimalSteps: res.data.optimalSteps ?? steps.length };
  } catch (err) {
    console.error('findConnection error:', err);
    // Network/server error is distinct from "no path"; surface as undefined steps.
    return { steps: undefined, chain: undefined, optimalSteps: null };
  }
}

// Two artists guaranteed to be connected, with their optimal step count.
export async function getRandomPair(difficulty = 'any') {
  try {
    const res = await api.get('/game/random-pair', { params: { difficulty } });
    return res.data || null;
  } catch (err) {
    console.error('getRandomPair error:', err);
    return null;
  }
}

// Deterministic, always-solvable puzzle for the given date (YYYY-MM-DD).
export async function getDailyPuzzle(dateStr) {
  try {
    const params = dateStr ? { date: dateStr } : {};
    const res = await api.get('/game/daily', { params });
    return res.data || null;
  } catch (err) {
    console.error('getDailyPuzzle error:', err);
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
