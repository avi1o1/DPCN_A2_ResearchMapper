# Handoff: IIIT team (v2 pipeline, all-institutes run)

**For:** the teammate (and their Claude Code session) who will scrape the IIITs of the course brief (Groups 9–11).
**From:** the IIT team (Aviral Gupta), 2026-10-26. The IIT team runs all 23 IITs on its own machine at the same time.
**Repository:** this repo, branch `v2-all-institutes` (contains the v2 pipeline, the registry, the agent kit and this file).

This document is meant to be given to your Claude Code session as context, together with the files it links. Read all of
"Read first" before running anything: the procedure is strict on purpose, and every rule in it exists because something went
wrong without it.

---

## 1. Goal and standard

Collect *every* publication dated 2016-01-01 … 2026-12-31 of each assigned institution, with
`title, authors, year, type, venue, issn, doi, citations, references`, an evidence trail per record, and `TODO` for anything
that cannot be established. The professor's brief is `DPCN_Instruction_Note.pdf` (repo root); the course rule on sharing
between groups has been cleared with him.

The standard is **research-paper level**: more institutions must not mean a looser procedure. Concretely, for each institution:
* recall is measured against an **independent golden set** (built without the bibliographic APIs the pipeline uses);
* precision is measured by a **seeded, stratified manual audit** against the affiliation printed on the paper;
* every classifier decision is a **written rule with a test case**;
* every step, number, decision and incident is written into a **lab notebook** in the style of `WebScrape/PROCESS.md`.

## 2. Read first (in this order)

1. [`WebScrape/PROCESS.md`](../PROCESS.md) — the whole file. §§0–14 are the v1 method (3 IITs); **§15 is the v2 method you will
   run** (registry, classifier v2, token roles, the review procedure, the agent design, every incident so far). The notebook is
   the specification: if this handoff and PROCESS.md ever disagree, PROCESS.md wins and tell the IIT team.
2. [`WebScrape/RESULTS.md`](../RESULTS.md) and [`WebScrape/README.md`](../README.md) — what the outputs look like.
3. `WebScrape/scripts/institutes.py` (docstring: every registry field) and `WebScrape/scripts/affil.py` (docstring + the
   `_C` class comment: institution-type fields `mention`, `explicit_full`, `confusable`, `family`).
4. `WebScrape/scripts/test_affil_cases.tsv` — 63 real strings and the decisions taken on them; they teach the classifier's
   behaviour faster than the code does.
5. `WebScrape/agents/roster_brief.md`, `WebScrape/agents/golden_brief.md` — the sub-agent briefs, including the
   "Decisions already taken" sections learned on the pilots (IIT Palakkad, IIT Bombay).
6. Worked examples: `WebScrape/rosters/iit_palakkad_faculty.csv` + `rosters/notes/…`, `WebScrape/golden/golden_iit_palakkad.csv`
   + `golden/notes/…` (small institute), and the IIT Bombay pair (large institute).

## 3. Setup on your machine

```sh
git clone <repo-url> && cd ANLP_A2_ResearchMapper && git checkout v2-all-institutes && git checkout -b v2-iiit
python3 --version            # 3.10+; tested with 3.12
pip install requests         # the only third-party package the pipeline needs
sudo apt install poppler-utils   # pdftotext, used by golden-set agents for PDFs
export RM_MAILTO=<your e-mail>   # Crossref polite-pool / fetcher contact: use YOUR address, not the IIT team's
export RM_OUT=v2                 # every pipeline step writes to WebScrape/v2/ (run_v2.sh sets it for you)
python3 WebScrape/scripts/test_affil.py   # must print "63/63 cases pass" (more once you add yours)
```
* Disk: allow ~1 GB of caches per 10 institutions (`WebScrape/raw/`, git-ignored). Keep ≥ 10 GB free.
* Secrets: an OpenAlex key is only needed later for the Enrichment stage; it lives in `.env` (git-ignored). Never commit keys.
* Your machine has its own IP, hence its **own** Crossref concurrency allowance and ORCID daily quota — that is the point of
  running in parallel. Do not route requests through the IIT team's machine and vice versa.

## 4. Your institutions

