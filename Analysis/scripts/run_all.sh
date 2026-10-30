#!/bin/sh
# Re-run every statistic (tables -> results, charts -> figures) from the Enrichment output.
#   sh run_all.sh                                  Kharagpur + Roorkee from ../Enrichment/out -> results/ (as before)
#   ANALYSIS_PROFILE=v2 ANALYSIS_IN_DIR=/path/to/Enrichment/out_v2 sh run_all.sh
#                                                  the 14 newer IITs -> results_v2/, figures_v2/, cache_v2/, offline
# The institutes, folders and online/offline mode come from environment variables; they are listed in common.py.
# Offline mode (default under ANALYSIS_PROFILE=v2, or ANALYSIS_OFFLINE=1) never calls OpenAlex: the steps that need it
# are skipped and written to <results>/skipped_panels.csv. Re-run after the enrichment files are refreshed: every step
# reads its inputs again and overwrites its own outputs (nothing is appended).
# Online steps, cached in the cache folder after the first run (set OPENALEX_API_KEY or OPENALEX_KEY_FILE for new data):
#   fetch_openalex_extra.py  yearly citation counts, journal IF, faculty OpenAlex profiles (~200-600 credits)
#   stats_connectivity.py    topic profiles of new partners (1 credit each)
#   stats_citing_top.py      citation counts of citing works (~1,410 requests, no key needed)
# ANALYSIS_KEEP_GOING=1 carries on after a failing script and lists the failures at the end (default: stop at the first).
# Each script's wall time (and peak memory when /usr/bin/time exists) is appended to <results>/run_times.csv.
cd "$(dirname "$0")"
export PYTHONIOENCODING=utf-8
export PYTHONHASHSEED=${PYTHONHASHSEED:-0}   # ties in a few rankings follow set order: a fixed seed makes the run repeatable
PY=${PYTHON:-python}
RESDIR=$($PY -c "import common; print(common.RES)") || exit 1
OFFLINE=$($PY -c "import common; print(int(common.OFFLINE))")
mkdir -p "$RESDIR"
rm -f "$RESDIR/skipped_panels.csv"          # rebuilt by this run
echo "script,exit_code,seconds,peak_memory_mb" > "$RESDIR/run_times.csv"
FAILED=""

run() {
  s="$1"; t0=$(date +%s)
  if [ -x /usr/bin/time ]; then
    /usr/bin/time -f "%M" -o "$RESDIR/.mem" $PY "$s"; rc=$?
    mem=$(( $(cat "$RESDIR/.mem" | tail -1) / 1024 ))
  else
    $PY "$s"; rc=$?; mem=""
  fi
  echo "$s,$rc,$(( $(date +%s) - t0 )),$mem" >> "$RESDIR/run_times.csv"
  if [ $rc -ne 0 ]; then
    echo "FAILED: $s (exit $rc)"
    FAILED="$FAILED $s"
    [ -z "$ANALYSIS_KEEP_GOING" ] && exit $rc
  fi
}

if [ "$OFFLINE" = "1" ]; then echo "offline: fetch_openalex_extra.py not run"; else run fetch_openalex_extra.py; fi   # only fetches ids missing from the cache
run stats_bibliometric.py       # writes faculty.csv, used by the next three
run stats_faculty.py
run stats_faculty_cohort.py     # seniority-controlled cohort (current, joined by 2017) and roster completeness against NIRF; warns if the cohort is < 20
run stats_journals.py
run stats_large_collab.py       # papers with more than 10 authors: effect on the headline numbers, where they are
run stats_mega_collab.py        # papers with more than 100 authors: every per-institute statistic with and without them, rank changes
run stats_areas.py
run stats_citation.py           # writes citation_flow_partners.csv, used by stats_connectivity.py
run stats_authorship.py
run stats_citation_dynamics.py    # self-citation, PageRank corrections, distribution fits, preferential attachment
run stats_authorship_dynamics.py  # Leiden, hierarchy, robustness, SIR spreading, growth (needs faculty_centrality.csv)
run stats_connectivity.py
run stats_citing_top.py
# second round
run stats_if_authors.py         # PRL list, Nature journals' IF, IF > 10 with < 10 authors, Q1 / IF / team-size grid
run stats_matrix_centrality.py  # Katz, HITS, communicability, dynamic communicability (needs faculty_centrality.csv)
run stats_hypergraph.py         # nonlinear hypergraph centrality (Tudisco & Higham 2021)
run stats_simplicial.py         # simplicial closure (Benson et al. 2018)
run stats_coauthor_citation.py  # citing co-authors, citing vs collaborating over time, inwardness (needs faculty.csv)
run stats_bowtie.py             # bow-tie of the faculty citation network, department hierarchy (SpringRank)
run stats_cross_dept.py         # cross-department teams vs FWCI (needs oa_fwci.json)
run stats_dept_areas.py         # department strengths, relatedness prediction, fitness-complexity
run stats_rosters.py            # yearly faculty lists (needs WebScrape/scripts/wayback_rosters.py output)
rm -f "$RESDIR/.mem"
if [ -n "$FAILED" ]; then echo "STATS-DONE with failures:$FAILED"; exit 1; fi
echo STATS-DONE
