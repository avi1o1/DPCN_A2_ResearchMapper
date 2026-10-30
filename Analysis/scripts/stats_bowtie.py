"""Core and periphery of the faculty citation network (research_directions.md §3c).
The paper citation network is almost a DAG (papers cite older papers), so its strongly connected core is tiny. Built
up to faculty, citation cycles appear (a cites b in one year, b cites a later), so the bow-tie picture of directed
networks applies (Broder et al. 2000, Comput. Netw. 33, 309; studied further by Timar, Goltsev, Dorogovtsev & Mendes
2017, PRL 118, 078301). Faculty network: a -> b when faculty a cites faculty b (faculty_layers.py, 'pure' citations;
'strict' as a check). Edge a -> b means knowledge flows from b to a.
  CORE      the largest strongly connected component: every member reaches every other along citation chains
  IN        faculty with a citation chain into the core that the core does not return: they draw on the core
  OUT       faculty the core cites (directly or through others) who do not cite back into it: sources of the core
  TUBES     reached from IN and reaching OUT without passing the core
  TENDRILS  hang off IN or OUT only
  OTHER     in other weakly connected parts; ISOLATED: no pure faculty citation at all
Null model: RANDOM_GRAPHS degree-preserving rewirings (same in- and out-degree for everyone): core size by chance.
Growth: the same decomposition on the network of citations made up to each year.
Departments: weighted citation flows between departments (pure faculty citations, departments with at least MIN_FAC
faculty). SpringRank (De Bacco, Larremore & Moore 2018, Sci. Adv. 4, eaar8260) places departments on one line so that
departments that are cited sit above those that cite them; checked against the simpler net balance (in - out)/(in + out).
Checks: core found by networkx and by scipy (strongly connected components); IN / OUT by both libraries.
Outputs (results/): bowtie_summary.csv, bowtie_faculty.csv, bowtie_growth.csv, bowtie_departments.csv,
  department_citation_hierarchy.csv
Figure: bowtie_growth.png
usage: python stats_bowtie.py"""
import collections as C
import numpy as np
import networkx as nx
import scipy.sparse as sp
from scipy.sparse.csgraph import connected_components, breadth_first_order
from scipy.stats import spearmanr
from common import INSTS, write_csv, style, save, COLOR, plt, N_INST
from faculty_layers import faculty_table, paper_table, citation_edges, faculty_citations

RANDOM_GRAPHS = 10
SEED = 11
MIN_FAC = 5
PARTS = ["CORE", "IN", "OUT", "TUBES", "TENDRILS", "OTHER", "ISOLATED"]


def bowtie(G):
    """node -> part, and the core set."""
    core = max(nx.strongly_connected_components(G), key=len)
    c0 = next(iter(core))
    out = nx.descendants(G, c0) | {c0}
    inn = nx.ancestors(G, c0) | {c0}
    IN, OUT = inn - core, out - core
    from_in = set().union(*(nx.descendants(G, x) for x in IN)) - core - OUT - IN if IN else set()
    to_out = set().union(*(nx.ancestors(G, x) for x in OUT)) - core - OUT - IN if OUT else set()
    wcc = next(c for c in nx.weakly_connected_components(G) if c0 in c)
    part = {}
    for v in G:
        if v in core:
            part[v] = "CORE"
        elif v in IN:
            part[v] = "IN"
        elif v in OUT:
            part[v] = "OUT"
        elif v in from_in and v in to_out:
            part[v] = "TUBES"
        elif v in wcc:
            part[v] = "TENDRILS"
        elif G.degree(v) == 0:
            part[v] = "ISOLATED"
        else:
            part[v] = "OTHER"
    return part, core


def springrank(A):
    """SpringRank scores s (A[i, j] = times i is placed above j); least-squares solution, centred at 0."""
    dout, din = A.sum(1), A.sum(0)
    M = np.diag(dout + din) - (A + A.T)
    s = np.linalg.lstsq(M, dout - din, rcond=None)[0]
    return s - s.mean()


