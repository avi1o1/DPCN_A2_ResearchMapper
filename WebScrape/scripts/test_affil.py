"""Rule tests of the affiliation classifier (no network access): every decision taken in the string review
(PROCESS.md §15.4) is a case in test_affil_cases.tsv (institute, expected class, real affiliation string, reason).
usage: python3 test_affil.py   -> prints failures, exit code 1 if any"""
import os, sys, csv
from affil import classify

import glob
# test_affil_cases.tsv (IIT team) + test_affil_cases_<team>.tsv (one file per team, same columns)
rows = []
for fn in sorted(glob.glob(os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_affil_cases*.tsv"))):
    rows += list(csv.DictReader(open(fn, encoding="utf-8"), delimiter="\t"))
bad = 0
for r in rows:
    got = classify(r["inst"], r["string"])
    if str(got) != r["expected"]:
        bad += 1
        print(f"FAIL {r['inst']}: expected {r['expected']}, got {got} | {r['string'][:120]} | {r['reason (PROCESS.md section)']}")
print(f"{len(rows) - bad}/{len(rows)} cases pass")
sys.exit(1 if bad else 0)
