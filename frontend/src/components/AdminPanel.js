import React, { useState } from 'react';
import { RefreshCw } from 'lucide-react';

const AdminPanel = () => {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleFetchImages = async () => {
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await fetch('https://connectthenotes.onrender.com/api/fetch-images', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
      });

      if (!response.ok) {
        throw new Error('Failed to fetch images');
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="admin-panel" style={styles.container}>
      <div style={styles.card}>
        <h2 style={styles.title}>🔧 Admin Panel</h2>
        <p style={styles.description}>
          Populate all artist images from Deezer API. This will fetch real photos for artists that don't have images yet.
        </p>

        <button
          onClick={handleFetchImages}
          disabled={loading}
          style={{
            ...styles.button,
            ...(loading ? styles.buttonDisabled : {}),
          }}
        >
          {loading ? (
            <>
              <RefreshCw size={16} style={styles.spinner} />
              Fetching images...
            </>
          ) : (
            <>
              <RefreshCw size={16} />
              Fetch Artist Images
            </>
          )}
        </button>

        {result && (
          <div style={styles.result}>
            <h3 style={styles.resultTitle}>✨ {result.summary}</h3>
            <div style={styles.stats}>
              <div style={styles.stat}>
                <span style={styles.statLabel}>Updated:</span>
                <span style={styles.statValue}>{result.updated}</span>
              </div>
              <div style={styles.stat}>
                <span style={styles.statLabel}>Skipped:</span>
                <span style={styles.statValue}>{result.skipped}</span>
              </div>
              <div style={styles.stat}>
                <span style={styles.statLabel}>Failed:</span>
                <span style={styles.statValue}>{result.failed}</span>
              </div>
              <div style={styles.stat}>
                <span style={styles.statLabel}>Total:</span>
                <span style={styles.statValue}>{result.total}</span>
              </div>
            </div>
            <details style={styles.details}>
              <summary style={styles.summary}>View full log</summary>
              <div style={styles.log}>
                {result.log.map((line, i) => (
                  <div key={i} style={styles.logLine}>{line}</div>
                ))}
              </div>
            </details>
          </div>
        )}

        {error && (
          <div style={styles.error}>
            ❌ Error: {error}
          </div>
        )}
      </div>
    </div>
  );
};

const styles = {
  container: {
    padding: '2rem',
    maxWidth: '800px',
    margin: '0 auto',
    fontFamily: 'system-ui, -apple-system, sans-serif',
  },
  card: {
    background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    borderRadius: '1rem',
    padding: '2rem',
    boxShadow: '0 20px 60px rgba(0,0,0,0.3)',
    color: 'white',
  },
  title: {
    fontSize: '2rem',
    fontWeight: 'bold',
    marginBottom: '0.5rem',
    textShadow: '0 2px 4px rgba(0,0,0,0.2)',
  },
  description: {
    fontSize: '0.95rem',
    opacity: 0.9,
    marginBottom: '1.5rem',
    lineHeight: '1.6',
  },
  button: {
    display: 'flex',
    alignItems: 'center',
    gap: '0.5rem',
    padding: '0.875rem 1.5rem',
    fontSize: '1rem',
    fontWeight: '600',
    color: '#667eea',
    background: 'white',
    border: 'none',
    borderRadius: '0.5rem',
    cursor: 'pointer',
    transition: 'all 0.2s',
    boxShadow: '0 4px 12px rgba(0,0,0,0.15)',
  },
  buttonDisabled: {
    opacity: 0.6,
    cursor: 'not-allowed',
  },
  spinner: {
    animation: 'spin 1s linear infinite',
  },
  result: {
    marginTop: '1.5rem',
    background: 'rgba(255,255,255,0.15)',
    borderRadius: '0.75rem',
    padding: '1.25rem',
    backdropFilter: 'blur(10px)',
  },
  resultTitle: {
    fontSize: '1.25rem',
    fontWeight: 'bold',
    marginBottom: '1rem',
  },
  stats: {
    display: 'grid',
    gridTemplateColumns: 'repeat(2, 1fr)',
    gap: '0.75rem',
    marginBottom: '1rem',
  },
  stat: {
    background: 'rgba(255,255,255,0.1)',
    padding: '0.75rem',
    borderRadius: '0.5rem',
    display: 'flex',
    justifyContent: 'space-between',
  },
  statLabel: {
    opacity: 0.8,
    fontSize: '0.9rem',
  },
  statValue: {
    fontWeight: 'bold',
    fontSize: '1.1rem',
  },
  details: {
    marginTop: '1rem',
  },
  summary: {
    cursor: 'pointer',
    fontWeight: '600',
    padding: '0.5rem',
    background: 'rgba(255,255,255,0.1)',
    borderRadius: '0.5rem',
    marginBottom: '0.5rem',
  },
  log: {
    background: 'rgba(0,0,0,0.2)',
    padding: '1rem',
    borderRadius: '0.5rem',
    maxHeight: '400px',
    overflowY: 'auto',
    fontSize: '0.85rem',
    fontFamily: 'monospace',
  },
  logLine: {
    padding: '0.25rem 0',
    borderBottom: '1px solid rgba(255,255,255,0.1)',
  },
  error: {
    marginTop: '1.5rem',
    padding: '1rem',
    background: 'rgba(239, 68, 68, 0.2)',
    borderRadius: '0.5rem',
    border: '1px solid rgba(239, 68, 68, 0.4)',
  },
};

export default AdminPanel;
