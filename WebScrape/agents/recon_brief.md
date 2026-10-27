# Task: reconnaissance and draft registry entries for {LABS}

You are drafting the institute-registry entries of the other-institutes team (operator Varun Shastry; DPCN course project,
IIIT Hyderabad) for a research-grade bibliometric dataset. Your drafts are **proposals**: the operator reviews, tests and
merges them. Precision matters more than speed — every rule must rest on real affiliation strings you saw.

## Read first
1. `C:\Users\varun\rm_v2\WebScrape\handoff\HANDOFF_other_institutes.md` §5.1, §5.2, §6 (your institution type's notes).
2. `C:\Users\varun\rm_v2\WebScrape\PROCESS_OTHER.md` §2 — the pilot (CSIR-CECRI): how tokens got their roles, what went
   wrong (AcSIR's Taramani address, the Italian "CECRI" acronym) and how it was fixed.
3. `C:\Users\varun\rm_v2\WebScrape\scripts\institutes_other.py` — the CECRI entry is your template (every field, `CSIR_MENTION`,
   `CSIR_OTHER_LAB`, `CECRI_NAME` pattern for acronyms, `exclude`, `other` + `GENERIC_OTHER`). `institutes.py` docstring and
   `affil.py` (the `_C` class and `_unit`) define what each field does.
4. `C:\Users\varun\rm_v2\WebScrape\scripts\test_affil_cases_other.tsv` — test-case format.

## For each institution
1. **ROR** (`https://api.ror.org/v2/organizations?affiliation=<name>`, the `chosen: true` record; then the record itself for the
   GRID id). Several campuses/units → list them. Never use ROR aliases as match strings.
2. **INSPIRE** institution records (`https://inspirehep.net/api/institutions?q=<name>`): legacy names, or none.
3. **Crossref token probes**: `python3 recon_probe.py <key> <token> [<token> ...] --sample 12` (run from
   `C:\Users\varun\rm_v2\WebScrape\scripts`). Probe the lab name's distinctive words, its acronym, the city/town, every campus
   PIN and locality, old names, spelling variants. Single rare tokens only (Crossref ORs multi-word queries). Read the sample
   strings: who else prints this token?
4. **Decide token roles** exactly as the pilot did: sweep tokens (`crossref`); `anchor` only for tokens verified unique to the
   campus (rare — leave None if unsure); `city` for small shared places; `shared` only when a type mention is reliable there;
   the name (typo-tolerant) and a context-restricted acronym in `explicit_full` and `units`; organisations sharing the place in
   `exclude` (if they could carry a CSIR/DAE mention) or `other`; `confusable` = `CSIR_OTHER_LAB.format(me=<this lab's
   name/acronym alternatives>)` for CSIR labs. Check every acronym for collisions (other countries, other fields) in the probe
   strings and with a probe of the acronym alone.
5. **Test cases** from the real strings you saw: at least 8 per lab — the lab named, typo/variant forms, each look-alike
   organisation, AcSIR/HBNI alone, an acronym collision if any.

## Output (do NOT edit any file in the repository; write only under C:\Users\varun\rm_v2_work\registry_drafts\)
* `<key>.py`: one Python dict literal per lab, `"<key>": dict(...)`, all fields of the CECRI entry (you may reference the names
  `CSIR_MENTION`, `CSIR_OTHER_LAB`, `GENERIC_OTHER` that exist in institutes_other.py); comments state the evidence for each rule.
* `<key>_tests.tsv`: rows `inst<TAB>expected<TAB>string<TAB>reason` (expected = iit | other | uncertain | None; `iit` means "this
  institution"); strings copied exactly from the probe output, never made up.
* `<key>_recon.md`: ROR/GRID/INSPIRE findings, the token table (token, hits, who prints it, role) with the probe counts, campus
  list, decisions and open questions.

## Conduct
* Every shell command starts with `. /c/Users/varun/rm_v2_env.sh && ` (project Python, contact e-mail). Crossref concurrency is
  limited machine-wide by the scripts: be patient, never loop probes in parallel.
* Use only real strings from the APIs; if something cannot be established, say so in the recon notes.
* No git commands that change state, no edits to repository files, no harvests (the operator runs them).

## Final reply
≤ 15 lines per lab group: per lab the ROR id, sweep tokens with hit counts, the main look-alikes, acronym collisions found, open
questions.
