// Avatar and icon utilities for artist display

// Generate unique profile picture URL using DiceBear API
// Uses "lorelei" style for elegant line-art faces that match diamond aesthetic
export function getAvatarUrl(name, size = 128) {
  const seed = encodeURIComponent(name.trim());
  return `https://api.dicebear.com/9.x/lorelei/svg?seed=${seed}&size=${size}&backgroundColor=b6e3f4,c0aede,d1d4f9,ffd5dc,ffdfbf&backgroundType=gradientLinear`;
}

// Small avatar for lists/search results  
export function getSmallAvatarUrl(name) {
  return getAvatarUrl(name, 64);
}

// Large avatar for game board / selected state
export function getLargeAvatarUrl(name) {
  return getAvatarUrl(name, 200);
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
