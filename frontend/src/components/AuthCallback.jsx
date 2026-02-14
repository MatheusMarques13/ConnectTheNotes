import React, { useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { exchangeSessionId } from '../services/api';
import { Loader2 } from 'lucide-react';

// REMINDER: DO NOT HARDCODE THE URL, OR ADD ANY FALLBACKS OR REDIRECT URLS, THIS BREAKS THE AUTH
const AuthCallback = ({ onAuthSuccess }) => {
  const navigate = useNavigate();
  const hasProcessed = useRef(false);

  useEffect(() => {
    // Use useRef to prevent double-processing in StrictMode
    if (hasProcessed.current) return;
    hasProcessed.current = true;

    const processAuth = async () => {
      // Extract session_id from URL hash
      const hash = window.location.hash;
      const params = new URLSearchParams(hash.replace('#', ''));
      const sessionId = params.get('session_id');

      if (!sessionId) {
        console.error('No session_id found in URL');
        navigate('/', { replace: true });
        return;
      }

      try {
        // Exchange session_id for user data
        const result = await exchangeSessionId(sessionId);
        
        if (result && result.user) {
          // Clear URL hash
          window.history.replaceState(null, '', window.location.pathname);
          
          // Notify parent of successful auth
          if (onAuthSuccess) {
            onAuthSuccess(result.user);
          }
          
          // Navigate to home with user data
          navigate('/', { 
            replace: true, 
            state: { user: result.user, justLoggedIn: true } 
          });
        } else {
          console.error('Failed to exchange session_id');
          navigate('/', { replace: true });
        }
      } catch (err) {
        console.error('Auth error:', err);
        navigate('/', { replace: true });
      }
    };

    processAuth();
  }, [navigate, onAuthSuccess]);

  return (
    <div className="auth-callback" data-testid="auth-callback">
      <div className="auth-loading">
        <Loader2 size={32} className="spin-icon" />
        <span>Signing you in...</span>
      </div>
    </div>
  );
};

export default AuthCallback;
