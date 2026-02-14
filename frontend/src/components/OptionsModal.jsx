import React from 'react';
import { X, Volume2, VolumeX, Palette, RotateCcw, Timer, Zap, Trophy, Clock } from 'lucide-react';

const OptionsModal = ({ isOpen, onClose, options, onOptionsChange, difficultyConfig }) => {
  if (!isOpen) return null;

  const formatTime = (seconds) => {
    if (!seconds) return '-';
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return mins > 0 ? `${mins}:${secs.toString().padStart(2, '0')}` : `${secs}s`;
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content options-modal" onClick={e => e.stopPropagation()}>
        <button className="modal-close-btn" onClick={onClose}>
          <X size={20} />
        </button>
        <h2 className="modal-title">Options</h2>
        
        {/* Game Mode Section */}
        <div className="options-section">
          <h3 className="options-section-title">
            <Timer size={16} />
            <span>Game Mode</span>
          </h3>
          
          {/* Timed Mode Toggle */}
          <div className="option-item">
            <div className="option-label">
              <Clock size={18} />
              <div className="option-text">
                <span>Timed Challenge</span>
                <span className="option-description">Race against the clock!</span>
              </div>
            </div>
            <button 
              className={`toggle-btn ${options.timedMode ? 'active' : ''}`}
              onClick={() => onOptionsChange({ ...options, timedMode: !options.timedMode })}
              data-testid="timed-mode-toggle"
            >
              <div className="toggle-knob" />
            </button>
          </div>

          {/* Difficulty Selector (only show when timed mode is on) */}
          {options.timedMode && (
            <div className="difficulty-selector">
              <label className="difficulty-label">Difficulty</label>
              <div className="difficulty-buttons">
                {Object.entries(difficultyConfig).map(([key, config]) => (
                  <button
                    key={key}
                    className={`difficulty-btn ${options.difficulty === key ? 'active' : ''}`}
                    onClick={() => onOptionsChange({ ...options, difficulty: key })}
                    data-testid={`difficulty-${key}`}
                  >
                    <span className="difficulty-name">{config.label}</span>
                    <span className="difficulty-desc">{config.description}</span>
                  </button>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Regular Options */}
        <div className="options-section">
          <h3 className="options-section-title">
            <Zap size={16} />
            <span>Gameplay</span>
          </h3>
          
          <div className="option-item">
            <div className="option-label">
              {options.sound ? <Volume2 size={18} /> : <VolumeX size={18} />}
              <span>Sound Effects</span>
            </div>
            <button 
              className={`toggle-btn ${options.sound ? 'active' : ''}`}
              onClick={() => onOptionsChange({ ...options, sound: !options.sound })}
            >
              <div className="toggle-knob" />
            </button>
          </div>
          
          <div className="option-item">
            <div className="option-label">
              <Palette size={18} />
              <span>Show Genres</span>
            </div>
            <button 
              className={`toggle-btn ${options.showGenres ? 'active' : ''}`}
              onClick={() => onOptionsChange({ ...options, showGenres: !options.showGenres })}
            >
              <div className="toggle-knob" />
            </button>
          </div>
          
          {!options.timedMode && (
            <div className="option-item">
              <div className="option-label">
                <RotateCcw size={18} />
                <span>Show Hints</span>
              </div>
              <button 
                className={`toggle-btn ${options.showHints ? 'active' : ''}`}
                onClick={() => onOptionsChange({ ...options, showHints: !options.showHints })}
              >
                <div className="toggle-knob" />
              </button>
            </div>
          )}
        </div>

        {/* Stats Section */}
        <div className="options-stats">
          <h3>
            <Trophy size={14} />
            <span>Your Stats</span>
          </h3>
          <div className="stats-grid">
            <div className="stat-item">
              <span className="stat-value">{options.gamesPlayed || 0}</span>
              <span className="stat-label">Played</span>
            </div>
            <div className="stat-item">
              <span className="stat-value">{options.gamesWon || 0}</span>
              <span className="stat-label">Won</span>
            </div>
            <div className="stat-item">
              <span className="stat-value">{options.gamesLost || 0}</span>
              <span className="stat-label">Lost</span>
            </div>
            <div className="stat-item">
              <span className="stat-value">{options.bestScore || '-'}</span>
              <span className="stat-label">Best Steps</span>
            </div>
            <div className="stat-item">
              <span className="stat-value">{formatTime(options.bestTime)}</span>
              <span className="stat-label">Best Time</span>
            </div>
            <div className="stat-item">
              <span className="stat-value">
                {options.gamesPlayed > 0 
                  ? Math.round((options.gamesWon / options.gamesPlayed) * 100) + '%'
                  : '-'}
              </span>
              <span className="stat-label">Win Rate</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default OptionsModal;
