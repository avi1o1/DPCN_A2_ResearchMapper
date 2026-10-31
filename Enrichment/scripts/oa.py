"""Shared paths and OpenAlex helpers: key loading, a polite GET with retries, and credit logging.
API key: only needed by the online steps. Give it as the environment variable OPENALEX_API_KEY, or put it in a file
and set OPENALEX_KEY_FILE to that file's path. Never commit a key (.gitignore blocks .openalex_key* and .env)."""
import os, time, json, requests

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)                        # Enrichment/
REPO = os.path.dirname(ROOT)
# Directories can be redirected for the v2 institutes (defaults unchanged = the Kharagpur/Roorkee runs):
#   ENRICH_SCRAPE_DIR  scraped datasets  (default ../WebScrape;  v2: ../WebScrape/v2)
#   ENRICH_OUT_DIR     outputs           (default Enrichment/out; v2: Enrichment/out_v2)
#   ENRICH_CACHE_DIR   per-institute caches (default Enrichment/cache; v2: Enrichment/cache_v2)
# Relative values are resolved against the repo root. Scimago/CORE rank files always stay in Enrichment/cache.
def _dir(env, default):
    v = os.environ.get(env)
    return default if not v else (v if os.path.isabs(v) else os.path.join(REPO, v))


DATA = _dir("ENRICH_SCRAPE_DIR", os.path.join(REPO, "WebScrape"))   # input: the scraped datasets (iit_<inst>.json)
SHARED_CACHE = os.path.join(ROOT, "cache")          # rank files (cache/scimago, cache/core): shared by all runs
CACHE = _dir("ENRICH_CACHE_DIR", SHARED_CACHE)
OUT = _dir("ENRICH_OUT_DIR", os.path.join(ROOT, "out"))
os.makedirs(CACHE, exist_ok=True)
os.makedirs(OUT, exist_ok=True)

BASE = "https://api.openalex.org"
_key = []


def api_key():
    """The OpenAlex key, read on first use (offline steps never need it)."""
    if not _key:
        k = os.environ.get("OPENALEX_API_KEY")
        if not k:
            fn = os.environ.get("OPENALEX_KEY_FILE") or os.path.join(ROOT, ".openalex_key")
            if not os.path.exists(fn):
                raise SystemExit("OpenAlex key missing: set OPENALEX_API_KEY or OPENALEX_KEY_FILE (see oa.py)")
            k = open(fn).read().strip()
        _key.append(k)
    return _key[0]
