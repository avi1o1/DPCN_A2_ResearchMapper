"""Matrix-function centralities (second round): Katz, HITS, subgraph centrality, communicability, dynamic communicability.
All of them count walks in the network, weighted by length, so they look further than degree and differently from
PageRank (Estrada & Higham 2010, SIAM Rev. 52, 696; Benzi & Klymko 2015, SIAM J. Matrix Anal. Appl. 36, 686).
1. Paper citation network (the same graph as stats_citation.py: internal citations between our analysis-set papers).
   in-degree, PageRank (0.85), Katz and HITS authorities/hubs. Katz score of paper j = sum over k >= 1 of a^k times the
   number of citation chains of length k that end at j, with a = KATZ_F / rho (rho = spectral radius; the graph is not a
   pure DAG because of mutual citations, so rho >= 1 and is computed exactly on the strongly connected components).
   Out-of-sample test: every centrality is computed on the network as it was at the end of TEST_YEAR (papers and
   citations up to that year) and compared with the worldwide citations the paper got later (OpenAlex counts_by_year,
   TEST_YEAR+1 .. 2026). Spearman is taken inside each publication year (so paper age cannot drive it) and averaged;
   'top 1% hit rate' = share of a metric's top 1% that is in the top 1% of later citations.
   Does a score add anything once a paper's worldwide citations up to TEST_YEAR are known? Checked two ways:
   partial Spearman (ranks, linear effect of past citations removed), and plain Spearman inside bands of equal
   publication year and equal past citations. Internal citations are also split into self-citations (definition of
   stats_citation_dynamics.py) and the rest.
2. Faculty co-authorship network (the graph of stats_authorship.py, unweighted A).
   eigenvector localisation: inverse participation ratio IPR = sum v_i^4 of the leading eigenvector (1/n = spread
   evenly, 1 = one node). Katz at a = f / lambda_1 for several f: f -> 0 gives the degree ranking, f -> 1 the
   eigenvector ranking. Subgraph centrality SC_i = [e^A]_ii (closed walks), total communicability TC_i = [e^A 1]_i.
   Communicability G = e^A. Raw G_pq is dominated by the lambda_1 term (lambda_1 - lambda_2 is large), so campuses and
   departments are compared with the communicability angle cos = G_pq / sqrt(G_pp G_qq).
   Campus ratio rho_KR = mean G_KR / sqrt(mean G_KK mean G_RR), and the share of it lost when one faculty member is
   removed (recomputed for every faculty member). With more than two institutes in the run the communicability angle is
   given for every institute pair, and the ratio and the removal test are done for the pair with the most direct
   co-author ties between them (K = the first, R = the second institute of that pair).
3. Dynamic communicability (Grindrod, Parsons, Higham & Estrada 2011, Phys. Rev. E 83, 046120): one co-authorship
   graph per year A_t; Q = prod_t (I - a A_t)^-1 counts walks that respect time (a later step uses a later or the same
   year). Broadcast b = Q 1 (who can start chains that reach many others later), receive r = Q' 1.
   a = DYN_F / max_t rho(A_t); Q is rescaled after each year (ranking unchanged).
Outputs (results/): citation_centrality_top10.csv, citation_centrality_test.csv, citation_centrality_summary.csv,
  faculty_matrix_centrality.csv, faculty_matrix_summary.csv, faculty_katz_path.csv, campus_communicability.csv,
  department_communicability.csv, cross_campus_removal.csv, dynamic_communicability_top.csv
Figures: katz_interpolation.png, cross_campus_removal.png, centrality_prediction.png
usage: python stats_matrix_centrality.py"""
import os, json, itertools, collections as C
import numpy as np
import networkx as nx
import scipy.sparse as sp
from scipy.sparse.linalg import svds, expm_multiply
from scipy.stats import spearmanr, rankdata
from common import INSTS, CACHE, DATA, RES, read_csv, iter_csv, write_csv, style, save, COLOR, TEXT2, MUTED, plt, N_INST, oa_have, note_skip
from stats_citation import citation_graph
from stats_authorship import faculty_graph

