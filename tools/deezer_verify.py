"""Deterministic Deezer-catalog verification of every collaboration edge (v2).

For each unique song (title,type,year) in data/source_data.py, queries the
public Deezer API and collects the set of credited artist names for the best
matching track/album (main artist + contributors + names parsed from
"feat."-style title suffixes). Every edge (A,B) on that song then gets:
  BOTH          - both artists credited on the found recording -> catalog-verified
  ONE           - recording found, only one of the two credited -> suspicious
  NONE_CREDITED - recording found, neither credited              -> suspicious
  NOT_FOUND     - no matching recording (all searches completed) -> unknown

v2 changes:
- Sharding: SHARD_INDEX/SHARD_TOTAL env vars split songs by stable hash, so
  N CI runners (distinct IPs -> distinct Deezer quotas) work in parallel.
- Adaptive pacing: starts polite, backs off hard on quota errors, speeds up
  again after sustained success. Quota failures are retried patiently; if a
  song still can't complete, it is SKIPPED (not written) so a rerun retries
  it - a throttled run can never pollute results with fake NOT_FOUNDs.
- Fewer requests: max 2 search anchors + 1 plain fallback per song, and the
  per-track credits fetch is skipped when search-level credits already cover
  every edge artist.
- Resume: rows already in the prior results with a non-null link are kept;
  null-link rows from v1 (possibly quota-polluted) are requeued.

Run: DEEZER_OUT=dir [SHARD_INDEX=k SHARD_TOTAL=n] python3 tools/deezer_verify.py
"""
import sys, os, re, json, time, hashlib, unicodedata, urllib.request, urllib.parse

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data"))
import source_data as sd

OUT_DIR = os.environ.get("DEEZER_OUT") or os.path.dirname(os.path.abspath(__file__))
os.makedirs(OUT_DIR, exist_ok=True)
DONE = os.path.join(OUT_DIR, "songs_done.jsonl")
PRIOR = os.environ.get("DEEZER_PRIOR", DONE)   # combined prior results (read-only)
SHARD_INDEX = int(os.environ.get("SHARD_INDEX", "0"))
SHARD_TOTAL = int(os.environ.get("SHARD_TOTAL", "1"))
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
    out = []
    for m in re.finditer(r"[\(\[\-]\s*(?:feat\.?|featuring|with|com|part\.?)\s+([^\)\]\-]+)", t or "", re.I):
        for nm in re.split(r",|&| e | y | and |feat\.?|featuring", m.group(1), flags=re.I):
            nm = nm.strip()
            if nm:
                out.append(norm_name(nm))
    return out

# ── adaptive-paced GET ──────────────────────────────────────────────────────
class Pacer:
    def __init__(self):
        self.interval = 0.6          # start polite
        self.last = 0.0
        self.streak = 0
    def wait(self):
        d = self.interval - (time.time() - self.last)
        if d > 0:
            time.sleep(d)
        self.last = time.time()
    def ok(self):
        self.streak += 1
        if self.streak >= 25:
            self.streak = 0
            self.interval = max(0.25, self.interval * 0.85)
    def throttled(self):
        self.streak = 0
        self.interval = min(20.0, self.interval * 1.6)

PACER = Pacer()
GAVE_UP = object()

def get(url):
    """Returns parsed JSON, None on non-quota API error, GAVE_UP if quota
    could not be cleared after many patient retries."""
    for k in range(12):
        PACER.wait()
        try:
            with urllib.request.urlopen(urllib.request.Request(
                    url, headers={"User-Agent": "ConnectTheNotes-verify/2.0"}), timeout=20) as r:
                d = json.loads(r.read().decode("utf-8"))
        except Exception:
            PACER.throttled()
            time.sleep(min(30, 2 ** k))
            continue
        if isinstance(d, dict) and d.get("error"):
            if d["error"].get("code") == 4:      # quota
                PACER.throttled()
                time.sleep(min(60, 3 * (k + 1)))
                continue
            return None
        PACER.ok()
        return d
    return GAVE_UP

def q(s):
    return urllib.parse.quote((s or "").replace('"', ""))

# ── matching ────────────────────────────────────────────────────────────────
def title_matches(ours, theirs):
    a, b = base_title(ours), base_title(theirs)
    if not a or not b:
        return False
    if a == b:
        return True
    return (a in b or b in a) and abs(len(a) - len(b)) <= 15

