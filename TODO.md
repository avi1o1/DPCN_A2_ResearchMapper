# TODO — pick what we do for the second round

One line per task. Effort: (S) a few hours, (M) a day or two, (L) several days. Details and references for the new
analyses are in [docs/research_directions.md](docs/research_directions.md) (section numbers in brackets).

## Already done
- Data, the four CSV files, report (rephrased, roll numbers, dashboard link), dashboard on GitHub Pages, data on the TAs' Drive.
- Stats: trends, Q1, IF > 5 / > 10, CORE, h-index and i10 (incl. why h is low), departments, big-team papers.
- Networks: PageRank (+ corrected), in-degree, preferential attachment, self-citations, communities, null models,
  k-core, rich club, robustness, SIR spreading, network growth.

## 1. Professor's follow-up questions (part 1)
- [ ] (S) List all 16 PRL papers (10 KGP, 6 Roorkee) in the report.
- [ ] (S) Table of the Nature group journals and their IF (all above 10 except Nature Cities, 9.3).
- [ ] (S) List of IF > 10 papers with fewer than 10 authors (KGP 1,057, Roorkee 736) and which journals they are in.
- [ ] (S) The class-notes grid: Q1 / Q1 + IF > 10 / Q1 + IF > 5, each split into fewer vs more than 10 authors.
- [ ] (S) Say clearly that our IF (OpenAlex) runs higher than the official Clarivate IF.

## 2. New analysis — choose 2 or 3 (the "something new" part)
- [ ] (M) Teams as groups, not pairs (hypergraph): who is central when a paper links all its authors at once [§1b, §1c].
- [ ] (M) Do three people who wrote in pairs later write together as three? Use it to predict next year's teams [§1a].
- [ ] (M) Who cites their own co-authors, how much, and does citing come before working together [§3b].
- [ ] (S) New ranking methods (Katz, HITS hubs/authorities, communicability) instead of PageRank [§2].
- [ ] (S) Which faculty connect people early on, using the year-by-year co-authorship networks [§2, dynamic].
- [ ] (S) Core and periphery of the faculty citation network (the bow-tie idea from Mendes's own paper) [§3c].
- [ ] (S) Which research areas each department is strong in, and predicting which areas it moves into next [§3f].
- [ ] (S) Do teams mixing several departments get more citations [§3d].
- [ ] (L) Do small teams make more "disruptive" papers than big ones (needs a large OpenAlex download) [§3a].

## 3. Report and dashboard
- [ ] (M) Add the chosen new analyses as report sections, each with a clear "key finding" in one sentence.
- [ ] (S) A "Key findings" list at the start of the report and on the dashboard (the professor asked for this).
- [ ] (M) Dashboard panels for the new analyses (for example a "real teams" view and a "likely next collaborators" list).
- [ ] (S) Re-check every new number by recomputing it a second way before it goes in.

## 4. Discussion prep (after 25 Oct)
- [ ] (S) Short slides or notes: key statistics, network results, why they matter, modelling used, related methods.
- [ ] (S) Ask the professor which José Fernando Mendes dashboard he meant (not found online).

## 5. Housekeeping
- [ ] (S) Fix the duplicate SciPy 1.0 entry in the "most cited papers citing us" table.
- [ ] (S) Run `git lfs pull` in this clone before re-running any statistics (the big data files are placeholders here).
- [ ] (M) Optional: finish the yearly faculty lists from old institute websites (script exists, the download was slow and its cache was lost).
