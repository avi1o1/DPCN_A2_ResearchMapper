# OpenAlex works for the v2 IIIT datasets

`a_works_<inst>.jsonl.gz`: one OpenAlex work per line (the Enrichment stage A `SELECT` fields) for every DOI in
`WebScrape/v2/<inst>.json`, fetched 2026-10-30 with `Enrichment/scripts/stage_a_fetch.py`. The command is
`WebScrape/scripts/openalex_fetch_v2.sh`, a wrapper that points the shared `oa.DATA` at `WebScrape/v2`; the shared
Enrichment scripts are unchanged. 97–99 % of each institute's DOIs were found.

Unzip into `Enrichment/cache/a_works_<inst>.jsonl` to use them with the Enrichment scripts; stage A then skips DOIs it has
already queried only if `cache/a_queried_<inst>.txt` exists, so otherwise it re-queries them (about 1 credit per 100 DOIs).
OpenAlex data is CC0. Only the online fetch was run: the offline Enrichment steps (merge, faculty, export, networks) are
still written for the v1 Kharagpur/Roorkee data.
