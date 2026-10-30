"""Shared inputs for the second-round faculty analyses (stats_coauthor_citation.py, stats_bowtie.py,
stats_cross_dept.py, stats_dept_areas.py): one table of unique papers for all institutes of the run, the faculty table, and the
faculty -> faculty citation layer.

Papers: the analysis set of both institutes (common.load_records), one entry per paper_key. 8 DOIs occur twice in the
IIT Kharagpur set (online-first year and issue year); as in results/faculty.csv the later-year record is kept (checked on
Crossref, see Dashboard/site/build_profiles.py) and the faculty of both copies are credited. A paper in both IITs' sets
is one entry with both institutes.
Faculty: the people of results/faculty.csv (1,410 for Kharagpur + Roorkee) (institution, department, roster_id). Department = faculty.csv's.
Citation layer: the 'internal' edges of citation_network.csv (a paper of our set citing another paper of our set,
from OpenAlex reference lists). Faculty a cites faculty b when a is on the citing paper and b on the cited paper, a != b.
  'pure' citation: also a is not an author of the cited paper and b is not an author of the citing paper (otherwise a
  is partly citing their own paper). Used by default, so co-authors are not counted as citing each other just because
  one of them cites a paper they wrote together."""
import os, json, collections as C
from common import INSTS, DATA, RES, CACHE, load_records, paper_key, cites, n_authors, read_csv, iter_csv


def faculty_table():
    """roster_id -> row of results/faculty.csv (institution, faculty, department, papers, h_index, ...)."""
    return {r["roster_id"]: r for r in read_csv(os.path.join(RES, "faculty.csv"))}


def paper_table():
    """paper_key -> dict(year, cites, cites_oa, insts, fac, authors, n_auth, field, subfield, topic, oa, fwci, pct)."""
    fw_fn = os.path.join(CACHE, "oa_fwci.json")
    fw = json.load(open(fw_fn, encoding="utf-8")) if os.path.exists(fw_fn) else {}
    P = {}
    for ik, name in INSTS.items():
        recs, fac = {}, C.defaultdict(set)
        for r in load_records(ik):
            k = paper_key(r)
            fac[k] |= {f["roster_id"] for f in r.get("faculty") or []}
            if k not in recs or r["year"] >= recs[k]["year"]:
                recs[k] = r
        for k, r in recs.items():
            ra = r.get("research_area") or {}
            p = P.get(k)
            if p is None:
                f = fw.get(r.get("openalex_id") or "") or {}
                p = P[k] = {"key": k, "year": r["year"], "cites": cites(r),
                            "cites_oa": r["citations_openalex"] if isinstance(r.get("citations_openalex"), int) else None,
                            "insts": set(), "fac": set(), "oa": r.get("openalex_id"), "n_auth": n_authors(r),
                            "authors": {a["openalex_author"] for a in r.get("authors_openalex") or [] if a.get("openalex_author")},
                            "field": ra.get("field") or "", "subfield": ra.get("subfield") or "", "topic": ra.get("topic") or "",
                            "type": r["type"], "title": r["title"], "fwci": f.get("fwci"), "pct": f.get("pct"),
                            "dois": set()}
            else:
                p["year"] = max(p["year"], r["year"])
            p["insts"].add(name)
            p["fac"] |= fac[k]
            if isinstance(r["doi"], str) and not r["doi"].startswith("TODO"):
                p["dois"].add(r["doi"].lower())
    return P


def citation_edges(P):
    """Unique internal citation pairs (citing key, cited key), citing != cited, both in P. Nodes of
    citation_network.csv are matched by OpenAlex id, else by DOI."""
    by_oa, by_doi = {}, {}
    for k, p in P.items():
        if p["oa"]:
            by_oa[p["oa"]] = k
        for d in p["dois"]:
            by_doi[d] = k

    def find(oa, doi):
        return by_oa.get(oa) or by_doi.get((doi or "").lower())

    E = set()
    for e in iter_csv(os.path.join(DATA, "citation_network.csv")):
        if e["edge_type"] != "internal":
            continue
        u, v = find(e["source_openalex"], e["source_doi"]), find(e["target_openalex"], e["target_doi"])
        if u and v and u != v:
            E.add((u, v))
    return E


def faculty_citations(P, E, fac_ok, pure=True):
    """List of (a, b, citing_key, cited_key, citing_year) for faculty a citing faculty b (both in fac_ok)."""
    out = []
    for u, v in E:
        fu, fv = P[u]["fac"] & fac_ok, P[v]["fac"] & fac_ok
        for a in fu:
            for b in fv:
                if a == b or (pure and (a in fv or b in fu)):
                    continue
                out.append((a, b, u, v, P[u]["year"]))
    return out


def main_subfield(P, fac_ok):
    """roster_id -> the OpenAlex subfield of most of their papers (ties: alphabetical), '' if none."""
    cnt = C.defaultdict(C.Counter)
    for p in P.values():
        if p["subfield"]:
            for a in p["fac"] & fac_ok:
                cnt[a][p["subfield"]] += 1
    return {a: min(c.items(), key=lambda x: (-x[1], x[0]))[0] for a, c in cnt.items()}