def search_credits(item):
    names = set()
    a = (item.get("artist") or {}).get("name")
    if a:
        names.add(norm_name(a))
    for nm in feat_names(item.get("title") or ""):
        names.add(nm)
    return names

def verify_song(title, ctype, anchors, needed):
    """anchors: artist display names to search with. needed: set of normalized
    edge-artist names. Returns (credited:set, link, complete:bool)."""
    is_album = ctype in ("album", "ep", "mixtape")
    kind = "album" if is_album else "track"
    gave_up = False
    variants = [title]
    if ctype in ("live", "dvd") and "ao vivo" not in title.lower():
        variants.append(title + " (Ao Vivo)")

    searches = []
    for nm in anchors[:2]:
        for tv in variants:
            searches.append(f'{API}/search/{kind}?q={kind}:"{q(tv)}" artist:"{q(nm)}"&limit=25')
    if anchors:
        searches.append(f"{API}/search/{kind}?q={q(title + ' ' + anchors[0])}&limit=25")

    for url in searches:
        d = get(url)
        if d is GAVE_UP:
            gave_up = True
            continue
        for cand in (d or {}).get("data") or []:
            if not title_matches(title, cand.get("title", "")):
                continue
            credited = search_credits(cand)
            link = cand.get("link") or f"https://www.deezer.com/{kind}/{cand['id']}"
            if needed <= credited:
                return credited, link, True       # search-level credits suffice
            det = get(f"{API}/{kind}/{cand['id']}")
            if det is GAVE_UP:
                return credited, link, False      # found it but credits incomplete
            if det:
                for c in det.get("contributors") or []:
                    credited.add(norm_name(c.get("name", "")))
                aa = (det.get("artist") or {}).get("name")
                if aa:
                    credited.add(norm_name(aa))
                for nm in feat_names(det.get("title") or ""):
                    credited.add(nm)
            return credited, link, True
    return set(), None, not gave_up

def main():
    byid = {i: n for i, n, g in sd.ARTISTS}
    def songkey(t): return re.sub(r"\s+", " ", (t or "").strip()).lower()
    groups = {}
    for idx, (a, b, t, ty, y) in enumerate(sd.COLLABORATIONS):
        groups.setdefault((songkey(t), ty, y), {"title": t, "type": ty, "year": y,
                                                "edges": []})["edges"].append((idx, a, b))
    def shard_of(key):
        h = hashlib.md5(json.dumps(list(key), ensure_ascii=False).encode()).hexdigest()
        return int(h[:8], 16) % SHARD_TOTAL

    done = set()
    if os.path.exists(PRIOR):
        with open(PRIOR) as fh:
            for line in fh:
                try:
                    r = json.loads(line)
                    if r.get("link"):              # requeue null-link rows
                        done.add(tuple(r["key"]))
                except Exception:
                    pass
    todo = [(k, v) for k, v in groups.items()
            if k not in done and shard_of(k) == SHARD_INDEX]
    print(f"shard {SHARD_INDEX}/{SHARD_TOTAL}: songs total={len(groups)} "
          f"prior-done={len(done)} todo(this shard)={len(todo)}", flush=True)

    out = open(DONE, "a", buffering=1)
    t0 = time.time()
    written = skipped = 0
    for n, (key, g) in enumerate(todo):
        ids, anchors = [], []
        for _, a, b in g["edges"]:
            for x in (a, b):
                if x not in ids:
                    ids.append(x)
                    anchors.append(byid[x])
        needed = {norm_name(byid[x]) for x in ids}
        credited, link, complete = verify_song(g["title"], g["type"], anchors, needed)
        if not link and not complete:
            skipped += 1                            # quota-ambiguous: retry next run
            continue
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
                              "year": g["year"], "link": link, "complete": complete,
                              "credited": sorted(credited), "edges": edges},
                             ensure_ascii=False) + "\n")
        written += 1
        if (n + 1) % 100 == 0:
            rate = (n + 1) / (time.time() - t0)
            print(f"{n+1}/{len(todo)}  ({rate:.2f} songs/s, interval {PACER.interval:.2f}s, "
                  f"written {written}, skipped {skipped}, eta {int((len(todo)-n-1)/max(rate,0.01)/60)}min)", flush=True)
    print(f"SHARD DONE written={written} skipped={skipped}", flush=True)

if __name__ == "__main__":
    main()
