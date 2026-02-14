import React, { useState, useRef, useEffect } from 'react';
import { Search, Shuffle, X, Music } from 'lucide-react';
import { searchArtists, getRandomArtist } from '../data/mockData';

const ArtistCard = ({ number, artist, onSelect, onClear, excludeIds = [] }) => {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [showDropdown, setShowDropdown] = useState(false);
  const inputRef = useRef(null);
  const dropdownRef = useRef(null);

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

  const handleSearch = (value) => {
    setQuery(value);
    if (value.length > 0) {
      const found = searchArtists(value).filter(a => !excludeIds.includes(a.id));
      setResults(found);
      setShowDropdown(true);
    } else {
      setResults([]);
      setShowDropdown(false);
    }
  };

  const handleSelect = (selectedArtist) => {
    onSelect(selectedArtist);
    setQuery('');
    setResults([]);
    setShowDropdown(false);
  };

  const handleRandom = () => {
    const randomArtist = getRandomArtist(excludeIds);
    onSelect(randomArtist);
    setQuery('');
    setShowDropdown(false);
  };

  const handleClear = () => {
    onClear();
    setQuery('');
  };

  const getInitials = (name) => {
    return name.split(' ').map(w => w[0]).join('').slice(0, 2).toUpperCase();
  };

  return (
    <div className="artist-card">
      <div className="card-number">{number}</div>
      <div className="card-image-area">
        {artist ? (
          <div className="artist-selected">
            <div className="artist-avatar">
              <span className="artist-initials">{getInitials(artist.name)}</span>
            </div>
            <button className="clear-btn" onClick={handleClear}>
              <X size={14} />
            </button>
          </div>
        ) : (
          <div className="artist-placeholder">
            <Music size={64} strokeWidth={1} className="placeholder-icon" />
          </div>
        )}
      </div>
      {artist ? (
        <div className="artist-info">
          <div className="artist-name-display">{artist.name}</div>
          <div className="artist-genre">{artist.genre}</div>
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
          </div>
          {showDropdown && results.length > 0 && (
            <div className="search-dropdown" ref={dropdownRef}>
              {results.map(r => (
                <button
                  key={r.id}
                  className="search-result-item"
                  onClick={() => handleSelect(r)}
                >
                  <div className="result-avatar-small">
                    <span>{getInitials(r.name)}</span>
                  </div>
                  <div className="result-info">
                    <span className="result-name">{r.name}</span>
                    <span className="result-genre">{r.genre}</span>
                  </div>
                </button>
              ))}
            </div>
          )}
          <button className="choose-for-me-btn" onClick={handleRandom}>
            <Shuffle size={14} />
            <span>CHOOSE FOR ME</span>
          </button>
        </div>
      )}
    </div>
  );
};

export default ArtistCard;
