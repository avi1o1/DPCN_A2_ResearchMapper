# IIIT sanity-rule rerun: steps for the IIIT team (2026-11-01)

Why: the IIT datasets went through the sanity rules of PROCESS.md §15.17 (start-year rule F1, namesake guard F5, `affiliation_substatus`,
`mega_collab`, cohort statistics) and the arXiv co-author cap (§15.18). The IIIT datasets on `v2-all-institutes` were built before these
rules (their JSON records carry no `affiliation_substatus` / `mega_collab`; `finalize.py` applies the demotions to the IIITs only when
`RM_SANITY_RULES=all`). The rerun needs the raw caches (`WebScrape/raw/`, `Enrichment/cache_v2` with the IIIT OpenAlex caches,
`Enrichment/cache/scimago` with all ten Scimago years), which exist only on the machine where the IIIT pipeline ran, so it cannot be done
from the repository alone.

Already done in the repository (commit of 2026-11-01): founding dates of all 30 IIITs in `scripts/institutes.py`; F7 in `finalize.py`;
`verify.py` tolerance fix; the runner `scripts/iiit_sanity_rerun.sh`. Dry run on the committed files: F1 would demote 56 of 12,813
likely-tier records.

## Steps
1. `git pull origin v2-all-institutes` (needs the files above).
2. `sh WebScrape/scripts/iiit_sanity_rerun.sh`  (all 30; or name institutes). It runs, with `RM_SANITY_RULES=all`:
   `run_v2.sh refresh` (merge, OpenCitations fallback, finalize with F1/F5/F7, recall, TODO sheet, `validate.py`), then the offline
   enrichment rebuild into `Enrichment/out_v2_iiit` (merge, faculty, verify, export, networks, network checks). No new discovery, no
   OpenAlex credits. Expect hours (the IIT refresh took about 18 min per large institute); it can be run per institute.
3. Check: `validate.py` 0 violations; `verify` passes (`author_count` / `mega_*` no longer flagged); records per institute fall by the
   demoted counts (see `v2/logs/startyear_demoted_*`, `namesake_demoted_*`, `arxivcap_demoted_*`).
4. Keep the ten-year Scimago files (rule: paper-year file, else the journal's latest year). Do not rerun Scimago.
5. Recompute recall (`run_v2.sh refresh` does it) and carry the precision-audit verdicts over by DOI as in `PROCESS_IIIT.md` §7.6; demoted records
   simply leave the likely tier. Update the tables in `PROCESS_IIIT.md` §6, §7.3, §7.5 and note the rerun in a new §7.7.
6. Commit the changed `v2/iiit_*.json`, `Enrichment/out_v2_iiit/*` (same files as before) and push to `v2-all-institutes`.
