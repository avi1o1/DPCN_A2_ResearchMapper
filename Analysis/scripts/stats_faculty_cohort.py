"""Seniority-controlled per-faculty statistics and roster completeness (sanity audit F4, 2026-10-30).
Per-faculty numbers mix people with 9 window years and people who joined last year, and institutes whose roster misses a fifth of the
faculty (IIT Delhi: 648 current against 833 in NIRF 2025). This script reports, per institute:
  cohort            current faculty (roster status 'current', departments in field scope) with joining_year <= 2017, i.e. at least
                    9 of the 11 window years at the institute. People without a joining year are NOT in the cohort (the cohort is
                    only as large as the roster's joining-year coverage; a cohort smaller than MIN_COHORT = 20 people is flagged
                    'cohort too small' and its statistics should not be compared).
  roster completeness  current roster rows against the NIRF faculty counts in WebScrape/rosters/nirf_faculty_counts.csv (the counts
                    the roster notes documented; blank where none was extracted), and the share of current rows with a joining year.
Outputs (results/), read by nothing else:
  faculty_cohort.csv       per institute: cohort size, cohort members with papers, papers / citations / h-index per cohort member (members
                           without a paper count as 0), the same for all current faculty, median h of the faculty with papers (the
                           existing statistic), the rank on papers per cohort member among institutes with a large enough cohort, warning
  roster_completeness.csv  per institute: roster rows, current rows, share with joining year, NIRF working / regular count and edition,
                           current / NIRF, flag ('roster short' < 0.90, 'roster longer than NIRF' > 1.15, 'no NIRF count')
usage: python stats_faculty_cohort.py       (needs results/faculty.csv from stats_bibliometric.py)"""
import os, csv, re, statistics as st, collections as C
from common import INSTS, RES, A2, read_csv, write_csv, safe_div
from scope import FACULTY_DEPT_OUT

COHORT_MAX_JOIN = 2017          # joined by 2017 = at least 9 of the 11 window years (2016-2026)
MIN_COHORT = 20
LOW, HIGH = 0.90, 1.15
ROSTERS = os.path.join(A2, "WebScrape", "rosters")


def roster_people(inst):
    """[{rid, name, department, status, joining_year}] one per person (rows sharing an ORCID are one person: first row's rid, as
    Enrichment/scripts/faculty.py)."""
    fn = os.path.join(ROSTERS, f"{inst}_faculty.csv")
    if not os.path.exists(fn):
        return None
    out, first = [], {}
    for i, r in enumerate(csv.DictReader(open(fn, encoding="utf-8-sig"))):
        o = (r.get("orcid") or "").strip().replace("https://orcid.org/", "") or None
        rid = first.setdefault(o, f"{inst}:{i}") if o else f"{inst}:{i}"
        jy = re.match(r"(\d{4})", (r.get("joining_year") or "").strip())
        out.append({"rid": rid, "dup": bool(o) and rid != f"{inst}:{i}", "name": r["name"], "department": r.get("department") or "",
                    "status": r.get("status") or "", "jy": int(jy.group(1)) if jy else None})
    return [p for p in out if not p["dup"]]


def nirf_counts():
    fn = os.path.join(ROSTERS, "nirf_faculty_counts.csv")
    if not os.path.exists(fn):
        return {}
    return {r["inst"]: r for r in read_csv(fn)}


def num(x):
    try:
        return int(x)
    except (TypeError, ValueError):
        return None


def med(v):
    return float(st.median(v)) if v else ""


def mean(v):
    return round(sum(v) / len(v), 2) if v else ""


