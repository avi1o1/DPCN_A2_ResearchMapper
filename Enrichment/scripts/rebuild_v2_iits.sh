#!/bin/sh
# Offline rebuild of the 23 IIT enrichment outputs from the existing caches (no OpenAlex calls): merge -> faculty -> verify per
# institute (2 in parallel), then the combined export, networks and network checks.  Run after the WebScrape records changed
# (e.g. a finalize rerun) and nothing else is running (the network build needs ~10-12 GB).
set -e
R=$(cd "$(dirname "$0")/../.." && pwd)
export ENRICH_SCRAPE_DIR=$R/WebScrape/v2 ENRICH_OUT_DIR=$R/Enrichment/out_v2 ENRICH_CACHE_DIR=$R/Enrichment/cache_v2 PYTHONIOENCODING=utf-8
cd "$R/Enrichment/scripts"
KEYS=$(cd "$R/WebScrape/scripts" && python3 -c "from institutes import REG; print(' '.join(k for k in REG if k.startswith('iit_')))")
python3 test_rules.py > /dev/null && echo "rule tests passed"
echo $KEYS | tr ' ' '\n' | xargs -P 2 -I{} sh -c 'ENRICH_INSTS={} python3 merge.py {} && ENRICH_INSTS={} python3 faculty.py {} && ENRICH_INSTS={} python3 verify.py {} && echo "ENRICHED {}"'
ALL=$(echo $KEYS | tr ' ' ',')
ENRICH_INSTS=$ALL python3 export_csv.py
ENRICH_INSTS=$ALL python3 build_networks.py
ENRICH_INSTS=$ALL python3 verify_networks.py
echo REBUILD-IITS-DONE
