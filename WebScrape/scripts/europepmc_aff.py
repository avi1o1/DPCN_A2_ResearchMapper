"""Channel A2: Europe PMC affiliation search (resultType=core: full author affiliations, DOI,
journal ISSN, citedByCount). Raw records -> WebScrape/raw/europepmc/<inst>.jsonl.gz

usage: python3 europepmc_aff.py <inst_key>
"""
import os, sys
from common import get, RAW, LOGS, write_jsonl_gz
from institutes import REG

QUERIES = {k: v["europepmc"] for k, v in REG.items()}
inst = sys.argv[1]
os.makedirs(os.path.join(RAW, "europepmc"), exist_ok=True)
params = {"query": QUERIES[inst], "format": "json", "resultType": "core", "pageSize": 1000, "cursorMark": "*"}
rows = []
while True:
    d = get("https://www.ebi.ac.uk/europepmc/webservices/rest/search", params=params, timeout=300).json()
    res = d.get("resultList", {}).get("result", [])
    rows += res
    print(inst, len(rows), "/", d["hitCount"], flush=True)
    if not res or d.get("nextCursorMark") in (None, params["cursorMark"]):
        break
    params["cursorMark"] = d["nextCursorMark"]
write_jsonl_gz(os.path.join(RAW, "europepmc", inst + ".jsonl.gz"), rows)
with open(os.path.join(LOGS, "europepmc_runs.tsv"), "a") as lg:
    lg.write(f"{inst}\t{QUERIES[inst]}\t{len(rows)}\t{d['hitCount']}\n")
