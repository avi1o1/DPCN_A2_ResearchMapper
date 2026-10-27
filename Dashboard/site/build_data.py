"""Build data.js for the static dashboard (index.html) from the computed statistics.
Reads Analysis/results/*.csv (small) and, for the two network panels and paper titles, Enrichment/out/
(citation_network.csv, authorship_network.csv, group3_data.csv). Graph layouts are precomputed here with networkx so
the browser only draws. Output: data.js (window.DASH = {...}), loaded by index.html. No network access, no API key.
usage: python Dashboard/site/build_data.py   (re-run after Analysis/scripts/run_all.sh)"""
import os, re, csv, json, math, urllib.parse, collections as C
import networkx as nx

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
RES = os.path.join(REPO, "Analysis", "results")
OUT = os.path.join(REPO, "Enrichment", "out")
csv.field_size_limit(10 ** 8)
INSTS = ["IIT Kharagpur", "IIT Roorkee"]
N_HUBS = 30                     # citation-network panel: top papers by PageRank, drawn with every paper citing them


def rd(name, folder=RES):
    with open(os.path.join(folder, name), encoding="utf-8-sig", newline="") as fh:
        return list(csv.DictReader(fh))


def num(x, f=float):
    try:
        return f(x)
    except (TypeError, ValueError):
        return None


def by_inst(rows, key="institution"):
    d = C.defaultdict(list)
    for r in rows:
        d[r[key]].append(r)
    return d


def packed_layout(G, aspect=1.25, gap=0.12):
    """Lay out each connected component on its own (spring layout scaled to its size), then pack the components in
    rows, largest first. A single spring layout pushes disconnected clusters far apart and shrinks each one."""
    comps = sorted(nx.connected_components(G), key=len, reverse=True)
    radius = lambda c: 0.09 * math.sqrt(len(c))          # component radius grows with its size
    area = sum((2 * radius(c) + gap) ** 2 for c in comps)
    width = max(2 * radius(comps[0]) + gap, math.sqrt(area * aspect) * 1.08)   # rows as wide as the panel's shape
    pos, x, y, row_h = {}, 0.0, 0.0, 0.0
    for comp in comps:
        H = G.subgraph(comp)
        r = radius(comp)
        p = nx.spring_layout(H, seed=3, iterations=200) if len(comp) > 1 else {next(iter(comp)): (0.0, 0.0)}
        xs, ys = [v[0] for v in p.values()], [v[1] for v in p.values()]
        cx, cy = (max(xs) + min(xs)) / 2, (max(ys) + min(ys)) / 2
        span = max(max(xs) - min(xs), max(ys) - min(ys)) or 1.0
        if x > 0 and x + 2 * r > width:                    # next row
            x, y, row_h = 0.0, y + row_h + gap, 0.0
        for v, (a, b) in p.items():
            pos[v] = (x + r + (a - cx) / span * 2 * r, -(y + r + (b - cy) / span * 2 * r))
        x += 2 * r + gap
        row_h = max(row_h, 2 * r)
    return pos


FIRST_NUM = re.compile(r"-?\d+(?:\.\d+)?")
# PRL titles whose maths OpenAlex lost ("JeffDescription ... Insulatorα−RuCl3"): the publisher's title from Crossref,
# written in plain Unicode (the report has the same titles in LaTeX, Report/make_tables.py)
PRL_TITLE = {
    "10.1103/physrevlett.131.056202": "Anomalous Reentrant 5/2 Quantum Hall Phase at Moderate Landau-Level-Mixing Strength",
    "10.1103/physrevlett.132.029602": "Das et al. Reply (reply to a comment)",
    "10.1103/physrevlett.132.106501": "Fractional Quantum Hall States of the 𝒜 Phase in the Second Landau Level",
    "10.1103/physrevlett.117.126403": "J_eff Description of the Honeycomb Mott Insulator α-RuCl₃",
    "10.1103/physrevlett.116.072501": "Single and Double Beta-Decay Q Values among the Triplet ⁹⁶Zr, ⁹⁶Nb, and ⁹⁶Mo",
    "10.1103/physrevlett.118.151802": "Measurement of the Neutrino Mixing Angle θ₂₃ in NOvA",
    "10.1103/physrevlett.123.262701": "Discovery of an Exceptionally Strong β-Decay Transition of ²⁰F and Implications for the Fate of Intermediate-Mass Stars",
    "10.1103/s7hr-y7zq": "Probing the Shell Effects on Fission: The New Superheavy Nucleus ²⁵⁷Sg",
}


def first_num(s):
    """First number in a text value such as '0.689 (n = 1105)' or '72 (name)'."""
    m = FIRST_NUM.search(str(s))
    return float(m.group()) if m else None


ROSTERS = os.path.join(REPO, "WebScrape", "rosters")
SUPPLEMENT = os.path.join(REPO, "Enrichment", "cache")
LINK_STATUS = os.path.join(HERE, "link_status.json")   # optional, written by check_links.py
ORCID_RE = re.compile(r"\d{4}-\d{4}-\d{4}-\d{3}[\dX]")


def clean_url(u):
    """http(s) URL with spaces and other unsafe characters percent-encoded; anything else -> None."""
    u = (u or "").strip()
    if not re.match(r"https?://[\w-]+(\.[\w-]+)+(/|$|:|\?)", u, re.I):   # rejects "http://Nil", "To be updated", ...
        return None
    u = u.replace("://www.facweb.iitkgp.ac.in", "://facweb.iitkgp.ac.in")   # dead www. alias of KGP's faculty web server
    return urllib.parse.quote(u, safe=":/?&=#%+@,;~!$'()*[]")