| Institution (brief name) | suggested key | official name / notes to verify |
|---|---|---|
| IIIT Hyderabad | `iiit_hyderabad` | International Institute of Information Technology, Hyderabad (Gachibowli) |
| IIIT Delhi | `iiit_delhi` | Indraprastha Institute of Information Technology Delhi (Okhla Phase III) |
| IIIT Allahabad | `iiit_allahabad` | Indian Institute of Information Technology Allahabad (Jhalwa, Prayagraj) |
| IIIT Bangalore | `iiit_bangalore` | International Institute of Information Technology Bangalore (Electronic City) |
| IIIT Gwalior | `iiit_gwalior` | ABV-Indian Institute of Information Technology and Management Gwalior (ABV-IIITM) |
| IIIT Jabalpur | `iiit_jabalpur` | PDPM Indian Institute of Information Technology, Design and Manufacturing Jabalpur |
| IIIT Pune | `iiit_pune` | Indian Institute of Information Technology Pune (transit campus; check its history) |
| IIIT Kancheepuram | `iiit_kancheepuram` | IIITDM Kancheepuram (Indian Institute of Information Technology Design and Manufacturing), Chennai |

Registry keys use the prefix shown (`iiit_…`). Confirm each ROR id yourself (`https://api.ror.org/v2/organizations?affiliation=<name>`,
take the `chosen: true` record) and record ROR quirks — the IIT run found wrong aliases in ROR (e.g. "AIIMS Jodhpur" as an alias
of IIT Jodhpur), so **never use ROR aliases as match strings**.

## 5. Procedure (one institution = all steps; record everything in your notebook)

### 5.1 Reconnaissance (PROCESS.md §1, §15.2)
* ROR record, official names, old names, campuses (current, temporary/transit, extension, offshore), the PIN codes and
  localities of every campus, the e-mail domain.
* Crossref hit counts per candidate token (`query.affiliation=<token>`, `filter=from-pub-date:2016-01-01,until-pub-date:2026-12-31`,
  `rows=0`): city, PINs, localities, old campuses, spelling variants, abbreviations. Facts learned: Crossref tokenises on dots
  (e-mail-domain queries are useless: ~3,500 hits of `ac`/`in`), multi-word queries are OR-searches (use single rare tokens).
* INSPIRE-HEP institution record(s) (`https://inspirehep.net/api/institutions?q="<name>"`); some institutes have two.

### 5.2 Registry entries (no edits to shared files)
Create **`WebScrape/scripts/institutes_iiit.py`** with `EXT = {key: dict(...)}`. `institutes.py` merges it automatically and refuses
duplicate keys. Fields: see the `institutes.py` docstring; template:

```python
EXT = {
    "iiit_hyderabad": dict(
        name="International Institute of Information Technology Hyderabad", ror="https://ror.org/…", grid="grid.…",
        family="iiit",                 # institutes of one family are compared for "another institute is named"
        mention=r"inter?national\s+institute\s+of\s+information\s+technology|indian\s+institute\s+of\s+information\s+technology|\biiit",      # how this TYPE of institution is named (replaces "Indian Institute of Technology")
        explicit_full=r"inter?national\s+institute\s+of\s+information\s+technology,?\s*\(?\s*(iiit\s*-?\s*h\)?\s*,?\s*)?hyderabad|\biiit\s*-?\s*h(yderabad)?\b",   # naming THIS institution explicitly (decisive)
        confusable=r"indian\s+institute\s+of\s+technology\b|\biit\b",    # look-alike names of other organisations
        crossref=[...], crossref_broad=[...],  # sweep tokens (single rare tokens) / state tokens if a state rule applies
        anchor=r"…",   # campus-unique tokens only (PIN/locality/e-mail domain) — the department rule relies on them
        city=r"…",     # in-scope tokens shared with a few organisations (no mention -> 'uncertain')
        shared=r"…",   # big-city tokens (no mention -> not about this institute at all)
        units=r"…",    # names that exist only at this institute (count without a city)
        state=None,    # a state rule only if it is the only institute of its family in the state
        other=r"…",    # organisations sharing its tokens (grows during the review)
        europepmc="…", doaj=[...], inspire=None, orcid_q="…", orcid_city=r"…", dblp=("…", r"…"),
        tenure_lag=1),
}
```
Write channel queries the way §15.2 describes: campus tokens alone, shared/noisy tokens only together with the institution's
name, plus name phrases (`AFF:"…"` in Europe PMC, `bibjson.author.affiliation:"…"` fragments in DOAJ, `affiliation-org-name:"…"`
and `ror-org-id:"…"` in ORCID).

