import React, { useState, useEffect, useMemo, useRef } from 'react';
import { ArrowLeft, ArrowRight, RotateCcw, Lightbulb, Loader2, Clock, XCircle, Search, X, Flag, Share2 } from 'lucide-react';
import { nameSong, findConnection } from '../services/api';
import { getAvatarUrl } from '../utils/avatars';
import ConstellationGraph from './ConstellationGraph';

const parLabel = (used, optimal) => {
  if (optimal == null) return null;
  if (used <= optimal) return 'Perfect — optimal path!';
  if (used <= optimal + 1) return 'Great';
  if (used <= optimal + 3) return 'Nice';
  return 'Connected';
};

// Are two artists connected through the songs the player has named?
function connected(edges, a, b) {
  const parent = {};
  const find = (x) => {
    if (!(x in parent)) parent[x] = x;
    while (parent[x] !== x) { parent[x] = parent[parent[x]]; x = parent[x]; }
    return x;
  };
  const union = (x, y) => { const rx = find(x), ry = find(y); if (rx !== ry) parent[rx] = ry; };
  for (const e of edges) {
    const m = e.artistIds;
    for (let i = 1; i < m.length; i++) union(m[0], m[i]);
  }
  return find(a) === find(b);
}

// Turn a linear solution chain (from findConnection) into the web shape the
// constellation renders.
function chainToWeb(chain) {
  const found = chain.map((c) => c.artist).filter(Boolean);
  const edges = [];
  for (let i = 1; i < chain.length; i++) {
    edges.push({ song: chain[i].collab, artistIds: [chain[i - 1].artist.id, chain[i].artist.id] });
  }
  return { found, edges };
}

const ArtistMiniAvatar = ({ artist, size = 28, className = '' }) => {
  const [loaded, setLoaded] = useState(false);
  const name = typeof artist === 'string' ? artist : artist?.name || 'Unknown';
  const imageUrl = getAvatarUrl(artist, size);
  const initials = name.split(' ').map((w) => w[0]).join('').slice(0, 2).toUpperCase();
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
      <div className="timer-bar"><div className="timer-bar-fill" style={{ width: `${percentage}%` }} /></div>
    </div>
  );
};

