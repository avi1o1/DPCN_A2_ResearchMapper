"""Fill the empty `orcid` column of an IIIT roster (IIIT team, PROCESS_IIIT.md §4.5).

Why: roster_channels.py's ORCID-works channel (B4) only runs for people whose roster row carries an ORCID. Roster agents
take ORCIDs only from institute pages (few IIIT pages print them) and had no ORCID API quota, so most rows are empty, while
the person's verified papers often carry a publisher-deposited ORCID (e.g. IIITDM Kancheepuram: 36 % of the golden set
missed, many of them by people whose ORCID is on their own verified papers).

An ORCID is accepted for a roster person only if:
  R1 deposited  it is deposited for an institute author (institute_author = true) whose name matches the person on >= 2
                affiliation-VERIFIED records of this institute, and no other ORCID is deposited for that name on such
                records (conflict -> blank)
  R2 registry   (only if R1 gives nothing) among all ORCID records that list this institute's ROR id as an affiliation
                (registry search ror-org-id; includes students), exactly one matches the person's name
Every decision goes to rosters/notes/<inst>_orcid_ids.tsv. Only empty `orcid` cells are written; visiting / adjunct
people are skipped (their ORCID works would bring in home-institution papers; roster_channels skips them anyway).
usage: python3 orcid_roster_ids.py <inst> [--dry]   (needs RM_OUT=v2, the first-pass v2/<inst>.json; ORCID token in .env)
"""
import sys, os, re, csv, json, collections, unicodedata
from common import get, ROOT, OUT
from institutes import REG

inst = sys.argv[1]; DRY = "--dry" in sys.argv
TITLES = re.compile(r"^(prof\.?|professor|dr\.?|mr\.?|ms\.?|mrs\.?|shri|smt\.?)\s+", re.I)


def asc(s):
    return unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode().lower()


def tokens(name):
    n = name.strip()
    while TITLES.match(n):
        n = TITLES.sub("", n)
    return [asc(t) for t in re.split(r"[\s.,]+", n) if t]


def matches(person_toks, author_name):
    """All full (>1 char) tokens of the roster name occur in the author name, and the author's initials are consistent."""
    a = tokens(author_name)
    full = [t for t in person_toks if len(t) > 1]
    if not full or not all(t in a for t in full):
        return False
    ini = {t[0] for t in person_toks}
    return all(t[0] in ini for t in a)


fn = os.path.join(ROOT, "rosters", f"{inst}_faculty.csv")
rows = list(csv.DictReader(open(fn, encoding="utf-8-sig")))
todo = [r for r in rows if not (r.get("orcid") or "").strip() and r.get("status") not in ("visiting", "adjunct")]
recs = [r for r in json.load(open(os.path.join(OUT, inst + ".json"), encoding="utf-8"))["records"]
        if r["affiliation_status"] == "verified" and isinstance(r["authors"], list)]
print(inst, "roster", len(rows), "to fill", len(todo), "verified records", len(recs), flush=True)
ror = (REG[inst]["ror"] or "").rsplit("/", 1)[-1]   # four IIITs have no ROR record (PROCESS_IIIT.md §7.1): R2 is skipped
# everyone whose ORCID record lists this institute (ROR) as an affiliation: faculty, but also students -> unique match only
ROR_PEOPLE, start = [], 0
while ror:
    d = get("https://pub.orcid.org/v3.0/expanded-search/", params={"q": f'ror-org-id:"https://ror.org/{ror}"', "rows": 1000,
            "start": start}, headers={"Accept": "application/json"}).json()
    page = d.get("expanded-result") or []
    ROR_PEOPLE += [(x["orcid-id"], f'{x.get("given-names") or ""} {x.get("family-names") or ""}') for x in page]
    start += len(page)
    if not page or start >= (d.get("num-found") or 0):
        break
print("ORCID records listing ROR", ror, len(ROR_PEOPLE), flush=True)

log, n_set = [], collections.Counter()
for p in todo:
    pt = tokens(p["name"])
    seen = collections.Counter()
    for r in recs:
        for a in r["authors"]:
            if a.get("institute_author") is True and a.get("orcid") and matches(pt, a["name"]):
                seen[a["orcid"][-19:]] += 1
    choice, route = None, None
    if len(seen) > 1:
        log.append([p["name"], ";".join(f"{o}x{c}" for o, c in seen.most_common()), "conflict", "several deposited ORCIDs", ""])
        continue
    if seen:
        o, c = seen.most_common(1)[0]
        if c >= 2:
            choice, route = o, f"R1 deposited on {c} verified records"
        else:
            log.append([p["name"], o, "not accepted", "deposited on only 1 verified record", c])
    if not choice and len([t for t in pt if len(t) > 1]) >= 1 and len(pt) >= 2:
        res = [o for o, nm in ROR_PEOPLE if matches(pt, nm)]
        if len(res) == 1:
            choice, route = res[0], "R2 registry (ORCID record lists this institute's ROR; unique name match)"
        elif res:
            log.append([p["name"], ";".join(res), "ambiguous", "registry: several iDs with this institute's ROR", ""])
            continue
    if choice:
        p["orcid"] = choice; n_set[route.split(" ")[0]] += 1
        log.append([p["name"], choice, "accepted", route, ""])

print("accepted", dict(n_set), "of", len(todo), flush=True)
with open(os.path.join(ROOT, "rosters", "notes", f"{inst}_orcid_ids.tsv"), "w", encoding="utf-8", newline="") as f:
    w = csv.writer(f, delimiter="\t", lineterminator="\n")
    w.writerow(["roster_name", "orcid", "decision", "route_or_reason", "n"]); w.writerows(log)
if not DRY:
    with open(fn, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n"); w.writeheader(); w.writerows(rows)
