"""Build data_v2.js for the draft multi-institute dashboard (index.html in this folder) from the tables of
Analysis/scripts (run with ANALYSIS_PROFILE=v2 -> Analysis/results_v2/). Only aggregates are written (about 1 MB):
no paper rows, no network edges. The institutes are read from the tables, so a re-run after the enrichment files are
refreshed (Analysis/scripts/run_all.sh, then this script) updates the page without any edit.
Generalises Dashboard/site/build_data.py (two institutes, one fixed list) to any number of institutes; that script and
the existing site are not touched.

Environment (all optional):
  DASH_RES       folder with the result tables      (default: Analysis/results_v2)
  DASH_ROSTERS   folder with <inst>_faculty.csv     (default: WebScrape/rosters; roster size is left out when absent)
  DASH_OUT       output file                        (default: Dashboard/site/v2/data_v2.js)
usage: python Dashboard/site/v2/build_data_v2.py"""
import os, re, csv, json, statistics, collections as C

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
RES = os.environ.get("DASH_RES") or os.path.join(REPO, "Analysis", "results_v2")
ROSTERS = os.environ.get("DASH_ROSTERS") or os.path.join(REPO, "WebScrape", "rosters")
OUT = os.environ.get("DASH_OUT") or os.path.join(HERE, "data_v2.js")
csv.field_size_limit(10 ** 8)
YEARS = list(range(2016, 2027))

# colour per institute, fixed (same as Analysis/scripts/common.py REGISTRY); other names get the spare colours
COLORS = {"IIT Kharagpur": "#2a78d6", "IIT Roorkee": "#eb6834", "IIT Bombay": "#1baf7a", "IIT Madras": "#e34948",
          "IIT Kanpur": "#6250d6", "IIT Goa": "#eda100", "IIT Tirupati": "#e87ba4", "IIT Patna": "#008300",
          "IIT Palakkad": "#0b8a9c", "IIT Guwahati": "#8a5a2b", "IIT Hyderabad": "#b44fd1", "IIT Bhubaneswar": "#3b4a6b",
          "IIT (BHU) Varanasi": "#9bbf2f", "IIT Gandhinagar": "#7a7a7a", "IIT Indore": "#d4572b", "IIT Mandi": "#4ea3c9"}
SPARE = ["#a05195", "#665191", "#2f4b7c", "#f95d6a"]
OA_NAME = {"IIT (BHU) Varanasi": "Indian Institute of Technology BHU"}      # others: 'Indian Institute of Technology X'
ROSTER_FILE = {"IIT (BHU) Varanasi": "iit_bhu"}
OUT_DEPTS = {"Academy of Classical and Folk Arts", "Centre of Excellence for Indian Knowledge Systems",
             "Centre of Excellence in Public Policy, Law and Governance", "Education", "Humanities and Social Sciences"}


def rd(name, required=True):
    fn = os.path.join(RES, name)
    if not os.path.exists(fn):
        if required:
            raise SystemExit(f"missing {fn}: run Analysis/scripts/run_all.sh with ANALYSIS_PROFILE=v2 first")
        return []
    with open(fn, encoding="utf-8-sig", newline="") as fh:
        return list(csv.DictReader(fh))


def num(x, f=float):
    try:
        v = f(x)
        return None if v != v else v
    except (TypeError, ValueError):
        return None


def r2(x, nd=2):
    v = num(x)
    return None if v is None else round(v, nd)


def group(rows, key="institution"):
    d = C.defaultdict(list)
    for r in rows:
        d[r[key]].append(r)
    return d


def roster_size(name):
    """(people listed, of them regular faculty) on the institute's pages, departments out of scope left out."""
    key = ROSTER_FILE.get(name) or "iit_" + name.replace("IIT ", "").lower().split()[0]
    fn = os.path.join(ROSTERS, key + "_faculty.csv")
    if not os.path.exists(fn):
        return None, None
    with open(fn, encoding="utf-8-sig", newline="") as fh:
        rows = [r for r in csv.DictReader(fh) if r["department"] not in OUT_DEPTS]
    return len(rows), sum(1 for r in rows if (r.get("status") or "").lower() in ("regular", "faculty", "active", ""))


