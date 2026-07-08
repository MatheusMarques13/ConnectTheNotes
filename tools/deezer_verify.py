"""Deterministic Deezer-catalog verification of every collaboration edge.

For each unique song (title,type,year) in data/source_data.py, queries the
public Deezer API and collects the set of credited artist names for the best
matching track/album (main artist + contributors + names parsed from
"feat."-style title suffixes). Every edge (A,B) on that song then gets:
  BOTH   - both artists found among the credited names   -> catalog-verified
  ONE    - track found, but only one of the two credited -> suspicious
  NONE   - no matching track/album found on Deezer       -> unknown (not proof of fake)

Fully resumable: every song verdict is appended to songs_done.jsonl and skipped
on rerun. Rate-limited to ~8 req/s (Deezer allows 50/5s). Run from repo root:
  python3 deezer_verify.py
"""
import sys, os, re, json, time, unicodedata, urllib.request, urllib.parse

sys.path.insert(0, "data")
import source_data as sd

OUT_DIR = os.environ.get("DEEZER_OUT") or os.path.dirname(os.path.abspath(__file__))
os.makedirs(OUT_DIR, exist_ok=True)
DONE = os.path.join(OUT_DIR, "songs_done.jsonl")
API = "https://api.deezer.com"

# ── name/title normalization ────────────────────────────────────────────────
def strip_accents(s):
    s = unicodedata.normalize("NFKD", s or "")
    return "".join(c for c in s if not unicodedata.combining(c))

def norm_name(s):
    s = strip_accents(s).lower()
    s = re.sub(r"[&+]| e | y | and ", " ", " " + s + " ")
    s = re.sub(r"[^a-z0-9]+", "", s)
    return s

PAREN_DROP = re.compile(
    r"\s*[\(\[](feat\.?|featuring|with|com|part\.?|participa|ao vivo|live|bonus|deluxe|version|versao|radio edit)[^\)\]]*[\)\]]",
    re.I)

def base_title(t):
    t = strip_accents(t or "").lower()
    t = PAREN_DROP.sub("", t)
    t = re.sub(r"\s*-\s*(ao vivo|live|remix|radio edit).*$", "", t)
    t = re.sub(r"[^a-z0-9]+", " ", t).strip()
    return t

def feat_names(t):
    """Artist names hidden in the raw title: 'Work (feat. Drake)' -> ['drake']"""
    out = []
    for m in re.finditer(r"[\(\[\-]\s*(?:feat\.?|featuring|with|com|part\.?)\s+([^\)\]\-]+)", t or "", re.I):
        chunk = m.group(1)
        for nm in re.split(r",|&| e | y | and |feat\.?|featuring", chunk, flags=re.I):
            nm = nm.strip()
            if nm:
                out.append(norm_name(nm))
    return out

# ── rate-limited GET with retry ─────────────────────────────────────────────
_last = [0.0]
def get(url, tries=4):
    for k in range(tries):
        wait = 0.125 - (time.time() - _last[0])   # ~8 req/s
        if wait > 0:
            time.sleep(wait)
        _last[0] = time.time()
        try:
            with urllib.request.urlopen(urllib.request.Request(
                    url, headers={"User-Agent": "ConnectTheNotes-verify/1.0"}), timeout=20) as r:
                d = json.loads(r.read().decode("utf-8"))
            if isinstance(d, dict) and d.get("error"):
                code = d["error"].get("code")
                if code == 4:            # quota exceeded — back off hard
                    time.sleep(5 + 5 * k)
                    continue
                return None              # other API error: treat as no result
            return d
        except Exception:
            time.sleep(1 + 2 * k)
    return None

def q(s):
    return urllib.parse.quote((s or "").replace('"', ""))

# ── credited-name harvesting ────────────────────────────────────────────────
def track_credits(tr):
    names = set()
    a = (tr.get("artist") or {}).get("name")
    if a:
        names.add(norm_name(a))
    for nm in feat_names(tr.get("title") or ""):
        names.add(nm)
    return names

def full_track_credits(tid):
    d = get(f"{API}/track/{tid}")
    names = set()
    if d:
        for c in d.get("contributors") or []:
            names.add(norm_name(c.get("name", "")))
        a = (d.get("artist") or {}).get("name")
        if a:
            names.add(norm_name(a))
        for nm in feat_names(d.get("title") or ""):
            names.add(nm)
    return names

