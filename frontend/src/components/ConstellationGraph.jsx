import React, { useMemo, useId } from 'react';
import { getSmallAvatarUrl } from '../utils/avatars';

// Responsive viewBox. The SVG scales to fit its container (preserveAspectRatio),
// so nodes are always fully contained — never clipping out of the frame.
const W = 880;
const H = 340;
const NODE_R = 26;
const PAD_X = NODE_R + 14;
const PAD_Y = NODE_R + 26; // room for the name label under each node
const MAX_NAME = 16;
const MAX_TITLE = 18;

const trunc = (s, n) => (s && s.length > n ? s.slice(0, n) + '…' : s || '');

// BFS distances over the player's web (found artists + the songs they've named).
function bfs(startId, adj) {
  const dist = { [startId]: 0 };
  const q = [startId];
  let i = 0;
  while (i < q.length) {
    const cur = q[i++];
    for (const nb of adj[cur] || []) {
      if (!(nb in dist)) { dist[nb] = dist[cur] + 1; q.push(nb); }
    }
  }
  return dist;
}

// Dual-anchor layout: start anchors the left, target the right; everything else
// settles into columns by how far it is from each side. The two halves grow
// toward the middle and meet when the puzzle is solved.
function layout(found, edges, startId, targetId) {
  const ids = found.map((a) => a.id);
  const adj = {};
  ids.forEach((id) => { adj[id] = new Set(); });
  for (const e of edges) {
    const members = e.artistIds.filter((id) => adj[id]);
    for (const a of members) for (const b of members) if (a !== b) adj[a].add(b);
  }
  const adjArr = {};
  ids.forEach((id) => { adjArr[id] = [...adj[id]]; });

  const dStart = bfs(startId, adjArr);
  const dTarget = bfs(targetId, adjArr);

  const meta = {};
  for (const id of ids) {
    const ds = dStart[id];
    const dt = dTarget[id];
    let side, rank;
    if (ds != null && (dt == null || ds <= dt)) { side = 'start'; rank = ds; }
    else if (dt != null) { side = 'target'; rank = dt; }
    else { side = 'start'; rank = 0; } // isolated (shouldn't happen)
    meta[id] = { side, rank };
  }
  const maxS = Math.max(0, ...ids.filter((id) => meta[id].side === 'start').map((id) => meta[id].rank));
  const maxT = Math.max(0, ...ids.filter((id) => meta[id].side === 'target').map((id) => meta[id].rank));
  const cols = (maxS + 1) + (maxT + 1);
  const colIndex = (id) => {
    const m = meta[id];
    return m.side === 'start' ? m.rank : (maxS + 1) + (maxT - m.rank);
  };

  // Group by column, then spread vertically within each column.
  const byCol = {};
  for (const id of ids) {
    const ci = colIndex(id);
    (byCol[ci] = byCol[ci] || []).push(id);
  }

  const pos = {};
  for (const ci of Object.keys(byCol)) {
    const group = byCol[ci];
    const n = group.length;
    const xnorm = cols <= 1 ? 0.5 : (Number(ci) + 0.5) / cols;
    group.forEach((id, k) => {
      const ynorm = n <= 1 ? 0.5 : (k + 0.5) / n;
      pos[id] = {
        x: PAD_X + xnorm * (W - 2 * PAD_X),
        y: PAD_Y + ynorm * (H - 2 * PAD_Y),
      };
    });
  }
  return pos;
}