def main():
    fac = C.defaultdict(dict)
    for f in read_csv(os.path.join(RES, "faculty.csv")):
        fac[f["institution"]][f["roster_id"]] = f
    nirf = nirf_counts()
    crow, rrow, missing = [], [], []
    for inst, name in INSTS.items():
        people = roster_people(inst)
        if people is None:
            missing.append(inst)
            continue
        cur = [p for p in people if p["status"] == "current"]
        cur_scope = [p for p in cur if p["department"] not in FACULTY_DEPT_OUT]
        cohort = [p for p in cur_scope if p["jy"] is not None and p["jy"] <= COHORT_MAX_JOIN]
        have = fac[name]

        def stats(ps):
            fs = [have.get(p["rid"]) for p in ps]
            papers = [num(f["papers"]) or 0 if f else 0 for f in fs]
            cit = [num(f["citations"]) or 0 if f else 0 for f in fs]
            h = [num(f["h_index"]) or 0 if f else 0 for f in fs]
            return papers, cit, h, sum(1 for f in fs if f)
        cp, cc, ch, cwith = stats(cohort)
        ap, ac, ah, awith = stats(cur_scope)
        wh = [num(f["h_index"]) for f in have.values() if num(f["h_index"]) is not None]
        warn = ""
        if len(cohort) < MIN_COHORT:
            warn = (f"cohort too small: {len(cohort)} current faculty with joining year <= {COHORT_MAX_JOIN} (< {MIN_COHORT}); "
                    f"{sum(1 for p in cur_scope if p['jy'] is None)} of {len(cur_scope)} current people have no joining year")
            print("WARNING", name, warn)
        crow.append({"institution": name, "cohort_definition": f"current, joining_year <= {COHORT_MAX_JOIN}, in field scope",
                     "cohort_size": len(cohort), "cohort_with_papers": cwith,
                     "cohort_mean_papers": mean(cp), "cohort_median_papers": med(cp), "cohort_median_citations": med(cc),
                     "cohort_median_h": med(ch), "cohort_mean_h": mean(ch),
                     "all_current_in_scope": len(cur_scope), "all_current_with_papers": awith,
                     "all_current_mean_papers": mean(ap), "all_current_median_h": med(ah),
                     "published_median_h_faculty_with_papers": med(wh),
                     "warning": warn})
        n = nirf.get(inst) or {}
        nw, nr = num(n.get("nirf_working")), num(n.get("nirf_regular"))
        ref = nr if nr else nw
        ratio = round(len(cur) / ref, 3) if ref else ""
        flag = "no NIRF count" if not ref else "roster short" if ratio < LOW else "roster longer than NIRF" if ratio > HIGH else "ok"
        rrow.append({"institution": name, "roster_rows": len(people), "current_rows": len(cur),
                     "current_with_joining_year": sum(1 for p in cur if p["jy"] is not None),
                     "share_current_with_joining_year": safe_div(sum(1 for p in cur if p["jy"] is not None), len(cur)),
                     "nirf_edition": n.get("nirf_edition", ""), "nirf_working": nw if nw is not None else "",
                     "nirf_regular": nr if nr is not None else "", "current_over_nirf": ratio, "flag": flag,
                     "nirf_note": n.get("note", "")})
        if flag in ("roster short", "roster longer than NIRF"):
            print("NOTE", name, f"{len(cur)} current roster rows against NIRF {ref} ({edition_of(n)}): {flag}")
    ok = {r["institution"]: r["cohort_mean_papers"] for r in crow if r["cohort_size"] >= MIN_COHORT and r["cohort_mean_papers"] != ""}
    order = sorted(ok.values(), reverse=True)
    for r in crow:
        r["rank_mean_papers_among_cohorts_of_20plus"] = order.index(ok[r["institution"]]) + 1 if r["institution"] in ok else ""
    write_csv("faculty_cohort.csv", crow)
    write_csv("roster_completeness.csv", rrow)
    if missing:
        print("no roster file for", ", ".join(missing))
    for r in crow:
        print({k: r[k] for k in ("institution", "cohort_size", "cohort_with_papers", "cohort_mean_papers", "cohort_median_h", "warning")})


def edition_of(n):
    return "NIRF " + n.get("nirf_edition", "?")


if __name__ == "__main__":
    main()
