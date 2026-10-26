"""Classifier review aid (PROCESS.md §3.2, §15.4): every distinct author-affiliation string of an institute's Crossref sweep
records that mentions one of its tokens (or an IIT), with its class and frequency.
Writes <outdir>/<inst>_{uncertain,other,iit,iitnone}.tsv (string, author slots, records) and prints the class counts.
`iitnone` = strings with an IIT mention and one of the institute's shared tokens that classify as None (possible misses).
usage: python3 review_strings.py <inst> <outdir>"""
import os, sys, glob, re, collections
from common import RAW, read_jsonl_gz
from affil import classify, C, IIT, explicit_other
from institutes import REG

inst, outd = sys.argv[1], sys.argv[2]
toks = [t.replace(" ", "_") for t in REG[inst]["crossref"] + REG[inst]["crossref_broad"]]
c = C[inst]
slots, recs = collections.Counter(), collections.defaultdict(set)
for t in toks:
    fn = os.path.join(RAW, "crossref_aff", t + ".light.jsonl.gz")
    for it in read_jsonl_gz(fn):
        for au in it.get("author", []):
            s = " | ".join(a.get("name", "") for a in au.get("affiliation", []))
            if s and (c.place.search(s) or (c.state and c.state.search(s) and c.mention.search(s))):
                slots[s] += 1
                recs[s].add(it["DOI"])
cls = {s: classify(inst, s) for s in slots}
out = collections.defaultdict(list)
for k in ("iit", "other", "uncertain", "iitnone", "iitnoname"):
    if os.path.exists(os.path.join(outd, f"{inst}_{k}.tsv")):
        os.remove(os.path.join(outd, f"{inst}_{k}.tsv"))
for s, k in cls.items():
    if k is None:
        if c.mention.search(s):
            out["iitnone"].append(s)
        continue
    out[k].append(s)
    if k == "iit" and not c.mention.search(s) and not c.explicit.search(s):
        out["iitnoname"].append(s)   # iit without any IIT mention (department rule / unit name): highest-risk verdicts
for k, L in out.items():
    L.sort(key=lambda s: -slots[s])
    with open(os.path.join(outd, f"{inst}_{k}.tsv"), "w") as f:
        for s in L:
            f.write(f"{s}\t{slots[s]}\t{len(recs[s])}\n")
print(inst, {k: (len(L), sum(slots[s] for s in L)) for k, L in sorted(out.items())})