def candidates_for(title, artist, is_album):
    kind = "album" if is_album else "track"
    d = get(f'{API}/search/{kind}?q={kind}:"{q(title)}" artist:"{q(artist)}"&limit=25')
    res = (d or {}).get("data") or []
    if not res:
        d = get(f"{API}/search/{kind}?q={q(title + ' ' + artist)}&limit=25")
        res = (d or {}).get("data") or []
    return res

def title_matches(ours, theirs):
    a, b = base_title(ours), base_title(theirs)
    if not a or not b:
        return False
    if a == b:
        return True
    return (a in b or b in a) and abs(len(a) - len(b)) <= 15

def verify_song(title, ctype, names_by_id, edge_ids):
    """Returns (credited_names:set, deezer_link or None)."""
    is_album = ctype in ("album", "ep", "mixtape")
    # try search anchored on up to 3 distinct artists of this song
    seen_anchor = []
    for aid in edge_ids:
        nm = names_by_id[aid]
        if nm in seen_anchor:
            continue
        seen_anchor.append(nm)
        if len(seen_anchor) > 3:
            break
        variants = [title]
        if ctype in ("live", "dvd") and "ao vivo" not in title.lower():
            variants.append(title + " (Ao Vivo)")
        for tv in variants:
            for cand in candidates_for(tv, nm, is_album):
                if not title_matches(title, cand.get("title", "")):
                    continue
                credited = track_credits(cand)
                if is_album:
                    d = get(f"{API}/album/{cand['id']}")
                    for c in (d or {}).get("contributors") or []:
                        credited.add(norm_name(c.get("name", "")))
                else:
                    credited |= full_track_credits(cand["id"])
                link = cand.get("link") or f"https://www.deezer.com/{'album' if is_album else 'track'}/{cand['id']}"
                return credited, link
    return set(), None

def main():
    byid = {i: n for i, n, g in sd.ARTISTS}
    # group edges by song key (same normalization as build.py)
    def songkey(t): return re.sub(r"\s+", " ", (t or "").strip()).lower()
    groups = {}
    for idx, (a, b, t, ty, y) in enumerate(sd.COLLABORATIONS):
        groups.setdefault((songkey(t), ty, y), {"title": t, "type": ty, "year": y,
                                                "edges": []})["edges"].append((idx, a, b))
    done = set()
    if os.path.exists(DONE):
        with open(DONE) as fh:
            for line in fh:
                try:
                    done.add(tuple(json.loads(line)["key"]))
                except Exception:
                    pass
    todo = [(k, v) for k, v in groups.items() if k not in done]
    print(f"songs total={len(groups)} done={len(done)} todo={len(todo)}", flush=True)
    out = open(DONE, "a", buffering=1)
    t0 = time.time()
    for n, (key, g) in enumerate(todo):
        ids = []
        for _, a, b in g["edges"]:
            for x in (a, b):
                if x not in ids:
                    ids.append(x)
        credited, link = verify_song(g["title"], g["type"], byid, ids)
        edges = []
        for idx, a, b in g["edges"]:
            if credited:
                na, nb = norm_name(byid[a]), norm_name(byid[b])
                hit_a = any(na == c or (len(na) > 4 and na in c) or (len(c) > 4 and c in na) for c in credited)
                hit_b = any(nb == c or (len(nb) > 4 and nb in c) or (len(c) > 4 and c in nb) for c in credited)
                v = "BOTH" if (hit_a and hit_b) else "ONE" if (hit_a or hit_b) else "NONE_CREDITED"
            else:
                v = "NOT_FOUND"
            edges.append({"i": idx, "a": byid[a], "b": byid[b], "v": v})
        out.write(json.dumps({"key": list(key), "title": g["title"], "type": g["type"],
                              "year": g["year"], "link": link,
                              "credited": sorted(credited), "edges": edges},
                             ensure_ascii=False) + "\n")
        if (n + 1) % 200 == 0:
            rate = (n + 1) / (time.time() - t0)
            print(f"{n+1}/{len(todo)} songs  ({rate:.1f}/s, eta {int((len(todo)-n-1)/rate/60)}min)", flush=True)
    print("DONE", flush=True)

if __name__ == "__main__":
    main()
