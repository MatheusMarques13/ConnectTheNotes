import React, { useState, useEffect, useCallback, useRef } from 'react';
import { ArrowLeft, ArrowRight, Music, Disc, Radio, Mic2, RotateCcw, Lightbulb, Check, ChevronRight, Loader2, Clock, AlertTriangle, XCircle } from 'lucide-react';
import {
  getCollaborationsForArtist,
  getConnectedArtists,
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

const ArtistMiniAvatar = ({ name, size = 28, className = '' }) => {
  const [loaded, setLoaded] = useState(false);
  const initials = name.split(' ').map(w => w[0]).join('').slice(0, 2).toUpperCase();
  return (
    <div className={`mini-avatar ${className}`} style={{ width: size, height: size }}>
      <img
        src={getSmallAvatarUrl(name)}
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

// Timer Component
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
        <div 
          className="timer-bar-fill" 
          style={{ width: `${percentage}%` }}
        />
      </div>
    </div>
  );
};

const GameBoard = ({ artist1, artist2, onBack, showHints, onWin, onLose, timedMode, timeLimit, difficulty }) => {
  const [chain, setChain] = useState([{ artist: artist1, collab: null }]);
  const [selectedCollab, setSelectedCollab] = useState(null);
  const [gameWon, setGameWon] = useState(false);
  const [gameLost, setGameLost] = useState(false);
  const [showHint, setShowHint] = useState(false);
  const [hint, setHint] = useState(null);
  const [searchQuery, setSearchQuery] = useState('');

  const [availableCollabs, setAvailableCollabs] = useState([]);
  const [connectedArtists, setConnectedArtists] = useState([]);
  const [collabArtists, setCollabArtists] = useState([]);
  const [loading, setLoading] = useState(false);
  const [artistCache, setArtistCache] = useState({});

  // Timer state
  const [timeRemaining, setTimeRemaining] = useState(timeLimit || 0);
  const [timeSpent, setTimeSpent] = useState(0);
  const timerRef = useRef(null);
  const startTimeRef = useRef(Date.now());

  const currentArtist = chain[chain.length - 1].artist;

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

    return () => {
      if (timerRef.current) clearInterval(timerRef.current);
    };
  }, [timedMode, gameWon, gameLost, onLose]);

  // Calculate time spent on win (for non-timed mode tracking too)
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

  useEffect(() => {
    let cancelled = false;
    const fetchData = async () => {
      setLoading(true);
      const [collabs, connected] = await Promise.all([
        getCollaborationsForArtist(currentArtist.id),
        getConnectedArtists(currentArtist.id),
      ]);
      if (!cancelled) {
        setAvailableCollabs(collabs);
        setConnectedArtists(connected);
        connected.forEach(a => cacheArtist(a));
        setLoading(false);
      }
    };
    fetchData();
    return () => { cancelled = true; };
  }, [currentArtist.id, cacheArtist]);

  useEffect(() => {
    if (!showHints || !showHint) {
      setHint(null);
      return;
    }
    let cancelled = false;
    const fetchHint = async () => {
      const path = await findConnection(currentArtist.id, artist2.id);
      if (!cancelled && path && path.length > 0) {
        const nextId = path[0].toArtist;
        const cached = artistCache[nextId];
        if (cached) {
          setHint(cached);
        } else {
          const artist = await getArtistById(nextId);
          if (!cancelled && artist) {
            setHint(artist);
            cacheArtist(artist);
          }
        }
      }
    };
    fetchHint();
    return () => { cancelled = true; };
  }, [currentArtist.id, artist2.id, showHints, showHint, artistCache, cacheArtist]);

  useEffect(() => {
    if (!selectedCollab) {
      setCollabArtists([]);
      return;
    }
    const otherIds = selectedCollab.artistIds.filter(id => id !== currentArtist.id);
    const artists = otherIds.map(id => {
      return connectedArtists.find(a => a.id === id) || artistCache[id] || null;
    }).filter(Boolean);
    setCollabArtists(artists);
  }, [selectedCollab, currentArtist.id, connectedArtists, artistCache]);

  const handleSelectCollab = (collab) => {
    setSelectedCollab(collab);
    setSearchQuery('');
  };

  const handleSelectNextArtist = (nextArtist) => {
    const newChain = [...chain, { artist: nextArtist, collab: selectedCollab }];
    setChain(newChain);
    setSelectedCollab(null);
    setSearchQuery('');
    cacheArtist(nextArtist);

    if (nextArtist.id === artist2.id) {
      setGameWon(true);
      if (timerRef.current) clearInterval(timerRef.current);
      if (onWin) onWin(newChain.length - 1, timeSpent);
    }
  };

  const handleUndo = () => {
    if (chain.length > 1) {
      setChain(chain.slice(0, -1));
      setSelectedCollab(null);
      setGameWon(false);
    }
  };

  const handleRestart = () => {
    setChain([{ artist: artist1, collab: null }]);
    setSelectedCollab(null);
    setGameWon(false);
    setGameLost(false);
    setShowHint(false);
    setTimeRemaining(timeLimit || 0);
    setTimeSpent(0);
    startTimeRef.current = Date.now();
  };

  const getArtistsForCollab = (collab) => {
    return collab.artistIds
      .filter(id => id !== currentArtist.id)
      .map(id => connectedArtists.find(a => a.id === id) || artistCache[id])
      .filter(Boolean);
  };

  const filteredCollabArtists = searchQuery
    ? collabArtists.filter(a => a.name.toLowerCase().includes(searchQuery.toLowerCase()))
    : collabArtists;

  const isWarning = timedMode && timeRemaining <= 30 && timeRemaining > 10;
  const isCritical = timedMode && timeRemaining <= 10;

  // Game Lost Screen (Time's Up)
  if (gameLost) {
    return (
      <div className="game-board">
        <div className="game-lost" data-testid="game-lost-screen">
          <div className="lost-icon-wrap">
            <XCircle size={64} className="lost-icon" />
          </div>
          <h2 className="lost-title">Time's Up!</h2>
          <p className="lost-subtitle">
            You ran out of time trying to connect {artist1.name} to {artist2.name}
          </p>
          <div className="lost-stats">
            <div className="lost-stat">
              <span className="lost-stat-value">{chain.length - 1}</span>
              <span className="lost-stat-label">Steps Taken</span>
            </div>
            <div className="lost-stat">
              <span className="lost-stat-value">{currentArtist.name}</span>
              <span className="lost-stat-label">Last Artist</span>
            </div>
          </div>
          <div className="lost-chain">
            <h4>Your Progress:</h4>
            <ConstellationGraph chain={chain} targetArtist={artist2} />
          </div>
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
              <div key={i} className="firework" style={{
                '--delay': `${i * 0.15}s`,
                '--x': `${Math.random() * 100}%`,
                '--y': `${Math.random() * 60}%`,
              }} />
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
          <ArrowLeft size={18} />
          <span>BACK</span>
        </button>
        
        {/* Timer (if timed mode) */}
        {timedMode && (
          <GameTimer 
            timeRemaining={timeRemaining}
            timeLimit={timeLimit}
            isWarning={isWarning}
            isCritical={isCritical}
          />
        )}
        
        <div className="game-goal">
          <div className="goal-artist">
            <ArtistMiniAvatar name={artist1.name} size={28} />
            <span>{artist1.name}</span>
          </div>
          <ArrowRight size={16} className="goal-arrow" />
          <div className="goal-artist">
            <ArtistMiniAvatar name={artist2.name} size={28} />
            <span>{artist2.name}</span>
          </div>
        </div>
        <div className="game-controls">
          <span className="step-counter">Steps: {chain.length - 1}</span>
          {chain.length > 1 && (
            <button className="game-ctrl-btn" onClick={handleUndo} title="Undo">
              <RotateCcw size={16} />
            </button>
          )}
          {showHints && (
            <button
              className={`game-ctrl-btn ${showHint ? 'active' : ''}`}
              onClick={() => setShowHint(!showHint)}
              title="Hint"
            >
              <Lightbulb size={16} />
            </button>
          )}
        </div>
      </div>

      {/* Chain so far */}
      {chain.length > 1 && (
        <ConstellationGraph chain={chain} targetArtist={artist2} />
      )}

      {/* Hint display */}
      {showHint && hint && (
        <div className="hint-bar">
          <Lightbulb size={14} />
          <span>Try connecting through <strong>{hint.name}</strong></span>
        </div>
      )}

      {/* Current artist display */}
      <div className="current-artist-section">
        <div className="current-avatar-large" style={{ borderColor: getGenreColor(currentArtist.genre) }}>
          <img
            src={getLargeAvatarUrl(currentArtist.name)}
            alt={currentArtist.name}
            className="current-avatar-img"
            onError={(e) => { e.target.style.display = 'none'; }}
          />
        </div>
        <h2 className="current-artist-name">{currentArtist.name}</h2>
        <p className="current-artist-genre">{currentArtist.genre}</p>
      </div>

      {loading ? (
        <div className="loading-section">
          <Loader2 size={24} className="spin-icon" />
          <span>Loading collaborations...</span>
        </div>
      ) : !selectedCollab ? (
        <div className="collab-section">
          <h3 className="section-title">SELECT A COLLABORATION</h3>
          {availableCollabs.length === 0 ? (
            <div className="empty-state">
              <p>No collaborations found for this artist. Try undoing your last step.</p>
            </div>
          ) : (
            <div className="collab-grid">
              {availableCollabs.map(collab => {
                const otherArtists = getArtistsForCollab(collab);
                return (
                  <button
                    key={collab.id}
                    className="collab-card"
                    onClick={() => handleSelectCollab(collab)}
                  >
                    <div className="collab-card-top">
                      <div className="collab-type-badge">
                        {typeIcons[collab.type]}
                        <span>{typeLabels[collab.type] || collab.type}</span>
                      </div>
                      <div className="collab-artists-avatars">
                        {otherArtists.slice(0, 2).map(a => (
                          <ArtistMiniAvatar key={a.id} name={a.name} size={24} className="collab-mini-av" />
                        ))}
                      </div>
                    </div>
                    <div className="collab-title">{collab.title}</div>
                    <div className="collab-year">{collab.year}</div>
                    <div className="collab-with">
                      with {otherArtists.map(a => a.name).join(', ') || '...'}
                    </div>
                  </button>
                );
              })}
            </div>
          )}
        </div>
      ) : (
        <div className="next-artist-section">
          <div className="selected-collab-display">
            <div className="collab-type-badge">
              {typeIcons[selectedCollab.type]}
              <span>{typeLabels[selectedCollab.type] || selectedCollab.type}</span>
            </div>
            <span className="selected-collab-title">{selectedCollab.title} ({selectedCollab.year})</span>
            <button className="change-collab-btn" onClick={() => setSelectedCollab(null)}>Change</button>
          </div>
          <h3 className="section-title">SELECT NEXT ARTIST</h3>
          {collabArtists.length > 3 && (
            <div className="next-artist-search">
              <input
                type="text"
                placeholder="Search connected artist..."
                value={searchQuery}
                onChange={e => setSearchQuery(e.target.value)}
                className="artist-search-input"
              />
            </div>
          )}
          <div className="next-artist-grid">
            {filteredCollabArtists.map(artist => (
              <button
                key={artist.id}
                className={`next-artist-card ${artist.id === artist2.id ? 'target' : ''} ${showHint && hint && artist.id === hint.id ? 'hinted' : ''}`}
                onClick={() => handleSelectNextArtist(artist)}
              >
                <ArtistMiniAvatar name={artist.name} size={40} />
                <div className="next-artist-info">
                  <span className="next-artist-name">{artist.name}</span>
                  <span className="next-artist-genre">{artist.genre}</span>
                </div>
                {artist.id === artist2.id && (
                  <div className="target-badge">
                    <Check size={14} />
                    <span>TARGET</span>
                  </div>
                )}
              </button>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default GameBoard;
