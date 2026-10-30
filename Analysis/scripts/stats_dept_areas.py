"""Which research areas each department is strong in, and can we predict the areas it moves into next
(research_directions.md §3f; Hidalgo, Klinger, Barabasi & Hausmann 2007, Science 317, 482; Guevara et al. 2016,
Scientometrics 109, 1695; Tacchella et al. 2012, Sci. Rep. 2, 723).
Area = OpenAlex subfield of a paper (its primary topic's subfield). Department = (IIT, department of faculty.csv);
departments with at least MIN_FAC faculty and MIN_PAPERS papers. A paper counts once for each department of its faculty.
  strength  revealed comparative advantage RCA_ds = (X_ds / X_d) / (X_s / X), X = papers; 'strong' = RCA >= 1 and at
            least MIN_STRONG papers in the period: the department publishes a larger share of its papers in s than
            our two IITs do overall, and not by one or two papers
  rising    subfields whose share of the department's papers grew most from P1 = 2016-2020 to P2 = 2021-2026
  proximity of two subfields (P1 only, faculty level): phi_ss' = number of faculty strong in both (RCA >= 1 and at
            least 2 papers there; faculty with at least MIN_FAC_PAPERS papers in P1) / the larger of the two counts
            (Hidalgo et al. 2007)
  density   omega_ds = sum_s' M_ds' phi_ss' / sum_s' phi_ss' (M = department strong in s' in P1): how related s is
            to what the department already does
Prediction test: candidates = (department, subfield) pairs not strong in P1; 'entry' = strong in P2. Does P1 density
rank entries above non-entries? ROC AUC (0.5 = chance), against
  - the department's P1 RCA in s (being close already); density, RCA and both also as logistic models fitted with
    one department left out at a time (the same pipeline for all three)
  - a null: subfield labels of the proximity matrix shuffled (SHUFFLES times)
Fitness and complexity (Tacchella et al. 2012) of the department x subfield matrix (whole window, RCA >= 1): fitness is
high for departments strong in many subfields, especially in subfields few departments are strong in.
Outlook: for each department, the subfields with the highest density that it is not yet strong in (P2 data, P2
proximity), among subfields at least MIN_K faculty are strong in (a proximity built on one or two people is noise);
an indication of nearby areas, not a forecast of what will happen.
Check: each department's paper count here vs results/departments.csv.
Outputs (results/): dept_area_strengths.csv, dept_area_rising.csv, dept_area_prediction.csv,
  dept_area_prediction_bins.csv (entry rate by density: pairs with density 0, then quintiles of the rest), dept_fitness.csv,
  dept_area_outlook.csv
Figure: dept_area_prediction.png
usage: python stats_dept_areas.py"""
import os
from collections import Counter, defaultdict
import numpy as np
from scipy.stats import spearmanr, rankdata
from sklearn.metrics import roc_auc_score
from sklearn.linear_model import LogisticRegression
from common import RES, read_csv, write_csv, style, save, plt
from faculty_layers import faculty_table, paper_table

P1, P2 = (2016, 2020), (2021, 2026)
MIN_FAC, MIN_PAPERS = 5, 100
MIN_FAC_PAPERS = 5
MIN_STRONG = 5
SHUFFLES = 500
TOP = 5
SEED = 3
FC_ITERS = 100
MIN_K = 5


def rca(X):
    tot = X.sum()
    rs, cs = X.sum(1, keepdims=True), X.sum(0, keepdims=True)
    with np.errstate(invalid="ignore", divide="ignore"):
        R = (X / np.where(rs == 0, 1, rs)) / np.where(cs == 0, 1, cs / tot)
    return np.nan_to_num(R)


def proximity(Mf):
    k = Mf.sum(0)
    co = Mf.T @ Mf
    phi = co / np.maximum.outer(k, k).clip(min=1)
    np.fill_diagonal(phi, 0)
    return phi