KATZ_F = 0.5          # Katz a = KATZ_F / rho for the citation network
TEST_YEAR = 2020
FUTURE = [str(y) for y in range(TEST_YEAR + 1, 2027)]
KATZ_PATH = [0.01, 0.1, 0.3, 0.5, 0.7, 0.9, 0.99]
DYN_F = 0.5
TOP = 10
SUPPORT_ONLY = {"HITS authority"}     # scores that are zero outside one part of the graph: compared on their support
BANDS = [(5, 10), (10, 20), (20, 40), (40, 80), (80, 10 ** 9)]     # past worldwide citations, for the band check


# ---------------------------------------------------------------- helpers
def spectral_radius(A):
    """Exact spectral radius of a sparse non-negative matrix: max over its strongly connected components."""
    n_c, lab = sp.csgraph.connected_components(A, directed=True, connection="strong")
    rho = 0.0
    for c in np.flatnonzero(np.bincount(lab) > 1):
        idx = np.flatnonzero(lab == c)
        rho = max(rho, float(np.max(np.abs(np.linalg.eigvals(A[idx][:, idx].toarray())))))
    return rho


def katz_in(A, a, iters=500):
    """Katz score of incoming walks: sum_{k>=1} a^k (A^T)^k 1."""
    x, term, AT = np.zeros(A.shape[0]), np.ones(A.shape[0]), A.T.tocsr()
    for _ in range(iters):
        term = a * (AT @ term)
        x += term
        if term.max() < 1e-12:
            break
    return x


def on_support(v, rel=1e-10):
    """A Perron-type vector from a numerical solver: (|v| with entries below rel * max set to exactly 0, whether the
    kept entries all have one sign). On a disconnected graph the vector lives on one part; the rest is solver noise,
    which must not be ranked."""
    keep = np.abs(v) > rel * np.abs(v).max()
    one_sign = bool(np.all(v[keep] > 0) or np.all(v[keep] < 0))
    return np.where(keep, np.abs(v), 0.0), one_sign


def hits(A):
    """(hubs, authorities, info) = leading singular vectors of A (A[s, t] = 1 when s cites t). info: s1/s2 (a value
    near 1 means the leading pair is not well separated), support sizes, sign check."""
    u, s, vt = svds(A.astype(float), k=2, random_state=0)
    i = int(np.argmax(s))
    hub, ok_h = on_support(u[:, i])
    auth, ok_a = on_support(vt[i])
    return hub, auth, {"s1/s2": round(float(s.max() / s.min()), 4), "hub support": int((hub > 0).sum()),
                       "authority support": int((auth > 0).sum()), "one sign": ok_h and ok_a}


def ranks_spearman(x, y):
    return float(spearmanr(x, y).statistic)


def partial_spearman(x, y, z):
    """Spearman correlation of x and y after removing the linear effect of z from both ranks."""
    rx, ry, rz = (rankdata(v) for v in (x, y, z))
    res = [r - np.polyval(np.polyfit(rz, r, 1), rz) for r in (rx, ry)]
    return float(np.corrcoef(*res)[0, 1])


def citation_metrics(G, nodes):
    idx = {n: i for i, n in enumerate(nodes)}
    A = nx.to_scipy_sparse_array(G, nodelist=nodes, format="csr", dtype=float)
    rho = spectral_radius(A)
    a = KATZ_F / rho
    hub, auth, info = hits(A)
    pr = nx.pagerank(G, alpha=0.85)
    m = {"in-degree": np.asarray(A.sum(axis=0)).ravel(), "PageRank": np.array([pr[n] for n in nodes]),
         "Katz": katz_in(A, a), "HITS authority": auth}
    return m, hub, rho, a, info


