# TODO — pick what we do for the second round

One line per task. Effort: (S) a few hours, (M) a day or two, (L) several days. Details and references for the new
analyses are in [docs/research_directions.md](docs/research_directions.md) (section numbers in brackets).
Status: [x] done, [~] in progress (note says what is left), [ ] not started. Work order agreed on 26 Oct:
5 (setup) → 1 → 2 (Katz/HITS → early connectors → hypergraph → simplicial closure) → 3 → 4.
27 Oct: the v2 all-institutes scrape is paused (state in the v2 clone's WebScrape/PROCESS_OTHER.md §7); focus is section
6 (Mendes-style dashboard), then the open items of section 2.

## Progress log (final, checked numbers; all on the real data after `git lfs pull`)
- 26 Oct, checks done on everything below: second independent count, deterministic re-run (identical files),
  scores that are zero outside one network part are no longer ranked (they were noise before), name-keyed authors
  split per paper as a check (no headline moves), all new references checked on Crossref / PubMed. Rank comparisons
  of eigenvector-type scores use only the nodes where the score is non-zero (faculty giant component, HITS support).
- Professor's tables (`stats_if_authors.py`): match the numbers already sent and an independent recount from
  `group3_data.csv`, cell by cell. PRL 10 KGP + 6 Roorkee (IF 9.05). Nature journals: 16 in our data, all IF > 10
  except Nature Cities (9.31). IF > 10: KGP 1,148 (1,057 with < 10 authors), Roorkee 797 (736). Grid has a column for
  exactly 10 authors so it adds up; Q1 totals match `quartiles.csv`.
- Matrix centralities (`stats_matrix_centrality.py`):
  - Faculty network: the eigenvector sits on one dense Kharagpur group. 45% of its weight is on 10 faculty (9 of them
    in the 23-member top k-core, all KGP). Only 1.3% is on Roorkee faculty, who are 45% of all faculty.
  - Katz moves from the degree ranking to the eigenvector ranking as its parameter grows (giant component, 1,110
    faculty: Spearman with degree 0.99 → 0.69, with eigenvector 0.67 → 0.99). Degree vs eigenvector: 0.61.
  - Campus closeness (communicability angle): KGP 0.35, Roorkee 0.14, between campuses 0.066. Removing Pradip K. Maji
    (Roorkee, 6 cross-campus co-authors) lowers the campus communicability ratio by 31%; 18 faculty lower it by > 5%.
  - Citation network: HITS authority is non-zero for only 5,086 of 46,072 papers (30 papers in the 2020 network);
    on its support its Spearman with worldwide citations is only 0.13. 72 of its top 100 papers are one MOF chemistry group. Katz top 100: 26 from the same group. Largest citation cycle:
    10 papers of one Roorkee author (sets the spectral radius 2.93).
  - Prediction of 2021-26 citations from the network at end of 2020 (mean Spearman within publication year):
    in-degree 0.38, Katz 0.38, PageRank 0.36, worldwide citations so far 0.75; HITS not rankable (non-zero for 30
    papers). Expected: our internal network is a thin slice of all citations.
  - At equal past worldwide citations, papers whose citations were more often self-citations get fewer citations
    later (partial Spearman -0.087, within-band -0.093, negative in 15 of 16 bands). A self-citation does not signal
    impact the way an outside citation does. Internal non-self citations: about zero (+0.04, 2 of 16 negative).
  - Early connectors (dynamic communicability): Amit Basak (degree rank 104) and Sunando Dasgupta (157) rank 11-12.
- Hypergraph (`stats_hypergraph.py`): 41,435 authors, 38,089 papers. The 696 papers with > 10 authors (1.8%) give 27%
  of author pairs. Linear and max models put 87% and 97% of their weight on 10 authors, on different labs (faculty
  Spearman 0.69). log-exp collapses on 33 authors and 88 papers (3 faculty), so it cannot rank faculty at all. Without the > 10-author
  papers the linear top 20 changes 17 of 20, partly because two labs almost tie (s1/s2 = 1.003); distinct co-author
  counts keep 16 of 20. Linear power method = exact singular vector (Spearman 1.0).
- Simplicial closure (`stats_simplicial.py`, Benson et al. 2018; papers <= 25 authors, check <= 10; train <= 2021):
  - 96% of triangles in the all-author pairwise graph come from one paper with all three; faculty network 54%
    (partly mechanical: only 659 papers have >= 3 faculty).
  - Chance that three authors write together after 2021, by how many of their pairs already had: 0 pairs 2.9e-9,
    1 pair 5.9e-6, 2 pairs 0.45%, all 3 (open triangle) 3.7% (95% CI 3.2-4.4%).
  - Which open triangles close is hard to predict: best score (harmonic mean of tie strengths) ROC AUC 0.56, p = 0.005
    with cap 25, not significant with cap 10 (p = 0.10). Call it weak.
- 26 Oct, review fixes: early connectors broadcast vs degree is 0.80 over the 1,156 faculty with a faculty co-author
  (0.89 included zero ties). New trios by earlier pairs: 0 → 20%, 1 → 49%, 2 → 30%, open triangle → 0.8%
  (probability per trio rises, but most new trios come from the many trios with fewer pairs). The co-authorship file
  holds papers with >= 1 linked faculty and <= 50 authors, so its > 10-author count is 696, against 979 distinct in
  `group3_data.csv` (259 no faculty, 23 over 50 authors, 1 other); stated in the report.
- `run_all.sh` runs the four new scripts (before the roster step, which needs the lost Wayback cache).

- 27 Oct: Mendes-style profile explorer started (section 6). Its data builder (`Dashboard/site/build_profiles.py`)
  recomputes papers, citations, h-index, i10-index and Q1 papers for all 1,410 faculty and refuses to write unless every
  value equals `results/faculty.csv` — 0 mismatches. It found 8 DOIs that occur twice in the KGP analysis set (online-
  first year and issue year, different citation counts); checked on Crossref: in all 8 the later record has Crossref's
  issued year and citation count, and it is the record `faculty.csv` already keeps. OpenAlex FWCI fetched for all 45,986
  works (461 credits).

## 6. Mendes-style dashboard (prof's request, 27 Oct: "present data like jfmendes-sciart.github.io")
Reference: the research page's summary tiles, ego co-author network and the 12-page Power BI report (screenshots in
`rm_v2_work/mendes/`). Our version: `Dashboard/site/explorer.html`, data `profiles.js` (built offline, self-checked).
- [x] (S) Data builder with the same paper set and definitions as the statistics; FWCI fetch; self-check vs faculty.csv.
- [~] (M) Explorer page: scope = both IITs / one IIT / department / faculty member, year range; KPI tiles (papers,
  citations, citations per paper, cited %, h, i10, Q1, most-cited, avg FWCI, single-author equivalent, first / last
  author, co-authors, partner institutions, years active); papers / citations per year, citations per paper by year,
  quartile per year, type and quartile donuts; top journals, topics, partner institutions (papers, citations, FWCI),
  most-cited papers; ego co-author network (top 10 / 20 / all); researcher scatter; paper search card; compare two.
