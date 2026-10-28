"""Fill the empty `dblp` column of an IIIT roster (IIIT team, PROCESS_IIIT.md §4.2).

Why: roster_channels.py's DBLP channel (B5) only runs for roster people with a DBLP pid, and the roster brief accepts only
identifiers printed on institute pages, which IIITs rarely show (0-1 pids per roster). For CS-heavy institutes DBLP is the
main person channel for conference papers without DOI/affiliation metadata (HANDOFF_IIITs §6).

A DBLP person (public SPARQL endpoint; the website is bot-walled) is accepted for a roster person only if its name is one of
the person's name variants AND one of:
  R1 orcid     the DBLP person carries the roster person's ORCID
  R2 aff       a DBLP affiliation string of the person classifies as this institute (affil.classify)
  R3 verified  >= 2 of its DOIs are affiliation-VERIFIED records of this institute in which an institute author
               (institute_author = true) carries the person's distinctive name token, AND these are >= 5 % of the DBLP
               person's DOIs (common names: a prolific namesake profile can contain a few of our papers; first run
               accepted "Sunil Kumar" with 3 of 277, "Amit Kumar" 3 of 241 - rejected by this rule). The 5 % guard applies only
               when the matched name is shared by several DBLP persons: a unique name with a long career elsewhere (Mayank
               Vatsa, 3 of 441) is not a namesake profile, unless other DBLP names extend it ("Sushant Kumar Jha"): then the
               single exact holder is DBLP's undisambiguated catch-all profile and the guard applies
A DBLP person with a different ORCID is never accepted. If several DBLP persons qualify, the best one is taken only if it
beats the runner-up by 2x on R3 overlaps; otherwise the person is left blank (ambiguous). Every decision goes to
rosters/notes/<inst>_dblp_ids.tsv. Only empty `dblp` cells are written.
usage: python3 dblp_roster_ids.py <inst> [--dry]       (needs RM_OUT=v2 and the institute's first-pass v2/<inst>.json)
"""
import sys, os, re, csv, io, json, collections, unicodedata
from common import get, ROOT, OUT, norm_doi
from affil import classify

inst = sys.argv[1]; DRY = "--dry" in sys.argv
EP = "https://sparql.dblp.org/sparql"
PFX = "PREFIX dblp: <https://dblp.org/rdf/schema#>\n"
TITLES = re.compile(r"^(prof\.?|professor|dr\.?|mr\.?|ms\.?|mrs\.?|shri|smt\.?)\s+", re.I)


def sparql(q):
    return list(csv.DictReader(io.StringIO(get(EP, params={"query": PFX + q}, headers={"Accept": "text/csv"}, timeout=300).text)))


def asc(s):
    return unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode().lower()


def tokens(name):
    n = name.strip()
    while TITLES.match(n):
        n = TITLES.sub("", n)
    return [t for t in re.split(r"[\s.]+", n) if t]


def variants(name):
    """Name forms DBLP may use. Handles the Tamil/Telugu patronymic-initial forms ('Sadagopan N', 'S. Kalpana') by putting
    the initials first, as publications print them ('N. Sadagopan')."""
    t = tokens(name)
    if not t:
        return set()
    full = [x for x in t if len(x) > 1]
    ini = [x for x in t if len(x) == 1]
    out = set()
    if ini and full:   # initials + given name(s): "N. Sadagopan", "N Sadagopan", "Sadagopan N"
        i_dot, i_sp = " ".join(x.upper() + "." for x in ini), " ".join(x.upper() for x in ini)
        f = " ".join(x.capitalize() if x.islower() or x.isupper() else x for x in full)
        out |= {f"{i_dot} {f}", f"{i_sp} {f}", f"{f} {i_sp}", f"{f} {i_dot}"}
        # middle-initial names ("Binsu J Kailath"): keep the order, dot the initial
        out.add(" ".join((x.upper() + ".") if len(x) == 1 else x for x in t))
    else:
        out.add(" ".join(t))
        if len(t) >= 3:   # drop middle names: "Kumar Prasannajit Pradhan" -> also "Prasannajit Pradhan"? no: first+last only
            out.add(f"{t[0]} {t[-1]}")
    return {re.sub(r"\s+", " ", v).strip() for v in out}


def key_token(name):
    """The person's longest name token: the one that appears in the author string on a paper."""
    t = [asc(x) for x in tokens(name) if len(x) > 1]
    return max(t, key=len) if t else ""


fn = os.path.join(ROOT, "rosters", f"{inst}_faculty.csv")
rows = list(csv.DictReader(open(fn, encoding="utf-8-sig")))
todo = [r for r in rows if not (r.get("dblp") or "").strip()]
# verified DOIs of this institute -> institute-author names on that record
VER = collections.defaultdict(list)
for r in json.load(open(os.path.join(OUT, inst + ".json"), encoding="utf-8"))["records"]:
    if r["affiliation_status"] == "verified" and isinstance(r["authors"], list) and r["doi"] != "TODO":
        VER[norm_doi(r["doi"])] = [asc(a["name"]) for a in r["authors"] if a.get("institute_author") is True]
