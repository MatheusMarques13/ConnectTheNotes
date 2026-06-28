import React, { useState, useEffect, useCallback, useRef } from 'react';
import { ArrowLeft, ArrowRight, Music, Disc, Disc3, Radio, Mic2, Tv, Film, RotateCcw, Lightbulb, Check, Loader2, Clock, XCircle, Search, X, Flag, Share2 } from 'lucide-react';
import {
  getArtistSongs,
  findConnection,
  getArtistById,
} from '../services/api';
import { getAvatarUrl, getLargeAvatarUrl, getGenreColor } from '../utils/avatars';
import ConstellationGraph from './ConstellationGraph';

const typeIcons = {
  song: <Music size={14} />,
  album: <Disc size={14} />,
  ep: <Disc3 size={14} />,
  mixtape: <Disc3 size={14} />,
  live: <Radio size={14} />,
  dvd: <Tv size={14} />,
  video: <Film size={14} />,
  feature: <Mic2 size={14} />,
};

const typeLabels = {
  song: 'Song',
  album: 'Album',
  ep: 'EP',
  mixtape: 'Mixtape',
  live: 'Live',
  dvd: 'DVD',
  video: 'Music Video',
  feature: 'Feature',
};

const parLabel = (used, optimal) => {
  if (optimal == null) return null;
  if (used <= optimal) return 'Perfect — optimal path!';
  if (used <= optimal + 1) return 'Great';
  if (used <= optimal + 3) return 'Nice';
  return 'Connected';
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

const GameBoard = ({ artist1, artist2, optimalSteps, puzzleType, onBack, showHints, onWin, onLose, showGenres = true, timedMode, timeLimit, difficulty }) => {
  const [chain, setChain] = useState([{ artist: artist1, collab: null }]);
  const [gameWon, setGameWon] = useState(false);
  const [gameLost, setGameLost] = useState(false);
  const [gaveUp, setGaveUp] = useState(false);
  const [solutionChain, setSolutionChain] = useState(null);
  const [revealing, setRevealing] = useState(false);
  const [showHint, setShowHint] = useState(false);
  const [hint, setHint] = useState(null);
  const [hintStatus, setHintStatus] = useState('idle'); // idle|loading|found|none
  const [searchQuery, setSearchQuery] = useState('');
  const [copied, setCopied] = useState(false);

  const [songs, setSongs] = useState([]);
  const [loadError, setLoadError] = useState(false);
  const [loading, setLoading] = useState(false);
  const [artistCache, setArtistCache] = useState({});

  const [timeRemaining, setTimeRemaining] = useState(timeLimit || 0);
  const [timeSpent, setTimeSpent] = useState(0);
  const timerRef = useRef(null);
  const startTimeRef = useRef(Date.now());
  const searchRef = useRef(null);

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

  // Load the current artist's songs (each carries its collaborator)
  useEffect(() => {
    let cancelled = false;
    const fetchData = async () => {
      setLoading(true);
      setLoadError(false);
      setSearchQuery('');
      const list = await getArtistSongs(currentArtist.id);
      if (!cancelled) {
        setSongs(list);
        list.forEach(s => s.collaborators.forEach(c => cacheArtist(c)));
        setLoadError(list.length === 0);
        setLoading(false);
      }
    };
    fetchData();
    return () => { cancelled = true; };
  }, [currentArtist.id, cacheArtist]);

  // Hint logic — points at the next artist toward the target
  useEffect(() => {
    if (!showHints || !showHint) { setHint(null); setHintStatus('idle'); return; }
    let cancelled = false;
    const fetchHint = async () => {
      setHintStatus('loading');
      const { steps } = await findConnection(currentArtist.id, artist2.id);
      if (cancelled) return;
      if (steps && steps.length > 0) {
        const nextId = steps[0].toArtist;
        const cached = artistCache[nextId];
        if (cached) { setHint(cached); setHintStatus('found'); }
        else {
          const artist = await getArtistById(nextId);
          if (!cancelled && artist) { setHint(artist); cacheArtist(artist); setHintStatus('found'); }
        }
      } else {
        setHint(null);
        setHintStatus('none');
      }
    };
    fetchHint();
    return () => { cancelled = true; };
  }, [currentArtist.id, artist2.id, showHints, showHint, artistCache, cacheArtist]);

  // Filter songs by title OR any collaborator name
  const q = searchQuery.trim().toLowerCase();
  const filteredSongs = q
    ? songs.filter(s => s.title.toLowerCase().includes(q) || s.collaborators.some(c => c.name.toLowerCase().includes(q)))
    : songs;

  const targetIsNeighbor = songs.some(s => s.collaborators.some(c => c.id === artist2.id));

  const winWith = (newChain) => {
    setChain(newChain);
    setGameWon(true);
    if (timerRef.current) clearInterval(timerRef.current);
    if (onWin) onWin(newChain.length - 1, timeSpent);
  };

  // Pick a song + which collaborator to travel to (a track may credit several)
  const handlePick = (song, next) => {
    const newChain = [...chain, { artist: next, collab: { title: song.title, type: song.type, year: song.year, coverUrl: song.coverUrl } }];
    setSearchQuery('');
    cacheArtist(next);
    if (next.id === artist2.id) winWith(newChain);
    else setChain(newChain);
  };

  const handleClearSearch = () => {
    setSearchQuery('');
    if (searchRef.current) searchRef.current.focus();
  };

  const handleUndo = () => {
    if (chain.length > 1) {
      setChain(chain.slice(0, -1));
      setSearchQuery('');
    }
  };

  const handleGiveUp = async () => {
    if (revealing) return;
    setRevealing(true);
    const { chain: solChain } = await findConnection(artist1.id, artist2.id);
    setRevealing(false);
    if (solChain && solChain.length) setSolutionChain(solChain);
    setGaveUp(true);
    if (timerRef.current) clearInterval(timerRef.current);
    if (onLose) onLose();
  };

  const handleRestart = () => {
    setChain([{ artist: artist1, collab: null }]);
    setSearchQuery('');
    setGameWon(false);
    setGameLost(false);
    setGaveUp(false);
    setSolutionChain(null);
    setShowHint(false);
    setTimeRemaining(timeLimit || 0);
    setTimeSpent(0);
    startTimeRef.current = Date.now();
  };

  const buildShare = () => {
    const used = chain.length - 1;
    const head = puzzleType === 'daily' ? 'Connect the Notes — Daily' : 'Connect the Notes';
    const par = optimalSteps != null ? ` (best possible: ${optimalSteps})` : '';
    return `${head}\n${artist1.name} → ${artist2.name}\nSolved in ${used} song${used !== 1 ? 's' : ''}${par}\n${'🎵'.repeat(Math.min(used, 12))}`;
  };

  const handleShare = async () => {
    const text = buildShare();
    try {
      if (navigator.share) { await navigator.share({ text }); return; }
      await navigator.clipboard.writeText(text);
      setCopied(true);
      setTimeout(() => setCopied(false), 1800);
    } catch (e) { /* user cancelled */ }
  };

  const isWarning = timedMode && timeRemaining <= 30 && timeRemaining > 10;
  const isCritical = timedMode && timeRemaining <= 10;

  // Game Lost / Gave Up Screen
  if (gameLost || gaveUp) {
    return (
      <div className="game-board">
        <div className="game-lost" data-testid="game-lost-screen">
          <div className="lost-icon-wrap"><XCircle size={64} className="lost-icon" /></div>
          <h2 className="lost-title">{gaveUp ? 'Solution Revealed' : "Time's Up!"}</h2>
          <p className="lost-subtitle">
            {gaveUp
              ? `Here's one way to connect ${artist1.name} to ${artist2.name}:`
              : `You ran out of time trying to connect ${artist1.name} to ${artist2.name}`}
          </p>
          {gaveUp && solutionChain ? (
            <div className="lost-chain">
              <h4>Optimal path{optimalSteps != null ? ` · ${optimalSteps} songs` : ''}:</h4>
              <ConstellationGraph chain={solutionChain} targetArtist={artist2} isVictory={true} />
            </div>
          ) : (
            <>
              <div className="lost-stats">
                <div className="lost-stat"><span className="lost-stat-value">{chain.length - 1}</span><span className="lost-stat-label">Songs Played</span></div>
                <div className="lost-stat"><span className="lost-stat-value">{currentArtist.name}</span><span className="lost-stat-label">Last Artist</span></div>
              </div>
              <div className="lost-chain"><h4>Your Progress:</h4><ConstellationGraph chain={chain} targetArtist={artist2} /></div>
            </>
          )}
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
    const used = chain.length - 1;
    const rating = parLabel(used, optimalSteps);
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
              <div key={i} className="firework" style={{ '--delay': `${i * 0.15}s`, '--x': `${(i * 37) % 100}%`, '--y': `${(i * 23) % 60}%` }} />
            ))}
          </div>
          <h2 className="won-title">Connected!</h2>
          <p className="won-subtitle">
            You linked {artist1.name} to {artist2.name} in {used} song{used !== 1 ? 's' : ''}
            {timedMode && <span className="won-time"> • {formatTime(timeSpent)}</span>}
          </p>
          {rating && (
            <div className="won-par">
              <span className="won-par-rating">{rating}</span>
              {optimalSteps != null && (
                <span className="won-par-detail">You: {used} · Best possible: {optimalSteps}</span>
              )}
            </div>
          )}
          <ConstellationGraph chain={chain} targetArtist={artist2} isVictory={true} />
          <div className="won-actions">
            <button className="btn-secondary won-share" onClick={handleShare}>
              <Share2 size={16} /> {copied ? 'Copied!' : 'Share'}
            </button>
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
          <span className="step-counter">
            Songs: {chain.length - 1}{optimalSteps != null ? ` · par ${optimalSteps}` : ''}
          </span>
          {chain.length > 1 && (
            <button className="game-ctrl-btn" onClick={handleUndo} title="Undo"><RotateCcw size={16} /></button>
          )}
          {showHints && (
            <button className={`game-ctrl-btn ${showHint ? 'active' : ''}`} onClick={() => setShowHint(!showHint)} title="Hint">
              <Lightbulb size={16} />
            </button>
          )}
          <button className="game-ctrl-btn give-up-btn" onClick={handleGiveUp} title="Give up & reveal solution" disabled={revealing}>
            {revealing ? <Loader2 size={16} className="spin-icon" /> : <Flag size={16} />}
          </button>
        </div>
      </div>

      {/* Chain graph */}
      {chain.length > 1 && <ConstellationGraph chain={chain} targetArtist={artist2} />}

      {/* Target reachable banner */}
      {targetIsNeighbor && !loading && (
        <div className="target-near-banner">
          <Check size={14} /> <strong>{artist2.name}</strong> is one song away — find the track you both share!
        </div>
      )}

      {/* Hint */}
      {showHint && (
        <div className="hint-bar">
          <Lightbulb size={14} />
          {hintStatus === 'loading' && <span>Finding a route…</span>}
          {hintStatus === 'found' && hint && <span>Try a song with <strong>{hint.name}</strong></span>}
          {hintStatus === 'none' && <span>No route from here — try Undo to take another path.</span>}
        </div>
      )}

      {/* Current artist */}
      <div className="current-artist-section">
        <div className="current-avatar-large" style={{ borderColor: getGenreColor(currentArtist.genre) }}>
          <img src={getLargeAvatarUrl(currentArtist)} alt={currentArtist.name} className="current-avatar-img" onError={(e) => { e.target.style.display = 'none'; }} />
        </div>
        <h2 className="current-artist-name">{currentArtist.name}</h2>
        {showGenres && <p className="current-artist-genre">{currentArtist.genre}</p>}
      </div>

      {loading ? (
        <div className="loading-section">
          <Loader2 size={24} className="spin-icon" />
          <span>Loading songs...</span>
        </div>
      ) : loadError ? (
        <div className="dead-end-panel" data-testid="dead-end">
          <p className="dead-end-title">No songs found for {currentArtist.name}.</p>
          <p className="dead-end-hint">Undo to take another route.</p>
          <div className="dead-end-actions">
            {chain.length > 1 && <button className="btn-primary" onClick={handleUndo}>Undo last step</button>}
            <button className="btn-secondary" onClick={handleGiveUp}>Reveal solution</button>
          </div>
        </div>
      ) : (
        <div className="search-section">
          <h3 className="section-title">PICK A SONG BY {currentArtist.name.toUpperCase()}</h3>
          <p className="search-subtitle">Choose a track to travel to whoever they made it with</p>

          {/* Search input (by song title or collaborator) */}
          <div className="search-input-wrapper">
            <Search size={18} className="search-icon" />
            <input
              ref={searchRef}
              type="text"
              placeholder="Search a song or collaborator..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
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

          {/* Song list — pick a collaborator chip to travel via that track */}
          {filteredSongs.length > 0 ? (
            <div className="song-list">
              {filteredSongs.map(song => (
                <div key={song.id} className="song-item">
                  <div className="song-cover">
                    {song.coverUrl
                      ? <img src={song.coverUrl} alt="" className="song-cover-img" onError={(e) => { e.target.style.display = 'none'; }} />
                      : <span className="song-type-icon">{typeIcons[song.type] || <Music size={14} />}</span>}
                  </div>
                  <div className="song-info">
                    <span className="song-title">{song.title}</span>
                    <span className="song-meta">{typeLabels[song.type] || song.type} · {song.year}</span>
                  </div>
                  <div className="song-collabs">
                    {song.collaborators.map(c => {
                      const isTarget = c.id === artist2.id;
                      const isHinted = showHint && hint && c.id === hint.id;
                      return (
                        <button
                          key={c.id}
                          className={`collab-chip ${isTarget ? 'target' : ''} ${isHinted ? 'hinted' : ''}`}
                          onClick={() => handlePick(song, c)}
                          title={`Go to ${c.name}`}
                        >
                          <ArtistMiniAvatar artist={c} size={22} />
                          <span className="collab-chip-name">{c.name}</span>
                          {isTarget && <Check size={13} className="collab-chip-check" />}
                        </button>
                      );
                    })}
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="search-no-results">
              <p>No song or collaborator of {currentArtist.name} matches "{searchQuery}".</p>
              <p className="search-no-results-hint">Clear the search to see all their tracks, or use a hint.</p>
            </div>
          )}

          <div className="connections-count">
            {songs.length} song{songs.length !== 1 ? 's' : ''} by {currentArtist.name}
          </div>
        </div>
      )}
    </div>
  );
};

export default GameBoard;
