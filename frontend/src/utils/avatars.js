// Avatar and icon utilities for artist display

const imageCache = new Map();

// Fetch artist photo from MusicBrainz + Cover Art Archive (free, no auth)
export async function fetchArtistImage(artistName) {
  try {
    // Step 1: Search MusicBrainz for artist
    const searchUrl = `https://musicbrainz.org/ws/2/artist/?query=${encodeURIComponent(artistName)}&fmt=json&limit=1`;
    const searchRes = await fetch(searchUrl);
    const searchData = await searchRes.json();
    
    if (searchData.artists && searchData.artists.length > 0) {
      const artistMbid = searchData.artists[0].id;
      
      // Step 2: Try to get image from Fanart.tv (has CORS enabled)
      const fanartUrl = `https://webservice.fanart.tv/v3/music/${artistMbid}?api_key=439f6e9277143b734c95f08f45513c0d`;
      try {
        const fanartRes = await fetch(fanartUrl);
        const fanartData = await fanartRes.json();
        
        if (fanartData.artistthumb && fanartData.artistthumb.length > 0) {
          const imageUrl = fanartData.artistthumb[0].url;
          imageCache.set(`${artistName}-large`, imageUrl);
          imageCache.set(`${artistName}-medium`, imageUrl);
          return imageUrl;
        }
      } catch (e) {
        console.log('Fanart.tv fetch failed, trying alternatives');
      }
    }
  } catch (error) {
    console.warn('MusicBrainz fetch failed:', error);
  }
  
  // Fallback: return null so component uses UI Avatars
  return null;
}

// Generate fallback avatar URL using UI Avatars (initials-based)
function getFallbackAvatarUrl(name, size = 128) {
  const initials = name.split(' ').map(w => w[0]).join('').slice(0, 2).toUpperCase();
  // Use genre-based color from the artist's genre if available, otherwise pick from palette
  const colors = ['6366f1', '8b5cf6', 'ec4899', 'ef4444', '14b8a6', '06b6d4', 'f59e0b', 'a78bfa', 'fb923c'];
  const colorIndex = name.split('').reduce((acc, char) => acc + char.charCodeAt(0), 0) % colors.length;
  const color = colors[colorIndex];
  return `https://ui-avatars.com/api/?name=${encodeURIComponent(initials)}&size=${size}&background=${color}&color=fff&bold=true&font-size=0.4&rounded=true`;
}

// Avatar URL with fallback chain: MusicBrainz → Fanart.tv → UI Avatars
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