print(inst, "roster", len(rows), "without dblp", len(todo), "verified DOIs", len(VER), flush=True)

# 1. candidate DBLP persons by exact name variant
V = {}
for r in todo:
    for v in variants(r["name"]):
        V.setdefault(v, []).append(r["name"])
cand = collections.defaultdict(lambda: {"names": set(), "orcid": set(), "aff": set()})
vl = sorted(V)
for i in range(0, len(vl), 60):
    vals = " ".join(json.dumps(v) for v in vl[i:i + 60])
    for x in sparql(f"SELECT ?p ?n ?o ?aff WHERE {{ VALUES ?n {{ {vals} }} ?p dblp:creatorName ?n . "
                    f"OPTIONAL {{ ?p dblp:orcid ?o }} OPTIONAL {{ ?p dblp:affiliation ?aff }} }}"):
        c = cand[x["p"]]; c["names"].add(x["n"])
        if x["o"]: c["orcid"].add(x["o"].rsplit("/", 1)[-1])
        if x["aff"]: c["aff"].add(x["aff"])
print("candidate DBLP persons", len(cand), flush=True)
HOLDERS = collections.defaultdict(set)   # name -> DBLP persons carrying it (homonyms)
for p, c in cand.items():
    for n in c["names"]:
        HOLDERS[n].add(p)
_EXT = {}


def extended(n):
    """DBLP persons whose name extends this one ("Sushant Kumar Jha" for "Sushant Kumar"): a common name whose only exact
    holder is DBLP's undisambiguated catch-all profile (precision audit 2026-10-29: pid 166/1095, 120 papers of several
    people, 4 ours)."""
    if n not in _EXT:
        _EXT[n] = len(sparql(f"SELECT DISTINCT ?p WHERE {{ ?p dblp:creatorName ?m . FILTER(STRSTARTS(?m, {json.dumps(n + ' ')})) }} LIMIT 1"))
    return _EXT[n]
# 2. their DOIs
DOIS = collections.defaultdict(set)
pl = sorted(cand)
for i in range(0, len(pl), 40):
    vals = " ".join(f"<{p}>" for p in pl[i:i + 40])
    for x in sparql(f"SELECT ?p ?doi WHERE {{ VALUES ?p {{ {vals} }} ?pub dblp:authoredBy ?p ; dblp:doi ?doi }}"):
        d = norm_doi(x["doi"])
        if d:
            DOIS[x["p"]].add(d)

# 3. decide
log, n_set = [], collections.Counter()
for r in todo:
    vs = variants(r["name"]); kt = key_token(r["name"]); my_orcid = (r.get("orcid") or "").strip()
    scored = []
    for p, c in cand.items():
        if not (c["names"] & vs):
            continue
        if my_orcid and c["orcid"] and my_orcid not in c["orcid"]:
            log.append([r["name"], p, "rejected", "different ORCID " + ",".join(sorted(c["orcid"])), 0]); continue
        r1 = bool(my_orcid and my_orcid in c["orcid"])
        r2 = any(classify(inst, a) == "iit" for a in c["aff"])
        r3 = sum(1 for d in DOIS[p] if d in VER and any(kt and kt in n for n in VER[d]))
        if r3 and r3 < 0.05 * len(DOIS[p]) and any(len(HOLDERS[n]) > 1 or extended(n) for n in c["names"] & vs):
            log.append([r["name"], p, "rejected", f"overlap {r3} < 5% of {len(DOIS[p])} DBLP DOIs (namesake profile?)", r3])
            r3 = 0
        scored.append((p, r1, r2, r3))
    acc = [s for s in scored if s[1] or s[2] or s[3] >= 2]
    if not acc:
        if scored:
            log.append([r["name"], ";".join(s[0] for s in scored), "not accepted", "no route", max(s[3] for s in scored)])
        continue
    acc.sort(key=lambda s: (s[1], s[2], s[3]), reverse=True)
    best = acc[0]
    if len(acc) > 1 and not (best[1] and not acc[1][1]) and not (best[2] and not acc[1][2]) and best[3] < 2 * max(1, acc[1][3]):
        log.append([r["name"], ";".join(s[0] for s in acc), "ambiguous", "several qualifying DBLP persons", best[3]]); continue
    route = "R1 orcid" if best[1] else "R2 aff" if best[2] else "R3 verified"
    n_set[route] += 1
    log.append([r["name"], best[0], "accepted", route, best[3]])
    r["dblp"] = best[0]

print("accepted", dict(n_set), "of", len(todo), flush=True)
with open(os.path.join(ROOT, "rosters", "notes", f"{inst}_dblp_ids.tsv"), "w", encoding="utf-8", newline="") as f:
    w = csv.writer(f, delimiter="\t", lineterminator="\n")
    w.writerow(["roster_name", "dblp_person", "decision", "route_or_reason", "verified_doi_overlap"]); w.writerows(log)
if not DRY:
    with open(fn, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n"); w.writeheader(); w.writerows(rows)
