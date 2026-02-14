import React, { useState, useEffect, useCallback } from 'react';
import { X, Trophy, Clock, Footprints, Medal, Crown, Loader2, Calendar, CalendarDays, CalendarRange } from 'lucide-react';
import { getLeaderboard, getUserRank } from '../services/api';
import { getSmallAvatarUrl } from '../utils/avatars';

const LeaderboardModal = ({ isOpen, onClose, currentUser }) => {
  const [leaderboard, setLeaderboard] = useState([]);
  const [loading, setLoading] = useState(true);
  const [period, setPeriod] = useState('all');
  const [sortBy, setSortBy] = useState('wins');
  const [userRank, setUserRank] = useState(null);

  const fetchLeaderboard = useCallback(async () => {
    setLoading(true);
    const data = await getLeaderboard(period, sortBy, 20);
    setLeaderboard(data.leaderboard || []);
    
    if (currentUser) {
      const rankData = await getUserRank(currentUser.user_id, period);
      setUserRank(rankData);
    }
    
    setLoading(false);
  }, [period, sortBy, currentUser]);

  useEffect(() => {
    if (isOpen) {
      fetchLeaderboard();
    }
  }, [isOpen, fetchLeaderboard]);

  if (!isOpen) return null;

  const formatTime = (seconds) => {
    if (!seconds) return '-';
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return mins > 0 ? `${mins}:${secs.toString().padStart(2, '0')}` : `${secs}s`;
  };

  const getRankIcon = (rank) => {
    if (rank === 1) return <Crown size={18} className="rank-crown" />;
    if (rank === 2) return <Medal size={16} className="rank-silver" />;
    if (rank === 3) return <Medal size={16} className="rank-bronze" />;
    return <span className="rank-number">{rank}</span>;
  };

  const periodOptions = [
    { key: 'daily', label: 'Today', icon: <Calendar size={14} /> },
    { key: 'weekly', label: 'This Week', icon: <CalendarDays size={14} /> },
    { key: 'all', label: 'All Time', icon: <CalendarRange size={14} /> },
  ];

  const sortOptions = [
    { key: 'wins', label: 'Most Wins', icon: <Trophy size={14} /> },
    { key: 'steps', label: 'Fewest Steps', icon: <Footprints size={14} /> },
    { key: 'time', label: 'Fastest Time', icon: <Clock size={14} /> },
  ];

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content leaderboard-modal" onClick={e => e.stopPropagation()}>
        <button className="modal-close-btn" onClick={onClose}>
          <X size={20} />
        </button>
        
        <div className="leaderboard-header">
          <h2 className="modal-title">
            <Trophy size={24} className="title-icon" />
            Leaderboard
          </h2>
        </div>

        {/* Period Selector */}
        <div className="leaderboard-filters">
          <div className="filter-group">
            {periodOptions.map(opt => (
              <button
                key={opt.key}
                className={`filter-btn ${period === opt.key ? 'active' : ''}`}
                onClick={() => setPeriod(opt.key)}
                data-testid={`period-${opt.key}`}
              >
                {opt.icon}
                <span>{opt.label}</span>
              </button>
            ))}
          </div>
          
          <div className="filter-group">
            {sortOptions.map(opt => (
              <button
                key={opt.key}
                className={`filter-btn ${sortBy === opt.key ? 'active' : ''}`}
                onClick={() => setSortBy(opt.key)}
                data-testid={`sort-${opt.key}`}
              >
                {opt.icon}
                <span>{opt.label}</span>
              </button>
            ))}
          </div>
        </div>

        {/* User's Current Rank */}
        {currentUser && userRank && (
          <div className="user-rank-card" data-testid="user-rank-card">
            <div className="user-rank-info">
              <img 
                src={currentUser.picture || getSmallAvatarUrl(currentUser.name)} 
                alt={currentUser.name}
                className="user-rank-avatar"
              />
              <div className="user-rank-details">
                <span className="user-rank-name">Your Rank</span>
                <span className="user-rank-position">
                  {userRank.rank ? `#${userRank.rank}` : 'Unranked'}
                </span>
              </div>
            </div>
            <div className="user-rank-stats">
              <div className="mini-stat">
                <span className="mini-stat-value">{userRank.wins || 0}</span>
                <span className="mini-stat-label">Wins</span>
              </div>
              <div className="mini-stat">
                <span className="mini-stat-value">{userRank.best_steps || '-'}</span>
                <span className="mini-stat-label">Best</span>
              </div>
              <div className="mini-stat">
                <span className="mini-stat-value">{formatTime(userRank.best_time)}</span>
                <span className="mini-stat-label">Time</span>
              </div>
            </div>
          </div>
        )}

        {/* Leaderboard List */}
        <div className="leaderboard-list">
          {loading ? (
            <div className="leaderboard-loading">
              <Loader2 size={24} className="spin-icon" />
              <span>Loading leaderboard...</span>
            </div>
          ) : leaderboard.length === 0 ? (
            <div className="leaderboard-empty">
              <Trophy size={32} className="empty-icon" />
              <p>No games recorded yet for this period.</p>
              <p className="empty-hint">Be the first to make the leaderboard!</p>
            </div>
          ) : (
            leaderboard.map((entry, index) => {
              const isCurrentUser = currentUser && entry.user_id === currentUser.user_id;
              return (
                <div 
                  key={entry.user_id || index} 
                  className={`leaderboard-entry ${index < 3 ? `top-${index + 1}` : ''} ${isCurrentUser ? 'current-user' : ''}`}
                  data-testid={`leaderboard-entry-${index}`}
                >
                  <div className="entry-rank">
                    {getRankIcon(index + 1)}
                  </div>
                  <div className="entry-user">
                    <img 
                      src={entry.user_picture || getSmallAvatarUrl(entry.user_name)} 
                      alt={entry.user_name}
                      className="entry-avatar"
                    />
                    <span className="entry-name">{entry.user_name}</span>
                  </div>
                  <div className="entry-stats">
                    {sortBy === 'wins' && (
                      <>
                        <span className="entry-main-stat">{entry.wins} wins</span>
                        {entry.best_steps && <span className="entry-sub-stat">{entry.best_steps} best</span>}
                      </>
                    )}
                    {sortBy === 'steps' && (
                      <>
                        <span className="entry-main-stat">{entry.best_steps} steps</span>
                        {entry.artist1_name && (
                          <span className="entry-sub-stat">
                            {entry.artist1_name} → {entry.artist2_name}
                          </span>
                        )}
                      </>
                    )}
                    {sortBy === 'time' && (
                      <>
                        <span className="entry-main-stat">{formatTime(entry.best_time)}</span>
                        <span className="entry-sub-stat">
                          {entry.difficulty || 'timed'} • {entry.best_steps} steps
                        </span>
                      </>
                    )}
                  </div>
                </div>
              );
            })
          )}
        </div>
      </div>
    </div>
  );
};

export default LeaderboardModal;
