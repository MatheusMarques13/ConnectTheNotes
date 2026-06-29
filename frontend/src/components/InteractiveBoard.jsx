import React, { useRef, useReducer, useMemo, useEffect, useLayoutEffect, useCallback } from 'react';
import { Music2, Disc, Disc3, Radio, Tv, Film, Mic2, Play, Pause } from 'lucide-react';
import { getSmallAvatarUrl } from '../utils/avatars';
import { getSongMedia } from '../utils/deezer';
import { useArtistImage } from '../utils/useArtistImage';
import * as preview from '../utils/preview';
import './board.css';

// ── node id helpers (namespace by first char: 'a' artist, 's' song) ──
const artistNodeId = (id) => 'a' + id;
const songNodeId = (id) => 's' + id;
const W_A = 132, H_A = 150, W_S = 162, H_S = 228;
const sizeById = (id) => (id[0] === 'a' ? { w: W_A, h: H_A } : { w: W_S, h: H_S });

const ANCHOR_GAP = 500, STEP = 58, RING_BASE = 140, GAP = 16, MAX_RING = 16;
const MIN_Z = 0.4, MAX_Z = 2.4, THRESH = 5;
const clamp = (v, a, b) => Math.min(b, Math.max(a, v));
const snap = (v) => Math.round(v / STEP) * STEP;
const hashStr = (s) => { let h = 0; for (let i = 0; i < s.length; i++) h = (h * 31 + s.charCodeAt(i)) >>> 0; return h; };

const TYPE_ICON = { song: Music2, album: Disc, ep: Disc3, mixtape: Disc3, live: Radio, dvd: Tv, video: Film, feature: Mic2 };
const TYPE_LABEL = { song: 'Song', album: 'Album', ep: 'EP', mixtape: 'Mixtape', live: 'Live', dvd: 'DVD', video: 'Video', feature: 'Feature' };

const buildNodes = (found, edges) => {
  const out = [];
  for (const a of found) out.push({ id: artistNodeId(a.id), kind: 'artist', artistId: a.id, data: a });
  for (const e of edges) out.push({ id: songNodeId(e.song.id), kind: 'song', songId: e.song.id, data: e.song, artistIds: e.artistIds });
  return out;
};
const buildLinks = (edges, foundIds) => {
  const out = [];
  for (const e of edges) {
    const s = songNodeId(e.song.id);
    for (const aid of e.artistIds) if (foundIds.has(aid)) out.push({ id: s + '|' + artistNodeId(aid), from: s, to: artistNodeId(aid) });
  }
  return out;
};

const MiniAvatar = ({ artist }) => {
  const [loaded, setLoaded] = React.useState(false);
  const initials = (artist?.name || '?').split(' ').map((w) => w[0]).join('').slice(0, 2).toUpperCase();
  return (
    <span className="ctn-mini-av">
      <img src={getSmallAvatarUrl(artist)} alt="" onLoad={() => setLoaded(true)} onError={(e) => { e.target.style.display = 'none'; }} style={{ opacity: loaded ? 1 : 0 }} />
      {!loaded && <span style={{ position: 'absolute', inset: 0, display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 9, color: '#0c1121', fontWeight: 700 }}>{initials}</span>}
    </span>
  );
};

const ArtistCardInner = ({ artist, isStart, isTarget }) => {
  const [loaded, setLoaded] = React.useState(false);
  const imgUrl = useArtistImage(artist, 200);
  const initials = (artist?.name || '?').split(' ').map((w) => w[0]).join('').slice(0, 2).toUpperCase();
  return (
    <div className="ctn-artist-note">
      {(isStart || isTarget) && <span className={`ctn-node-tag ${isStart ? 'start' : 'target'}`}>{isStart ? 'Start' : 'Target'}</span>}
      <div className="ctn-artist-photo">
        <span className="ctn-artist-ring" />
        <img src={imgUrl} alt={artist.name} onLoad={() => setLoaded(true)} onError={(e) => { e.target.style.display = 'none'; }} style={{ opacity: loaded ? 1 : 0 }} />
        {!loaded && <span className="ctn-artist-fallback">{initials}</span>}
      </div>
      <div className="ctn-artist-name">{artist.name}</div>
    </div>
  );
};

