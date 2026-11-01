# v2 run: final state (2026-11-01 09:50)

All 23 institutes (20 new IITs + Kharagpur, Roorkee, Ropar) have finished the v2 procedure: roster, arXiv pass, loose pass, verification, refresh
with the sanity rules, recall against the golden set, a precision audit of 65 sampled records, and OpenAlex enrichment (`WebScrape/logs/pq4/<inst>.enriched`
for all 23, `ALL.enriched`). Combined files: `Enrichment/out_v2/` (group3_data.csv, citation and authorship networks, indian_connections.csv; git-ignored,
too large for plain git). Analysis: `Analysis/results_v2/` and the draft page `Dashboard/site/v2/index.html` (all 23 institutes). Table of results: `WebScrape/V2_PROGRESS.md`.

Quartiles use the Scimago files for 2016, 2020 and 2025 only (`Enrichment/cache/scimago`, git-ignored); the other seven years were not found and are skipped.
Papers from years without a file use the journal's latest available year.

## To rerun parts
* Enrichment (resumable, credit-aware, all OpenAlex keys of `.env` plus the free allowance): `systemctl --user start iit-final.service`
  (the unit is not enabled for autostart). NB: run the combined export for ALL institutes, not the priority list:
  `ENRICH_INSTS=<all 23 keys comma separated> python3 Enrichment/scripts/export_csv.py && python3 build_networks.py && python3 verify_networks.py`
  (about 12 GB of memory for the network build; nothing else should run). Do not export while a runner rewrites an institute's file (it lacks the faculty
  links until its last step).
* Analysis and page: see `Analysis/README_v2.md`; python environment `~/.venvs/iit-analysis` (outside `/tmp`, which is wiped by a reboot).
* Open items: Scimago 2017-2019 and 2021-2024; the enrichment is otherwise complete.
