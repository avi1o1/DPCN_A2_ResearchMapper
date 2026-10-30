"""Sanity-check rules F1, F2(b), F3 and F5 (2026-10-30 sanity audit; PROCESS.md section 15.17).  Pure functions and one small class, no
network access, used by finalize.py (applied at every `run_v2.sh refresh`, no roster pass needed) and by roster_channels.py (applied
to new roster passes).  Tested by test_sanity_rules.py.

F1  start-year rule for person-channel ("likely") records.  A record found only through roster people is kept when at least one of
    the linked people was already there: year >= max(founded, start - lag), start = roster joining_year, else - for people who
    are no longer current - the first year of the '(YYYY-YYYY)' range in the designation.  lag = 1 year (a paper is often written
    before the person's listed joining date), 0 for institutes founded 2015 or later (the whole institute did not exist yet).
    The check passes whenever one linked person passes or cannot be tested (no roster row = ORCID-profile person with dated
    tenure; no start year); it fails only when EVERY linked person is a roster person with a start year after the record year.
    The bound uses `founded`, never `became_iit`: an "Indian School of Mines" paper of 2016 is a paper of IIT (ISM) Dhanbad.
F2b Records that passed only because every linked roster person has no start year are labelled `likely-untimed` (the part F1 cannot
    test); the rest `likely-timed` (a linked person's start year was tested and is not after the paper) or `likely-nonroster`
    (linked only to ORCID-profile people who are not in the roster; their ORCID tenure dates were used by build_candidates.py).
F3  `mega_collab`: more than 100 authors (Crossref author list; channel author list as fallback; the Enrichment stage falls back to the
    OpenAlex list, which is capped at 100).
F5  namesake guard.  A person whose family name or first given name is a very common name (Kumar, Singh, Verma, ...: the list is
    built from the data) is credited with a paper only by ORCID identity (ORCID profile / roster ORCID works, or a roster DBLP pid),
    a printed affiliation, or >= 2 shared affiliation-verified co-authors.  The one-co-author-plus-venue acceptance of the plain
    roster rule is not enough for such names."""
import os, re, csv, glob, math, unicodedata, collections

from institutes import REG

MEGA_LIMIT = 100                 # more than this many authors = mega-collaboration
YEAR_MIN_WINDOW = 2016

# very common Indian names seeded by hand; the data-built list below extends it (pooled roster frequency)
GENERIC_SEED = frozenset("""kumar singh verma sharma gupta das ghosh mishra roy prasad chandra krishna prakash rao sarkar mukherjee
banerjee chakraborty dutta srivastava bhattacharya jain mandal yadav pal pandey reddy sinha nath chatterjee saha jha biswas
sahoo mondal tiwari shankar ram raj""".split())
GENERIC_SHARE = 0.005            # a name token carried by >= 0.5 % of the pooled roster people (or >= 8 people) is generic
GENERIC_MIN = 8

TITLES = {"dr", "prof", "professor", "mr", "mrs", "ms", "shri", "smt", "sri"}
RANGE_RX = re.compile(r"\((\d{4})\s*-\s*(\d{4})\)")
ORCID_RX = re.compile(r"\d{4}-\d{4}-\d{4}-\d{3}[\dX]")
# evidence that identifies the person by an identifier (ORCID iD / DBLP pid) rather than by name matching
IDENTITY_EVIDENCE = {"roster_orcid", "orcid_tenure", "orcid_untimed", "roster_dblp"}


def asc(s):
    return unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode().lower()


def name_tokens(name):
    n = re.sub(r"[\(\[].*", "", asc(name))
    return [t for t in re.split(r"[^a-z]+", n) if t and t not in TITLES]


def to_int(v):
    try:
        return int(str(v or "").strip()[:4])
    except ValueError:
        return None


# ------------------------------------------------------------------------------------------------ F1 / F2b
def lag_for(inst):
    """Years a paper may precede the listed start: 1, but 0 for institutes founded 2015 or later (F1)."""
    f = REG[inst].get("founded")
    return 0 if f is not None and f >= 2015 else 1


