# Resuming the v2 run (state at 2026-10-31 15:35, everything stopped on purpose)

## State
* 23 institutes (20 new IITs + Kharagpur, Roorkee, Ropar) have finished the v2 procedure (roster, arXiv pass, loose pass, verify, refresh with the
  sanity rules); recall and precision audits exist for all of them except the Kharagpur recall/audit (its refresh finished at 15:31; flag
  `WebScrape/logs/pq4/iit_kharagpur.ready`).
* OpenAlex enrichment (`Enrichment/out_v2`): complete for 19 institutes (`WebScrape/logs/pq4/<inst>.enriched`). Still to do: Madras, Bombay, Roorkee,
  Kharagpur. Their OpenAlex caches are partly filled; every step resumes from `Enrichment/cache_v2`.
* Quartiles: Scimago files for 2016, 2020, 2025 only (`Enrichment/cache/scimago`, git-ignored); other years use the journal's latest available year.
  The other seven years were not found and are skipped (decision 2026-10-31).
* The OpenAlex keys (`.env`, `OPENALEX_KEYS`) reset at about 05:30 local time; OpenAlex's free unauthenticated allowance is also used.

## To resume (any time after the credit reset, or earlier for whatever credits exist)
1. `systemctl --user start iit-final.service`   (credit-aware runner; finishes Madras, Bombay, Roorkee, Kharagpur; then export + networks for all)
   (the units were disabled for autostart; `systemctl --user enable iit-final.service` re-enables them; `iit-resume.service` is not needed now)
2. When `WebScrape/logs/pq4/ALL.enriched` exists: rerun the Analysis and the draft page, see `Analysis/README_v2.md`
   (`ANALYSIS_PROFILE=v2 ... sh run_all.sh`, then `Dashboard/site/v2/build_data_v2.py`; remove the "partial enrichment" badges with `DASH_PARTIAL=`).
3. Kharagpur recall and audit: `RM_OUT=v2 python3 WebScrape/scripts/eval_recall.py iit_kharagpur`, `precision_sample.py iit_kharagpur`, then the audit agent (brief as for the other institutes).
4. Recompute `WebScrape/V2_PROGRESS.md` (table of all institutes) and push.

Do not run export/networks while the runner is rewriting an institute's enriched file (it lacks the faculty links until its last step); the runner does the final export itself.
