"""Interim, credit-free finish: merge -> faculty -> verify on whatever OpenAlex caches already exist, for the given institutes,
then export + networks for every institute that has an enriched file. Output is marked partial for institutes whose OpenAlex steps
(B/C/A2) have not completed; run_final.py overwrites it when credits are available.
usage: python3 run_interim.py <inst> [<inst> ...]"""
import os, subprocess, sys, glob
from concurrent.futures import ThreadPoolExecutor
import threading
HERE = os.path.dirname(os.path.abspath(__file__))
R = os.path.dirname(os.path.dirname(HERE))
base = dict(os.environ, ENRICH_SCRAPE_DIR=R + "/WebScrape/v2", ENRICH_OUT_DIR=R + "/Enrichment/out_v2",
            ENRICH_CACHE_DIR=R + "/Enrichment/cache_v2", PYTHONIOENCODING="utf-8")
SEM = threading.Semaphore(2)


def run(step, insts):
    e = dict(base, ENRICH_INSTS=",".join(insts))
    print("==", " ".join(step), insts if len(insts) < 3 else len(insts), flush=True)
    return subprocess.run([sys.executable] + step, cwd=HERE, env=e).returncode == 0


def one(inst):
    with SEM:
        for s in ("merge.py", "faculty.py", "verify.py"):
            if not run([s, inst], [inst]):
                print("FAILED", inst, s, flush=True); return False
    open(f"{R}/WebScrape/logs/pq4/{inst}.interim", "w").close()
    return True


insts = sys.argv[1:]
with ThreadPoolExecutor(3) as ex:
    list(ex.map(one, insts))
have = sorted(os.path.basename(f)[:-len("_enriched.json")] for f in glob.glob(R + "/Enrichment/out_v2/iit_*_enriched.json"))
for s in (["export_csv.py"], ["build_networks.py"], ["verify_networks.py"]):
    run(s, have)
print("INTERIM-DONE", len(have), "institutes", flush=True)
