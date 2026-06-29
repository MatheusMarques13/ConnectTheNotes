import React, { useEffect, useState } from 'react';
import { X, Music2, Disc, Disc3, Radio, Tv, Film, Mic2, Play, Pause } from 'lucide-react';
import { getSmallAvatarUrl } from '../utils/avatars';
import { useArtistImage } from '../utils/useArtistImage';
import * as preview from '../utils/preview';
import { useI18n } from '../i18n';

const TYPE_ICON = { song: Music2, album: Disc, ep: Disc3, mixtape: Disc3, live: Radio, dvd: Tv, video: Film, feature: Mic2 };
const TYPE_LABEL = { song: 'Song', album: 'Album', ep: 'EP', mixtape: 'Mixtape', live: 'Live', dvd: 'DVD', video: 'Music Video', feature: 'Feature' };

// Card-detail popover opened when a node is clicked (not dragged).
const InfoModal = ({ node, onClose }) => {
  const { t } = useI18n();
  const isSong = node && node.kind === 'song';
  const song = isSong ? node.song : null;
  const primary = (isSong && node.artists[0] && node.artists[0].name) || '';
  const [st, setSt] = useState(() => (song ? preview.status(song.id) : { playing: false }));
  const artistImg = useArtistImage(node && node.kind === 'artist' ? node.artist : null, 200);

  useEffect(() => {
    const onKey = (e) => { if (e.key === 'Escape') onClose(); };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, [onClose]);

  // Opening a song card auto-plays its 30s preview through the shared player
  // (the click is the user gesture, so autoplay is allowed).
  useEffect(() => {
    if (!song) return undefined;
    const unsub = preview.subscribe(() => setSt(preview.status(song.id)));
    preview.play(song, primary);
    return unsub;
  }, [song, primary]);

  if (!node) return null;

  const togglePlay = () => { if (song) { preview.unlock(); preview.toggle(song, primary); } };
  const playing = st.playing;

  return (
    <div className="ctn-info-backdrop" onClick={onClose}>
      <div className="ctn-info-card" onClick={(e) => e.stopPropagation()}>
        <button className="ctn-info-close" onClick={onClose} aria-label={t('close')}><X size={16} /></button>

        {node.kind === 'artist' ? (
          <>
            <div className="ctn-info-photo">
              <img src={artistImg} alt={node.artist.name} onError={(e) => { e.target.style.display = 'none'; }} />
            </div>
            <div className="ctn-info-name">{node.artist.name}</div>
            <div className="ctn-info-meta">{node.artist.genre || t('genre')}</div>
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

            <div className="ctn-preview">
              <button className={`ctn-preview-btn${playing ? ' playing' : ''}`} onClick={togglePlay}>
                {playing ? <Pause size={15} /> : <Play size={15} />}
                <span>{t('preview')}</span>
                <span className="ctn-preview-eq" aria-hidden="true"><i /><i /><i /><i /></span>
              </button>
            </div>

            <div className="ctn-info-credits-title">{t('artists_on_track')}</div>
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
