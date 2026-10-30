"""Mega-collaboration papers (more than 100 authors) and what they do to the institute comparison (sanity audit F3, 2026-10-30).
stats_large_collab.py asks the same question for papers of more than 10 authors; this script uses the `mega_collab` flag that the
scrape and the enrichment stage put on every record (WebScrape/scripts/finalize.py: Crossref author list, channel list as
fallback; Enrichment/scripts/oa_extract.mega_flag: scraped list, then OpenAlex's list, capped at 100 authors, so there 100 or
more counts as mega). A record without any author list has an unknown flag and is counted as 'not mega' here (listed per institute).
Every per-institute statistic is given with and without the mega papers; citations per paper is the one the audit found unstable
(Gandhinagar 29.3 -> 13.3, rank 1 -> 10), so the institutes should not be ranked on it including them.
Outputs (results/):
  mega_by_institute.csv   per institute: papers, mega papers and their share, share of all citations, flag basis, unknown flags,
                          the person with most mega papers
  mega_with_without.csv   per institute and metric: all papers, without mega papers, change, change in % (papers, citations,
                          citations per paper, median citations, papers with >= 100 citations, Q1 share of ranked journal
                          papers, institute h-index, faculty with papers, median / mean / max faculty h-index)
  mega_ranks.csv          rank of every institute (1 = highest) on citations per paper, median faculty h-index and papers, with and
                          without mega papers, and the rank change
usage: python stats_mega_collab.py"""
import statistics as st, collections as C
import numpy as np
from common import INSTS, load_records, paper_key, cites, h_index, write_csv, safe_div
from oa_extract import mega_flag


def is_mega(r):
    return bool(mega_flag(r)[1])


def headline(rs):
    cs = [cites(r) for r in rs if cites(r) is not None]
    ranked = [r for r in rs if r["type"] == "journal" and (r.get("quartile") or {}).get("quartile")]
    fac = C.defaultdict(dict)
    for r in rs:
        for f in r["faculty"]:
            fac[f["roster_id"]][paper_key(r)] = cites(r)
    hs = [h_index(list(ps.values())) for ps in fac.values()]
    return {"papers": len(rs), "citations": sum(cs),
            "citations per paper": round(sum(cs) / len(cs), 2) if cs else "",
            "median citations per paper": st.median(cs) if cs else "",
            "papers with >= 100 citations": sum(1 for c in cs if c >= 100),
            "Q1 share of ranked journal papers": safe_div(sum(r["quartile"]["quartile"] == "Q1" for r in ranked), len(ranked)),
            "institute h-index": h_index(cs),
            "faculty with papers": len(hs),
            "median faculty h-index": float(np.median(hs)) if hs else "",
            "mean faculty h-index": round(float(np.mean(hs)), 2) if hs else "",
            "max faculty h-index": max(hs, default="")}


def ranks(vals):
    """{name: rank} with 1 = highest; institutes without a value are left out; ties share the better rank."""
    v = {k: x for k, x in vals.items() if isinstance(x, (int, float))}
    order = sorted(v.values(), reverse=True)
    return {k: order.index(x) + 1 for k, x in v.items()}


def main():
    inst_rows, rows, per = [], [], {}
    for inst, name in INSTS.items():
        rs = load_records(inst)
        mega = [r for r in rs if is_mega(r)]
        rest = [r for r in rs if not is_mega(r)]
        a, b = headline(rs), headline(rest)
        per[name] = (a, b)
        for k in a:
            row = {"institution": name, "metric": k, "all_papers": a[k], "without_mega": b[k]}
            if isinstance(a[k], (int, float)) and a[k] and isinstance(b[k], (int, float)):
                row["change"] = round(b[k] - a[k], 4)
                row["change_pct"] = round(100 * (b[k] - a[k]) / a[k], 2)
            rows.append(row)
        cit_all, cit_mega = a["citations"], sum(cites(r) or 0 for r in mega)
        by_person = C.Counter(f["name"] for r in mega for f in r["faculty"])
        top = by_person.most_common(1)
        inst_rows.append({"institution": name, "papers": len(rs), "mega_papers": len(mega), "mega_share_of_papers": safe_div(len(mega), len(rs)),
                          "mega_share_of_citations": safe_div(cit_mega, cit_all),
                          "flag_unknown": sum(1 for r in rs if mega_flag(r)[1] is None),
                          "flag_basis": "; ".join(f"{k or 'none'}: {v}" for k, v in C.Counter(mega_flag(r)[2] for r in rs).most_common()),
                          "person_with_most_mega_papers": f"{top[0][0]} ({top[0][1]})" if top else ""})
    write_csv("mega_by_institute.csv", inst_rows)
    write_csv("mega_with_without.csv", rows, ["institution", "metric", "all_papers", "without_mega", "change", "change_pct"])
    rk = []
    for metric in ("citations per paper", "median faculty h-index", "papers"):
        ra = ranks({n: a[metric] for n, (a, b) in per.items()})
        rb = ranks({n: b[metric] for n, (a, b) in per.items()})
        for n, (a, b) in per.items():
            if n in ra and n in rb:
                rk.append({"metric": metric, "institution": n, "value_all": a[metric], "rank_all": ra[n], "value_without_mega": b[metric],
                           "rank_without_mega": rb[n], "rank_change": ra[n] - rb[n]})
    write_csv("mega_ranks.csv", rk)
    for r in inst_rows:
        print(r)
    moved = [r for r in rk if r["metric"] == "citations per paper" and abs(r["rank_change"]) >= 3]
    for r in sorted(moved, key=lambda r: -abs(r["rank_change"])):
        print("citations per paper rank moves by", r["rank_change"], ":", r["institution"], r["value_all"], "->", r["value_without_mega"])


if __name__ == "__main__":
    main()
