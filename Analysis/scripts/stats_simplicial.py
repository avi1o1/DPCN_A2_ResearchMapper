"""Simplicial closure (second round): do three people who have each written in pairs later write as a trio?
Follows Benson, Abebe, Schaub, Jadbabaie & Kleinberg (2018, PNAS 115, E11221), on our co-authorship data.
A paper with authors S is a simplex: every pair and every triple inside S is 'closed'. Only papers with at most CAP
authors are used (Benson et al. use 25), so one very large paper does not create thousands of trios; CAP = 10 (the
professor's split) is run as a check.
1. Where do triangles come from? In the pairwise co-author graph (an edge = the two wrote a paper together), a
   triangle is either closed (all three on one paper) or open (three pairs from different papers). Measured for all
   authors and for the faculty network of stats_authorship.py (all papers, no cap).
2. Closure over time: train = papers up to SPLIT, test = papers after SPLIT. Every triple of authors who all appear in
   the train period is put in one class by the number of pairs among them that wrote together in the train period
   (0, 1, 2 or 3 edges; 3 edges and no joint paper = open triangle). Closure probability = share of the class whose
   three members are all on one test paper. Open triangles are also split by their weakest edge (joint papers).
3. Prediction among open triangles: rank them by a score, compare with the triangles that closed. Average precision
   (area under the precision-recall curve) divided by the share that closed (= random ranking) and ROC AUC, with a
   one-sided Mann-Whitney p-value for AUC > 0.5. Closure probabilities have 95% Wilson intervals.
   Scores (Benson et al. Table 2 style): arithmetic, geometric and harmonic mean of the three edge weights, common
   neighbours of all three, sum of degrees.
Authors are the ids in authorship_network.csv (faculty by roster id, others by OpenAlex id or name). That file holds the
papers with at least one linked faculty member and at most 50 authors, with their full author lists.
'share_of_new_trios' = where the new trios come from (their split over the four classes), next to the probability.
Outputs (results/): simplicial_summary.csv, simplicial_closure_by_config.csv, simplicial_prediction.csv
Figure: simplicial_closure.png (closure probability by class, log scale, 95% Wilson intervals)
usage: python stats_simplicial.py"""
import os, math, collections as C, itertools as it
import numpy as np
import networkx as nx
from scipy.stats import mannwhitneyu
from sklearn.metrics import average_precision_score, roc_auc_score
from common import DATA, read_csv, write_csv, style, save, COLOR, plt
from stats_authorship import faculty_graph

CAP = 25
CHECK_CAP = 10
SPLIT = 2021


def wilson(k, n, z=1.96):
    """95% Wilson score interval for a proportion k / n."""
    if not n:
        return float("nan"), float("nan")
    p = k / n
    c = (p + z * z / (2 * n)) / (1 + z * z / n)
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n)
    return max(0.0, c - h), c + h


def load_papers(split_names=False):
    """Author set and year of every paper. split_names=True treats an author without OpenAlex or roster id (keyed by
    name in the network file) as a different person on every paper: a check that merged namesakes do not make
    triangles."""
    mem, yr = C.defaultdict(set), {}
    for e in read_csv(os.path.join(DATA, "authorship_network.csv")):
        p = e["paper_doi"]
        if p:
            ids = (e["author_a_id"], e["author_b_id"])
            if split_names:
                ids = tuple(a + "|" + p if not (a.startswith("A") and a[1:].isdigit()) and not a.startswith("iit_") else a
                            for a in ids)
            mem[p] |= set(ids)
            yr[p] = int(e["year"])
    return mem, yr


def projection(papers, mem):
    """Weighted pairwise graph (weight = joint papers) and the set of closed triples, from a list of papers."""
    G, closed = nx.Graph(), set()
    for p in papers:
        s = sorted(mem[p])
        for u, v in it.combinations(s, 2):
            G.add_edge(u, v, weight=G[u][v]["weight"] + 1 if G.has_edge(u, v) else 1)
        closed.update(it.combinations(s, 3))
    return G, closed


def triangles(G):
    out = []
    for u in G:
        nu = G[u]
        for v in nu:
            if v <= u:
                continue
            for w in set(nu) & set(G[v]):
                if w > v:
                    out.append((u, v, w))
    return out


