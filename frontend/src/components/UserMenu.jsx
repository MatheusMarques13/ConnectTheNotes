import React, { useState } from 'react';
import { LogIn, Clock } from 'lucide-react';

const UserMenu = () => {
  const [showTooltip, setShowTooltip] = useState(false);

  return (
    <div style={{ position: 'relative' }}>
      <button 
        className="login-btn" 
        onClick={() => setShowTooltip(!showTooltip)}
        data-testid="login-btn"
        style={{ opacity: 0.6, cursor: 'default' }}
      >
        <LogIn size={16} />
        <span>Sign In</span>
      </button>
      {showTooltip && (
        <div style={{
          position: 'absolute',
          top: '100%',
          right: 0,
          marginTop: '8px',
          padding: '12px 16px',
          background: 'rgba(12, 17, 33, 0.95)',
          border: '1px solid rgba(184, 198, 224, 0.15)',
          borderRadius: '8px',
          whiteSpace: 'nowrap',
          zIndex: 100,
          display: 'flex',
          alignItems: 'center',
          gap: '8px',
          color: 'rgba(184, 198, 224, 0.8)',
          fontSize: '13px',
          fontFamily: 'var(--font-body)',
          backdropFilter: 'blur(12px)',
        }}>
          <Clock size={14} style={{ color: '#c084fc' }} />
          Login coming soon!
        </div>
      )}
    </div>
  );
};

export default UserMenu;
