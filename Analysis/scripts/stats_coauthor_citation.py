"""Who cites their own co-authors, and does citing come before working together (research_directions.md §3b;
Wallace, Lariviere & Gingras 2012, PLoS ONE 7, e33339; Martin, Ball, Karrer & Newman 2013, PRE 88, 012814).
Two layers on the same faculty (results/faculty.csv; faculty_layers.py):
  co-authorship  faculty a and b wrote a paper together (papers with at most MAX_AUTHORS authors, the rule of the
                 faculty network in stats_authorship.py; faculty credited as in faculty.csv)
  citation       a cites b, in two definitions:
                 'pure'   a is not an author of the cited paper and b is not an author of the citing paper
                 'strict' also the citing and cited paper share no author at all (no faculty, no OpenAlex author id),
                          so a citation that a shared third co-author may have made is not counted
1. Citation rate by co-authorship distance d (1 = co-authors, 2 = a common faculty co-author, 3, 'far' = 4 or more /
   not connected). Rate = share of ordered pairs (a, b) where a cites b at least once. Co-authors share departments,
   topics and are productive, so the rate is compared with what 'far' pairs of the same kind show: strata = same
   department / same institute, other department / other institute x same main subfield x a's paper count band x
   b's paper count band (terciles). O/E = observed citing pairs at d / expected (pairs at d in each stratum x the
   far-pair rate of that stratum). O/E = 1: no co-author effect.
2. Order in time, two tests at the end of SPLIT_YEAR (both faculty active: a paper up to SPLIT_YEAR and one after):
   (a) pairs not co-authors by then: do pairs where one cited the other start writing together more often later?
   (b) pairs with no citation by then: do co-authors start citing each other more often later?
   Both as raw rates and as O/E against the same strata (unordered pairs: paper bands as low/high). Plus, for pairs
   with no contact at all up to NEW_PAIR_UNTIL, which came first: the first citation or the first joint paper
   (descriptive: our window starts in 2016).
3. Reciprocity of the citation layer: share of citing pairs (a -> b) where b also cites a, against the directed
   configuration model (same in- and out-degrees; analytic expectation and RANDOM_GRAPHS degree-preserving rewirings).
4. Institute inwardness (Baccini, De Nicolao & Petrovich 2019, PLoS ONE 14, e0221212), institute level only:
   citations a paper gets from papers of the same institute in our set / all its OpenAlex citations, by publication
   year; split into author self-citations (citing and cited paper share an author) and others. A lower bound: our
   set holds only verified, in-scope papers, and OpenAlex reference lists are incomplete.
Checks (printed and in coauthor_citation_summary.csv): faculty citation count by a second route (paper x faculty
incidence matrices), co-author edges vs stats_authorship.faculty_graph, distances vs networkx on sampled sources.
Outputs (results/): coauthor_citation_distance.csv, coauthor_citation_precedence.csv, coauthor_citation_summary.csv,
  institute_inwardness.csv
Figures: coauthor_citation_distance.png, institute_inwardness.png
usage: python stats_coauthor_citation.py"""
import collections as C
import numpy as np
import networkx as nx
import scipy.sparse as sp
from scipy.sparse.csgraph import shortest_path
from common import INSTS, YEARS, write_csv, style, save, COLOR, plt
from faculty_layers import faculty_table, paper_table, citation_edges, faculty_citations, main_subfield
from stats_authorship import faculty_graph

MAX_AUTHORS = 50
SPLIT_YEAR = 2020
NEW_PAIR_UNTIL = 2018
RANDOM_GRAPHS = 10
SEED = 7
DCLASS = ["1", "2", "3", "far"]


def band(x, cuts):
    return int(np.searchsorted(cuts, x, side="right"))


def o_over_e(outcome, strata, mask, ref):
    """Observed count in mask, expected from the reference rate of each stratum."""
    obs = int(outcome[mask].sum())
    exp = float(sum(ref.get(s, 0.0) * k for s, k in zip(*np.unique(strata[mask], return_counts=True))))
    return obs, exp


