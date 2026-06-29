// One shared <audio> for the whole game so only a single 30s preview ever plays
// at a time. Components subscribe to know whether a given song is the one
// playing, so the play/pause button on each card stays in sync.
import { getSongMedia } from './deezer';

let audio = null;
let currentId = null;
let playing = false;
let unlocked = false;
const subs = new Set();
const notify = () => subs.forEach((f) => { try { f(); } catch (e) { /* ignore */ } });

function el() {
  if (!audio) {
    audio = new Audio();
    audio.preload = 'none';
    audio.addEventListener('play', () => { playing = true; notify(); });
    audio.addEventListener('playing', () => { playing = true; notify(); });
    audio.addEventListener('pause', () => { playing = false; notify(); });
    audio.addEventListener('ended', () => { playing = false; notify(); });
  }
  return audio;
}

export const subscribe = (fn) => { subs.add(fn); return () => subs.delete(fn); };
export const status = (songId) => ({ current: currentId === songId, playing: playing && currentId === songId });

// Call from a real user gesture (e.g. submitting a guess) so the browser lets
// us start audio programmatically a moment later (autoplay-on-insert).
export function unlock() {
  if (unlocked) return;
  const a = el();
  try {
    a.muted = true;
    const p = a.play();
    if (p && p.then) p.then(() => { a.pause(); a.muted = false; a.currentTime = 0; unlocked = true; }).catch(() => { a.muted = false; });
    else { a.muted = false; unlocked = true; }
  } catch (e) { a.muted = false; }
}

async function resolveUrl(song, artist) {
  if (song && song.previewUrl) return song.previewUrl;
  const m = await getSongMedia(song.title, artist || '');
  return (m && m.preview) || '';
}

export async function play(song, artist) {
  if (!song) return false;
  const a = el();
  const url = await resolveUrl(song, artist);
  if (!url) return false;
  if (currentId !== song.id || a.src !== url) { a.src = url; currentId = song.id; }
  try { a.currentTime = 0; await a.play(); return true; } catch (e) { return false; }
}

export function toggle(song, artist) {
  const a = el();
  if (currentId === song.id && !a.paused) { a.pause(); return; }
  play(song, artist);
}

export function stopAll() { if (audio) { try { audio.pause(); } catch (e) { /* ignore */ } } }
