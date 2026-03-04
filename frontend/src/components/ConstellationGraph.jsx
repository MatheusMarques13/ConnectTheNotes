import React, { useMemo, useId } from 'react';
import { getSmallAvatarUrl } from '../utils/avatars';

// Constants for layout
const SVG_WIDTH = 800;
const SVG_HEIGHT = 320;
const NODE_RADIUS = 30;
const CENTER_X = SVG_WIDTH / 2;
const CENTER_Y = SVG_HEIGHT / 2;
const STEP_DISTANCE = 160;
const MAX_ARTIST_NAME_LENGTH = 14;
const MAX_COLLAB_TITLE_LENGTH = 20;

// Spread nodes in an organic/spiral pattern to avoid straight lines
function computeNodePositions(chain) {
  if (!chain || chain.length === 0) return [];

  const positions = [];

  // First node at center
  positions.push({ x: CENTER_X, y: CENTER_Y });

  // Golden angle to spread nodes naturally
  const goldenAngle = 137.5 * (Math.PI / 180);

  for (let i = 1; i < chain.length; i++) {
    const prevPos = positions[i - 1];

    // Pick a direction based on golden angle to create organic spread
    const angle = goldenAngle * i + (i % 2 === 0 ? 0.3 : -0.3);

    let x = prevPos.x + STEP_DISTANCE * Math.cos(angle);
    let y = prevPos.y + STEP_DISTANCE * Math.sin(angle);

    // Clamp within viewBox with padding
    const padding = NODE_RADIUS + 40;
    x = Math.max(padding, Math.min(SVG_WIDTH - padding, x));
    y = Math.max(padding, Math.min(SVG_HEIGHT - padding, y));

    // Simple overlap avoidance: nudge if too close to any existing node
    let attempts = 0;
    while (attempts < 8) {
      const tooClose = positions.some(
        (p) => Math.hypot(p.x - x, p.y - y) < NODE_RADIUS * 2.5
      );
      if (!tooClose) break;
      const nudgeAngle = angle + (attempts + 1) * 0.6;
      x = prevPos.x + STEP_DISTANCE * Math.cos(nudgeAngle);
      y = prevPos.y + STEP_DISTANCE * Math.sin(nudgeAngle);
      x = Math.max(padding, Math.min(SVG_WIDTH - padding, x));
      y = Math.max(padding, Math.min(SVG_HEIGHT - padding, y));
      attempts++;
    }

    positions.push({ x, y });
  }

  return positions;
}