const GameBoard = ({ artist1, artist2, optimalSteps, puzzleType, onBack, showHints, onWin, onLose, showGenres = true, timedMode, timeLimit, difficulty }) => {
  // The "web": the artists you've uncovered, and the songs you've named to link
  // them. Both endpoints are in play from the start — name a song by any of
  // them (or anyone you reveal) to grow the web until the two ends meet.
  const [found, setFound] = useState([artist1, artist2]);
  const [edges, setEdges] = useState([]);
  const [guess, setGuess] = useState('');
  const [guessError, setGuessError] = useState('');

  const [gameWon, setGameWon] = useState(false);
  const [gameLost, setGameLost] = useState(false);
  const [gaveUp, setGaveUp] = useState(false);
  const [solutionWeb, setSolutionWeb] = useState(null);
  const [revealing, setRevealing] = useState(false);

  const [showHint, setShowHint] = useState(false);
  const [hint, setHint] = useState(null);
  const [hintStatus, setHintStatus] = useState('idle'); // idle|loading|found|none
  const [copied, setCopied] = useState(false);

  const [timeRemaining, setTimeRemaining] = useState(timeLimit || 0);
  const [timeSpent, setTimeSpent] = useState(0);
  const timerRef = useRef(null);
  const startTimeRef = useRef(Date.now());
  const searchRef = useRef(null);

  const foundIds = useMemo(() => new Set(found.map((a) => a.id)), [found]);

  // Countdown timer
  useEffect(() => {
    if (!timedMode || gameWon || gameLost) return;
    timerRef.current = setInterval(() => {
      setTimeRemaining((prev) => {
        if (prev <= 1) { clearInterval(timerRef.current); setGameLost(true); if (onLose) onLose(); return 0; }
        return prev - 1;
      });
      setTimeSpent((prev) => prev + 1);
    }, 1000);
    return () => { if (timerRef.current) clearInterval(timerRef.current); };
  }, [timedMode, gameWon, gameLost, onLose]);

  useEffect(() => {
    if (!timedMode) {
      const interval = setInterval(() => setTimeSpent(Math.floor((Date.now() - startTimeRef.current) / 1000)), 1000);
      return () => clearInterval(interval);
    }
  }, [timedMode]);

  // Hint — the next artist on an optimal route that you haven't uncovered yet.
  useEffect(() => {
    if (!showHints || !showHint) { setHint(null); setHintStatus('idle'); return; }
    let cancelled = false;
    (async () => {
      setHintStatus('loading');
      const { chain } = await findConnection(artist1.id, artist2.id);
      if (cancelled) return;
      const next = chain && chain.map((c) => c.artist).find((a) => a && !foundIds.has(a.id));
      if (next) { setHint(next); setHintStatus('found'); }
      else { setHint(null); setHintStatus('none'); }
    })();
    return () => { cancelled = true; };
  }, [showHints, showHint, artist1.id, artist2.id, edges.length, foundIds]);

  const focusInput = () => { if (searchRef.current) searchRef.current.focus(); };

  const handleGuessSubmit = async (e) => {
    if (e) e.preventDefault();
    const raw = guess.trim();
    if (!raw) return;
    const res = await nameSong([...foundIds], raw);
    if (!res) {
      setGuessError(`No collaboration called “${raw}” by anyone you've found. Try another song.`);
      return;
    }
    if (edges.some((ed) => ed.song.id === res.song.id)) {
      setGuessError(`You've already played “${res.song.title}”.`);
      return;
    }
    const newArtists = res.artists.filter((a) => !foundIds.has(a.id));
    const newEdges = [...edges, { song: res.song, artistIds: res.artists.map((a) => a.id) }];
    setEdges(newEdges);
    setFound((prev) => [...prev, ...newArtists]);
    setGuess('');
    setGuessError('');
    if (connected(newEdges, artist1.id, artist2.id)) {
      setGameWon(true);
      if (timerRef.current) clearInterval(timerRef.current);
      if (onWin) onWin(newEdges.length, timeSpent);
    }
  };

  const handleClearGuess = () => { setGuess(''); setGuessError(''); focusInput(); };

  const handleUndo = () => {
    if (!edges.length) return;
    const newEdges = edges.slice(0, -1);
    const ids = new Set([artist1.id, artist2.id]);
    newEdges.forEach((e) => e.artistIds.forEach((id) => ids.add(id)));
    setEdges(newEdges);
    setFound((prev) => prev.filter((a) => ids.has(a.id)));
    setGuess('');
    setGuessError('');
  };

  const handleGiveUp = async () => {
    if (revealing) return;
    setRevealing(true);
    const { chain } = await findConnection(artist1.id, artist2.id);
    setRevealing(false);
    if (chain && chain.length) setSolutionWeb(chainToWeb(chain));
    setGaveUp(true);
    if (timerRef.current) clearInterval(timerRef.current);
    if (onLose) onLose();
  };

  const handleRestart = () => {
    setFound([artist1, artist2]);
    setEdges([]);
    setGuess('');
    setGuessError('');
    setGameWon(false);
    setGameLost(false);
    setGaveUp(false);
    setSolutionWeb(null);
    setShowHint(false);
    setTimeRemaining(timeLimit || 0);
    setTimeSpent(0);
    startTimeRef.current = Date.now();
  };

  const buildShare = () => {
    const used = edges.length;
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
    } catch (e) { /* cancelled */ }
  };

  const isWarning = timedMode && timeRemaining <= 30 && timeRemaining > 10;
  const isCritical = timedMode && timeRemaining <= 10;

  // ── Lost / Gave-up screen ───────────────────────────────
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
          {gaveUp && solutionWeb ? (
            <div className="lost-chain">
              <h4>Optimal path{optimalSteps != null ? ` · ${optimalSteps} songs` : ''}:</h4>
              <ConstellationGraph found={solutionWeb.found} edges={solutionWeb.edges} startId={artist1.id} targetId={artist2.id} isVictory />
            </div>
          ) : (
            <>
              <div className="lost-stats">
                <div className="lost-stat"><span className="lost-stat-value">{edges.length}</span><span className="lost-stat-label">Songs Played</span></div>
                <div className="lost-stat"><span className="lost-stat-value">{found.length}</span><span className="lost-stat-label">Artists Found</span></div>
              </div>
              <div className="lost-chain"><h4>Your Web:</h4><ConstellationGraph found={found} edges={edges} startId={artist1.id} targetId={artist2.id} /></div>
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

  // ── Win screen ──────────────────────────────────────────
  if (gameWon) {
    const used = edges.length;
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
              {optimalSteps != null && <span className="won-par-detail">You: {used} · Best possible: {optimalSteps}</span>}
            </div>
          )}
          <ConstellationGraph found={found} edges={edges} startId={artist1.id} targetId={artist2.id} isVictory />
          <div className="won-actions">
            <button className="btn-secondary won-share" onClick={handleShare}><Share2 size={16} /> {copied ? 'Copied!' : 'Share'}</button>
            <button className="btn-primary" onClick={onBack}>New Game</button>
            <button className="btn-secondary" onClick={handleRestart}>Play Again</button>
          </div>
        </div>
      </div>
    );
  }

  // ── Playing ─────────────────────────────────────────────
  return (
    <div className="game-board playing web">
      <div className="game-header">
        <button className="game-back-btn" onClick={onBack}><ArrowLeft size={18} /><span>BACK</span></button>
        {timedMode && <GameTimer timeRemaining={timeRemaining} timeLimit={timeLimit} isWarning={isWarning} isCritical={isCritical} />}
        <div className="game-goal">
          <div className="goal-artist"><ArtistMiniAvatar artist={artist1} size={28} /><span>{artist1.name}</span></div>
          <ArrowRight size={16} className="goal-arrow" />
          <div className="goal-artist"><ArtistMiniAvatar artist={artist2} size={28} /><span>{artist2.name}</span></div>
        </div>
        <div className="game-controls">
          <span className="step-counter">Songs: {edges.length}{optimalSteps != null ? ` · par ${optimalSteps}` : ''}</span>
          {edges.length > 0 && (
            <button className="game-ctrl-btn" onClick={handleUndo} title="Undo"><RotateCcw size={16} /></button>
          )}
          {showHints && (
            <button className={`game-ctrl-btn ${showHint ? 'active' : ''}`} onClick={() => setShowHint(!showHint)} title="Hint"><Lightbulb size={16} /></button>
          )}
          <button className="game-ctrl-btn give-up-btn" onClick={handleGiveUp} title="Give up & reveal solution" disabled={revealing}>
            {revealing ? <Loader2 size={16} className="spin-icon" /> : <Flag size={16} />}
          </button>
        </div>
      </div>

      <ConstellationGraph found={found} edges={edges} startId={artist1.id} targetId={artist2.id} />

      {showHint && (
        <div className="hint-bar">
          <Lightbulb size={14} />
          {hintStatus === 'loading' && <span>Finding a route…</span>}
          {hintStatus === 'found' && hint && <span>Try a song with <strong>{hint.name}</strong></span>}
          {hintStatus === 'none' && <span>You've already uncovered everyone on the best route — name the song that links them.</span>}
        </div>
      )}

      <div className="search-section guess-mode">
        <h3 className="section-title">NAME A SONG</h3>
        <p className="search-subtitle">
          Type a track by <strong>anyone you've found</strong> — either end or anyone in between — then press Enter. No list, recall it.
        </p>

        <form className="guess-form" onSubmit={handleGuessSubmit}>
          <div className={`search-input-wrapper ${guessError ? 'has-error' : ''}`}>
            <Search size={18} className="search-icon" />
            <input
              ref={searchRef}
              type="text"
              placeholder="Name a collaboration…"
              value={guess}
              onChange={(e) => { setGuess(e.target.value); if (guessError) setGuessError(''); }}
              className="game-search-input"
              autoComplete="off"
              autoCorrect="off"
              spellCheck="false"
              autoFocus
            />
            {guess && <button type="button" className="search-clear-btn" onClick={handleClearGuess}><X size={16} /></button>}
          </div>
          <button type="submit" className="guess-submit-btn" disabled={!guess.trim()}>Travel <ArrowRight size={16} /></button>
        </form>

        {guessError && <div className="guess-error" role="alert"><XCircle size={14} /> {guessError}</div>}

        <p className="guess-tip">
          {found.length} artist{found.length !== 1 ? 's' : ''} in play · stuck? use the <Lightbulb size={13} /> hint or <Flag size={13} /> to reveal.
        </p>
      </div>
    </div>
  );
};

export default GameBoard;