def density(M, phi):
    return (M @ phi) / np.where(phi.sum(0) == 0, 1, phi.sum(0))


def fitness_complexity(M, iters=FC_ITERS):
    """Fitness and complexity after `iters` steps, and those after iters / 2 (for the ranking-stability check).
    The values of weakly diversified rows shrink towards 0 as the map runs (the matrix is not perfectly nested; Pugliese
    et al. 2016, Eur. Phys. J. Spec. Top. 225, 1893), but the ranking settles, so rankings and log10 values are used."""
    F, Q = np.ones(M.shape[0]), np.ones(M.shape[1])
    for n in range(1, iters + 1):
        F2 = M @ Q
        Q2 = 1 / (M.T @ (1 / F))
        F, Q = F2 / F2.mean(), Q2 / Q2.mean()
        if n == iters // 2:
            half = (F.copy(), Q.copy())
    return F, Q, half


def main():
    style()
    Ft = faculty_table()
    P = paper_table()
    dept_of = {a: (r["institution"], r["department"]) for a, r in Ft.items()}
    nfac = Counter(dept_of.values())
    papers = [p for p in P.values() if p["subfield"]]
    allp = Counter(d for p in P.values() for d in {dept_of[a] for a in p["fac"] if a in dept_of})
    depts = sorted(d for d in nfac if nfac[d] >= MIN_FAC and allp[d] >= MIN_PAPERS)
    subs = sorted({p["subfield"] for p in papers})
    di, si = {d: i for i, d in enumerate(depts)}, {s: i for i, s in enumerate(subs)}
    fac = sorted(Ft)
    fi = {a: i for i, a in enumerate(fac)}

    def matrices(lo, hi):
        X = np.zeros((len(depts), len(subs)))
        Xf = np.zeros((len(fac), len(subs)))
        for p in papers:
            if lo <= p["year"] <= hi:
                for d in {dept_of[a] for a in p["fac"] if a in dept_of}:
                    if d in di:
                        X[di[d], si[p["subfield"]]] += 1
                for a in p["fac"]:
                    if a in fi:
                        Xf[fi[a], si[p["subfield"]]] += 1
        return X, Xf

    Xall, _ = matrices(1900, 3000)
    X1, Xf1 = matrices(*P1)
    X2, Xf2 = matrices(*P2)
    summ = [("departments (>= %d faculty, >= %d papers)" % (MIN_FAC, MIN_PAPERS), len(depts)),
            ("OpenAlex subfields in our papers", len(subs)),
            ("papers without a subfield (left out)", sum(1 for p in P.values() if not p["subfield"]))]
    # check: department paper counts vs departments.csv (all papers, incl. those without a subfield)
    ref = {(r["institution"], r["department"]): int(r["papers"]) for r in read_csv(os.path.join(RES, "departments.csv"))}
    summ.append(("check: departments whose paper count differs from departments.csv", sum(1 for d in depts if allp[d] != ref.get(d))))

    # ---- strengths and rising areas
    R = rca(Xall)
    srows, rrows = [], []
    for d in depts:
        i = di[d]
        order = np.argsort(-Xall[i])
        for s in [j for j in order if R[i, j] >= 1][:TOP]:
            srows.append({"institution": d[0], "department": d[1], "subfield": subs[s], "papers": int(Xall[i, s]),
                          "share_of_department": round(Xall[i, s] / Xall[i].sum(), 3), "rca": round(float(R[i, s]), 2)})
        s1, s2 = X1[i] / max(X1[i].sum(), 1), X2[i] / max(X2[i].sum(), 1)
        for s in np.argsort(-(s2 - s1))[:3]:
            if X2[i, s] >= 10 and s2[s] > s1[s]:
                rrows.append({"institution": d[0], "department": d[1], "subfield": subs[s], "papers_2016_20": int(X1[i, s]),
                              "papers_2021_26": int(X2[i, s]), "share_2016_20": round(float(s1[s]), 3),
                              "share_2021_26": round(float(s2[s]), 3)})
    write_csv("dept_area_strengths.csv", srows)
    write_csv("dept_area_rising.csv", rrows)

    # ---- prediction test
    R1, R2 = rca(X1), rca(X2)
    S1, S2 = (R1 >= 1) & (X1 >= MIN_STRONG), (R2 >= 1) & (X2 >= MIN_STRONG)
    M1 = S1.astype(float)
    act = Xf1.sum(1) >= MIN_FAC_PAPERS
    Mf1 = ((rca(Xf1[act]) >= 1) & (Xf1[act] >= 2)).astype(float)
    phi = proximity(Mf1)
    om = density(M1, phi)
    cand = ~S1
    entry = S2
    y, w, r1 = entry[cand].astype(int), om[cand], R1[cand]
    dep_idx = np.broadcast_to(np.arange(len(depts))[:, None], cand.shape)[cand]
    auc_w, auc_r = roc_auc_score(y, w), roc_auc_score(y, r1)
    def cv_auc(Z):
        pred = np.zeros(len(y))
        for g in range(len(depts)):
            tr, te = dep_idx != g, dep_idx == g
            if te.any():
                pred[te] = LogisticRegression().fit(Z[tr], y[tr]).predict_proba(Z[te])[:, 1]
        return roc_auc_score(y, pred)
    cv = {k: cv_auc(Z) for k, Z in (("density", w[:, None]), ("RCA", np.log1p(r1)[:, None]),
                                    ("density + RCA", np.column_stack([w, np.log1p(r1)])))}
    rng = np.random.default_rng(SEED)
    null = []
    for _ in range(SHUFFLES):
        perm = rng.permutation(len(subs))
        null.append(roc_auc_score(y, density(M1, phi[np.ix_(perm, perm)])[cand]))
    null = np.array(null)
    new = cand & (X1 == 0)
    prow = [{"metric": f"candidate (department, subfield) pairs: not strong in 2016-20 (strong = RCA >= 1 and >= {MIN_STRONG} papers)",
             "value": int(cand.sum())},
            {"metric": "entries: strong in 2021-26", "value": int(y.sum())},
            {"metric": "faculty used for the proximity (>= %d papers in 2016-20)" % MIN_FAC_PAPERS, "value": int(act.sum())},
            {"metric": "ROC AUC: density (relatedness to what the department does)", "value": round(auc_w, 3)},
            {"metric": "ROC AUC: RCA in 2016-20 (already close)", "value": round(auc_r, 3)},
            *[{"metric": f"ROC AUC, logistic with one department left out: {k}", "value": round(v, 3)} for k, v in cv.items()],
            {"metric": f"ROC AUC: density with shuffled subfield labels, {SHUFFLES} shuffles: mean (95% range)",
             "value": f"{null.mean():.3f} ({np.quantile(null, 0.025):.3f}-{np.quantile(null, 0.975):.3f})"},
            {"metric": "share of shuffles with AUC >= observed (p)", "value": round(float((null >= auc_w).mean()), 4)},
            {"metric": "brand-new areas (0 papers in 2016-20): candidates / entries", "value": f"{int(new.sum())} / {int(entry[new].sum())}"},
            {"metric": "ROC AUC: density, brand-new areas only",
             "value": round(roc_auc_score(entry[new].astype(int), om[new]), 3) if 0 < entry[new].sum() < new.sum() else ""}]
    write_csv("dept_area_prediction.csv", prow)

    # ---- fitness and complexity (whole window)
    M = ((R >= 1) & (Xall >= MIN_STRONG)).astype(float)
    keep = M.sum(0) > 0
    Fd, Qs, (Fh, Qh) = fitness_complexity(M[:, keep])
    div = M.sum(1)
    frank = rankdata(-Fd, method="min")
    frows = [{"institution": d[0], "department": d[1], "faculty": nfac[d], "papers": int(allp[d]),
              "strong_subfields": int(div[di[d]]), "fitness_rank": int(frank[di[d]]),
              "log10_fitness": round(float(np.log10(Fd[di[d]])), 2)} for d in depts]
    frows.sort(key=lambda r: r["fitness_rank"])
    write_csv("dept_fitness.csv", frows)
    qsub = np.array(subs)[keep]
    summ += [(f"fitness-complexity: ranking stability, Spearman of fitness after {FC_ITERS // 2} and {FC_ITERS} steps",
              round(float(spearmanr(Fd, Fh).statistic), 4)),
             ("fitness-complexity: same for subfield complexity", round(float(spearmanr(Qs, Qh).statistic), 4)),
             ("Spearman fitness vs number of strong subfields (check: fitness grows with diversity)",
              round(float(spearmanr(Fd, div).statistic), 3)),
             ("most complex subfields (few, diverse departments strong in them)", "; ".join(qsub[np.argsort(-Qs)[:5]])),
             ("least complex subfields", "; ".join(qsub[np.argsort(Qs)[:5]]))]

    # ---- outlook: nearby areas not yet strong (P2)
    act2 = Xf2.sum(1) >= MIN_FAC_PAPERS
    Mf2 = ((rca(Xf2[act2]) >= 1) & (Xf2[act2] >= 2)).astype(float)
    phi2 = proximity(Mf2)
    common = Mf2.sum(0) >= MIN_K
    om2 = density(S2.astype(float), phi2)
    orows = []
    for d in depts:
        i = di[d]
        c = [j for j in np.argsort(-om2[i]) if not S2[i, j] and common[j]][:3]
        for rank, j in enumerate(c, 1):
            orows.append({"institution": d[0], "department": d[1], "rank": rank, "subfield": subs[j],
                          "density": round(float(om2[i, j]), 3), "papers_2021_26": int(X2[i, j]), "rca_2021_26": round(float(R2[i, j]), 2)})
    write_csv("dept_area_outlook.csv", orows)
    write_csv("dept_area_summary.csv", [{"metric": k, "value": v} for k, v in summ])
    for k, v in summ:
        print(k, "|", v)
    for r in prow:
        print(r)
    for r in frows[:5] + frows[-3:]:
        print(r)

    # entry rate by density: many pairs have density exactly 0 (one group), the rest in quintiles
    pos = w > 0
    cuts = np.quantile(w[pos], [0.2, 0.4, 0.6, 0.8])
    grp = np.where(pos, 1 + np.searchsorted(cuts, w, side="right"), 0)
    brows = []
    for g in range(6):
        m = grp == g
        brows.append({"bin": "density 0" if g == 0 else f"quintile {g}", "density_min": round(float(w[m].min()), 4),
                      "density_max": round(float(w[m].max()), 4), "pairs": int(m.sum()), "entries": int(y[m].sum()),
                      "entry_rate": round(float(y[m].mean()), 4)})
    write_csv("dept_area_prediction_bins.csv", brows)
    fig, ax = plt.subplots(figsize=(7.2, 3.4))
    ax.bar(range(6), [100 * r["entry_rate"] for r in brows], color=["#c9c8c3"] + ["#3987e5"] * 5)
    for k, r in enumerate(brows):
        ax.text(k, 100 * r["entry_rate"], f"{r['entries']}/{r['pairs']}", ha="center", va="bottom", fontsize=8, color="#52514e")
    ax.set_xticks(range(6), ["0", "Q1", "Q2", "Q3", "Q4", "Q5"])
    ax.set_xlabel("relatedness density in 2016-20 (0 = no related strength, then quintiles of the rest)")
    ax.set_ylabel("% of department-area pairs\nthat became a strength in 2021-26")
    ax.set_title(f"Departments move into related areas (AUC {auc_w:.2f})")
    save(fig, "dept_area_prediction.png")


if __name__ == "__main__":
    main()
