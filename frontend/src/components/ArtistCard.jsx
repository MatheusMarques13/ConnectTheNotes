import React, { useState, useRef, useEffect, useCallback } from 'react';
import { Search, Shuffle, X, Music, Mic2, Disc3, Guitar, Heart, Sparkles, Flame, Trees, Sun, Cloud, Star, Radio } from 'lucide-react';
import { searchArtists, getRandomArtist } from '../services/api';
import { getGenreIcon, getGenreColor, getAvatarUrl } from '../utils/avatars';

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

const ArtistAvatar = ({ artist, genre }) => {
  const [imgLoaded, setImgLoaded] = useState(false);
  const imageUrl = getAvatarUrl(artist, 128);
  const name = typeof artist === 'string' ? artist : artist?.name || 'Unknown';
  const initials = name.split(' ').map(w => w[0]).join('').slice(0, 2).toUpperCase();

  return (
    <div className="artist-avatar-ring" style={{ borderColor: getGenreColor(genre) }}>
      <img
        src={imageUrl}
        alt={name}
        className={`artist-avatar-img ${imgLoaded ? 'loaded' : ''}`}
        onLoad={() => setImgLoaded(true)}
        onError={(e) => { e.target.style.display = 'none'; }}
      />
      {!imgLoaded && (
        <span className="artist-initials-fallback">{initials}</span>
      )}
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

  // Render genre-specific placeholder icon
  const renderPlaceholderIcons = () => {
    return (
      <div className="placeholder-icons-grid">
        <div className="placeholder-icon-item">
          <Mic2 size={28} strokeWidth={1.2} />
        </div>
        <div className="placeholder-icon-item">
          <Music size={28} strokeWidth={1.2} />
        </div>
        <div className="placeholder-icon-item">
          <Guitar size={28} strokeWidth={1.2} />
        </div>
        <div className="placeholder-icon-item">
          <Disc3 size={28} strokeWidth={1.2} />
        </div>
        <div className="placeholder-icon-item">
          <Star size={28} strokeWidth={1.2} />
        </div>
        <div className="placeholder-icon-item">
          <Radio size={28} strokeWidth={1.2} />
        </div>
      </div>
    );
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
    <div className="artist-card">
      <div className="card-number">{number}</div>
      <div className="card-image-area">
        {artist ? (
          <div className="artist-selected">
            <div className="artist-avatar-wrapper">
              <ArtistAvatar artist={artist} genre={artist.genre} />
            </div>
            <button className="clear-btn" onClick={handleClear}>
              <X size={14} />
            </button>
          </div>
        ) : (
          <div className="artist-placeholder">
            {renderPlaceholderIcons()}
          </div>
        )}
      </div>
      {artist ? (
        <div className="artist-info">
          <div className="artist-name-display">{artist.name}</div>
          <div className="artist-genre">
            {renderGenreBadge(artist.genre)}
            {artist.genre}
          </div>
        </div>
      ) : (
        <div className="search-area" style={{ position: 'relative' }}>
          <div className="search-input-wrapper">
            <Search size={14} className="search-icon" />
            <input
              ref={inputRef}
              type="text"
              placeholder="Enter an artist's name"
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
            <span>{loading ? 'PICKING...' : 'CHOOSE FOR ME'}</span>
          </button>
        </div>
      )}
    </div>
  );
};

export default ArtistCard;
