import React, { useState, useMemo } from 'react';
import { ArrowLeft, ArrowRight, Music, Disc, Radio, Mic2, RotateCcw, Lightbulb, Check, ChevronRight } from 'lucide-react';
import {
  getArtistById,
  getCollaborationsForArtist,
  getCollaborationsBetween,
  findConnection,
  searchArtists,
  getConnectedArtists,
} from '../data/mockData';

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

const GameBoard = ({ artist1, artist2, onBack, showHints, onWin }) => {
  const [chain, setChain] = useState([{ artist: artist1, collab: null }]);
  const [selectedCollab, setSelectedCollab] = useState(null);
  const [gameWon, setGameWon] = useState(false);
  const [showHint, setShowHint] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState([]);

  const currentArtist = chain[chain.length - 1].artist;

  const availableCollabs = useMemo(() => {
    return getCollaborationsForArtist(currentArtist.id);
  }, [currentArtist.id]);

  const connectedArtists = useMemo(() => {
    return getConnectedArtists(currentArtist.id);
  }, [currentArtist.id]);

  const hint = useMemo(() => {
    if (!showHints) return null;
    const path = findConnection(currentArtist.id, artist2.id);
    if (path && path.length > 0) {
      const nextArtist = getArtistById(path[0].toArtist);
      return nextArtist;
    }
    return null;
  }, [currentArtist.id, artist2.id, showHints]);

  const handleSelectCollab = (collab) => {
    setSelectedCollab(collab);
    setSearchQuery('');
    setSearchResults([]);
  };

  const handleSelectNextArtist = (nextArtist) => {
    const newChain = [...chain, { artist: nextArtist, collab: selectedCollab }];
    setChain(newChain);
    setSelectedCollab(null);
    setSearchQuery('');
    setSearchResults([]);

    if (nextArtist.id === artist2.id) {
      setGameWon(true);
      if (onWin) onWin(newChain.length - 1);
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
    setShowHint(false);
  };

  const getArtistsForCollab = (collab) => {
    return collab.artistIds
      .filter(id => id !== currentArtist.id)
      .map(id => getArtistById(id))
      .filter(Boolean);
  };

  const handleArtistSearch = (value) => {
    setSearchQuery(value);
    if (value.length > 0) {
      const filtered = connectedArtists.filter(a =>
        a.name.toLowerCase().includes(value.toLowerCase())
      );
      setSearchResults(filtered);
    } else {
      setSearchResults([]);
    }
  };

  const getInitials = (name) => {
    return name.split(' ').map(w => w[0]).join('').slice(0, 2).toUpperCase();
  };

  if (gameWon) {
    return (
      <div className="game-board">
        <div className="game-won">
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
          <p className="won-subtitle">You linked {artist1.name} to {artist2.name} in {chain.length - 1} step{chain.length - 1 !== 1 ? 's' : ''}!</p>
          <div className="won-chain">
            {chain.map((step, i) => (
              <React.Fragment key={i}>
                <div className="won-chain-artist">
                  <div className="won-avatar">
                    <span>{getInitials(step.artist.name)}</span>
                  </div>
                  <span className="won-artist-name">{step.artist.name}</span>
                </div>
                {i < chain.length - 1 && (
                  <div className="won-chain-collab">
                    <ChevronRight size={16} />
                    <span className="won-collab-title">{chain[i + 1].collab?.title}</span>
                    <ChevronRight size={16} />
                  </div>
                )}
              </React.Fragment>
            ))}
          </div>
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
        <div className="game-goal">
          <div className="goal-artist">
            <div className="goal-avatar small">
              <span>{getInitials(artist1.name)}</span>
            </div>
            <span>{artist1.name}</span>
          </div>
          <ArrowRight size={16} className="goal-arrow" />
          <div className="goal-artist">
            <div className="goal-avatar small">
              <span>{getInitials(artist2.name)}</span>
            </div>
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
        <div className="chain-display">
          {chain.map((step, i) => (
            <React.Fragment key={i}>
              <div className={`chain-node ${i === chain.length - 1 ? 'current' : 'visited'}`}>
                <span>{step.artist.name}</span>
              </div>
              {i < chain.length - 1 && (
                <div className="chain-edge">
                  <span className="chain-collab-name">{chain[i + 1].collab?.title}</span>
                </div>
              )}
            </React.Fragment>
          ))}
        </div>
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
        <div className="current-avatar-large">
          <span>{getInitials(currentArtist.name)}</span>
        </div>
        <h2 className="current-artist-name">{currentArtist.name}</h2>
        <p className="current-artist-genre">{currentArtist.genre}</p>
      </div>

      {/* Select collaboration */}
      {!selectedCollab ? (
        <div className="collab-section">
          <h3 className="section-title">SELECT A COLLABORATION</h3>
          <div className="collab-grid">
            {availableCollabs.map(collab => {
              const otherArtists = getArtistsForCollab(collab);
              return (
                <button
                  key={collab.id}
                  className="collab-card"
                  onClick={() => handleSelectCollab(collab)}
                >
                  <div className="collab-type-badge">
                    {typeIcons[collab.type]}
                    <span>{typeLabels[collab.type]}</span>
                  </div>
                  <div className="collab-title">{collab.title}</div>
                  <div className="collab-year">{collab.year}</div>
                  <div className="collab-with">
                    with {otherArtists.map(a => a.name).join(', ')}
                  </div>
                </button>
              );
            })}
          </div>
        </div>
      ) : (
        <div className="next-artist-section">
          <div className="selected-collab-display">
            <div className="collab-type-badge">
              {typeIcons[selectedCollab.type]}
              <span>{typeLabels[selectedCollab.type]}</span>
            </div>
            <span className="selected-collab-title">{selectedCollab.title} ({selectedCollab.year})</span>
            <button className="change-collab-btn" onClick={() => setSelectedCollab(null)}>Change</button>
          </div>
          <h3 className="section-title">SELECT NEXT ARTIST</h3>
          <div className="next-artist-search">
            <input
              type="text"
              placeholder="Search connected artist..."
              value={searchQuery}
              onChange={e => handleArtistSearch(e.target.value)}
              className="artist-search-input"
            />
          </div>
          <div className="next-artist-grid">
            {(searchQuery ? searchResults : getArtistsForCollab(selectedCollab)).map(artist => (
              <button
                key={artist.id}
                className={`next-artist-card ${artist.id === artist2.id ? 'target' : ''} ${showHint && hint && artist.id === hint.id ? 'hinted' : ''}`}
                onClick={() => handleSelectNextArtist(artist)}
              >
                <div className="next-avatar">
                  <span>{getInitials(artist.name)}</span>
                </div>
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
