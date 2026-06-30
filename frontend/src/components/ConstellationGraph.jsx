import React from 'react';
import { Music2 } from 'lucide-react';
import { getAvatarUrl } from '../utils/avatars';
import { useArtistImage } from '../utils/useArtistImage';

// The solution reveal. A solved puzzle is a linear chain
// (start → … → target), so we render it as a flowing "trail": squared artist
// photos (matching the board's polaroid cards) linked by legible song chips and
// the connecting thread. Everything is set in the game's mono typeface so the
// reveal reads as elegantly as the board itself.

// Square photos everywhere — the initials fallback (UI-Avatars) defaults to a
// circle, so force the square variant; real photos are left untouched.
const squared = (url) => (url || '').replace('rounded=true', 'rounded=false');

const TrailArtist = ({ artist, role }) => {
  const src = squared(useArtistImage(artist));
  return (
    <div className={`sol-artist${role ? ` is-${role}` : ''}`}>
      {role && <span className={`sol-tag ${role}`}>{role === 'start' ? 'START' : 'TARGET'}</span>}
      <div className="sol-photo">
        <img src={src} alt={artist.name} loading="lazy"
          onError={(e) => { e.currentTarget.src = squared(getAvatarUrl(artist, 200)); }} />
      </div>
      <span className="sol-name">{artist.name}</span>
    </div>
  );
};

const TrailLink = ({ song }) => {
  const title = song?.title || 'Unknown';
  const meta = [song?.type && song.type !== 'song' ? song.type : null, song?.year]
    .filter(Boolean).join(' · ');
  return (
    <div className="sol-link" aria-label={`linked by ${title}`}>
      <span className="sol-thread" aria-hidden="true" />
      <div className="sol-song">
        <span className="sol-song-note" aria-hidden="true"><Music2 size={13} /></span>
        <span className="sol-song-title">{title}</span>
        {meta && <span className="sol-song-meta">{meta}</span>}
      </div>
      <span className="sol-thread" aria-hidden="true" />
    </div>
  );
};

const ConstellationGraph = ({ found, edges = [], startId, targetId }) => {
  if (!found || !found.length) return null;

  // chainToWeb hands us `found` already in path order with edges[i] linking
  // found[i] → found[i+1]; render them interleaved into one trail.
  return (
    <div className="solution-trail">
      {found.map((artist, i) => {
        const role = artist.id === startId ? 'start' : artist.id === targetId ? 'target' : null;
        return (
          <React.Fragment key={artist.id}>
            <TrailArtist artist={artist} role={role} />
            {i < found.length - 1 && edges[i] && <TrailLink song={edges[i].song} />}
          </React.Fragment>
        );
      })}
    </div>
  );
};

export default ConstellationGraph;
