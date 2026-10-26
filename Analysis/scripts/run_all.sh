#!/bin/sh
# Re-run every statistic (tables -> ../results, charts -> ../figures) from Enrichment/out.
# Online steps, cached in ../cache after the first run (set OPENALEX_API_KEY or OPENALEX_KEY_FILE for new data):
#   fetch_openalex_extra.py  yearly citation counts, journal IF, faculty OpenAlex profiles (~200-600 credits)
#   stats_connectivity.py    topic profiles of new partners (1 credit each)
#   stats_citing_top.py      citation counts of citing works (~1,410 requests, no key needed)
set -e
cd "$(dirname "$0")"
export PYTHONIOENCODING=utf-8
python fetch_openalex_extra.py     # only fetches ids missing from the cache
python stats_bibliometric.py       # writes faculty.csv, used by the next three
python stats_faculty.py
python stats_journals.py
python stats_large_collab.py       # papers with more than 10 authors: effect on the headline numbers, where they are
python stats_areas.py
python stats_citation.py           # writes citation_flow_partners.csv, used by stats_connectivity.py
python stats_authorship.py
python stats_citation_dynamics.py    # self-citation, PageRank corrections, distribution fits, preferential attachment
python stats_authorship_dynamics.py  # Leiden, hierarchy, robustness, SIR spreading, growth (needs faculty_centrality.csv)
python stats_connectivity.py
python stats_citing_top.py
# second round
python stats_if_authors.py         # PRL list, Nature journals' IF, IF > 10 with < 10 authors, Q1 / IF / team-size grid
python stats_matrix_centrality.py  # Katz, HITS, communicability, dynamic communicability (needs faculty_centrality.csv)
python stats_hypergraph.py         # nonlinear hypergraph centrality (Tudisco & Higham 2021)
python stats_simplicial.py         # simplicial closure (Benson et al. 2018)
python stats_rosters.py            # yearly faculty lists (needs WebScrape/scripts/wayback_rosters.py output)
echo STATS-DONE
