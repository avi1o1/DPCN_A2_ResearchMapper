"""Professor's follow-up (second round): PRL papers, Nature journals and their IF, high-IF papers by team size, and the
class-notes grid (Q1 / Q1 + IF > 5 / Q1 + IF > 10, split by number of authors).
Needs fetch_openalex_extra.py (sources, paper -> source). Journal papers only (Scimago quartile and IF exist for journals).
IF (OpenAlex) is the journal's current OpenAlex 2-year mean citedness (see stats_journals.py); it usually runs higher
than Clarivate's Journal Impact Factor, so 'IF > 10' here is not the same list as 'JIF > 10'.
Author counts come from OpenAlex (at most 100 listed). 'Exactly 10' authors is its own column, so the grid adds up.
Outputs (results/):
  prl_papers.csv                 every PRL paper, with faculty, authors and citations
  nature_journals_if.csv         each Nature journal we publish in: IF (OpenAlex) and papers per institute
  if10_small_team_papers.csv     papers in IF > 10 journals with fewer than 10 authors
  if10_small_team_journals.csv   the journals of those papers, with counts per institute
  q1_if_author_grid.csv          the grid, per institute
usage: python stats_if_authors.py"""
import collections as C
from common import INSTS, load_records, cites, write_csv, impact_factor, source_of, n_authors, oa_have, note_skip
from stats_journals import groups_of

LIMIT = 10


def team(r):
    n = n_authors(r)
    if n is None:
        return "authors unknown"
    return "fewer than 10" if n < LIMIT else "exactly 10" if n == LIMIT else "more than 10"


TEAMS = ["fewer than 10", "exactly 10", "more than 10", "authors unknown"]


def q1(r):
    return (r.get("quartile") or {}).get("quartile") == "Q1"


def row_of(name, r):
    f = impact_factor(r)
    return {"institution": name, "year": r["year"], "journal": r["venue"], "if_openalex": round(f, 2) if f is not None else "",
            "title": r["title"], "authors": "100+" if (n_authors(r) or 0) >= 100 else n_authors(r),
            "citations": cites(r), "faculty": "; ".join(f["name"] for f in r["faculty"]), "doi": r["doi"]}


def main():
    recs = {name: [r for r in load_records(inst) if r["type"] == "journal"] for inst, name in INSTS.items()}
    if not oa_have("sources", "paper_source"):
        note_skip("stats_if_authors.py", "Nature journals with IF, IF > 10 papers, Q1 / IF grid rows that use IF (nature_journals_if.csv, if10_small_team_*.csv, q1_if_author_grid.csv)",
                  "IF (OpenAlex) and the Nature-journal publisher test come from the OpenAlex source cache, which does not exist for these institutes (PRL list and the Q1 row are filled)",
                  "fetch_openalex_extra.py (OpenAlex credits): oa_sources.json, oa_paper_source.json")

    # ------------------------------------------------ PRL
    prl = [row_of(name, r) for name, rs in recs.items() for r in rs if "PRL" in groups_of(r)]
    prl.sort(key=lambda x: (x["institution"], x["year"], x["title"]))
    write_csv("prl_papers.csv", prl)

    # ------------------------------------------------ Nature journals
    nat = C.defaultdict(lambda: {"journal": "", "publisher": "", "if_openalex": None,
                                 **{n: 0 for n in INSTS.values()}})
    for name, rs in recs.items():
        for r in rs:
            if "Nature journals" in groups_of(r):
                d = nat[r["venue"]]
                d["journal"], d["publisher"], d["if_openalex"] = r["venue"], (source_of(r) or {}).get("publisher"), impact_factor(r)
                d[name] += 1
    nrows = sorted(nat.values(), key=lambda d: -(d["if_openalex"] or 0))
    for d in nrows:
        d["if_openalex"] = round(d["if_openalex"], 2) if d["if_openalex"] is not None else ""
        d["total"] = sum(d[n] for n in INSTS.values())
    write_csv("nature_journals_if.csv", nrows)

    # ------------------------------------------------ IF > 10 with fewer than 10 authors
    small = [(name, r) for name, rs in recs.items() for r in rs
             if (impact_factor(r) or 0) > 10 and team(r) == "fewer than 10"]
    prows = sorted((row_of(n, r) for n, r in small), key=lambda x: (x["institution"], -(x["if_openalex"] or 0), -(x["citations"] or 0)))
    write_csv("if10_small_team_papers.csv", prows)
    allhi = C.Counter((name, r["venue"]) for name, rs in recs.items() for r in rs if (impact_factor(r) or 0) > 10)
    jr = C.Counter((n, r["venue"]) for n, r in small)
    ifv = {r["venue"]: impact_factor(r) for _, r in small}
    jrows = [{"institution": n, "journal": v, "if_openalex": round(ifv[v], 2), "papers_fewer_than_10_authors": k,
              "papers_all_team_sizes": allhi[(n, v)]} for (n, v), k in jr.items()]
    jrows.sort(key=lambda x: (x["institution"], -x["papers_fewer_than_10_authors"], x["journal"]))
    write_csv("if10_small_team_journals.csv", jrows)

    # ------------------------------------------------ the grid
    rows_def = [("Q1", lambda r: q1(r)),
                ("Q1 and IF > 5", lambda r: q1(r) and (impact_factor(r) or 0) > 5),
                ("Q1 and IF > 10", lambda r: q1(r) and (impact_factor(r) or 0) > 10),
                ("IF > 10 (any quartile)", lambda r: (impact_factor(r) or 0) > 10)]
    grid = []
    for name, rs in recs.items():
        for label, test in rows_def:
            sel = [r for r in rs if test(r)]
            c = C.Counter(team(r) for r in sel)
            known = len(sel) - c["authors unknown"]
            grid.append({"institution": name, "row": label, "papers": len(sel), **{t: c[t] for t in TEAMS},
                         "share_fewer_than_10": round(c["fewer than 10"] / known, 4) if known else "",
                         "share_more_than_10": round(c["more than 10"] / known, 4) if known else ""})
    write_csv("q1_if_author_grid.csv", grid)

    for name in INSTS.values():
        print(name, "PRL", sum(p["institution"] == name for p in prl),
              "IF>10 & <10 authors", sum(p["institution"] == name for p in prows))
    print("Nature journals:", [(d["journal"], d["if_openalex"], d["total"]) for d in nrows])
    for g in grid:
        print(g)


if __name__ == "__main__":
    main()
