"""Co-authorship as a hypergraph (second round): a paper links all its authors at once, instead of one edge per pair.
Hypergraph H: nodes = every author in authorship_network.csv (faculty by roster id, others by OpenAlex id), one
hyperedge per paper (its full author set, at least 2 authors). B = node x paper incidence matrix. The file holds the
papers with at least one linked faculty member and at most 50 authors (Enrichment/scripts/build_networks.py), so the
> 10-author count here (696) is smaller than in group3_data.csv (979 distinct papers): 259 have no linked faculty,
23 have more than 50 authors, 1 has its faculty member not found in the author list.
Node and paper centrality = nonlinear eigenvector centrality of Tudisco & Higham (2021, Commun. Phys. 4, 201):
    lambda x = g(B f(y)),   mu y = psi(B' phi(x)),   x, y > 0,
computed with their nonlinear power method (Algorithm 1, ||x|| = ||y|| = 1 in the 2-norm), for their three models:
    linear   f = g = phi = psi = id          close to eigenvector centrality of the pairwise (clique) projection
    log-exp  f = id, g = sqrt, phi = ln, psi = exp
             a paper is worth the product of its authors' scores: small teams of central people count most
    max      f = g = id, phi = x^10, psi = x^(1/10)
             a paper is worth about its most central author: being on one important paper is enough
Faculty are compared across the models and with the pairwise view (distinct co-authors), and by how much of each
model's top 20 rests on papers with more than 10 authors (the professor's split). The linear model is also re-run
without those papers.
Outputs (results/): hypergraph_summary.csv, hypergraph_faculty.csv (every faculty member, all ranks),
  hypergraph_top_faculty.csv, hypergraph_top_papers.csv
usage: python stats_hypergraph.py"""
import os, collections as C
import numpy as np
import scipy.sparse as sp
from scipy.sparse.linalg import svds
from scipy.special import logsumexp
from scipy.stats import spearmanr, rankdata
from common import DATA, RES, read_csv, iter_csv, write_csv

LARGE = 10
ALPHA = 10                      # max model exponent (the paper's choice)
TOL, MAXIT = 1e-9, 5000
TOP = 20


def name_keyed(a):
    """True for authors without an OpenAlex id or roster id (the network file keys them by their name)."""
    return not (a.startswith("A") and a[1:].isdigit()) and not a.startswith("iit_")


def load_hypergraph(split_names=False):
    """(authors, papers, B, meta): incidence matrix over all authors and papers with >= 2 authors.
    split_names=True treats a name-keyed author as a different person on every paper (robustness check: a short name
    like 'R. Dutta' could otherwise join different people into one node)."""
    members, meta = C.defaultdict(set), {}
    for e in iter_csv(os.path.join(DATA, "authorship_network.csv")):
        p = e["paper_doi"]
        if not p:
            continue
        ids = (e["author_a_id"], e["author_b_id"])
        if split_names:
            ids = tuple(a + "|" + p if name_keyed(a) else a for a in ids)
        members[p] |= set(ids)
        meta[p] = {"year": e["year"], "n_authors": int(e["n_authors"]) if e["n_authors"].isdigit() else None}
    papers = sorted(p for p, s in members.items() if len(s) >= 2)
    authors = sorted(set().union(*(members[p] for p in papers)))
    ai = {a: i for i, a in enumerate(authors)}
    rows = [ai[a] for p in papers for a in members[p]]
    cols = [j for j, p in enumerate(papers) for _ in members[p]]
    B = sp.csr_matrix((np.ones(len(rows)), (rows, cols)), shape=(len(authors), len(papers)))
    return authors, papers, B, meta


def unit(v):
    return v / np.linalg.norm(v)


