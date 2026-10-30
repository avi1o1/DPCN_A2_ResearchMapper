"""Regression tests of the sanity-check rules F1, F2(b), F3, F5, F6 (sanity_rules.py, institutes.py).  No network, no data files:
every case is a real situation of the 2026-10-30 sanity audit, written out as a synthetic roster row.
usage: python3 test_sanity_rules.py   -> prints failures, exit code 1 if any"""
import os, sys, tempfile, csv
import sanity_rules as SR
from institutes import REG
from affil import classify

bad = 0
n = 0


def check(label, got, want):
    global bad, n
    n += 1
    if got != want:
        bad += 1
        print(f"FAIL {label}: expected {want!r}, got {got!r}")


def roster(inst, *rows):
    keys = ("name", "department", "status", "joining_year", "designation", "orcid")
    return SR.Roster(inst, [dict(zip(keys, r + ("",) * (len(keys) - len(r)))) for r in rows])


def start(inst, ros, persons, year):
    j = SR.judge_start(inst, ros, persons, year)
    return ("violates" if j["violates"] else j["substatus"])


# ------------------------------------------------------------------ F6: dates in institutes.py
check("F6 ISM founded", REG["iit_ism"]["founded"], 1926)
check("F6 ISM became IIT", REG["iit_ism"]["became_iit"], 2016)
check("F6 ISM former name", "Indian School of Mines" in REG["iit_ism"]["former_names"], True)
check("F6 BHU", (REG["iit_bhu"]["founded"], REG["iit_bhu"]["became_iit"]), (1919, 2012))
check("F6 Roorkee", (REG["iit_roorkee"]["founded"], REG["iit_roorkee"]["became_iit"]), (1847, 2001))
check("F6 Delhi", (REG["iit_delhi"]["founded"], REG["iit_delhi"]["became_iit"]), (1961, 1963))
check("F6 2016 institutes", {REG[k]["founded"] for k in ("iit_bhilai", "iit_dharwad", "iit_jammu", "iit_goa")}, {2016})
check("F6 every IIT has both dates", [k for k in REG if k.startswith("iit_") and (REG[k]["founded"] is None or REG[k]["became_iit"] is None)], [])
# an "Indian School of Mines" paper of 2016 is a paper of IIT (ISM): the classifier counts it and no start-year bound drops it
check("F6 ISM 2016 string is IIT (ISM)", classify("iit_ism", "Department of Applied Mathematics, Indian School of Mines, Dhanbad, India"), "iit")
ism = roster("iit_ism", ("Ashok Kumar", "Electrical Engineering", "current", "2022"), ("No Year", "Physics", "current", ""))
check("F6 ISM 2016 record, person without start year: kept, untimed (bound is founded 1926, not the 2016 IIT date)",
      start("iit_ism", ism, ["No Year [roster:Physics]"], 2016), "likely-untimed")
check("F6 lower bound without start year = founded", SR.lower_bound("iit_ism", ism.rows[1]), 1926)

# ------------------------------------------------------------------ F1: start-year rule
kan = roster("iit_kanpur", ("Raghvendra Kumar Chaudhary", "Electrical Engineering", "current", "2022", "", "0000-0001-6186-4089"),
             ("Singh Raghvendra", "Chemical Engineering", "current", "2009"))
rkc = ["Raghvendra Kumar Chaudhary [roster:Electrical Engineering]"]
check("F1 Kanpur Raghvendra Kumar Chaudhary 2016 (joined 2022): demoted", start("iit_kanpur", kan, rkc, 2016), "violates")
check("F1 Kanpur Raghvendra 2020 (2 years before): demoted", start("iit_kanpur", kan, rkc, 2020), "violates")
check("F1 Kanpur Raghvendra 2021 (lag 1 for current staff): kept", start("iit_kanpur", kan, rkc, 2021), "likely-timed")
check("F1 Kanpur Raghvendra 2022: kept", start("iit_kanpur", kan, rkc, 2022), "likely-timed")
check("F1 ORCID form of the same person resolves to the roster row",
      start("iit_kanpur", kan, ["Raghvendra Kumar Chaudhary (0000-0001-6186-4089)"], 2016), "violates")
check("F1 the roster-form and ORCID-form strings of one person count once",
      start("iit_kanpur", kan, rkc + ["Raghvendra Kumar Chaudhary (0000-0001-6186-4089)"], 2016), "violates")
check("F1 a namesake with another roster row (joined 2009) validates the record",
      start("iit_kanpur", kan, rkc + ["Singh Raghvendra [roster:Chemical Engineering]"], 2016), "likely-timed")

