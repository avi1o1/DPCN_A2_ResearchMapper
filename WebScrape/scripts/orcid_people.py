"""Channel B1: ORCID person channel.

1. Search ORCID for profiles whose affiliations mention the institute (name token OR ROR id).
2. Fetch each public record; keep affiliation entries (employment/education/qualification/
   invited-position) that are *this* IIT (name must contain the city token AND IIT/'Indian
   Institute of Technology', or carry the institute's ROR/GRID/Ringgold id).
3. Save person + tenure windows + work summaries to WebScrape/raw/orcid/<inst>.jsonl.gz.
Filtering of works by tenure window happens in the merge step (documented there).

usage: python3 orcid_people.py <inst_key>
"""
import os, re, sys, json, threading, queue, time
from common import get, RAW, LOGS, write_jsonl_gz
from institutes import REG

IIT = re.compile(r"\biit\b|indian institute of technology|iitkgp|iit-?kgp|iit\s*rpr", re.I)
CFG = {k: {"q": v["orcid_q"], "city": re.compile(v["orcid_city"], re.I), "ids": {v["ror"], v["grid"]},
          "units": re.compile(v["units"], re.I), "mention": re.compile(v["mention"], re.I) if v.get("mention") else IIT}
       for k, v in REG.items()}
H = {"Accept": "application/json"}
inst = sys.argv[1]; cfg = CFG[inst]

# 1. search. The ORCID search API pages only through the first 10,000 hits (IIT Madras has more): a larger result set is
# split by the first letter of the family name (plus a remainder query), and the union is checked against the total.
def search(q):
    out, start = [], 0
    while True:
        d = get("https://pub.orcid.org/v3.0/search/", params={"q": q, "rows": 1000, "start": start}, headers=H).json()
        res = d.get("result") or []
        out += [r["orcid-identifier"]["path"] for r in res]
        start += 1000
        if start >= d["num-found"] or not res or start >= 10000:
            return out, d["num-found"]


ids, total = search(cfg["q"])
if total > 10000:
    ids = []
    letters = "abcdefghijklmnopqrstuvwxyz"
    for c in letters:
        part, n = search(f"({cfg['q']}) AND family-name:{c}*")
        assert n <= 10000, f"partition {c} still has {n} hits"
        ids += part
    rest, n = search(f"({cfg['q']}) AND NOT (" + " OR ".join(f"family-name:{c}*" for c in letters) + ")")
    ids += rest
ids = sorted(set(ids))
print(inst, "profiles:", len(ids), "reported total:", total, flush=True)
if len(ids) < total:
    print(inst, "WARNING: partitioned search covers", len(ids), "of", total, flush=True)


def yr(dt):
    try:
        return int(dt["year"]["value"])
    except Exception:
        return None


def matches(org):
    name = org.get("name", "")
    did = (org.get("disambiguated-organization") or {}).get("disambiguated-organization-identifier", "")
    return (cfg["city"].search(name) and cfg["mention"].search(name)) or did in cfg["ids"] or bool(cfg["units"].search(name))


def parse(orcid, rec):
    a = rec.get("activities-summary") or {}
    tenures = []
    for sec, key in (("employments", "employment-summary"), ("educations", "education-summary"),
                     ("qualifications", "qualification-summary"), ("invited-positions", "invited-position-summary")):
        for g in (a.get(sec) or {}).get("affiliation-group", []):
            for s in g.get("summaries", []):
                e = s.get(key) or {}
                org = e.get("organization") or {}
                if matches(org):
                    tenures.append({"kind": sec, "org": org.get("name"), "dept": e.get("department-name"),
                                    "role": e.get("role-title"), "start": yr(e.get("start-date")), "end": yr(e.get("end-date"))})
    works = []
    for g in (a.get("works") or {}).get("group", []):
        s = g["work-summary"][0]
        ext = {}
        for x in (g.get("external-ids") or {}).get("external-id", []):
            ext.setdefault(x["external-id-type"], x["external-id-value"])
        works.append({"title": ((s.get("title") or {}).get("title") or {}).get("value"),
                      "year": yr(s.get("publication-date")), "type": s.get("type"),
                      "journal": (s.get("journal-title") or {}).get("value"), "ext": ext,
                      "source": ((s.get("source") or {}).get("source-name") or {}).get("value")})
    p = (rec.get("person") or {}).get("name") or {}
    name = " ".join(filter(None, [((p.get("given-names") or {}).get("value")), ((p.get("family-name") or {}).get("value"))]))
    return {"orcid": orcid, "name": name, "tenures": tenures, "works": works}


# checkpoint (v2): every fetched profile is appended to <inst>.part.jsonl, so a restart after a hang (2026-10-25: a suspend
# left all workers blocked) resumes instead of refetching; failed fetches are not checkpointed and are retried
os.makedirs(os.path.join(RAW, "orcid"), exist_ok=True)
PART = os.path.join(RAW, "orcid", inst + ".part.jsonl")
q, out, lock = queue.Queue(), [], threading.Lock()
if os.path.exists(PART):
    for line in open(PART, encoding="utf-8"):
        try:
            out.append(json.loads(line))
        except json.JSONDecodeError:
            pass   # truncated last line
done_ids = {r["orcid"] for r in out}
print(inst, "resumed from checkpoint:", len(done_ids), flush=True)
for i in ids:
    if i not in done_ids:
        q.put(i)
cp = open(PART, "a", encoding="utf-8")


def worker():
    while True:
        try:
            o = q.get_nowait()
        except queue.Empty:
            return
        try:
            r = get(f"https://pub.orcid.org/v3.0/{o}/record", headers=H)
            row = parse(o, r.json()) if r.status_code == 200 else {"orcid": o, "error": r.status_code}
        except Exception as e:
            row = {"orcid": o, "error": str(e)}
        with lock:
            out.append(row)
            if "error" not in row:
                cp.write(json.dumps(row, ensure_ascii=False) + "\n"); cp.flush()
            if len(out) % 250 == 0:
                print(inst, len(out), "/", len(ids), flush=True)
        time.sleep(0.5)


ts = [threading.Thread(target=worker) for _ in range(6)]
[t.start() for t in ts]; [t.join() for t in ts]
cp.close()
write_jsonl_gz(os.path.join(RAW, "orcid", inst + ".jsonl.gz"), out)
os.remove(PART)
nt = sum(1 for r in out if r.get("tenures"))
with open(os.path.join(LOGS, "orcid_runs.tsv"), "a") as lg:
    lg.write(f"{inst}\t{cfg['q']}\tprofiles={len(ids)}\twith_matching_tenure={nt}\terrors={sum(1 for r in out if 'error' in r)}\n")
print("done", inst, len(out), "with tenure", nt)
