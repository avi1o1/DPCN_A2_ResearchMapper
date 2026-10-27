"""Why were golden-set papers never discovered? (PROCESS_OTHER.md, recall follow-up.) For every `not_discovered` row of
v2/golden/misses_<inst>.csv, look the paper up in Crossref (DOI if printed, else title search; title-word overlap >= 0.9 both
ways and |year| <= 1) and classify the deposited author affiliations:
  no_crossref       - not found in Crossref (not indexable by the Crossref channels)
  no_affiliation    - found, but no author affiliation deposited (only person channels / Europe PMC can find it)
  aff_other         - affiliations deposited, none names this institution (golden row or deposit problem)
  aff_ours_no_token - an affiliation is classified as this institution, but contains none of its Crossref sweep tokens
                      (fixable: a token is missing)
  aff_ours_token    - classified as ours and contains a sweep token (the sweep should have found it: harvest problem)
usage: python3 diagnose_misses.py <inst>      (RM_OUT=v2; writes v2/golden/miss_diagnosis_<inst>.csv)"""
import csv, os, re, sys, unicodedata
from collections import Counter
from common import OUT, get
from affil import classify
from institutes import REG

inst = sys.argv[1]
c = REG[inst]
tokens = [t.lower() for t in c["crossref"] + c["crossref_broad"]]
STOP = set("a an the of and in on for with to by from at as is are via its into using based new".split())


def words(s):
    s = unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode().lower()
    return [w for w in re.sub(r"[^a-z0-9]+", " ", s).split() if len(w) > 2 and w not in STOP]


def same(a, b):
    wa, wb = words(a), set(words(b))
    return bool(wa) and sum(w in wb for w in wa) / len(wa) >= 0.9


rows = [r for r in csv.DictReader(open(os.path.join(OUT, "golden", f"misses_{inst}.csv"), encoding="utf-8"))
        if r.get("diagnosis") == "not_discovered"]
out, cnt = [], Counter()
for r in rows:
    it = None
    if r["doi"].strip():
        try:
            it = get("https://api.crossref.org/works/" + r["doi"].strip()).json()["message"]
        except Exception:
            it = None
    if it is None:
        try:
            items = get("https://api.crossref.org/works", params={"query.bibliographic": r["title"], "rows": 3}).json()["message"]["items"]
        except Exception:
            items = []
        for x in items:
            t = (x.get("title") or [""])[0]
            y = ((x.get("issued") or {}).get("date-parts") or [[0]])[0][0] or 0
            if same(r["title"], t) and same(t, r["title"]) and abs(y - int(r["year"] or 0)) <= 1:
                it = x
                break
    affs = [a.get("name", "") for au in (it or {}).get("author", []) for a in au.get("affiliation", [])]
    ours = [a for a in affs if classify(inst, a) == "iit"]
    if it is None:
        d = "no_crossref"
    elif not affs:
        d = "no_affiliation"
    elif not ours:
        d = "aff_other"
    elif not any(re.search(r"\b" + re.escape(t) + r"\b", a.lower()) for a in ours for t in tokens):
        d = "aff_ours_no_token"
    else:
        d = "aff_ours_token"
    cnt[d] += 1
    out.append({"title": r["title"][:150], "year": r["year"], "golden_doi": r["doi"], "crossref_doi": (it or {}).get("DOI", ""),
                "diagnosis": d, "example_affiliation": (ours or affs or [""])[0][:200]})
fn = os.path.join(OUT, "golden", f"miss_diagnosis_{inst}.csv")
with open(fn, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(out[0].keys()) if out else ["title"])
    w.writeheader()
    w.writerows(out)
print(inst, len(rows), "not_discovered:", dict(cnt))
for o in out:
    if o["diagnosis"] in ("aff_ours_no_token", "aff_ours_token"):
        print(" ", o["diagnosis"], o["crossref_doi"], "|", o["example_affiliation"][:150])
