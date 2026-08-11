import { useState, useEffect } from 'react';
import { ARTIST_IMAGES } from '../data/images.generated';
import { getAvatarUrl } from './avatars';
import { getArtistImage } from './itunes';

// Returns a photo URL for an artist: the build-time baked photo if present,
// otherwise a runtime iTunes lookup (cached), falling back to the styled
// initials avatar until/unless a real photo is found.
//
// iTunes exposes no artist portrait, so the runtime path returns the artist's
// album artwork. That is a downgrade from a photo and the reason the baked
// map is still consulted first.
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
