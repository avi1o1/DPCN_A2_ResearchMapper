"""Shared helpers for the publication scrape (HTTP session with retry/back-off, paths)."""
import gzip, json, os, time, random
import requests

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Inputs (rosters/, golden/, affil_manual/) live in ROOT = WebScrape/. Outputs (datasets, unconfirmed candidates, reports)
# go to OUT: WebScrape/ for the v1 run (Group 3 files used by Enrichment/ and Analysis/), WebScrape/v2/ for the v2 run of
# all IITs (set RM_OUT=v2; PROCESS.md §15). Run-time caches raw/ and logs/ are shared and git-ignored.
OUT = os.path.join(ROOT, os.environ["RM_OUT"]) if os.environ.get("RM_OUT") else ROOT
RAW = os.path.join(ROOT, "raw")
LOGS = os.path.join(ROOT, "logs")
MAILTO = os.environ.get("RM_MAILTO", "aviral.gupta@research.iiit.ac.in")  # Crossref "polite pool" contact: set RM_MAILTO to your own address
UA = f"DPCN-ResearchMapper/1.0 (mailto:{MAILTO})"
YEAR_MIN, YEAR_MAX = 2016, 2026
os.makedirs(RAW, exist_ok=True)   # run-time caches (git-ignored)
os.makedirs(LOGS, exist_ok=True)  # run-time logs (git-ignored)
os.makedirs(os.path.join(OUT, "logs"), exist_ok=True)
os.makedirs(os.path.join(OUT, "golden"), exist_ok=True)

from institutes import REG  # noqa: E402  (all institute facts: scripts/institutes.py)
INSTITUTES = {k: {"name": v["name"], "ror": v["ror"]} for k, v in REG.items()}

# Optional ORCID Public API token (free, personal; ORCID developer tools -> client_credentials, scope /read-public). The
# anonymous public API has a small per-IP daily quota (exhausted by one full roster run on 2026-10-27). Read from the
# environment or the git-ignored WebScrape/.env; never commit it. Without it, ORCID calls stay anonymous as before.
def _dotenv(key):
    try:
        for line in open(os.path.join(ROOT, ".env"), encoding="utf-8"):
            k, _, v = line.strip().partition("=")
            if k == key:
                return v.strip()
    except OSError:
        pass
    return ""


ORCID_TOKEN = os.environ.get("ORCID_TOKEN") or _dotenv("ORCID_TOKEN")

_session = requests.Session()
_session.headers["User-Agent"] = UA


# Crossref's polite pool allows 3 concurrent requests per client (x-concurrency-limit, 2026-10-25). Every Crossref call
# from any script/thread takes one of 3 file-lock slots, so parallel jobs can never exceed the limit together.
CROSSREF_SLOTS = 3
_SLOTDIR = os.path.join(LOGS, "crossref_slots")
os.makedirs(_SLOTDIR, exist_ok=True)

def try_lock(f):
    """Non-blocking exclusive lock on an open file; raises OSError if another process holds it.
    fcntl on Linux/macOS (unchanged behaviour); msvcrt byte-range lock on Windows, where fcntl does not exist."""
    if os.name == "nt":
        import msvcrt
        f.seek(0); msvcrt.locking(f.fileno(), msvcrt.LK_NBLCK, 1)
    else:
        import fcntl
        fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)


def unlock(f):
    if os.name == "nt":
        import msvcrt
        f.seek(0); msvcrt.locking(f.fileno(), msvcrt.LK_UNLCK, 1)
    else:
        import fcntl
        fcntl.flock(f, fcntl.LOCK_UN)


class _Slot:
    def __init__(self, url):
        self.f = None
        self.on = "api.crossref.org" in url

    def __enter__(self):
        while self.on:
            for k in range(CROSSREF_SLOTS):
                f = open(os.path.join(_SLOTDIR, f"slot{k}"), "a")
                try:
                    try_lock(f)
                    self.f = f
                    return self
                except OSError:
                    f.close()
            time.sleep(0.05 + random.random() * 0.1)
        return self

    def __exit__(self, *a):
        if self.f:
            unlock(self.f); self.f.close()


def get(url, params=None, tries=8, timeout=120, **kw):
    """GET with exponential back-off on 429/5xx/network errors. Returns Response or raises."""
    for i in range(tries):
        try:
            if ORCID_TOKEN and url.startswith("https://pub.orcid.org/"):
                kw["headers"] = {**(kw.get("headers") or {}), "Authorization": "Bearer " + ORCID_TOKEN}
            with _Slot(url):
                r = _session.get(url, params=params, timeout=timeout, **kw)
            if r.status_code == 200:
                return r
            if r.status_code == 404:
                return r
            wait = float(r.headers.get("Retry-After", 0) or 0) or min(120, 2 ** i + random.random())
        except requests.RequestException:
            wait = min(120, 2 ** i + random.random())
        time.sleep(wait)
    raise RuntimeError(f"GET failed after {tries} tries: {url} {params}")


def post(url, json_body=None, params=None, tries=8, timeout=120, **kw):
    for i in range(tries):
        try:
            r = _session.post(url, json=json_body, params=params, timeout=timeout, **kw)
            if r.status_code == 200:
                return r
            wait = float(r.headers.get("Retry-After", 0) or 0) or min(120, 2 ** i + random.random())
        except requests.RequestException:
            wait = min(120, 2 ** i + random.random())
        time.sleep(wait)
    raise RuntimeError(f"POST failed after {tries} tries: {url}")


def write_jsonl_gz(path, rows):
    with gzip.open(path, "wt", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


def read_jsonl_gz(path):
    """Yield JSON rows; stops quietly at a truncated/partially-written tail (shards may be appended
    to by a concurrent run). Use check_shards.py to verify caches are fully readable."""
    import zlib
    try:
        with gzip.open(path, "rt", encoding="utf-8") as f:
            for line in f:
                try:
                    yield json.loads(line)
                except json.JSONDecodeError:
                    return
    except (EOFError, zlib.error, OSError):
        return


DOI_RX = __import__("re").compile(r"10\.\d{4,9}/[^\s\"<>]+", __import__("re").I)


def norm_doi(d):
    """Extract and lowercase the DOI from strings such as 'doi 10.1/x', 'https://doi.org/10.1/x',
    'doi.org/10.1/x'. Returns None if no DOI pattern is present (e.g. '1-25', 'volumes/112/07')."""
    if not d:
        return None
    m = DOI_RX.search(d.strip())
    if not m:
        return None
    d = m.group(0).lower().rstrip(".,;)")
    # URL-style suffixes copied from publisher pages are not part of the DOI (e.g. IOP ".../meta")
    return __import__("re").sub(r"/(meta|full|abstract|pdf|epdf|fulltext|full/html|html)$", "", d)