def main():
    style()
    F = faculty_table()
    fac = sorted(F)
    P = paper_table()
    E = citation_edges(P)
    pure = faculty_citations(P, E, set(fac))
    shared = {(u, v): bool(P[u]["authors"] & P[v]["authors"] or P[u]["fac"] & P[v]["fac"]) for u, v in E}
    defs = {"pure": pure, "strict": [c for c in pure if not shared[(c[2], c[3])]]}
    summ, frows = [], []
    for defn, cl in defs.items():
        G = nx.DiGraph()
        G.add_nodes_from(fac)
        G.add_edges_from(sorted({(a, b) for a, b, *_ in cl}))      # sorted: seeded rewiring is then reproducible
        part, core = bowtie(G)
        cnt = C.Counter(part.values())
        # second route: scipy strong components and BFS on the adjacency matrix
        ix = {a: i for i, a in enumerate(fac)}
        Am = nx.to_scipy_sparse_array(G, nodelist=fac, format="csr")
        _, lab = connected_components(Am, directed=True, connection="strong")
        big = np.bincount(lab).argmax()
        core2 = {fac[i] for i in np.where(lab == big)[0]}
        c0 = ix[next(iter(core))]
        out2 = {fac[i] for i in breadth_first_order(Am, c0, directed=True, return_predecessors=False)} - core2
        in2 = {fac[i] for i in breadth_first_order(Am.T.tocsr(), c0, directed=True, return_predecessors=False)} - core2
        same = core2 == core and out2 == {v for v in fac if part[v] == "OUT"} and in2 == {v for v in fac if part[v] == "IN"}
        sims = []
        for g in range(RANDOM_GRAPHS):
            R = G.copy()
            nx.directed_edge_swap(R, nswap=3 * R.number_of_edges(), max_tries=100 * R.number_of_edges(), seed=SEED + g)
            sims.append(len(max(nx.strongly_connected_components(R), key=len)))
        active = sum(1 for v in fac if G.degree(v) > 0)
        summ += [{"definition": defn, "metric": "faculty", "value": len(fac)},
                 {"definition": defn, "metric": "faculty with at least one citation link (either direction)", "value": active},
                 {"definition": defn, "metric": "citing pairs between the two IITs" if N_INST == 2 else f"citing pairs between institutes (of {N_INST})",
                  "value": sum(1 for a, b in G.edges if F[a]["institution"] != F[b]["institution"])},
                 {"definition": defn, "metric": "CORE members citing or cited by the other IIT within the CORE" if N_INST == 2 else "CORE members citing or cited by another institute's faculty within the CORE",
                  "value": len({x for a, b in G.subgraph(core).edges if F[a]["institution"] != F[b]["institution"] for x in (a, b)})},
                 {"definition": defn, "metric": "citing pairs a -> b", "value": G.number_of_edges()}]
        summ += [{"definition": defn, "metric": f"{p} (faculty)", "value": cnt[p]} for p in PARTS]
        summ += [{"definition": defn, "metric": "CORE share of linked faculty", "value": round(cnt["CORE"] / active, 4)},
                 {"definition": defn, "metric": f"CORE size in {RANDOM_GRAPHS} degree-preserving rewirings: mean (min-max)",
                  "value": f"{np.mean(sims):.0f} ({min(sims)}-{max(sims)})"},
                 {"definition": defn, "metric": "check: networkx and scipy give the same CORE, IN and OUT", "value": same}]
        for name in INSTS.values():
            sel = [v for v in fac if F[v]["institution"] == name]
            for p in PARTS:
                summ.append({"definition": defn, "metric": f"{name}: {p}", "value": sum(1 for v in sel if part[v] == p)})
        if defn == "pure":
            pure_part, Gp = part, G
            for v in fac:
                frows.append({"roster_id": v, "faculty": F[v]["faculty"], "institution": F[v]["institution"],
                              "department": F[v]["department"], "part": part[v], "cites_faculty": G.out_degree(v),
                              "cited_by_faculty": G.in_degree(v), "papers": F[v]["papers"], "citations": F[v]["citations"],
                              "h_index": F[v]["h_index"], "part_strict": ""})
        else:
            for r in frows:
                r["part_strict"] = part[r["roster_id"]]
    # who sits where: medians of papers / citations / h by part (pure)
    for p in PARTS:
        rs = [r for r in frows if r["part"] == p]
        if rs:
            summ += [{"definition": "pure", "metric": f"{p}: median {k}", "value": float(np.median([int(r[k]) for r in rs]))}
                     for k in ("papers", "citations", "h_index")]
    write_csv("bowtie_faculty.csv", sorted(frows, key=lambda r: (PARTS.index(r["part"]), -int(r["cited_by_faculty"]))))

    # ---- growth: decomposition of the network of citations made up to year Y (pure)
    grows = []
    for Y in range(2017, 2027):
        G = nx.DiGraph()
        G.add_nodes_from(fac)
        G.add_edges_from(sorted({(a, b) for a, b, _, _, y in pure if y <= Y}))
        part, _ = bowtie(G)
        cnt = C.Counter(part.values())
        active = sum(1 for v in fac if G.degree(v) > 0)
        grows.append({"up_to_year": Y, "citing_pairs": G.number_of_edges(), "linked_faculty": active,
                      **{p: cnt[p] for p in PARTS}, "core_share_of_linked": round(cnt["CORE"] / active, 4) if active else ""})
    write_csv("bowtie_growth.csv", grows)

    # ---- departments: share of each department's faculty in each part (pure)
    drows = []
    by_d = C.defaultdict(list)
    for r in frows:
        by_d[(r["institution"], r["department"])].append(r)
    for (inst, d), rs in sorted(by_d.items(), key=lambda x: -len(x[1])):
        c = C.Counter(r["part"] for r in rs)
        drows.append({"institution": inst, "department": d, "faculty": len(rs), **{p: c[p] for p in PARTS},
                      "core_share": round(c["CORE"] / len(rs), 3)})
    write_csv("bowtie_departments.csv", drows)

    # ---- department citation hierarchy (SpringRank) on weighted pure citations between departments
    depts = sorted(k for k, rs in by_d.items() if len(rs) >= MIN_FAC)
    di = {k: i for i, k in enumerate(depts)}
    dkey = {v: (F[v]["institution"], F[v]["department"]) for v in fac}
    W = np.zeros((len(depts), len(depts)))          # W[x, y] = citations from department x to department y
    within = C.Counter()
    for a, b, *_ in pure:
        x, y = dkey[a], dkey[b]
        if x == y:
            within[x] += 1
        elif x in di and y in di:
            W[di[x], di[y]] += 1
    s = springrank(W.T)                              # y is placed above x when x cites y
    cin, cout = W.sum(0), W.sum(1)
    bal = np.where(cin + cout > 0, (cin - cout) / np.maximum(cin + cout, 1), 0)
    rho = spearmanr(s, bal).statistic
    hrows = [{"institution": k[0], "department": k[1], "faculty": len(by_d[k]), "springrank": round(float(s[i]), 3),
              "cited_by_other_departments": int(cin[i]), "cites_other_departments": int(cout[i]),
              "net_balance": round(float(bal[i]), 3), "citations_within_department": within[k],
              "within_share_of_received": round(float(within[k] / (within[k] + cin[i])), 3) if within[k] + cin[i] else ""}
             for i, k in enumerate(depts)]
    hrows.sort(key=lambda r: -r["springrank"])
    write_csv("department_citation_hierarchy.csv", hrows)
    summ += [{"definition": "pure", "metric": f"departments in the hierarchy (>= {MIN_FAC} faculty)", "value": len(depts)},
             {"definition": "pure", "metric": "check: Spearman SpringRank vs net balance", "value": round(float(rho), 3)},
             {"definition": "pure", "metric": "citations between departments (weighted edges)", "value": int(W.sum())},
             {"definition": "pure", "metric": "citations within a department", "value": sum(within.values())}]
    write_csv("bowtie_summary.csv", summ)
    for r in summ:
        print(r["definition"], "|", r["metric"], "|", r["value"])
    for r in grows:
        print(r)
    for r in hrows[:8] + hrows[-8:]:
        print(r)

    fig, ax = plt.subplots(figsize=(7.2, 3.4))
    ys = [r["up_to_year"] for r in grows]
    bottom = np.zeros(len(ys))
    for p, col in zip(["CORE", "IN", "OUT", "TENDRILS", "OTHER"], ["#0d366b", "#3987e5", "#86b6ef", "#c9c8c3", "#e6e5e1"]):
        v = np.array([r[p] + (r["TUBES"] if p == "TENDRILS" else 0) for r in grows])
        ax.bar(ys, v, bottom=bottom, color=col, label=p if p != "TENDRILS" else "tendrils / tubes")
        bottom += v
    ax.set_ylabel("faculty")
    ax.set_xlabel("citations made up to year")
    ax.set_title("Faculty citation network: the strongly connected core grows")
    ax.set_ylim(0, 1.18 * bottom.max())
    ax.legend(ncol=5, loc="upper left")
    save(fig, "bowtie_growth.png")


if __name__ == "__main__":
    main()
