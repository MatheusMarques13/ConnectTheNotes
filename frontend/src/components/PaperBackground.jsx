import React from 'react';

// Warm "sheet music" backdrop — five-line staves with faint notes, on paper.
// Fixed, behind everything, non-interactive. (art-comfy direction)
const PaperBackground = () => (
  <div className="paper-bg" aria-hidden="true">
    <div className="paper-staves" />
    <div className="paper-notes" />
    <div className="paper-vignette" />
  </div>
);

export default PaperBackground;