# ---------------------------------------------------------------- 1. citation network
def citation_part():
    G, meta, _ = citation_graph()
    nodes = list(G)
    m, hub, rho, a, info = citation_metrics(G, nodes)
    year = np.array([meta[n]["year"] for n in nodes])
    glob = np.array([meta[n]["citations"] if meta[n]["citations"] is not None else -1 for n in nodes])
    summ = [{"metric": "papers (nodes)", "value": len(nodes)}, {"metric": "citations (edges)", "value": G.number_of_edges()},
            {"metric": "spectral radius rho", "value": round(rho, 4)}, {"metric": "Katz a", "value": round(a, 4)},
            {"metric": "papers with Katz score > 0 (cited at least once)", "value": int((m["Katz"] > 0).sum())}]
    summ += [{"metric": f"HITS: {k}", "value": v} for k, v in info.items()]
    known = glob >= 0
    names = list(m)
    # HITS is zero outside its support (solver noise removed); comparisons with it use its support only. Zeros of
    # in-degree / Katz are real (uncited papers) and stay in.
    def sup(k):
        return m[k] > 0 if k in SUPPORT_ONLY else np.ones(len(nodes), bool)
    for k in names:
        top100 = np.argsort(-m[k])[:100]
        s = sup(k) & known
        summ += [{"metric": f"{k}: Spearman with worldwide citations (n = {int(s.sum())})",
                  "value": round(ranks_spearman(m[k][s], glob[s]), 3)},
                 {"metric": f"{k}: top-100 share from 2016-2017", "value": round(float(np.mean(year[top100] <= 2017)), 3)}]
    for i, k in enumerate(names):
        for k2 in names[i + 1:]:
            s = sup(k) & sup(k2)
            summ.append({"metric": f"Spearman {k} vs {k2} (n = {int(s.sum())})", "value": round(ranks_spearman(m[k][s], m[k2][s]), 3)})
    # HITS authorities concentrate on one dense group (the 'tightly knit community' effect, Lempel & Moran 2000):
    # field mix and the faculty member with most papers in each top 100
    fname = {f["roster_id"]: f"{f['faculty']} ({f['institution']})" for f in read_csv(os.path.join(RES, "faculty.csv"))}
    for k in names:
        top100 = [nodes[i] for i in np.argsort(-m[k])[:100]]
        f = C.Counter(meta[p]["field"] or "unknown" for p in top100)
        who = C.Counter(fid for p in top100 for fid in meta[p]["faculty"])
        summ += [{"metric": f"{k}: top-100 most common field", "value": f"{f.most_common(1)[0][0]} ({f.most_common(1)[0][1]})"},
                 {"metric": f"{k}: top-100 papers of the most frequent faculty member",
                  "value": f"{who.most_common(1)[0][1]} ({fname.get(who.most_common(1)[0][0], who.most_common(1)[0][0])})"}]
    # citation cycles (mutual citations): they set rho and so the largest allowed Katz a
    scc = sorted((c for c in nx.strongly_connected_components(G) if len(c) > 1), key=len, reverse=True)
    summ += [{"metric": "citation cycles: strongly connected groups of >= 2 papers", "value": len(scc)},
             {"metric": "papers inside citation cycles", "value": sum(map(len, scc))}]
    if scc:
        who = C.Counter(fid for p in scc[0] for fid in meta[p]["faculty"])
        summ.append({"metric": "largest cycle group: papers, citations, faculty",
                     "value": f"{len(scc[0])}, {G.subgraph(scc[0]).number_of_edges()}, "
                              + "; ".join(f"{fname.get(k_, k_)} {c}" for k_, c in who.most_common(2))})
    write_csv("citation_centrality_summary.csv", summ)

    trows = []
    m["HITS hub"] = hub
    for k, v in m.items():
        for r, i in enumerate(np.argsort(-v)[:TOP], 1):
            n = nodes[i]
            trows.append({"metric": k, "rank": r, "score": f"{v[i]:.6g}", "in_degree": int(m["in-degree"][i]),
                          "out_degree": G.out_degree(n), "year": meta[n]["year"], "title": meta[n]["title"],
                          "journal": meta[n]["venue"], "field": meta[n]["field"], "global_citations": meta[n]["citations"],
                          "institutions": "; ".join(sorted(meta[n]["insts"])), "doi": meta[n]["doi"]})
    write_csv("citation_centrality_top10.csv", trows)

    # ---- out-of-sample: network at the end of TEST_YEAR -> citations received afterwards
    if not oa_have("counts_by_year"):
        note_skip("stats_matrix_centrality.py", "citation centrality out-of-sample test (citation_centrality_test.csv, centrality_prediction.png)",
                  "needs the worldwide citations each paper received per year (OpenAlex counts_by_year), not cached for these institutes",
                  "fetch_openalex_extra.py (OpenAlex credits): oa_counts_by_year.json")
        return summ, []
    cby = json.load(open(os.path.join(CACHE, "oa_counts_by_year.json"), encoding="utf-8"))
    old = [n for n in nodes if meta[n]["year"] <= TEST_YEAR]
    H = G.subgraph(old)
    mh, _, rho_h, a_h, info_h = citation_metrics(H, old)
    yr = np.array([meta[n]["year"] for n in old])
    fut = np.array([sum((cby.get(n) or {}).get(y, 0) for y in FUTURE) if n in cby and cby[n] is not None else -1 for n in old])
    past = np.array([sum(v for y, v in (cby.get(n) or {}).items() if int(y) <= TEST_YEAR) if n in cby and cby[n] is not None else -1
                     for n in old])
    # internal citations by TEST_YEAR split into self-citations (citing and cited paper share an OpenAlex author or a
    # faculty member, the definition of stats_citation_dynamics.py) and the rest
    selfc = np.array([sum(1 for s in H.predecessors(n) if meta[s]["authors"] & meta[n]["authors"] or meta[s]["faculty"] & meta[n]["faculty"])
                      for n in old], float)
    mh["internal self-citations by test year"] = selfc
    mh["internal non-self citations by test year"] = mh["in-degree"] - selfc
    mh["worldwide citations up to test year (baseline)"] = past.astype(float)
    ok = fut >= 0
    test = []
    top = max(1, int(0.01 * ok.sum()))
    for k, v in mh.items():
        nonzero = int(np.sum(v[ok] > 0))
        if k in SUPPORT_ONLY and nonzero < top:      # e.g. HITS: lives on a few papers, cannot rank the rest
            test.append({"metric": k, "papers": int(ok.sum()), "papers_with_nonzero_score": nonzero,
                         "note": f"not rankable: non-zero for only {nonzero} papers (fewer than the top 1% = {top})"})
            continue
        per = [ranks_spearman(v[ok & (yr == y)], fut[ok & (yr == y)]) for y in range(2016, TEST_YEAR + 1)]
        # partial Spearman given the baseline: does the score add anything once past worldwide citations are known?
        part = [partial_spearman(v[ok & (yr == y)], fut[ok & (yr == y)], past[ok & (yr == y)]) for y in range(2016, TEST_YEAR + 1)]
        # second check of the same question without a linear model: Spearman inside bands of equal publication year
        # and equal past worldwide citations (bands with >= 50 papers), weighted by band size
        band = []
        for y in range(2016, TEST_YEAR + 1):
            for lo, hi in BANDS:
                sel = ok & (yr == y) & (past >= lo) & (past < hi)
                if sel.sum() >= 50 and np.std(v[sel]) > 0:
                    band.append((ranks_spearman(v[sel], fut[sel]), sel.sum()))
        band = np.array(band)
        sel = np.flatnonzero(ok)
        best = set(sel[np.argsort(-fut[sel])[:top]])
        mine = set(sel[np.argsort(-v[sel])[:top]])
        test.append({"metric": k, "papers": int(ok.sum()), "papers_with_nonzero_score": nonzero,
                     "spearman_within_year_mean": round(float(np.mean(per)), 3),
                     "partial_spearman_given_past_citations": round(float(np.mean(part)), 3) if "baseline" not in k else "",
                     "spearman_within_year_and_past_band": round(float(np.average(band[:, 0], weights=band[:, 1])), 3)
                     if "baseline" not in k and len(band) else "",
                     "bands_used": len(band) if "baseline" not in k else "",
                     "bands_negative": int(np.sum(band[:, 0] < 0)) if "baseline" not in k and len(band) else "",
                     **{f"spearman_{y}": round(p, 3) for y, p in zip(range(2016, TEST_YEAR + 1), per)},
                     "top1pct_hit_rate": round(len(best & mine) / top, 3)})
    test.append({"metric": f"(network up to {TEST_YEAR}: rho {rho_h:.3f}, Katz a {a_h:.3f}; HITS s1/s2 {info_h['s1/s2']}, "
                           f"authority support {info_h['authority support']}, one sign {info_h['one sign']})", "papers": len(old)})
    cols = ["metric", "papers", "papers_with_nonzero_score", "note", "spearman_within_year_mean",
            "partial_spearman_given_past_citations", "spearman_within_year_and_past_band", "bands_used", "bands_negative",
            *[f"spearman_{y}" for y in range(2016, TEST_YEAR + 1)], "top1pct_hit_rate"]
    write_csv("citation_centrality_test.csv", test, cols)

    style()
    fig, ax = plt.subplots(figsize=(7.5, 3.2))
    rows = [t for t in test if "spearman_within_year_mean" in t]
    lab = {"internal self-citations by test year": f"self-citations by {TEST_YEAR}",
           "internal non-self citations by test year": f"other internal citations by {TEST_YEAR}",
           "worldwide citations up to test year (baseline)": f"worldwide citations by {TEST_YEAR}"}
    ax.barh([lab.get(t["metric"], t["metric"]) for t in rows][::-1],
            [t["spearman_within_year_mean"] for t in rows][::-1], color=COLOR["IIT Kharagpur"])
    ax.set_xlabel(f"Spearman with citations received {FUTURE[0]}-{FUTURE[-1]} (mean within publication year)")
    ax.set_title(f"Which score, computed at the end of {TEST_YEAR}, predicts later citations?")
    ax.grid(axis="y", visible=False)
    save(fig, "centrality_prediction.png")
    return summ, test