def closure(mem, yr, cap):
    train = [p for p in mem if yr[p] <= SPLIT and len(mem[p]) <= cap]
    test = [p for p in mem if yr[p] > SPLIT and len(mem[p]) <= cap]
    G, closed = projection(train, mem)
    nodes = set(G)
    n = len(nodes)
    tri = triangles(G)
    open_tri = [t for t in tri if t not in closed]
    # number of train triples in each class (exact counts)
    T = len(tri)
    deg = dict(G.degree())
    W = sum(d * (d - 1) // 2 for d in deg.values()) - 3 * T           # triples with exactly 2 edges
    E1 = sum(n - 2 - (deg[u] - 1) - (deg[v] - 1) + len(set(G[u]) & set(G[v])) for u, v in G.edges())
    E0 = math.comb(n, 3) - T - W - E1
    # new trios in the test period among train authors, by class
    new = set()
    for p in test:
        s = sorted(a for a in mem[p] if a in nodes)
        new.update(t for t in it.combinations(s, 3) if t not in closed)
    by = C.Counter(sum(G.has_edge(a, b) for a, b in it.combinations(t, 2)) for t in new)
    rows = [{"cap": cap, "class": "0 edges", "triples": E0, "closed_later": by[0]},
            {"cap": cap, "class": "1 edge", "triples": E1, "closed_later": by[1]},
            {"cap": cap, "class": "2 edges (open wedge)", "triples": W, "closed_later": by[2]},
            {"cap": cap, "class": "3 edges, no joint paper (open triangle)", "triples": len(open_tri), "closed_later": by[3]}]
    y = np.array([t in new for t in open_tri])
    wmin = np.array([min(G[a][b]["weight"] for a, b in it.combinations(t, 2)) for t in open_tri])
    for lo, hi, lab in ((1, 2, "weakest edge 1 joint paper"), (2, 3, "weakest edge 2 joint papers"), (3, 10 ** 9, "weakest edge 3+ joint papers")):
        sel = (wmin >= lo) & (wmin < hi)
        rows.append({"cap": cap, "class": f"open triangle, {lab}", "triples": int(sel.sum()), "closed_later": int(y[sel].sum())})
    # probability per triple is not the same as where new trios come from: most triples have few prior pairs
    new_total = sum(r["closed_later"] for r in rows[:4])
    for r in rows[:4]:
        r["share_of_new_trios"] = round(r["closed_later"] / new_total, 4)
    for r in rows:
        r["closure_probability"] = f"{r['closed_later'] / r['triples']:.3g}" if r["triples"] else ""
        lo, hi = wilson(r["closed_later"], r["triples"])
        r["ci95_low"], r["ci95_high"] = f"{lo:.3g}", f"{hi:.3g}"
    return G, tri, closed, open_tri, y, rows, len(train), len(test)


def scores(G, open_tri):
    w = np.array([[G[a][b]["weight"] for a, b in it.combinations(t, 2)] for t in open_tri], float)
    common = [len(set(G[a]) & set(G[b]) & set(G[c])) for a, b, c in open_tri]
    deg = [sum(G.degree(x) for x in t) for t in open_tri]
    return {"arithmetic mean of edge weights": w.mean(axis=1), "geometric mean of edge weights": np.exp(np.log(w).mean(axis=1)),
            "harmonic mean of edge weights": 3 / (1 / w).sum(axis=1), "common neighbours of all three": np.array(common, float),
            "sum of degrees": np.array(deg, float)}


def main():
    mem, yr = load_papers()
    summ, crows, prows = [], [], []

    # 1. where triangles come from (all years)
    for cap in (CAP, CHECK_CAP):
        G, closed = projection([p for p in mem if len(mem[p]) <= cap], mem)
        tri = triangles(G)
        summ.append({"metric": f"all authors, papers <= {cap} authors, all years: triangles in the pairwise graph", "value": len(tri)})
        summ.append({"metric": f"all authors, papers <= {cap} authors, all years: share of triangles closed by one paper",
                     "value": round(sum(t in closed for t in tri) / len(tri), 4)})
    Gf, info = faculty_graph()
    ftri = triangles(Gf)
    fclosed = set()
    for p, s in mem.items():
        fs = sorted(a for a in s if a in info)
        fclosed.update(it.combinations(fs, 3))
    summ += [{"metric": "papers with >= 3 faculty (only these can close a faculty triangle in one paper)",
              "value": sum(1 for s in mem.values() if sum(a in info for a in s) >= 3)},
             {"metric": "faculty network (all papers): triangles", "value": len(ftri)},
             {"metric": "faculty network: share of triangles closed by one paper with all three faculty",
              "value": round(sum(t in fclosed for t in ftri) / len(ftri), 4) if ftri else ""}]

    # 2-3. closure over time and prediction
    for cap in (CAP, CHECK_CAP):
        G, tri, closed, open_tri, y, rows, ntr, nte = closure(mem, yr, cap)
        crows += rows
        summ += [{"metric": f"cap {cap}: train papers (<= {SPLIT}) / test papers (> {SPLIT})", "value": f"{ntr} / {nte}"},
                 {"metric": f"cap {cap}: open triangles at end of {SPLIT}", "value": len(open_tri)},
                 {"metric": f"cap {cap}: open triangles that became a joint paper after {SPLIT}", "value": int(y.sum())}]
        base = y.mean()
        for k, s in scores(G, open_tri).items():
            prows.append({"cap": cap, "score": k, "open_triangles": len(open_tri), "closed": int(y.sum()),
                          "random_precision": round(float(base), 4),
                          "average_precision": round(float(average_precision_score(y, s)), 4),
                          "ap_over_random": round(float(average_precision_score(y, s) / base), 2),
                          "roc_auc": round(float(roc_auc_score(y, s)), 3),
                          # one-sided Mann-Whitney test that closed triangles score higher (ROC AUC > 0.5)
                          "p_value_auc_above_half": f"{mannwhitneyu(s[y], s[~y], alternative='greater').pvalue:.3g}"})
    # check: name-keyed authors split per paper (cap CAP)
    mem2, yr2 = load_papers(split_names=True)
    G2, closed2 = projection([p for p in mem2 if len(mem2[p]) <= CAP], mem2)
    tri2 = triangles(G2)
    summ.append({"metric": f"check (names split): papers <= {CAP} authors, all years: share of triangles closed by one paper",
                 "value": round(sum(t in closed2 for t in tri2) / len(tri2), 4)})
    G2, _, _, open2, y2, rows2, _, _ = closure(mem2, yr2, CAP)
    for r in rows2[:4]:
        summ.append({"metric": f"check (names split): cap {CAP}: closure probability, {r['class']}",
                     "value": f"{r['closure_probability']} ({r['closed_later']} of {r['triples']})"})
    s2 = scores(G2, open2)["harmonic mean of edge weights"]
    summ.append({"metric": f"check (names split): cap {CAP}: harmonic mean score, ROC AUC (p)",
                 "value": f"{roc_auc_score(y2, s2):.3f} ({mannwhitneyu(s2[y2], s2[~y2], alternative='greater').pvalue:.3g})"})
    write_csv("simplicial_summary.csv", summ)
    write_csv("simplicial_closure_by_config.csv", crows)
    style()
    fig, ax = plt.subplots(figsize=(6.2, 3.2))
    labels = ["0", "1", "2", "3 (open\ntriangle)"]
    for cap, col, dx in ((CAP, COLOR["IIT Kharagpur"], -0.08), (CHECK_CAP, COLOR["IIT Roorkee"], 0.08)):
        rs = [r for r in crows if r["cap"] == cap][:4]
        p = np.array([float(r["closure_probability"]) for r in rs])
        lo, hi = np.array([float(r["ci95_low"]) for r in rs]), np.array([float(r["ci95_high"]) for r in rs])
        ax.errorbar(np.arange(4) + dx, p, yerr=[p - lo, hi - p], fmt="o", color=col, capsize=3,
                    label=f"papers with at most {cap} authors")
    ax.set_yscale("log")
    ax.set_xticks(range(4), labels)
    ax.set_xlabel(f"pairs among the three who had written together by {SPLIT}")
    ax.set_ylabel(f"chance of a joint paper\nafter {SPLIT}")
    ax.set_title("Trios form along existing pairs")
    ax.legend(loc="upper left")
    save(fig, "simplicial_closure.png")
    write_csv("simplicial_prediction.csv", prows)
    for r in summ + crows + prows:
        print(r)


if __name__ == "__main__":
    main()
