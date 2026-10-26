# Handoff: Other-institutes team (NITs, universities, IISc/TIFR/IISERs, premier institutes, CSIR, DAE)

**For:** the teammate (and their Claude Code session) who will scrape all non-IIT, non-IIIT institutions of the course brief (Groups 12–30).
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
git clone <repo-url> && cd ANLP_A2_ResearchMapper && git checkout v2-all-institutes && git checkout -b v2-other
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

| Group (brief) | Institutions | suggested key prefix / `family` |
|---|---|---|
| NITs (12–15) | NIT Trichy, NITK Surathkal, NIT Warangal, NIT Rourkela, NIT Calicut, NIT Kurukshetra, NIT Durgapur, MANIT Bhopal, NIT Jamshedpur, NIT Silchar | `nit_…` / `nit` |
| Central universities (16–17) | JNU, University of Hyderabad, University of Delhi, BHU, Jadavpur University, Jamia Millia Islamia | `univ_…` / `univ` |
| IISc · TIFR · IISERs (18–20) | IISc, TIFR Mumbai, IISER Pune, Kolkata, Bhopal, Mohali, Thiruvananthapuram | `iisc`, `tifr`, `iiser_…` / `iisc_iiser` |
| Premier science institutes (21–23) | ISI (all campuses), IMSc, CMI, HRI, NCBS, S. N. Bose Centre, Bose Institute, SINP | `isi`, `imsc`, … / `premier` |
| CSIR chemistry & physics (24–26) | NCL, IICT, CECRI, CFTRI, NIIST, NML, NPL, CSIO, CGCRI | `csir_…` / `csir` |
| CSIR engineering (27–28) | CMERI, CRRI, CIMFR, CBRI, CEERI, SERC, AMPRI, CDRI | `csir_…` / `csir` |
| CSIR biology · DAE (29–30) | CCMB, IGIB, IMTECH; BARC, IGCAR, RRCAT, NISER | `csir_…` / `csir`; `dae_…` / `dae` |

