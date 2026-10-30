"""Do teams that mix departments get more citations? (research_directions.md §3d, team composition; Stirling 2007,
J. R. Soc. Interface 4, 707; Rafols & Meyer 2010, Scientometrics 82, 263; Leinster & Cobbold 2012, Ecology 93, 477).
Papers with at least two of our faculty (faculty_layers.py). A paper is
  one department    all its faculty are in the same department of the same IIT
  cross-department  faculty from two or more departments of the same IIT
  cross-campus      faculty from both IITs
Impact = OpenAlex FWCI (field-weighted citation impact: citations / the world average for the same field, year and
type; 1 = world average) and 'top 10%' = OpenAlex citation-normalized percentile >= 0.9. Raw citations are not
compared: they depend on field and age. Main window: publication years up to LAST_YEAR (later papers have had little
time to be cited); all years as a check.
Bigger teams get more citations, and a team with more faculty is more likely to span departments, so every comparison
holds team size fixed:
  1. strata of (number of faculty band, number of authors band, year, OpenAlex field): within each stratum the mean of
     log(1 + FWCI) and the top-10% share of cross-department papers minus one-department papers, averaged with the
     cross-department papers' weights (an exact-matching estimate);
  2. least squares: log(1 + FWCI) ~ cross-department + cross-campus + faculty band + author band + year + field, with
     heteroskedasticity-robust (HC1) standard errors; the same for top 10% (linear probability);
  3. the same faculty member: for every faculty member with both kinds of papers, their mean log(1 + FWCI) on
     cross-department papers minus on one-department papers (removes 'better researchers build mixed teams');
  4. how far apart the departments are: Rao-Stirling diversity of a paper's faculty, sum_{i != j} p_i p_j d_ij, with
     p_i = share of the paper's faculty in department i and d_ij = 1 - cosine similarity of the two departments'
     subfield profiles (their papers per OpenAlex subfield; our own data, not a fixed map).
Check: number of cross-department papers recounted from group3_data.csv (one row per paper and faculty member).
Outputs (results/): cross_dept_summary.csv, cross_dept_strata.csv, cross_dept_regression.csv, cross_dept_by_pair.csv
Figure: cross_dept_fwci.png
usage: python stats_cross_dept.py"""
import os
from collections import Counter, defaultdict
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from scipy.stats import wilcoxon
from common import DATA, CACHE, read_csv, write_csv, style, save, plt, note_skip
from faculty_layers import faculty_table, paper_table

LAST_YEAR = 2023
MIN_STRATUM = 1
AUTH_BANDS = [(2, 3), (4, 5), (6, 10), (11, 20), (21, 10 ** 6)]
FAC_BANDS = [(2, 2), (3, 3), (4, 10 ** 6)]


def band(x, bands):
    return next((str(a) if a == b else f"{a}-{b}") if b < 10 ** 6 else f"{a}+" for a, b in bands if a <= x <= b)


def kind(depts):
    insts = {i for i, _ in depts}
    return "cross-campus" if len(insts) > 1 else "cross-department" if len(depts) > 1 else "one department"


