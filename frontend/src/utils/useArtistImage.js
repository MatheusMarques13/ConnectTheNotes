import { useState, useEffect } from 'react';
import { ARTIST_IMAGES } from '../data/images.generated';
import { getAvatarUrl } from './avatars';
import { getArtistImage } from './deezer';

// Returns a photo URL for an artist: the build-time baked photo if present,
// otherwise a runtime Deezer lookup (cached), falling back to the styled
// initials avatar until/unless a real photo is found.
export function useArtistImage(artist, size = 200) {
  const name = typeof artist === 'string' ? artist : (artist && artist.name) || '';
  const baked = ARTIST_IMAGES[name];
  const [url, setUrl] = useState(baked || getAvatarUrl(artist, size));

  useEffect(() => {
    setUrl(baked || getAvatarUrl(artist, size));
    if (baked || !name) return undefined;
    let alive = true;
    getArtistImage(name).then((u) => { if (alive && u) setUrl(u); });
    return () => { alive = false; };
  }, [name]); // eslint-disable-line react-hooks/exhaustive-deps

  return url;
}
