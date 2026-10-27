#!/bin/sh
# Discovery harvest queue of the other-institutes team (HANDOFF_other_institutes.md §5.3), replacing the IIT team's
# git-ignored raw/run_*.sh runners. Per institute key: every Crossref sweep token (light, 3 at a time; common.get also caps
# Crossref at 3 concurrent requests across processes), and Europe PMC, DOAJ, INSPIRE, DBLP and ORCID in parallel (one
# process per service). Each job runs under a watchdog (timeout 2h: a hung HTTP call after a machine suspend is the known
# failure, PROCESS.md §10); ORCID is retried up to 5 times because it resumes from its checkpoint.
# Progress: logs/harvest_other.log (START / DONE / FAIL with exit code); job output in logs/harvest_other_<job>.out
# usage: [CHANNELS="crossref europepmc doaj inspire dblp orcid"] sh run_harvest_other.sh <inst> [<inst> ...]
cd "$(dirname "$0")"
LOG=../logs/harvest_other.log
CHANNELS=${CHANNELS:-"crossref europepmc doaj inspire dblp orcid"}
mkdir -p ../logs
job() {  # job <name> <cmd...>
  name=$1; shift
  echo "$(date '+%F %T') START $name" >> $LOG
  timeout 2h "$@" >> "../logs/harvest_other_$(echo "$name" | tr ' /' '__').out" 2>&1
  rc=$?
  if [ $rc -eq 0 ]; then echo "$(date '+%F %T') DONE $name" >> $LOG; else echo "$(date '+%F %T') FAIL $name (exit $rc)" >> $LOG; fi
  return $rc
}
on() { case " $CHANNELS " in *" $1 "*) return 0;; *) return 1;; esac; }
for I in "$@"; do
  # tr -d '\r': on Windows Python writes CRLF, and a token ending in \r makes an invalid cache file name
  python3 -c "from institutes import REG; print('\n'.join(REG['$I']['crossref'] + REG['$I']['crossref_broad']))" | tr -d '\r' > ../logs/tokens_$I.txt
  if on crossref; then
    ( while read -r T; do
        [ -n "$T" ] || continue
        job "crossref $T" python3 crossref_aff.py "$T" --light &
        while [ "$(jobs -r | wc -l)" -ge 3 ]; do sleep 2; done
      done < ../logs/tokens_$I.txt; wait ) &
  fi
  on europepmc && job "europepmc $I" python3 europepmc_aff.py $I &
  on doaj && job "doaj $I" python3 doaj_aff.py $I &
  on inspire && job "inspire $I" python3 inspire_aff.py $I &
  on dblp && job "dblp $I" python3 dblp_people.py $I &
  on orcid && ( for k in 1 2 3 4 5; do job "orcid $I try$k" python3 orcid_people.py $I && break; done ) &
  wait
  echo "$(date '+%F %T') HARVEST-DONE $I ($CHANNELS)" >> $LOG
done