- [ ] (S) Second-way check of the explorer's numbers in the browser against `faculty.csv` / `departments.csv`.
- [ ] (S) Link from the main dashboard; README note. Not possible with our data: Scopus topic prominence, CiteScore.

## Already done
- Data, the four CSV files, report (rephrased, roll numbers, dashboard link), dashboard on GitHub Pages, data on the TAs' Drive.
- Stats: trends, Q1, IF > 5 / > 10, CORE, h-index and i10 (incl. why h is low), departments, big-team papers.
- Networks: PageRank (+ corrected), in-degree, preferential attachment, self-citations, communities, null models,
  k-core, rich club, robustness, SIR spreading, network growth.

## 1. Professor's follow-up questions (part 1)
- [x] (S) List all 16 PRL papers (10 KGP, 6 Roorkee) in the report. Table IV (III-E); titles with maths taken from
  Crossref; one KGP entry is a reply to a comment, marked as such.
- [x] (S) Table of the Nature group journals and their IF (all above 10 except Nature Cities, 9.3). Table V.
- [x] (S) List of IF > 10 papers with fewer than 10 authors (KGP 1,057, Roorkee 736) and which journals they are in.
  Table VIII (top 5 journals each); full list in `if10_small_team_papers.csv`.
- [x] (S) The class-notes grid: Q1 / Q1 + IF > 10 / Q1 + IF > 5, each split into fewer vs more than 10 authors.
  Table VII (III-J), journal papers only, exactly-10 column.
