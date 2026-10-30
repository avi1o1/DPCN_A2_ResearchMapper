"""IIIT Hyderabad's own publication repository as a discovery channel (IIIT team, PROCESS_IIIT.md §7.4).

Why: the institute keeps an official repository of its publications (https://www.iiit.ac.in/publications/index.php,
6,678 items on 2026-10-30) that faculty report into. The operator decided (2026-10-30) to add every repository item to
the IIIT Hyderabad dataset without a tenure filter or audit ("it's all official"). Items enter as person-channel records
with evidence `institute_list`, so finalize.py puts them in the main file as `unverified-likely` unless publisher metadata
contradicts them. Items whose affiliation is printed are `verified` through the normal channels anyway.
CAUTION: the IIIT Hyderabad golden set took 260 of its 322 papers from this repository (per-faculty listings), so recall
measured after this channel is no longer an independent check; the independent figure is the one before (§6).

Fetching: the page's own AJAX paging (POST page=N&ajax=1, as its JavaScript does), 1 request/s; robots.txt allows
/publications/. Pages are cached under raw/iiith_publist/pages/.
Output: raw/roster/iiit_hyderabad_publist.jsonl.gz (read by build_candidates.py like the other roster channels).
usage: python3 iiith_publist.py [--no-fetch]
"""
import os, re, sys, csv, json, glob, html, time, unicodedata
import requests
from common import RAW, ROOT, MAILTO, write_jsonl_gz, norm_doi

INST = "iiit_hyderabad"
URL = "https://www.iiit.ac.in/publications/index.php"
D = os.path.join(RAW, "iiith_publist", "pages")
os.makedirs(D, exist_ok=True)


def fetch():
    s = requests.Session()
    s.headers.update({"User-Agent": f"DPCN-ResearchMapper/1.0 (IIIT Hyderabad course project; mailto:{MAILTO})",
                      "X-Requested-With": "XMLHttpRequest", "Referer": URL})
    form = {"ajax": "1", "stitle": "", "sauthor": "", "sconfname": "", "sacronym": "", "spyear": "", "sconftype": ""}
    p, last = 1, None
    while last is None or p <= last:
        fn = os.path.join(D, f"{p}.json")
        if not os.path.exists(fn):
            for a in range(5):
                try:
                    r = s.post(URL, data={**form, "page": p}, timeout=60)
                    if r.status_code == 200 and r.text.lstrip().startswith("{"):
                        open(fn, "w", encoding="utf-8").write(r.text); break
                    print(p, "status", r.status_code, flush=True)
                except requests.RequestException as e:
                    print(p, "error", e, flush=True)
                time.sleep(5 * (a + 1))
            time.sleep(1.0)
        if last is None and os.path.exists(fn):
            pg = json.load(open(fn, encoding="utf-8")).get("pagination", "")
            last = max([int(x) for x in re.findall(r"data-page='(\d+)'", pg)] + [1])
        p += 1


def parse():
    out, seen = [], set()
    for fn in sorted(glob.glob(os.path.join(D, "*.json")), key=lambda f: int(os.path.basename(f)[:-5])):
        for c in json.load(open(fn, encoding="utf-8"))["cards"].split('<div class="card">')[1:]:
            c = re.sub(r"\s+", " ", c)
            g = lambda rx: (lambda m: html.unescape(m.group(1)).strip() if m else "")(re.search(rx, c))
            iid = g(r'id="AbsModal(\d+)"') or g(r'toggleDispl\("(\d+)"\)')
            if not iid or iid in seen:
                continue
            seen.add(iid)
            about = g(r'<div class="about-publication">(.*?)<div class="special">')
            m = re.match(r"(.*?),\s*([^,]*),\s*(\d{4})\s*$", about)
            by = g(r"YEAR = \{(\d{4})\}")
            year = int(m.group(3)) if m else (int(by) if by else None)
            link = g(r'<a href="([^"]+)" target="_blank" class="alink"><span class="article-btn">DOI</span>')
            dm = re.search(r"(10\.\d{4,9}/[^\s\"'<>]+)", link)
            out.append({"id": iid, "title": re.sub(r"<[^>]+>", "", g(r'<div class="publication-title">(.*?)</div>')),
                        "authors": [a.strip() for a in g(r'<div class="author"><em>(.*?)</em>').split(",") if a.strip()],
                        "venue": m.group(1).strip() if m else about, "year": year, "link": link,
                        "doi": norm_doi(dm.group(1).rstrip(".")) if dm else None})
    return out


def key(n):
    n = unicodedata.normalize("NFKD", n).encode("ascii", "ignore").decode().lower()
    return " ".join(t for t in re.split(r"[\s.]+", re.sub(r"^(prof|dr|mr|ms|mrs)\.?\s+", "", n)) if len(t) > 1)


if "--no-fetch" not in sys.argv:
    fetch()
items = parse()
roster = list(csv.DictReader(open(os.path.join(ROOT, "rosters", f"{INST}_faculty.csv"), encoding="utf-8-sig")))
RK = {key(r["name"]): r for r in roster}
rows, nperson = [], 0
for it in items:
    if not it["year"] or not it["title"]:
        continue
    hit = next((RK[key(a)] for a in it["authors"] if key(a) in RK), None)
    nperson += bool(hit)
    person = f"{hit['name']} [roster:{hit.get('department', '')}]" if hit else (it["authors"][0] if it["authors"] else "IIIT Hyderabad repository")
    rows.append({"doi": it["doi"], "title": it["title"], "year": it["year"], "channel": "institute_list", "person": person,
                 "why": f"listed in the IIIT Hyderabad publication repository (item {it['id']}; {it['venue'][:80]})"})
write_jsonl_gz(os.path.join(RAW, "roster", f"{INST}_publist.jsonl.gz"), rows)
print(len(items), "items;", len(rows), "written;", sum(1 for r in rows if r["doi"]), "with a DOI;", nperson, "matched to a roster person;",
      sum(1 for r in rows if 2016 <= r["year"] <= 2026), "in 2016-2026", flush=True)