### 5.3 Discovery harvest (PROCESS.md §4)
From `WebScrape/scripts/` (each command resumes / skips finished work where noted):
```sh
python3 crossref_aff.py <token> --light            # every crossref + crossref_broad token (≤ 3 concurrent overall)
python3 europepmc_aff.py <key>; python3 doaj_aff.py <key>; python3 inspire_aff.py <key>; python3 dblp_people.py <key>
python3 orcid_people.py <key>                      # checkpointed; see §7 on the daily quota
```
`common.get` already limits Crossref to 3 concurrent requests across all your processes; DOAJ/Europe PMC/INSPIRE/DBLP/ORCID can
run in parallel with each other (one queue per service). `WebScrape/raw/run_sweeps.sh`, `run_channels.sh`, `run_orcid.sh` are the
IIT team's queue runners — copy them with your institute list.

### 5.4 Classifier review (PROCESS.md §3.2, §15.4) — the step that decides precision
```sh
python3 review_strings.py <key> <review_dir>     # writes <key>_{uncertain,other,iit,iitnone,iitnoname}.tsv
```
(`iit` in the file names means "classified as this institute".) Read **all** `uncertain` strings, **all** `iitnoname` strings
(classified as the institute without naming it: department rule / unit names — this is where the false positives were),
all `iitnone` strings, the top `other` strings and a random `iit` sample. Then adjust the registry entry, re-run, repeat.
Lessons from the 20 new IITs that will apply to you too:
* **A campus PIN or locality is rarely unique.** Cancer Institute (WIA) shares IIT Madras's 600036, NIPER Ahmedabad shares IIT
  Gandhinagar's Palaj 382355, IISER Tirupati shares IIT Tirupati's 517619, hospitals share Bihta / North Guwahati. Only
  verified campus-unique tokens may be `anchor`.
* Addresses abroad and Chinese postcodes collide with PINs (110016 = Shenyang, 221005 = Xuzhou); e-mail addresses are not
  affiliation evidence; abbreviations collide (IITD matched "IIITD&M" and a Nigerian institute).
* Every decision becomes a line in **`WebScrape/scripts/test_affil_cases_iiit.tsv`** (same columns as `test_affil_cases.tsv`);
  `test_affil.py` runs all teams' files. Never change an existing IIT test; if your rule needs one changed, tell the IIT team.
* IIIT-specific: see §6 for the identity traps to test first.

### 5.5 Rosters and golden sets (sub-agents; PROCESS.md §6, §7, §15.3)
1. Add your institutes to **`WebScrape/agents/iiits.json`** (same shape as `agents/iits.json`: `NAME`, `CAMPUS_HINT`,
   `SPECIAL`, `TARGET`, `AUTHCOL`). `SPECIAL` carries institute-specific rules (mentor institutes, look-alike neighbours, what
   counts as "faculty" — see §6).
2. `python3 WebScrape/agents/fill.py <work_dir_outside_repo> <key> …` writes one roster and one golden brief per institute to
   `WebScrape/agents/briefs/` (git-ignored).
3. Launch one Claude Code sub-agent per brief (general-purpose), with this prompt:
   > Build the faculty roster of <NAME> (2016–2026) for a research-grade bibliometric dataset. Your complete brief — scope,
   > decisions already taken, exact output format and paths, allowed sources, and non-negotiable conduct rules (all fetching
   > through a shared rate-limited fetcher; no bot-wall bypass; no git writes) — is in this file; read it fully first and follow
   > it exactly: `<path to filled brief>`. The finished rosters in WebScrape/rosters/ (IIT Palakkad, IIT Bombay) and their notes
   > are worked examples. If an instruction proves impossible or ambiguous, do the most rigorous reasonable thing and list it
   > under "Brief issues" in your final reply.

   (golden set: same with "Build an independent golden set (recall benchmark) of <NAME> publications 2016–2026 …".)
