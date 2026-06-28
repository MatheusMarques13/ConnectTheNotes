import React from 'react';

// Warm ruled "paper" backdrop (staff-paper vibe) — the art-comfy direction.
// Fixed, behind everything, non-interactive.
const PaperBackground = () => (
  <div className="paper-bg" aria-hidden="true">
    <div className="paper-rules" />
    <div className="paper-vignette" />
  </div>
);

export default PaperBackground;