INST = {
    "iit_kharagpur": {"oa": "I145894827", "ror": "https://ror.org/03w5sq511", "name": "IIT Kharagpur"},
    "iit_roorkee": {"oa": "I154851008", "ror": "https://ror.org/00582g326", "name": "IIT Roorkee"},
    "iit_ropar": {"oa": "I119241673", "ror": "https://ror.org/02qkhhn56", "name": "IIT Ropar"},   # id read from cached OpenAlex records; ROR from institutes.py
# IIT v2 institutes (WebScrape/v2): OpenAlex ids looked up 2026-10-30 via /institutions?filter=ror:...; ROR from WebScrape/scripts/institutes.py
    "iit_bhilai": {"oa": "I4210121466", "ror": "https://ror.org/02sscsx71", "name": "IIT Bhilai"},
    "iit_bhu": {"oa": "I56404289", "ror": "https://ror.org/01kh5gc44", "name": "IIT (BHU) Varanasi"},
    "iit_bhubaneswar": {"oa": "I99729588", "ror": "https://ror.org/04gx72j20", "name": "IIT Bhubaneswar"},
    "iit_bombay": {"oa": "I162827531", "ror": "https://ror.org/02qyf5152", "name": "IIT Bombay"},
    "iit_delhi": {"oa": "I68891433", "ror": "https://ror.org/049tgcd06", "name": "IIT Delhi"},
    "iit_dharwad": {"oa": "I4210152718", "ror": "https://ror.org/0509djg30", "name": "IIT Dharwad"},
    "iit_gandhinagar": {"oa": "I27674431", "ror": "https://ror.org/0036p5w23", "name": "IIT Gandhinagar"},
    "iit_goa": {"oa": "I4210112052", "ror": "https://ror.org/02v7trd43", "name": "IIT Goa"},
    "iit_guwahati": {"oa": "I1317621060", "ror": "https://ror.org/0022nd079", "name": "IIT Guwahati"},
    "iit_hyderabad": {"oa": "I65181880", "ror": "https://ror.org/01j4v3x97", "name": "IIT Hyderabad"},
    "iit_indore": {"oa": "I64295750", "ror": "https://ror.org/01hhf7w52", "name": "IIT Indore"},
    "iit_ism": {"oa": "I189109744", "ror": "https://ror.org/013v3cc28", "name": "IIT (ISM) Dhanbad"},
    "iit_jammu": {"oa": "I4210127441", "ror": "https://ror.org/02f0vsw63", "name": "IIT Jammu"},
    "iit_jodhpur": {"oa": "I154549908", "ror": "https://ror.org/03yacj906", "name": "IIT Jodhpur"},
    "iit_kanpur": {"oa": "I94234084", "ror": "https://ror.org/05pjsgx75", "name": "IIT Kanpur"},
    "iit_madras": {"oa": "I24676775", "ror": "https://ror.org/03v0r5n49", "name": "IIT Madras"},
    "iit_mandi": {"oa": "I9579091", "ror": "https://ror.org/05r9r2f34", "name": "IIT Mandi"},
    "iit_palakkad": {"oa": "I4210113248", "ror": "https://ror.org/0264cg909", "name": "IIT Palakkad"},
    "iit_patna": {"oa": "I132153292", "ror": "https://ror.org/01ft5vz71", "name": "IIT Patna"},
    "iit_tirupati": {"oa": "I4210109292", "ror": "https://ror.org/01xtkxh20", "name": "IIT Tirupati"},
# IIIT v2 institutes (WebScrape/v2, IIIT team): OpenAlex ids from the institutions on the cached stage-A works whose ROR is the
# registry's ROR (WebScrape/scripts/institutes_iiit.py); None = no ROR and no OpenAlex institution (raw strings still classify)
    "iiit_agartala": {"oa": None, "ror": None, "name": "IIIT Agartala"},
    "iiit_allahabad": {"oa": "I26072440", "ror": "https://ror.org/03rgjt374", "name": "IIIT Allahabad"},
    "iiit_bangalore": {"oa": "I181514455", "ror": "https://ror.org/05h9eqy10", "name": "IIIT Bangalore"},
    "iiit_bhagalpur": {"oa": None, "ror": None, "name": "IIIT Bhagalpur"},
    "iiit_bhopal": {"oa": "I4405259253", "ror": "https://ror.org/01zhs7w23", "name": "IIIT Bhopal"},
    "iiit_bhubaneswar": {"oa": "I4210097016", "ror": "https://ror.org/00qryer39", "name": "IIIT Bhubaneswar"},
    "iiit_delhi": {"oa": "I119939252", "ror": "https://ror.org/03vfp4g33", "name": "IIIT-Delhi"},
    "iiit_dharwad": {"oa": "I4387153068", "ror": "https://ror.org/0237jt454", "name": "IIIT Dharwad"},
    "iiit_guwahati": {"oa": "I4210089896", "ror": "https://ror.org/00bb9ch64", "name": "IIIT Guwahati"},
    "iiit_gwalior": {"oa": "I9747756", "ror": "https://ror.org/008b3ap06", "name": "ABV-IIITM Gwalior"},
    "iiit_hyderabad": {"oa": "I64189192", "ror": "https://ror.org/05f11g639", "name": "IIIT Hyderabad"},
    "iiit_jabalpur": {"oa": "I207223250", "ror": "https://ror.org/00gmd7q80", "name": "IIITDM Jabalpur"},
    "iiit_kalyani": {"oa": "I4405259730", "ror": "https://ror.org/02m9zjj28", "name": "IIIT Kalyani"},
    "iiit_kancheepuram": {"oa": "I39244652", "ror": "https://ror.org/023c9pb11", "name": "IIITDM Kancheepuram"},
    "iiit_kota": {"oa": "I4405265662", "ror": "https://ror.org/05dtb1875", "name": "IIIT Kota"},
    "iiit_kottayam": {"oa": "I4405285013", "ror": "https://ror.org/04mj1ps34", "name": "IIIT Kottayam"},
    "iiit_kurnool": {"oa": "I4387155923", "ror": "https://ror.org/01kw6bd80", "name": "IIITDM Kurnool"},
    "iiit_lucknow": {"oa": "I4405256517", "ror": "https://ror.org/048m7sg95", "name": "IIIT Lucknow"},
    "iiit_manipur": {"oa": "I4210161644", "ror": "https://ror.org/052ndvg69", "name": "IIIT Manipur"},
    "iiit_nagpur": {"oa": "I4210138251", "ror": "https://ror.org/03e2e3s57", "name": "IIIT Nagpur"},
    "iiit_naya_raipur": {"oa": "I4387155265", "ror": "https://ror.org/016kfyg29", "name": "IIIT Naya Raipur"},
    "iiit_pune": {"oa": "I4210113821", "ror": "https://ror.org/01f8qyw75", "name": "IIIT Pune"},
    "iiit_raichur": {"oa": None, "ror": None, "name": "IIIT Raichur"},
    "iiit_ranchi": {"oa": "I4405284359", "ror": "https://ror.org/03desb770", "name": "IIIT Ranchi"},
    "iiit_sonepat": {"oa": "I4405255737", "ror": "https://ror.org/03c52pz66", "name": "IIIT Sonepat"},
    "iiit_sri_city": {"oa": "I4387155292", "ror": "https://ror.org/026873d40", "name": "IIIT Sri City"},
    "iiit_surat": {"oa": "I4405261310", "ror": "https://ror.org/053p6zp61", "name": "IIIT Surat"},
    "iiit_tiruchirappalli": {"oa": None, "ror": None, "name": "IIIT Tiruchirappalli"},
    "iiit_una": {"oa": "I4210127244", "ror": "https://ror.org/02z8z1589", "name": "IIIT Una"},
    "iiit_vadodara": {"oa": "I4210100893", "ror": "https://ror.org/0163rt176", "name": "IIIT Vadodara"},
}

