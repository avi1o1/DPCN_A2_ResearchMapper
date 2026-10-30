#!/bin/sh
# Dry run of the refresh path (build_candidates -> finalize) of ONE institute in a scratch folder: the old code (BASE_REF) and the
# current code are run on the same copied inputs, so the difference between the two outputs is exactly the effect of the rules.
# Nothing is written outside <scratch>; the live data (<live WebScrape dir>) is only read: the big read-only caches are symlinked.
#   usage: sh dry_run.sh <inst> <scratch_dir> <live_WebScrape_dir> [BASE_REF]       (BASE_REF default: v2-all-institutes)
#   then:  python3 compare_runs.py <scratch_dir> <inst> [<live_WebScrape_dir>]
# The network steps of `refresh` (doi_resolve.py, crossref_enrich.py, datacite_enrich.py, opencitations.py) are not run: their
# results are already in the live raw/ caches that finalize.py reads.
set -e
INST=$1; SCR=$2; LIVE=$3; BASE=${4:-v2-all-institutes}
[ -n "$INST" ] && [ -n "$SCR" ] && [ -d "$LIVE/raw" ] || { echo "usage: sh dry_run.sh <inst> <scratch_dir> <live_WebScrape_dir> [BASE_REF]"; exit 2; }
HERE=$(cd "$(dirname "$0")" && pwd)
REPO=$(cd "$HERE/../.." && pwd)
LIVE=$(cd "$LIVE" && pwd)
mkdir -p "$SCR"; SCR=$(cd "$SCR" && pwd)
for V in old new; do
  W=$SCR/$V/WebScrape
  rm -rf "$SCR/$V"; mkdir -p "$W/scripts" "$W/raw" "$W/logs" "$W/v2/logs" "$W/golden"
  if [ $V = old ]; then (cd "$REPO" && git archive "$BASE" WebScrape/scripts | tar -x -C "$SCR/old"); else cp "$HERE"/*.py "$HERE"/*.sh "$HERE"/*.tsv "$W/scripts/"; fi
  cp -r "$LIVE/rosters" "$W/rosters"                       # all rosters: the generic-name list is built from the whole family
  mkdir -p "$W/raw/roster"
  for D in crossref_aff crossref_full dblp doaj europepmc inspire landing opencitations s2 orcid; do [ -e "$LIVE/raw/$D" ] && ln -s "$LIVE/raw/$D" "$W/raw/$D" || true; done
  [ -e "$LIVE/raw/issn_lookup.json" ] && cp "$LIVE/raw/issn_lookup.json" "$W/raw/"
  for F in "$LIVE"/raw/roster/${INST}*.jsonl.gz; do cp "$F" "$W/raw/roster/"; done
  cp "$LIVE"/raw/doi_resolved*_$INST.tsv "$W/raw/" 2>/dev/null || true
  [ -d "$LIVE/affil_manual" ] && cp -r "$LIVE/affil_manual" "$W/affil_manual" || true
  (cd "$W/scripts" && RM_OUT=v2 python3 build_candidates.py "$INST" > /dev/null && RM_OUT=v2 python3 finalize.py "$INST" > "$W/v2/finalize_$INST.json")
  echo "$V done: $W/v2/$INST.json"
done
