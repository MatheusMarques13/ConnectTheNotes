import React, { useState, useEffect, useMemo, useRef } from 'react';
import { ChevronLeft, HelpCircle, Crosshair, Plus, Minus, MousePointerClick, Hand, ZoomIn, Music2, CornerDownLeft, AlertCircle, RotateCcw, Lightbulb, Loader2, Clock, XCircle, X, Flag, Share2, Moon, Sun } from 'lucide-react';
import { nameSong, findConnection } from '../services/api';
import ConstellationGraph from './ConstellationGraph';
import InteractiveBoard from './InteractiveBoard';
import InfoModal from './InfoModal';
import MyndLogo from './MyndLogo';
import * as preview from '../utils/preview';
import { useI18n } from '../i18n';

const parKey = (used, optimal) => {
  if (optimal == null) return null;
  if (used <= optimal) return 'rating_perfect';
  if (used <= optimal + 1) return 'rating_great';
  if (used <= optimal + 3) return 'rating_nice';
  return 'rating_connected';
};

// The path the player actually used to link the two stars: BFS over the named
// songs, returning start + alternating song→artist steps ending at the target.
function victoryTrail(edges, startId, targetId, artistById) {
  const adj = {};
  for (const e of edges) {
    const ids = e.artistIds;
    for (let i = 0; i < ids.length; i++) for (let j = 0; j < ids.length; j++) {
      if (i === j) continue;
      (adj[ids[i]] = adj[ids[i]] || []).push({ to: ids[j], song: e.song });
    }
  }
  const prev = { [startId]: null };
  const q = [startId]; let qi = 0;
  while (qi < q.length) {
    const cur = q[qi++];
    if (cur === targetId) break;
    for (const { to, song } of adj[cur] || []) if (!(to in prev)) { prev[to] = { from: cur, song }; q.push(to); }
  }
  if (!(targetId in prev)) return null;
  const steps = [];
  let cur = targetId;
  while (prev[cur]) { steps.unshift({ song: prev[cur].song, artist: artistById[cur] }); cur = prev[cur].from; }
  return { start: artistById[startId], steps };
}

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