const ConstellationGraph = ({ chain, targetArtist, isVictory = false }) => {
  const instanceId = useId().replace(/[^a-zA-Z0-9]/g, '_');
  const positions = useMemo(() => computeNodePositions(chain), [chain]);

  if (!chain || chain.length < 1) return null;

  return (
    <div className={`constellation-container${isVictory ? ' constellation-victory' : ''}`}>
      <svg
        viewBox={`0 0 ${SVG_WIDTH} ${SVG_HEIGHT}`}
        xmlns="http://www.w3.org/2000/svg"
        aria-label="Artist connection constellation"
      >
        <defs>
          {/* Glow filter for nodes */}
          <filter id={`nodeGlow-${instanceId}`} x="-40%" y="-40%" width="180%" height="180%">
            <feGaussianBlur stdDeviation="4" result="blur" />
            <feMerge>
              <feMergeNode in="blur" />
              <feMergeNode in="SourceGraphic" />
            </feMerge>
          </filter>

          {/* Brighter glow for current / victory */}
          <filter id={`nodeBrightGlow-${instanceId}`} x="-50%" y="-50%" width="200%" height="200%">
            <feGaussianBlur stdDeviation="7" result="blur" />
            <feMerge>
              <feMergeNode in="blur" />
              <feMergeNode in="SourceGraphic" />
            </feMerge>
          </filter>

          {/* Line glow filter */}
          <filter id={`lineGlow-${instanceId}`} x="-20%" y="-100%" width="140%" height="300%">
            <feGaussianBlur stdDeviation="2.5" result="blur" />
            <feMerge>
              <feMergeNode in="blur" />
              <feMergeNode in="SourceGraphic" />
            </feMerge>
          </filter>

          {/* Gradient for constellation lines */}
          <linearGradient id={`lineGradient-${instanceId}`} x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stopColor="#8fa8d6" stopOpacity="0.6" />
            <stop offset="50%" stopColor="#b8c6e0" stopOpacity="0.9" />
            <stop offset="100%" stopColor="#8fa8d6" stopOpacity="0.6" />
          </linearGradient>

          {/* Victory line gradient */}
          <linearGradient id={`victoryLineGradient-${instanceId}`} x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stopColor="#c084fc" stopOpacity="0.7" />
            <stop offset="50%" stopColor="#e8eeff" stopOpacity="1" />
            <stop offset="100%" stopColor="#c084fc" stopOpacity="0.7" />
          </linearGradient>

          {/* Clip circles for avatar images */}
          {chain.map((_, i) => (
            <clipPath key={`clip-${i}`} id={`clip-${instanceId}-${i}`}>
              <circle cx={positions[i]?.x ?? 0} cy={positions[i]?.y ?? 0} r={NODE_RADIUS - 2} />
            </clipPath>
          ))}
        </defs>

        {/* Draw lines between consecutive nodes */}
        {chain.length > 1 &&
          chain.slice(0, -1).map((step, i) => {
            const from = positions[i];
            const to = positions[i + 1];
            if (!from || !to) return null;
            const midX = (from.x + to.x) / 2;
            const midY = (from.y + to.y) / 2;
            const collabTitle = chain[i + 1].collab?.title ?? '';
            const lineLen = Math.hypot(to.x - from.x, to.y - from.y);

            return (
              <g key={`line-${i}`} className="constellation-line-group">
                {/* Background glow line */}
                <line
                  x1={from.x}
                  y1={from.y}
                  x2={to.x}
                  y2={to.y}
                  stroke={isVictory ? `url(#victoryLineGradient-${instanceId})` : `url(#lineGradient-${instanceId})`}
                  strokeWidth={isVictory ? 3 : 1.5}
                  filter={`url(#lineGlow-${instanceId})`}
                  className="constellation-line"
                  strokeDasharray={lineLen}
                  strokeDashoffset={lineLen}
                  style={{ animationDelay: `${i * 0.15}s` }}
                />
                {/* Collab label at midpoint */}
                {collabTitle && (
                  <text
                    x={midX}
                    y={midY - 8}
                    textAnchor="middle"
                    className="constellation-collab-label"
                  >
                    {collabTitle.length > MAX_COLLAB_TITLE_LENGTH ? collabTitle.slice(0, MAX_COLLAB_TITLE_LENGTH) + '…' : collabTitle}
                  </text>
                )}
              </g>
            );
          })}

        {/* Draw nodes */}
        {chain.map((step, i) => {
          const pos = positions[i];
          if (!pos) return null;
          const isCurrentNode = i === chain.length - 1;
          const isTargetNode = targetArtist && step.artist.id === targetArtist.id;
          const avatarUrl = getSmallAvatarUrl(step.artist.name);

          const ringColor = isVictory
            ? '#c084fc'
            : isCurrentNode
            ? '#b8c6e0'
            : isTargetNode
            ? '#f472b6'
            : '#8fa8d6';

          const ringWidth = isCurrentNode || isVictory ? 2.5 : 1.5;
          const filterId =
            isCurrentNode || isVictory ? `nodeBrightGlow-${instanceId}` : `nodeGlow-${instanceId}`;

          return (
            <g
              key={`node-${i}`}
              className={`constellation-node${isCurrentNode ? ' node-current' : ''}${isTargetNode ? ' node-target' : ''}${isVictory ? ' node-victory' : ''}`}
              style={{ animationDelay: `${i * 0.12}s` }}
            >
              {/* Outer glow ring */}
              <circle
                cx={pos.x}
                cy={pos.y}
                r={NODE_RADIUS + 6}
                fill="none"
                stroke={ringColor}
                strokeWidth={ringWidth}
                opacity={0.35}
                filter={`url(#${filterId})`}
                className={isCurrentNode || isVictory ? 'node-ring-pulse' : 'node-ring'}
              />

              {/* Avatar background circle */}
              <circle
                cx={pos.x}
                cy={pos.y}
                r={NODE_RADIUS}
                fill="#0c1121"
                stroke={ringColor}
                strokeWidth={ringWidth}
                filter={`url(#${filterId})`}
              />

              {/* Avatar image */}
              <image
                href={avatarUrl}
                x={pos.x - NODE_RADIUS + 2}
                y={pos.y - NODE_RADIUS + 2}
                width={(NODE_RADIUS - 2) * 2}
                height={(NODE_RADIUS - 2) * 2}
                clipPath={`url(#clip-${instanceId}-${i})`}
                preserveAspectRatio="xMidYMid slice"
              />

              {/* Artist name label */}
              <text
                x={pos.x}
                y={pos.y + NODE_RADIUS + 16}
                textAnchor="middle"
                className={`constellation-label${isCurrentNode ? ' label-current' : ''}`}
              >
                {step.artist.name.length > MAX_ARTIST_NAME_LENGTH
                  ? step.artist.name.slice(0, MAX_ARTIST_NAME_LENGTH) + '…'
                  : step.artist.name}
              </text>
            </g>
          );
        })}
      </svg>
    </div>
  );
};

export default ConstellationGraph;
