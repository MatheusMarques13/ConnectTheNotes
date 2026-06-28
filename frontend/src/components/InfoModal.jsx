import React, { useEffect } from 'react';
import { X, Music2, Disc, Disc3, Radio, Tv, Film, Mic2 } from 'lucide-react';
import { getLargeAvatarUrl, getSmallAvatarUrl } from '../utils/avatars';

const TYPE_ICON = { song: Music2, album: Disc, ep: Disc3, mixtape: Disc3, live: Radio, dvd: Tv, video: Film, feature: Mic2 };
const TYPE_LABEL = { song: 'Song', album: 'Album', ep: 'EP', mixtape: 'Mixtape', live: 'Live', dvd: 'DVD', video: 'Music Video', feature: 'Feature' };

// Card-detail popover opened when a node is clicked (not dragged).
const InfoModal = ({ node, onClose }) => {
  useEffect(() => {
    const onKey = (e) => { if (e.key === 'Escape') onClose(); };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, [onClose]);

  if (!node) return null;

  return (
    <div className="ctn-info-backdrop" onClick={onClose}>
      <div className="ctn-info-card" onClick={(e) => e.stopPropagation()}>
        <button className="ctn-info-close" onClick={onClose} aria-label="Close"><X size={16} /></button>

        {node.kind === 'artist' ? (
          <>
            <div className="ctn-info-photo">
              <img src={getLargeAvatarUrl(node.artist)} alt={node.artist.name} onError={(e) => { e.target.style.display = 'none'; }} />
            </div>
            <div className="ctn-info-name">{node.artist.name}</div>
            <div className="ctn-info-meta">{node.artist.genre || 'Artist'}</div>
          </>
        ) : (
          <>
            <div className="ctn-info-cover">
              {node.song.coverUrl
                ? <img src={node.song.coverUrl} alt="" onError={(e) => { e.target.style.display = 'none'; }} />
                : (() => { const Icon = TYPE_ICON[node.song.type] || Music2; return <Icon />; })()}
            </div>
            <div className="ctn-info-name">{node.song.title}</div>
            <div className="ctn-info-meta">{(TYPE_LABEL[node.song.type] || node.song.type)} · {node.song.year}</div>
            <div className="ctn-info-credits-title">Artists on this track</div>
            <div className="ctn-info-credit-list">
              {node.artists.map((a) => (
                <div key={a.id} className="ctn-info-credit">
                  <span className="ctn-info-credit-av"><img src={getSmallAvatarUrl(a)} alt="" onError={(e) => { e.target.style.display = 'none'; }} /></span>
                  <span className="ctn-info-credit-name">{a.name}</span>
                </div>
              ))}
            </div>
          </>
        )}
      </div>
    </div>
  );
};

export default InfoModal;