bhi = roster("iit_bhilai", ("Sudhanwa Patra", "Physics", "current", "2017", "", "0000-0002-7469-2279"),
             ("Arnab Patra", "Mathematics", "current", "2021"), ("Sabyasachi Ghosh", "Physics", "current", "2018"))
sp, ap = ["Sudhanwa Patra [roster:Physics]", "Sudhanwa Patra (0000-0002-7469-2279)"], ["Arnab Patra [roster:Mathematics]"]
check("F1 Bhilai (founded 2016, lag 0): Sudhanwa Patra 2016 is before the joining year 2017", start("iit_bhilai", bhi, sp, 2016), "violates")
check("F1 Bhilai Sudhanwa Patra 2017: kept", start("iit_bhilai", bhi, sp, 2017), "likely-timed")
check("F1 Bhilai Arnab Patra 2018 (joined 2021; iit_bhilai-000039): demoted", start("iit_bhilai", bhi, ap, 2018), "violates")
check("F1 Bhilai Sabyasachi Ghosh 2017 (joined 2018, lag 0): demoted", start("iit_bhilai", bhi, ["Sabyasachi Ghosh [roster:Physics]"], 2017), "violates")
check("F1 lag: 1 for an old institute, 0 for institutes founded 2015+", (SR.lag_for("iit_kanpur"), SR.lag_for("iit_palakkad"), SR.lag_for("iit_goa")), (1, 0, 0))

jam = roster("iit_jammu", ("Rakesh K Tekade", "Materials Engineering", "former", "", "Former faculty (2019-2019); last listed as Assistant Professor"),
             ("No Range", "Physics", "former", "", "Former faculty"))
tek = ["Rakesh K Tekade [roster:Materials Engineering]"]
check("F1 Jammu Tekade RK: no joining year, designation range 2019-2019 -> start 2019", SR.start_year(jam.rows[0]), (2019, "designation_range"))
check("F1 Jammu Tekade RK 2017 (before the listed range): demoted", start("iit_jammu", jam, tek, 2017), "violates")
check("F1 Jammu Tekade RK 2019: kept", start("iit_jammu", jam, tek, 2019), "likely-timed")
check("F1 a person who is current never takes the range", SR.start_year({"status": "current", "designation": "x (2019-2019)"}), (None, None))
check("F1 former person with neither year nor range: untested", start("iit_jammu", jam, ["No Range [roster:Physics]"], 2017), "likely-untimed")

# the founding year is a lower bound of its own
REG["iit_zz"] = {"founded": 2018, "became_iit": 2018, "former_names": ()}
zz = roster("iit_zz", ("Early Bird", "Physics", "current", "2010"), ("Undated", "Physics", "current", ""))
check("F1/F6 founded bound: joining year 2010 is not an excuse for a 2017 paper at an institute founded 2018",
      start("iit_zz", zz, ["Early Bird [roster:Physics]"], 2017), "violates")
check("F1/F6 founded bound also holds for a person without start year", start("iit_zz", zz, ["Undated [roster:Physics]"], 2017), "violates")
check("F1/F6 founded bound: 2018 kept", start("iit_zz", zz, ["Early Bird [roster:Physics]"], 2018), "likely-timed")
del REG["iit_zz"]

# ------------------------------------------------------------------ F2(b): untimed sub-tier
mix = roster("iit_kanpur", ("Has Year", "Physics", "current", "2010"), ("No Year", "Physics", "current", ""), ("Late Joiner", "Physics", "current", "2024"))
check("F2b all linked roster people without a joining year -> likely-untimed", start("iit_kanpur", mix, ["No Year [roster:Physics]"], 2017), "likely-untimed")
check("F2b a tested person who passes -> likely-timed", start("iit_kanpur", mix, ["Has Year [roster:Physics]", "No Year [roster:Physics]"], 2017), "likely-timed")
check("F2b linked only to an ORCID-profile person who is not in the roster -> likely-nonroster",
      start("iit_kanpur", mix, ["Somebody Else (0000-0002-1825-0097)"], 2017), "likely-nonroster")
check("F2b one person fails, the other has no year: the record rests on the untimed one -> likely-untimed",
      start("iit_kanpur", mix, ["Late Joiner [roster:Physics]", "No Year [roster:Physics]"], 2017), "likely-untimed")
check("F2b no person at all: no sub-tier", SR.judge_start("iit_kanpur", mix, [], 2017)["substatus"], None)