# institutes covered by the export / network steps: ENRICH_INSTS="iit_palakkad,iit_goa" or the default pair
RUN_INSTS = [x for x in os.environ.get("ENRICH_INSTS", "iit_kharagpur,iit_roorkee").replace(" ", "").split(",") if x]

S = requests.Session()
_last = [0.0]
credits = {"used": 0, "remaining": None}


def get(path, params=None, tries=8):
    """GET an OpenAlex endpoint; returns parsed JSON, or None for a 404."""
    # OPENALEX_NO_KEY=1: use OpenAlex's free unauthenticated daily allowance (about 1,000 credits per network address, shared)
    params = dict(params or {}) if os.environ.get("OPENALEX_NO_KEY") == "1" else dict(params or {}, api_key=api_key())
    for attempt in range(tries):
        wait = 0.12 - (time.time() - _last[0])
        if wait > 0:
            time.sleep(wait)
        _last[0] = time.time()
        try:
            r = S.get(BASE + path, params=params, timeout=90)
        except requests.RequestException:
            time.sleep(2 + 3 * attempt)
            continue
        if r.headers.get("X-RateLimit-Remaining"):
            credits["remaining"] = int(r.headers["X-RateLimit-Remaining"])
        if r.status_code == 200:
            credits["used"] += 1
            return r.json()
        if r.status_code == 404:
            credits["used"] += 1
            return None
        if r.status_code == 429:
            if credits["remaining"] is not None and credits["remaining"] <= 0:
                raise SystemExit("OpenAlex daily credit budget exhausted - resume after reset")
            time.sleep(5 + 10 * attempt)
            continue
        time.sleep(2 + 3 * attempt)
    raise RuntimeError(f"OpenAlex request failed after {tries} tries: {path} {params.get('filter', '')[:120]}")


def norm_doi(d):
    if not isinstance(d, str):
        return None
    d = d.strip().lower()
    for p in ("https://doi.org/", "http://doi.org/", "https://dx.doi.org/", "doi:"):
        if d.startswith(p):
            d = d[len(p):]
    return d if d.startswith("10.") else None


def load_records(inst):
    return json.load(open(os.path.join(DATA, inst + ".json"), encoding="utf8"))["records"]


def read_jsonl(fn):
    out = []
    if os.path.exists(fn):
        with open(fn, encoding="utf8") as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        out.append(json.loads(line))
                    except json.JSONDecodeError:
                        pass  # tolerate a truncated last line after an interruption
    return out


SELECT = ("id,doi,title,publication_year,type,primary_location,authorships,referenced_works,"
          "referenced_works_count,cited_by_count,primary_topic,topics,ids")
