"""Build profiles.js for the dashboard's profile explorer (a per-institute / department / faculty view with a year range,
modelled on the Power BI dashboard of J. F. F. Mendes's research page: KPI tiles, papers and citations per year, type and
quartile mix, top journals / topics / co-authors, and an ego co-authorship network).

Same paper set and definitions as the statistics (Analysis/scripts/common.py): the analysis set (verified affiliation,
science & engineering scope), citations = Crossref-led count (`cites`), h-index / i10-index helpers, a faculty member's
papers = the unique papers that list them in `faculty`. The script checks itself: for every faculty member it recomputes
papers, citations, h-index, i10-index and Q1 papers from the table it wrote and stops unless all equal results/faculty.csv.

Per paper: year, citations, quartile, type, venue, OpenAlex field / topic, number of authors (OpenAlex lists at most 100),
FWCI and citation percentile (Analysis/cache/oa_fwci.json, fetch_openalex_extra.py), citations received per year
2016–2026 (oa_counts_by_year.json), co-author institutions (OpenAlex ids), author list (OpenAlex author ids, else the name).
Per faculty paper: the author position of that faculty member, found by name compatibility (Enrichment/scripts/faculty.py)
among the authors OpenAlex marks as institute authors, then among all; ambiguous or unmatched -> unknown (never guessed).
usage: python Dashboard/site/build_profiles.py      (offline; re-run after the statistics and fetch_openalex_extra.py)"""
import os, sys, json, collections as C

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(REPO, "Analysis", "scripts"))
sys.path.insert(0, os.path.join(REPO, "Enrichment", "scripts"))
from common import INSTS, YEARS, RES, CACHE, load_records, paper_key, cites, n_authors, h_index, i10_index, read_csv  # noqa: E402
from faculty import compatible  # noqa: E402

POS = {"middle": 0, "first": 1, "last": 2, "sole": 3, "unknown": -1}


def load_json(name):
    fn = os.path.join(CACHE, name)
    return json.load(open(fn, encoding="utf-8")) if os.path.exists(fn) else {}


class Index(list):
    """Value -> small integer, so repeated strings are stored once."""
    def __init__(self):
        super().__init__()
        self.pos = {}

    def __call__(self, v):
        if v not in self.pos:
            self.pos[v] = len(self)
            self.append(v)
        return self.pos[v]


def position(r, fac_name):
    """Author position of a faculty member on a paper, or 'unknown' (never guessed)."""
    au = r.get("authors_openalex") or []
    if not au:
        return "unknown", None
    hits = [i for i, a in enumerate(au) if a.get("institute_author") and compatible(a.get("name", ""), fac_name)]
    if not hits:
        hits = [i for i, a in enumerate(au) if compatible(a.get("name", ""), fac_name)]
    if len(hits) != 1:
        return "unknown", None
    i, n = hits[0], len(au)
    if n == 1:
        return "sole", i
    if i == 0:
        return "first", i
    if i == n - 1 and n < 100:              # OpenAlex lists at most 100 authors: the 100th need not be the last
        return "last", i
    return "middle", i


