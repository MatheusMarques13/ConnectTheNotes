import React, { useState, useRef, useEffect, useCallback } from 'react';
import { Search, Shuffle, X, Music, Mic2, Disc3, Guitar, Heart, Sparkles, Flame, Trees, Sun, Cloud, Star, Radio } from 'lucide-react';
import { searchArtists, getRandomArtist } from '../services/api';
import { getGenreIcon, getGenreColor, getAvatarUrl } from '../utils/avatars';
import { useArtistImage } from '../utils/useArtistImage';
import { useI18n } from '../i18n';

const iconMap = {
  'music': Music,
  'mic-2': Mic2,
  'disc-3': Disc3,
  'guitar': Guitar,
  'heart': Heart,
  'sparkles': Sparkles,
  'flame': Flame,
  'trees': Trees,
  'sun': Sun,
  'cloud': Cloud,
  'star': Star,
  'radio': Radio,
};

const hashStr = (s) => { let h = 0; const str = String(s || ''); for (let i = 0; i < str.length; i++) h = (h * 31 + str.charCodeAt(i)) >>> 0; return h; };

// Full-size polaroid, 1989-style: a square instant photo over a thick taped
// bottom border. Empty until an artist is picked — the photo only loads on
// selection.
const ArtistPolaroid = ({ artist, number }) => {
  const { t } = useI18n();
  const [imgLoaded, setImgLoaded] = useState(false);
  const hasArtist = !!artist;
  const name = typeof artist === 'string' ? artist : artist?.name || '';
  const genre = (typeof artist === 'object' && artist?.genre) || '';
  const initials = name ? name.split(' ').map(w => w[0]).join('').slice(0, 2).toUpperCase() : '';
  const tone = hashStr(artist?.id || name || `slot-${number}`) % 5;
  const imageUrl = useArtistImage(artist, 400);
  const GenreIcon = iconMap[getGenreIcon(genre)] || Music;

  return (
    <div className={`artist-polaroid tone-${tone} ${hasArtist ? 'filled' : 'empty'}`}>
      <span className="artist-postit" />
      <div className="artist-polaroid-photo">
        {hasArtist ? (
          <>
            <img
              key={imageUrl}
              src={imageUrl}
              alt={name}
              className={`polaroid-img ${imgLoaded ? 'loaded' : ''}`}
              onLoad={() => setImgLoaded(true)}
              onError={(e) => { e.target.style.display = 'none'; }}
            />
            {!imgLoaded && <span className="artist-initials-fallback">{initials}</span>}
          </>
        ) : (
          <span className="polaroid-empty-mark"><Music size={44} strokeWidth={1.3} /></span>
        )}
      </div>
      <div className="artist-polaroid-cap">
        <span className="artist-polaroid-name">{hasArtist ? name : t('artist_n', { n: number })}</span>
        {hasArtist && genre && (
          <span className="artist-polaroid-genre" style={{ color: getGenreColor(genre) }}>
            <GenreIcon size={11} strokeWidth={2} />
            {genre}
          </span>
        )}
      </div>
    </div>
  );
};

const SearchResultAvatar = ({ artist }) => {
  const [imgLoaded, setImgLoaded] = useState(false);
  const imageUrl = getAvatarUrl(artist, 64);
  const name = typeof artist === 'string' ? artist : artist?.name || 'Unknown';
  const initials = name.split(' ').map(w => w[0]).join('').slice(0, 2).toUpperCase();

  return (
    <div className="result-avatar-img-wrapper">
      <img
        src={imageUrl}
        alt={name}
        className={`result-avatar-img ${imgLoaded ? 'loaded' : ''}`}
        onLoad={() => setImgLoaded(true)}
        onError={(e) => { e.target.style.display = 'none'; }}
      />
      {!imgLoaded && <span style={{ fontSize: '11px', fontWeight: 600 }}>{initials}</span>}
    </div>
  );
};

const ArtistCard = ({ number, artist, onSelect, onClear, excludeIds = [] }) => {
  const { t } = useI18n();
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [showDropdown, setShowDropdown] = useState(false);
  const [loading, setLoading] = useState(false);
  const inputRef = useRef(null);
  const dropdownRef = useRef(null);
  const debounceRef = useRef(null);

  useEffect(() => {
    const handleClickOutside = (e) => {
      if (dropdownRef.current && !dropdownRef.current.contains(e.target) &&
          inputRef.current && !inputRef.current.contains(e.target)) {
        setShowDropdown(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const handleSearch = useCallback((value) => {
    setQuery(value);
    if (debounceRef.current) clearTimeout(debounceRef.current);

    if (value.length > 0) {
      setLoading(true);
      debounceRef.current = setTimeout(async () => {
        const found = await searchArtists(value);
        const filtered = found.filter(a => !excludeIds.includes(a.id));
        setResults(filtered);
        setShowDropdown(true);
        setLoading(false);
      }, 200);
    } else {
      setResults([]);
      setShowDropdown(false);
      setLoading(false);
    }
  }, [excludeIds]);

  const handleSelect = (selectedArtist) => {
    onSelect(selectedArtist);
    setQuery('');
    setResults([]);
    setShowDropdown(false);
  };

  const handleRandom = async () => {
    setLoading(true);
    const randomArtist = await getRandomArtist(excludeIds);
    if (randomArtist) {
      onSelect(randomArtist);
    }
    setQuery('');
    setShowDropdown(false);
    setLoading(false);
  };

  const handleClear = () => {
    onClear();
    setQuery('');
  };

  const renderGenreBadge = (genre) => {
    const iconName = getGenreIcon(genre);
    const IconComp = iconMap[iconName] || Music;
    const color = getGenreColor(genre);
    return (
      <span className="genre-icon-badge" style={{ color }}>
        <IconComp size={12} />
      </span>
    );
  };

  return (
    <div className={`artist-card${artist ? ' has-artist' : ''}`}>
      <div className="card-number">{number}</div>

      <ArtistPolaroid artist={artist} number={number} />

      {artist && (
        <div className="artist-card-actions">
          <button className="clear-btn" onClick={handleClear} aria-label="remove artist">
            <X size={14} />
          </button>
          <button className="shuffle-btn" onClick={handleRandom} disabled={loading} aria-label="shuffle artist">
            {loading ? <span className="search-spinner small" /> : <Shuffle size={14} />}
          </button>
        </div>
      )}

      {!artist && (
        <div className="search-area" style={{ position: 'relative' }}>
          <div className="search-input-wrapper">
            <Search size={14} className="search-icon" />
            <input
              ref={inputRef}
              type="text"
              placeholder={t('enter_artist')}
              value={query}
              onChange={(e) => handleSearch(e.target.value)}
              className="search-input"
              onFocus={() => query.length > 0 && setShowDropdown(true)}
            />
            {loading && <span className="search-spinner" />}
          </div>
          {showDropdown && results.length > 0 && (
            <div className="search-dropdown" ref={dropdownRef}>
              {results.map(r => (
                <button
                  key={r.id}
                  className="search-result-item"
                  onClick={() => handleSelect(r)}
                >
                  <SearchResultAvatar artist={r} />
                  <div className="result-info">
                    <span className="result-name">{r.name}</span>
                    <span className="result-genre">
                      {renderGenreBadge(r.genre)}
                      {r.genre}
                    </span>
                  </div>
                </button>
              ))}
            </div>
          )}
          <button className="choose-for-me-btn" onClick={handleRandom} disabled={loading}>
            <Shuffle size={14} />
            <span>{loading ? t('picking') : t('choose_for_me')}</span>
          </button>
        </div>
      )}
    </div>
  );
};

export default ArtistCard;