def main():
    trend = group(rd("trend.csv"))
    insts = list(trend)
    spare = iter(SPARE)
    colors = {n: COLORS.get(n) or next(spare) for n in insts}
    quart, core = {r["institution"]: r for r in rd("quartiles.csv")}, {r["institution"]: r for r in rd("core_ranks.csv")}
    fac = group(rd("faculty.csv"))
    dept = group(rd("departments.csv"))
    hsum = group(rd("h_index_summary.csv"))
    csum = group(rd("core_summary.csv"))
    cvenue = group(rd("core_top_venues.csv"))
    cited = group(rd("most_cited.csv"), "scope")
    partners = group(rd("partners.csv"))
    topc = group(rd("top_collaborators.csv", False))
    cent = group(rd("faculty_centrality.csv", False))
    cnet = {r["scope"]: r for r in rd("citation_network_summary.csv")}
    cflow = {r["institution"]: r for r in rd("citation_flow_summary.csv")}
    cyear = group(rd("citation_flow_yearly.csv"))
    selfc = {r["scope"]: r for r in rd("self_citation_summary.csv", False)}
    prank = group(rd("pagerank_top10.csv"), "scope")
    areas = group(rd("research_areas.csv"))
    large = {r["institution"]: r for r in rd("large_collaborations.csv") if r["scope"] == "all years"}
    sens = defaultdict_metric(rd("large_sensitivity.csv"))
    skipped = rd("skipped_panels.csv", False)
    times = rd("run_times.csv", False)
    oa_to_name = {OA_NAME.get(n, "Indian Institute of Technology " + n.replace("IIT ", "")): n for n in insts}

    D = {"generated": "October 2026", "years": YEARS, "insts": [{"name": n, "color": colors[n]} for n in insts], "per": {}}
    for n in insts:
        t = sorted(trend[n], key=lambda r: int(r["year"]))
        by_year = {int(r["year"]): r for r in t}
        types = ["journal", "conference", "book-chapter", "preprint", "other"]
        p = {"papers": {"total": [num(by_year[y]["total"], int) if y in by_year else 0 for y in YEARS],
                        **{k: [num(by_year[y][k], int) if y in by_year else 0 for y in YEARS] for k in types}}}
        # ---- faculty
        fl = fac.get(n, [])
        hs = [int(r["h_index"]) for r in fl]
        bins = [0, 2, 5, 10, 15, 20, 30, 40, 60, 1000]
        hist = [sum(1 for h in hs if lo <= h < hi) for lo, hi in zip(bins, bins[1:])]
        hrow = {r["metric"]: r for r in hsum.get(n, []) if r["department"] == "All departments"}
        listed, regular = roster_size(n)
        hh = hrow.get("h-index", {})
        ii = hrow.get("i10-index", {})
        p["faculty"] = {
            "with_papers": len(fl), "departments": len(dept.get(n, [])), "roster_listed": listed, "roster_regular": regular,
            "h": {k: num(hh.get(k)) for k in ("n", "mean", "sd", "min", "q1", "median", "q3", "p90", "max")},
            "i10": {k: num(ii.get(k)) for k in ("mean", "median", "p90", "max")},
            "h_hist": {"edges": bins, "counts": hist},
            "top": [{"name": r["faculty"], "dept": r["department"], "h": int(r["h_index"]), "i10": int(r["i10_index"]),
                     "papers": int(r["papers"]), "citations": int(r["citations"])}
                    for r in sorted(fl, key=lambda r: (-int(r["h_index"]), -int(r["citations"])))[:10]],
            "depts": [{"name": r["department"], "faculty": int(r["faculty_with_papers"]), "papers": int(r["papers"]),
                       "citations": int(r["citations"]), "mean_h": num(r["mean_h_index"]), "median_h": num(r["median_h_index"]),
                       "max_h": num(r["max_h_index"], int)}
                      for r in sorted(dept.get(n, []), key=lambda r: -int(r["papers"]))[:12]]}
        # ---- journals: quartiles (all zero until Scimago is added) and venues
        q = quart[n]
        p["quartiles"] = {k: num(q[k], int) for k in ("journal_papers", "Q1", "Q2", "Q3", "Q4", "not_in_scimago")}
        # ---- CORE
        c = core[n]
        yr = {r["scope"]: r for r in csum.get(n, []) if not r["department"] and r["scope"] != "all years"}
        p["core"] = {"conference_papers": num(c["conference_papers"], int), "A*": num(c["A*"], int), "A": num(c["A"], int),
                     "B": num(c["B"], int), "C": num(c["C"], int), "not_ranked": num(c["not_core_ranked"], int),
                     "by_year": {k: [num(yr[str(y)][k], int) if str(y) in yr else 0 for y in YEARS]
                                 for k in ("conference_papers", "A*", "A", "B", "C")},
                     "top_venues": [{"venue": r["conference"], "rank": r["core_rank"], "papers": int(r["papers"])}
                                    for r in sorted(cvenue.get(n, []), key=lambda r: int(r["rank_by_papers"]))[:10]]}
        # ---- top papers
        p["top_papers"] = [{"title": r["title"], "journal": r["journal"], "year": int(r["year"]), "citations": int(r["citations"]),
                            "doi": r["doi"], "insts": r["institutions"]}
                           for r in sorted(cited.get(n, []), key=lambda r: int(r["rank"]))]
        # ---- partners (Indian institutions) and faculty collaborators
        pl = sorted(partners.get(n, []), key=lambda r: int(r["rank_by_shared_papers"]))
        p["partners"] = [{"name": r["partner"], "shared": int(r["shared_papers"]), "cites_from": int(r["citations_from_partner"]),
                          "cites_to": int(r["citations_to_partner"]), "cluster": r["cluster"]} for r in pl[:15]]
        cl = C.Counter()
        for r in pl:
            cl[r["cluster"]] += int(r["shared_papers"])
        p["partner_clusters"] = [{"cluster": k, "shared": v} for k, v in cl.most_common()]
        p["collaborators"] = [{"name": r["faculty"], "dept": r["department"], "faculty_coauthors": int(r["faculty_coauthors"]),
                               "joint_papers": int(r["joint_papers_with_faculty"]), "betweenness": r2(r["betweenness"], 4)}
                              for r in topc.get(n, [])[:10]]
        # ---- networks
        ce = cnet.get(n, {})
        fl_ = cflow.get(n, {})
        sc = selfc.get(n, {})
        cr = sorted(cent.get(n, []), key=lambda r: -int(r["faculty_coauthors"]))
        deg = [int(r["faculty_coauthors"]) for r in cr]
        p["network"] = {
            "citation": {"papers": num(ce.get("papers"), int), "edges": num(ce.get("citation_edges"), int),
                         "mean_in_degree": num(ce.get("mean_in_degree")), "cited_once": num(ce.get("papers_cited_at_least_once"), int),
                         "citing_none": num(ce.get("papers_citing_none_in_corpus"), int),
                         "largest_component": num(ce.get("largest_weak_component"), int), "reciprocal_pairs": num(ce.get("reciprocal_pairs"), int),
                         "pagerank_vs_year": num(ce.get("spearman_pagerank_vs_year")),
                         "self_share": num(sc.get("self_share")), "self_citations": num(sc.get("self_citations"), int)},
            "flow": {"in": num(fl_.get("in_flow"), int), "out": num(fl_.get("out_flow"), int), "ratio": num(fl_.get("impact_ratio_in_over_out"))},
            "flow_yearly": {"in": [num(next((r["in_flow"] for r in cyear.get(n, []) if int(r["year"]) == y), 0), int) for y in YEARS],
                            "out": [num(next((r["out_flow"] for r in cyear.get(n, []) if int(r["year"]) == y), 0), int) for y in YEARS]},
            "pagerank": [{"title": r["title"], "year": int(r["year"]), "journal": r["journal"], "in_degree": int(r["in_degree"]),
                          "citations": num(r["global_citations"], int), "doi": r["doi"]}
                         for r in sorted(prank.get(n, []), key=lambda r: int(r["rank"]))[:5]],
            "faculty_net": {"nodes": len(deg), "with_tie": sum(1 for d in deg if d), "mean_ties": round(statistics.mean(deg), 2) if deg else None,
                            "max_ties": max(deg) if deg else None, "communities": len({r["community"] for r in cr})}}
        # ---- research areas, big teams
        p["areas"] = [{"field": r["field"], "papers": int(r["papers"]), "share": num(r["share"])}
                      for r in sorted(areas.get(n, []), key=lambda r: -int(r["papers"]))[:8]]
        lg = large.get(n, {})
        p["large"] = {"more_than_10": num(lg.get("more_than_10_authors"), int), "share": num(lg.get("share")),
                      "with_100_plus": num(lg.get("with_100_or_more"), int)}
        sn = sens.get(n, {})
        p["headline"] = {"papers": num(sn.get("papers"), int), "citations": num(sn.get("citations"), int),
                         "citations_per_paper": num(sn.get("citations per paper")), "median_citations": num(sn.get("median citations per paper")),
                         "papers_100": num(sn.get("papers with >= 100 citations"), int), "institute_h": num(sn.get("institute h-index"), int)}
        D["per"][n] = p
    # ---- shared papers between the institutes (from the partner tables: a partner that is one of the institutes)
    idx = {n: i for i, n in enumerate(insts)}
    M = [[0] * len(insts) for _ in insts]
    for n in insts:
        for r in partners.get(n, []):
            m = oa_to_name.get(r["partner"])
            if m and m != n:
                M[idx[n]][idx[m]] = int(r["shared_papers"])
    D["shared_matrix"] = M
    D["skipped"] = [{"panel": r["panel"], "script": r["script"], "reason": r["reason"], "needs": r["needs"]} for r in skipped]
    D["run_times"] = [{"script": r["script"], "seconds": num(r["seconds"], int), "memory_mb": num(r["peak_memory_mb"], int),
                       "exit": num(r["exit_code"], int)} for r in times]
    D["cluster_net"] = {k: {kk: num(vv) if kk != "scope" and kk != "density" else vv for kk, vv in v.items()} for k, v in cnet.items()
                        if k not in insts}
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write("window.DASH_V2 = " + json.dumps(D, ensure_ascii=False, separators=(",", ":")) + ";\n")
    print(f"{OUT}: {os.path.getsize(OUT) / 1e6:.2f} MB, {len(insts)} institutes")


def defaultdict_metric(rows):
    """large_sensitivity.csv: institution -> {metric: all_papers value}."""
    d = C.defaultdict(dict)
    for r in rows:
        d[r["institution"]][r["metric"]] = r["all_papers"]
    return d


if __name__ == "__main__":
    main()