def main():
    style()
    if not os.path.exists(os.path.join(CACHE, "oa_fwci.json")):
        note_skip("stats_cross_dept.py", "cross-department teams vs FWCI (cross_dept_*.csv, cross_dept_fwci.png)",
                  "impact is OpenAlex's field-weighted citation impact (FWCI) per paper, not cached for these institutes",
                  "fetch_openalex_extra.py (OpenAlex credits): oa_fwci.json")
        return
    F = faculty_table()
    P = paper_table()
    dept = {a: (r["institution"], r["department"]) for a, r in F.items()}

    # department subfield profiles -> cosine distances
    prof = defaultdict(Counter)
    for p in P.values():
        if p["subfield"]:
            for d in {dept[a] for a in p["fac"] if a in dept}:
                prof[d][p["subfield"]] += 1
    subs = sorted({s for c in prof.values() for s in c})
    si = {s: i for i, s in enumerate(subs)}
    vec = {}
    for d, c in prof.items():
        v = np.zeros(len(subs))
        for s, k in c.items():
            v[si[s]] = k
        vec[d] = v / np.linalg.norm(v)

    rows = []
    for k, p in P.items():
        fs = [a for a in p["fac"] if a in dept]
        if len(fs) < 2 or not p["n_auth"]:
            continue
        cnt = Counter(dept[a] for a in fs)
        ds = list(cnt)
        rs = sum(cnt[x] * cnt[y] * (1 - float(vec[x] @ vec[y])) for x in ds for y in ds if x != y) / len(fs) ** 2
        rows.append({"key": k, "year": p["year"], "field": p["field"] or "unknown", "n_fac": len(fs), "n_auth": p["n_auth"],
                     "n_dept": len(ds), "kind": kind(ds), "rao_stirling": rs, "fwci": p["fwci"], "pct": p["pct"],
                     "cites": p["cites"], "fac": fs, "depts": ds})
    df = pd.DataFrame(rows)
    df["fac_band"] = [band(x, FAC_BANDS) for x in df.n_fac]
    df["auth_band"] = [band(x, AUTH_BANDS) for x in df.n_auth]
    df["cross"] = (df.kind != "one department").astype(int)
    df["campus"] = (df.kind == "cross-campus").astype(int)
    df["dept_only"] = (df.kind == "cross-department").astype(int)
    df["lf"] = np.log1p(df.fwci)
    df["top10"] = (df.pct >= 0.9).astype(float).where(df.pct.notna())

    summ = [("papers with >= 2 faculty (with an author count)", len(df))]
    for kd, g in df.groupby("kind"):
        summ.append((f"{kd}: papers", len(g)))
    # check against group3_data.csv
    g3 = defaultdict(set)
    for r in read_csv(os.path.join(DATA, "group3_data.csv")):
        if r["department"] and r["faculty_match"] and not r["faculty_match"].startswith("none"):
            g3[(r["doi"] or r["record_id"]).lower()].add((r["institution"], r["department"]))
    multi_g3 = sum(1 for v in g3.values() if len(v) > 1)
    summ += [("check: papers with faculty of >= 2 departments, this script", int(df.cross.sum())),
             ("check: the same from group3_data.csv", multi_g3)]

    sumrows, srows, regrows = [], [], []
    for window, d0 in (("<= %d" % LAST_YEAR, df[df.year <= LAST_YEAR]), ("all years", df)):
        d0 = d0[d0.fwci.notna()]
        for kd, g in d0.groupby("kind"):
            sumrows.append({"window": window, "group": kd, "papers": len(g), "median_fwci": round(g.fwci.median(), 3),
                            "mean_log1p_fwci": round(g.lf.mean(), 4), "top10_share": round(g.top10.mean(), 4),
                            "median_authors": float(g.n_auth.median()), "median_faculty": float(g.n_fac.median())})
        # 1. exact matching on strata
        for label, treat in (("cross-department (same IIT) vs one department", d0[d0.kind != "cross-campus"]),
                             ("cross-campus vs one department", d0[d0.kind != "cross-department"])):
            t = treat.copy()
            t["s"] = t.fac_band + "|" + t.auth_band + "|" + t.year.astype(str) + "|" + t.field
            diff_l, diff_t, w, used = 0.0, 0.0, 0, 0
            for s, g in t.groupby("s"):
                a, b = g[g.cross == 1], g[g.cross == 0]
                if len(a) >= MIN_STRATUM and len(b) >= MIN_STRATUM:
                    diff_l += len(a) * (a.lf.mean() - b.lf.mean())
                    diff_t += len(a) * (a.top10.mean() - b.top10.mean())
                    w += len(a)
                    used += 1
            srows.append({"window": window, "comparison": label, "strata_used": used, "treated_papers_matched": w,
                          "treated_papers": int(t.cross.sum()), "diff_mean_log1p_fwci": round(diff_l / w, 4),
                          "fwci_ratio_exp_diff": round(float(np.exp(diff_l / w)), 3),
                          "diff_top10_share": round(diff_t / w, 4)})
        # 2. regression
        for y, fam in (("lf", "log(1 + FWCI)"), ("top10", "top 10% (linear probability)")):
            dd = d0[d0[y].notna()]
            m = smf.ols(f"{y} ~ dept_only + campus + C(fac_band) + C(auth_band) + C(year) + C(field)", data=dd).fit(cov_type="HC1")
            for v in ("dept_only", "campus"):
                lo, hi = m.conf_int().loc[v]
                regrows.append({"window": window, "outcome": fam, "term": {"dept_only": "cross-department (same IIT)",
                                "campus": "cross-campus"}[v], "coef": round(m.params[v], 4), "ci95_low": round(lo, 4),
                                "ci95_high": round(hi, 4), "p_value": f"{m.pvalues[v]:.2g}", "papers": int(m.nobs)})
        # 4. Rao-Stirling among cross-department papers of one IIT
        dd = d0[d0.kind == "cross-department"]
        m = smf.ols("lf ~ rao_stirling + C(fac_band) + C(auth_band) + C(year) + C(field)", data=dd).fit(cov_type="HC1")
        lo, hi = m.conf_int().loc["rao_stirling"]
        regrows.append({"window": window, "outcome": "log(1 + FWCI), cross-department papers only", "term":
                        "Rao-Stirling diversity (0 = same profile, higher = departments further apart)",
                        "coef": round(m.params["rao_stirling"], 4), "ci95_low": round(lo, 4), "ci95_high": round(hi, 4),
                        "p_value": f"{m.pvalues['rao_stirling']:.2g}", "papers": int(m.nobs)})

    # 3. same faculty member (main window, same IIT only)
    d0 = df[(df.year <= LAST_YEAR) & df.fwci.notna() & (df.kind != "cross-campus")]
    per = defaultdict(lambda: ([], []))
    for fs, c, lf in zip(d0.fac, d0.cross, d0.lf):
        for a in fs:
            per[a][c].append(lf)
    diffs = [np.mean(x[1]) - np.mean(x[0]) for x in per.values() if x[0] and x[1]]
    st = wilcoxon(diffs)
    summ += [("same faculty member: faculty with both one-department and cross-department papers", len(diffs)),
             ("same faculty member: median of (mean log(1+FWCI) cross-dept - one-dept)", round(float(np.median(diffs)), 4)),
             ("same faculty member: share of faculty with a higher value on cross-department papers",
              round(float(np.mean(np.array(diffs) > 0)), 4)),
             ("same faculty member: Wilcoxon signed-rank p", f"{st.pvalue:.2g}")]

    # department pairs that work together most, and how their joint papers do
    pr = defaultdict(list)
    for ds, lf, fw in zip(d0.depts, d0.lf, d0.fwci):
        if len(ds) == 2:
            pr[tuple(sorted(ds))].append(fw)
    prow = [{"institution": a[0], "department_a": a[1], "department_b": b[1], "joint_papers": len(v),
             "median_fwci": round(float(np.median(v)), 3)} for (a, b), v in pr.items()]
    prow.sort(key=lambda r: -r["joint_papers"])
    write_csv("cross_dept_by_pair.csv", prow[:40])
    write_csv("cross_dept_strata.csv", srows)
    write_csv("cross_dept_regression.csv", regrows)
    write_csv("cross_dept_summary.csv", [{"metric": k, "value": v} for k, v in summ] +
              [{"metric": f"{r['window']} | {r['group']}", "value": "; ".join(f"{k} {v}" for k, v in r.items()
                                                                                 if k not in ("window", "group"))} for r in sumrows])
    for k, v in summ:
        print(k, "|", v)
    for r in sumrows + srows + regrows + prow[:8]:
        print(r)

    fig, ax = plt.subplots(figsize=(7.2, 3.4))
    d0 = df[(df.year <= LAST_YEAR) & df.fwci.notna()]
    kinds = ["one department", "cross-department", "cross-campus"]
    bands = [b for b in [band(x[0], FAC_BANDS) for x in FAC_BANDS]]
    w = 0.26
    for k, kd in enumerate(kinds):
        gs = [d0[(d0.kind == kd) & (d0.fac_band == b)].fwci for b in bands]
        xs = np.arange(len(bands)) + (k - 1) * w
        ax.bar(xs, [g.median() for g in gs], width=w, color=["#86b6ef", "#3987e5", "#0d366b"][k], label=kd)
        for x, g in zip(xs, gs):
            ax.text(x, g.median(), f"n={len(g)}", ha="center", va="bottom", fontsize=7, color="#52514e")
    ax.axhline(1, color="#8a8984", lw=1, ls="--")
    ax.set_xticks(range(len(bands)), [f"{b} faculty" for b in bands])
    ax.set_ylabel("median FWCI (1 = world average)")
    ax.set_title(f"Papers with several faculty, published 2016-{LAST_YEAR}")
    ax.legend()
    save(fig, "cross_dept_fwci.png")


if __name__ == "__main__":
    main()
