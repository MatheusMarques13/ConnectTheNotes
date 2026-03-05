import React, { useState, useEffect, useCallback, useRef } from 'react';
import { ArrowLeft, ArrowRight, Music, Disc, Radio, Mic2, RotateCcw, Lightbulb, Check, Loader2, Clock, XCircle, Search, X } from 'lucide-react';
import {
  getCollaborationsForArtist,
  getConnectedArtists,
  getCollaborationsBetween,
  findConnection,
  getArtistById,
} from '../services/api';
import { getAvatarUrl, getSmallAvatarUrl, getLargeAvatarUrl, getGenreColor } from '../utils/avatars';
import ConstellationGraph from './ConstellationGraph';

const typeIcons = {
  song: <Music size={14} />,
  album: <Disc size={14} />,
  live: <Radio size={14} />,
  feature: <Mic2 size={14} />,
};

const typeLabels = {
  song: 'Song',
  album: 'Album',
  live: 'Live Performance',
  feature: 'Feature',
};

const ArtistMiniAvatar = ({ artist, size = 28, className = '' }) => {
  const [loaded, setLoaded] = useState(false);
  const name = typeof artist === 'string' ? artist : artist?.name || 'Unknown';
  const imageUrl = getAvatarUrl(artist, size);
  const initials = name.split(' ').map(w => w[0]).join('').slice(0, 2).toUpperCase();
  return (
    <div className={`mini-avatar ${className}`} style={{ width: size, height: size }}>
      <img
        src={imageUrl}
        alt={name}
        className={`mini-avatar-img ${loaded ? 'loaded' : ''}`}
        onLoad={() => setLoaded(true)}
        onError={(e) => { e.target.style.display = 'none'; }}
        style={{ width: size, height: size }}
      />
      {!loaded && <span className="mini-avatar-fallback" style={{ fontSize: size * 0.35 }}>{initials}</span>}
    </div>
  );
};

const GameTimer = ({ timeRemaining, timeLimit, isWarning, isCritical }) => {
  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };
  const percentage = (timeRemaining / timeLimit) * 100;
  return (
    <div className={`game-timer ${isWarning ? 'warning' : ''} ${isCritical ? 'critical' : ''}`} data-testid="game-timer">
      <Clock size={16} className="timer-icon" />
      <span className="timer-value">{formatTime(timeRemaining)}</span>
      <div className="timer-bar">
        <div className="timer-bar-fill" style={{ width: `${percentage}%` }} />
      </div>
    </div>
  );
};