def faculty_links(drop_dead=True):
    """roster_id -> {profile, scholar, home, dblp, scopus, irins, orcid: [...]}, taken only from what the institute
    pages list (WebScrape/rosters) plus the ORCID-verified additions (Enrichment/cache/roster_supplement_*.json).
    Nothing is searched for or guessed. Links that check_links.py found dead (404/410/no such host) are dropped."""
    dead = set()
    if drop_dead and os.path.exists(LINK_STATUS):
        with open(LINK_STATUS, encoding="utf-8") as fh:
            dead = {u for u, s in json.load(fh).items() if s in (404, 410, "dns")}
    links = {}
    for inst in ("iit_kharagpur", "iit_roorkee"):
        for k, r in enumerate(rd(f"{inst}_faculty.csv", ROSTERS)):
            L = {"profile": clean_url(r["profile_url"]), "scholar": clean_url(r["google_scholar"]),
                 "home": clean_url(r["homepage"]), "dblp": clean_url(r["dblp"]), "irins": clean_url(r["irins"]),
                 "scopus": f"https://www.scopus.com/authid/detail.uri?authorId={r['scopus_id'].strip()}"
                           if r["scopus_id"].strip().isdigit() else None,
                 "orcid": ORCID_RE.findall(r["orcid"] or "")}
            links[f"{inst}:{k}"] = L
        sfn = os.path.join(SUPPLEMENT, f"roster_supplement_{inst}.json")
        if os.path.exists(sfn):
            with open(sfn, encoding="utf-8") as fh:
                for s in json.load(fh):
                    rid = s["roster_id"] if s.get("kind") == "alt_orcid" else f"{inst}:orcid:{s['orcid']}"
                    L = links.setdefault(rid, {"orcid": []})
                    if s["orcid"] not in L["orcid"]:
                        L["orcid"].append(s["orcid"])
    for L in links.values():
        L["orcid"] = [f"https://orcid.org/{o}" for o in L["orcid"]]
        for k in list(L):
            if not L[k] or (isinstance(L[k], str) and L[k] in dead):
                del L[k]
    return links