const GameBoard = ({ artist1, artist2, optimalSteps, puzzleType, onBack, onHowToPlay, showHints, onWin, onLose, showGenres = true, timedMode, timeLimit, difficulty, darkMode, onToggleDark }) => {
  const { t } = useI18n();
  // The "web": the artists you've uncovered, and the songs you've named to link
  // them. Both endpoints are in play from the start — name a song by any of
  // them (or anyone you reveal) to grow the web until the two ends meet.
  const [found, setFound] = useState([artist1, artist2]);
  const [edges, setEdges] = useState([]);
  const [guess, setGuess] = useState('');
  const [guessError, setGuessError] = useState('');
  const [suggestion, setSuggestion] = useState(null);

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

  const tryName = async (raw) => {
    if (!raw) return;
    const res = await nameSong([...foundIds], raw);
    if (!res) {
      setSuggestion(null);
      setGuessError(t('no_collab', { q: raw }));
      return;
    }
    if (res.suggestion) {
      // typed almost right — offer the real title
      setSuggestion(res.suggestion);
      setGuessError('');
      return;
    }
    if (edges.some((ed) => ed.song.id === res.song.id)) {
      setSuggestion(null);
      setGuessError(t('already_played', { title: res.song.title }));
      return;
    }
    const newArtists = res.artists.filter((a) => !foundIds.has(a.id));
    const newEdges = [...edges, { song: res.song, artistIds: res.artists.map((a) => a.id) }];
    setEdges(newEdges);
    setFound((prev) => [...prev, ...newArtists]);
    setGuess('');
    setGuessError('');
    setSuggestion(null);
    // Seamlessly start the 30s preview the moment the song lands on the board.
    preview.play(res.song, (res.artists[0] && res.artists[0].name) || '');
    if (connected(newEdges, artist1.id, artist2.id)) {
      setGameWon(true);
      if (timerRef.current) clearInterval(timerRef.current);
      if (onWin) onWin(newEdges.length, timeSpent);
    }
  };

  const handleGuessSubmit = (e) => { if (e) e.preventDefault(); preview.unlock(); tryName(guess.trim()); };
  const acceptSuggestion = () => { if (suggestion) { setGuess(suggestion); tryName(suggestion); } };

  const handleClearGuess = () => { setGuess(''); setGuessError(''); setSuggestion(null); focusInput(); };

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
  const ratingKey = parKey(used, optimalSteps);
  const artistById = useMemo(() => { const m = {}; found.forEach((a) => { m[a.id] = a; }); return m; }, [found]);
  const trail = gameWon ? victoryTrail(edges, artist1.id, artist2.id, artistById) : null;
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
          <button className="ctn-btn-ghost ctn-back" onClick={onBack}><ChevronLeft size={16} /><span>{t('back')}</span></button>
        </div>
        <div className="ctn-brand">
          <div className="ctn-brand-logo"><MyndLogo className="ctn-brand-gem" size={20} /><span>Connect the Notes</span></div>
          <div className="ctn-brand-sub">
            {t('connect')} <span className="ctn-brand-endpoint start">{artist1.name}</span> {t('and')} <span className="ctn-brand-endpoint target">{artist2.name}</span>
          </div>
        </div>
        <div className="ctn-topbar-right">
          {timedMode && <GameTimer timeRemaining={timeRemaining} timeLimit={timeLimit} isWarning={isWarning} isCritical={isCritical} />}
          {edges.length > 0 && <button className="ctn-btn-ghost ctn-btn-icon" onClick={handleUndo} title={t('undo')}><RotateCcw size={16} /></button>}
          {showHints && <button className={`ctn-btn-ghost ctn-btn-icon ${showHint ? 'active' : ''}`} onClick={() => setShowHint(!showHint)} title={t('hint')}><Lightbulb size={16} /></button>}
          <button className="ctn-btn-ghost ctn-btn-icon" onClick={handleGiveUp} title={t('give_up')} disabled={revealing}>{revealing ? <Loader2 size={16} className="spin-icon" /> : <Flag size={16} />}</button>
          {onToggleDark && <button className="ctn-btn-ghost ctn-btn-icon" onClick={onToggleDark} title={darkMode ? t('light_mode') : t('dark_mode')}>{darkMode ? <Sun size={16} /> : <Moon size={16} />}</button>}
          <button className="ctn-btn-ghost ctn-help" onClick={onHowToPlay}><HelpCircle size={16} /><span>{t('how_to_play')}</span></button>
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
        <span className="ctn-hint"><MousePointerClick size={13} />{t('click_card')}</span>
        <span className="ctn-hint"><Hand size={13} />{t('drag_board')}</span>
        <span className="ctn-hint"><ZoomIn size={13} />{t('zoom_hint')}</span>
      </div>

      {/* Bottom input dock + status */}
      <div className="ctn-input-dock">
        {showHint && (
          <div className="ctn-input-error" style={{ background: 'rgba(184,198,224,.08)', borderColor: 'rgba(184,198,224,.25)', color: 'var(--diamond-light)' }} role="status">
            <Lightbulb size={14} />
            {hintStatus === 'loading' && <span>{t('finding_route')}</span>}
            {hintStatus === 'found' && hint && <span dangerouslySetInnerHTML={{ __html: t('try_song_with', { name: `<strong>${hint.name}</strong>` }) }} />}
            {hintStatus === 'none' && <span>{t('everyone_found')}</span>}
          </div>
        )}
        <div className="ctn-status">
          <div className="ctn-stat"><span className="ctn-stat-label">{t('artists_found')}</span><span className="ctn-stat-value" key={'a' + found.length}>{found.length}</span></div>
          <span className="ctn-stat-sep" />
          <div className="ctn-stat"><span className="ctn-stat-label">{t('songs_found')}</span><span className="ctn-stat-value" key={'s' + edges.length}>{edges.length}</span></div>
          <span className="ctn-stat-sep" />
          <div className="ctn-stat"><span className="ctn-stat-label">{t('best_path')}</span>
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
              placeholder={t('name_a_song')}
              value={guess}
              onChange={(e) => { setGuess(e.target.value); if (guessError) setGuessError(''); if (suggestion) setSuggestion(null); }}
              autoComplete="off"
              autoCorrect="off"
              spellCheck="false"
            />
            {guess && <button type="button" className="ctn-input-clear" onClick={handleClearGuess}><X size={16} /></button>}
          </div>
          <button type="submit" className="ctn-input-submit" disabled={!guess.trim()}>{t('play')} <CornerDownLeft size={16} /></button>
        </form>
        {suggestion && (
          <button type="button" className="ctn-suggest" onClick={acceptSuggestion}>
            {t('did_you_mean')} <strong>“{suggestion}”</strong>? <span className="ctn-suggest-use">{t('use_it')}</span>
          </button>
        )}
        {guessError && <div className="ctn-input-error" role="alert"><AlertCircle size={14} /> {guessError}</div>}
      </div>

      {infoNode && <InfoModal node={infoNode} onClose={() => setInfoNode(null)} />}

      {/* Win overlay — board stays mounted behind it (data-victory glow). */}
      {gameWon && (
        <div className="ctn-overlay win">
          <button className="ctn-overlay-close" onClick={onBack} aria-label={t('close')} title={t('close')}><X size={20} /></button>
          <div className="ctn-win-fireworks">
            {[...Array(14)].map((_, i) => (
              <div key={i} className="firework" style={{ '--delay': `${i * 0.13}s`, '--x': `${(i * 37) % 100}%`, '--y': `${(i * 23) % 70}%` }} />
            ))}
          </div>
          <h2 className="ctn-overlay-title">{t('connected')}</h2>
          <p className="ctn-overlay-sub">
            {t('you_linked', { a: artist1.name, b: artist2.name, n: used, songs: t(used !== 1 ? 'songs' : 'song') })}
            {timedMode && <span className="ctn-win-time"> · {fmtTime(timeSpent)}</span>}
          </p>
          {trail && (
            <div className="ctn-trail-wrap">
              <div className="ctn-trail-label">{t('your_trail')}</div>
              <div className="ctn-trail">
                <span className="ctn-trail-artist start">{trail.start?.name}</span>
                {trail.steps.map((s, i) => (
                  <React.Fragment key={i}>
                    <span className="ctn-trail-link"><Music2 size={11} /> {s.song.title}</span>
                    <span className={`ctn-trail-artist${i === trail.steps.length - 1 ? ' target' : ''}`}>{s.artist?.name}</span>
                  </React.Fragment>
                ))}
              </div>
            </div>
          )}
          {ratingKey && (
            <div className="ctn-overlay-par">
              <span className="rating">{t(ratingKey)}</span>
              {optimalSteps != null && <span className="detail">{t('you_best', { used, best: optimalSteps })}</span>}
            </div>
          )}
          <div className="ctn-overlay-actions">
            <button className="ctn-btn-primary" onClick={handleRestart}>{t('play_again')}</button>
            <button className="ctn-btn-secondary" onClick={handleShare}><Share2 size={16} /> {copied ? t('copied') : t('share')}</button>
            <button className="ctn-btn-secondary" onClick={onBack}>{t('new_game')}</button>
          </div>
        </div>
      )}

      {/* Lose / give-up overlay */}
      {(gameLost || gaveUp) && (
        <div className="ctn-overlay lose">
          <button className="ctn-overlay-close" onClick={onBack} aria-label={t('close')} title={t('close')}><X size={20} /></button>
          <XCircle size={56} className="ctn-lose-icon" />
          <h2 className="ctn-overlay-title">{gaveUp ? t('solution_revealed') : t('times_up')}</h2>
          <p className="ctn-overlay-sub">
            {gaveUp
              ? t('one_way', { a: artist1.name, b: artist2.name, par: optimalSteps != null ? t('in_n_songs', { n: optimalSteps }) : '' })
              : t('ran_out', { a: artist1.name, b: artist2.name })}
          </p>
          {gaveUp && solutionWeb && (
            <div className="ctn-overlay-solution">
              <ConstellationGraph found={solutionWeb.found} edges={solutionWeb.edges} startId={artist1.id} targetId={artist2.id} isVictory />
            </div>
          )}
          <div className="ctn-overlay-actions">
            <button className="ctn-btn-primary" onClick={handleRestart}>{t('try_again')}</button>
            <button className="ctn-btn-secondary" onClick={onBack}>{t('new_game')}</button>
          </div>
        </div>
      )}
    </div>
  );
};

export default GameBoard;