About 55 institutions: plan waves by type (one type's look-alikes are reviewed together). Suggested order: CSIR and DAE labs
(clear names, small rosters) → NITs → IISERs/IISc/TIFR → premier institutes → the large universities last.

Registry keys use the prefix shown (`<type>_…`). Confirm each ROR id yourself (`https://api.ror.org/v2/organizations?affiliation=<name>`,
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
Create **`WebScrape/scripts/institutes_other.py`** with `EXT = {key: dict(...)}`. `institutes.py` merges it automatically and refuses
duplicate keys. Fields: see the `institutes.py` docstring; template:

```python
EXT = {
    "nit_trichy": dict(
        name="National Institute of Technology Tiruchirappalli", ror="https://ror.org/…", grid="grid.…",
        family="nit",                 # institutes of one family are compared for "another institute is named"
        mention=r"national\s+institute\s+of\s+technology|\bnit\b|regional\s+engineering\s+college",      # how this TYPE of institution is named (replaces "Indian Institute of Technology")
        explicit_full=r"(national\s+institute\s+of\s+technology|\bnit)\s*,?\s*-?\s*\(?\s*(tiruchirappalli|trichy|tiruchirapalli)\b",   # naming THIS institution explicitly (decisive)
        confusable=r"indian\s+institute\s+of\s+technology\b|\biit\b|institute\s+of\s+information\s+technology",    # look-alike names of other organisations
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
* Every decision becomes a line in **`WebScrape/scripts/test_affil_cases_other.tsv`** (same columns as `test_affil_cases.tsv`);
  `test_affil.py` runs all teams' files. Never change an existing IIT test; if your rule needs one changed, tell the IIT team.
* Per-type identity traps: §6. Review institutions that share a city together (Kolkata: SINP, S. N. Bose, Bose Institute,
  ISI, IISER Kolkata, Jadavpur, CGCRI; Hyderabad: UoH, IICT, CCMB; Delhi: JNU, DU, Jamia, NPL, CRRI, IGIB; Chennai: IMSc, CMI,
  SERC; Bangalore: IISc, NCBS, ISI Bangalore; Pune: NCL, IISER Pune; Chandigarh/Mohali: CSIO, IMTECH, IISER Mohali).

### 5.5 Rosters and golden sets (sub-agents; PROCESS.md §6, §7, §15.3)
1. Add your institutes to **`WebScrape/agents/others.json`** (same shape as `agents/iits.json`: `NAME`, `CAMPUS_HINT`,
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

## 6. Notes per institution type (verify each on your own strings)

**General**
* Set `family`, `mention`, `explicit_full` and `confusable` for every entry (§5.2). Within a family the "another institute
  named" check compares registered institutes only; unregistered look-alikes (the other ~20 NITs, other IISERs, other CSIR labs)
  go into `confusable`/`other`.
* **Consistency with the IIT entries:** many of your institutions already appear in IIT entries' `other` lists (e.g. CSIR-CBRI
  and NIH in Roorkee, CIMFR in Dhanbad, NISER at Jatni, IISER Tirupati, RRCAT and UGC-DAE in Indore, ARCI and IMSc in Chennai,
  NIPER, ISI Delhi at 110016). Your entries must reach the mirror decision on the same strings (e.g. "IIT Kharagpur | National
  Institute of Hydrology, Roorkee" is *other* for IIT Roorkee and should be an NIH paper only if NIH were in scope).
  Add such strings to your test file as cases for your institute.
* **Rosters for non-teaching institutions:** "faculty" = scientific staff (Scientist B–H / Chief Scientist / Director at CSIR;
  Scientific Officers at BARC/IGCAR/RRCAT; faculty + fellows at TIFR/NCBS/IMSc). Put the definition in `SPECIAL` for each lab and
  state it in your notebook; technical staff, project staff and students stay out.

**NITs** — renamed from Regional Engineering Colleges in 2002–03 ("REC Warangal" still appears in old addresses of long-serving
people); NITK = "National Institute of Technology Karnataka"; MANIT = "Maulana Azad National Institute of Technology". A state
rule (mention + state, no other NIT named) is possible where the state has one NIT — check against the full NIT list, not only
the registered ones (e.g. Tamil Nadu has NIT Trichy; NIT Puducherry is outside it).

**Central universities** — very large, many colleges and centres. Decide and record **before** harvesting whether affiliated /
constituent colleges count (University of Delhi's ~90 colleges; JNU's special centres), and how hospitals / medical faculties
are treated (the course analysis later restricts to science & engineering, but the scrape collects everything). **BHU** shares
campus, PIN 221005 and name with IIT (BHU): mirror the IIT entry's rule (PROCESS.md §15.4) — an IIT mention or an IIT (BHU)
engineering department means IIT (BHU); departments that exist at both (chemistry, physics, mathematics, humanistic studies,
architecture) without an IIT mention are *uncertain* for both; everything else is BHU. Jadavpur University is in Kolkata
(many look-alikes: "Jadavpur" is also a locality). Jamia Millia Islamia vs Jamia Hamdard (different university, also Delhi).

**IISc / TIFR / IISERs** — "Indian Institute of Science" is a prefix of "Indian Institute of Science Education and Research":
IISc's `mention`/`explicit_full` must exclude IISER strings. TIFR has centres in other cities (TIFR Hyderabad, ICTS and NCBS in
Bangalore, NCRA Pune, HBCSE Mumbai, Balloon Facility Hyderabad): the brief lists "TIFR Mumbai" and NCBS separately — decide which
centres belong to which key, record it, and keep the keys disjoint. IISER Mohali (140306) is near IIT Ropar; IISER Kolkata
(Mohanpur 741246) shares the locality with BCKV; IISER Thiruvananthapuram moved from the CET campus to Vithura.

**Premier institutes** — the brief says: *use the ROR id directly* (ISI `ror.org/01an7q238`) to avoid wrong-institution
matches; ISI has several campuses (Kolkata, Delhi 110016 — in IIT Delhi's `other`, Bangalore, Chennai, Tezpur, Giridih …) and
possibly several ROR ids — list all, and decide whether "all campuses" is one key or several (one key, with a campus field
recorded in the notebook, is the brief's reading). Salt Lake, Kolkata (S. N. Bose Centre, 700106) and Bidhannagar (SINP,
700064; VECC nearby) share localities; Bose Institute has several campuses. NCBS is on the GKVK campus (shared with UAS-GKVK
and inStem). HRI is at Jhunsi, Prayagraj (shares the city with IIIT Allahabad and Allahabad University). CMI is at Siruseri
(SIPCOT IT park).

**CSIR labs** — names collide with unrelated organisations: NPL (also the UK's National Physical Laboratory, Teddington),
CRRI (also the Central Rice Research Institute, now ICAR-NRRI Cuttack), SERC (also IISc's Supercomputer Education and Research
Centre and the UK Science and Engineering Research Council), IICT vs ICT Mumbai, CGCRI vs CGRI. Strings usually read
"CSIR-<lab>"; **AcSIR** (Academy of Scientific and Innovative Research, Ghaziabad) appears as a second affiliation of CSIR
students — AcSIR alone must not count for any lab; AcSIR + lab counts for the lab.

**DAE institutes** — **HBNI** (Homi Bhabha National Institute) is the deemed university of BARC, IGCAR, RRCAT, NISER, IMSc, HRI,
SINP, TIFR …: HBNI alone counts for none of them; HBNI + unit counts for the unit. BARC has units outside Trombay (Visakhapatnam,
Mysuru, Tarapur …) — decide whether they count and record it. NISER shares Jatni with IIT Bhubaneswar (the IIT entry treats
NISER as other). RRCAT is in Indore (IIT Indore's `other` lists it). IGCAR is at Kalpakkam (also MAPS, BHAVINI).

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
  Your changes go into your own files: `scripts/institutes_other.py`, `scripts/test_affil_cases_other.tsv`, `agents/others.json`,
  `rosters/…`, `golden/…`, and your notebook **`WebScrape/PROCESS_OTHER.md`** (same structure as PROCESS.md §15: decisions,
  token-role table, review findings, incidents, numbers).
* If a shared script needs a change (a bug, or a new feature your institution type needs), make it on your branch in a separate
  commit, state why in the commit message, and tell the IIT team — they re-run the IIT regression (`test_affil.py` plus the v1
  string regression) before merging. Changes must keep IIT behaviour identical.
* Commit to `v2-other`: your registry/test/settings files, rosters + notes, golden sets + notes, precision audits, the notebook,
  and the final `WebScrape/v2/<key>.json` files. Never commit `WebScrape/raw/`, `logs/`, `.env`, `agents/.runtime/`.
* When an institution is finished, report: records (verified / likely / unconfirmed), recall (all / with DOI), precision per tier,
  validation result, and the open problems.

## 9. Status of the IIT run (for orientation; 2026-10-26)

* Code: registry + classifier v2 + agent kit done; 63 rule tests; v1→v2 regression read string by string (§15.1, §15.4).
* Harvest: Crossref sweeps, Europe PMC, DOAJ, INSPIRE, DBLP done for 23 IITs; ORCID for 16 (quota-limited).
* First pass `merge` done for all 23 (e.g. IIT Delhi 27,905 records, IIT Goa 665 — without person/verification channels).
* Rosters done: Palakkad, Tirupati, Bombay; golden sets done: Palakkad, Tirupati, Bombay; more running.
* Contact the IIT team for anything unclear before improvising; the notebook is the shared source of truth.