# ---------------------------------------------------------------- 2. faculty co-authorship network
def faculty_part():
    G, info = faculty_graph()
    nodes = sorted(G)
    n = len(nodes)
    A = nx.to_numpy_array(G, nodelist=nodes, weight=None)
    lam, V = np.linalg.eigh(A)
    l1 = lam[-1]
    v1, v1_one_sign = on_support(V[:, -1])          # zero outside the component that carries lambda_1
    deg = A.sum(axis=1)
    ipr = float(np.sum(v1 ** 4))
    eA = (V * np.exp(lam - l1)) @ V.T                 # e^A scaled by e^-lambda1 (ranking and ratios unchanged)
    sc, tc = np.diag(eA), eA.sum(axis=1)
    bc = {r["roster_id"]: float(r["betweenness"]) for r in read_csv(os.path.join(RES, "faculty_centrality.csv"))}
    btw = np.array([bc[v] for v in nodes])

    # rank comparisons use the giant component only: outside it the eigenvector is exactly 0 for everyone, and
    # Katz / communicability scores of small components are not comparable with the giant component
    gc = max(nx.connected_components(G), key=len)
    g = np.array([v in gc for v in nodes])
    katz = {}
    for f in KATZ_PATH:
        katz[f] = np.linalg.solve(np.eye(n) - (f / l1) * A, np.ones(n)) - 1
    path = [{"f (a = f / lambda_1)": f, "faculty (giant component)": int(g.sum()),
             "spearman_vs_degree": round(ranks_spearman(katz[f][g], deg[g]), 3),
             "spearman_vs_eigenvector": round(ranks_spearman(katz[f][g], v1[g]), 3)} for f in KATZ_PATH]
    write_csv("faculty_katz_path.csv", path)

    top_v = np.argsort(-v1)[:TOP]
    inst = np.array([info[v]["institution"] for v in nodes])
    dept = np.array([info[v]["department"] or "unknown" for v in nodes])
    metrics = {"degree": deg, "betweenness": btw, "eigenvector": v1, "Katz (f=0.5)": katz[0.5],
               "subgraph centrality": sc, "total communicability": tc}
    summ = [{"metric": "faculty (nodes)", "value": n}, {"metric": "edges", "value": int(A.sum() / 2)},
            {"metric": "lambda_1", "value": round(float(l1), 3)}, {"metric": "lambda_2", "value": round(float(lam[-2]), 3)},
            {"metric": "sqrt(max degree)", "value": round(float(np.sqrt(deg.max())), 3)},
            {"metric": "eigenvector: faculty with a non-zero score (its component)", "value": int((v1 > 0).sum())},
            {"metric": "eigenvector: one sign on its support (check)", "value": v1_one_sign},
            {"metric": "eigenvector IPR", "value": round(ipr, 4)}, {"metric": "IPR if spread evenly (1/n)", "value": round(1 / n, 5)},
            {"metric": "eigenvector weight (sum v^2) on its top 10 faculty", "value": round(float(np.sum(v1[top_v] ** 2)), 3)},
            {"metric": "eigenvector top 10: institutions", "value": "; ".join(f"{k} {c}" for k, c in C.Counter(inst[top_v]).most_common())},
            {"metric": "eigenvector top 10: departments", "value": "; ".join(f"{k} {c}" for k, c in C.Counter(dept[top_v]).most_common())}]
    names = list(metrics)
    for i, k in enumerate(names):
        for k2 in names[i + 1:]:
            summ.append({"metric": f"Spearman {k} vs {k2} (giant component, n = {int(g.sum())})",
                         "value": round(ranks_spearman(metrics[k][g], metrics[k2][g]), 3)})
        summ.append({"metric": f"{k}: top-10 overlap with degree top-10",
                     "value": len(set(np.argsort(-metrics[k])[:TOP]) & set(np.argsort(-deg)[:TOP]))})
    rows = [{"roster_id": v, "faculty": info[v]["name"], "institution": info[v]["institution"], "department": info[v]["department"],
             "degree": int(deg[i]), "betweenness": round(btw[i], 5), "eigenvector": round(float(v1[i]), 6),
             "katz_f0.5": round(float(katz[0.5][i]), 5), "subgraph_centrality_rel": f"{sc[i]:.4g}",
             "total_communicability_rel": f"{tc[i]:.4g}"} for i, v in enumerate(nodes)]
    for k in names:
        rk = rankdata(-metrics[k], method="min")      # ties (e.g. zeros) share the best rank of their group
        for i, r in enumerate(rows):
            r[f"rank_{k}"] = int(rk[i])
    rows.sort(key=lambda r: r["rank_total communicability"])
    write_csv("faculty_matrix_centrality.csv", rows)

    # ---- where the leading eigenvector sits: localisation on the densest core (lambda_1 > sqrt(k_max) means a
    # dense core, not one hub, sets lambda_1; Pastor-Satorras & Castellano 2016, Sci. Rep. 6, 18847)
    inames = list(INSTS.values())
    lab = lambda nm: nm.replace("IIT ", "")                   # 'Kharagpur', 'Roorkee', ...
    if N_INST == 2:
        K = inst == inames[0]
        R = ~K
        nK, nR = inames
    else:                                                     # the pair of institutes with the most direct co-author ties
        direct = {(a_, b_): int(A[np.ix_(inst == a_, inst == b_)].sum()) for a_, b_ in itertools.combinations(inames, 2)}
        nK, nR = max(direct, key=lambda k: (direct[k], -inames.index(k[0]), -inames.index(k[1])))
        K, R = inst == nK, inst == nR
    core = nx.core_number(G)
    kmax = max(core.values())
    kcore = {i for i, v in enumerate(nodes) if core[v] == kmax}
    if N_INST == 2:
        summ += [{"metric": f"share of eigenvector weight (sum v^2) on {lab(nR)} faculty", "value": round(float(np.sum(v1[R] ** 2)), 4)},
                 {"metric": f"{lab(nR)} share of faculty", "value": round(float(R.mean()), 4)}]
    else:
        summ += [{"metric": f"share of eigenvector weight (sum v^2) on {nm} faculty", "value": round(float(np.sum(v1[inst == nm] ** 2)), 4)}
                 for nm in inames]
        summ += [{"metric": f"{nm} share of faculty", "value": round(float((inst == nm).mean()), 4)} for nm in inames]
    summ += [
            {"metric": "max k-core: k, faculty, institutions",
              "value": f"{kmax}, {len(kcore)}, " + "; ".join(f"{k} {c}" for k, c in C.Counter(inst[list(kcore)]).most_common())},
             {"metric": "eigenvector top 10 inside the max k-core", "value": len(kcore & set(top_v.tolist()))}]

    # ---- communicability angle cos(theta_pq) = G_pq / sqrt(G_pp G_qq) (Estrada & Hatano 2016, SIAM Rev. 58, 692).
    # Raw G_pq is dominated by the lambda_1 term, so it mostly repeats the eigenvector; the angle removes that.
    # Means are over faculty in the giant component (other pairs have no walk at all, cos = 0).
    d = np.sqrt(np.diag(eA))
    cos = eA / np.outer(d, d)
    off = ~np.eye(n, dtype=bool)

    def mean_cos(a_, b_):
        m = np.ix_(a_ & g, b_ & g)
        return cos[m][off[m]]

    crow = []
    if N_INST == 2:
        pairs = ((K, K, f"{lab(nK)} - {lab(nK)}"), (R, R, f"{lab(nR)} - {lab(nR)}"), (K, R, f"{lab(nK)} - {lab(nR)}"))
    else:
        masks = {nm: inst == nm for nm in inames}
        pairs = [(masks[a_], masks[a_], f"{lab(a_)} - {lab(a_)}") for a_ in inames] + \
                [(masks[a_], masks[b_], f"{lab(a_)} - {lab(b_)}") for a_, b_ in itertools.combinations(inames, 2)]
    for a_, b_, label in pairs:
        c = mean_cos(a_, b_)
        if not c.size:
            continue
        crow.append({"pair": label, "faculty_in_giant_component": f"{int((a_ & g).sum())} x {int((b_ & g).sum())}",
                     "direct_coauthor_pairs": int(A[np.ix_(a_, b_)].sum() / (2 if a_ is b_ else 1)),
                     "mean_cos_angle": round(float(c.mean()), 4), "median_cos_angle": round(float(np.median(c)), 4)})
    write_csv("campus_communicability.csv", crow)
    unit = np.array([f"{i_}|{d_}" for i_, d_ in zip(inst, dept)])     # a department of one institute
    big = sorted(u for u, c in C.Counter(unit[g]).items() if c >= 5 and not u.endswith("|unknown"))
    drows = []
    for i, d1 in enumerate(big):
        for d2 in big[i + 1:]:
            a_, b_ = unit == d1, unit == d2
            drows.append({"department_1": d1.split("|")[1], "institution_1": d1.split("|")[0],
                          "department_2": d2.split("|")[1], "institution_2": d2.split("|")[0],
                          "faculty_in_giant_1": int((a_ & g).sum()), "faculty_in_giant_2": int((b_ & g).sum()),
                          "direct_coauthor_pairs": int(A[np.ix_(a_, b_)].sum()),
                          "mean_cos_angle": round(float(mean_cos(a_, b_).mean()), 4)})
    drows.sort(key=lambda r: -r["mean_cos_angle"])
    write_csv("department_communicability.csv", drows)

    # ---- campus communicability ratio rho_KR = mean G_KR / sqrt(mean G_KK * mean G_RR) (means over all pairs,
    # p = q included), and how much of it is lost when one faculty member is removed (who links the two campuses,
    # beyond sitting in a dense core)
    S = sp.csr_matrix(A)

    def campus_ratio(M, keep):
        k, r = (K & keep).astype(float), (R & keep).astype(float)
        Ek, Er = expm_multiply(M, np.column_stack([k, r])).T
        nk, nr = k.sum(), r.sum()
        return (k @ Er / (nk * nr)) / np.sqrt((k @ Ek / nk ** 2) * (r @ Er / nr ** 2))

    base = campus_ratio(S, np.ones(n, bool))
    lost = np.zeros(n)
    for i in np.flatnonzero(deg > 0):
        T = S.tolil(copy=True)
        T[i, :] = 0
        T[:, i] = 0
        keep = np.ones(n, bool)
        keep[i] = False
        lost[i] = 1 - campus_ratio(T.tocsr(), keep) / base
    rrows = []
    for r_, i in enumerate(np.argsort(-lost)[:20], 1):
        rrows.append({"rank": r_, "faculty": info[nodes[i]]["name"], "institution": inst[i], "department": dept[i],
                      "campus_ratio_lost": round(float(lost[i]), 4), "degree": int(deg[i]),
                      "rank_betweenness": rows_rank(btw, i), "rank_degree": rows_rank(deg, i),
                      "direct_cross_campus_coauthors": int(A[i, R].sum() if K[i] else A[i, K].sum())})
    write_csv("cross_campus_removal.csv", rrows)
    rk = "rho_KR" if N_INST == 2 else f"rho ({lab(nK)} vs {lab(nR)})"
    summ += [{"metric": f"campus communicability ratio {rk}", "value": round(float(base), 4)},
             {"metric": f"{rk} lost by removing the single most important faculty member", "value": round(float(lost.max()), 4)},
             {"metric": f"faculty whose removal lowers {rk} by more than 5%", "value": int(np.sum(lost > 0.05))},
             {"metric": f"Spearman of {rk} loss with betweenness (faculty with degree > 0)",
              "value": round(ranks_spearman(lost[deg > 0], btw[deg > 0]), 3)},
             {"metric": f"top-10 overlap: {rk} loss vs betweenness",
              "value": len(set(np.argsort(-lost)[:TOP]) & set(np.argsort(-btw)[:TOP]))}]
    write_csv("faculty_matrix_summary.csv", summ)

    style()
    fig, ax = plt.subplots(figsize=(6.5, 3.2))
    ax.plot(KATZ_PATH, [p["spearman_vs_degree"] for p in path], marker="o", color=COLOR["IIT Kharagpur"], label="vs degree")
    ax.plot(KATZ_PATH, [p["spearman_vs_eigenvector"] for p in path], marker="o", color=COLOR["IIT Roorkee"], label="vs eigenvector")
    ax.set_xlabel(r"Katz parameter $a\,\lambda_1$")
    ax.set_ylabel("Spearman rank correlation")
    ax.set_title("Katz moves from degree to eigenvector ranking")
    ax.legend()
    save(fig, "katz_interpolation.png")

    fig, ax = plt.subplots(figsize=(6.5, 3.4))
    has = lost > 0
    for name, sel in ((nK, K), (nR, R)):
        ax.scatter(btw[has & sel], lost[has & sel] * 100, s=10, color=COLOR[name], alpha=0.7, label=name)
    ax.legend(loc="upper left")
    ax.set_xscale("symlog", linthresh=1e-4)
    ax.set_xlabel("betweenness")
    ax.set_ylabel("% of campus communicability ratio lost")
    ax.set_title("Removing one faculty member: who links the campuses?" if N_INST == 2 else f"Removing one faculty member: who links {lab(nK)} and {lab(nR)}?")
    save(fig, "cross_campus_removal.png")
    return G, info, nodes, deg


