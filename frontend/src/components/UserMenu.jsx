import React, { useState, useRef, useEffect } from 'react';
import { LogIn, LogOut, User, Trophy, History, ChevronDown } from 'lucide-react';
import { logout } from '../services/api';
import { getSmallAvatarUrl } from '../utils/avatars';

// REMINDER: DO NOT HARDCODE THE URL, OR ADD ANY FALLBACKS OR REDIRECT URLS, THIS BREAKS THE AUTH
const UserMenu = ({ user, onLogin, onLogout, onShowLeaderboard, onShowHistory }) => {
  const [isOpen, setIsOpen] = useState(false);
  const menuRef = useRef(null);

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (menuRef.current && !menuRef.current.contains(event.target)) {
        setIsOpen(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const handleLogin = () => {
    // REMINDER: DO NOT HARDCODE THE URL, OR ADD ANY FALLBACKS OR REDIRECT URLS, THIS BREAKS THE AUTH
    const redirectUrl = window.location.origin;
    window.location.href = `https://auth.emergentagent.com/?redirect=${encodeURIComponent(redirectUrl)}`;
  };

  const handleLogout = async () => {
    setIsOpen(false);
    await logout();
    if (onLogout) onLogout();
  };

  if (!user) {
    return (
      <button 
        className="login-btn" 
        onClick={handleLogin}
        data-testid="login-btn"
      >
        <LogIn size={16} />
        <span>Sign In</span>
      </button>
    );
  }

  return (
    <div className="user-menu" ref={menuRef}>
      <button 
        className="user-menu-trigger"
        onClick={() => setIsOpen(!isOpen)}
        data-testid="user-menu-trigger"
      >
        <img 
          src={user.picture || getSmallAvatarUrl(user.name)} 
          alt={user.name}
          className="user-avatar-small"
        />
        <span className="user-name-display">{user.name.split(' ')[0]}</span>
        <ChevronDown size={14} className={`chevron ${isOpen ? 'open' : ''}`} />
      </button>

      {isOpen && (
        <div className="user-menu-dropdown" data-testid="user-menu-dropdown">
          <div className="user-menu-header">
            <img 
              src={user.picture || getSmallAvatarUrl(user.name)} 
              alt={user.name}
              className="dropdown-avatar"
            />
            <div className="dropdown-user-info">
              <span className="dropdown-name">{user.name}</span>
              <span className="dropdown-email">{user.email}</span>
            </div>
          </div>
          
          <div className="user-menu-divider" />
          
          <button 
            className="user-menu-item"
            onClick={() => { setIsOpen(false); onShowLeaderboard && onShowLeaderboard(); }}
            data-testid="menu-leaderboard"
          >
            <Trophy size={16} />
            <span>Leaderboard</span>
          </button>
          
          <button 
            className="user-menu-item"
            onClick={() => { setIsOpen(false); onShowHistory && onShowHistory(); }}
            data-testid="menu-history"
          >
            <History size={16} />
            <span>Game History</span>
          </button>
          
          <div className="user-menu-divider" />
          
          {user.stats && (
            <div className="user-menu-stats">
              <div className="menu-stat">
                <span className="menu-stat-value">{user.stats.games_played || 0}</span>
                <span className="menu-stat-label">Played</span>
              </div>
              <div className="menu-stat">
                <span className="menu-stat-value">{user.stats.games_won || 0}</span>
                <span className="menu-stat-label">Won</span>
              </div>
              <div className="menu-stat">
                <span className="menu-stat-value">
                  {user.stats.games_played > 0 
                    ? Math.round((user.stats.games_won / user.stats.games_played) * 100) + '%'
                    : '-'}
                </span>
                <span className="menu-stat-label">Win Rate</span>
              </div>
            </div>
          )}
          
          <div className="user-menu-divider" />
          
          <button 
            className="user-menu-item logout"
            onClick={handleLogout}
            data-testid="menu-logout"
          >
            <LogOut size={16} />
            <span>Sign Out</span>
          </button>
        </div>
      )}
    </div>
  );
};

export default UserMenu;
