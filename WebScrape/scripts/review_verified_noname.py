"""Output check of the other-institutes team (PROCESS_OTHER.md §2.6): every record of v2/<inst>.json that is `verified`
although none of its matched affiliation strings names the institute explicitly (explicit_full). Name collisions (an
acronym shared with an unrelated body, e.g. Rome's nursing "CECRI") and over-broad place rules show up here; every listed
record is read before the dataset is accepted.
usage: python3 review_verified_noname.py <inst>      (RM_OUT=v2)"""
import json, os, sys
from common import OUT
from affil import C

inst = sys.argv[1]
c = C[inst]
n = flagged = 0
for line in open(os.path.join(OUT, inst + ".json"), encoding="utf-8"):
    if not line.startswith('{"'):
        continue
    r = json.loads(line.rstrip(",\n"))
    if r.get("affiliation_status") != "verified":
        continue
    n += 1
    m = r.get("institute_affiliations_matched") or []
    if not any(c.explicit.search(s) for s in m):
        flagged += 1
        print(r.get("doi"), r.get("year"), "|", str(r.get("title"))[:70], "|", r.get("evidence"))
        for s in m[:3]:
            print("    ", s[:200])
print(f"{inst}: {flagged} of {n} verified records have no matched string naming the institute explicitly")
