# Modo Mynd — art direction

The house visual language. Comfy, clean, tactile — *a terminal made cozy*
crossed with the warmth of analog paper and scrapbook stickies. Reusable
across projects; copy the token block below and the principles to re-skin
anything into Modo Mynd.

## Principles

1. **One typeface, monospace, everywhere.** `IBM Plex Mono` (weights 400 / 500).
   It carries most of the identity on its own.
2. **Lowercase, low-key copy.** Headings and labels in lowercase; write the
   strings lowercase rather than forcing it in CSS.
3. **Warm paper ground.** A soft, warm off-white. The background can be themed
   with faint ruled lines — here it's **music staves ("partitura")** for
   *Connect the Notes*; elsewhere it can be notebook rules, grid, dots, etc.
4. **Things look placed by hand.** Cards are **post-its** and **polaroids**:
   solid fills, soft drop shadows, a gentle 1–2° tilt, washi-tape strips,
   sticky-note accents, folded corners.
5. **Sparse, muted color.** The base is paper + ink; color shows up only as
   small pastel accents (blue / pink / mint / yellow / lilac), assorted.
6. **Soft, not hard.** Hairline borders (~5–10% alpha), one consistent radius
   (~12px), generous spacing, gentle springy motion.

## Tokens (copy-paste)

```css
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:ital,wght@0,400;0,500;0,600;1,400&display=swap');

:root {
  /* paper + ink */
  --paper: #faf6ed;
  --paper-2: #f3ecdd;
  --paper-line: #e9dfca;     /* ruled lines / staves */
  --text-primary: #2c2722;   /* ink */
  --text-secondary: #6f6657;
  --text-muted: #9c9384;

  /* sparse muted accents */
  --accent: #3e6ad4;         /* calm blue (primary) */
  --accent-warm: #c4663c;    /* clay / terracotta   */
  --accent-mint: #3aa37c;

  /* surfaces + shape */
  --surface: #f1eadc;
  --surface-hover: #eae1cf;
  --border-soft: rgba(44, 39, 34, 0.10);
  --border-hair: rgba(44, 39, 34, 0.06);
  --radius: 12px;

  --font-mono: 'IBM Plex Mono', monospace;
}

/* pastel sticky tones (assorted, hash a stable id -> 0..4) */
.tone-0 { --tone-bg:#dce9fb; --tone-bd:#b9d2f2; --tone-ink:#39598a; } /* blue   */
.tone-1 { --tone-bg:#fbdde8; --tone-bd:#f1c1d4; --tone-ink:#9a4d68; } /* pink   */
.tone-2 { --tone-bg:#d9f0e4; --tone-bd:#bde5d1; --tone-ink:#3a7a5c; } /* mint   */
.tone-3 { --tone-bg:#fbf1c9; --tone-bd:#efe2a6; --tone-ink:#7d6a2c; } /* yellow */
.tone-4 { --tone-bg:#e8e0f7; --tone-bd:#d5c8ef; --tone-ink:#5e4e86; } /* lilac  */

* { font-family: var(--font-mono); }
body { background: var(--paper); color: var(--text-primary); }
```

## Building blocks (where they live in this repo)

- **Background** — `frontend/src/components/PaperBackground.jsx` +
  `.paper-staves` / `.paper-notes` in `App.css` (swap the ruling for other
  projects).
- **Post-it / polaroid cards** — `.ctn-*` tone/tilt classes in
  `frontend/src/components/board.css` (board) and the `.artist-polaroid` /
  `.artist-postit` block in `App.css` (selection).
- **Tilt + tone** — assign per element from a stable hash of its id
  (`ctn-tone-N ctn-tilt-N`), so layout is varied but deterministic.

Keep it comfy.
