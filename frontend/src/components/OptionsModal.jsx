import React, { useState } from 'react';
import { X, Volume2, VolumeX, Palette, RotateCcw } from 'lucide-react';

const OptionsModal = ({ isOpen, onClose, options, onOptionsChange }) => {
  if (!isOpen) return null;

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content options-modal" onClick={e => e.stopPropagation()}>
        <button className="modal-close-btn" onClick={onClose}>
          <X size={20} />
        </button>
        <h2 className="modal-title">Options</h2>
        <div className="options-list">
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
        </div>
        <div className="options-stats">
          <h3>Stats</h3>
          <div className="stats-grid">
            <div className="stat-item">
              <span className="stat-value">{options.gamesPlayed || 0}</span>
              <span className="stat-label">Games Played</span>
            </div>
            <div className="stat-item">
              <span className="stat-value">{options.gamesWon || 0}</span>
              <span className="stat-label">Games Won</span>
            </div>
            <div className="stat-item">
              <span className="stat-value">{options.bestScore || '-'}</span>
              <span className="stat-label">Best Score</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default OptionsModal;
