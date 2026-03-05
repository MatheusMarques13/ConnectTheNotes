// Avatar and icon utilities for artist display

// Helper to fetch artist image from Last.fm (free API, no auth required)
const LASTFM_API_KEY = '9d1c9c9d7f4c0e4e8b9c9c9d7f4c0e4e'; // Public demo key
const imageCache = new Map();

export function getArtistImageUrl(artistName, size = 'large') {
  // Return cached URL if available
  const cacheKey = `${artistName}-${size}`;
  if (imageCache.has(cacheKey)) {
    return imageCache.get(cacheKey);
  }

  // Return placeholder that will be replaced by actual fetch
  return null;
}

// Fetch real artist image from Last.fm API
export async function fetchArtistImage(artistName) {
  try {
    const response = await fetch(
      `https://ws.audioscrobbler.com/2.0/?method=artist.getinfo&artist=${encodeURIComponent(artistName)}&api_key=${LASTFM_API_KEY}&format=json`
    );
    const data = await response.json();
    
    if (data.artist?.image) {
      // Last.fm returns images in sizes: small, medium, large, extralarge, mega
      const images = data.artist.image;
      const largeImg = images.find(img => img.size === 'extralarge' || img.size === 'large');
      
      if (largeImg && largeImg['#text']) {
        // Cache for future use
        imageCache.set(`${artistName}-large`, largeImg['#text']);
        const mediumImg = images.find(img => img.size === 'medium');
        if (mediumImg?.['#text']) {
          imageCache.set(`${artistName}-medium`, mediumImg['#text']);
        }
        return largeImg['#text'];
      }
    }
  } catch (error) {
    console.warn('Failed to fetch artist image from Last.fm:', error);
  }
  
  // Return null if fetch fails - component will use fallback
  return null;
}

// Generate fallback avatar URL using UI Avatars (initials-based)
function getFallbackAvatarUrl(name, size = 128) {
  const initials = name.split(' ').map(w => w[0]).join('').slice(0, 2).toUpperCase();
  const colors = ['6366f1', '8b5cf6', 'ec4899', 'ef4444', '14b8a6', '06b6d4', 'f59e0b'];
  const color = colors[name.charCodeAt(0) % colors.length];
  return `https://ui-avatars.com/api/?name=${encodeURIComponent(initials)}&size=${size}&background=${color}&color=fff&bold=true&font-size=0.4`;
}

// Avatar URL with fallback chain: Last.fm → UI Avatars
export function getAvatarUrl(name, size = 128) {
  const cached = imageCache.get(`${name}-large`);
  if (cached) return cached;
  
  // Return fallback immediately, async fetch will update via component state
  return getFallbackAvatarUrl(name, size);
}

// Small avatar for lists/search results  
export function getSmallAvatarUrl(name) {
  const cached = imageCache.get(`${name}-medium`);
  if (cached) return cached;
  return getFallbackAvatarUrl(name, 64);
}

// Large avatar for game board / selected state
export function getLargeAvatarUrl(name) {
  const cached = imageCache.get(`${name}-large`);
  if (cached) return cached;
  return getFallbackAvatarUrl(name, 200);
}

// Genre-to-icon mapping for selector cards
// Returns the lucide icon name based on genre
export function getGenreIcon(genre) {
  if (!genre) return 'music';
  const g = genre.toLowerCase();
  if (g.includes('hip-hop') || g.includes('rap') || g.includes('grime') || g.includes('drill')) return 'mic-2';
  if (g.includes('edm') || g.includes('electronic') || g.includes('house') || g.includes('techno') || g.includes('dubstep')) return 'disc-3';
  if (g.includes('rock') || g.includes('metal') || g.includes('punk') || g.includes('grunge')) return 'guitar';
  if (g.includes('r&b') || g.includes('soul') || g.includes('neo-soul')) return 'heart';
  if (g.includes('pop') && g.includes('k-')) return 'sparkles';
  if (g.includes('k-pop')) return 'sparkles';
  if (g.includes('latin') || g.includes('reggaeton') || g.includes('bachata') || g.includes('salsa')) return 'flame';
  if (g.includes('country') || g.includes('folk')) return 'trees';
  if (g.includes('afrobeat') || g.includes('afro')) return 'sun';
  if (g.includes('indie') || g.includes('alternative')) return 'cloud';
  if (g.includes('jazz')) return 'music-3';
  if (g.includes('classical')) return 'music-4';
  if (g.includes('reggae') || g.includes('dancehall')) return 'palmtree';
  if (g.includes('pop')) return 'star';
  if (g.includes('producer') || g.includes('dj')) return 'radio';
  return 'music';
}

// Genre color mapping for avatar ring/background accents
export function getGenreColor(genre) {
  if (!genre) return '#8fa8d6';
  const g = genre.toLowerCase();
  if (g.includes('hip-hop') || g.includes('rap')) return '#a78bfa';
  if (g.includes('edm') || g.includes('electronic')) return '#67e8f9';
  if (g.includes('rock') || g.includes('metal') || g.includes('punk')) return '#f87171';
  if (g.includes('r&b') || g.includes('soul')) return '#c084fc';
  if (g.includes('k-pop')) return '#f472b6';
  if (g.includes('latin') || g.includes('reggaeton')) return '#fb923c';
  if (g.includes('country') || g.includes('folk')) return '#a3e635';
  if (g.includes('afrobeat')) return '#fbbf24';
  if (g.includes('indie') || g.includes('alternative')) return '#6ee7b7';
  if (g.includes('pop')) return '#93c5fd';
  return '#8fa8d6';
}