def start_year(row):
    """(year, basis) from which a roster person counts at this institute: joining_year, else for people who are not current
    the first year of the designation's '(YYYY-YYYY)' range (archived-page range = upper bound, like a joining year)."""
    jy = to_int(row.get("joining_year"))
    if jy:
        return jy, "joining_year"
    if (row.get("status") or "") != "current":
        m = RANGE_RX.search(row.get("designation") or "")
        if m:
            return int(m.group(1)), "designation_range"
    return None, None


def lower_bound(inst, row):
    """Earliest record year that is plausible for the person: max(founded, start - lag); None when no start year (and no
    founding year to fall back on)."""
    f = REG[inst].get("founded")
    s, _ = start_year(row)
    if s is None:
        return f
    return max(f or 0, s - lag_for(inst))


def split_person(ps):
    """'Name [roster:Dept]' / 'Name (0000-0000-0000-0000)' / 'Name' -> (name, dept|None, orcid|None)"""
    m = re.match(r"^(.*?) \[roster:(.*)\]$", ps or "")
    if m:
        return m.group(1).strip(), m.group(2).strip(), None
    m = re.match(r"^(.*?) \((" + ORCID_RX.pattern + r")\)$", ps or "")
    if m:
        return m.group(1).strip(), None, m.group(2)
    return (ps or "").strip(), None, None


class Roster:
    """Roster rows of one institute with the lookups needed to turn a `found_via_person` string into a roster row."""

    def __init__(self, inst, rows):
        self.inst = inst
        self.rows = rows
        self.by_nd, self.by_n, self.by_o = collections.defaultdict(list), collections.defaultdict(list), {}
        for i, r in enumerate(rows):
            r["_i"] = i
            n = " ".join(name_tokens(r.get("name")))
            d = asc(r.get("department")).strip()
            self.by_nd[(n, d)].append(r)
            self.by_n[n].append(r)
            if (r.get("orcid") or "").strip():
                self.by_o[r["orcid"].strip()[-19:]] = r

    @classmethod
    def load(cls, inst, rosters_dir):
        fn = os.path.join(rosters_dir, f"{inst}_faculty.csv")
        if not os.path.exists(fn):
            return cls(inst, [])
        return cls(inst, list(csv.DictReader(open(fn, encoding="utf-8-sig"))))

    def resolve(self, ps):
        """roster row for a person string, or None (ORCID-profile person who is not in the roster / ambiguous name)."""
        name, dept, orcid = split_person(ps)
        n = " ".join(name_tokens(name))
        if dept is not None:
            c = self.by_nd.get((n, asc(dept).strip())) or self.by_n.get(n)
            return c[0] if c else None
        if orcid and orcid in self.by_o:
            return self.by_o[orcid]
        c = self.by_n.get(n)
        if c and (orcid or len(c) == 1):      # ORCID-profile person with a roster namesake; plain DBLP name only when unique
            return c[0]
        return None


def person_status(inst, roster, ps, year):
    """-> (status, info) with status in pass / fail / untimed / unresolved."""
    row = roster.resolve(ps)
    if row is None:
        return "unresolved", {"person": ps}
    lb = lower_bound(inst, row)
    s, basis = start_year(row)
    info = {"person": ps, "roster_name": row.get("name"), "status": row.get("status"), "start": s, "start_basis": basis,
            "lag": lag_for(inst), "bound": lb, "roster_row": row["_i"]}
    if lb is not None and year < lb:
        return "fail", info
    if s is None:
        return "untimed", info
    return "pass", info


