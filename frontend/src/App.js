import React, { useState, useCallback, useEffect } from "react";
import { BrowserRouter } from "react-router-dom";
import "./App.css";
import StarryBackground from "./components/StarryBackground";
import ArtistCard from "./components/ArtistCard";
import HowToPlayModal from "./components/HowToPlayModal";
import OptionsModal from "./components/OptionsModal";
import GameBoard from "./components/GameBoard";
import UserMenu from "./components/UserMenu";
import LeaderboardModal from "./components/LeaderboardModal";
import GameHistoryModal from "./components/GameHistoryModal";
import { Info, Settings, Trophy } from "lucide-react";
import { getStats } from "./services/api";

const DIFFICULTY_CONFIG = {
  easy: { timeLimit: 300, hintsEnabled: true, label: 'Easy', description: '5 min, hints on' },
  medium: { timeLimit: 180, hintsEnabled: true, label: 'Medium', description: '3 min, hints on' },
  hard: { timeLimit: 90, hintsEnabled: false, label: 'Hard', description: '90 sec, no hints' },
  expert: { timeLimit: 60, hintsEnabled: false, label: 'Expert', description: '60 sec, no hints' },
};

function MainApp() {
  const [artist1, setArtist1] = useState(null);
  const [artist2, setArtist2] = useState(null);
  const [gameStarted, setGameStarted] = useState(false);
  const [showHowToPlay, setShowHowToPlay] = useState(false);
  const [showOptions, setShowOptions] = useState(false);
  const [showLeaderboard, setShowLeaderboard] = useState(false);
  const [showHistory, setShowHistory] = useState(false);
  const [options, setOptions] = useState({
    sound: true,
    showGenres: true,
    showHints: true,
    timedMode: false,
    difficulty: 'medium',
    gamesPlayed: 0,
    gamesWon: 0,
    gamesLost: 0,
    bestScore: null,
    bestTime: null,
  });
  const [stats, setStats] = useState({ totalArtists: 0, totalCollaborations: 0 });

  useEffect(() => {
    getStats().then(s => setStats(s));
  }, []);

  const handleStartGame = () => {
    if (artist1 && artist2) {
      setGameStarted(true);
      setOptions(prev => ({ ...prev, gamesPlayed: prev.gamesPlayed + 1 }));
    }
  };

  const handleBack = useCallback(() => {
    setGameStarted(false);
    setArtist1(null);
    setArtist2(null);
  }, []);

  const handleWin = useCallback(async (steps, timeSpent) => {
    setOptions(prev => ({
      ...prev,
      gamesWon: prev.gamesWon + 1,
      bestScore: prev.bestScore === null ? steps : Math.min(prev.bestScore, steps),
      bestTime: options.timedMode 
        ? (prev.bestTime === null ? timeSpent : Math.min(prev.bestTime, timeSpent))
        : prev.bestTime,
    }));
  }, [options.timedMode]);

  const handleLose = useCallback(async () => {
    setOptions(prev => ({
      ...prev,
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
              <button className="top-btn" onClick={() => setShowLeaderboard(true)} data-testid="leaderboard-btn">
                <Trophy size={18} />
                <span>LEADERBOARD</span>
              </button>
              <button className="top-btn" onClick={() => setShowOptions(true)}>
                <Settings size={18} />
                <span>OPTIONS</span>
              </button>
              <UserMenu />
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

          <div className="cards-container">
            <ArtistCard
              number={1}
              artist={artist1}
              onSelect={setArtist1}
              onClear={() => setArtist1(null)}
              excludeIds={artist2 ? [artist2.id] : []}
            />
            <ArtistCard
              number={2}
              artist={artist2}
              onSelect={setArtist2}
              onClear={() => setArtist2(null)}
              excludeIds={artist1 ? [artist1.id] : []}
            />
          </div>

          <button
            className={`start-game-btn ${artist1 && artist2 ? "ready" : ""}`}
            onClick={handleStartGame}
            disabled={!artist1 || !artist2}
          >
            <span className="btn-diamond" />
            START GAME
          </button>

          <div className="footer-stats">
            {stats.totalArtists} ARTISTS · {stats.totalCollaborations} CONNECTIONS
          </div>
        </div>
      ) : (
        <GameBoard
          artist1={artist1}
          artist2={artist2}
          onBack={handleBack}
          showHints={getGameSettings().hintsEnabled}
          onWin={handleWin}
          onLose={handleLose}
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
      <LeaderboardModal 
        isOpen={showLeaderboard} 
        onClose={() => setShowLeaderboard(false)} 
        currentUser={null}
      />
      <GameHistoryModal
        isOpen={showHistory}
        onClose={() => setShowHistory(false)}
        currentUser={null}
      />
    </div>
  );
}

function App() {
  return (
    <BrowserRouter>
      <MainApp />
    </BrowserRouter>
  );
}

export default App;