def main():
    fw, cby = load_json("oa_fwci.json"), load_json("oa_counts_by_year.json")
    venues, fields, topics, types, insts, authors = Index(), Index(), Index(), Index(), Index(), Index()
    papers, pidx = [], {}
    fac = {}                                                  # (inst, roster_id) -> {...}
    for ik, iname in INSTS.items():
        bit = 1 << list(INSTS).index(ik)
        # 8 DOIs occur twice in the IIT Kharagpur set (online-first year and issue year, different citation counts).
        # Checked against Crossref on 2026-10-27: in all 8 the later-year record carries Crossref's issued year and
        # citation count, and it is the one results/faculty.csv keeps. Keep it; credit the faculty of both copies.
        recs, extra_fac = {}, C.defaultdict(list)
        for r in load_records(ik):
            k = paper_key(r)
            extra_fac[k].extend(r.get("faculty") or [])
            if k not in recs or r["year"] >= recs[k]["year"]:
                recs[k] = r
        for k, r in recs.items():
            r = dict(r, faculty=extra_fac[k])
            if k in pidx:
                p = papers[pidx[k]]
                p["h"] |= bit
            else:
                ra = r.get("research_area") or {}
                wid = r.get("openalex_id")
                f = fw.get(wid) or {}
                yc = cby.get(wid) or {}
                q = ((r.get("quartile") or {}).get("quartile") or "")
                au = r.get("authors_openalex") or []
                cy = [int(yc.get(str(y), 0)) for y in YEARS] if yc else None
                p = {"t": r["title"],
                     "doi": r["doi"].replace("https://doi.org/", "") if isinstance(r["doi"], str) and not r["doi"].startswith("TODO") else "",
                     "y": r["year"], "c": cites(r), "q": int(q[1]) if q[:1] == "Q" and q[1:].isdigit() else 0,
                     "ty": types(r["type"]),
                     "v": venues(r["venue"]) if r.get("venue") and not str(r["venue"]).startswith("TODO") else -1,
                     "f": fields(ra["field"]) if ra.get("field") else -1,
                     "tp": topics(ra["topic"]) if ra.get("topic") else -1,
                     "n": n_authors(r) or 0,
                     "fw": None if f.get("fwci") is None else round(f["fwci"], 2),
                     "pc": None if f.get("pct") is None else round(f["pct"], 3),
                     "cy": cy if cy and any(cy) else (cy and 0),   # 0 = OpenAlex has the work, no citations 2016-26

                     "in": sorted({insts(i["name"]) for i in r.get("coauthor_institutions") or [] if i.get("name")}),
                     "au": [authors(a.get("openalex_author") or "n:" + a.get("name", "?")) for a in au],
                     "an": [a.get("name", "") for a in au],
                     "h": bit}
                pidx[k] = len(papers)
                papers.append(p)
            i = pidx[k]
            for f_ in r.get("faculty") or []:
                key = (iname, f_["roster_id"])
                d = fac.setdefault(key, {"name": f_["name"], "dept": f_["department"], "inst": iname, "rid": f_["roster_id"],
                                         "p": {}})
                if i not in d["p"]:
                    pos, ai = position(r, f_["name"])
                    d["p"][i] = (POS[pos], ai)
    # author display names: the most common printed form of each id
    names = C.defaultdict(C.Counter)
    for p in papers:
        for a, nm in zip(p["au"], p["an"]):
            names[a][nm] += 1
    author_names = [names[i].most_common(1)[0][0] if names[i] else a for i, a in enumerate(authors)]

    # ---------------------------------------------------------------- self-check against results/faculty.csv
    ref = {(r["institution"], r["roster_id"]): r for r in read_csv(os.path.join(RES, "faculty.csv"))}
    bad = []
    for key, d in fac.items():
        ps = [papers[i] for i in d["p"]]
        cs = [p["c"] for p in ps]
        got = {"papers": len(ps), "citations": sum(c for c in cs if c is not None), "h_index": h_index(cs),
               "i10_index": i10_index(cs), "q1_papers": sum(1 for p in ps if p["q"] == 1)}
        want = ref.get(key)
        if want is None or any(str(got[c]) != str(want[c]) for c in got):
            bad.append((key, got, {c: want[c] for c in got} if want else None))
    missing = set(ref) - set(fac)
    print(f"faculty: {len(fac)} built, {len(ref)} in faculty.csv; mismatches {len(bad)}, missing {len(missing)}")
    for b in bad[:10]:
        print("  MISMATCH", b)
    if bad or missing:
        raise SystemExit("profiles do not agree with results/faculty.csv — not written")

    # ---------------------------------------------------------------- compact output
    cols = ["t", "doi", "y", "c", "q", "ty", "v", "f", "tp", "n", "fw", "pc", "cy", "in", "au", "h"]
    out = {"years": YEARS, "insts": list(INSTS.values()), "types": types, "venues": venues, "fields": fields,
           "topics": topics, "coinst": insts, "authors": author_names, "cols": cols,
           "papers": [[p[c] for c in cols] for p in papers],
           "faculty": [{"n": d["name"], "d": d["dept"], "i": d["inst"], "rid": d["rid"],
                        "p": [[i, pos, -1 if ai is None else ai] for i, (pos, ai) in sorted(d["p"].items())]}
                       for d in sorted(fac.values(), key=lambda d: (d["inst"], d["dept"], d["name"]))],
           "notes": {"fwci_papers": sum(1 for p in papers if p["fw"] is not None),
                     "cby_papers": sum(1 for p in papers if p["cy"]), "positions_known":
                     sum(1 for d in fac.values() for pos, _ in d["p"].values() if pos >= 0),
                     "positions_total": sum(len(d["p"]) for d in fac.values())}}
    fn = os.path.join(HERE, "profiles.js")
    with open(fn, "w", encoding="utf-8") as fh:
        fh.write("window.PROF = ")
        json.dump(out, fh, ensure_ascii=False, separators=(",", ":"))
        fh.write(";\n")
    print(f"wrote {fn}: {len(papers)} papers, {len(fac)} faculty, {len(author_names)} authors, "
          f"{os.path.getsize(fn) / 1e6:.1f} MB; notes {out['notes']}")


if __name__ == "__main__":
    main()
