"""Acceptance checks for agent outputs (the checks applied to every roster and golden set before it is used).
usage: python3 check_outputs.py <inst> [<inst> ...]
Exit code 1 if a hard check fails; warnings are printed for the reviewer to read."""
import csv, os, re, sys, collections, unicodedata

WS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROSTER_HDR = "name,department,designation,status,joining_year,profile_url,email,orcid,google_scholar,dblp,scopus_id,irins,homepage,source_url".split(",")
STATUS = {"current", "former", "emeritus", "visiting", "adjunct"}
RANGE = re.compile(r"\((\d{4})\s*-\s*(\d{4})\)")
bad = 0


def fail(msg):
    global bad
    bad += 1
    print("  FAIL", msg)


def norm(n):
    n = unicodedata.normalize("NFKD", n).encode("ascii", "ignore").decode().lower()
    return " ".join(sorted(x for x in re.split(r"[\s.\-,]+", n) if x))


def roster(inst):
    fn = os.path.join(WS, "rosters", f"{inst}_faculty.csv")
    if not os.path.exists(fn):
        print("  (no roster yet)"); return
    R = list(csv.DictReader(open(fn, encoding="utf-8-sig")))
    print(f"  roster: {len(R)} rows", dict(collections.Counter(r['status'] for r in R)))
    if list(R[0].keys()) != ROSTER_HDR:
        fail("roster header differs from the brief")
    if any(r["status"] not in STATUS for r in R):
        fail(f"unknown status values {set(r['status'] for r in R) - STATUS}")
    f = [r for r in R if r["status"] == "former" and not RANGE.search(r["designation"])]
    if f:
        fail(f"{len(f)} former rows without a (Y1-Y2) range, e.g. {f[0]['name']}")
    for r in R:
        m = RANGE.search(r["designation"])
        if m and not (1950 <= int(m.group(1)) <= int(m.group(2)) <= 2026):
            fail(f"implausible range {m.group(0)} for {r['name']}")
    if any(r["orcid"] and not re.fullmatch(r"\d{4}-\d{4}-\d{4}-\d{3}[\dX]", r["orcid"]) for r in R):
        fail("malformed ORCID iDs (must be bare 0000-0000-0000-000X)")
    if any(r["joining_year"] and not re.fullmatch(r"(19|20)\d\d", r["joining_year"]) for r in R):
        fail("malformed joining_year")
    dup = [k for k, c in collections.Counter(norm(r["name"]) for r in R).items() if c > 1]
    if dup:
        print(f"  warn: {len(dup)} names occur twice (check they are different people): {dup[:5]}")
    em = [e for e, c in collections.Counter(r["email"].lower() for r in R if r["email"]).items() if c > 1]
    if em:
        print(f"  warn: {len(em)} e-mail addresses on several rows (office / coordinator address? keep it only for its owner): {em[:3]}")
    if not os.path.exists(os.path.join(WS, "rosters", "notes", f"{inst}_roster_notes.md")):
        fail("roster notes file missing")


def golden(inst):
    fn = os.path.join(WS, "golden", f"golden_{inst}.csv")
    if not os.path.exists(fn):
        print("  (no golden set yet)"); return
    R = list(csv.DictReader(open(fn, encoding="utf-8-sig")))
    hdr = list(R[0].keys())
    print(f"  golden: {len(R)} rows", dict(collections.Counter(r['confidence'] for r in R)), dict(collections.Counter(r['evidence_source'] for r in R)))
    if hdr[:5] != ["title", "year", "doi", "venue", "type"] or not hdr[5].endswith("_author") or hdr[6:] != ["department", "evidence_source", "source_url", "confidence", "notes"]:
        fail(f"golden header differs from the brief: {hdr}")
    if any(not re.fullmatch(r"20(1[6-9]|2[0-6])", r["year"]) for r in R):
        fail("years outside 2016-2026")
    if any(r["doi"] and not r["doi"].startswith("10.") for r in R):
        fail("DOIs must be bare 10.xxxx/...")
    if any(r["confidence"] not in ("high", "medium") for r in R):
        fail("confidence must be high or medium")
    t = [k for k, c in collections.Counter(re.sub(r"\W", "", r["title"].lower()) for r in R).items() if c > 1]
    if t:
        fail(f"{len(t)} duplicate titles")
    top = collections.Counter(r[hdr[5]] for r in R).most_common(1)
    if top and top[0][1] > 8:
        print(f"  warn: {top[0][0]!r} has {top[0][1]} rows (cap 8 per person - or several people share this name form?)")
    if not os.path.exists(os.path.join(WS, "golden", "notes", f"golden_{inst}_notes.md")):
        fail("golden notes file missing")


for inst in sys.argv[1:]:
    print(inst)
    roster(inst)
    golden(inst)
sys.exit(1 if bad else 0)
