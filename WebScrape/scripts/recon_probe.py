"""Reconnaissance aid for the other-institutes team (HANDOFF_other_institutes.md §5.1): Crossref `query.affiliation` hit
counts 2016-2026 per candidate token (rows=0), plus a sample of real affiliation strings that contain the token, so each
token's role (anchor / city / shared / rejected) can be decided from evidence. Appends counts to logs/recon_<label>.tsv.
usage: python3 recon_probe.py <label> <token> [<token> ...] [--sample N]"""
import os, sys, re, json
from common import get, LOGS

args = sys.argv[1:]
n = int(args[args.index("--sample") + 1]) if "--sample" in args else 15
if "--sample" in args:
    i = args.index("--sample"); args = args[:i] + args[i + 2:]
label, toks = args[0], args[1:]
F = "from-pub-date:2016-01-01,until-pub-date:2026-12-31"
log = open(os.path.join(LOGS, f"recon_{label}.tsv"), "a", encoding="utf-8")
for t in toks:
    d = get("https://api.crossref.org/works", params={"query.affiliation": t, "filter": F, "rows": 0}).json()
    total = d["message"]["total-results"]
    log.write(f"{t}\t{total}\n"); log.flush()
    print(f"\n### {t}: {total:,} hits", flush=True)
    if not n:
        continue
    items = get("https://api.crossref.org/works", params={"query.affiliation": t, "filter": F, "rows": n,
                                                         "select": "DOI,author"}).json()["message"]["items"]
    rx = re.compile(re.escape(t), re.I)
    seen = set()
    for it in items:
        for au in it.get("author", []):
            s = " | ".join(a.get("name", "") for a in au.get("affiliation", []))
            if s and rx.search(s) and s not in seen:
                seen.add(s); print("   ", s[:180])
