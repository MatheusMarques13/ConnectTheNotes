import { useState, useEffect } from 'react';
import { fetchArtistImage, getAvatarUrl } from '../utils/avatars';

/**
 * Hook to fetch real artist image from Last.fm API
 * Returns fallback immediately, then updates with real image when available
 */
export function useArtistImage(artistName, size = 'large') {
  const [imageUrl, setImageUrl] = useState(() => getAvatarUrl(artistName, size === 'large' ? 128 : 64));
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    let cancelled = false;
    
    const loadImage = async () => {
      try {
        const realImage = await fetchArtistImage(artistName);
        if (!cancelled && realImage) {
          setImageUrl(realImage);
          setIsLoading(false);
        } else if (!cancelled) {
          // Keep fallback if fetch failed
          setIsLoading(false);
        }
      } catch (err) {
        if (!cancelled) {
          setError(err);
          setIsLoading(false);
        }
      }
    };

    loadImage();
    return () => { cancelled = true; };
  }, [artistName]);

  return { imageUrl, isLoading, error };
}
