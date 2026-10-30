#!/bin/sh
# v2 pipeline driver (PROCESS.md §15): every step writes to WebScrape/v2/ (RM_OUT=v2).
# usage: sh run_v2.sh <stage> [inst ...]       (default: every institute in institutes.py)
#   merge    : union -> DOI resolution -> Crossref/DataCite enrichment -> finalize -> recall   (works without a roster)
#   roster   : strict roster pass (Crossref author search, roster ORCID works, DBLP) -> merge        [Crossref queue]
#   arxiv    : arXiv author pass (5 s per person, a separate host -> may run in parallel with `roster` of other institutes)
#   verify   : Europe PMC DOI verification, Springer landing-page verification, TODO resolution   [slow, 3 workers/1 req/s]
#   refresh  : merge -> OpenCitations fallback -> finalize -> recall -> TODO sheet; then cross-institute validation
#   loose    : OPTIONAL loose roster pass (feeds only the unconfirmed-candidates file, a diagnostic outside the dataset);
#              off by default since 2026-10-27 (it doubles the Crossref time; PROCESS.md §15.7)
# Typical order per institute: roster -> arxiv -> verify -> refresh.  Sequential per queue on purpose:
# shared caches must have a single writer per institute.
set -e
cd "$(dirname "$0")"
export RM_OUT=v2
STAGE=$1; shift
INSTS=${*:-$(python3 -c "from institutes import ALL; print(' '.join(ALL))")}
python3 test_affil.py > /dev/null && echo "classifier rule tests passed"
python3 test_sanity_rules.py > /dev/null && echo "sanity rule tests passed (start year, untimed tier, mega flag, namesake guard)"
post() {  # OpenCitations fallback, finalize, recall, TODO sheet
  python3 opencitations.py $1
  python3 finalize.py $1 > ../logs/finalize_v2_$1.json
  if [ -f ../golden/golden_$1.csv ]; then python3 eval_recall.py $1 > /dev/null; fi
  python3 export_todo.py $1
}
case $STAGE in
  merge)   for I in $INSTS; do sh run_merge.sh $I; done ;;
  roster)  for I in $INSTS; do python3 roster_channels.py $I; sh run_merge.sh $I; done ;;
  loose)   for I in $INSTS; do python3 roster_channels.py $I --loose; done ;;
  arxiv)   for I in $INSTS; do python3 roster_channels.py $I --arxiv-only; done ;;
  verify)  for I in $INSTS; do python3 verify_epmc.py $I; python3 verify_springer.py $I; python3 resolve_todos.py $I; done ;;
  refresh) for I in $INSTS; do sh run_merge.sh $I; post $I; done
           python3 validate.py $INSTS ;;
  *) echo "unknown stage $STAGE"; exit 2 ;;
esac
echo "V2-$STAGE-DONE"