4. **About four agents at a time.** Four agents plus the main session exhaust a session's usage limit in about 1–2 hours;
   when an agent stops with a rate-limit error, resume it with a message after the reset (its work is saved) instead of
   starting a new one.
5. Accept an output only after `python3 WebScrape/agents/check_outputs.py <key>` passes **and** you have read its notes and its
   "Brief issues". Fix brief problems in your copy of the brief before the next wave, and record them in your notebook.
6. Golden sets must stay independent: never let a golden agent read pipeline output for its institute.

### 5.6 Pipeline run (PROCESS.md §5, §8–§12; `WebScrape/scripts/run_v2.sh`)
```sh
sh run_v2.sh merge <keys…>     # first pass: union -> DOI resolution -> enrichment -> finalize (works without rosters)
sh run_v2.sh final <keys…>     # after rosters exist: strict roster pass, loose pass, arXiv pass, merge, OpenCitations, recall
python3 verify_epmc.py <key>; python3 verify_springer.py <key>; python3 resolve_todos.py <key>   # verification + TODO resolution
sh run_v2.sh refresh <keys…>   # rebuild from caches + cross-institute validation (validate.py)
```
Always pass your keys explicitly (the defaults are "every registered institute"). Outputs: `WebScrape/v2/<key>.json`, **one JSON
per institution** (`{summary, records[]}`, one record per line). Then:
* recall: `python3 eval_recall.py <key>` (needs `golden/golden_<key>.csv`), reported like RESULTS.md (all / with DOI / by source);
* precision: `python3 precision_sample.py <key>` (seed 20261007) and a separate audit agent filling
  `golden/precision_audit_<key>.csv` against the affiliation printed on the paper (format: the existing audit files);
* validation report (`validate.py`): 0 violations required.

## 6. IIIT-specific notes (verify each on your own strings)

* **Institution type.** Set `family="iiit"` and a `mention` regex for "International / Indian Institute of Information
  Technology" and "IIIT"; the default `mention` is the IIT pattern, which never matches an IIIT (by design: the IIT entries list
  IIITs among their `other` organisations). Set `confusable` to the IIT name pattern so that "IIT …" strings never count.
* **Many IIITs are not in your list** (IIIT Lucknow, Kota, Vadodara, Sri City, Guwahati, Kalyani, Bhagalpur, Agartala,
  Bhubaneswar, Naya Raipur, Dharwad, Una, Sonepat …). The "another institute named" check only knows registered institutes, so
  put the unregistered ones into each entry's `confusable`/`other` (e.g. `iiit\s*-?\s*(lucknow|kota|vadodara|…)`).
* **Abbreviation collisions to test:** IIIT-H vs IIIT-Hyderabad-only; IIITD vs IIITDM / IIIT-D&M; IIIT-B (Bangalore) vs IIIT
  Bhubaneswar / Bhagalpur; IIITA (Allahabad) vs IIIT Agartala; IIITM (Gwalior) vs IITM (IIT Madras / Tropical Meteorology Pune);
  ABV-IIITM vs "IIIT" alone. The IIT run's rule: short abbreviations count alone only when nothing else is named in the part.
* **Shared campuses / PINs to check before declaring an anchor:** Gachibowli (University of Hyderabad, ISB, many companies);
  Okhla Phase III, Delhi (industrial estate); Electronic City, Bangalore (Infosys and other firms); Melakottaiyur / 600127,
  Chennai (VIT Chennai is nearby); Jhalwa / Prayagraj; Dumna Airport Road, Jabalpur. IIITDM Kancheepuram is not IIT Madras,
  although early papers were mentored there — the IIT Madras entry treats "IIITD&M Kancheepuram" as another organisation.
* **IIIT Delhi** is "Indraprastha Institute of Information Technology" (a state university): its strings rarely say "Indian
  Institute of Information Technology". IIIT Hyderabad and IIIT Bangalore are "International …".
* **Rosters:** research centres with research scientists and many adjunct/visiting faculty (IIIT-H); PPP IIITs list "faculty on
  contract". The IIT rule applies: visiting/adjunct people contribute only papers that print the IIIT affiliation (§15.6).