def npm(B, model):
    """Nonlinear power method (Tudisco & Higham 2021, Algorithm 1). Returns (x, y, iterations)."""
    n, m = B.shape
    BT = B.T.tocsr()
    size = np.asarray(B.sum(axis=0)).ravel()
    x, y = unit(np.ones(n)), unit(np.ones(m))
    for it in range(1, MAXIT + 1):
        if model == "linear":
            u = np.sqrt(x * (B @ y))
            v = np.sqrt(y * (BT @ x))
        elif model == "max":
            s = x.max()
            u = np.sqrt(x * (B @ y))
            v = np.sqrt(y * s * (BT @ (x / s) ** ALPHA) ** (1 / ALPHA))
        elif model == "log-exp":
            u = np.sqrt(x * np.sqrt(B @ y))
            logv = 0.5 * (np.log(y) + BT @ np.log(x))           # psi(B' ln x) = prod of x over the paper, in logs
            v = np.exp(logv - 0.5 * logsumexp(2 * logv))        # already unit 2-norm
        x1, y1 = unit(u), unit(v)
        y1 = np.maximum(y1, 1e-300)
        err = np.linalg.norm(x1 - x) + np.linalg.norm(y1 - y)
        x, y = x1, y1
        if err < TOL:
            break
    return x, y, it, size


def rank_of(v):
    """Rank 1 = highest; ties (e.g. exact zeros) share the best rank of their group."""
    return rankdata(-v, method="min").astype(int)


def on_support(v, rel=1e-10):
    """(|v| with entries below rel * max set to exactly 0, whether the kept entries all have one sign). Eigenvector-type
    scores live on one part of a disconnected hypergraph; the rest is numerical noise and must not be ranked."""
    keep = np.abs(v) > rel * np.abs(v).max()
    return np.where(keep, np.abs(v), 0.0), bool(np.all(v[keep] > 0) or np.all(v[keep] < 0))


