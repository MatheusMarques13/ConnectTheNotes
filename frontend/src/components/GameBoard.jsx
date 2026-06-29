import React, { useState, useEffect, useMemo, useRef } from 'react';
import { ChevronLeft, HelpCircle, Crosshair, Plus, Minus, MousePointerClick, Hand, ZoomIn, Music2, CornerDownLeft, AlertCircle, RotateCcw, Lightbulb, Loader2, Clock, XCircle, X, Flag, Share2 } from 'lucide-react';
import { nameSong, findConnection } from '../services/api';
import ConstellationGraph from './ConstellationGraph';
import InteractiveBoard from './InteractiveBoard';
import InfoModal from './InfoModal';
import MyndLogo from './MyndLogo';

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

const GameBoard = ({ artist1, artist2, optimalSteps, puzzleType, onBack, onHowToPlay, showHints, onWin, onLose, showGenres = true, timedMode, timeLimit, difficulty }) => {
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
  const [infoNode, setInfoNode] = useState(null);
  const boardApiRef = useRef(null);

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

  // Focus the input on desktop only — don't pop the soft keyboard over a touch board.
  useEffect(() => {
    if (window.matchMedia && window.matchMedia('(pointer: fine)').matches) searchRef.current?.focus();
  }, []);

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
  const used = edges.length;
  const rating = parLabel(used, optimalSteps);
  const fmtTime = (s) => { const m = Math.floor(s / 60); const r = s % 60; return m > 0 ? `${m}m ${r}s` : `${r}s`; };
  const atPar = gameWon && optimalSteps != null && used <= optimalSteps;

  // ── Full-screen board (overlays handle win / lose on top of it) ─────────
  return (
    <div className="ctn-board-root game-board ctn-fullbleed" data-victory={gameWon || undefined}>
      <InteractiveBoard
        found={found}
        edges={edges}
        startId={artist1.id}
        targetId={artist2.id}
        onOpenInfo={setInfoNode}
        boardApiRef={boardApiRef}
      />

      {/* Top bar */}
      <header className="ctn-topbar">
        <div className="ctn-topbar-left">
          <button className="ctn-btn-ghost ctn-back" onClick={onBack}><ChevronLeft size={16} /><span>BACK</span></button>
        </div>
        <div className="ctn-brand">
          <div className="ctn-brand-logo"><MyndLogo className="ctn-brand-gem" size={20} /><span>Connect the Notes</span></div>
          <div className="ctn-brand-sub">
            CONNECT <span className="ctn-brand-endpoint start">{artist1.name}</span> AND <span className="ctn-brand-endpoint target">{artist2.name}</span>
          </div>
        </div>
        <div className="ctn-topbar-right">
          {timedMode && <GameTimer timeRemaining={timeRemaining} timeLimit={timeLimit} isWarning={isWarning} isCritical={isCritical} />}
          {edges.length > 0 && <button className="ctn-btn-ghost ctn-btn-icon" onClick={handleUndo} title="Undo last song"><RotateCcw size={16} /></button>}
          {showHints && <button className={`ctn-btn-ghost ctn-btn-icon ${showHint ? 'active' : ''}`} onClick={() => setShowHint(!showHint)} title="Hint"><Lightbulb size={16} /></button>}
          <button className="ctn-btn-ghost ctn-btn-icon" onClick={handleGiveUp} title="Give up & reveal solution" disabled={revealing}>{revealing ? <Loader2 size={16} className="spin-icon" /> : <Flag size={16} />}</button>
          <button className="ctn-btn-ghost ctn-help" onClick={onHowToPlay}><HelpCircle size={16} /><span>HOW TO PLAY</span></button>
        </div>
      </header>

      {/* Recenter + zoom (bottom-left) */}
      <button className="ctn-recenter" onClick={() => boardApiRef.current?.recenter()} aria-label="Recenter board"><Crosshair size={20} /></button>
      <div className="ctn-zoom">
        <button onClick={() => boardApiRef.current?.zoomBy(1.2)} aria-label="Zoom in"><Plus size={16} /></button>
        <span className="ctn-zoom-div" />
        <button onClick={() => boardApiRef.current?.zoomBy(1 / 1.2)} aria-label="Zoom out"><Minus size={16} /></button>
      </div>

      {/* Helper hints (bottom-right) */}
      <div className={`ctn-hints${edges.length > 0 ? ' dismissed' : ''}`}>
        <span className="ctn-hint"><MousePointerClick size={13} />CLICK A CARD FOR MORE INFO</span>
        <span className="ctn-hint"><Hand size={13} />DRAG THE BOARD OR A CARD</span>
        <span className="ctn-hint"><ZoomIn size={13} />ZOOM IN / OUT</span>
      </div>

      {/* Bottom input dock + status */}
      <div className="ctn-input-dock">
        {showHint && (
          <div className="ctn-input-error" style={{ background: 'rgba(184,198,224,.08)', borderColor: 'rgba(184,198,224,.25)', color: 'var(--diamond-light)' }} role="status">
            <Lightbulb size={14} />
            {hintStatus === 'loading' && <span>Finding a route…</span>}
            {hintStatus === 'found' && hint && <span>Try a song with <strong>{hint.name}</strong></span>}
            {hintStatus === 'none' && <span>You've uncovered everyone on the best route — name the song that links them.</span>}
          </div>
        )}
        <div className="ctn-status">
          <div className="ctn-stat"><span className="ctn-stat-label">Artists Found</span><span className="ctn-stat-value" key={'a' + found.length}>{found.length}</span></div>
          <span className="ctn-stat-sep" />
          <div className="ctn-stat"><span className="ctn-stat-label">Songs Found</span><span className="ctn-stat-value" key={'s' + edges.length}>{edges.length}</span></div>
          <span className="ctn-stat-sep" />
          <div className="ctn-stat"><span className="ctn-stat-label">My Best Path</span>
            {optimalSteps != null
              ? <span className={`ctn-stat-value${atPar ? ' is-par' : ''}`}>{optimalSteps}</span>
              : <span className="ctn-stat-value ctn-unknown">???</span>}
          </div>
        </div>

        <form className="ctn-input-form" onSubmit={handleGuessSubmit}>
          <div className={`ctn-input-wrap${guessError ? ' has-error' : ''}`}>
            <Music2 size={18} className="ctn-input-icon" />
            <input
              ref={searchRef}
              className="ctn-input"
              placeholder="Name a song..."
              value={guess}
              onChange={(e) => { setGuess(e.target.value); if (guessError) setGuessError(''); }}
              autoComplete="off"
              autoCorrect="off"
              spellCheck="false"
            />
            {guess && <button type="button" className="ctn-input-clear" onClick={handleClearGuess}><X size={16} /></button>}
          </div>
          <button type="submit" className="ctn-input-submit" disabled={!guess.trim()}>PLAY <CornerDownLeft size={16} /></button>
        </form>
        {guessError && <div className="ctn-input-error" role="alert"><AlertCircle size={14} /> {guessError}</div>}
      </div>

      {infoNode && <InfoModal node={infoNode} onClose={() => setInfoNode(null)} />}

      {/* Win overlay — board stays mounted behind it (data-victory glow). */}
      {gameWon && (
        <div className="ctn-overlay win">
          <div className="ctn-win-fireworks">
            {[...Array(14)].map((_, i) => (
              <div key={i} className="firework" style={{ '--delay': `${i * 0.13}s`, '--x': `${(i * 37) % 100}%`, '--y': `${(i * 23) % 70}%` }} />
            ))}
          </div>
          <h2 className="ctn-overlay-title">Connected!</h2>
          <p className="ctn-overlay-sub">
            You linked {artist1.name} to {artist2.name} in {used} song{used !== 1 ? 's' : ''}
            {timedMode && <span className="ctn-win-time"> · {fmtTime(timeSpent)}</span>}
          </p>
          {rating && (
            <div className="ctn-overlay-par">
              <span className="rating">{rating}</span>
              {optimalSteps != null && <span className="detail">You: {used} · Best possible: {optimalSteps}</span>}
            </div>
          )}
          <div className="ctn-overlay-actions">
            <button className="ctn-btn-primary" onClick={handleRestart}>Play Again</button>
            <button className="ctn-btn-secondary" onClick={handleShare}><Share2 size={16} /> {copied ? 'Copied!' : 'Share'}</button>
            <button className="ctn-btn-secondary" onClick={onBack}>New Game</button>
          </div>
        </div>
      )}

      {/* Lose / give-up overlay */}
      {(gameLost || gaveUp) && (
        <div className="ctn-overlay lose">
          <XCircle size={56} className="ctn-lose-icon" />
          <h2 className="ctn-overlay-title">{gaveUp ? 'Solution Revealed' : "Time's Up!"}</h2>
          <p className="ctn-overlay-sub">
            {gaveUp
              ? `One way to connect ${artist1.name} and ${artist2.name}${optimalSteps != null ? ` in ${optimalSteps} songs` : ''}:`
              : `You ran out of time connecting ${artist1.name} to ${artist2.name}.`}
          </p>
          {gaveUp && solutionWeb && (
            <div className="ctn-overlay-solution">
              <ConstellationGraph found={solutionWeb.found} edges={solutionWeb.edges} startId={artist1.id} targetId={artist2.id} isVictory />
            </div>
          )}
          <div className="ctn-overlay-actions">
            <button className="ctn-btn-primary" onClick={handleRestart}>Try Again</button>
            <button className="ctn-btn-secondary" onClick={onBack}>New Game</button>
          </div>
        </div>
      )}
    </div>
  );
};

export default GameBoard;
