import React from 'react';
import { X, Music, ArrowRight, Link2, Trophy } from 'lucide-react';

const HowToPlayModal = ({ isOpen, onClose }) => {
  if (!isOpen) return null;

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content how-to-play-modal" onClick={e => e.stopPropagation()}>
        <button className="modal-close-btn" onClick={onClose}>
          <X size={20} />
        </button>
        <h2 className="modal-title">How To Play</h2>
        <div className="htp-steps">
          <div className="htp-step">
            <div className="htp-step-icon">
              <Music size={24} />
            </div>
            <div className="htp-step-content">
              <h3>1. Choose Two Artists</h3>
              <p>Select two musical artists you want to connect. You can search by name or let the game choose randomly for you.</p>
            </div>
          </div>
          <div className="htp-step">
            <div className="htp-step-icon">
              <Link2 size={24} />
            </div>
            <div className="htp-step-content">
              <h3>2. Find the Connection</h3>
              <p>Connect the two artists by finding a chain of collaborations. Artists can be linked through songs, albums, features, or live performances they've shared.</p>
            </div>
          </div>
          <div className="htp-step">
            <div className="htp-step-icon">
              <ArrowRight size={24} />
            </div>
            <div className="htp-step-content">
              <h3>3. Build Your Chain</h3>
              <p>At each step, pick a collaboration, then choose the next artist until you reach your target. The fewer steps, the better!</p>
            </div>
          </div>
          <div className="htp-step">
            <div className="htp-step-icon">
              <Trophy size={24} />
            </div>
            <div className="htp-step-content">
              <h3>4. Win!</h3>
              <p>You win when you successfully connect the two artists. Try to do it in as few steps as possible!</p>
            </div>
          </div>
        </div>
        <div className="htp-example">
          <h3>Example</h3>
          <div className="htp-example-chain">
            <span className="example-artist">Drake</span>
            <span className="example-arrow">→</span>
            <span className="example-collab">\"Forever\"</span>
            <span className="example-arrow">→</span>
            <span className="example-artist">Eminem</span>
            <span className="example-arrow">→</span>
            <span className="example-collab">\"River\"</span>
            <span className="example-arrow">→</span>
            <span className="example-artist">Ed Sheeran</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default HowToPlayModal;
