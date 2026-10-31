# Analysis v2: how to rerun (all institutes in `Enrichment/out_v2`)

The multi-institute run reads `Enrichment/out_v2/` (read-only) and writes `Analysis/results_v2/`, `Analysis/figures_v2/` and
the draft page `Dashboard/site/v2/` (`data_v2.js`, `index.html`). It never calls OpenAlex or Crossref
(`ANALYSIS_OFFLINE` is 1 under `ANALYSIS_PROFILE=v2`). Python needs matplotlib, networkx, numpy, scipy, pandas, scikit-learn,
statsmodels, powerlaw, python-igraph, leidenalg (the run of 31 October 2026 used networkx 3.7, numpy 2.5, scipy 1.18).

## Which institutes are analysed

`ANALYSIS_PROFILE=v2` without `ANALYSIS_INSTS` selects the preset `auto` (= `v2all`): every institute of the registry
(`REGISTRY` in `Analysis/scripts/common.py`) that has `iit_<inst>_enriched.json` **and** rows in `group3_data.csv` in the input
folder, in registry order. So `iit_kharagpur` and `iit_roorkee` join the run by themselves once their files are in
`Enrichment/out_v2/` (and `group3_data.csv` has their rows); nothing needs editing. Other values of `ANALYSIS_INSTS`:
`v2` = the same without Kharagpur and Roorkee (the first-round list), `v2all` = `auto`, or a comma list of keys.
The run prints and the tables show the institutes used; check `results_v2/trend.csv` (one block per institute).

## Rerun

```
cd Analysis/scripts
export ANALYSIS_PROFILE=v2 ANALYSIS_IN_DIR=/home/avilol/Downloads/GitHub/ANLP_A2_ResearchMapper/Enrichment/out_v2 ANALYSIS_KEEP_GOING=1
# PYTHON=/path/to/venv/bin/python if python is not the one with the libraries
sh run_all.sh                                   # about 25 minutes, peak about 3 GB; stats_authorship.py is the slow one
python ../../Dashboard/site/v2/build_data_v2.py # writes Dashboard/site/v2/data_v2.js (under 1 MB)
```

Results: `results_v2/run_times.csv` (seconds and peak memory of each script, `exit_code` 0 = fine),
`results_v2/skipped_panels.csv` (panels that need OpenAlex data not cached; they stay skipped, never zero-filled).
Open `Dashboard/site/v2/index.html` in a browser (it loads ECharts from cdnjs).

Run one heavy script at a time: `stats_coauthor_citation.py` and `stats_matrix_centrality.py` are the largest in memory.

## When the credits-dependent steps complete (about 05:30 on 1 November 2026)

1. The enrichment owner refreshes `Enrichment/out_v2/` (bombay, madras, kanpur, guwahati, delhi, ropar complete; kharagpur and
   roorkee added). Nothing in the Analysis folder is edited.
2. Rerun the three commands above (`export ...`, `sh run_all.sh`, `build_data_v2.py`).
3. Remove the "partial enrichment" badges: they come from `PARTIAL_DEFAULT` in `Dashboard/site/v2/build_data_v2.py`
   (bombay, madras, kanpur, guwahati, delhi, ropar). Either run the builder with an empty list:

   ```
   DASH_PARTIAL= python ../../Dashboard/site/v2/build_data_v2.py
   ```

   or with only the institutes that are still partial, e.g. `DASH_PARTIAL=delhi,ropar`; for a lasting change edit
   `PARTIAL_DEFAULT`. With an empty list the badge, the note under the page title and the per-institute banner are not drawn.
4. If OpenAlex credits are available and the OpenAlex extras are wanted (IF, yearly citation counts, FWCI, author profiles),
   run the online steps first (this calls OpenAlex; it is not part of the offline run):
   `ANALYSIS_OFFLINE=0 OPENALEX_KEY_FILE=<key file> python fetch_openalex_extra.py`, then `sh run_all.sh` with
   `ANALYSIS_OFFLINE=0` as well, so that `stats_connectivity.py` and `stats_citing_top.py` can fill their panels. The skipped
   panels listed at the bottom of the page then fill in.
5. Screenshot check (headless Chrome): `Analysis/figures_v2/screens/` has the pages of the 31 October interim run.

## Sanity statistics added to the run

* `stats_mega_collab.py`: every per-institute statistic with and without papers of more than 100 authors
  (`mega_by_institute`, `mega_with_without`, `mega_ranks`); page section "Papers with more than 100 authors".
* `stats_faculty_cohort.py`: per-faculty numbers for current faculty who joined by 2017, and roster completeness against the
  NIRF counts (`faculty_cohort`, `roster_completeness`); page section "Faculty cohort: joined by 2017". A cohort below 20 people
  is flagged and not ranked; an institute whose roster lacks joining years (IIT Delhi, about 14 % of current rows have one)
  has a cohort that is only a small part of its faculty.

## Notes on the interim run

* Quartiles come from the Scimago 2016 and 2020 tables only; the latest available table is used for the other years.
* The six partial institutes have no complete Indian-citation steps and no title search yet: their citation-flow, partner and
  network figures (and the shared-paper matrix) are interim, and their paper counts can still grow.
* Run settings of `common.py` are documented in its docstring (`ANALYSIS_INSTS`, `ANALYSIS_PROFILE`, folders, offline mode).

## Run of 31 October 2026 (21 institutes, interim set): timings, failures, fixes

22 scripts, about 30 minutes of script time, peak memory 3.2 GB (`stats_matrix_centrality.py` 3,206 MB,
`stats_coauthor_citation.py` 3,207 MB). Slowest: `stats_authorship.py` 1,024 s (null models on a faculty network of about 6,200
people), `stats_matrix_centrality.py` 432 s. Per-script values: `results_v2/run_times.csv`. Two scripts failed on the first
pass and were fixed:

* `stats_coauthor_citation.py` (killed at about 4.9 GB, above the memory limit set for the run): with 21 institutes the n x n
  pair arrays (n = 6,200 faculty) were int64 index arrays, a string array of distance classes and a float64 distance matrix.
  Now int32 indices, int8 distance classes and strata, a float32 distance matrix and a sparse matrix for the check count; the
  order of the pairs and all counts are unchanged. 60 s, 3.2 GB.
* `stats_dept_areas.py` (ValueError, NaN): the fitness-complexity map divided by the fitness of a department with no strong
  subfield (all departments of IIT Ropar, which has no OpenAlex research-area data yet: every paper is 'Unknown') and the whole
  map turned to NaN. Such departments are now left out of the map and written with an empty rank.
