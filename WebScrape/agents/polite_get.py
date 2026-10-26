"""Polite, shared-cache HTTP GET for all roster / golden-set agents (one machine, one IP).

usage: python3 -I polite_get.py URL [--out FILE] [--accept MIME] [--refresh]
Prints: <status>\t<path-of-cached-body>\t<final-url>
* Per-host minimum gap between requests, enforced ACROSS PROCESSES with a file lock
  (web.archive.org 3 s, arxiv.org 5 s, orcid.org 1 s, everything else 1 s per host).
* Honest User-Agent (no browser spoofing). Pages that answer with a bot challenge are reported, never bypassed.
* Body cached by URL hash in the shared cache, so agents never fetch the same URL twice.
"""
import sys, os, time, hashlib, json, urllib.parse
import requests

# blocking exclusive file lock: fcntl on Linux/macOS (unchanged); msvcrt byte-range lock on Windows (no fcntl there)
if os.name == "nt":
    import msvcrt

    def _lock(f):
        while True:
            try:
                f.seek(0); msvcrt.locking(f.fileno(), msvcrt.LK_NBLCK, 1); return
            except OSError:
                time.sleep(0.05)

    def _unlock(f):
        f.seek(0); msvcrt.locking(f.fileno(), msvcrt.LK_UNLCK, 1)
else:
    import fcntl

    def _lock(f):
        fcntl.flock(f, fcntl.LOCK_EX)

    def _unlock(f):
        fcntl.flock(f, fcntl.LOCK_UN)

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".runtime")   # git-ignored
CACHE, LOCKS = os.path.join(BASE, "shared_cache"), os.path.join(BASE, "locks")
os.makedirs(CACHE, exist_ok=True); os.makedirs(LOCKS, exist_ok=True)
UA = f"DPCN-ResearchMapper/1.0 (IIIT Hyderabad course project; mailto:{os.environ.get('RM_MAILTO', 'aviral.gupta@research.iiit.ac.in')})"
GAP = {"web.archive.org": 3.0, "archive.org": 3.0, "arxiv.org": 5.0, "export.arxiv.org": 5.0}  # operator decision 2026-10-25: 5 s (robots.txt asks 15 s), stop on 403
DEFAULT_GAP = 1.0

args = sys.argv[1:]
url = args[0]
out = args[args.index("--out") + 1] if "--out" in args else None
accept = args[args.index("--accept") + 1] if "--accept" in args else None
host = urllib.parse.urlsplit(url).hostname or "x"
key = hashlib.sha1((url + "|" + (accept or "")).encode()).hexdigest()
body_fn, meta_fn = os.path.join(CACHE, key + ".body"), os.path.join(CACHE, key + ".json")

if host.endswith("arxiv.org") and os.path.exists(os.path.join(LOCKS, "ARXIV_BLOCKED")):
    print("ARXIV_BLOCKED	-	arXiv returned 403 earlier: arXiv fetching is stopped for all agents"); sys.exit(0)
if os.path.exists(meta_fn) and "--refresh" not in args:
    meta = json.load(open(meta_fn))
else:
    meta = None
    for attempt in range(6):
        lk = open(os.path.join(LOCKS, host + ".lock"), "a+")
        _lock(lk)
        try:
            lk.seek(0); last = float(lk.read().strip() or 0)
            wait = GAP.get(host, DEFAULT_GAP) - (time.time() - last)
            if wait > 0:
                time.sleep(wait)
            lk.seek(0); lk.truncate(); lk.write(str(time.time())); lk.flush()
        finally:
            _unlock(lk); lk.close()
        try:
            h = {"User-Agent": UA}
            if accept:
                h["Accept"] = accept
            r = requests.get(url, headers=h, timeout=90, allow_redirects=True)
            st = r.status_code
        except requests.RequestException as e:
            st, r = f"ERR:{type(e).__name__}", None
            # DNS failures and broken TLS chains never succeed on retry: record them once and stop (pilot feedback)
            msg = str(e)
            if isinstance(e, requests.exceptions.SSLError) or "NameResolutionError" in msg or "Name or service not known" in msg                     or "nodename nor servname" in msg or "getaddrinfo failed" in msg:
                st = f"DEAD:{type(e).__name__}"
                break
        if st == 403 and host.endswith("arxiv.org"):
            # arXiv blocks over-eager clients with 403: create a stop file so every agent stops fetching arXiv
            open(os.path.join(LOCKS, "ARXIV_BLOCKED"), "w").write(time.strftime("%Y-%m-%dT%H:%M:%S"))
            break
        if st in (429, 500, 502, 503, 504) or isinstance(st, str):
            time.sleep(min(120, 10 * 2 ** attempt))
            continue
        break
    if r is not None:
        open(body_fn, "wb").write(r.content)
    meta = {"url": url, "status": st, "final_url": r.url if r is not None else None, "fetched": time.strftime("%Y-%m-%dT%H:%M:%S")}
    if (not isinstance(st, str) and st not in (429, 500, 502, 503, 504)) or str(st).startswith("DEAD:"):
        json.dump(meta, open(meta_fn, "w"))
if out and os.path.exists(body_fn):
    import shutil; shutil.copyfile(body_fn, out)
print(f"{meta['status']}\t{out or body_fn}\t{meta['final_url']}")
