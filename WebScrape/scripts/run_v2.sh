#!/bin/sh
# v2 pipeline driver (PROCESS.md §15): every step writes to WebScrape/v2/ (RM_OUT=v2).
# usage: sh run_v2.sh merge|final|refresh [inst ...]       (default: every institute in institutes.py)
#   merge   : union -> DOI resolution -> Crossref/DataCite enrichment -> finalize -> recall (after the discovery harvests)
#   final   : strict roster pass -> merge -> loose roster pass -> arXiv pass -> merge -> OpenCitations -> finalize -> recall
#             -> TODO sheet (needs rosters/<inst>_faculty.csv)
#   refresh : rebuild from the caches after verify_*.py / resolve_todos.py, then cross-institute validation
# Sequential on purpose: shared caches must have a single writer.
set -e
cd "$(dirname "$0")"
export RM_OUT=v2
STAGE=$1; shift
INSTS=${*:-$(python3 -c "from institutes import ALL; print(' '.join(ALL))")}
python3 test_affil.py > /dev/null && echo "classifier rule tests passed"
post() {  # OpenCitations fallback, finalize, recall, TODO sheet
  python3 opencitations.py $1
  python3 finalize.py $1 > ../logs/finalize_v2_$1.json
  if [ -f ../golden/golden_$1.csv ]; then python3 eval_recall.py $1 > /dev/null; fi
  python3 export_todo.py $1
}
case $STAGE in
  merge)   for I in $INSTS; do sh run_merge.sh $I; done ;;
  final)   for I in $INSTS; do python3 roster_channels.py $I; sh run_merge.sh $I; done
           for I in $INSTS; do python3 roster_channels.py $I --loose; done
           for I in $INSTS; do python3 roster_channels.py $I --arxiv-only; done
           for I in $INSTS; do sh run_merge.sh $I; post $I; done ;;
  refresh) for I in $INSTS; do sh run_merge.sh $I; post $I; done
           python3 validate.py $INSTS ;;
  *) echo "unknown stage $STAGE"; exit 2 ;;
esac
echo "V2-$STAGE-DONE"