const SongCardInner = ({ song, artists }) => {
  const [broken, setBroken] = React.useState(false);
  const [cover, setCover] = React.useState(song.coverUrl || '');
  const [st, setSt] = React.useState(() => preview.status(song.id));
  const Icon = TYPE_ICON[song.type] || Music2;
  const primary = (artists[0] && artists[0].name) || '';

  // Keep the play/pause button in sync with the single shared audio.
  React.useEffect(() => preview.subscribe(() => setSt(preview.status(song.id))), [song.id]);
  // Lazily pull the album cover from Deezer at runtime if it wasn't baked.
  React.useEffect(() => {
    if (cover) return undefined;
    let alive = true;
    getSongMedia(song.title, primary).then((m) => { if (alive && m && m.cover) setCover(m.cover); });
    return () => { alive = false; };
  }, [song.id]); // eslint-disable-line react-hooks/exhaustive-deps

  const hasArt = cover && !broken;
  const shown = artists.slice(0, 4);
  const extra = artists.length - shown.length;
  const onPlay = (e) => { e.stopPropagation(); e.preventDefault(); preview.unlock(); preview.toggle(song, primary); };

  return (
    <div className="ctn-song-card">
      <div className={`ctn-song-cover${hasArt ? '' : ' no-art'}`}>
        {hasArt
          ? <img src={cover} alt="" onError={() => setBroken(true)} />
          : <Icon />}
        <span className="ctn-song-type"><Icon size={9} /> {TYPE_LABEL[song.type] || song.type}</span>
        <button
          className={`ctn-song-play${st.playing ? ' playing' : ''}`}
          onPointerDown={(e) => e.stopPropagation()}
          onClick={onPlay}
          aria-label={st.playing ? 'pause preview' : 'play preview'}
        >
          {st.playing ? <Pause size={15} /> : <Play size={15} />}
        </button>
      </div>
      <div className="ctn-song-body">
        <div className="ctn-song-title">{song.title}</div>
        <div className="ctn-song-year">{song.year}</div>
        <div className="ctn-song-caption">Artists found</div>
        <div className="ctn-song-credits">
          {shown.map((a) => <MiniAvatar key={a.id} artist={a} />)}
          {extra > 0 && <span className="ctn-credit-more">+{extra}</span>}
        </div>
      </div>
    </div>
  );
};