def main():
    style()
    F = faculty_table()
    fac = sorted(F)
    ix = {a: i for i, a in enumerate(fac)}
    n = len(fac)
    ok = set(fac)
    P = paper_table()
    E = citation_edges(P)
    shared = {(u, v): bool(P[u]["authors"] & P[v]["authors"] or P[u]["fac"] & P[v]["fac"]) for u, v in E}
    cit_all = faculty_citations(P, E, ok, pure=False)
    defs = {"pure": faculty_citations(P, E, ok)}
    defs["strict"] = [c for c in defs["pure"] if not shared[(c[2], c[3])]]
    summ = [("faculty", n), ("papers", len(P)), ("internal citation pairs (paper -> paper)", len(E)),
            ("faculty citations, all (a on citing paper, b on cited paper, a != b)", len(cit_all)),
            ("faculty citations, pure", len(defs["pure"])), ("faculty citations, strict", len(defs["strict"]))]

    # ---- second route for the faculty citation count: (paper x faculty)' A (paper x faculty), off-diagonal
    keys = list(P)
    pk = {k: i for i, k in enumerate(keys)}
    rows, cols = zip(*[(pk[k], ix[a]) for k in keys for a in P[k]["fac"] & ok])
    Fm = sp.csr_matrix((np.ones(len(rows)), (rows, cols)), shape=(len(keys), n))
    u, v = zip(*E)
    A = sp.csr_matrix((np.ones(len(E)), ([pk[x] for x in u], [pk[x] for x in v])), shape=(len(keys), len(keys)))
    W = (Fm.T @ A @ Fm).toarray()
    check_all = int(W.sum() - np.trace(W))
    summ.append(("check: faculty citations (all) by matrix route", check_all))
    assert check_all == len(cit_all), (check_all, len(cit_all))

    # ---- co-authorship layer (papers <= MAX_AUTHORS authors), first joint year
    first_co = {}
    for p in P.values():
        fs = sorted(p["fac"] & ok)
        if len(fs) < 2 or not p["n_auth"] or p["n_auth"] > MAX_AUTHORS:
            continue
        for i, a in enumerate(fs):
            for b in fs[i + 1:]:
                first_co[(a, b)] = min(first_co.get((a, b), 9999), p["year"])
    Gf, _ = faculty_graph()
    ref_edges = {tuple(sorted(e)) for e in Gf.edges}
    summ += [("co-author pairs (faculty, papers <= 50 authors)", len(first_co)),
             ("check: co-author pairs in stats_authorship.faculty_graph", len(ref_edges)),
             ("check: pairs in one but not the other (faculty.csv credits both on the paper, the authorship file matched "
              "only one of them to an author slot)", len(ref_edges ^ set(first_co)))]
    co = sp.lil_matrix((n, n))
    for a, b in first_co:
        co[ix[a], ix[b]] = co[ix[b], ix[a]] = 1
    D = shortest_path(co.tocsr(), unweighted=True, directed=False)
    G = nx.Graph()
    G.add_nodes_from(range(n))
    G.add_edges_from((ix[a], ix[b]) for a, b in first_co)
    rng = np.random.default_rng(SEED)
    diff = 0
    for s in rng.choice(n, 50, replace=False):
        L = nx.single_source_shortest_path_length(G, int(s))
        diff += sum(1 for t in range(n) if (L.get(t, np.inf) != D[s, t]))
    summ.append(("check: distances differing from networkx (50 sampled sources)", diff))

    # ---- strata
    dept = np.array([F[a]["institution"] + "|" + F[a]["department"] for a in fac])
    inst = np.array([F[a]["institution"] for a in fac])
    msub = main_subfield(P, ok)
    sub = np.array([msub.get(a, "") for a in fac])
    npap = np.array([int(F[a]["papers"]) for a in fac])
    cuts = np.quantile(npap, [1 / 3, 2 / 3])
    pb = np.array([band(x, cuts) for x in npap])
    summ.append(("paper-count bands (terciles): cut points", f"{cuts[0]:.0f}, {cuts[1]:.0f}"))
    # ordered pairs
    I, J = np.where(~np.eye(n, dtype=bool))
    d = D[I, J]
    dc = np.where(d == 1, "1", np.where(d == 2, "2", np.where(d == 3, "3", "far")))
    same_dept, same_inst = dept[I] == dept[J], inst[I] == inst[J]
    same_sub = (sub[I] == sub[J]) & (sub[I] != "")
    stratum = (np.where(same_dept, 2, np.where(same_inst, 1, 0)) * 2 + same_sub) * 9 + pb[I] * 3 + pb[J]
    far = dc == "far"
    scopes = {"all pairs": np.ones(len(I), bool), "same department": same_dept,
              "same institute, other department": same_inst & ~same_dept, "other institute": ~same_inst}
    summ.append(("share of ordered faculty pairs that are co-authors", round(float((d == 1).mean()), 5)))
    # unordered pairs of faculty active before and after SPLIT_YEAR
    yrs = C.defaultdict(set)
    for p in P.values():
        for a in p["fac"] & ok:
            yrs[a].add(p["year"])
    active = np.array([any(y <= SPLIT_YEAR for y in yrs[a]) and any(y > SPLIT_YEAR for y in yrs[a]) for a in fac])
    iu, ju = np.triu_indices(n, 1)
    keep = active[iu] & active[ju]
    iu, ju = iu[keep], ju[keep]
    FCO = np.full((n, n), 9999, dtype=np.int32)             # first joint year per pair, as a matrix (no list of n^2/2 tuples)
    for (a_, b_), y_ in first_co.items():
        FCO[ix[a_], ix[b_]] = FCO[ix[b_], ix[a_]] = y_
    fco = FCO[iu, ju]
    sd = np.where(dept[iu] == dept[ju], 2, np.where(inst[iu] == inst[ju], 1, 0))
    ss = (sub[iu] == sub[ju]) & (sub[iu] != "")
    st = (sd * 2 + ss) * 9 + np.minimum(pb[iu], pb[ju]) * 3 + np.maximum(pb[iu], pb[ju])
    summ.append((f"faculty active before and after {SPLIT_YEAR}", int(active.sum())))

    drows, prow = [], []
    for defn, cl in defs.items():
        cited = np.zeros((n, n), bool)
        ncit = np.zeros((n, n), np.int32)
        first_cite = {}
        FCI = np.full((n, n), 9999, dtype=np.int32)
        for a, b, _, _, y in cl:
            i, j = ix[a], ix[b]
            cited[i, j] = True
            ncit[i, j] += 1
            k = (min(a, b), max(a, b))
            first_cite[k] = min(first_cite.get(k, 9999), y)
            FCI[i, j] = FCI[j, i] = first_cite[k]

        # ---- 1. distance
        cy = cited[I, J]
        ref = {s: cy[far & (stratum == s)].mean() for s in np.unique(stratum[far])}
        for scope, m in scopes.items():
            for c in DCLASS:
                mm = m & (dc == c)
                if not mm.any():
                    continue
                obs, exp = o_over_e(cy, stratum, mm, ref)
                drows.append({"definition": defn, "scope": scope, "coauthor_distance": c, "ordered_pairs": int(mm.sum()),
                              "pairs_citing": obs, "citing_rate": round(obs / int(mm.sum()), 5),
                              "citations_per_pair": round(float(ncit[I[mm], J[mm]].mean()), 4),
                              "expected_citing_pairs": round(exp, 1), "obs_over_expected": round(obs / exp, 2) if exp else ""})
        summ.append((f"{defn}: share of faculty citations that go to a co-author",
                     round(sum(1 for a, b, *_ in cl if D[ix[a], ix[b]] == 1) / len(cl), 4)))

        # ---- 2. order in time
        fci = FCI[iu, ju]

        def test(name, base, exposed, outcome):
            ref_ = {s: outcome[base & ~exposed & (st == s)].mean() for s in np.unique(st[base & ~exposed])}
            for grp, m in (("yes", base & exposed), ("no", base & ~exposed)):
                obs, exp = o_over_e(outcome, st, m, ref_)
                prow.append({"definition": defn, "test": name, "exposed": grp, "pairs": int(m.sum()),
                             "pairs_with_outcome": obs, "rate": round(obs / int(m.sum()), 5) if m.sum() else "",
                             "expected_same_strata": round(exp, 1), "obs_over_expected": round(obs / exp, 2) if exp else ""})

        test(f"(a) not co-authors by {SPLIT_YEAR}: exposed = one cited the other by {SPLIT_YEAR}; outcome = first joint "
             f"paper {SPLIT_YEAR + 1}-2026", fco > SPLIT_YEAR, fci <= SPLIT_YEAR, (fco > SPLIT_YEAR) & (fco < 9999))
        test(f"(b) no citation by {SPLIT_YEAR}: exposed = co-authors by {SPLIT_YEAR}; outcome = first citation "
             f"{SPLIT_YEAR + 1}-2026", fci > SPLIT_YEAR, fco <= SPLIT_YEAR, (fci > SPLIT_YEAR) & (fci < 9999))
        newp = [p for p in set(first_co) & set(first_cite) if min(first_co[p], first_cite[p]) > NEW_PAIR_UNTIL]
        order = C.Counter("citation first" if first_cite[p] < first_co[p] else "same year" if first_cite[p] == first_co[p]
                          else "joint paper first" for p in newp)
        for k in ("citation first", "same year", "joint paper first"):
            prow.append({"definition": defn, "test": f"(c) pairs with no contact up to {NEW_PAIR_UNTIL} that later both "
                         f"co-author and cite: which came first", "exposed": k, "pairs": len(newp),
                         "pairs_with_outcome": order[k], "rate": round(order[k] / len(newp), 4) if newp else ""})

        # ---- 3. reciprocity
        DG = nx.DiGraph()
        DG.add_nodes_from(fac)
        DG.add_edges_from(sorted({(a, b) for a, b, *_ in cl}))      # sorted: seeded rewiring is then reproducible
        L = DG.number_of_edges()
        rec = sum(1 for a, b in DG.edges if DG.has_edge(b, a)) / L
        x = np.array([DG.out_degree(a) * DG.in_degree(a) for a in fac], float)
        exp_rec = float((x.sum() ** 2 - (x ** 2).sum()) / L ** 2) / L     # sum_{i!=j} (ko_i ki_j / L)(ko_j ki_i / L) / L
        sims = []
        for g in range(RANDOM_GRAPHS):
            R = DG.copy()
            nx.directed_edge_swap(R, nswap=3 * L, max_tries=100 * L, seed=SEED + g)
            sims.append(sum(1 for a, b in R.edges if R.has_edge(b, a)) / L)
        ce = [(a, b) for a, b in DG.edges if (min(a, b), max(a, b)) in first_co]
        ne = [(a, b) for a, b in DG.edges if (min(a, b), max(a, b)) not in first_co]
        summ += [(f"{defn}: citing pairs a -> b", L),
                 (f"{defn}: reciprocity (share of a -> b with b -> a)", round(rec, 4)),
                 (f"{defn}: reciprocity expected, configuration model (analytic)", round(exp_rec, 4)),
                 (f"{defn}: reciprocity, {RANDOM_GRAPHS} degree-preserving rewirings: mean (min-max)",
                  f"{np.mean(sims):.4f} ({min(sims):.4f}-{max(sims):.4f})"),
                 (f"{defn}: citing pairs that are co-author pairs", len(ce)),
                 (f"{defn}: reciprocity among co-author pairs", round(sum(DG.has_edge(b, a) for a, b in ce) / len(ce), 4)),
                 (f"{defn}: reciprocity among pairs that never co-authored", round(sum(DG.has_edge(b, a) for a, b in ne) / len(ne), 4))]
    write_csv("coauthor_citation_distance.csv", drows)
    write_csv("coauthor_citation_precedence.csv", prow)

    # ---- 4. institute inwardness by publication year
    irows = []
    for name in INSTS.values():
        inc = C.defaultdict(lambda: [0, 0])
        for u, v in E:
            if name in P[u]["insts"] and name in P[v]["insts"]:
                inc[v][0 if shared[(u, v)] else 1] += 1
        for y in YEARS + ["all"]:
            ps = [k for k, p in P.items() if name in p["insts"] and (y == "all" or p["year"] == y) and p["cites_oa"] is not None]
            tot = sum(P[k]["cites_oa"] for k in ps)
            s_, o_ = sum(inc[k][0] for k in ps), sum(inc[k][1] for k in ps)
            over = sum(1 for k in ps if sum(inc[k]) > P[k]["cites_oa"])
            irows.append({"institution": name, "publication_year": y, "papers": len(ps), "openalex_citations": tot,
                          "same_institute_citations": s_ + o_, "of_which_author_self": s_, "of_which_other": o_,
                          "inwardness": round((s_ + o_) / tot, 4) if tot else "",
                          "inwardness_without_author_self": round(o_ / tot, 4) if tot else "",
                          "papers_with_more_internal_than_total (check)": over})
    write_csv("institute_inwardness.csv", irows)
    write_csv("coauthor_citation_summary.csv", [{"metric": k, "value": v} for k, v in summ])

    for k, v in summ:
        print(f"{k}: {v}")
    for r in drows + prow + [r for r in irows if r["publication_year"] == "all"]:
        print({k: v for k, v in r.items() if k != "test"}, r.get("test", "")[:40])

    # ---- figures
    fig, ax = plt.subplots(figsize=(7.2, 3.6))
    sc = [s for s in scopes if s != "all pairs"]
    w = 0.26
    for k, s in enumerate(sc):
        rs = [r for r in drows if r["scope"] == s and r["definition"] == "strict"]
        ax.bar([DCLASS.index(r["coauthor_distance"]) + (k - 1) * w for r in rs], [100 * r["citing_rate"] for r in rs],
               width=w, color=["#0d366b", "#3987e5", "#86b6ef"][k], label=s)
    ax.set_xticks(range(4), ["co-authors", "2 steps", "3 steps", "4+ / none"])
    ax.set_ylabel("% of faculty pairs where\nA cites B (log scale)")
    ax.set_yscale("log")
    ax.set_title("Faculty cite their co-authors far more often (strict: papers share no author)")
    ax.legend()
    save(fig, "coauthor_citation_distance.png")

    fig, ax = plt.subplots(figsize=(7.2, 3.4 if len(INSTS) <= 2 else 5))
    for name in INSTS.values():
        rs = [r for r in irows if r["institution"] == name and r["publication_year"] != "all" and r["inwardness"] != ""]
        ax.plot([r["publication_year"] for r in rs], [100 * r["inwardness"] for r in rs], color=COLOR[name], marker="o",
                markersize=4, label=name)
        ax.plot([r["publication_year"] for r in rs], [100 * r["inwardness_without_author_self"] for r in rs],
                color=COLOR[name], ls="--", lw=1.4)
    ax.set_ylabel("% of a paper's citations from\nits own institute (our set)")
    ax.set_xlabel("publication year (dashed: without author self-citations)")
    ax.set_title("Institute inwardness")
    ax.legend(ncol=1 if len(INSTS) <= 4 else 2, fontsize=9 if len(INSTS) <= 4 else 6)
    save(fig, "institute_inwardness.png")


if __name__ == "__main__":
    main()
