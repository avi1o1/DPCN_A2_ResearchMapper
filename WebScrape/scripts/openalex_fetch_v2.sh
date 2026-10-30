#!/bin/bash
# OpenAlex works for every DOI of the v2 IIIT datasets (Enrichment stage A, online part only; offline steps not adapted yet).
# The wrapper points oa.DATA at WebScrape/v2 instead of the v1 folder; the shared Enrichment scripts are unchanged.
cd /c/Users/Arihant/Git/DPCN_A2_ResearchMapper/Enrichment/scripts
export PYTHONUTF8=1 PATH=~/.venvs/rm/Scripts:$PATH
export OPENALEX_API_KEY=$(grep '^OPENALEX_API_KEY=' ../../WebScrape/.env | cut -d= -f2)
run() { for i in "$@"; do python -c "
import sys, os, oa; oa.DATA = os.path.join(oa.REPO, 'WebScrape', 'v2'); sys.argv = ['stage_a_fetch.py', '$i']
exec(open('stage_a_fetch.py', encoding='utf-8').read())" > ../../WebScrape/logs/enrich_fetch_$i.log 2>&1; echo "$(date +%T) $i rc=$?"; done; }
run iiit_delhi iiit_allahabad iiit_bhubaneswar iiit_naya_raipur iiit_kota &
run iiit_jabalpur iiit_gwalior iiit_guwahati iiit_sri_city iiit_dharwad &
run iiit_bangalore iiit_kancheepuram iiit_pune iiit_kurnool iiit_lucknow iiit_vadodara &
wait
echo ENRICH-FETCH-DONE
