import React, { useState, useCallback, useEffect } from "react";
import "./App.css";
import StarryBackground from "./components/StarryBackground";
import ArtistCard from "./components/ArtistCard";
import HowToPlayModal from "./components/HowToPlayModal";
import OptionsModal from "./components/OptionsModal";
import GameBoard from "./components/GameBoard";
import { Info, Settings } from "lucide-react";
import { getStats } from "./services/api";

// Difficulty settings configuration
const DIFFICULTY_CONFIG = {
  easy: { timeLimit: 300, hintsEnabled: true, label: 'Easy', description: '5 min, hints on' },
  medium: { timeLimit: 180, hintsEnabled: true, label: 'Medium', description: '3 min, hints on' },
  hard: { timeLimit: 90, hintsEnabled: false, label: 'Hard', description: '90 sec, no hints' },
  expert: { timeLimit: 60, hintsEnabled: false, label: 'Expert', description: '60 sec, no hints' },
};

function App() {
  const [artist1, setArtist1] = useState(null);
  const [artist2, setArtist2] = useState(null);
  const [gameStarted, setGameStarted] = useState(false);
  const [showHowToPlay, setShowHowToPlay] = useState(false);
  const [showOptions, setShowOptions] = useState(false);
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

  const handleWin = useCallback((steps) => {
    setOptions(prev => ({
      ...prev,
      gamesWon: prev.gamesWon + 1,
      bestScore: prev.bestScore === null ? steps : Math.min(prev.bestScore, steps),
    }));
  }, []);

  return (
    <div className="app-container">
      <StarryBackground />

      {!gameStarted ? (
        <div className="home-screen">
          {/* Top bar */}
          <div className="top-bar">
            <button className="top-btn" onClick={() => setShowHowToPlay(true)}>
              <Info size={16} />
              <span>HOW TO PLAY</span>
            </button>
            <button className="top-btn" onClick={() => setShowOptions(true)}>
              <Settings size={16} />
              <span>OPTIONS</span>
            </button>
          </div>

          {/* Logo & Title */}
          <div className="hero-section">
            <div className="logo-icon">
              <svg width="56" height="56" viewBox="0 0 56 56" fill="none">
                {/* Diamond shape */}
                <path d="M28 2L48 22L28 54L8 22L28 2Z" 
                      stroke="#a3bffa" strokeWidth="1.5" fill="none" opacity="0.6"/>
                <path d="M28 8L42 22L28 48L14 22L28 8Z" 
                      stroke="#c7d2fe" strokeWidth="1" fill="none" opacity="0.3"/>
                {/* Inner facets */}
                <line x1="8" y1="22" x2="48" y2="22" stroke="#a3bffa" strokeWidth="0.8" opacity="0.4"/>
                <line x1="28" y1="2" x2="18" y2="22" stroke="#a3bffa" strokeWidth="0.5" opacity="0.3"/>
                <line x1="28" y1="2" x2="38" y2="22" stroke="#a3bffa" strokeWidth="0.5" opacity="0.3"/>
                {/* Center sparkle */}
                <circle cx="28" cy="22" r="2" fill="#d4dff5" opacity="0.7"/>
              </svg>
            </div>
            <h1 className="main-title">Connect the Notes</h1>
            <p className="subtitle">CHOOSE TWO ARTISTS</p>
          </div>

          {/* Artist Selection Cards */}
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

          {/* Start Game Button */}
          <div className="start-section">
            <button
              className={`start-game-btn ${artist1 && artist2 ? 'ready' : 'disabled'}`}
              onClick={handleStartGame}
              disabled={!artist1 || !artist2}
            >
              Start Game
            </button>
          </div>

          {/* Footer */}
          <footer className="home-footer">
            <p className="footer-credit">
              {stats.totalArtists} artists · {stats.totalCollaborations} connections
            </p>
          </footer>
        </div>
      ) : (
        <GameBoard
          artist1={artist1}
          artist2={artist2}
          onBack={handleBack}
          showHints={options.showHints}
          onWin={handleWin}
        />
      )}

      {/* Modals */}
      <HowToPlayModal isOpen={showHowToPlay} onClose={() => setShowHowToPlay(false)} />
      <OptionsModal
        isOpen={showOptions}
        onClose={() => setShowOptions(false)}
        options={options}
        onOptionsChange={setOptions}
      />
    </div>
  );
}

export default App;
