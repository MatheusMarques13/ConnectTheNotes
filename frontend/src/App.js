import React, { useState, useCallback, useEffect } from "react";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import "./App.css";
import "./components/GameBoard.css";
import StarryBackground from "./components/StarryBackground";
import ArtistCard from "./components/ArtistCard";
import HowToPlayModal from "./components/HowToPlayModal";
import OptionsModal from "./components/OptionsModal";
import GameBoard from "./components/GameBoard";
import { Info, Settings, Sparkles, Loader2, Calendar, Flame } from "lucide-react";
import { getStats, findConnection, getRandomPair, getDailyPuzzle } from "./services/api";

const DIFFICULTY_CONFIG = {
  easy: { timeLimit: 300, hintsEnabled: true, label: 'Easy', description: '5 min, hints on' },
  medium: { timeLimit: 180, hintsEnabled: true, label: 'Medium', description: '3 min, hints on' },
  hard: { timeLimit: 90, hintsEnabled: false, label: 'Hard', description: '90 sec, no hints' },
  expert: { timeLimit: 60, hintsEnabled: false, label: 'Expert', description: '60 sec, no hints' },
};

const DEFAULT_OPTIONS = {
  showGenres: true,
  showHints: true,
  timedMode: false,
  difficulty: 'medium',
  gamesPlayed: 0,
  gamesWon: 0,
  gamesLost: 0,
  bestScore: null,
  bestTime: null,
  dailyStreak: 0,
  lastDailyDate: null,
};

const STORAGE_KEY = 'ctn_options_v1';

function loadOptions() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (raw) return { ...DEFAULT_OPTIONS, ...JSON.parse(raw) };
  } catch (e) { /* ignore */ }
  return DEFAULT_OPTIONS;
}

function localDateStr(d = new Date()) {
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
}

