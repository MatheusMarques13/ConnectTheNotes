import React from 'react';

// Modo Mynd mark — a pastel-pink record player with a slowly spinning vinyl.
// Shared by the home hero and the in-game board header.
const MyndLogo = ({ className, size, spin = true }) => (
  <svg
    viewBox="0 0 100 100"
    className={className}
    width={size}
    height={size}
    aria-hidden="true"
  >
    {/* plinth */}
    <rect x="8" y="11" width="84" height="78" rx="13" fill="#f4d7e2" stroke="#e3b3c7" strokeWidth="1.4" />
    {/* platter mat */}
    <circle cx="44" cy="51" r="32" fill="#ecc3d3" />
    {/* spinning vinyl */}
    <g>
      {spin && <animateTransform attributeName="transform" type="rotate" from="0 44 51" to="360 44 51" dur="14s" repeatCount="indefinite" />}
      <circle cx="44" cy="51" r="30" fill="#b07f93" />
      <circle cx="44" cy="51" r="24" fill="none" stroke="#c8a0b1" strokeWidth="0.8" />
      <circle cx="44" cy="51" r="18" fill="none" stroke="#c8a0b1" strokeWidth="0.8" />
      <circle cx="44" cy="51" r="12" fill="none" stroke="#c8a0b1" strokeWidth="0.8" />
      <path d="M44 51 L44 23 A28 28 0 0 1 61 30 Z" fill="#ffffff" opacity="0.12" />
      <circle cx="44" cy="51" r="9" fill="#f6b6d0" />
    </g>
    {/* spindle */}
    <circle cx="44" cy="51" r="1.6" fill="#6e4a59" />
    {/* tonearm */}
    <circle cx="80" cy="24" r="5" fill="#f6b6d0" stroke="#e3b3c7" strokeWidth="1" />
    <circle cx="85" cy="20" r="2.6" fill="#9b7686" />
    <line x1="80" y1="24" x2="58" y2="42" stroke="#a98b97" strokeWidth="2.4" strokeLinecap="round" />
    <rect x="53.5" y="39.5" width="7" height="4.6" rx="1.2" fill="#9b7686" transform="rotate(140 57 42)" />
  </svg>
);

export default MyndLogo;