const InteractiveBoard = ({ found, edges, startId, targetId, onOpenInfo, boardApiRef }) => {
  const viewportRef = useRef(null), layerRef = useRef(null), edgesGroupRef = useRef(null);
  const camRef = useRef({ panX: 0, panY: 0, zoom: 1 });
  const [, bump] = useReducer((c) => c + 1, 0);
  const posRef = useRef({});                 // nodeId -> { x, y, manual }
  const modeRef = useRef('IDLE');            // IDLE|MAYBE_BG|MAYBE_NODE|PAN|NODE_DRAG|PINCH
  const pointers = useRef(new Map());
  const startRef = useRef({ x: 0, y: 0 }), lastRef = useRef({ x: 0, y: 0 });
  const dragIdRef = useRef(null), rafRef = useRef(0), pinchRef = useRef(null);
  const nodeElRef = useRef({}), lineElRef = useRef({});
  const incidenceRef = useRef({});
  const tweenRef = useRef(0);
  const didCenterRef = useRef(false);
  const [selectedId, setSelectedId] = React.useState(null);

  const startNodeId = artistNodeId(startId);
  const targetNodeId = artistNodeId(targetId);

  const foundIds = useMemo(() => new Set(found.map((a) => a.id)), [found]);
  const artistById = useMemo(() => { const m = {}; found.forEach((a) => { m[a.id] = a; }); return m; }, [found]);
  const nodes = useMemo(() => buildNodes(found, edges), [found, edges]);
  const links = useMemo(() => buildLinks(edges, foundIds), [edges, foundIds]);
  const edgesRef = useRef(edges); edgesRef.current = edges;

  // incidence: nodeId -> [link]
  useMemo(() => {
    const inc = {};
    for (const lk of links) { (inc[lk.from] = inc[lk.from] || []).push(lk); (inc[lk.to] = inc[lk.to] || []).push(lk); }
    incidenceRef.current = inc;
  }, [links]);

  const rectOf = () => viewportRef.current.getBoundingClientRect();
  const applyTransform = useCallback(() => {
    const { panX, panY, zoom } = camRef.current;
    if (layerRef.current) layerRef.current.style.transform = `translate(${panX}px,${panY}px) scale(${zoom})`;
    if (edgesGroupRef.current) edgesGroupRef.current.setAttribute('transform', `translate(${panX} ${panY}) scale(${zoom})`);
  }, []);
  const schedule = (fn) => { if (!rafRef.current) rafRef.current = requestAnimationFrame(() => { rafRef.current = 0; fn(); }); };
  const freezeCam = () => { cancelAnimationFrame(tweenRef.current); tweenRef.current = 0; camRef.current = { ...camRef.current }; };

  const toBoard = (cx, cy) => { const r = rectOf(); const c = camRef.current; return { x: (cx - r.left - c.panX) / c.zoom, y: (cy - r.top - c.panY) / c.zoom }; };
  const zoomAt = (sx, sy, nextZoom) => { const c = camRef.current; const nz = clamp(nextZoom, MIN_Z, MAX_Z); const k = nz / c.zoom; c.panX = sx - (sx - c.panX) * k; c.panY = sy - (sy - c.panY) * k; c.zoom = nz; };

  // keep DOM transform synced to camRef after every render
  useLayoutEffect(() => { applyTransform(); });

  // ── layout placement ──
  const collides = (cx, cy, w, h, placed) => {
    for (const id of placed) {
      const o = posRef.current[id]; if (!o) continue; const s = sizeById(id);
      if (Math.abs(cx - o.x) * 2 < (w + s.w + 2 * GAP) && Math.abs(cy - o.y) * 2 < (h + s.h + 2 * GAP)) return true;
    }
    return false;
  };
  const spiralPlace = (node, src, placed) => {
    const { w, h } = sizeById(node.id);
    for (let ring = 0; ring <= MAX_RING; ring++) {
      const r = RING_BASE + ring * STEP, slots = ring === 0 ? 1 : 6 * ring;
      for (let k = 0; k < slots; k++) {
        const ang = (2 * Math.PI / slots) * k + ring * 0.4;
        const cx = snap(src.x + r * Math.cos(ang)), cy = snap(src.y + r * Math.sin(ang));
        if (!collides(cx, cy, w, h, placed)) return { x: cx, y: cy };
      }
    }
    return { x: snap(src.x), y: snap(src.y + RING_BASE + MAX_RING * STEP) };
  };
  const sourceFor = (node, placed) => {
    if (node.kind === 'song') {
      const cand = node.artistIds.map(artistNodeId).filter((id) => placed.has(id));
      if (cand.length) return cand.sort((a, b) => Math.abs(posRef.current[a].x) - Math.abs(posRef.current[b].x))[0];
      return startNodeId;
    }
    for (const e of edgesRef.current) if (e.artistIds.includes(node.artistId)) { const s = songNodeId(e.song.id); if (placed.has(s)) return s; }
    return startNodeId;
  };
  const reconcile = useCallback((nodeList) => {
    const pos = posRef.current;
    if (!pos[startNodeId]) pos[startNodeId] = { x: -ANCHOR_GAP / 2, y: 0, manual: false };
    if (!pos[targetNodeId]) pos[targetNodeId] = { x: ANCHOR_GAP / 2, y: 0, manual: false };
    const placed = new Set(Object.keys(pos));
    const pending = nodeList.filter((n) => !placed.has(n.id)).sort((a, b) => (a.kind === 'song' ? 0 : 1) - (b.kind === 'song' ? 0 : 1));
    for (const n of pending) {
      const src = pos[sourceFor(n, placed)] || pos[startNodeId];
      pos[n.id] = { ...spiralPlace(n, src, placed), manual: false };
      placed.add(n.id);
    }
    const live = new Set(nodeList.map((n) => n.id)); live.add(startNodeId); live.add(targetNodeId);
    for (const id of Object.keys(pos)) if (!live.has(id)) delete pos[id];
  }, [startNodeId, targetNodeId]);

  useLayoutEffect(() => { reconcile(nodes); bump(); }, [nodes, reconcile]);

  // ── camera animation / recenter ──
  const setCameraCommit = () => { camRef.current = { ...camRef.current }; bump(); };
  const tweenTo = (target) => {
    cancelAnimationFrame(tweenRef.current);
    if (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) { camRef.current = { ...target }; applyTransform(); setCameraCommit(); return; }
    const from = { ...camRef.current }; const t0 = performance.now(); const dur = 360;
    const ease = (t) => (t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2);
    const step = (now) => {
      const t = Math.min(1, (now - t0) / dur); const e = ease(t);
      camRef.current = { panX: from.panX + (target.panX - from.panX) * e, panY: from.panY + (target.panY - from.panY) * e, zoom: from.zoom + (target.zoom - from.zoom) * e };
      applyTransform();
      if (t < 1) tweenRef.current = requestAnimationFrame(step); else setCameraCommit();
    };
    tweenRef.current = requestAnimationFrame(step);
  };
  const recenter = useCallback(() => {
    const ids = Object.keys(posRef.current); const r = rectOf();
    if (!ids.length) { camRef.current = { panX: r.width / 2, panY: r.height / 2, zoom: 1 }; applyTransform(); setCameraCommit(); return; }
    let minX = Infinity, minY = Infinity, maxX = -Infinity, maxY = -Infinity;
    for (const id of ids) { const p = posRef.current[id]; const s = sizeById(id); minX = Math.min(minX, p.x - s.w / 2); maxX = Math.max(maxX, p.x + s.w / 2); minY = Math.min(minY, p.y - s.h / 2); maxY = Math.max(maxY, p.y + s.h / 2); }
    // fit into the area left clear of the fixed chrome (top bar, input dock,
    // zoom controls, helper hints), with a little breathing room.
    const insT = 80, insB = 140, insX = 80;
    const availW = Math.max(80, r.width - 2 * insX), availH = Math.max(80, r.height - insT - insB);
    const contentW = Math.max(1, maxX - minX), contentH = Math.max(1, maxY - minY);
    const cx = (minX + maxX) / 2, cy = (minY + maxY) / 2;
    const z = clamp(Math.min(availW / contentW, availH / contentH) * 0.96, MIN_Z, 1.15);
    const regionCx = insX + availW / 2, regionCy = insT + availH / 2;
    tweenTo({ zoom: z, panX: regionCx - cx * z, panY: regionCy - cy * z });
  }, [applyTransform]);
  const zoomBy = useCallback((f) => { const r = rectOf(); zoomAt(r.width / 2, r.height / 2, camRef.current.zoom * f); applyTransform(); setCameraCommit(); }, [applyTransform]);

  useEffect(() => { if (boardApiRef) boardApiRef.current = { recenter, zoomBy }; }, [boardApiRef, recenter, zoomBy]);
  // keep the whole web framed: fit once after first layout, then re-fit whenever
  // the web grows (a new artist/song appears) — but never mid-gesture.
  const prevCountRef = useRef(0);
  useEffect(() => {
    const n = nodes.length; if (!n) return;
    if (!didCenterRef.current) { didCenterRef.current = true; prevCountRef.current = n; recenter(); return; }
    if (n > prevCountRef.current && modeRef.current === 'IDLE') recenter();
    prevCountRef.current = n;
  }, [nodes.length, recenter]);

  // ── imperative painters during drag ──
  const paintNode = (id) => { const el = nodeElRef.current[id]; const p = posRef.current[id]; if (el && p) { el.style.left = p.x + 'px'; el.style.top = p.y + 'px'; } };
  const paintIncident = (id) => { for (const lk of incidenceRef.current[id] || []) { const line = lineElRef.current[lk.id]; if (!line) continue; const from = posRef.current[lk.from], to = posRef.current[lk.to]; if (from && to) { line.setAttribute('x1', from.x); line.setAttribute('y1', from.y); line.setAttribute('x2', to.x); line.setAttribute('y2', to.y); } } };

  // ── wheel (native, non-passive) ──
  useEffect(() => {
    const el = viewportRef.current; if (!el) return;
    const onWheel = (e) => { e.preventDefault(); const r = el.getBoundingClientRect(); zoomAt(e.clientX - r.left, e.clientY - r.top, camRef.current.zoom * Math.exp(-e.deltaY * 0.0015)); schedule(applyTransform); clearTimeout(onWheel._t); onWheel._t = setTimeout(setCameraCommit, 140); };
    el.addEventListener('wheel', onWheel, { passive: false });
    return () => el.removeEventListener('wheel', onWheel);
  }, [applyTransform]); // eslint-disable-line react-hooks/exhaustive-deps

  // ── pinch ──
  const startPinch = () => {
    const pts = [...pointers.current.values()]; if (pts.length < 2) return; freezeCam(); const r = rectOf();
    const p0 = { x: pts[0].x - r.left, y: pts[0].y - r.top }, p1 = { x: pts[1].x - r.left, y: pts[1].y - r.top };
    pinchRef.current = { startDist: Math.hypot(p1.x - p0.x, p1.y - p0.y) || 1, startZoom: camRef.current.zoom, lastMid: { x: (p0.x + p1.x) / 2, y: (p0.y + p1.y) / 2 } };
    modeRef.current = 'PINCH';
  };
  const updatePinch = () => {
    const pts = [...pointers.current.values()]; if (pts.length < 2 || !pinchRef.current) return; const r = rectOf();
    const p0 = { x: pts[0].x - r.left, y: pts[0].y - r.top }, p1 = { x: pts[1].x - r.left, y: pts[1].y - r.top };
    const dist = Math.hypot(p1.x - p0.x, p1.y - p0.y) || 1; const mid = { x: (p0.x + p1.x) / 2, y: (p0.y + p1.y) / 2 };
    zoomAt(mid.x, mid.y, pinchRef.current.startZoom * dist / pinchRef.current.startDist);
    const c = camRef.current; c.panX += mid.x - pinchRef.current.lastMid.x; c.panY += mid.y - pinchRef.current.lastMid.y; pinchRef.current.lastMid = mid;
    applyTransform();
  };

  // ── pointer state machine ──
  const onViewportPointerDown = (e) => {
    viewportRef.current.setPointerCapture(e.pointerId);
    pointers.current.set(e.pointerId, { x: e.clientX, y: e.clientY });
    startRef.current = lastRef.current = { x: e.clientX, y: e.clientY };
    if (pointers.current.size === 2) startPinch();
    else { modeRef.current = 'MAYBE_BG'; }
  };
  const onNodePointerDown = (e, id) => {
    e.stopPropagation();
    viewportRef.current.setPointerCapture(e.pointerId);
    pointers.current.set(e.pointerId, { x: e.clientX, y: e.clientY });
    startRef.current = lastRef.current = { x: e.clientX, y: e.clientY };
    if (pointers.current.size === 2) { startPinch(); return; } // 2nd finger on a card → pinch, not node-drag
    dragIdRef.current = id; modeRef.current = 'MAYBE_NODE';
  };
  const onPointerMove = (e) => {
    if (!pointers.current.has(e.pointerId)) return;
    pointers.current.set(e.pointerId, { x: e.clientX, y: e.clientY });
    if (modeRef.current === 'PINCH') { schedule(updatePinch); return; }
    const dx = e.clientX - lastRef.current.x, dy = e.clientY - lastRef.current.y;
    if (modeRef.current === 'MAYBE_BG' || modeRef.current === 'MAYBE_NODE') {
      if (Math.hypot(e.clientX - startRef.current.x, e.clientY - startRef.current.y) <= THRESH) { lastRef.current = { x: e.clientX, y: e.clientY }; return; }
      modeRef.current = modeRef.current === 'MAYBE_BG' ? 'PAN' : 'NODE_DRAG';
      freezeCam(); // stop any in-flight recenter tween so it doesn't fight the drag
      if (modeRef.current === 'PAN' && viewportRef.current) viewportRef.current.classList.add('panning');
      if (modeRef.current === 'NODE_DRAG') { const el = nodeElRef.current[dragIdRef.current]; if (el) el.classList.add('dragging'); }
    }
    if (modeRef.current === 'PAN') { const c = camRef.current; c.panX += dx; c.panY += dy; schedule(applyTransform); }
    else if (modeRef.current === 'NODE_DRAG') { const z = camRef.current.zoom; const p = posRef.current[dragIdRef.current]; if (p) { p.x += dx / z; p.y += dy / z; p.manual = true; const id = dragIdRef.current; schedule(() => { paintNode(id); paintIncident(id); }); } }
    lastRef.current = { x: e.clientX, y: e.clientY };
  };
  const onPointerUp = (e) => {
    try { viewportRef.current.releasePointerCapture(e.pointerId); } catch (err) { /* ignore */ }
    pointers.current.delete(e.pointerId);
    if (viewportRef.current) viewportRef.current.classList.remove('panning');
    const mode = modeRef.current;
    if (mode === 'MAYBE_NODE') {
      const node = nodes.find((n) => n.id === dragIdRef.current);
      setSelectedId(dragIdRef.current);
      if (node && onOpenInfo) onOpenInfo(node.kind === 'artist' ? { kind: 'artist', artist: node.data } : { kind: 'song', song: node.data, artists: node.artistIds.map((aid) => artistById[aid]).filter(Boolean) });
    } else if (mode === 'MAYBE_BG') {
      setSelectedId(null);
    } else if (mode === 'PAN' || mode === 'PINCH') {
      setCameraCommit();
    } else if (mode === 'NODE_DRAG') {
      const el = nodeElRef.current[dragIdRef.current]; if (el) el.classList.remove('dragging');
      bump();
    }
    if (pointers.current.size === 1) { modeRef.current = 'PAN'; const only = [...pointers.current.values()][0]; startRef.current = lastRef.current = { ...only }; dragIdRef.current = null; pinchRef.current = null; }
    else if (pointers.current.size === 0) { modeRef.current = 'IDLE'; dragIdRef.current = null; pinchRef.current = null; }
  };

  return (
    <div
      ref={viewportRef}
      className="ctn-board-viewport"
      onPointerDown={onViewportPointerDown}
      onPointerMove={onPointerMove}
      onPointerUp={onPointerUp}
      onPointerCancel={onPointerUp}
    >
      <svg className="ctn-edges" xmlns="http://www.w3.org/2000/svg">
        <defs>
          <linearGradient id="ctnLineGradient" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stopColor="#8fa8d6" stopOpacity="0.55" />
            <stop offset="50%" stopColor="#b8c6e0" stopOpacity="0.9" />
            <stop offset="100%" stopColor="#8fa8d6" stopOpacity="0.55" />
          </linearGradient>
          <linearGradient id="ctnVictoryLineGradient" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stopColor="#c084fc" stopOpacity="0.7" />
            <stop offset="50%" stopColor="#e8eeff" stopOpacity="1" />
            <stop offset="100%" stopColor="#c084fc" stopOpacity="0.7" />
          </linearGradient>
        </defs>
        <g ref={edgesGroupRef}>
          {links.map((lk) => {
            const from = posRef.current[lk.from], to = posRef.current[lk.to];
            if (!from || !to) return null;
            const active = selectedId && (lk.from === selectedId || lk.to === selectedId);
            return (
              <line
                key={lk.id}
                ref={(el) => { if (el) lineElRef.current[lk.id] = el; else delete lineElRef.current[lk.id]; }}
                className={`ctn-edge-line${active ? ' is-active' : ''}`}
                x1={from.x} y1={from.y} x2={to.x} y2={to.y}
              />
            );
          })}
        </g>
      </svg>

      <div ref={layerRef} className="ctn-board-layer">
        {nodes.map((node) => {
          const p = posRef.current[node.id]; if (!p) return null;
          const isStart = node.kind === 'artist' && node.artistId === startId;
          const isTarget = node.kind === 'artist' && node.artistId === targetId;
          const h = hashStr(node.id);
          const deco = ` ctn-tone-${h % 5} ctn-tilt-${h % 3}`;
          const cls = (node.kind === 'artist'
            ? `ctn-node ctn-node-artist${isStart ? ' is-start' : ''}${isTarget ? ' is-target' : ''}${selectedId === node.id ? ' selected' : ''}`
            : `ctn-node ctn-node-song${selectedId === node.id ? ' selected' : ''}`) + deco;
          return (
            <div
              key={node.id}
              ref={(el) => { if (el) nodeElRef.current[node.id] = el; else delete nodeElRef.current[node.id]; }}
              className={cls}
              style={{ left: p.x, top: p.y }}
              onPointerDown={(e) => onNodePointerDown(e, node.id)}
            >
              {node.kind === 'artist'
                ? <ArtistCardInner artist={node.data} isStart={isStart} isTarget={isTarget} />
                : <SongCardInner song={node.data} artists={node.artistIds.map((aid) => artistById[aid]).filter(Boolean)} />}
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default InteractiveBoard;