def rows_rank(x, i):
    return int(np.sum(x > x[i]) + 1)


# ---------------------------------------------------------------- 3. dynamic communicability
def dynamic_part(G, info, nodes, deg):
    pos = {v: i for i, v in enumerate(nodes)}
    n = len(nodes)
    yearly = C.defaultdict(set)
    for e in iter_csv(os.path.join(DATA, "authorship_network.csv")):
        a, b = e["author_a_id"], e["author_b_id"]
        if e["a_is_faculty"] == "TRUE" and e["b_is_faculty"] == "TRUE" and a in pos and b in pos and a != b and e["year"]:
            yearly[int(e["year"])].add((pos[a], pos[b]))
    years = sorted(y for y in yearly if 2016 <= y <= 2026)
    def mat(y):                                    # one yearly matrix at a time (11 dense n x n matrices do not fit for n = 4,000+)
        M = np.zeros((n, n))
        for i, j in yearly[y]:
            M[i, j] = M[j, i] = 1
        return M

    rho = max(float(np.max(np.linalg.eigvalsh(mat(y)))) for y in years)
    a = DYN_F / rho
    Q = np.eye(n)
    for y in years:
        Q = Q @ np.linalg.inv(np.eye(n) - a * mat(y))
        Q /= np.linalg.norm(Q)
    np.fill_diagonal(Q, 0)
    bcast, recv = Q.sum(axis=1), Q.sum(axis=0)
    first = {}
    for y in years:
        for i, j in yearly[y]:
            first.setdefault(i, y)
            first.setdefault(j, y)
    rows = []
    for k, v in (("broadcast", bcast), ("receive", recv)):
        for r, i in enumerate(np.argsort(-v)[:20], 1):
            rows.append({"measure": k, "rank": r, "faculty": info[nodes[i]]["name"], "institution": info[nodes[i]]["institution"],
                         "department": info[nodes[i]]["department"], "score_rel": round(float(v[i] / v.max()), 4),
                         "degree_all_years": int(deg[i]), "rank_degree": rows_rank(deg, i),
                         "first_faculty_coauthorship_year": first.get(i, "")})
    act = deg > 0                                  # faculty without a faculty co-author tie at zero: left out
    rows.append({"measure": f"(a = {a:.4f}, max yearly rho {rho:.3f}; faculty with degree > 0: {int(act.sum())}; "
                            f"Spearman broadcast vs degree {ranks_spearman(bcast[act], deg[act]):.3f}, "
                            f"broadcast vs receive {ranks_spearman(bcast[act], recv[act]):.3f})"})
    write_csv("dynamic_communicability_top.csv", rows)
    return rows


def main():
    print("citation network ...", flush=True)
    summ, test = citation_part()
    for s in summ:
        print(s)
    for t in test:
        print(t)
    print("faculty network ...", flush=True)
    G, info, nodes, deg = faculty_part()
    for r in read_csv(os.path.join(RES, "faculty_matrix_summary.csv")):
        print(r)
    print("dynamic communicability ...", flush=True)
    for r in dynamic_part(G, info, nodes, deg)[:10]:
        print(r)


if __name__ == "__main__":
    main()