- [x] (S) Say clearly that our IF (OpenAlex) runs higher than the official Clarivate IF. Already in III-C (Scientific
  Reports 5.2 vs about 3.8); PRL 9.05 is stated on our scale.

## 2. New analysis — choose 2 or 3 (the "something new" part)
- [x] (M) Teams as groups, not pairs (hypergraph) [§1b, §1c]. In the report (VIII-E).
- [x] (M) Do three people who wrote in pairs later write together as three? [§1a]. In the report (VIII-F).
- [ ] (M) Who cites their own co-authors, how much, and does citing come before working together [§3b].
- [x] (S) New ranking methods (Katz, HITS hubs/authorities, communicability) instead of PageRank [§2]. In the report (VIII-A, B, D).
- [x] (S) Which faculty connect people early on, using the year-by-year co-authorship networks [§2, dynamic]. In the report (VIII-C).
- [ ] (S) Core and periphery of the faculty citation network (the bow-tie idea from Mendes's own paper) [§3c].
- [ ] (S) Which research areas each department is strong in, and predicting which areas it moves into next [§3f].
- [ ] (S) Do teams mixing several departments get more citations [§3d].
- [ ] (L) Do small teams make more "disruptive" papers than big ones (needs a large OpenAlex download) [§3a].

## 3. Report and dashboard
- [x] (M) Add the chosen new analyses as report sections. Section VIII "Beyond Pairs and PageRank" (16 pages now);
  tables generated by `Report/make_tables.py`; compiles with no undefined references or overfull boxes.
- [x] (S) A "Key findings" list at the start of the report and on the dashboard. Report I-A; dashboard overview
  (same 8 findings, numbers built from the CSVs).
- [x] (M) Dashboard panels for the new analyses. Quality: all PRL papers, Nature journals with IF, team-size grid;
  new section "Beyond pairs". Data rebuilt (SciPy duplicate gone from the site). Checked in headless Edge, both
  themes, no console errors. Local only: goes live when pushed.
- [~] (S) Re-check every new number by recomputing it a second way before it goes in. Done for all numbers so far.

## 4. Discussion prep (after 25 Oct)
- [ ] (S) Short slides or notes: key statistics, network results, why they matter, modelling used, related methods.
- [x] (S) Ask the professor which José Fernando Mendes dashboard he meant (not found online). Mail sent 26 Oct.
- [ ] (M) Possible addition for the "modelling" point of the brief: a dynamical model on our data, e.g. research
  topics spreading along co-author teams (simplicial contagion). Not started; team to decide.

## 5. Housekeeping
- [x] (S) Fix the duplicate SciPy 1.0 entry in the "most cited papers citing us" table. Same-title records now count
  once; LiTS benchmark moves into the KGP top 10. Report text still correct; dashboard data rebuilt.
- [x] (S) Run `git lfs pull` in this clone before re-running any statistics. Done; both files match their checksums.
- [x] (S) Send the Mendes mail to the professor. Sent 26 Oct; waiting for his reply.
- [ ] (M) Optional: finish the yearly faculty lists from old institute websites (script exists, the download was slow and its cache was lost).