const ConstellationGraph = ({ found, edges = [], startId, targetId, isVictory = false }) => {
  const instanceId = useId().replace(/[^a-zA-Z0-9]/g, '_');
  const pos = useMemo(() => layout(found || [], edges || [], startId, targetId), [found, edges, startId, targetId]);

  if (!found || !found.length) return null;

  return (
    <div className={`constellation-container${isVictory ? ' constellation-victory' : ''}`}>
      <svg
        viewBox={`0 0 ${W} ${H}`}
        preserveAspectRatio="xMidYMid meet"
        xmlns="http://www.w3.org/2000/svg"
        aria-label="Artist connection constellation"
      >
        <defs>
          <filter id={`nodeGlow-${instanceId}`} x="-40%" y="-40%" width="180%" height="180%">
            <feGaussianBlur stdDeviation="4" result="blur" />
            <feMerge><feMergeNode in="blur" /><feMergeNode in="SourceGraphic" /></feMerge>
          </filter>
          <filter id={`nodeBrightGlow-${instanceId}`} x="-50%" y="-50%" width="200%" height="200%">
            <feGaussianBlur stdDeviation="7" result="blur" />
            <feMerge><feMergeNode in="blur" /><feMergeNode in="SourceGraphic" /></feMerge>
          </filter>
          <filter id={`lineGlow-${instanceId}`} x="-20%" y="-120%" width="140%" height="340%">
            <feGaussianBlur stdDeviation="2.2" result="blur" />
            <feMerge><feMergeNode in="blur" /><feMergeNode in="SourceGraphic" /></feMerge>
          </filter>
          <linearGradient id={`lineGradient-${instanceId}`} x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stopColor="#8fa8d6" stopOpacity="0.55" />
            <stop offset="50%" stopColor="#b8c6e0" stopOpacity="0.9" />
            <stop offset="100%" stopColor="#8fa8d6" stopOpacity="0.55" />
          </linearGradient>
          <linearGradient id={`victoryLineGradient-${instanceId}`} x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stopColor="#c084fc" stopOpacity="0.7" />
            <stop offset="50%" stopColor="#e8eeff" stopOpacity="1" />
            <stop offset="100%" stopColor="#c084fc" stopOpacity="0.7" />
          </linearGradient>
          {found.map((a) => (
            <clipPath key={`clip-${a.id}`} id={`clip-${instanceId}-${a.id}`}>
              <circle cx={pos[a.id]?.x ?? 0} cy={pos[a.id]?.y ?? 0} r={NODE_R - 2} />
            </clipPath>
          ))}
        </defs>

        {/* Edges: each named song links its credited artists (sorted left→right). */}
        {edges.map((e, ei) => {
          const members = (e.artistIds || []).filter((id) => pos[id]).sort((a, b) => pos[a].x - pos[b].x);
          if (members.length < 2) return null;
          const title = e.song?.title || '';
          const segs = [];
          for (let i = 0; i < members.length - 1; i++) {
            segs.push([pos[members[i]], pos[members[i + 1]]]);
          }
          const mid = segs[Math.floor((segs.length - 1) / 2)];
          const mx = (mid[0].x + mid[1].x) / 2;
          const my = (mid[0].y + mid[1].y) / 2;
          return (
            <g key={`edge-${ei}`} className="constellation-line-group">
              {segs.map(([from, to], si) => {
                const len = Math.hypot(to.x - from.x, to.y - from.y);
                return (
                  <line
                    key={si}
                    x1={from.x} y1={from.y} x2={to.x} y2={to.y}
                    stroke={isVictory ? `url(#victoryLineGradient-${instanceId})` : `url(#lineGradient-${instanceId})`}
                    strokeWidth={isVictory ? 2.6 : 1.6}
                    filter={`url(#lineGlow-${instanceId})`}
                    className="constellation-line"
                    strokeDasharray={len}
                    strokeDashoffset={len}
                    style={{ animationDelay: `${ei * 0.12 + si * 0.06}s` }}
                  />
                );
              })}
              {title && (
                <text x={mx} y={my - 9} textAnchor="middle" className="constellation-collab-label">
                  {trunc(title, MAX_TITLE)}
                </text>
              )}
            </g>
          );
        })}

        {/* Nodes */}
        {found.map((artist) => {
          const p = pos[artist.id];
          if (!p) return null;
          const isStart = artist.id === startId;
          const isTarget = artist.id === targetId;
          const ringColor = isVictory && (isStart || isTarget) ? '#c084fc'
            : isTarget ? '#f472b6'
            : isStart ? '#b8c6e0'
            : '#8fa8d6';
          const strong = isStart || isTarget || isVictory;
          const ringWidth = strong ? 2.5 : 1.5;
          const filterId = strong ? `nodeBrightGlow-${instanceId}` : `nodeGlow-${instanceId}`;
          return (
            <g
              key={`node-${artist.id}`}
              className={`constellation-node${isStart ? ' node-current' : ''}${isTarget ? ' node-target' : ''}${isVictory ? ' node-victory' : ''}`}
            >
              <circle cx={p.x} cy={p.y} r={NODE_R + 6} fill="none" stroke={ringColor} strokeWidth={ringWidth}
                opacity={0.35} filter={`url(#${filterId})`} className={strong ? 'node-ring-pulse' : 'node-ring'} />
              <circle cx={p.x} cy={p.y} r={NODE_R} fill="#0c1121" stroke={ringColor} strokeWidth={ringWidth} filter={`url(#${filterId})`} />
              <image
                href={getSmallAvatarUrl(artist)}
                x={p.x - NODE_R + 2} y={p.y - NODE_R + 2}
                width={(NODE_R - 2) * 2} height={(NODE_R - 2) * 2}
                clipPath={`url(#clip-${instanceId}-${artist.id})`}
                preserveAspectRatio="xMidYMid slice"
              />
              {(isStart || isTarget) && (
                <text x={p.x} y={p.y - NODE_R - 7} textAnchor="middle" className="constellation-anchor-tag">
                  {isStart ? 'START' : 'TARGET'}
                </text>
              )}
              <text x={p.x} y={p.y + NODE_R + 16} textAnchor="middle"
                className={`constellation-label${isStart || isTarget ? ' label-current' : ''}`}>
                {trunc(artist.name, MAX_NAME)}
              </text>
            </g>
          );
        })}
      </svg>
    </div>
  );
};

export default ConstellationGraph;