* **Publication profile:** computer-science heavy → conference papers dominate; DBLP (person channel) and arXiv matter more than
  for IITs; ACM/IEEE deposit affiliations to Crossref reasonably well, Springer LNCS does not (person channels needed).
* **Suggested order:** a clearly identifiable one first (IIITDM Jabalpur or ABV-IIITM Gwalior) to calibrate the tooling, then
  the others; IIIT Hyderabad and IIIT Delhi last (big cities, many look-alikes).

## 7. Conduct rules and known pitfalls (all learned the hard way — PROCESS.md §10, §15)

* **Never bypass bot protection** (Cloudflare, CAPTCHAs, 403 challenges); use Wayback copies and record it. All agent fetches go
  through `WebScrape/agents/polite_get.py` (per-host gaps across processes: Wayback 3 s, arXiv 5 s by operator decision — robots.txt
  asks 15 s — with an automatic stop on a 403 from arXiv; others 1 s; DNS/TLS failures reported as `DEAD:`).
* IRINS, Scopus, Google Scholar scraping and keyed APIs are not used for discovery. OpenAlex stays out of discovery so the
  method is identical across institutes (it is used later, in Enrichment).
* **ORCID public API**: a daily quota per IP (~60,000 record fetches exhausted it); after that every call is HTTP 429 for many
  hours. Plan the ORCID harvest and the roster agents' ORCID lookups within one quota, or register for free public-API
  credentials. Searches page through at most 10,000 hits (handled: `orcid_people.py` partitions by family-name initial).
* **Crossref**: polite pool = 3 concurrent requests (enforced in `common.get`); include your `RM_MAILTO`.
* **Hangs**: a machine suspend left HTTP calls hung for hours (twice). Run long jobs under a watchdog (`timeout 2h …` with retries,
  as in `raw/run_orcid.sh`); the ORCID and Crossref caches resume.
* **DataCite** outages: handled (a failed DOI is retried next run, never cached as missing).
* `pkill -f <pattern>` matches its own shell — use `pgrep -f "^python3 …"` and kill by PID.
* Shell heredocs: use `<<'EOF'` (quoted) when the text contains backticks or `$` — an unquoted heredoc silently ran the
  backticked words of a brief as commands.
* Raw caches have a single writer: do not run two pipeline stages for the same institute at once.

## 8. What not to change, and how to hand back

* Do **not** edit `institutes.py`, `affil.py`, the IIT tests, `agents/iits.json`, the IIT rosters/golden sets or PROCESS.md.
  Your changes go into your own files: `scripts/institutes_iiit.py`, `scripts/test_affil_cases_iiit.tsv`, `agents/iiits.json`,
  `rosters/…`, `golden/…`, and your notebook **`WebScrape/PROCESS_IIIT.md`** (same structure as PROCESS.md §15: decisions,
  token-role table, review findings, incidents, numbers).
* If a shared script needs a change (a bug, or a new feature your institution type needs), make it on your branch in a separate
  commit, state why in the commit message, and tell the IIT team — they re-run the IIT regression (`test_affil.py` plus the v1
  string regression) before merging. Changes must keep IIT behaviour identical.
* Commit to `v2-iiit`: your registry/test/settings files, rosters + notes, golden sets + notes, precision audits, the notebook,
  and the final `WebScrape/v2/<key>.json` files. Never commit `WebScrape/raw/`, `logs/`, `.env`, `agents/.runtime/`.
* When an institution is finished, report: records (verified / likely / unconfirmed), recall (all / with DOI), precision per tier,
  validation result, and the open problems.

## 9. Status of the IIT run (for orientation; 2026-10-26)

* Code: registry + classifier v2 + agent kit done; 63 rule tests; v1→v2 regression read string by string (§15.1, §15.4).
* Harvest: Crossref sweeps, Europe PMC, DOAJ, INSPIRE, DBLP done for 23 IITs; ORCID for 16 (quota-limited).
* First pass `merge` done for all 23 (e.g. IIT Delhi 27,905 records, IIT Goa 665 — without person/verification channels).
* Rosters done: Palakkad, Tirupati, Bombay; golden sets done: Palakkad, Tirupati, Bombay; more running.
* Contact the IIT team for anything unclear before improvising; the notebook is the shared source of truth.