def main():
    D = {"generated": "October 2026", "insts": INSTS}

    # ---------------- overview numbers
    trend = by_inst(rd("trend.csv"))
    quart = {r["institution"]: r for r in rd("quartiles.csv")}
    core = {r["institution"]: r for r in rd("core_ranks.csv")}
    fac = rd("faculty.csv")
    cent = {r["roster_id"]: r for r in rd("faculty_centrality.csv")}
    flow = {r["institution"]: r for r in rd("citation_flow_summary.csv")}
    hsum = rd("h_index_summary.csv")
    hchk = {r["institution"]: r for r in rd("h_index_check_summary.csv")}
    hyr = by_inst(rd("h_index_by_year.csv"))
    D["h_summary"] = {i: {r["metric"]: {k: num(r[k]) for k in ("n", "mean", "sd", "q1", "median", "q3", "p90", "max")}
                          for r in hsum if r["institution"] == i and r["department"] == "All departments"} for i in INSTS}
    D["h_check"] = {i: {k: num(v) for k, v in hchk[i].items() if k != "institution"} for i in INSTS}
    D["h_by_year"] = {i: {k: [num(r[k]) for r in hyr[i]] for k in ("mean_h", "median_h", "p90_h", "institute_h_index")}
                      for i in INSTS}
    kpi = {}
    for i in INSTS:
        hs = sorted(int(r["h_index"]) for r in fac if r["institution"] == i)
        kpi[i] = {"papers": sum(int(r["total"]) for r in trend[i]),
                  "faculty": len(hs), "median_h": hs[len(hs) // 2], "max_h": hs[-1],
                  "q1_share": float(quart[i]["q1_fraction_of_ranked"]),
                  "journal_papers": int(quart[i]["journal_papers"]),
                  "in_flow": int(flow[i]["in_flow"]), "out_flow": int(flow[i]["out_flow"]),
                  "impact_ratio": float(flow[i]["impact_ratio_in_over_out"]),
                  "first_year_papers": int(trend[i][0]["total"]), "last_full_year_papers": int(trend[i][-2]["total"])}
    D["kpi"] = kpi

    # ---------------- output & quality
    types = ["journal", "conference", "book-chapter", "preprint", "other"]
    D["years"] = [int(r["year"]) for r in trend[INSTS[0]]]
    D["trend"] = {i: {"total": [int(r["total"]) for r in trend[i]], **{t: [int(r[t]) for r in trend[i]] for t in types}}
                  for i in INSTS}
    D["quartiles"] = {i: {k: int(quart[i][k]) for k in ("Q1", "Q2", "Q3", "Q4", "not_in_scimago")} for i in INSTS}
    D["core"] = {i: {k: int(core[i][k]) for k in ("A*", "A", "B", "C", "not_core_ranked", "conference_papers")} for i in INSTS}
    D["top_journals"] = {i: [{"journal": r["journal"], "papers": int(r["papers"]), "q": r["most_common_quartile"],
                              "if": num(r["if_openalex"])} for r in rows] for i, rows in by_inst(rd("top_journals.csv")).items()}
    imp = by_inst(rd("important_journals.csv"))
    ys = [str(y) for y in range(2016, 2027)]
    D["important"] = {i: [{"group": r["group"], "total": int(r["total"]), "years": [int(r[y]) for y in ys]} for r in imp[i]]
                      for i in INSTS}
    ipp = C.defaultdict(list)
    for r in rd("important_journal_papers.csv"):
        if r["group"] == "PRL" or len(ipp[(r["institution"], r["group"])]) < 6:     # PRL: every paper (professor's request)
            title = PRL_TITLE.get(r["doi"].replace("https://doi.org/", ""), r["title"])
            ipp[(r["institution"], r["group"])].append({"title": title, "journal": r["journal"], "year": int(r["year"]),
                                                        "cites": num(r["citations"], int), "doi": r["doi"], "faculty": r["faculty"]})
    D["important_papers"] = {f"{i}|{g}": v for (i, g), v in ipp.items()}
    ifr = rd("impact_factor.csv")
    D["impact"] = {i: {"all": next({k: r[k] for k in r} for r in ifr if r["institution"] == i and r["scope"] == "all years" and not r["department"]),
                       "over5": [float(r["share_if_over_5"] or 0) for y in ys for r in ifr if r["institution"] == i and r["scope"] == y and not r["department"]],
                       "over10": [float(r["share_if_over_10"] or 0) for y in ys for r in ifr if r["institution"] == i and r["scope"] == y and not r["department"]]}
                   for i in INSTS}
    lc = rd("large_collaborations.csv")
    D["large"] = {i: next({k: r[k] for k in r} for r in lc if r["institution"] == i and r["scope"] == "all years") for i in INSTS}
    cs = rd("core_summary.csv")
    D["core_years"] = {i: {k: [int(r[k]) for y in ys for r in cs if r["institution"] == i and r["scope"] == y and not r["department"]]
                           for k in ("A*", "A", "B", "C")} for i in INSTS}
    D["core_venues"] = {i: [{"conf": r["conference"], "rank": r["core_rank"], "papers": int(r["papers"])} for r in rows]
                        for i, rows in by_inst(rd("core_top_venues.csv")).items()}
    sub = rd("research_subfields.csv")
    D["subfields"] = {i: {} for i in INSTS}
    for r in sub:
        L = D["subfields"][r["institution"]].setdefault(r["field"], [])
        if len(L) < 8:
            L.append({"sub": r["subfield"], "papers": int(r["papers"]), "share": float(r["share_of_field"])})
    env = rd("env_science_breakdown.csv")
    D["env"] = {i: {b: [{"name": r["name"], "papers": int(r["papers"]), "share": float(r["share_of_env_papers"])}
                        for r in env if r["institution"] == i and r["by"] == b][:6] for b in ("subfield", "department", "topic")}
                for i in INSTS}
    areas = by_inst(rd("research_areas.csv"))
    D["areas"] = {i: [{"field": r["field"], "share": float(r["share"]), "papers": int(r["papers"])} for r in areas[i]] for i in INSTS}

    # ---------------- people
    D["faculty"] = []
    links = faculty_links()
    for r in fac:
        c = cent.get(r["roster_id"], {})
        D["faculty"].append({"id": r["roster_id"], "name": r["faculty"], "inst": r["institution"], "dept": r["department"],
                             "papers": int(r["papers"]), "cites": int(r["citations"]), "h": int(r["h_index"]),
                             "q1": int(r["q1_papers"]), "i10": int(r["i10_index"]), "oa_h": num(r["oa_h_index_all_career"], int),
                             "journal": r["top_journal"], "from": int(r["first_year"]),
                             "to": int(r["last_year"]), "coauthors": num(c.get("faculty_coauthors"), int),
                             "betw": num(c.get("betweenness")), "community": num(c.get("community"), int),
                             "links": links.get(r["roster_id"], {})})
    have = C.Counter(k for f in D["faculty"] for k in f["links"])
    print("faculty links:", dict(have), "| none:", sum(1 for f in D["faculty"] if not f["links"]))
    D["departments"] = [{"inst": r["institution"], "dept": r["department"], "faculty": int(r["faculty_with_papers"]),
                         "papers": int(r["papers"]), "cites": int(r["citations"]),
                         "q1": num(r["q1_fraction_of_ranked"]), "median_h": float(r["median_h_index"]), "max_h": int(r["max_h_index"]),
                         "mean_h": num(r["mean_h_index"]), "sd_h": num(r["sd_h_index"])}
                        for r in rd("departments.csv")]

    # ---------------- papers
    D["most_cited"] = {s: [{"title": r["title"], "journal": r["journal"], "year": int(r["year"]), "cites": int(r["citations"]),
                            "doi": r["doi"], "insts": r["institutions"]} for r in rows]
                       for s, rows in by_inst(rd("most_cited.csv"), "scope").items()}
    # slide 12: most-cited Indian papers that cite each institute (Analysis/scripts/stats_citing_top.py)
    if os.path.exists(os.path.join(RES, "top_citing_papers.csv")):     # online step; the panel hides until it has run
        D["top_citing"] = {s: [{"title": r["title"], "journal": r["journal"], "year": int(r["year"]) if r["year"] else None,
                                "cites": int(r["citations"]), "doi": r["doi"], "insts": r["citing_institutions"],
                                "n": int(r["papers_cited"])} for r in rows]
                           for s, rows in by_inst(rd("top_citing_papers.csv"), "scope").items()}
    D["pagerank_top"] = {s: [{"title": r["title"], "journal": r["journal"], "year": int(r["year"]), "pr": float(r["pagerank"]),
                              "indeg": int(r["in_degree"]), "indeg_rank": int(r["in_degree_rank"]), "doi": r["doi"]}
                             for r in rows] for s, rows in by_inst(rd("pagerank_top10.csv"), "scope").items()}
    D["netsum"] = {r["scope"]: {k: r[k] for k in r if k != "scope"} for r in rd("citation_network_summary.csv")}
    D["indegree"] = {s: [[int(r["in_degree"]), int(r["papers"])] for r in rows]
                     for s, rows in by_inst(rd("indegree_distribution.csv"), "scope").items()}

    # ---------------- citation flow
    D["flow_yearly"] = {i: {"in": [int(r["in_flow"]) for r in rows], "out": [int(r["out_flow"]) for r in rows]}
                        for i, rows in by_inst(rd("citation_flow_yearly.csv")).items()}
    fp = by_inst(rd("citation_flow_partners.csv"))
    D["top_citers"] = {i: [{"partner": r["partner"], "cites": int(r["citations_from_partner"]),
                            "out": int(r["citations_to_partner"])} for r in fp[i][:10]] for i in INSTS}

    # ---------------- collaboration
    D["auth_summary"] = {r["metric"]: r["value"] for r in rd("authorship_summary.csv")}
    D["null_models"] = [{k: r[k] for k in r} for r in rd("null_model_comparison.csv")]
    D["communities"] = [{"id": int(r["community"]), "size": int(r["faculty"]), "kgp": int(r["IIT Kharagpur"]),
                         "rkg": int(r["IIT Roorkee"]), "dept": r["top_department"], "dept_share": float(r["top_department_share"]),
                         "hub": r["most_connected_member"]} for r in rd("communities.csv")]
    D["bridging"] = [{"inst": r["institution"], "name": r["faculty"], "dept": r["department"],
                      "partners": int(r["indian_partner_institutions"])} for r in rd("bridging_faculty.csv")]

    # ---------------- papers with more than 10 authors (stats_journals.py, stats_large_collab.py)
    lc = {r["institution"]: r for r in rd("large_collaborations.csv") if r["scope"] == "all years"}
    by = lambda name: by_inst(rd(name))
    venue = by("large_by_venue.csv")
    D["teams"] = {i: {
        "papers": int(lc[i]["more_than_10_authors"]), "share": float(lc[i]["share"]), "cite_share": float(lc[i]["share_of_all_citations"]),
        "n100": int(lc[i]["with_100_or_more"]),
        "sens": [{"m": r["metric"], "all": num(r["all_papers"]), "wo": num(r["without_large"]), "pct": num(r["change_pct"])} for r in by("large_sensitivity.csv")[i]],
        "prem": {"years": [int(r["year"]) for r in by("large_premium.csv")[i] if r["year"].isdigit()],
                 "ratio": [float(r["ratio"]) for r in by("large_premium.csv")[i] if r["year"].isdigit()],
                 "overall": next(float(r["ratio"]) for r in by("large_premium.csv")[i] if not r["year"].isdigit())},
        "dept": [{"name": r["department"], "n": int(r["large_papers"]), "share": float(r["share_of_institute_large"]),
                  "of_dept": float(r["share_of_department"])} for r in by("large_by_department.csv")[i][:8]],
        "field": [{"name": r["field"], "n": int(r["large_papers"]), "share": float(r["share_of_large"])} for r in by("large_by_field.csv")[i][:6]],
        "venues": [{"name": r["label"], "n": int(r["large_papers"]), "rank": r["rank"]} for r in venue[i] if r["kind"] == "venue"][:6],
        "profile": {f'{r["kind"]}|{r["label"]}': [num(r["share_large"]), num(r["share_other"])] for r in venue[i] if r["kind"] != "venue"},
        "bands": [{"band": r["authors"], "n": int(r["papers"]), "median": num(r["median_citations"])} for r in by("large_size_bands.csv")[i]],
        "faculty": [{"name": r["faculty"], "dept": r["department"], "n": int(r["large_papers"]), "h": int(r["h_index"]),
                     "h_wo": int(r["h_without_large"])} for r in by("large_faculty_impact.csv")[i][:10]]} for i in INSTS}

    # ---------------- beyond the brief: self-citation, corrected PageRank, dynamics (stats_*_dynamics.py)
    kv = lambda name: {r["metric"]: r["value"] if num(r["value"]) is None else num(r["value"]) for r in rd(name)}
    D["selfcite"] = {r["scope"]: {"share": float(r["self_share"]), "edges": int(r["citation_edges"]), "non_self": int(r["non_self_edges"])}
                     for r in rd("self_citation_summary.csv")}
    sy = C.defaultdict(list)
    for r in rd("self_citation_yearly.csv"):
        sy[r["scope"]].append(num(r["self_share"]))
    D["selfcite_yearly"] = dict(sy)
    D["pr_variants"] = C.defaultdict(list)
    for r in rd("pagerank_variants_top10.csv"):
        D["pr_variants"][r["variant"]].append({"title": r["title"], "year": int(r["year"]), "doi": r["doi"], "insts": r["institutions"],
                                               "indeg": int(r["internal_in_degree"]), "nonself": int(r["non_self_in_degree"]),
                                               "cites": num(r["global_citations"], int)})
    D["pr_agree"] = {r["variant"]: {"cv": float(r["age_bias_cv_top1pct"]), "overlap": int(r["top100_overlap_with_all"])}
                     for r in rd("pagerank_variant_agreement.csv")}
    D["age_bias"] = [{"ranking": r["ranking"], "cv": float(r["cv_of_shares"]), "shares": [float(r[str(y)]) for y in range(2016, 2026)]}
                     for r in rd("pagerank_age_bias.csv")]
    pa = rd("preferential_attachment.csv")
    D["pa"] = {"k": [int(r["k_citations_before_year"]) for r in pa], "A": [float(r["attachment_rate_A_k"]) for r in pa],
               "n": [int(r["paper_years"]) for r in pa], **kv("citation_dynamics_summary.csv")}
    D["fits"] = [{k: r[k] for k in ("quantity", "alpha", "x_min", "papers_in_tail", "R_vs_lognormal", "p_vs_lognormal", "verdict")}
                 for r in rd("distribution_fits.csv")]
    D["structure"] = kv("authorship_structure.csv")
    D["leiden"] = [{k: num(v) if k != "algorithm" else v for k, v in r.items()} for r in rd("leiden_comparison.csv")]
    D["growth"] = [{k: num(v) for k, v in r.items()} for r in rd("network_growth.csv")]
    D["robust"] = [{k: num(v) for k, v in r.items()} for r in rd("robustness.csv")]
    D["sir"] = [{k: num(v) for k, v in r.items()} for r in rd("sir_outbreaks.csv")]
    D["spreader_rank"] = [{"c": r["centrality"], "rho": float(r["spearman_rho_with_outbreak"]), "top": float(r["top5pct_overlap_with_best_spreaders"])}
                          for r in rd("spreader_ranking.csv")]
    D["top_spreaders"] = [{"name": r["faculty"], "inst": r["institution"], "dept": r["department"], "share": float(r["expected_outbreak_share"]),
                           "deg": int(r["degree"]), "core": int(r["k_core"])} for r in rd("top_spreaders.csv")[:10]]
    D["cent_impact"] = [{k: num(v) if k not in ("centrality", "impact") else v for k, v in r.items()} for r in rd("centrality_vs_impact.csv")]
    D["tie_types"] = [{"type": r["tie_type"], "n": int(r["pair_paper_rows"]), "share": float(r["share"])} for r in rd("coauthor_tie_types.csv")]

    # ---------------- second round: professor's follow-up (stats_if_authors.py)
    D["nature"] = [{"journal": r["journal"], "if": float(r["if_openalex"]), "n": {i: int(r[i]) for i in INSTS}}
                   for r in rd("nature_journals_if.csv")]
    D["grid"] = {i: [{"row": r["row"], "papers": int(r["papers"]), "lt10": int(r["fewer than 10"]), "eq10": int(r["exactly 10"]),
                      "gt10": int(r["more than 10"]), "share_lt10": float(r["share_fewer_than_10"]),
                      "share_gt10": float(r["share_more_than_10"])} for r in rows]
                 for i, rows in by_inst(rd("q1_if_author_grid.csv")).items()}
    j10 = by_inst(rd("if10_small_team_journals.csv"))
    D["if10_journals"] = {i: {"journals": len(j10[i]), "papers": sum(int(r["papers_fewer_than_10_authors"]) for r in j10[i]),
                              "top": [{"journal": r["journal"], "if": float(r["if_openalex"]), "n": int(r["papers_fewer_than_10_authors"])}
                                      for r in j10[i][:10]]} for i in INSTS}

    # ---------------- second round: beyond pairs and PageRank (stats_matrix_centrality.py, stats_hypergraph.py, stats_simplicial.py)
    fm, cs, hs, ss = (kv(n) for n in ("faculty_matrix_summary.csv", "citation_centrality_summary.csv",
                                      "hypergraph_summary.csv", "simplicial_summary.csv"))
    dyn = rd("dynamic_communicability_top.csv")
    dyn_meta = dyn[-1]["measure"]                           # '(a = ..., faculty with degree > 0: 1156; Spearman ... 0.796, ...)'
    test = [r for r in rd("citation_centrality_test.csv") if not r["metric"].startswith("(")]
    pred = [r for r in rd("simplicial_prediction.csv") if r["score"] == "harmonic mean of edge weights"]
    D["beyond"] = {
        "katz_path": [{"f": float(r["f (a = f / lambda_1)"]), "deg": float(r["spearman_vs_degree"]),
                       "eig": float(r["spearman_vs_eigenvector"])} for r in rd("faculty_katz_path.csv")],
        "giant": int(fm["eigenvector: faculty with a non-zero score (its component)"]),
        "eig_top10": fm["eigenvector weight (sum v^2) on its top 10 faculty"],
        "eig_roorkee": fm["share of eigenvector weight (sum v^2) on Roorkee faculty"], "roorkee_share": fm["Roorkee share of faculty"],
        "eig_in_core": int(fm["eigenvector top 10 inside the max k-core"]),
        "campus": {r["pair"]: float(r["mean_cos_angle"]) for r in rd("campus_communicability.csv")},
        "bridges": [{"name": r["faculty"], "inst": r["institution"], "dept": r["department"], "lost": float(r["campus_ratio_lost"]),
                     "cross": int(r["direct_cross_campus_coauthors"]), "rank_btw": int(r["rank_betweenness"])}
                    for r in rd("cross_campus_removal.csv")[:10]],
        "bridges_over5": int(fm["faculty whose removal lowers rho_KR by more than 5%"]),
        "btw_overlap": int(fm["top-10 overlap: rho_KR loss vs betweenness"]),
        "early": [{"name": r["faculty"], "inst": r["institution"], "dept": r["department"], "rank": int(r["rank"]),
                   "rank_deg": int(r["rank_degree"]), "deg": int(r["degree_all_years"]), "first": num(r["first_faculty_coauthorship_year"], int)}
                  for r in dyn if r["measure"] == "broadcast"][:15],
        "early_n": int(first_num(dyn_meta.split("degree > 0:")[1])),
        "early_rho": first_num(dyn_meta.split("broadcast vs degree")[1]),
        "predict": [{"metric": r["metric"], "nonzero": num(r["papers_with_nonzero_score"], int), "note": r["note"],
                     "rho": num(r["spearman_within_year_mean"]), "partial": num(r["partial_spearman_given_past_citations"]),
                     "band": num(r["spearman_within_year_and_past_band"]), "neg": num(r["bands_negative"], int),
                     "bands": num(r["bands_used"], int)} for r in test],
        "papers": int(cs["papers (nodes)"]), "hits_support": int(cs["HITS: authority support"]),
        "hits_top_group": int(first_num(cs["HITS authority: top-100 papers of the most frequent faculty member"])),
        "katz_top_group": int(first_num(cs["Katz: top-100 papers of the most frequent faculty member"])),
        "cycle_papers": int(first_num(cs["largest cycle group: papers, citations, faculty"])), "rho_cit": cs["spectral radius rho"],
        "hyper": {"authors": int(hs["authors (nodes)"]), "papers": int(hs["papers with >= 2 authors (hyperedges)"]),
                  "big": int(hs["papers with more than 10 authors (n_authors)"]),
                  "pair_share": hs["author pairs (counted per paper) that come from papers with more than 10 authors, share of all"],
                  "top10": {m: hs[f"{m}: share of score weight (x^2) on its top 10 authors"] for m in ("linear", "max", "log-exp")},
                  "logexp_authors": int(hs["log-exp: authors with a non-zero score"]), "logexp_faculty": int(hs["log-exp: faculty with a non-zero score"]),
                  "lin_max_rho": first_num(hs["faculty Spearman: linear vs max (faculty non-zero in both)"]),
                  "kept_linear": int(hs["linear without >10-author papers: top 20 overlap with linear top 20"]),
                  "kept_coauthors": int(hs["distinct co-authors without >10-author papers: top 20 overlap with distinct co-authors (pairwise) top 20"]),
                  "name_check": int(hs["check (names split): linear: faculty top 20 overlap with the main run"])},
        "closure": [{"cap": int(r["cap"]), "cls": r["class"], "triples": int(r["triples"]), "closed": int(r["closed_later"]),
                     "p": float(r["closure_probability"]), "lo": float(r["ci95_low"]), "hi": float(r["ci95_high"]),
                     "share": num(r["share_of_new_trios"])} for r in rd("simplicial_closure_by_config.csv")],
        "tri_closed_all": ss["all authors, papers <= 25 authors, all years: share of triangles closed by one paper"],
        "tri_closed_fac": ss["faculty network: share of triangles closed by one paper with all three faculty"],
        "fac3_papers": int(ss["papers with >= 3 faculty (only these can close a faculty triangle in one paper)"]),
        "pred": {int(r["cap"]): {"auc": float(r["roc_auc"]), "p": float(r["p_value_auc_above_half"]), "ap_x": float(r["ap_over_random"])}
                 for r in pred}}

    # ---------------- second round: two layers and departments (stats_coauthor_citation.py, stats_bowtie.py,
    # stats_cross_dept.py, stats_dept_areas.py); 'strict' citations = citing and cited paper share no author
    cc, da, dp = kv("coauthor_citation_summary.csv"), kv("dept_area_summary.csv"), kv("dept_area_prediction.csv")
    bt = {r["metric"]: r["value"] for r in rd("bowtie_summary.csv") if r["definition"] == "pure"}
    bts = {r["metric"]: r["value"] for r in rd("bowtie_summary.csv") if r["definition"] == "strict"}
    prec = [r for r in rd("coauthor_citation_precedence.csv") if r["definition"] == "strict"]
    cx = kv("cross_dept_summary.csv")
    cx_groups = {}
    for k, v in cx.items():
        if isinstance(k, str) and k.startswith(f"<= ") and "|" in k:
            g = dict(x.strip().rsplit(" ", 1) for x in str(v).split(";"))
            cx_groups[k.split("|")[1].strip()] = {"n": int(g["papers"]), "fwci": float(g["median_fwci"]), "top10": float(g["top10_share"])}
    reg = {(r["window"].startswith("<="), r["outcome"], r["term"]): r for r in rd("cross_dept_regression.csv")}
    strata = {(r["window"].startswith("<="), r["comparison"].split(" ")[0]): r for r in rd("cross_dept_strata.csv")}
    inw = {r["institution"]: r for r in rd("institute_inwardness.csv") if r["publication_year"] == "all"}
    D["layers"] = {
        "dist": [{"scope": r["scope"], "d": r["coauthor_distance"], "rate": float(r["citing_rate"]), "oe": float(r["obs_over_expected"]),
                  "pairs": int(r["ordered_pairs"]), "citing": int(r["pairs_citing"])}
                 for r in rd("coauthor_citation_distance.csv") if r["definition"] == "strict"],
        "fac_cit_all": int(cc["faculty citations, all (a on citing paper, b on cited paper, a != b)"]),
        "fac_cit_strict": int(cc["faculty citations, strict"]), "pairs_strict": int(cc["strict: citing pairs a -> b"]),
        "recip": cc["strict: reciprocity (share of a -> b with b -> a)"], "recip_exp": cc["strict: reciprocity expected, configuration model (analytic)"],
        "recip_co": cc["strict: reciprocity among co-author pairs"], "recip_non": cc["strict: reciprocity among pairs that never co-authored"],
        "active": int(cc["faculty active before and after 2020"]),
        "prec": [{"test": r["test"][:3], "exposed": r["exposed"], "pairs": int(r["pairs"]), "hits": int(r["pairs_with_outcome"]),
                  "rate": num(r["rate"]), "oe": num(r["obs_over_expected"])} for r in prec],
        "inward": {i: {"all": float(inw[i]["inwardness"]), "other": float(inw[i]["inwardness_without_author_self"])} for i in INSTS},
        "bowtie": {"parts": {i: {p: int(bt[f"{i}: {p}"]) for p in ("CORE", "IN", "OUT", "TUBES", "TENDRILS", "OTHER", "ISOLATED")} for i in INSTS},
                   "linked": int(bt["faculty with at least one citation link (either direction)"]), "pairs": int(bt["citing pairs a -> b"]),
                   "cross": int(bt["citing pairs between the two IITs"]), "core_cross": int(bt["CORE members citing or cited by the other IIT within the CORE"]),
                   "null": bt["CORE size in 10 degree-preserving rewirings: mean (min-max)"], "core_strict": int(bts["CORE (faculty)"]),
                   "null_strict": bts["CORE size in 10 degree-preserving rewirings: mean (min-max)"],
                   "median": {p: {k: float(bt[f"{p}: median {k}"]) for k in ("papers", "h_index")} for p in ("CORE", "IN", "OUT", "ISOLATED")},
                   "growth": [{"y": int(r["up_to_year"]), **{p: int(r[p]) for p in ("CORE", "IN", "OUT", "TUBES", "TENDRILS", "OTHER")}}
                              for r in rd("bowtie_growth.csv")]},
        "hier": [{"inst": r["institution"], "dept": r["department"], "fac": int(r["faculty"]), "s": float(r["springrank"]),
                  "cin": int(r["cited_by_other_departments"]), "cout": int(r["cites_other_departments"])} for r in rd("department_citation_hierarchy.csv")],
        "hier_rho": float(bt["check: Spearman SpringRank vs net balance"]),
        "cross": {"groups": cx_groups, "n_multi_check": int(cx["check: the same from group3_data.csv"]),
                  "match_ratio": float(strata[(True, "cross-department")]["fwci_ratio_exp_diff"]),
                  "match_campus": float(strata[(True, "cross-campus")]["fwci_ratio_exp_diff"]),
                  "reg": {k: {"coef": float(r["coef"]), "lo": float(r["ci95_low"]), "hi": float(r["ci95_high"]), "p": float(r["p_value"])}
                          for k, r in (("dept", reg[(True, "log(1 + FWCI)", "cross-department (same IIT)")]),
                                       ("campus", reg[(True, "log(1 + FWCI)", "cross-campus")]),
                                       ("campus_all", reg[(False, "log(1 + FWCI)", "cross-campus")]))},
                  "rs_p": float(next(r for k, r in reg.items() if k[0] and k[2].startswith("Rao"))["p_value"]),
                  "same_fac": int(cx["same faculty member: faculty with both one-department and cross-department papers"]),
                  "same_share": float(cx["same faculty member: share of faculty with a higher value on cross-department papers"]),
                  "same_p": float(cx["same faculty member: Wilcoxon signed-rank p"])},
        "areas": {"cand": int(dp["candidate (department, subfield) pairs: not strong in 2016-20 (strong = RCA >= 1 and >= 5 papers)"]),
                  "entries": int(dp["entries: strong in 2021-26"]), "auc": dp["ROC AUC: density (relatedness to what the department does)"],
                  "auc_rca": dp["ROC AUC: RCA in 2016-20 (already close)"],
                  "auc_both": dp["ROC AUC, logistic with one department left out: density + RCA"],
                  "null": dp["ROC AUC: density with shuffled subfield labels, 500 shuffles: mean (95% range)"],
                  "auc_new": dp["ROC AUC: density, brand-new areas only"],
                  "bins": [{"bin": r["bin"], "pairs": int(r["pairs"]), "entries": int(r["entries"]), "rate": float(r["entry_rate"])}
                           for r in rd("dept_area_prediction_bins.csv")],
                  "fc_stable": da["fitness-complexity: ranking stability, Spearman of fitness after 50 and 100 steps"]},
        "depts": {}}
    dep = D["layers"]["depts"]
    for r in rd("dept_fitness.csv"):
        dep[f"{r['institution']}|{r['department']}"] = {"inst": r["institution"], "dept": r["department"], "fac": int(r["faculty"]),
                                                          "papers": int(r["papers"]), "nstrong": int(r["strong_subfields"]),
                                                          "fit": int(r["fitness_rank"]), "strong": [], "rising": [], "near": []}
    for r in rd("dept_area_strengths.csv"):
        dep[f"{r['institution']}|{r['department']}"]["strong"].append([r["subfield"], int(r["papers"]), float(r["rca"])])
    for r in rd("dept_area_rising.csv"):
        dep[f"{r['institution']}|{r['department']}"]["rising"].append([r["subfield"], int(r["papers_2016_20"]), int(r["papers_2021_26"])])
    for r in rd("dept_area_outlook.csv"):
        dep[f"{r['institution']}|{r['department']}"]["near"].append([r["subfield"], int(r["papers_2021_26"])])

    # ---------------- key findings (overview): the report's list, with every number read from the results
    yr = {i: (int(trend[i][0]["total"]), int(trend[i][-2]["total"])) for i in INSTS}
    g10 = {i: next(r for r in D["grid"][i] if r["row"].startswith("IF > 10")) for i in INSTS}
    B, H = D["beyond"], D["beyond"]["hyper"]
    cl = {r["cls"].split(" ")[0]: r for r in B["closure"] if r["cap"] == 25 and r["share"] is not None}
    D["findings"] = [
        f"From 2016 to 2025, output grew {yr[INSTS[0]][1] / yr[INSTS[0]][0]:.1f}× at Kharagpur and {yr[INSTS[1]][1] / yr[INSTS[1]][0]:.1f}× at Roorkee, "
        f"and most ranked journal papers are in Q1 ({float(quart[INSTS[0]]['q1_fraction_of_ranked']) * 100:.1f}% and {float(quart[INSTS[1]]['q1_fraction_of_ranked']) * 100:.1f}%).",
        f"High-IF work comes from small teams: of the {g10[INSTS[0]]['papers']:,} Kharagpur and {g10[INSTS[1]]['papers']:,} Roorkee papers in journals "
        f"with IF > 10, {g10[INSTS[0]]['share_lt10'] * 100:.0f}% and {g10[INSTS[1]]['share_lt10'] * 100:.0f}% have fewer than 10 authors.",
        f"{D['selfcite']['Cluster (both IITs)']['share'] * 100:.1f}% of the citations between papers of the two IITs are self-citations, and at equal "
        f"past citations a self-citation does not signal later impact the way an outside citation does.",
        f"Faculty work inside their own campus: the two IITs share only {D['auth_summary']['Kharagpur-Roorkee faculty pairs']} faculty links, and removing "
        f"Dr. {B['bridges'][0]['name']} alone lowers the campus communicability ratio by {B['bridges'][0]['lost'] * 100:.0f}%.",
        f"Big teams distort the pair view: papers with more than 10 authors are {H['big'] / H['papers'] * 100:.1f}% of the co-authorship papers, "
        f"but give {H['pair_share'] * 100:.0f}% of the author pairs.",
        f"Rankings that use the whole network at once settle on one dense lab: removing the big-team papers changes {20 - H['kept_linear']} of the "
        f"hypergraph's top 20 faculty, while a plain count of co-authors keeps {H['kept_coauthors']} of 20.",
        f"Trios form along existing pairs: three authors who have all worked in pairs write together {cl['3']['p'] * 100:.1f}% of the time, "
        f"against about {cl['0']['p'] * 1e9:.0f} in a billion with no earlier pair, and {(1 - cl['0']['share']) * 100:.0f}% of new trios follow at least one earlier pair.",
        f"The collaboration network grew denser every year (ties ∝ faculty^{D['structure']['densification exponent a, ties ~ faculty^a']:.2f}) and survives "
        f"random loss, but losing its biggest bridges splits the two campuses.",
        f"Faculty cite their co-authors {next(r['oe'] for r in D['layers']['dist'] if r['scope'] == 'all pairs' and r['d'] == '1'):.0f}× as often "
        f"as similar faculty far apart, even when the two papers share no author, and citing and co-authoring each predict the other.",
        f"Teams that mix departments get no citation gain once team size is fixed, but departments do move into research areas related to "
        f"what they already do (ROC AUC {D['layers']['areas']['auc']:.2f}, against {first_num(D['layers']['areas']['null']):.2f} for shuffled areas)."]

    # ---------------- partners
    part = by_inst(rd("partners.csv"))
    D["partners"] = {i: [{"partner": r["partner"], "shared": int(r["shared_papers"]), "cluster": r["cluster"],
                          "cross": r["cross_cluster"] == "True", "jaccard": num(r["jaccard_top20"]),
                          "cites_in": int(r["citations_from_partner"]), "cites_out": int(r["citations_to_partner"])}
                         for r in part[i][:15]] for i in INSTS}
    D["clusters"] = [{"inst": r["institution"], "cluster": r["cluster"], "cross": r["cross_cluster"] == "True",
                      "partners": int(r["partners"]), "shared": int(r["shared_papers"])} for r in rd("cluster_summary.csv")]
    D["jaccard"] = [{"inst": r["institution"], "partner": r["partner"], "shared": int(r["shared_papers"]),
                     "j": float(r["jaccard_top20"]), "cluster": r["cluster"]} for r in rd("jaccard_topics.csv")]

    # ---------------- citation network panel: the most influential papers (PageRank) and the papers citing them
    pm = {r["node"]: r for r in rd("paper_citation_metrics.csv")}
    titles, nauth = {}, {}
    rid = {(r["institution"], r["faculty"], r["department"]): r["roster_id"] for r in fac}
    plist, pidx, fpapers = [], {}, C.defaultdict(list)       # per-faculty paper lists -> papers.js (loaded on demand)
    venues, types = {}, {}                                  # stored once; papers refer to them by index
    for r in rd("group3_data.csv", OUT):
        for k in (r["openalex_id"], (r["doi"] or "").lower()):
            if k and k not in titles:
                titles[k] = (r["title"], r["journal_name"])
        if r["doi"]:
            nauth[r["doi"].lower()] = num(r["n_authors"], int)
        key = (r["doi"] or "").lower() or r["record_id"]
        if key not in pidx:
            pidx[key] = len(plist)
            plist.append([r["title"], num(r["year"], int), venues.setdefault(r["journal_name"], len(venues)),
                          num(r["citations"], int), (r["doi"] or "").replace("https://doi.org/", ""),
                          num(r["n_authors"], int), types.setdefault(r["type"], len(types))])
        f = rid.get((r["institution"], r["author"], r["department"]))
        if f and pidx[key] not in fpapers[f]:
            fpapers[f].append(pidx[key])
    for rows in D["most_cited"].values():
        for p in rows:
            p["na"] = nauth.get((p["doi"] or "").lower())
    for f in fpapers:
        fpapers[f].sort(key=lambda k: -(plist[k][3] or 0))
    pjs = "window.PAPERS = " + json.dumps({"p": plist, "f": fpapers, "v": list(venues), "t": list(types)}, ensure_ascii=False, separators=(",", ":")) + ";\n"
    open(os.path.join(HERE, "papers.js"), "w", encoding="utf8").write(pjs)
    print(f"papers.js {len(pjs) / 1e6:.2f} MB, {len(plist)} papers, {len(fpapers)} faculty")
    yfn = os.path.join(RES, "faculty_by_year.csv")
    if os.path.exists(yfn):
        D["fac_years"] = {i: {"listed": [int(r["faculty_listed"]) for r in rows], "snaps": [int(r["snapshots_used"]) for r in rows]}
                          for i, rows in by_inst(rd("faculty_by_year.csv")).items()}
    full = nx.DiGraph()
    for e in rd("citation_network.csv", OUT):
        if e["edge_type"] != "internal":
            continue
        s = e["source_openalex"] or e["source_doi"].lower()
        t = e["target_openalex"] or e["target_doi"].lower()
        if s in pm and t in pm and s != t:
            full.add_edge(s, t)
    hubs = sorted((n for n in pm if n in full), key=lambda n: -float(pm[n]["pagerank_cluster"]))[:N_HUBS]
    keep = set(hubs)
    for h in hubs:
        keep |= set(full.predecessors(h))                    # papers in our corpus that cite a hub
    G = full.subgraph(keep).copy()
    top = {n: pm[n] for n in G}
    D["citation_graph_hubs"] = hubs
    pos = packed_layout(G.to_undirected())
    nodes = []
    for n, r in top.items():
        t = titles.get(n) or titles.get((r["doi"] or "").lower()) or ("(title unavailable)", "")
        nodes.append({"id": n, "x": round(pos[n][0] * 1000, 1), "y": round(pos[n][1] * 1000, 1), "title": t[0], "journal": t[1],
                      "year": int(r["year"]), "insts": r["institutions"], "pr": float(r["pagerank_cluster"]),
                      "indeg": int(r["in_degree_cluster"]), "cites": num(r["global_citations"], int), "doi": r["doi"]})
    D["citation_graph"] = {"nodes": nodes, "edges": [[s, t] for s, t in G.edges]}

    # ---------------- faculty co-authorship network (faculty with >= 1 faculty co-author)
    w = C.Counter()
    for e in rd("authorship_network.csv", OUT):
        if e["a_is_faculty"] == "TRUE" and e["b_is_faculty"] == "TRUE":
            a, b = sorted((e["author_a_id"], e["author_b_id"]))
            w[(a, b, e["paper_doi"] or e["year"])] += 1
    pairs = C.Counter((a, b) for a, b, _ in w)
    F = nx.Graph()
    for (a, b), k in pairs.items():
        if a in cent and b in cent:
            F.add_edge(a, b, weight=k)
    pos = nx.spring_layout(F, seed=3, k=1.1 / math.sqrt(F.number_of_nodes()), iterations=250, weight=None)
    hidx = {r["roster_id"]: int(r["h_index"]) for r in fac}
    D["faculty_graph"] = {
        "nodes": [{"id": v, "x": round(pos[v][0] * 1000, 1), "y": round(pos[v][1] * 1000, 1), "name": cent[v]["faculty"],
                   "inst": cent[v]["institution"], "dept": cent[v]["department"], "deg": F.degree(v),
                   "community": int(cent[v]["community"]), "betw": float(cent[v]["betweenness"]), "h": hidx.get(v, 0)}
                  for v in F],
        "edges": [[a, b, d["weight"], cent[a]["institution"] != cent[b]["institution"]] for a, b, d in F.edges(data=True)]}

    js = "window.DASH = " + json.dumps(D, ensure_ascii=False, separators=(",", ":")) + ";\n"
    open(os.path.join(HERE, "data.js"), "w", encoding="utf8").write(js)
    print(f"data.js {len(js) / 1e6:.2f} MB | citation graph {G.number_of_nodes()} nodes / {G.number_of_edges()} edges | "
          f"faculty graph {F.number_of_nodes()} nodes / {F.number_of_edges()} edges")


if __name__ == "__main__":
    main()