def judge_start(inst, roster, persons, year):
    """F1 + F2b for one person-channel record.  -> dict(violates: bool, substatus, persons: [info...])"""
    seen, stats, infos = set(), collections.Counter(), []
    for ps in persons:
        row = roster.resolve(ps)
        if row is not None:
            if row["_i"] in seen:           # roster form and ORCID form of the same person count once
                continue
            seen.add(row["_i"])
        st, info = person_status(inst, roster, ps, year)
        stats[st] += 1
        info["result"] = st
        infos.append(info)
    if not infos:
        return {"violates": False, "substatus": None, "persons": []}
    if stats["pass"]:
        sub = "likely-timed"
    elif stats["unresolved"]:
        sub = "likely-nonroster"
    elif stats["untimed"]:
        sub = "likely-untimed"
    else:
        return {"violates": True, "substatus": None, "persons": infos}
    return {"violates": False, "substatus": sub, "persons": infos}


# ------------------------------------------------------------------------------------------------ F5
def generic_tokens(rosters_dir, family="iit", extra=()):
    """Name tokens that identify nobody: GENERIC_SEED + tokens carried by >= max(8, 0.5 %) of all roster people of this institution
    family (pooled over the family's roster files, distinct people) + `extra` (roster_channels.py: its COMMON_SURNAMES, the family
    names carried by >= 8 distinct first names in the verified pool)."""
    cnt, n = collections.Counter(), 0
    for fn in glob.glob(os.path.join(rosters_dir, f"{family}_*_faculty.csv")):
        seen = set()
        for r in csv.DictReader(open(fn, encoding="utf-8-sig")):
            toks = tuple(t for t in name_tokens(r.get("name")) if len(t) > 1)
            if not toks or toks in seen:
                continue
            seen.add(toks)
            n += 1
            for t in set(toks):
                cnt[t] += 1
    thr = max(GENERIC_MIN, math.ceil(GENERIC_SHARE * n))
    return set(GENERIC_SEED) | {t for t, c in cnt.items() if c >= thr} | set(extra)


def is_generic_name(name, generic):
    """family name (last token) or first given name (first token) is a generic token (initials never are)."""
    toks = name_tokens(name)
    if len(toks) < 2:
        return bool(toks) and toks[0] in generic
    return any(len(t) > 1 and t in generic for t in (toks[0], toks[-1]))


def why_ok(why):
    """Is this roster-channel `why` string enough to credit a generic-name person?  orcid / affiliation, or >= 2 shared
    co-authors (the plain rule's 'coauthors=1,venue=True' is not enough)."""
    if not why:
        return False
    w = str(why)
    if w in ("orcid", "affiliation"):
        return True
    m = re.search(r"coauthors=(\d+)", w)
    return bool(m and int(m.group(1)) >= 2)


def judge_namesake(persons, evidence, whys, generic):
    """F5 for one person-channel record.  -> None (not applicable / accepted) or dict(reason, ...) when the record must be demoted.
    Applies when every linked person has a generic name; accepted when the record has ORCID/DBLP-pid identity evidence, or one of the
    stored roster `why` strings is orcid / affiliation / >= 2 shared co-authors.  Without stored whys the record is not touched."""
    names = [split_person(p)[0] for p in persons]
    if not names or not all(is_generic_name(n, generic) for n in names):
        return None
    if IDENTITY_EVIDENCE & set(evidence):
        return None
    if not (set(evidence) & {"roster_crossref_author", "roster_arxiv"}):
        return None                    # no roster name-match evidence: nothing for this guard to judge
    whys = [w for w in (whys or []) if w]
    if not whys or any(why_ok(w) for w in whys):
        return None
    return {"reason": "namesake guard: generic name, no ORCID, no printed affiliation, fewer than 2 shared verified co-authors",
            "persons": names, "whys": whys}


# ------------------------------------------------------------------------------------------------ F3
def mega_collab(n_crossref=None, n_channel=None):
    """-> (author_count, mega_collab, basis).  Crossref author list first, then a channel list (Europe PMC / DOAJ / INSPIRE)."""
    if n_crossref:
        return n_crossref, n_crossref > MEGA_LIMIT, "crossref"
    if n_channel:
        return n_channel, n_channel > MEGA_LIMIT, "channel"
    return None, None, None
