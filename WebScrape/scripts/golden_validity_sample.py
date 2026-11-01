"""Seeded sample of medium-confidence golden-set rows for the golden-set validity audit (PROCESS.md section 15.16 / 15.18).
usage: python3 golden_validity_sample.py <inst> [n=30]      -> v2/golden/golden_validity_sample_<inst>.csv
Up to n rows of the institute's golden file whose confidence is not 'high', drawn at random (seed 20261101 + institute name) and
stratified by evidence_source in proportion to the stratum size (at least one row per stratum while rows remain).  The sample keeps
the golden row's line number (header = line 1) in `golden_line`; the verdict columns stay empty for the auditing agents."""
import csv, os, random, sys, collections, zlib
HERE = os.path.dirname(os.path.abspath(__file__))
inst, n = sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 30
rows = list(csv.DictReader(open(os.path.join(HERE, "..", "golden", f"golden_{inst}.csv"), encoding="utf-8-sig")))
cand = [(i + 2, r) for i, r in enumerate(rows) if (r.get("confidence") or "").strip().lower() != "high"]
rng = random.Random(20261101 + zlib.crc32(inst.encode()))
by = collections.defaultdict(list)
for ln, r in cand:
    by[r.get("evidence_source") or ""].append((ln, r))
pick = []
if len(cand) <= n:
    pick = cand
else:
    quota = {k: max(1, round(n * len(v) / len(cand))) for k, v in by.items()}
    while sum(quota.values()) > n:
        quota[max(quota, key=quota.get)] -= 1
    while sum(quota.values()) < n:
        k = max(by, key=lambda k: len(by[k]) - quota[k]); quota[k] += 1
    for k, v in by.items():
        pick += rng.sample(v, min(quota[k], len(v)))
pick.sort(key=lambda t: t[0])
out = os.path.join(HERE, "..", "v2", "golden", f"golden_validity_sample_{inst}.csv")
cols = ["golden_line", "title", "year", "doi", "venue", "author", "department", "evidence_source", "source_url", "verdict", "evidence_url", "notes"]
authcol = next(c for c in rows[0] if c.endswith("_author"))
w = csv.writer(open(out, "w", newline="", encoding="utf-8"))
w.writerow(cols)
for ln, r in pick:
    w.writerow([ln, r["title"], r["year"], r["doi"], r["venue"], r[authcol], r["department"], r["evidence_source"], r["source_url"], "", "", ""])
print(inst, "medium rows", len(cand), "sampled", len(pick), dict(collections.Counter(r["evidence_source"] for _, r in pick)))
