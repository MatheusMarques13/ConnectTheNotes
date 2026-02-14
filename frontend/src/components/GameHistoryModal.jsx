import React, { useState, useEffect } from 'react';
import { X, History, Trophy, XCircle, Clock, Footprints, Loader2 } from 'lucide-react';
import { getUserGameHistory } from '../services/api';
import { getSmallAvatarUrl } from '../utils/avatars';

const GameHistoryModal = ({ isOpen, onClose, currentUser }) => {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (isOpen && currentUser) {
      const fetchHistory = async () => {
        setLoading(true);
        const data = await getUserGameHistory(currentUser.user_id, 50);
        setHistory(data.history || []);
        setLoading(false);
      };
      fetchHistory();
    }
  }, [isOpen, currentUser]);

  if (!isOpen) return null;

  const formatTime = (seconds) => {
    if (!seconds) return null;
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return mins > 0 ? `${mins}:${secs.toString().padStart(2, '0')}` : `${secs}s`;
  };

  const formatDate = (dateStr) => {
    const date = new Date(dateStr);
    const now = new Date();
    const diffMs = now - date;
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMs / 3600000);
    const diffDays = Math.floor(diffMs / 86400000);

    if (diffMins < 1) return 'Just now';
    if (diffMins < 60) return `${diffMins}m ago`;
    if (diffHours < 24) return `${diffHours}h ago`;
    if (diffDays < 7) return `${diffDays}d ago`;
    return date.toLocaleDateString();
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content history-modal" onClick={e => e.stopPropagation()}>
        <button className="modal-close-btn" onClick={onClose}>
          <X size={20} />
        </button>
        
        <h2 className="modal-title">
          <History size={24} className="title-icon" />
          Game History
        </h2>

        <div className="history-list">
          {loading ? (
            <div className="history-loading">
              <Loader2 size={24} className="spin-icon" />
              <span>Loading history...</span>
            </div>
          ) : history.length === 0 ? (
            <div className="history-empty">
              <History size={32} className="empty-icon" />
              <p>No games played yet.</p>
              <p className="empty-hint">Start playing to build your history!</p>
            </div>
          ) : (
            history.map((game, index) => (
              <div 
                key={game.result_id || index} 
                className={`history-entry ${game.won ? 'won' : 'lost'}`}
                data-testid={`history-entry-${index}`}
              >
                <div className="history-result-icon">
                  {game.won ? (
                    <Trophy size={18} className="win-icon" />
                  ) : (
                    <XCircle size={18} className="loss-icon" />
                  )}
                </div>
                
                <div className="history-artists">
                  <span className="history-artist">{game.artist1_name}</span>
                  <span className="history-arrow">→</span>
                  <span className="history-artist">{game.artist2_name}</span>
                </div>
                
                <div className="history-stats">
                  <span className="history-stat">
                    <Footprints size={12} />
                    {game.steps} steps
                  </span>
                  {game.time_seconds && (
                    <span className="history-stat">
                      <Clock size={12} />
                      {formatTime(game.time_seconds)}
                    </span>
                  )}
                  {game.difficulty && (
                    <span className="history-badge">{game.difficulty}</span>
                  )}
                </div>
                
                <span className="history-date">{formatDate(game.created_at)}</span>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
};

export default GameHistoryModal;