# ------------------------------------------------------------------ F3: mega-collaboration flag
check("F3 Seema Bahinipati / CMS paper (2,600 Crossref authors)", SR.mega_collab(2600, None), (2600, True, "crossref"))
check("F3 exactly 100 authors is not mega", SR.mega_collab(100, None), (100, False, "crossref"))
check("F3 101 authors is mega", SR.mega_collab(101, None), (101, True, "crossref"))
check("F3 Crossref list wins over the channel list", SR.mega_collab(8, 400), (8, False, "crossref"))
check("F3 channel list as fallback (INSPIRE / Europe PMC)", SR.mega_collab(None, 250), (250, True, "channel"))
check("F3 no author list at all: unknown, not False", SR.mega_collab(None, None), (None, None, None))
check("F3 empty Crossref list is not 'zero authors'", SR.mega_collab(0, None), (None, None, None))

# ------------------------------------------------------------------ F5: namesake guard
G = SR.generic_tokens(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "rosters"), family="iit")
for nm in ("Ashok Kumar", "Nagendra Kumar", "Vivek Verma", "Dinesh Kumar", "Sumit Kumar", "Deepak Kumar", "Kumar Raghvendra", "Anil Sharma"):
    check(f"F5 generic name: {nm}", SR.is_generic_name(nm, G), True)
for nm in ("Yogesh Singh Chauhan", "Sudhanwa Patra", "Seema Bahinipati", "Rakesh K Tekade", "Sridhar Chimalakonda"):
    check(f"F5 not generic (middle name or rare name): {nm}", SR.is_generic_name(nm, G), False)
check("F5 initials alone are never generic", SR.is_generic_name("K. S. Prabhu", G), False)
check("F5 data-built list: frequent given names of the rosters (not in the hand seed) are generic",
      ("amit" in G, "amit" in SR.GENERIC_SEED), (True, False))
with tempfile.TemporaryDirectory() as d:     # threshold: >= 8 distinct people, built from the roster files of the family
    with open(os.path.join(d, "iit_x_faculty.csv"), "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["name"])
        for i in range(8):
            w.writerow([f"P{chr(97 + i)}ula Zorba{chr(97 + i)} Qux"])
        for i in range(7):
            w.writerow([f"Rare{chr(97 + i)} Name{chr(97 + i)} Wibble"])
    g2 = SR.generic_tokens(d, family="iit", extra={"fromverifiedpool"})
    check("F5 token carried by 8 roster people is generic, by 7 is not, extra names are added",
          ("qux" in g2, "wibble" in g2, "fromverifiedpool" in g2), (True, False, True))
ak = ["Ashok Kumar [roster:Electrical Engineering]"]
check("F5 Ashok Kumar, roster author search with 1 co-author + venue: demoted",
      bool(SR.judge_namesake(ak, ["roster_crossref_author"], ["coauthors=1,venue=True"], G)), True)
check("F5 ... with 2 shared co-authors: accepted", SR.judge_namesake(ak, ["roster_crossref_author"], ["coauthors=2,venue=False"], G), None)
check("F5 ... one of several stored whys is enough", SR.judge_namesake(ak, ["roster_crossref_author"], ["coauthors=1,venue=True", "coauthors=3,venue=True"], G), None)
check("F5 ... ORCID match on the paper: accepted", SR.judge_namesake(ak, ["roster_crossref_author"], ["orcid"], G), None)
check("F5 ... printed affiliation: accepted", SR.judge_namesake(ak, ["roster_arxiv"], ["affiliation"], G), None)
check("F5 ... listed on the person's ORCID profile (roster_orcid / orcid_tenure): accepted", SR.judge_namesake(ak, ["orcid_tenure", "roster_crossref_author"], ["coauthors=1,venue=True"], G), None)
check("F5 ... arXiv, one shared co-author: demoted", bool(SR.judge_namesake(ak, ["roster_arxiv"], ["coauthors=1"], G)), True)
check("F5 ... no stored why (old candidates file): not touched", SR.judge_namesake(ak, ["roster_crossref_author"], [], G), None)
check("F5 ... a non-generic co-linked person keeps the record",
      SR.judge_namesake(ak + ["Yogesh Singh Chauhan [roster:Electrical Engineering]"], ["roster_crossref_author"], ["coauthors=1,venue=True"], G), None)
check("F5 non-generic person, 1 co-author + venue: the plain rule stands",
      SR.judge_namesake(["Sudhanwa Patra [roster:Physics]"], ["roster_crossref_author"], ["coauthors=1,venue=True"], G), None)
check("F5 why_ok", [SR.why_ok(w) for w in ("orcid", "affiliation", "coauthors=2,venue=False", "coauthors=1,venue=True", "coauthors=2,venue=True,ambiguous_name", None, "")],
      [True, True, True, False, True, False, False])

print(f"{n - bad}/{n} cases pass")
sys.exit(1 if bad else 0)