const GameBoard = ({ artist1, artist2, onBack, showHints, onWin, onLose, timedMode, timeLimit, difficulty }) => {
  const [chain, setChain] = useState([{ artist: artist1, collab: null }]);
  const [gameWon, setGameWon] = useState(false);
  const [gameLost, setGameLost] = useState(false);
  const [showHint, setShowHint] = useState(false);
  const [hint, setHint] = useState(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [showDropdown, setShowDropdown] = useState(false);
  const [selectedArtist, setSelectedArtist] = useState(null);
  const [matchingCollabs, setMatchingCollabs] = useState([]);
  const [loadingCollabs, setLoadingCollabs] = useState(false);

  const [connectedArtists, setConnectedArtists] = useState([]);
  const [loading, setLoading] = useState(false);
  const [artistCache, setArtistCache] = useState({});

  const [timeRemaining, setTimeRemaining] = useState(timeLimit || 0);
  const [timeSpent, setTimeSpent] = useState(0);
  const timerRef = useRef(null);
  const startTimeRef = useRef(Date.now());
  const searchRef = useRef(null);
  const dropdownRef = useRef(null);

  const currentArtist = chain[chain.length - 1].artist;

  // Close dropdown on outside click
  useEffect(() => {
    const handleClickOutside = (e) => {
      if (dropdownRef.current && !dropdownRef.current.contains(e.target) &&
          searchRef.current && !searchRef.current.contains(e.target)) {
        setShowDropdown(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    document.addEventListener('touchstart', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
      document.removeEventListener('touchstart', handleClickOutside);
    };
  }, []);

  // Timer logic
  useEffect(() => {
    if (!timedMode || gameWon || gameLost) return;
    timerRef.current = setInterval(() => {
      setTimeRemaining(prev => {
        if (prev <= 1) {
          clearInterval(timerRef.current);
          setGameLost(true);
          if (onLose) onLose();
          return 0;
        }
        return prev - 1;
      });
      setTimeSpent(prev => prev + 1);
    }, 1000);
    return () => { if (timerRef.current) clearInterval(timerRef.current); };
  }, [timedMode, gameWon, gameLost, onLose]);

  useEffect(() => {
    if (!timedMode) {
      const interval = setInterval(() => {
        setTimeSpent(Math.floor((Date.now() - startTimeRef.current) / 1000));
      }, 1000);
      return () => clearInterval(interval);
    }
  }, [timedMode]);

  const cacheArtist = useCallback((artist) => {
    setArtistCache(prev => ({ ...prev, [artist.id]: artist }));
  }, []);

  // Fetch connected artists for current artist
  useEffect(() => {
    let cancelled = false;
    const fetchData = async () => {
      setLoading(true);
      setSearchQuery('');
      setSelectedArtist(null);
      setMatchingCollabs([]);
      setShowDropdown(false);
      const connected = await getConnectedArtists(currentArtist.id);
      if (!cancelled) {
        setConnectedArtists(connected);
        connected.forEach(a => cacheArtist(a));
        setLoading(false);
      }
    };
    fetchData();
    return () => { cancelled = true; };
  }, [currentArtist.id, cacheArtist]);

  // Hint logic
  useEffect(() => {
    if (!showHints || !showHint) { setHint(null); return; }
    let cancelled = false;
    const fetchHint = async () => {
      const path = await findConnection(currentArtist.id, artist2.id);
      if (!cancelled && path && path.length > 0) {
        const nextId = path[0].toArtist;
        const cached = artistCache[nextId];
        if (cached) { setHint(cached); }
        else {
          const artist = await getArtistById(nextId);
          if (!cancelled && artist) { setHint(artist); cacheArtist(artist); }
        }
      }
    };
    fetchHint();
    return () => { cancelled = true; };
  }, [currentArtist.id, artist2.id, showHints, showHint, artistCache, cacheArtist]);

  // Filter connected artists based on search
  const filteredArtists = searchQuery.length >= 1
    ? connectedArtists.filter(a =>
        a.name.toLowerCase().includes(searchQuery.toLowerCase())
      ).slice(0, 8)
    : [];

  // When user selects an artist from dropdown
  const handleSelectArtist = async (artist) => {
    setSelectedArtist(artist);
    setSearchQuery(artist.name);
    setShowDropdown(false);
    setLoadingCollabs(true);
    const collabs = await getCollaborationsBetween(currentArtist.id, artist.id);
    setMatchingCollabs(collabs);
    setLoadingCollabs(false);
  };

  // When user confirms the move with a specific collab
  const handleConfirmMove = (collab) => {
    const nextArtist = selectedArtist;
    const newChain = [...chain, { artist: nextArtist, collab }];
    setChain(newChain);
    setSelectedArtist(null);
    setSearchQuery('');
    setMatchingCollabs([]);
    cacheArtist(nextArtist);

    if (nextArtist.id === artist2.id) {
      setGameWon(true);
      if (timerRef.current) clearInterval(timerRef.current);
      if (onWin) onWin(newChain.length - 1, timeSpent);
    }
  };

  // Quick confirm if only 1 collab
  const handleQuickSelect = async (artist) => {
    setLoadingCollabs(true);
    const collabs = await getCollaborationsBetween(currentArtist.id, artist.id);
    setLoadingCollabs(false);
    if (collabs.length === 1) {
      // Auto-select the only collab
      const nextArtist = artist;
      const newChain = [...chain, { artist: nextArtist, collab: collabs[0] }];
      setChain(newChain);
      setSelectedArtist(null);
      setSearchQuery('');
      setMatchingCollabs([]);
      cacheArtist(nextArtist);
      if (nextArtist.id === artist2.id) {
        setGameWon(true);
        if (timerRef.current) clearInterval(timerRef.current);
        if (onWin) onWin(newChain.length - 1, timeSpent);
      }
    } else {
      setSelectedArtist(artist);
      setSearchQuery(artist.name);
      setShowDropdown(false);
      setMatchingCollabs(collabs);
    }
  };

  const handleClearSearch = () => {
    setSearchQuery('');
    setSelectedArtist(null);
    setMatchingCollabs([]);
    setShowDropdown(false);
    if (searchRef.current) searchRef.current.focus();
  };

  const handleUndo = () => {
    if (chain.length > 1) {
      setChain(chain.slice(0, -1));
      setSelectedArtist(null);
      setSearchQuery('');
      setMatchingCollabs([]);
      setGameWon(false);
    }
  };

  const handleRestart = () => {
    setChain([{ artist: artist1, collab: null }]);
    setSelectedArtist(null);
    setSearchQuery('');
    setMatchingCollabs([]);
    setGameWon(false);
    setGameLost(false);
    setShowHint(false);
    setTimeRemaining(timeLimit || 0);
    setTimeSpent(0);
    startTimeRef.current = Date.now();
  };

  const isWarning = timedMode && timeRemaining <= 30 && timeRemaining > 10;
  const isCritical = timedMode && timeRemaining <= 10;

  // Game Lost Screen
  if (gameLost) {
    return (
      <div className="game-board">
        <div className="game-lost" data-testid="game-lost-screen">
          <div className="lost-icon-wrap"><XCircle size={64} className="lost-icon" /></div>
          <h2 className="lost-title">Time's Up!</h2>
          <p className="lost-subtitle">You ran out of time trying to connect {artist1.name} to {artist2.name}</p>
          <div className="lost-stats">
            <div className="lost-stat"><span className="lost-stat-value">{chain.length - 1}</span><span className="lost-stat-label">Steps Taken</span></div>
            <div className="lost-stat"><span className="lost-stat-value">{currentArtist.name}</span><span className="lost-stat-label">Last Artist</span></div>
          </div>
          <div className="lost-chain"><h4>Your Progress:</h4><ConstellationGraph chain={chain} targetArtist={artist2} /></div>
          <div className="lost-actions">
            <button className="btn-primary" onClick={handleRestart}>Try Again</button>
            <button className="btn-secondary" onClick={onBack}>New Game</button>
          </div>
        </div>
      </div>
    );
  }

  // Game Won Screen
  if (gameWon) {
    const formatTime = (seconds) => {
      const mins = Math.floor(seconds / 60);
      const secs = seconds % 60;
      return mins > 0 ? `${mins}m ${secs}s` : `${secs}s`;
    };
    return (
      <div className="game-board">
        <div className="game-won" data-testid="game-won-screen">
          <div className="won-fireworks">
            {[...Array(12)].map((_, i) => (
              <div key={i} className="firework" style={{ '--delay': `${i * 0.15}s`, '--x': `${Math.random() * 100}%`, '--y': `${Math.random() * 60}%` }} />
            ))}
          </div>
          <h2 className="won-title">Connected!</h2>
          <p className="won-subtitle">
            You linked {artist1.name} to {artist2.name} in {chain.length - 1} step{chain.length - 1 !== 1 ? 's' : ''}
            {timedMode && <span className="won-time"> • {formatTime(timeSpent)}</span>}
          </p>
          <ConstellationGraph chain={chain} targetArtist={artist2} isVictory={true} />
          <div className="won-actions">
            <button className="btn-primary" onClick={onBack}>New Game</button>
            <button className="btn-secondary" onClick={handleRestart}>Play Again</button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="game-board">
      {/* Header bar */}
      <div className="game-header">
        <button className="game-back-btn" onClick={onBack}>
          <ArrowLeft size={18} /><span>BACK</span>
        </button>
        {timedMode && (
          <GameTimer timeRemaining={timeRemaining} timeLimit={timeLimit} isWarning={isWarning} isCritical={isCritical} />
        )}
        <div className="game-goal">
          <div className="goal-artist">
            <ArtistMiniAvatar artist={artist1} size={28} />
            <span>{artist1.name}</span>
          </div>
          <ArrowRight size={16} className="goal-arrow" />
          <div className="goal-artist">
            <ArtistMiniAvatar artist={artist2} size={28} />
            <span>{artist2.name}</span>
          </div>
        </div>
        <div className="game-controls">
          <span className="step-counter">Steps: {chain.length - 1}</span>
          {chain.length > 1 && (
            <button className="game-ctrl-btn" onClick={handleUndo} title="Undo"><RotateCcw size={16} /></button>
          )}
          {showHints && (
            <button className={`game-ctrl-btn ${showHint ? 'active' : ''}`} onClick={() => setShowHint(!showHint)} title="Hint">
              <Lightbulb size={16} />
            </button>
          )}
        </div>
      </div>

      {/* Chain graph */}
      {chain.length > 1 && <ConstellationGraph chain={chain} targetArtist={artist2} />}

      {/* Hint */}
      {showHint && hint && (
        <div className="hint-bar">
          <Lightbulb size={14} />
          <span>Try connecting through <strong>{hint.name}</strong></span>
        </div>
      )}

      {/* Current artist */}
      <div className="current-artist-section">
        <div className="current-avatar-large" style={{ borderColor: getGenreColor(currentArtist.genre) }}>
          <img src={getLargeAvatarUrl(currentArtist)} alt={currentArtist.name} className="current-avatar-img" onError={(e) => { e.target.style.display = 'none'; }} />
        </div>
        <h2 className="current-artist-name">{currentArtist.name}</h2>
        <p className="current-artist-genre">{currentArtist.genre}</p>
      </div>

      {loading ? (
        <div className="loading-section">
          <Loader2 size={24} className="spin-icon" />
          <span>Loading connections...</span>
        </div>
      ) : (
        <div className="search-section">
          <h3 className="section-title">WHO DID THEY COLLABORATE WITH?</h3>
          <p className="search-subtitle">Type an artist name to make your next move</p>

          {/* Search input */}
          <div className="search-input-wrapper">
            <Search size={18} className="search-icon" />
            <input
              ref={searchRef}
              type="text"
              placeholder="Search for a connected artist..."
              value={searchQuery}
              onChange={(e) => {
                setSearchQuery(e.target.value);
                setShowDropdown(true);
                if (selectedArtist && e.target.value !== selectedArtist.name) {
                  setSelectedArtist(null);
                  setMatchingCollabs([]);
                }
              }}
              onFocus={() => { if (searchQuery.length >= 1) setShowDropdown(true); }}
              className="game-search-input"
              autoComplete="off"
              autoCorrect="off"
              spellCheck="false"
            />
            {searchQuery && (
              <button className="search-clear-btn" onClick={handleClearSearch}>
                <X size={16} />
              </button>
            )}
          </div>

          {/* Autocomplete dropdown */}
          {showDropdown && filteredArtists.length > 0 && !selectedArtist && (
            <div className="search-dropdown" ref={dropdownRef}>
              {filteredArtists.map(artist => (
                <button
                  key={artist.id}
                  className={`search-dropdown-item ${artist.id === artist2.id ? 'target' : ''} ${showHint && hint && artist.id === hint.id ? 'hinted' : ''}`}
                  onClick={() => handleQuickSelect(artist)}
                >
                  <ArtistMiniAvatar artist={artist} size={36} />
                  <div className="dropdown-artist-info">
                    <span className="dropdown-artist-name">{artist.name}</span>
                    <span className="dropdown-artist-genre">{artist.genre}</span>
                  </div>
                  {artist.id === artist2.id && (
                    <div className="target-badge"><Check size={14} /><span>TARGET</span></div>
                  )}
                </button>
              ))}
            </div>
          )}

          {/* No results message */}
          {showDropdown && searchQuery.length >= 1 && filteredArtists.length === 0 && !selectedArtist && (
            <div className="search-no-results">
              <p>No connected artist found matching "{searchQuery}"</p>
              <p className="search-no-results-hint">Try a different name — they need to have a collaboration with {currentArtist.name}</p>
            </div>
          )}

          {/* Loading collabs */}
          {loadingCollabs && (
            <div className="loading-section" style={{ marginTop: '1rem' }}>
              <Loader2 size={20} className="spin-icon" />
              <span>Finding collaborations...</span>
            </div>
          )}

          {/* Show matching collaborations after selecting an artist */}
          {selectedArtist && matchingCollabs.length > 0 && (
            <div className="matching-collabs">
              <h4 className="collabs-header">
                Collaborations between {currentArtist.name} & {selectedArtist.name}
              </h4>
              <div className="collabs-list">
                {matchingCollabs.map(collab => (
                  <button
                    key={collab.id}
                    className="collab-list-item"
                    onClick={() => handleConfirmMove(collab)}
                  >
                    <div className="collab-list-icon">
                      {typeIcons[collab.type] || <Music size={14} />}
                    </div>
                    <div className="collab-list-info">
                      <span className="collab-list-title">{collab.title}</span>
                      <span className="collab-list-meta">{typeLabels[collab.type] || collab.type} • {collab.year}</span>
                    </div>
                    <ArrowRight size={16} className="collab-list-arrow" />
                  </button>
                ))}
              </div>
            </div>
          )}

          {/* Connected artists count */}
          <div className="connections-count">
            {connectedArtists.length} artists connected to {currentArtist.name}
          </div>
        </div>
      )}
    </div>
  );
};

export default GameBoard;
