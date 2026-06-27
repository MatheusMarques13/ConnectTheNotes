"""Extract artists+collaborations from frontend/src/data/mockData.js,
keep only the largest connected component, and emit backend/seed_data.py."""
import re
from collections import defaultdict, deque

SRC = '/home/user/ConnectTheNotes/frontend/src/data/mockData.js'
OUT = '/home/user/ConnectTheNotes/backend/seed_data.py'

src = open(SRC, encoding='utf-8').read()

# --- Parse ARTISTS ---
art_block = re.search(r'const ARTISTS = \[(.*?)\n\];', src, re.S).group(1)
artists = {}
for m in re.finditer(r'\{\s*id:\s*(\d+),\s*name:\s*"([^"]+)",\s*genre:\s*"([^"]+)"', art_block):
    aid, name, genre = int(m.group(1)), m.group(2), m.group(3)
    artists[aid] = {'id': aid, 'name': name, 'genre': genre}

# --- Parse COLLABORATIONS ---
col_block = re.search(r'const COLLABORATIONS = \[(.*?)\n\];', src, re.S).group(1)
collabs = []
for m in re.finditer(
        r'artistIds:\s*\[(\d+),\s*(\d+)\],\s*title:\s*"([^"]+)",\s*type:\s*"([^"]+)",\s*year:\s*(\d+)',
        col_block):
    a1, a2 = int(m.group(1)), int(m.group(2))
    collabs.append((a1, a2, m.group(3), m.group(4), int(m.group(5))))

# --- Build graph & find largest connected component ---
adj = defaultdict(set)
for a1, a2, *_ in collabs:
    if a1 in artists and a2 in artists and a1 != a2:
        adj[a1].add(a2); adj[a2].add(a1)

seen, components = set(), []
for a in artists:
    if a in seen:
        continue
    comp, q = [], deque([a]); seen.add(a)
    while q:
        x = q.popleft(); comp.append(x)
        for y in adj[x]:
            if y not in seen:
                seen.add(y); q.append(y)
    components.append(comp)
components.sort(key=len, reverse=True)
giant = set(components[0])

dropped = [artists[a]['name'] for a in artists if a not in giant]

# Keep only artists in the giant component, and edges fully inside it
kept_artists = [artists[a] for a in sorted(giant)]
kept_collabs = [c for c in collabs if c[0] in giant and c[1] in giant]

# --- Verify the kept graph is a single component & every pair solvable ---
adj2 = defaultdict(set)
for a1, a2, *_ in kept_collabs:
    adj2[a1].add(a2); adj2[a2].add(a1)
ids = [a['id'] for a in kept_artists]
start = ids[0]
vis = {start}; q = deque([start])
while q:
    x = q.popleft()
    for y in adj2[x]:
        if y not in vis:
            vis.add(y); q.append(y)
assert len(vis) == len(ids), f"Kept graph NOT fully connected: {len(vis)}/{len(ids)}"

# Path-length distribution for a quick gameplay sanity check
dist_counts = defaultdict(int)
for s in ids:
    d = {s: 0}; q = deque([s])
    while q:
        x = q.popleft()
        for y in adj2[x]:
            if y not in d:
                d[y] = d[x] + 1; q.append(y)
    for t in ids:
        if t > s:
            dist_counts[d[t]] += 1

# --- Emit backend/seed_data.py ---
lines = []
lines.append('"""Canonical dataset for Connect the Notes (auto-generated from the')
lines.append('original mockData.js, filtered to the largest connected component so that')
lines.append('EVERY artist pair is solvable). Do not edit by hand — regenerate via')
lines.append('scripts/gen_seed_data.py if the source data changes.')
lines.append('')
lines.append(f'Artists: {len(kept_artists)}   Collaborations: {len(kept_collabs)}   Single connected component (100% solvable).')
lines.append('"""')
lines.append('')
lines.append('# (id, name, genre)')
lines.append('ARTISTS = [')
for a in kept_artists:
    lines.append(f'    ({a["id"]}, {a["name"]!r}, {a["genre"]!r}),')
lines.append(']')
lines.append('')
lines.append('# (artist1_id, artist2_id, song_title, type, year)')
lines.append('COLLABORATIONS = [')
for c in kept_collabs:
    lines.append(f'    ({c[0]}, {c[1]}, {c[2]!r}, {c[3]!r}, {c[4]}),')
lines.append(']')
lines.append('')

open(OUT, 'w', encoding='utf-8').write('\n'.join(lines))

print(f"Source: {len(artists)} artists, {len(collabs)} collab rows")
print(f"Components: {len(components)} (sizes: {[len(c) for c in components]})")
print(f"Dropped (not in giant component): {dropped}")
print(f"KEPT: {len(kept_artists)} artists, {len(kept_collabs)} collaborations")
print(f"Unique undirected edges: {sum(len(v) for v in adj2.values())//2}")
print(f"Single component verified: {len(vis)}/{len(ids)} reachable from {kept_artists[0]['name']}")
print("Path-length distribution (steps between artists):")
total = sum(dist_counts.values())
for k in sorted(dist_counts):
    print(f"  {k} step(s): {dist_counts[k]} pairs ({100*dist_counts[k]/total:.0f}%)")
print(f"Total solvable pairs: {total} (100% of {len(ids)*(len(ids)-1)//2})")
print(f"\nWrote {OUT}")
