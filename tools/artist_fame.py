"""Fetch a real popularity signal (Deezer fan count) for every roster artist.

The random-puzzle picker needs to favour artists players actually recognise.
Graph centrality alone can't do that: it measures "does lots of features", which
buries legacy/rock acts (Linkin Park, Ozzy Osbourne, The Notorious B.I.G.) and
over-rates regional collab hubs. Deezer's `nb_fan` is a real audience number, so
we fetch it once per artist and bake it into the dataset at build time.

Matching is deliberately strict: we only accept a Deezer artist whose normalized
name equals ours, so "Air"/"Cream"/"Woods"-style ambiguity fails closed
(match:"none") instead of importing a stranger's fan count. Among several exact
matches we keep the most-followed one, which is the well-known act.

Env: SHARD_INDEX, SHARD_TOTAL, FAME_OUT (dir), FAME_PRIOR (jsonl to resume from).
Writes JSONL: {id, name, dz_id, dz_name, fans, match}
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "data"))

from deezer_verify import norm_name, get, q, GAVE_UP  # noqa: E402
from source_data import ARTISTS  # noqa: E402

API = "https://api.deezer.com"
SHARD_INDEX = int(os.environ.get("SHARD_INDEX", "0"))
SHARD_TOTAL = int(os.environ.get("SHARD_TOTAL", "1"))
OUT_DIR = os.environ.get("FAME_OUT", "out")
PRIOR = os.environ.get("FAME_PRIOR", "")


# Roster names Deezer files under a different string. Without these, genuinely
# famous acts fall back to the graph-only score and drop out of random puzzles.
# A wrong guess here costs nothing: matching stays exact, so it just won't match.
ALIASES = {
    "The Black Eyed Peas": "Black Eyed Peas",
    "Bob Marley": "Bob Marley & The Wailers",
    "Carlos Santana": "Santana",
    "The Fugees": "Fugees",
    "Smashing Pumpkins": "The Smashing Pumpkins",
    "Goo Goo Dolls": "The Goo Goo Dolls",
    "Doobie Brothers": "The Doobie Brothers",
    "Isley Brothers": "The Isley Brothers",
    "The Four Tops": "Four Tops",
    "The Jackson 5": "Jackson 5",
    "The Grateful Dead": "Grateful Dead",
    "War on Drugs": "The War On Drugs",
    "Dixie Chicks": "The Chicks",
    "Noel Gallagher": "Noel Gallagher's High Flying Birds",
    "Machine Gun Kelly": "mgk",
    "Ty Dolla Sign": "Ty Dolla $ign",
    "ASAP Rocky": "A$AP Rocky",
    "ASAP Ferg": "A$AP Ferg",
    "Travi$ Scott": "Travis Scott",
    "Charlie XCX": "Charli XCX",
    "Puff Daddy": "Diddy",
    "Maître Gims": "GIMS",
    "Aurora Aksnes": "AURORA",
    "Emma Marrone": "Emma",
    "Lay Zhang": "LAY",
    "Enrique Bunbury": "Bunbury",
    "Cheb Khaled": "Khaled",
    "Years & Years": "Olly Alexander (Years & Years)",
    "Tinie Tempah": "Tinie Tempah",
    # Brazil
    "DJ Alok": "Alok",
    "Dennis DJ": "Dennis",
    "Safadão": "Wesley Safadão",
    "Bethânia": "Maria Bethânia",
    "MC Anitta": "Anitta",
    "Tom Jobim": "Antônio Carlos Jobim",
    "Paralamas do Sucesso": "Os Paralamas Do Sucesso",
    "Detonautas Roque Clube": "Detonautas",
    "Barões da Pisadinha": "Os Barões Da Pisadinha",
    "Fundo de Quintal": "Grupo Fundo De Quintal",
    "Jammil e Uma Cerveja": "Jammil e Uma Noites",
    "Grupo Molejo": "Molejo",
    "Felipe Ret": "Filipe Ret",
    "Murillo Huff": "Murilo Huff",
    "Banda MS": "Banda MS de Sergio Lizárraga",
    "Nicki Jam": "Nicky Jam",
    "Bieber": "Justin Bieber",
    # Non-Latin scripts
    "Zemfira": "Земфира",
    "Dima Bilan": "Дима Билан",
    "Egor Kreed": "Егор Крид",
    "Polina Gagarina": "Полина Гагарина",
    "Glukoza": "Глюкоза",
    "Ibrahim Tatlises": "İbrahim Tatlıses",
    "Kadim Al Saher": "كاظم الساهر",
    "Fayrouz": "فيروز",
}

# NFKD leaves "œ" and "$" alone, which breaks Cœur de Pirate / A$AP-style names.
EXTRA = str.maketrans({"œ": "oe", "Œ": "oe", "$": "s", "€": "e"})


def nkey(s):
    return norm_name((s or "").translate(EXTRA))


def candidates(name):
    """Our name plus safe spelling variants, all matched exactly."""
    base = ALIASES.get(name, name)
    out = [base, name]
    for art in ("the ", "os ", "as "):
        for n in (base, name):
            if n.lower().startswith(art):
                out.append(n[len(art):])
            else:
                out.append(art.title() + n)
    seen, uniq = set(), []
    for v in out:
        if v and v.lower() not in seen:
            seen.add(v.lower())
            uniq.append(v)
    return uniq


def lookup(name):
    """-> (dz_id, dz_name, fans, match) ; match in exact|none|error."""
    wanted = {nkey(v) for v in candidates(name)}
    query = ALIASES.get(name, name)
    d = get(f"{API}/search/artist?q={q(query)}&limit=10")
    if d is GAVE_UP:
        return None, None, None, "error"
    if not d or not d.get("data"):
        return None, None, None, "none"
    exact = [a for a in d["data"] if nkey(a.get("name")) in wanted]
    if not exact:
        return None, None, None, "none"
    best = max(exact, key=lambda a: a.get("nb_fan") or 0)
    return best.get("id"), best.get("name"), best.get("nb_fan") or 0, "exact"


def main():
    done = set()
    if PRIOR and os.path.exists(PRIOR):
        with open(PRIOR, encoding="utf-8") as fh:
            for line in fh:
                try:
                    r = json.loads(line)
                except Exception:
                    continue
                # Only a real fan count is settled. Unmatched names are retried
                # on every run, so improving ALIASES rescues them without
                # re-querying the 5,000+ artists already resolved.
                if r.get("match") == "exact":
                    done.add(r["id"])

    mine = [(i, n) for (i, n, _g) in ARTISTS
            if i % SHARD_TOTAL == SHARD_INDEX and i not in done]
    os.makedirs(OUT_DIR, exist_ok=True)
    path = os.path.join(OUT_DIR, "artist_fame.jsonl")
    written = errors = 0
    with open(path, "w", encoding="utf-8") as out:
        for k, (aid, name) in enumerate(mine):
            dz_id, dz_name, fans, match = lookup(name)
            if match == "error":
                errors += 1
                continue
            out.write(json.dumps({"id": aid, "name": name, "dz_id": dz_id,
                                  "dz_name": dz_name, "fans": fans,
                                  "match": match}, ensure_ascii=False) + "\n")
            out.flush()
            written += 1
            if k % 25 == 0:
                print(f"[{SHARD_INDEX}] {k}/{len(mine)} written={written}", flush=True)
    print(f"SHARD DONE written={written} errors={errors}", flush=True)


if __name__ == "__main__":
    main()