function MainApp() {
  const [artist1, setArtist1] = useState(null);
  const [artist2, setArtist2] = useState(null);
  const [gameStarted, setGameStarted] = useState(false);
  const [optimalSteps, setOptimalSteps] = useState(null);
  const [puzzleType, setPuzzleType] = useState('free'); // 'free' | 'daily'
  const [checking, setChecking] = useState(false);
  const [startError, setStartError] = useState(null);
  const [surprising, setSurprising] = useState(false);

  const [showHowToPlay, setShowHowToPlay] = useState(false);
  const [showOptions, setShowOptions] = useState(false);
  const [options, setOptions] = useState(loadOptions);
  const [stats, setStats] = useState({ totalArtists: 0, totalSongs: 0 });
  const [daily, setDaily] = useState(null);

  const today = localDateStr();
  const dailyDoneToday = options.lastDailyDate === today;

  // Persist options/stats
  useEffect(() => {
    try { localStorage.setItem(STORAGE_KEY, JSON.stringify(options)); } catch (e) { /* ignore */ }
  }, [options]);

  useEffect(() => {
    getStats().then(s => setStats(s));
    getDailyPuzzle(today).then(d => setDaily(d));
  }, [today]);

  const beginGame = (a1, a2, optSteps, type) => {
    setArtist1(a1);
    setArtist2(a2);
    setOptimalSteps(optSteps);
    setPuzzleType(type);
    setStartError(null);
    setGameStarted(true);
  };

  const handleStartFree = async () => {
    if (!artist1 || !artist2 || checking) return;
    setChecking(true);
    setStartError(null);
    const { steps, optimalSteps: opt } = await findConnection(artist1.id, artist2.id);
    setChecking(false);
    if (steps === undefined) {
      setStartError("Couldn't reach the server. Check your connection and try again.");
      return;
    }
    if (steps === null) {
      setStartError(`No known connection between ${artist1.name} and ${artist2.name}. Try different artists or Surprise Me.`);
      return;
    }
    beginGame(artist1, artist2, opt, 'free');
  };

  const handleSurprise = async () => {
    if (surprising) return;
    setSurprising(true);
    setStartError(null);
    const pair = await getRandomPair(options.timedMode ? options.difficulty : 'any');
    setSurprising(false);
    if (pair && pair.artist1 && pair.artist2) {
      setArtist1(pair.artist1);
      setArtist2(pair.artist2);
      setOptimalSteps(pair.optimalSteps);
    } else {
      setStartError("Couldn't fetch a puzzle. Try again.");
    }
  };

  const handlePlayDaily = () => {
    if (daily && daily.artist1 && daily.artist2) {
      beginGame(daily.artist1, daily.artist2, daily.optimalSteps, 'daily');
    }
  };

  const handleBack = useCallback(() => {
    setGameStarted(false);
    setArtist1(null);
    setArtist2(null);
    setOptimalSteps(null);
    setStartError(null);
  }, []);

  const handleWin = useCallback(async (steps, timeSpent) => {
    setOptions(prev => {
      const next = {
        ...prev,
        gamesPlayed: prev.gamesPlayed + 1,
        gamesWon: prev.gamesWon + 1,
        bestScore: prev.bestScore === null ? steps : Math.min(prev.bestScore, steps),
        bestTime: prev.timedMode
          ? (prev.bestTime === null ? timeSpent : Math.min(prev.bestTime, timeSpent))
          : prev.bestTime,
      };
      if (puzzleType === 'daily' && prev.lastDailyDate !== today) {
        const yesterday = localDateStr(new Date(Date.now() - 86400000));
        next.dailyStreak = prev.lastDailyDate === yesterday ? (prev.dailyStreak || 0) + 1 : 1;
        next.lastDailyDate = today;
      }
      return next;
    });
  }, [puzzleType, today]);

  const handleLose = useCallback(async () => {
    setOptions(prev => ({
      ...prev,
      gamesPlayed: prev.gamesPlayed + 1,
      gamesLost: prev.gamesLost + 1,
    }));
  }, []);

  const getGameSettings = useCallback(() => {
    const diffConfig = DIFFICULTY_CONFIG[options.difficulty];
    return {
      timeLimit: options.timedMode ? diffConfig.timeLimit : null,
      hintsEnabled: options.timedMode ? diffConfig.hintsEnabled : options.showHints,
    };
  }, [options.timedMode, options.difficulty, options.showHints]);

  return (
    <div className="app-container">
      <StarryBackground />
      {!gameStarted ? (
        <div className="main-content">
          <div className="top-bar">
            <button className="top-btn" onClick={() => setShowHowToPlay(true)}>
              <Info size={18} />
              <span>HOW TO PLAY</span>
            </button>

            <div className="top-bar-right">
              <button className="top-btn" onClick={() => setShowOptions(true)}>
                <Settings size={18} />
                <span>OPTIONS</span>
              </button>
            </div>
          </div>

          <div className="logo-section">
            <div className="logo-diamond">
              <svg viewBox="0 0 100 100" className="diamond-svg">
                <polygon points="50,5 95,50 50,95 5,50" fill="none" stroke="currentColor" strokeWidth="1"/>
                <polygon points="50,15 85,50 50,85 15,50" fill="none" stroke="currentColor" strokeWidth="0.5" opacity="0.5"/>
              </svg>
            </div>
            <h1 className="main-title">Connect the Notes</h1>
            <p className="subtitle">CHOOSE TWO ARTISTS</p>
          </div>

          {/* Daily Puzzle */}
          {daily && daily.artist1 && daily.artist2 && (
            <div className="daily-banner">
              <div className="daily-banner-head">
                <Calendar size={15} />
                <span>TODAY'S PUZZLE</span>
                {options.dailyStreak > 0 && (
                  <span className="daily-streak"><Flame size={13} /> {options.dailyStreak}</span>
                )}
              </div>
              <div className="daily-pair">
                <span>{daily.artist1.name}</span>
                <span className="daily-arrow">→</span>
                <span>{daily.artist2.name}</span>
              </div>
              <button
                className={`daily-play-btn ${dailyDoneToday ? 'done' : ''}`}
                onClick={handlePlayDaily}
              >
                {dailyDoneToday ? '✓ PLAY AGAIN' : 'PLAY TODAY'}
              </button>
            </div>
          )}

          <div className="freeplay-label">OR PLAY FREELY</div>

          <div className="cards-container">
            <ArtistCard
              number={1}
              artist={artist1}
              onSelect={(a) => { setArtist1(a); setStartError(null); }}
              onClear={() => setArtist1(null)}
              excludeIds={artist2 ? [artist2.id] : []}
            />
            <ArtistCard
              number={2}
              artist={artist2}
              onSelect={(a) => { setArtist2(a); setStartError(null); }}
              onClear={() => setArtist2(null)}
              excludeIds={artist1 ? [artist1.id] : []}
            />
          </div>

          {startError && <div className="start-error" role="alert">{startError}</div>}

          <div className="start-actions">
            <button
              className={`start-game-btn ${artist1 && artist2 ? "ready" : ""}`}
              onClick={handleStartFree}
              disabled={!artist1 || !artist2 || checking}
            >
              <span className="btn-diamond" />
              {checking ? 'CHECKING…' : 'START GAME'}
            </button>
            <button className="surprise-btn" onClick={handleSurprise} disabled={surprising}>
              {surprising ? <Loader2 size={16} className="spin-icon" /> : <Sparkles size={16} />}
              <span>{surprising ? 'PICKING…' : 'SURPRISE ME'}</span>
            </button>
          </div>

          <div className="footer-stats">
            {stats.totalArtists} ARTISTS · {stats.totalSongs} SONGS
          </div>
        </div>
      ) : (
        <GameBoard
          artist1={artist1}
          artist2={artist2}
          optimalSteps={optimalSteps}
          puzzleType={puzzleType}
          onBack={handleBack}
          onHowToPlay={() => setShowHowToPlay(true)}
          showHints={getGameSettings().hintsEnabled}
          onWin={handleWin}
          onLose={handleLose}
          showGenres={options.showGenres}
          timedMode={options.timedMode}
          timeLimit={getGameSettings().timeLimit}
          difficulty={options.difficulty}
        />
      )}

      <HowToPlayModal isOpen={showHowToPlay} onClose={() => setShowHowToPlay(false)} />
      <OptionsModal
        isOpen={showOptions}
        onClose={() => setShowOptions(false)}
        options={options}
        onOptionsChange={setOptions}
        difficultyConfig={DIFFICULTY_CONFIG}
      />
    </div>
  );
}

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<MainApp />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
