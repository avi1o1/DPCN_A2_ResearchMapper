"""Final OpenAlex enrichment for all 23 IITs, pipelined per institute: each institute starts as soon as its pipeline output is ready
(WebScrape/logs/pq4/<inst>.ready), so early institutes do not wait for the late arXiv passes. Credit-aware: each online step uses the key
with the most credits left (all keys in the repo .env, OPENALEX_KEYS), waits when none has any; every step is resumable. Never prints a key.
Per institute: fetch -> merge -> refdoi (exclusive) -> B||C -> A2 title search -> merge -> faculty -> verify.
At the end: export + networks for all.   Run: python3 -u Enrichment/scripts/run_final.py   (the cwd does not matter)"""
import os, subprocess, sys, time, threading, urllib.request
from concurrent.futures import ThreadPoolExecutor
HERE = os.path.dirname(os.path.abspath(__file__))
R = os.path.dirname(os.path.dirname(HERE))
READY = R + "/WebScrape/logs/pq4/%s.ready"
raw = [l.split("=", 1)[1].strip().strip('"').strip("'") for l in open(R + "/.env") if l.startswith("OPENALEX_KEYS=")][0]
KEYS = [k.strip() for k in raw.replace(";", ",").split(",") if k.strip()]
ORDER = ["iit_bhilai", "iit_dharwad", "iit_patna", "iit_jammu", "iit_mandi", "iit_indore", "iit_bhubaneswar", "iit_gandhinagar",
         "iit_jodhpur", "iit_goa", "iit_palakkad", "iit_tirupati", "iit_bhu", "iit_hyderabad", "iit_guwahati", "iit_delhi",
         "iit_ism", "iit_kanpur", "iit_madras", "iit_bombay", "iit_ropar", "iit_roorkee", "iit_kharagpur"]
base = dict(os.environ, ENRICH_SCRAPE_DIR=R + "/WebScrape/v2", ENRICH_OUT_DIR=R + "/Enrichment/out_v2",
            ENRICH_CACHE_DIR=R + "/Enrichment/cache_v2", PYTHONIOENCODING="utf-8")
MERGE_SEM = threading.Semaphore(2)      # merge/faculty/verify hold up to ~4 GB each
REF_LOCK = threading.Lock()             # refdoi writes shared cache files
log_lock = threading.Lock()


def remaining(k):
    """Credits left on a key; k=None probes the free unauthenticated allowance."""
    url = "https://api.openalex.org/works?per-page=1&select=id" + (f"&api_key={k}" if k else "")
    try:
        r = urllib.request.urlopen(url, timeout=30)
        return int(r.headers.get("X-RateLimit-Remaining") or 0)
    except Exception:
        return 0


def best_key(need):
    """Returns the key with the most credits (a string), or "" for the unauthenticated allowance; waits when none has any."""
    while True:
        cands = [(remaining(k), i, k) for i, k in enumerate(KEYS)] + [(remaining(None), -1, "")]
        rem, _, key = max(cands)
        if rem >= need:
            return key
        with log_lock:
            print(f"{time.strftime('%H:%M')} no key or free allowance has >= {need} credits (best {rem}); waiting 10 min", flush=True)
        time.sleep(600)


def run(step, inst, need=40, online=False, tries=300):
    for t in range(tries):
        e = dict(base, ENRICH_INSTS=inst)
        if online:
            k = best_key(need)
            if k:
                e["OPENALEX_API_KEY"] = k
                e.pop("OPENALEX_NO_KEY", None)
            else:
                e["OPENALEX_NO_KEY"] = "1"      # free unauthenticated allowance
                e.pop("OPENALEX_API_KEY", None)
        print(f"== {time.strftime('%H:%M')} {inst} {' '.join(step)} try {t}", flush=True)
        if subprocess.run([sys.executable] + step, cwd=HERE, env=e).returncode == 0:
            return True
        time.sleep(120)
    print("GAVE UP", inst, step, flush=True)
    return False


def heavy(step, inst):
    with MERGE_SEM:
        return run(step, inst)


def pipeline(inst):
    if os.path.exists(f"{R}/WebScrape/logs/pq4/{inst}.enriched"):
        return                      # already fully enriched in an earlier run
    while not os.path.exists(READY % inst):
        time.sleep(60)
    print(f"== {time.strftime('%H:%M')} {inst} READY", flush=True)
    run(["stage_a_fetch.py", inst], inst, online=True)
    heavy(["merge.py", inst], inst)
    with REF_LOCK:
        run(["stage_refdoi.py"], inst, online=True)
    with ThreadPoolExecutor(2) as ex:
        list(ex.map(lambda st: run(["stage_bc_indian.py", st, inst], inst, online=True), ("b", "c")))
    run(["stage_a2_title.py", inst], inst, online=True)
    for s in ("merge.py", "faculty.py", "verify.py"):
        heavy([s, inst], inst)
    open(f"{R}/WebScrape/logs/pq4/{inst}.enriched", "w").close()
    print(f"== {time.strftime('%H:%M')} {inst} ENRICHED", flush=True)


if __name__ == "__main__":
    if os.environ.get("ENRICH_ORDER"):          # priority order, e.g. cheapest institutes first, when credits are scarce
        ORDER = [x for x in os.environ["ENRICH_ORDER"].split(",") if x]
    with ThreadPoolExecutor(int(os.environ.get("ENRICH_WORKERS", "5"))) as ex:
        list(ex.map(pipeline, ORDER))
    ALL = ",".join(ORDER)
    for s in (["export_csv.py"], ["build_networks.py"], ["verify_networks.py"]):
        run(s, ALL)
    open(f"{R}/WebScrape/logs/pq4/ALL.enriched", "w").close()
    print("FINAL-ENRICH-DONE", flush=True)
