"""Extra review list for non-IIT families (PROCESS_OTHER.md §2.4): every distinct author-affiliation string of an
institute's Crossref sweeps that classifies as the institute WITHOUT naming it explicitly (explicit_full). review_strings.py's
`iitnoname` list covers only verdicts without any type mention; for CSIR/DAE/NIT families a bare type mention ("CSIR") plus
a place token is the riskiest verdict, and it is not in that list. Newlines inside strings are written as \n.
usage: python3 review_notexplicit.py <inst> <outdir>     -> <outdir>/<inst>_notexplicit.tsv (string, author slots, records)"""
import os, sys, collections
from common import RAW, read_jsonl_gz
from affil import classify, C
from institutes import REG

inst, outd = sys.argv[1], sys.argv[2]
c = C[inst]
slots, recs = collections.Counter(), collections.defaultdict(set)
for t in REG[inst]["crossref"] + REG[inst]["crossref_broad"]:
    for it in read_jsonl_gz(os.path.join(RAW, "crossref_aff", t.replace(" ", "_") + ".light.jsonl.gz")):
        for au in it.get("author", []):
            s = " | ".join(a.get("name", "") for a in au.get("affiliation", []))
            if s and c.place.search(s):
                slots[s] += 1
                recs[s].add(it["DOI"])
rows = [s for s in slots if classify(inst, s) == "iit" and not c.explicit.search(s)]
rows.sort(key=lambda s: -slots[s])
with open(os.path.join(outd, f"{inst}_notexplicit.tsv"), "w", encoding="utf-8") as f:
    for s in rows:
        f.write(f"{s.replace(chr(10), ' \n ').replace(chr(9), ' ')}\t{slots[s]}\t{len(recs[s])}\n")
print(inst, "classified as the institute without its explicit name:", len(rows), "strings,", sum(slots[s] for s in rows), "slots")