def main():
    authors, papers, B, meta = load_hypergraph()
    fac = {f["roster_id"]: f for f in read_csv(os.path.join(RES, "faculty.csv"))}
    fidx = np.array([i for i, a in enumerate(authors) if a in fac])
    size = np.asarray(B.sum(axis=0)).ravel()            # authors present in the network file for the paper
    # 'more than 10 authors' uses the paper's author count (n_authors, as in group3_data.csv); 150 papers have an
    # author with no usable id in the network file, so their set is one or two short of n_authors
    nauth = np.array([meta[p]["n_authors"] or size[j] for j, p in enumerate(papers)])
    big = nauth > LARGE
    summ = [{"metric": "authors (nodes)", "value": B.shape[0]}, {"metric": "papers with >= 2 authors (hyperedges)", "value": B.shape[1]},
            {"metric": "authors keyed by name (no OpenAlex id), share of nodes",
             "value": round(sum(1 for a in authors if name_keyed(a)) / len(authors), 4)},
            {"metric": "papers whose author set in the network file is smaller than n_authors", "value": int(np.sum(size < nauth))},
            {"metric": "faculty among the nodes", "value": len(fidx)},
            {"metric": "papers with more than 10 authors (n_authors)", "value": int(big.sum())},
            {"metric": "author pairs (counted per paper) that come from papers with more than 10 authors, share of all",
             "value": round(float((size[big] * (size[big] - 1) / 2).sum() / (size * (size - 1) / 2).sum()), 4)}]

    scores = {}
    for model in ("linear", "log-exp", "max"):
        x, y, it, _ = npm(B, model)
        scores[model] = (on_support(x)[0], y)
        summ.append({"metric": f"{model}: iterations to converge (tol {TOL:g}, max {MAXIT})", "value": it})
    # the linear model is the leading singular pair of B: compute it exactly as a check, and use the exact method
    # for the run without big papers (the power method is slow there because the top singular values are close)
    u, s, vt = svds(B, k=2, random_state=0)
    ux, one = on_support(u[:, np.argmax(s)])
    summ += [{"metric": "linear: Spearman of power method vs exact singular vector (all nodes)",
              "value": round(float(spearmanr(scores["linear"][0], ux).statistic), 4)},
             {"metric": "linear: exact singular vector has one sign on its support (check)", "value": one},
             {"metric": "linear: ratio of the two largest singular values of B", "value": round(float(s.max() / s.min()), 4)}]
    Bs = (B @ sp.diags((~big).astype(float))).tocsr()
    u, s, vt = svds(Bs, k=2, random_state=0)
    ux, one = on_support(u[:, np.argmax(s)])
    scores["linear without >10-author papers"] = (ux, None)
    summ += [{"metric": "linear without >10-author papers: ratio of the two largest singular values (near 1 = two labs "
                        "almost tie, the leader can switch with small changes)", "value": round(float(s.max() / s.min()), 4)},
             {"metric": "linear without >10-author papers: one sign on its support (check)", "value": one}]
    # localisation: inverse participation ratio of each node vector (1/n = spread evenly, 1 = one node), and support
    for k, (x, _) in scores.items():
        x = x / np.linalg.norm(x)
        summ += [{"metric": f"{k}: authors with a non-zero score", "value": int((x > 0).sum())},
                 {"metric": f"{k}: faculty with a non-zero score", "value": int((x[fidx] > 0).sum())},
                 {"metric": f"{k}: IPR of node scores (1/n = {1 / len(x):.2g})", "value": f"{np.sum(x ** 4):.4g}"},
                 {"metric": f"{k}: share of score weight (x^2) on its top 10 authors", "value": round(float(np.sort(x ** 2)[-10:].sum()), 3)}]

    # faculty view
    pap = np.asarray(B.sum(axis=1)).ravel()
    P = (B > 0).astype(float)
    big_share = np.asarray((B @ sp.diags(big.astype(float))).sum(axis=1)).ravel() / np.maximum(pap, 1)
    # distinct co-authors (pairwise view), only for the faculty rows: the full author x author product of a large network
    # (papers with hundreds of authors) does not fit in memory, and nothing else reads the other rows
    coauth = np.zeros(len(authors), dtype=np.int64)
    coauth[fidx] = np.asarray(((P[fidx] @ P.T) > 0).sum(axis=1)).ravel() - 1
    Ps = (Bs > 0).astype(float)
    coauth_s = np.zeros(len(authors), dtype=np.int64)
    coauth_s[fidx] = np.asarray(((Ps[fidx] @ Ps.T) > 0).sum(axis=1)).ravel() - (np.asarray(Ps[fidx].sum(axis=1)).ravel() > 0)
    frows = []
    fscore = {k: x[fidx] for k, (x, _) in scores.items()}
    fscore["distinct co-authors (pairwise)"] = coauth[fidx].astype(float)
    fscore["distinct co-authors without >10-author papers"] = coauth_s[fidx].astype(float)
    fscore["papers"] = pap[fidx].astype(float)
    franks = {k: rank_of(v) for k, v in fscore.items()}
    for j, i in enumerate(fidx):
        f = fac[authors[i]]
        frows.append({"roster_id": authors[i], "faculty": f["faculty"], "institution": f["institution"], "department": f["department"],
                      "papers_in_hypergraph": int(pap[i]), "distinct_coauthors": int(coauth[i]),
                      "share_papers_over_10_authors": round(float(big_share[i]), 3),
                      **{f"rank_{k}": int(r[j]) for k, r in franks.items()}})
    frows.sort(key=lambda r: r["rank_linear"])
    write_csv("hypergraph_faculty.csv", frows)

    # Spearman between two scores only over faculty where both are non-zero (zeros carry no ranking information)
    names = list(fscore)
    for a_ in range(len(names)):
        for b_ in range(a_ + 1, len(names)):
            both = (fscore[names[a_]] > 0) & (fscore[names[b_]] > 0)
            summ.append({"metric": f"faculty Spearman: {names[a_]} vs {names[b_]} (faculty non-zero in both)",
                         "value": f"{spearmanr(fscore[names[a_]][both], fscore[names[b_]][both]).statistic:.3f} (n = {int(both.sum())})"})
    trows = []
    summ.append({"metric": "all faculty: median share of their papers with > 10 authors",
                 "value": round(float(np.median([r["share_papers_over_10_authors"] for r in frows])), 3)})
    pairs = {"linear without >10-author papers": "linear",
             "distinct co-authors without >10-author papers": "distinct co-authors (pairwise)"}
    for k in ("linear", "log-exp", "max", "linear without >10-author papers", "distinct co-authors (pairwise)",
              "distinct co-authors without >10-author papers"):
        nz = int((fscore[k] > 0).sum())                     # faculty with a non-zero score (zeros all tie)
        top = [r for r in frows if r[f"rank_{k}"] <= min(TOP, nz)]
        top.sort(key=lambda r: r[f"rank_{k}"])
        ref = pairs.get(k, "linear")
        summ += [{"metric": f"{k}: top {TOP} faculty, median share of their papers with > 10 authors",
                  "value": round(float(np.median([r["share_papers_over_10_authors"] for r in top])), 3)},
                 {"metric": f"{k}: top {TOP} faculty, institutions",
                  "value": "; ".join(f"{i} {c}" for i, c in C.Counter(r["institution"] for r in top).most_common())},
                 {"metric": f"{k}: top {TOP} overlap with {ref} top {TOP}",
                  "value": sum(1 for r in top if r[f"rank_{ref}"] <= TOP)}]
        for r in top:
            trows.append({"model": k, "rank": r[f"rank_{k}"], **{c: r[c] for c in ("faculty", "institution", "department",
                          "papers_in_hypergraph", "distinct_coauthors", "share_papers_over_10_authors", "rank_linear",
                          "rank_log-exp", "rank_max", "rank_distinct co-authors (pairwise)",
                          "rank_distinct co-authors without >10-author papers")}})
    write_csv("hypergraph_top_faculty.csv", trows)

    # paper view: which papers each model ranks highest
    prows = []
    for k in ("linear", "log-exp", "max"):
        y = on_support(scores[k][1])[0]                    # paper scores: zero outside the support, like nodes
        nzp = np.flatnonzero(y > 0)
        top = nzp[np.argsort(-y[nzp])][:10]
        top100 = nzp[np.argsort(-y[nzp])][:100]
        summ += [{"metric": f"{k}: papers with a non-zero score", "value": len(nzp)},
                 {"metric": f"{k}: top {len(top100)} non-zero papers, median number of authors", "value": float(np.median(size[top100]))}]
        for r, j in enumerate(top, 1):
            faculty_on = [fac[authors[i]]["faculty"] for i in B[:, j].nonzero()[0] if authors[i] in fac]
            prows.append({"model": k, "rank": r, "paper_doi": papers[j], "year": meta[papers[j]]["year"],
                          "authors": int(size[j]), "faculty_on_paper": "; ".join(sorted(faculty_on))})
    write_csv("hypergraph_top_papers.csv", prows)

    # robustness: name-keyed authors made unique per paper. Do the localisation and the faculty top 20 change?
    a2, p2, B2, _ = load_hypergraph(split_names=True)
    pos2 = {a: i for i, a in enumerate(a2)}
    f2 = np.array([pos2[authors[i]] for i in fidx])
    summ.append({"metric": "check (name-keyed authors split per paper): authors (nodes)", "value": B2.shape[0]})
    for model in ("linear", "log-exp", "max"):
        x2 = on_support(npm(B2, model)[0])[0]
        x2 = x2 / np.linalg.norm(x2)
        top_main = set(np.flatnonzero((franks[model] <= TOP) & (fscore[model] > 0)))
        top_new = set(np.flatnonzero((rank_of(x2[f2]) <= TOP) & (x2[f2] > 0)))
        summ += [{"metric": f"check (names split): {model}: share of score weight on its top 10 authors",
                  "value": round(float(np.sort(x2 ** 2)[-10:].sum()), 3)},
                 {"metric": f"check (names split): {model}: faculty top {TOP} overlap with the main run", "value": len(top_main & top_new)}]
    write_csv("hypergraph_summary.csv", summ)
    for s in summ:
        print(s["metric"], "=", s["value"])


if __name__ == "__main__":
    main()
