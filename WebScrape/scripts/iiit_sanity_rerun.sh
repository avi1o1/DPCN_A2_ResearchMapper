#!/bin/sh
# IIIT sanity-rule rerun (2026-11-01).  Run on the machine that holds the IIIT raw caches (WebScrape/raw/, Enrichment/cache_v2 with
# the IIIT OpenAlex caches, Enrichment/cache/scimago with all ten Scimago years).  No new discovery and no OpenAlex credits: it
# rebuilds the IIIT datasets from the caches with the current code (founding dates, start-year rule F1, namesake guard F5,
# sub-tier / mega flags, arXiv co-author cap), then redoes the offline enrichment rebuild.
#   usage: sh iiit_sanity_rerun.sh            (all 30)   |   sh iiit_sanity_rerun.sh iiit_pune iiit_surat
set -e
cd "$(dirname "$0")"
ROOT=$(cd ../.. && pwd)
IIITS=${*:-$(python3 -c "from institutes import REG; print(' '.join(k for k in REG if k.startswith('iiit')))")}
export RM_SANITY_RULES=all          # finalize.py: demotions F1/F5 are applied to the IIITs as well as the IITs
# 1. WebScrape: rebuild + OpenCitations fallback + finalize + recall + TODO sheet + cross-institute validation
sh run_v2.sh refresh $IIITS
# 2. Enrichment, offline (the ten-year Scimago files stay in use; rule: paper-year file, else the journal's latest year)
export ENRICH_SCRAPE_DIR=$ROOT/WebScrape/v2 ENRICH_CACHE_DIR=$ROOT/Enrichment/cache_v2 ENRICH_OUT_DIR=$ROOT/Enrichment/out_v2_iiit PYTHONIOENCODING=utf-8
export ENRICH_INSTS=$(echo $IIITS | tr " " ",")   # export_csv / build_networks / verify_networks read this
ls $ROOT/Enrichment/cache/scimago | wc -l | xargs echo "Scimago files found (expect 10):"
cd $ROOT/Enrichment/scripts
python3 test_rules.py > /dev/null && echo "enrichment rule tests passed"
python3 merge.py $IIITS
python3 faculty.py $IIITS
python3 verify.py $IIITS
python3 export_csv.py
python3 build_networks.py
python3 verify_networks.py || true      # one known open item (Jabalpur W4398769804), see PROCESS_IIIT.md 7.5
echo IIIT-SANITY-RERUN-DONE
