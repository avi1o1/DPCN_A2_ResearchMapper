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
  DASH_PARTIAL   comma list of institute keys (bombay,madras,...) whose enrichment is still partial: the page shows a
                 'partial enrichment' badge for them (default: PARTIAL_DEFAULT below; set to '' once they are complete)
usage: python Dashboard/site/v2/build_data_v2.py"""
import os, re, csv, json, statistics, collections as C

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
RES = os.environ.get("DASH_RES") or os.path.join(REPO, "Analysis", "results_v2")
ROSTERS = os.environ.get("DASH_ROSTERS") or os.path.join(REPO, "WebScrape", "rosters")
OUT = os.environ.get("DASH_OUT") or os.path.join(HERE, "data_v2.js")
csv.field_size_limit(10 ** 8)
YEARS = list(range(2016, 2027))

# institute -> (registry key, OpenAlex name, colour), the same as REGISTRY in Analysis/scripts/common.py (colour fixed per institute,
# never by rank). An institute missing here gets a spare colour and generic names.
REG = {"IIT Kharagpur": ("iit_kharagpur", "Indian Institute of Technology Kharagpur", "#2a78d6"),
       "IIT Roorkee": ("iit_roorkee", "Indian Institute of Technology Roorkee", "#eb6834"),
       "IIT Ropar": ("iit_ropar", "Indian Institute of Technology Ropar", "#8a6bbf"),
       "IIT Bombay": ("iit_bombay", "Indian Institute of Technology Bombay", "#1baf7a"),
       "IIT Madras": ("iit_madras", "Indian Institute of Technology Madras", "#e34948"),
       "IIT Kanpur": ("iit_kanpur", "Indian Institute of Technology Kanpur", "#6250d6"),
       "IIT Goa": ("iit_goa", "Indian Institute of Technology Goa", "#eda100"),
       "IIT Tirupati": ("iit_tirupati", "Indian Institute of Technology Tirupati", "#e87ba4"),
       "IIT Patna": ("iit_patna", "Indian Institute of Technology Patna", "#008300"),
       "IIT Palakkad": ("iit_palakkad", "Indian Institute of Technology Palakkad", "#0b8a9c"),
       "IIT Guwahati": ("iit_guwahati", "Indian Institute of Technology Guwahati", "#8a5a2b"),
       "IIT Hyderabad": ("iit_hyderabad", "Indian Institute of Technology Hyderabad", "#b44fd1"),
       "IIT Bhubaneswar": ("iit_bhubaneswar", "Indian Institute of Technology Bhubaneswar", "#3b4a6b"),
       "IIT (BHU) Varanasi": ("iit_bhu", "Indian Institute of Technology BHU", "#9bbf2f"),
       "IIT Gandhinagar": ("iit_gandhinagar", "Indian Institute of Technology Gandhinagar", "#7a7a7a"),
       "IIT Indore": ("iit_indore", "Indian Institute of Technology Indore", "#d4572b"),
       "IIT Mandi": ("iit_mandi", "Indian Institute of Technology Mandi", "#4ea3c9"),
       "IIT Delhi": ("iit_delhi", "Indian Institute of Technology Delhi", "#a05195"),
       "IIT (ISM) Dhanbad": ("iit_ism", "Indian Institute of Technology Dhanbad", "#665191"),
       "IIT Jodhpur": ("iit_jodhpur", "Indian Institute of Technology Jodhpur", "#f95d6a"),
       "IIT Jammu": ("iit_jammu", "Indian Institute of Technology Jammu", "#2f4b7c"),
       "IIT Bhilai": ("iit_bhilai", "Indian Institute of Technology Bhilai", "#ff7c43"),
       "IIT Dharwad": ("iit_dharwad", "Indian Institute of Technology Dharwad", "#00876c")}
SPARE = ["#b5651d", "#5f9ea0", "#c71585", "#556b2f"]
# interim set of 31 October 2026: these six lack the complete Indian-citation steps and the title search (OpenAlex credits ran out)
PARTIAL_DEFAULT = "bombay,madras,kanpur,guwahati,delhi,ropar"
PARTIAL = {"iit_" + k.strip() for k in (os.environ["DASH_PARTIAL"] if "DASH_PARTIAL" in os.environ else PARTIAL_DEFAULT).split(",") if k.strip()}
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


def key_of(name):
    return REG[name][0] if name in REG else "iit_" + name.replace("IIT ", "").lower().split()[0]


def roster_size(name):
    """(people listed, of them regular faculty) on the institute's pages, departments out of scope left out."""
    key = key_of(name)
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
    colors = {n: REG[n][2] if n in REG else next(spare) for n in insts}
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
    oa_to_name = {(REG[n][1] if n in REG else "Indian Institute of Technology " + n.replace("IIT ", "")): n for n in insts}
    mega_i = {r["institution"]: r for r in rd("mega_by_institute.csv", False)}
    mega_ww = defaultdict_ww(rd("mega_with_without.csv", False))
    mega_rk = C.defaultdict(dict)
    for r in rd("mega_ranks.csv", False):
        mega_rk[r["institution"]][r["metric"]] = r
    cohort = {r["institution"]: r for r in rd("faculty_cohort.csv", False)}
    compl = {r["institution"]: r for r in rd("roster_completeness.csv", False)}

    D = {"generated": "31 October 2026", "years": YEARS,
         "insts": [{"name": n, "key": key_of(n), "color": colors[n], "partial": key_of(n) in PARTIAL} for n in insts], "per": {}}
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
            "with_papers": len(fl), "departments": len(dept.get(n, [])), "roster_listed": listed,
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
        # ---- sanity audit F3: > 100-author (mega-collaboration) papers, every statistic with and without them
        mi = mega_i.get(n, {})
        ww = mega_ww.get(n, {})
        p["mega"] = {"papers": num(mi.get("mega_papers"), int), "share_papers": num(mi.get("mega_share_of_papers")),
                     "share_citations": num(mi.get("mega_share_of_citations")), "unknown_flags": num(mi.get("flag_unknown"), int),
                     "top_person": mi.get("person_with_most_mega_papers") or None,
                     "metrics": {k: {"all": num(v["all_papers"]), "without": num(v["without_mega"]), "change_pct": num(v["change_pct"])}
                                 for k, v in ww.items()},
                     "ranks": {k: {"all": num(v["rank_all"], int), "without": num(v["rank_without_mega"], int),
                                   "change": num(v["rank_change"], int)} for k, v in mega_rk.get(n, {}).items()}}
        # ---- sanity audit F4: cohort of current faculty with joining year <= 2017, roster completeness against NIRF
        co, rc = cohort.get(n, {}), compl.get(n, {})
        p["cohort"] = {"size": num(co.get("cohort_size"), int), "with_papers": num(co.get("cohort_with_papers"), int),
                       "mean_papers": num(co.get("cohort_mean_papers")), "median_papers": num(co.get("cohort_median_papers")),
                       "median_citations": num(co.get("cohort_median_citations")), "median_h": num(co.get("cohort_median_h")),
                       "mean_h": num(co.get("cohort_mean_h")), "current": num(co.get("all_current_in_scope"), int),
                       "current_with_papers": num(co.get("all_current_with_papers"), int),
                       "current_mean_papers": num(co.get("all_current_mean_papers")), "current_median_h": num(co.get("all_current_median_h")),
                       "published_median_h": num(co.get("published_median_h_faculty_with_papers")),
                       "rank": num(co.get("rank_mean_papers_among_cohorts_of_20plus"), int), "warning": co.get("warning") or None,
                       "roster_rows": num(rc.get("roster_rows"), int), "roster_current": num(rc.get("current_rows"), int),
                       "with_joining_year": num(rc.get("share_current_with_joining_year")), "nirf_edition": rc.get("nirf_edition") or None,
                       "nirf_count": num(rc.get("nirf_regular") or rc.get("nirf_working"), int),
                       "current_over_nirf": num(rc.get("current_over_nirf")), "roster_flag": rc.get("flag") or None}
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
    D["partial_note"] = ("The Indian-citation steps (which Indian institutions cite and are cited by each paper) and the OpenAlex "
                         "title search are not complete yet because the OpenAlex credits ran out; they complete after about 05:30 on "
                         "1 November 2026. Paper, faculty, journal and conference numbers are usable, but citation-flow, partner and "
                         "network figures can change, a few papers found only by title search are still missing, and OpenAlex "
                         "research-area data can be absent (IIT Ropar has none yet).")
    D["cluster_net"] = {k: {kk: num(vv) if kk != "scope" and kk != "density" else vv for kk, vv in v.items()} for k, v in cnet.items()
                        if k not in insts}
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write("window.DASH_V2 = " + json.dumps(D, ensure_ascii=False, separators=(",", ":")) + ";\n")
    print(f"{OUT}: {os.path.getsize(OUT) / 1e6:.2f} MB, {len(insts)} institutes")


def defaultdict_ww(rows):
    """mega_with_without.csv: institution -> {metric: row}."""
    d = C.defaultdict(dict)
    for r in rows:
        d[r["institution"]][r["metric"]] = r
    return d


def defaultdict_metric(rows):
    """large_sensitivity.csv: institution -> {metric: all_papers value}."""
    d = C.defaultdict(dict)
    for r in rows:
        d[r["institution"]][r["metric"]] = r["all_papers"]
    return d


if __name__ == "__main__":
    main()
