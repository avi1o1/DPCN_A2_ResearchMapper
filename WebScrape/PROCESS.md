# Publication Scrape — Process & Decision Log

Project: DPCN Research Mapping 2026 (Group 3) — institutions: **IIT Ropar**, **IIT Kharagpur**, **IIT Roorkee** (added later, §13)
Window: publications dated **2016-01-01 … 2026-12-31**
Collection date: 2026-10-07 (citation counts are as of this date)
Operator: Aviral Gupta (with Claude Code as research assistant)

This file is written as a lab notebook: every step, decision and its rationale is recorded
in chronological order so the scrape can be reproduced and audited. Scripts live in
`scripts/`. Raw API dumps (`raw/`) and run logs (`logs/`) are written at run
time and are not kept in the repository. Final numbers are in [RESULTS.md](RESULTS.md).

---

## 0. Requirements (from `DPCN_Instruction_Note.pdf` + operator brief)

* Fetch *all* publications of the assigned institutions for 2016–2026.
* Per publication fields: `title, authors, year, type, journal/conference name, issn, doi,
  citations, references`.
* Anything uncertain or unretrievable is marked with the literal string `TODO` (optionally
  `TODO: <reason>`) so it can be followed up manually.
* Output: `iit_ropar.json`, `iit_kharagpur.json`.
* Goal is maximum recall ("no record missed") with documented precision controls.

## 1. Source reconnaissance (2026-10-07)

Probed every candidate source before designing the pipeline.

| Source | Status | Notes |
|---|---|---|
| OpenAlex API | **Blocked** — HTTP 429 | OpenAlex now requires an API key; the anonymous daily budget for our network IP was already exhausted (shared campus IP). Operator decided to **proceed without OpenAlex** and without other keyed APIs. We do *not* circumvent the limit. |
| Scopus / Elsevier API | Not available | No key. |
| Semantic Scholar (S2) API | Works intermittently (anonymous shared pool, 429s) | Used for enrichment (citations/references) with back-off. |
| Crossref REST API | **Works** | `query.affiliation=<rare token>` behaves like an exact filter for rare tokens (e.g. `Ropar`: 3,482 hits 2016–2026, 3,481 contain "Ropar" in an author affiliation). Limitation: only works whose publisher deposited affiliations (Elsevier largely does not). `filter=ror-id:` only 83 hits — useless. |
| Europe PMC REST | **Works** | `AFF:"…"` search. Ropar 1,232, Kharagpur 5,003 (2016–2026). Biomedical/life-science + chemistry heavy; includes Elsevier. |
| DOAJ API | **Works** | `bibjson.author.affiliation`. Ropar 447, Kharagpur 2,239 (all years). OA journals only. |
| ORCID public API | **Works** | `affiliation-org-name` search: Ropar 1,342 profiles, Kharagpur 9,141 profiles. Works lists give DOIs incl. Elsevier (Scopus sync). Person-level → needs date-window filtering. |
| DBLP | Website behind bot-wall; **SPARQL endpoint works** | CS coverage, person affiliations. |
| INSPIRE-HEP | Reachable, affiliation query returned 0 with our syntax | To revisit for HEP/physics. |
| IRINS (iitrpr/iitkgp.irins.org) | HTTP 403 to scripts | To try via browser/web fetch. |
| Institute websites | iitrpr.ac.in 200; iitkgp.ac.in timed out from our host | Rosters, golden set. |

ROR IDs: IIT Ropar `https://ror.org/02qkhhn56`, IIT Kharagpur `https://ror.org/03w5sq511`.

### 1.1 Affiliation search-string variants (Crossref hit counts, 2016–2026)

| Term | Hits | Comment |
|---|---|---|
| Ropar | 3,482 | primary |
| Rupnagar | 1,935 | official district name; overlaps Ropar; also matches other Rupnagar orgs → needs IIT check |
| Roopnagar | 42 | variant spelling |
| Rupar | 0 | |
| Kharagpur | 13,781 | primary |
| Khargpur | 11 | misspelling |
| Kgp | 43 | abbreviation (IIT KGP) |
| Kharagpure / Kharaghpur / Kharagpu | 0 / 0 / 1 | misspellings |

## 2. Strategy (multi-channel discovery → union → verification → enrichment)

Because no single open source covers everything, recall comes from the **union of
independent discovery channels**, and quality from a per-record **evidence trail**:

1. **Affiliation-string channels** (high precision): Crossref, Europe PMC, DOAJ, (INSPIRE).
2. **Person channels** (cover publishers without affiliation metadata, e.g. Elsevier):
   faculty rosters → ORCID works, DBLP, Semantic Scholar author pages, restricted to the
   person's tenure window.
3. **Golden set** built independently (web search, institute news, faculty homepages,
   annual reports) — used *only* to measure recall and diagnose misses; the search strings /
   channels are refined until the golden set is (near-)fully covered.
4. Enrichment of every DOI from Crossref (+ S2) for the required fields.
5. Every field that cannot be established is set to `TODO`.

(Sections below are appended as work proceeds.)

## 3. Affiliation-string search design & classification

### 3.1 How the search strings were chosen
* Crossref `query.affiliation` is a relevance (OR-of-tokens) search: multi-word queries such as
  `"IIT RPR"` or `"IIT KGP"` return ~21k mostly irrelevant hits (they match any "IIT" or "RPR").
  **Decision:** search only on *rare single tokens* (place names, PIN codes, institutional
  abbreviations) and do all precision filtering locally. Verified empirically: for `Ropar`,
  3,481/3,482 returned records contain "Ropar" in an author affiliation.
* Token list was grown iteratively by probing spelling variants and inspecting real strings
  (§1.1). Final tokens:
  * IIT Ropar: `Ropar, Rupnagar, Roopnagar, 140001` (+ broad sweep `Punjab`)
  * IIT Kharagpur: `Kharagpur, 721302, Khargpur, Kgp, Kharagapur, Kharagur, Kharapur, Khragpur,
    Karagpur, Kharagpu, IITKGP` (+ broad sweep `West Bengal`)
  * Tried, 0 hits: `Rupar, Ropad, Rupnager, IITRPR, iitrpr, Kharagpure, Kharaghpur, Kharakpur,
    Kharagpour, Kharaqpur, Kharghpur, Kharagpar, Kharagpuri, Kharagpr`.
  * `Roper` (170) rejected: only "Roper St Francis" (US hospital) etc.
* Broad sweeps (`Punjab` 65,860 and `West Bengal` 277,583 records, light fields only) catch
  strings that name the IIT without the city (e.g. "Indian Institute of Technology, Punjab").
* **Performance decision:** full-record affiliation queries ran at ~100 records / 40 s; switching to
  `select=DOI,author,title,type,issued` (light) gives 1,000 / 50 s. So discovery uses light sweeps
  and full metadata is fetched afterwards per DOI (`filter=doi:…` batches of 40, ~2 s each).

### 3.2 Classifier (`scripts/affil.py`)
Each author's affiliation strings are joined and classified as `iit | other | uncertain | None`:
1. `None` if no city/PIN/e-mail-domain token appears.
2. `iit` if a fuzzy "Indian Institute of Technology"/IIT pattern or an institute-specific unit name
   is present. Fuzzy because real strings contain typos: *Indian Institue / Institite / Insitute /
   Tnstitute / Tehcnology / Instituteof / "Indi | an Institute" / IIT1 / E&ECEIIT /
   "Indian Institute of Ropar" / "India Institute of Technology"*.
3. `other` if a known other organisation in the same city is named (Ropar: pharmacy colleges, IET
   Bhaddal, NIELIT, Shivalik, Lamrin, Rayat, InfraRed Vision Pvt Ltd, the Rupnagar locality of
   Guwahati, 140001 PIN collisions in Beijing/Hanoi, "AgroParisTech" substring; Kharagpur:
   Kharagpur/Hijli/Bhatter colleges, Govt. General Degree College Kharagpur-II, SE Railway, IIM,
   IIEST, ICT-IOC Bhubaneswar "Kharagpur extension", KGP Bremerhaven (German clinic), Kazakh "KGP"
   health centres, Tata Metaliks, Hijli Co-operative (residential) …).
4. `iit` if the string names a department/school/centre + the city and no other organisation
   (the IIT is the only multi-department research institution in Kharagpur 721302 / Rupnagar 140001).
5. otherwise `uncertain` (kept, flagged TODO).

Every distinct non-`iit` string containing the city token was printed and reviewed by hand
(Ropar: 42 → 4 uncertain; Kharagpur: 78 → 11 uncertain after rule refinement). Remaining
uncertain strings are bare locations ("Rupnagar/IN", "Kharagpur, West Bengal, India",
"Research Scholar, Ropar") — genuinely undecidable, therefore TODO.
Bug found & fixed during review: the pattern added for "Indi | an Institute" was initially too
loose and matched any "Indian Institute…" (e.g. "Indian Institute of Science, Kharagpur").

## 4. Discovery channels

| Id | Channel | Script | Evidence tag |
|---|---|---|---|
| A1 | Crossref affiliation-token sweeps | `crossref_aff.py` | `aff:crossref` |
| A2 | Europe PMC `AFF:` search (all tokens OR'ed, PUB_YEAR 2016–2026) | `europepmc_aff.py` | `aff:europepmc` |
| A3 | DOAJ `bibjson.author.affiliation` per token × year | `doaj_aff.py` | `aff:doaj` |
| B1 | ORCID profiles with an affiliation to the IIT (name token or ROR) → works within tenure | `orcid_people.py` | `orcid_tenure` / `orcid_untimed` |
| B2 | DBLP persons whose DBLP affiliation is the IIT → publications | `dblp_people.py` | `dblp_person` |
| B3–B5 | Faculty roster → Crossref author search with disambiguation; roster ORCID works; roster DBLP pid | `roster_channels.py` | `roster_crossref_author`, `roster_orcid`, `roster_dblp` |
| M2 | Missing DOIs resolved by exact-title Crossref bibliographic match (±1 yr) | `doi_resolve.py` | (metadata) |

ORCID tenure rule: a work counts if its year ∈ [start, end+1] of any matching affiliation
(employment, education, qualification, invited position; open end → 2026). The +1 year allows
for publication lag. Profiles whose matching affiliation has no start year → `orcid_untimed`.

DBLP: the website is bot-walled, so the public SPARQL endpoint (`sparql.dblp.org`) is used.
DBLP affiliations are undated, so these are weak evidence.

## 5. Merge, verification and field rules (`build_candidates.py`, `finalize.py`)

**Union key:** normalised DOI; else normalised title + year. DOI-less records are later merged
into DOI records with an identical normalised title (±1 year).

**Metadata sources:** Crossref full record (canonical) → DataCite for non-Crossref DOIs (arXiv
10.48550, Zenodo, LIPIcs…; `datacite_enrich.py`) → channel metadata (Europe PMC/DOAJ/ORCID/DBLP).

**Affiliation verification** (`affiliation_status`):
* `verified` — at least one affiliation-string evidence, or the Crossref record's deposited
  affiliations classify as the IIT.
* *rejected (contradicted)* — found only via a person channel, but Crossref has deposited
  affiliations and the channel person's affiliation on that paper is another organisation (or all
  authors have affiliations and none is the IIT). Logged at run time in `logs/rejected_<inst>.jsonl.gz`.
* `TODO: unverified-likely …` — person channel only, no affiliation metadata exists (typical for
  Elsevier), and the year lies within [min−1, max+1] of years in which the *same person* has an
  affiliation-verified paper (data-driven tenure, more reliable than self-reported ORCID dates).
* `TODO: unverified-possible …` — person channel only, outside that observed range.
* `TODO: ambiguous affiliation string only (…)`.

Audit of the first Ropar pass motivated the likely/possible split: unverified records were 32%
Elsevier, 13% Springer journals (publishers that do not deposit affiliations to Crossref), and a
random sample showed both genuine papers (e.g. PhD students' Elsevier papers) and pre-joining
papers of faculty.

**Excluded record types:** Crossref `peer-review, component, dataset, database, grant,
journal-issue, journal, proceedings, proceedings-series, book-series, report-component, standard`.
Preprints (`posted-content`, arXiv) that Crossref links to a published version in the set, or that
share an identical normalised title with a published record, are merged into the published record
(`preprint_versions`).

**Field rules**
| Field | Rule |
|---|---|
| title | Crossref/DataCite title, HTML stripped; else channel title; else `TODO` |
| authors | ordered list `{name, orcid, affiliations, institute_author}`; `institute_author` true/false/null (null = no affiliation deposited); else Europe PMC/DOAJ author names; else `TODO` |
| year | Crossref `issued` (earliest of print/online); must be 2016–2026 |
| type | `journal` (journal-article), `conference` (proceedings-article; or journal-article/book-chapter whose venue says Proceedings/Conference/Symposium/Workshop…, or has a Crossref `event`), `book-chapter`, `book`, `preprint`, `thesis`, `report`, `other`; raw type kept in `type_raw`; `TODO` if unknown |
| venue | container title (journal / proceedings / book series) → event name → channel venue; else `TODO` |
| issn | all ISSNs (print+electronic) from Crossref / Europe PMC / DOAJ; journals without ISSN → `TODO`; non-journal types without ISSN → `"N/A (not a journal)"` |
| doi | `https://doi.org/<doi>`; else `TODO` |
| citations | Crossref `is-referenced-by-count` at collection date (single consistent source); Europe PMC / OpenCitations counts kept in `citations_by_source`; `TODO` if no DOI and no other count |
| references | list of DOIs of referenced works from the Crossref deposited reference list; fallback OpenCitations Index v2; else `TODO` (`references_meta` records deposited count vs. DOI-resolved count) |

Extra audit fields per record: `affiliation_status, institute_affiliations_matched, evidence,
found_via_person, type_raw, publisher, isbn, citations_by_source, references_meta, pmid, arxiv,
todo_fields, record_id`.

## 6. Faculty rosters (`rosters/`)

Built by sub-agents from the institute websites (details, URLs and per-department counts in
the roster agents' notes; only the roster CSVs are kept):

* **IIT Ropar** — 273 people (202 current, 55 former, 15 adjunct, 1 visiting). Cross-checked
  against the institute's JSON endpoint `api/get-all-faculty` (205 entries, all covered). Former
  faculty from Wayback snapshots of department pages (2016–2025) and the joined/left tables of annual
  reports 2016-17…2023-24. Identifiers: ORCID 122, Scholar 128, DBLP 3, joining year 186.
* **IIT Kharagpur** — 1,144 people (834 current, 14 emeritus, 10 visiting, 286 former who left
  ≥2016). Lists from the site's POST endpoint `Departments/showPeopleFormerStaff` for all 65 unit
  codes; former lists carry the tenure range (used as an end bound, +1 year publication lag).
  458 archived profile pages checked: no additional former faculty found. ORCID 474 (360 by
  name-search, accepted only when the ORCID record shows IIT KGP employment), joining year 614.
* Not reachable: IRINS (Cloudflare challenge, 403/402), DBLP search (bot wall). Not circumvented.

## 7. Golden sets (`golden/`) — independent recall benchmark

Built by separate sub-agents **without** any bibliographic API for discovery (web search, institute
news, annual reports, faculty pages, arXiv PDFs with visible affiliation). Notes files list every
search string, result counts, results visited and yields.

* IIT Ropar: 339 papers (faculty pages 137, annual reports 112, arXiv 47, digest pages 39,
  web search 3, news 1). 47 % carry a DOI printed on the source.
* IIT Kharagpur: 637 papers (faculty pages 391, arXiv 102, dept pages 58, news 41, web search 24,
  annual reports 21). Generic web-search strings were unproductive (mostly aggregator pages); the
  institute news site and lab pages were productive.
* Caveat found during evaluation: faculty publication lists include papers written *before/after*
  the person's tenure. Golden entries whose publisher-deposited affiliation for that author is
  another institution (e.g. NREL, IIT Bombay, IIM Visakhapatnam) are reported as golden-set errors.

Recall evaluation (`eval_recall.py`): match by DOI, else normalised title, else token-Jaccard ≥ 0.8
(±1 year); each miss diagnosed (not discovered / dropped / rejected). Results in
summarised in [RESULTS.md](RESULTS.md) (the per-run recall reports are regenerated by `eval_recall.py`).

## 8. Iterative refinement log (recall against golden sets)

| Iter | Change | Ropar recall | KGP recall |
|---|---|---|---|
| 0 | Affiliation channels + ORCID + DBLP persons | 77.9 % | 63.9 % |
| 1 | + DataCite enrichment, preprint de-dup, INSPIRE-HEP, bare-"IIT" no longer counts as contradiction | 79.6 % | 64.2 % |
| 2 | + roster channels round 1 (Crossref author search w/ disambiguation, roster ORCID, roster DBLP) | 82.3 % | 70.2 % |
| 3 | + graded "full-name" rule + one snowball iteration + ORCID-mismatch / bare-IIT no longer hard rejects | 91.4 % (DOI 93.1 %) | 75.4 % (DOI 91.6 %) |
| 4 | precision audit → co-author keys use full first names; "full-name" rule removed; main/unconfirmed split | 85.5 % | — |
| 5 | + data-driven common-surname rule (no initial-only matches for 114/410 common surnames), name-ambiguity guard, Europe PMC DOI verification | 85.5 % | — |
| 6 | snowball removed from main-file profiles (drift); loose pass feeds the unconfirmed file only | 76.1 % | 62.6 % |
| 7 (final) | + arXiv pass, Springer-page + Europe PMC verification complete, OpenCitations fallback | **78.2 %** (DOI 83.8 %; 84.4 % incl. unconfirmed file) | **66.9 %** (DOI 80.8 %; 73.0 % incl. unconfirmed file) |

Recall in iterations ≥4 is measured on the **main file only**; the evaluator also reports recall
if the unconfirmed-candidates file were included and how many golden misses sit there.

Diagnostics that drove each change:
* Iter 0 misses were dominated by faculty without ORCID publishing in Elsevier/APS/Springer/LNCS
  venues (no deposited affiliations) → roster-driven author search.
* Broad sweeps (`Punjab`, `West Bengal`) initially "found" 650 extra KGP records: inspection showed
  these were false positives from *generic* unit names ("School of Energy Science and Engineering"
  matched Harbin/Tianjin…; "awadh" matched Awadh Dental College). Fix: generic unit names now count
  only with the city token; added the state rule (IIT + "West Bengal"/"Punjab", no other IIT city →
  this IIT). After the fix the broad sweeps add **0** (Ropar) and **3** (KGP) records beyond the
  targeted tokens → evidence that the targeted token list is complete for Crossref.
* arXiv API returned HTTP 429 when two processes queried concurrently; arXiv was split into a
  separate single-threaded pass at ≤1 request / 5 s.
* Malformed DOIs from ORCID ("1-25", "doi 10.…", "doi.org/10.…") broke Crossref batch filters →
  `norm_doi` now extracts the `10.xxxx/…` pattern and drops anything else.
* Known unrecoverable gaps: faculty with no verified seed papers and no joining year (e.g. one
  Ropar CSE faculty) cannot be safely disambiguated; papers with no DOI in Crossref/DataCite and no
  ORCID/DBLP listing (old conference papers, book chapters in small presses).

## 9. Precision audits and the resulting design (iterations 4–6)

Recall alone rewards over-inclusion, so a **precision audit** was run: a seeded stratified random
sample per institute (`precision_sample.py`, seed 20261007: 25 verified, 40 likely, 40 possible
records) was checked by a separate agent against the affiliation printed on the paper (Crossref,
Europe PMC, Springer citation meta tags, open-access PDFs, arXiv PDFs; no bot challenge bypassed).
Files: `golden/precision_audit_<inst>.csv`.

| Tier (iteration-3 data) | Ropar yes/no/unknown | precision | KGP yes/no/unknown | precision |
|---|---|---|---|---|
| verified | 25/0/0 | 1.00 | 24/1/0 | 0.96 |
| likely | 8/8/24 | 0.50 | 15/8/17 | 0.65 |
| possible | 5/18/17 | 0.22 | 3/23/14 | 0.12 |

Precision by evidence channel (both audits, unverified rows): `dblp_person` 0/6, `orcid_untimed`
3/12, `orcid_tenure` 20/7, `roster_orcid` 10/3, `roster_crossref_author` 21/32, round-2
"full-name" rule 0/3. Failure patterns: namesakes with common Indian names (Kumar, Sharma, Singh,
Das, Ghosh…), papers from before the person joined / after they left, ORCID/DBLP profiles of a
different person.

Decisions taken from the audit:
1. **Main file vs. unconfirmed file.** `<inst>.json` keeps verified records, records with
   an ambiguous affiliation string, and `unverified-likely` records that have dated/specific person
   evidence (`orcid_tenure, roster_orcid, roster_crossref_author, roster_arxiv, roster_dblp`).
   Everything else (tier *possible*; undated DBLP/ORCID-only; loose-pass-only) goes to
   `candidates_unconfirmed_<inst>.json` with an `unconfirmed_reason` — nothing is thrown
   away, but low-precision material does not pollute the dataset.
2. **Co-author identity keys** use surname + full first name (surname + initial collided massively).
3. **Common surnames** (data-driven: surname carried by ≥8 distinct first names in the institute's own
   verified papers — 114 at Ropar, 410 at KGP): initial-only author forms ("N. Kumar") are not
   matched to roster persons.
4. **Name-ambiguity guard:** `amb = Crossref works with this exact name / (verified seeds/0.35 + 5)`;
   if `amb > 2` only ORCID/affiliation evidence or (≥2 shared full-name co-authors AND shared venue)
   is accepted.
5. **Snowball removed** from main-file profiles: in iteration 5 one prolific-common-name profile grew
   from 325 to 424 seed papers by absorbing its own (partly wrong) acceptances. A separate *loose*
   pass that keeps the snowball writes only to the unconfirmed file (`roster_crossref_author_loose`).
6. **Verification channels** (confirm or refute unverified records with real affiliation text):
   * V2 Europe PMC by DOI (batched): 3,622 of 45,861 DOIs found with affiliations; e.g. 376 Ropar
     person-channel records refuted.
   * V1 Springer landing pages (`citation_author_institution` meta tags), honest User-Agent, paths
     allowed by robots.txt, 3 workers ≤1 req/s each. Browser-like User-Agents get a challenge page;
     an honestly declared bot gets the normal page — nothing is bypassed. Slow (~15 pages/min);
     re-run `finalize.py` when it completes (see §11).
   * Tested and abandoned: ScienceDirect (403), IEEE Xplore (202 challenge), Wiley/T&F/AIP/ACS (403).

Trade-off recorded honestly: removing the snowball lowered main-file recall on the Ropar golden set
from 85.5 % to 76.1 % (the difference sits largely in the unconfirmed file) in exchange for removing
a large volume of namesake errors.

## 10. Operational incidents (for reproducibility)
* Usage-limit interruption killed all sub-agents once; they were resumed from their scratch state.
* `pkill -f <pattern>` matched the invoking shell itself twice (pattern appeared in the command line);
  switched to anchored `pgrep -f "^python3 …"` + kill by PID.
* Two OpenCitations writers appended to one gzip file → corruption; caches that are appended to
  across runs (`opencitations/oc.jsonl`, `landing/springer.jsonl`) are now plain JSONL; readers
  tolerate a truncated tail; `scripts/check_shards.py` verifies gzip caches.
* A machine suspend left HTTP calls hung for ~3 h; jobs were restarted (all caches resume).
* arXiv API returned 429 under two concurrent processes → single-threaded pass at 1 req / 5 s.

## 11. Final results

See [RESULTS.md](RESULTS.md) (dataset size, per-year/type counts, TODO counts, recall, precision audits,
validation).

## 12. Confirmatory pass (2026-10-08/09): validation + TODO resolution

`scripts/validate.py` (report regenerated at run time; summary in [RESULTS.md](RESULTS.md)). Checks: schema/required fields, year range, DOI
format/lower-case/uniqueness, main∩unconfirmed overlap, ISSN format, citation values, references are
DOIs, no self-reference, type values, `todo_fields` consistency, re-classification of every verified
record's matched affiliation, near-duplicate titles, **live re-fetch of 200 random records per institute
from Crossref** (title/year/venue), cross-source citation agreement, joint papers between institutes.

Defects found by the check and fixed in the pipeline (not patched in the output):
1. ~300 records had lost their Crossref metadata (an early failed batch + DataCite "missing" rows
   blocking the Crossref retry) → retry logic fixed; also single-DOI retry for batch false negatives.
2. Duplicate registrations of the same work (ASME twin DOIs, Angewandte German-edition `ange.` DOIs,
   Inderscience twins, IOP `/meta` URL suffixes, multiple preprint versions) → merged, other DOIs kept
   in `duplicate_dois`; conference vs journal versions stay separate publications.
3. Self-references in publisher reference lists → removed.
4. INSPIRE hits without any author affiliation of the IIT (audit found one) → demoted to weak evidence
   (`inspire_unmatched`); INSPIRE matched strings now stored.
5. Year delivered as a string by CSL/DataCite → coerced.
6. ISSNs from the journal-title lookup unhyphenated / comma-joined → normalised to `XXXX-XXXX`.
7. Supplementary-material DOIs (`…-supplement`) → excluded.

TODO resolution (`scripts/resolve_todos.py`): R1 Crossref single-DOI retry; R2 doi.org content
negotiation (CSL-JSON, any registration agency); R3 DOI-less records → title search in Crossref,
DataCite and Semantic Scholar (accepted only if title-token Jaccard ≥ 0.9, |Δyear| ≤ 1 and a shared
author surname when authors are known; 23 / 314 / 175 DOIs found); R4 ISSN via Crossref journal-title
registry (exact title match); R5 Semantic Scholar reference lists / citation counts (fallback only).
Preprint venues are now filled from the preprint server (Crossref `institution` / `group-title`).
Example effect (Kharagpur): venue TODO 1,356 → 118, references 5,205 → 3,929, DOI 1,072 → 928.

Final validation: **0 violations on every check for all three institutes**; live re-check matched
title 99–100 %, year 99.5–100 %, venue 99.5–100 %; Crossref vs OpenCitations citations Spearman
ρ = 0.83 / 0.87 / 0.88 (median |diff| 0). Semantic Scholar counts agree less (ρ 0.32–0.67) and are used
only when Crossref has no count. Remaining near-duplicate titles (22 / 80 / 48 groups) are mostly a
conference paper and its later journal version.

## 13. IIT Roorkee (added 2026-10-08 on request)

Same pipeline and rules; institute-specific decisions:
* ROR `https://ror.org/00582g326`. Crossref tokens: `Roorkee` (11,833), `247667` (3,490), `Roorke` (12),
  `Rorkee` (9), `Saharanpur` (778) and `247001` (179) for the **Saharanpur campus** (Polymer & Process
  Engg, Paper Technology, Applied Science & Engg), broad sweep `Uttarakhand` (18,267). `IITR` alone was
  rejected as a token: it collides with CSIR-IITR (Indian Institute of Toxicology Research, Lucknow).
* Classifier additions after reviewing 293 distinct uncertain strings: other organisations in Roorkee /
  Saharanpur (National Institute of Hydrology, CSIR-CBRI, COER, Quantum, Motherhood, Haridwar University,
  Patanjali, CPPRI, Shobhit, medical colleges…); `IITR`+Roorkee and Saharanpur "Polymer & Process
  Engineering" count as IIT Roorkee; the department-only rule is **not** applied to Saharanpur strings
  (many unrelated institutions there). After review: 49 distinct uncertain strings (67 author slots).
* INSPIRE normalised name is `IIT, Roorkee` (357 records).
* Roster: 849 people (573 current, 227 former, 25 visiting, 18 adjunct, 6 emeritus); ORCID 371
  (322 by unique-name search accepted only with IIT Roorkee employment), joining year 482. Former-faculty
  end years are lower bounds (archive gaps) → end-of-tenure allowance +4 years for Roorkee (+1 elsewhere).
* Golden set: 562 papers (faculty pages 380, dept pages 111, arXiv 51, web search 8, news 6, annual
  reports 6); 82 % with DOI (354 looked up by exact title afterwards).

## 14. Files and how to reproduce

| Path | Content |
|---|---|
| `<inst>.json` | **Dataset** `{summary, records[]}`: pretty summary, one record per line (fields: [README](README.md)) |
| `rosters/<inst>_faculty.csv` | Faculty rosters (input to the person channels) |
| `golden/` | Golden sets (recall benchmark) and precision-audit sheets |
| `scripts/` | All scripts |

**Reproduce:** discovery harvests (`crossref_aff.py <token> --light` for every token in §3.1 / §13,
`europepmc_aff.py`, `doaj_aff.py`, `inspire_aff.py`, `orcid_people.py`, `dblp_people.py` per institute),
then `sh scripts/run_final.sh`; verification `verify_epmc.py`, `verify_springer.py`, `resolve_todos.py`;
finally `sh scripts/refresh_all.sh` (rebuild + recall + TODO sheets + validation). Crossref/ORCID/DataCite
content changes over time; citation counts are as of the collection date.

**Submission note (2026-10-09):** `candidates_unconfirmed_<inst>.json` (low-confidence person-channel
candidates, audit precision 12–22 %) is written by `finalize.py` for follow-up work but is git-ignored
and not part of the submission; likewise `todo_followup_<inst>.csv` (regenerate with
`scripts/export_todo.py`). Output JSON is written with a pretty-printed summary and one record per
line (valid JSON; fully pretty-printing would push the Kharagpur file past GitHub's 100 MB limit).

---

## 15. v2: extension to all 23 IITs (started 2026-10-25)

Operator brief: extend the dataset from 3 IITs to all IITs with the same procedure and the same strictness ("more data
points must not loosen the procedure"). The v1 datasets of §§1–14 (`WebScrape/<inst>.json`) stay untouched because
Enrichment/, Analysis/ and the Group 3 report are built on them; v2 writes to `WebScrape/v2/` (`RM_OUT=v2`).
All 23 IITs, the original three included, are (re)run with the v2 code so that every institute in the v2 corpus is produced
by the same pipeline version (the v1 raw caches were not kept, §14).

### 15.1 Code changes before any new data was used
* **Institute registry** `scripts/institutes.py`: every institute-specific fact (ROR/GRID, sweep tokens, classifier regexes,
  Europe PMC / DOAJ / INSPIRE / ORCID / DBLP queries, tenure lag) moved out of nine scripts into one module. Regression check:
  for the three v1 institutes the registry reproduces every v1 query string exactly (Europe PMC, DOAJ, INSPIRE, ORCID query/
  city/ids, DBLP, Crossref token list).
* **Classifier v2** (`affil.py`), motivated by the new geography: in Delhi, Mumbai, Chennai, Hyderabad, Varanasi … the IIT is
  one of many research organisations, so v1's "IIT mention + city token anywhere in the author's joined affiliations ⇒ this
  IIT" would credit e.g. `IIT Kanpur | Ministry of X, New Delhi` to IIT Delhi. Changes:
  1. Tokens get roles: `anchor` (campus PIN / locality / e-mail domain; may support the department-only rule), `city`
     (shared but small; no IIT mention ⇒ `uncertain`), `shared` (big city; no IIT mention ⇒ not about this IIT at all, never
     `uncertain` — otherwise every University of Delhi string would become a TODO).
  2. Each affiliation entry (` | `) and each `;` part is judged on its own. The whole string may only *rescue* an `iit`
     verdict (publishers often deposit one address as several entries: `Department of Chemistry | Indian Institute of
     Technology | Ropar | India`), and the rescue is refused (`uncertain`) if any part names another IIT or organisation.
  3. Explicit naming ("Indian Institute of Technology Kharagpur", "IIT (BHU)", "I.I.T. Delhi") is decisive, which also
     absorbs publisher PIN typos ("Indian Institute of Technology Kharagpur, Kharagpur 600036"). If another IIT is named
     explicitly and this one is not, our token is another organisation's address (`other`), or `uncertain` when our city
     *name* also appears ("Indian Institute of Technology Roorkee, Kharagpur, West Bengal 721302").
  4. Strong exclusions per institute (`exclude`): ICT Mumbai's IOC Odisha campus in the "IIT Kharagpur Extension Centre",
     Bhubaneswar.
  5. HTML entities are unescaped before splitting (`&#x0026;` contains a `;`).
  6. Manual decisions move from the git-ignored `logs/affil_manual_<inst>.tsv` (lost after v1, so v1 is not bit-reproducible)
     to the committed `affil_manual/<inst>.tsv`.
* **Regression of the classifier on v1 data**: all 64,944 distinct author-affiliation strings in the three v1 datasets were
  classified by v1 and v2 for each v1 institute. Changes (distinct strings / author slots): Ropar 2 / 2, Kharagpur 134 / 486,
  Roorkee 25 / 60. Every change was read: Kharagpur's are the ICT-IOC Bhubaneswar campus (v1 documented it as excluded in
  §3.2 but its IIT-first rule counted it) plus garbled strings now `uncertain`; Roorkee's are multi-affiliation strings in
  which Roorkee belongs to another organisation (`IIT Kharagpur | National Institute of Hydrology, Roorkee`, `CSIR-CBRI
  Roorkee | IIT Delhi`). These are v1 false positives; the bug found on the way (`drishti` matching IIT Roorkee's
  *Divyadrishti* lab) was fixed before the comparison.
* `common.OUT` is configurable (`RM_OUT`); inputs (rosters, golden sets, manual decisions) are read from `WebScrape/`.

### 15.2 Source reconnaissance for the 20 new IITs (2026-10-25)
* ROR records fetched from api.ror.org for all 20 (all `active`, matched with `chosen: true`). ROR data quirks recorded, and
  a reason never to use ROR aliases as match strings: IIT Jodhpur's record lists "AIIMS Jodhpur" as an alias, and IIT
  Hyderabad's lists a Malayalam label for "Indian Institute of *Chemical* Technology".
* Crossref (`query.affiliation`, 2016–2026, `rows=0`) hit counts were probed for every city, campus PIN, campus locality, old
  temporary campus, old district name and spelling variant (raw counts in the run logs). Findings:
  * Crossref tokenises on dots: e-mail-domain queries (`iitb.ac.in`, `iitm.ac.in` …) all return ≈3,520 hits of `ac`/`in`
    noise — unusable as queries (domains are still used by the local classifier).
  * Multi-word queries are OR-searches (`Madhya Pradesh` 96,013 = every "Pradesh"); state sweeps therefore use single rare
    tokens (`Madhya`, `Andhra`, `Himachal`, `Tamil`).
  * Polite pool limits on 2026-10-25: `x-rate-limit-limit: 3`, `x-concurrency-limit: 3` → all sweeps run with 3 workers
    and nothing else touches Crossref meanwhile.
  * Temporary/old campuses included as tokens: IIT Hyderabad (Yeddumailaram, ODF estate, old Medak district), IIT
    Gandhinagar (VGEC Chandkheda 382424), IIT Jodhpur (342011), IIT Patna (Patliputra 800013), IIT Indore (452017, Khandwa
    Road), IIT Mandi (175001), IIT Palakkad (Ahalia/Kozhippara 678557, Pudussery), IIT Tirupati (Renigunta 517506), IIT Bhilai
    (GEC Raipur, Sejbahar 492015), IIT Goa (GEC Farmagudi 403401), IIT Jammu (Paloura), IIT Dharwad (WALMI 580011),
    IIT Bhubaneswar (Samantapuri 751013). Offshore/extension campuses: IIT Madras Zanzibar, IIT Delhi Abu Dhabi, IIT Delhi
    Sonipat/Jhajjar.
* INSPIRE-HEP institution names looked up via the INSPIRE institutions API (registry `INSPIRE`); IIT Hyderabad and IIT (ISM)
  have two records each (both queried); IIT Jammu has none.
* Europe PMC / DOAJ / ORCID queries for the new institutes: campus tokens alone; shared big-city and noisy tokens (`Delhi`,
  `Mumbai`, `Mines`, `ISM` …) only together with "Indian Institute of Technology"; plus name phrases ("IIT Bombay",
  "Indian School of Mines", "IIT (BHU)" …). ORCID/DBLP person matching additionally accepts unit names unique to the IIT
  ("Indian School of Mines").

### 15.3 Rosters and golden sets for the new IITs (sub-agents)
Same design as §6/§7, briefs kept with the run notes. New in v2: every agent fetches through one shared fetcher with
per-host rate limits enforced across processes (Wayback 3 s, arXiv 5 s, others 1 s) and a shared cache, because 40 agents
on one IP would otherwise be throttled; and the agents' lab notes are kept in `rosters/notes/` and `golden/notes/`.
Golden-set sampling is now explicit: every unit, every year, ≤ 8 papers per person, fixed source mix, list order (no
cherry-picking of easy-to-find papers). The briefs were piloted on one small (Palakkad) and one large (Bombay) institute
before the other 18 were started.

### 15.4 Classifier review for the 20 new IITs (2026-10-25)
Procedure (as §3.2, made systematic for big cities): for each institute, every distinct author-affiliation string in its
Crossref sweep records that contains one of its tokens (or an IIT mention + its state) was classified, and the following
lists were read (`scripts/review_strings.py`): **all** `uncertain` strings; **all** `iit` strings *without any IIT mention*
(department rule / unit name — the riskiest verdicts); all strings with an IIT mention that classify as `None`; the most
frequent `other` strings; a random sample of `iit` strings. Every decision became a test case
(`scripts/test_affil_cases.tsv`, run by `test_affil.py` before every pipeline run).

Finding that shaped the design: **a campus PIN or locality is rarely unique to the IIT.** The department-only rule (a
department + an IIT-specific location ⇒ IIT, used in v1 for Kharagpur 721302 and Rupnagar 140001) produced false positives
wherever another organisation shares the location, e.g. Cancer Institute (WIA) departments with "Chennai 600036", PHFI's
Centre for Chronic Disease Control / FORE School of Management / DST Technology Bhavan with "New Delhi 110016", NIPER
Ahmedabad with "Palaj 382355", NSMCH hospital with "Bihta", GNRC hospital with "North Guwahati", and "Yale School of
Medicine, P.O. Box 208016". Each token was therefore re-assigned after the review:

| IIT | campus anchors kept (department rule allowed) | demoted to `city`/`shared`, because shared with |
|---|---|---|
| Bombay | Powai, 400076 | — (SAMEER on campus = strong exclusion) |
| Madras | e-mail domain only | 600036 (Cancer Institute WIA, IMSc, ARCI, VIT, CSIR-CEERI), Zanzibar (Tanzanian bodies) |
| Delhi | e-mail domain only | Hauz Khas / 110016 (institutional area; also Shenyang's postcode) |
| Kanpur | 208016 | Kalyanpur (also an IIT (ISM) address and a Lucknow locality) |
| Guwahati | 781039 | North Guwahati, Amingaon (GNRC hospital, Biotech Park, industrial park) |
| Hyderabad | 502285, 502284 | Kandi mandal (Aurobindo Pharma R&D, agricultural engineering college), Sangareddy, Medak, ODF estate 502205 |
| Bhubaneswar | Argul | Jatni / 752050 (NISER), Samantapuri / 751013 (CSIR-IMMT, ICT-IOC) |
| Gandhinagar | e-mail domain only | Palaj / 382355 (NIPER Ahmedabad, Gujarat Biotechnology University), Chandkheda / 382424 (GTU, VGEC) |
| Jodhpur | 342037, NH 62/65, Surpura Bypass, "Karwar, Jodhpur" | Karwar (also a town in Karnataka), 342011/342030 (DRDO Defence Lab, JNVU) |
| Patna | 801106, 801103 | Bihta (NSMCH, ESIC MC, NSIT, NIELIT, CIPET), Amhara (mostly the Ethiopian region), Patliputra / 800013 |
| Indore | Simrol, 453552 | Khandwa Road / 452017 (DAVV Takshashila campus, UGC-DAE CSR) |
| Mandi | Kamand, 175005, 175075, Kataula | 175001 (Mandi town) |
| BHU | e-mail domain only | the whole BHU campus (221005, "BHU") is shared with the university |
| Palakkad | 678623 | Ahalia campus / 678557 / Kozhippara / Pudussery (Ahalia's schools), Kanjikode (industrial area) |
| Tirupati | Chindepalle | Yerpedu / 517619 (IISER Tirupati), Renigunta / 517506 |
| ISM | 826004 | Dhanbad (CIMFR, BIT Sindri, BCCL, colleges) |
| Bhilai | Kutelabhata | Durg district, 491001/2, Sejbahar / 492015 (IIIT Bhilai, IIM Raipur, GEC Raipur) |
| Goa | e-mail domain only | Farmagudi / Ponda / 403401 (NIT Goa until 2023, GEC, PES and GVM colleges, NFSU), Cuncolim / 403703 (NIT Goa) |
| Jammu | Jagti, 181221, Paloura | Nagrota (Government Degree College; also Nagrota Bagwan, HP) |
| Dharwad | Chikkamalligawad | WALMI / 580011 (NFSU Dharwad campus), 580007 |

Other rules added from the review (all with tests):
* **Explicit naming** also accepts "Indian Institute of <city>" (generalises v1's "Indian Institute of Ropar"), and IIT Goa's
  school names with "Institute of Technology Goa" ("Indian" dropped), "Institute of Technology Madras" (word order separates
  it from Anna University's *Madras Institute of Technology*), "IITM … Chennai" (IITM alone is the Indian Institute of Tropical
  Meteorology, Pune).
* **Abbreviations:** single-letter forms (IIT-B, IIT-M, IIT-G, IIT-J, IIT-P …) are ambiguous between IITs (Madras/Mandi,
  Guwahati/Gandhinagar/Goa, Jodhpur/Jammu, Patna/Palakkad) and never count as unique. Four-letter forms (IITB, IITD, IITK,
  IITG, IITH, IITJ, IITP, IITI) count on their own only if nothing else is named in the same part — "Institute of International
  Trade and Development (IITD), University of Port Harcourt" and "IIITD&M Kancheepuram" matched IITD; otherwise they act as an
  IIT mention that needs the city. Longer forms (IITGN, IITBBS, IITPKD, IITISM, IITBHU …) stay unique.
* **E-mail addresses are not affiliation evidence:** they are stripped before unit/name matching (they still bring a string in
  scope, so at most `uncertain`). v1 counted "@iitkgp.ac.in" as an IIT mention, which credited e.g. a Duke University address
  and an IIT *Roorkee* address (`dsircar.iitkgp@gmail.com`) to IIT Kharagpur.
* **Addresses abroad** (USA, UK, P.O. Box … ) never trigger the department rule or `uncertain`; Chinese postcodes collide with
  PINs (110016 Shenyang, 221005 Xuzhou) and are `other`.
* **Generic neighbours** appended to every v2 institute's `other`: IISERs, IISc, NIPERs, IIMs, IIITs, NITs, medical / dental /
  pharmacy / nursing colleges, hospitals, polytechnics, colleges, universities, companies (Ltd, LLP, Inc), independent
  researchers. They never outrank an explicit IIT mention (checked first).
* **IIT (BHU):** the IIT shares campus, PIN and name with the university. "Banaras Hindu University" / "(BHU)" parts are part of
  the IIT's official name and do not block the rescue (`name_parts`; likewise "Indian School of Mines" for ISM). Without an
  IIT mention, engineering departments (ceramic, metallurgical, mining …, only at the IIT) count as IIT (BHU); departments that
  exist at both (chemistry, physics, mathematics, humanistic studies, architecture) give `uncertain`; everything else is the
  university (`other`). Known recall limitation: IIT (BHU) authors who write only "Banaras Hindu University" are lost.
* **IIT (ISM):** "Indian School of Mines" is the institute's name before the 2016 conversion and counts.
* **Hosted entities:** Technology Innovation Hubs run by an IIT count as that IIT (consistent with v1's iHub-AWaDH at Ropar):
  iHub Drishti (Jodhpur), TiHAN (Hyderabad), IPTIF (Palakkad), IITM Pravartak (Madras), IITG TIDF. IITB-Monash Research Academy
  counts (its PhD students are IIT Bombay students). Tenants of a campus are not the IIT: SAMEER (IIT Bombay campus),
  companies and ARCI centres in the IITM Research Park (strong exclusions).
* **v1 bugs found in the process and fixed** (v1 regression in §15.1 re-run after each change): "Mehta Family School" is
  not unique to Roorkee (it also exists at IIT Guwahati and IIT Palakkad; v1 credited "Mehta Family School of Sustainability,
  IIT Indore" to Roorkee); v1's non-IIT marker "drishti" is IIT Jodhpur's own iHub Drishti; e-mail evidence (above).
  Final v1→v2 differences on the 64,944 v1 strings: Ropar 1, Kharagpur 145, Roorkee 32 distinct strings, every one read.
* The department rule also accepts "Discipline of …" (IIT Indore / Gandhinagar / Jodhpur unit naming).

Effect at the end of the review (distinct strings classified `iit`, before → after the review): e.g. Patna 1,728 → 1,627,
Gandhinagar 2,349 → 2,129 (NIPER-A), Delhi 8,311 → 8,171; `uncertain` lists shrank to 0–80 distinct strings per institute
(Delhi 80: small organisations in the Hauz Khas institutional area; BHU 12: genuinely ambiguous departments).

### 15.5 Pipeline changes for scale
* `common.get` enforces Crossref's concurrency limit (3) across all processes and threads with file-lock slots, so scripts
  that run in parallel cannot exceed it together (tested: 12 parallel callers → peak 3).
* `crossref_enrich.py` stores only the fields `finalize.py` reads (references reduced to DOIs, as finalize did on load);
  abstracts, licences, links and funders made the cache several GB for 23 institutes.
* `finalize.py` / `roster_channels.py`: "bare IIT" (IIT mention without any IIT's place) is tested against all 23 IITs.
* `run_v2.sh merge|final|refresh` drives the v2 run; recall evaluation is skipped for an institute until its golden set exists.
* Operational incident (2026-10-25, ~15:00): a usage-limit interruption paused the sub-agents (resumed from their saved
  state), and a transient DataCite outage killed all four `datacite_enrich.py` workers during IIT Bombay's first pass (arXiv
  DOIs left without metadata in that pass). Fix: a DOI whose lookup fails after the retries is logged and *not* cached, so
  the next run retries it; it no longer kills the worker. The first pass is superseded by the final run anyway.
* Pilot results (Palakkad, 2026-10-25) and the brief changes they caused: the roster brief now fixes the status set, gives every
  non-current person a tenure range (mentor faculty from IIT Madras are `visiting (2015-2016)`), defines `joining_year`, names NIRF
  data submissions as a primary source, and warns that archived lists go stale. `roster_channels.py` now bounds every non-current
  person by their range (before: only `former`; no v1 roster has a ranged non-former person, so v1 is unaffected). The golden
  brief now forbids institute IRINS portals, requires the affiliation on the paper for `high` (annual reports list pre-joining
  papers), samples evenly through lists instead of the newest N, and caps 8 papers per person across sources. arXiv's
  robots.txt asks for a 15 s crawl delay: the shared fetcher used 5 s during the pilots and now enforces 15 s; the pipeline's
  arXiv pass uses the export API (documented limit one request / 3 s) at 5 s.
* Known inconsistency carried from v1: the Kharagpur/Roorkee golden sets added DOIs by exact-title Crossref lookup afterwards; v2
  golden sets carry only printed DOIs. Recall is therefore compared on title+DOI matching (unaffected); "recall on golden papers
  with a DOI" is not comparable between v1 and v2 golden sets without the same lookup, which will be applied uniformly at
  evaluation time and reported separately.
* arXiv pacing (operator decision, 2026-10-25): because of the deadline the shared fetcher uses 5 s between arxiv.org requests,
  not the 15 s crawl delay in arXiv's robots.txt. Safeguard: a 403 from arXiv (its blocking response) stops arXiv fetching for
  all agents; HTTP 429/5xx back off exponentially. Only allowed paths (/abs, /pdf, /list) are fetched; /search is not.
* Operational incident (2026-10-25/26): the ORCID harvest hung on IIT Kanpur (no progress for ~2.5 h, 0 % CPU, after a
  machine suspend — the same failure mode as v1 §10). `orcid_people.py` now checkpoints every fetched profile and resumes; the
  queue (`raw/run_orcid.sh`) runs each institute under a 2-hour watchdog with up to 5 resumed attempts.
* First pass (affiliation channels + DBLP; ORCID only for Bombay and Delhi; no roster channels, no verification channels):
  records per institute from 665 (Goa) to 27,905 (Delhi). Not comparable to v1 final numbers yet — the person and
  verification channels are added in the final run.
* ORCID limits (2026-10-26): (1) the anonymous public API has a **daily quota per IP**; after ~60,000 profile fetches in one
  day (16 institutes harvested) every request returned HTTP 429 "exceeded the daily quota for anonymous usage". The queue was
  stopped rather than retried; remaining: Madras, Kanpur (resumes from checkpoint), ISM (checkpoint), Bhilai, Goa, Jammu,
  Dharwad. (2) The search API pages through at most 10,000 hits; IIT Madras has more. A search above 10,000 is now split by the
  first letter of the family name plus a remainder query, and the union is checked against the reported total.

### 15.6 Roster-driven channels for people affiliated mainly elsewhere
The new IITs' rosters contain many `visiting` people (IIT Tirupati: 72 of 248 — mentor faculty from IIT Madras, guest
faculty) and `adjunct` people (professors of practice, honorary professors). Their ORCID/DBLP works lists and co-author
matches would bring in papers written at their home institutions, which the "likely" tier cannot tell apart where the
publisher deposits no affiliation. v2 rule (`roster_channels.py`): for `visiting` and `adjunct` roster people a paper is
accepted only if this IIT's affiliation is printed on it (Crossref deposited affiliation, arXiv affiliation); ORCID identity,
co-author/venue matches, ORCID works and DBLP works are not used for them. v1 rosters also had visiting/adjunct people (Ropar 16,
Kharagpur 10, Roorkee 43); the v2 re-run of the three applies the same rule.
* IIT Bombay golden set (2026-10-26): 582 papers (target 650; annual reports from 2016 carry counts only), 151 high / 431 medium.
  Two caveats kept in its notes: ~150 medium rows rest on on-page tenure evidence (no documented joining year) — the precision
  audit samples these first; 71 arXiv rows were found via arXiv `/search` before the "no /search" decision reached the agent
  (each has the IIT Bombay affiliation verified in the PDF, so they are kept). The golden brief now covers missing joining
  years, count-only annual reports, the per-person cap with co-authors, truncated titles, homonyms and a time budget.
* IIT Tirupati golden set: 313 papers, 26 high / 287 medium (the institute's profile API returned 502 and six department sites
  were "under maintenance", so most faculty-page rows come from Wayback copies and homepages). Decision: affiliations of joint
  centres that name the IIT explicitly (CAMOST, "joint initiative of IIT Tirupati & IISER Tirupati") count as the IIT (test
  case added); the golden agent had excluded such papers, which only removes them from the benchmark, not from the dataset.
* IIT Bombay roster (2026-10-26): 1,286 people (804 current, 189 former, 30 emeritus, 208 visiting, 56 adjunct), 30 units;
  NIRF 2026 lists 749 regular faculty working, 635 matched (most unmatched NIRF rows are truncated first-name-only entries); 13
  unit websites do not resolve in public DNS (archive + NIRF used). 179 people await ORCID lookup (quota). One duplicate removed
  after review (associated-faculty listing). The 208 `visiting` rows include honour rolls of past visitors: harmless for the
  pipeline because visiting people only contribute papers that print the IIT's affiliation (§15.6). The roster brief now
  prescribes a quota-frugal ORCID route, the treatment of associated faculty, honour rolls, defunct units and NIRF-only people;
  the shared fetcher no longer retries DNS/TLS failures (it reports them as DEAD).
* Golden sets, 2026-10-26: IIT Jammu 348 (48 high) and IIT Dharwad 297 (37 high) accepted (`agents/check_outputs.py` clean).
  Both new IITs have almost no 2016–2017 rows (institutes founded 2016; joining years are upper bounds from archived lists),
  and several annual reports are image-only PDFs (read from rendered pages where used). Consistency fix: 46 IIT Palakkad
  annual-report rows were `high` from the pilot, before the rule "an annual-report listing alone is medium"; harmonised.
* ORCID harvest complete for all 23 IITs (2026-10-27 08:00, after the quota reset at 22:51 — roughly 24 h after exhaustion).
  IIT Madras: 11,093 profiles, the partitioned search recovered all 11,093 reported. Roster agents now match faculty against an
  offline index of these harvested ORCID affiliation records (employment/education/invited-position entries naming the IIT, with
  dates) instead of per-person API lookups; same acceptance rule (an employment at this IIT on the ORCID record), no quota use.
* IIT Goa (287 papers, 38 high) and IIT Bhilai (287, 37 high) golden sets accepted. Bhilai caveats: the institute's live sites fail
  TLS (Wayback copies used), five annual-report PDFs were unreadable (truncated copies / image-only), no 2016–2017 rows (tenure
  rule + institute founded 2016). From 2026-10-27 new agents run on Sonnet 5.5 (operator decision, to finish faster within
  usage limits); the pilots and the first golden sets were Opus 5.5. Harness limit: 20 concurrent agents.
* IIT Mandi golden set accepted (2026-10-27): 300 papers (target 400), 40 high / 260 medium, 64 with a DOI; the first agent's
  ~215 transcribed rows were spot-checked only, the rest built by its Sonnet continuation (38 arXiv rows verified in the PDF,
  51 department/lab rows). Source mix off target (news ~1 %). Unused sources: the institute repository (odr.iitmandi.ac.in)
  and the SCS/SCEE publication listings.
* IIT Jodhpur golden set, first pass (2026-10-27): 126 papers against a 450 target and **not accepted as the benchmark**: no
  faculty-page or department-page rows (IITJ profiles list no publications, departmental publication pages are empty in the
  archive), 61 arXiv + 62 annual-report + 3 news rows, skewed to physics/CS/maths; Chemical Engineering, Design and CETSD are
  empty. A supplement agent extends it from personal homepages and lab pages (the standard sources of the other golden sets).
  Recall on Jodhpur is reported only after the supplement, with the first-pass size and bias stated.
* IIT Guwahati roster accepted (2026-10-27): 655 people (488 current, 65 former, 101 visiting, 1 emeritus), 17 units; 470 of 488
  current confirmed in NIRF; 276 ORCIDs from the offline index. Known gap: the archived 2016–2020 department faculty pages were
  not fetched (shared Wayback slot, ~30 min per CDX query), so former faculty rest on NIRF and annual-report tables and
  2016–2017 leavers are mostly missing. 72 NIRF-2026 people with designation "Other" (not on the faculty list) were excluded as
  presumed staff; two different people named Gautam Barua are both kept.

### 15.7 Run structure and timing (2026-10-27)
First complete run (IIT Palakkad, the smallest IIT, 230 roster people): 234 min wall-clock, 3 min CPU. Crossref author queries
(`query.author`, 1000 rows) take 9–14 s each and the polite pool allows 3 at once → ~15 min per roster pass for 230 people
(~90 min for IIT Bombay's 1,286); the arXiv pass is 5 s per person (~20 min); one pass took 3 h 15 min with no logged errors
(a Crossref slowdown). Consequences for the driver (`run_v2.sh`):
* stages are separate queues (`roster`, `arxiv`, `verify`, `refresh`) so different services run in parallel;
* the **loose roster pass is optional and off by default**: it feeds only `candidates_unconfirmed_<inst>.json` (precision
  12–22 %, git-ignored, not part of any dataset, §9) and doubled the Crossref time. Dataset counts are unaffected; only the
  diagnostic "recall if the unconfirmed file were added" is not produced for institutes run without it. Palakkad had it.
* the verification channels of v1 (§9: Europe PMC by DOI, Springer landing pages, TODO resolution) are an explicit `verify` stage;
  the first Palakkad run omitted them (782 `unverified-likely` records remained) and is superseded by the verified run.
Palakkad first run (without verification), against its 308-paper golden set: recall 67.2 % (83.3 % for golden papers with a
DOI); v1 for comparison 67–74 % / 81–83 %.
* IIT Hyderabad golden set accepted with caveats (2026-10-27): 398 papers (target ~650, floor ~550 not reached: the agent stopped
  at the interruption), 378 medium / 20 high, no IIIT-H papers (one arXiv candidate rejected for that). Seven units have 1–11 rows
  (Physics, Chemical, MSME, Design, BME, AI, Biotech): per-unit recall is reported as unreliable there. ~17 rows with broken
  title/venue parsing were dropped. News share 0 (institute news lists no papers).
* IIT (BHU) golden set accepted as a weak benchmark (2026-10-27): 365 papers (target 550), 100 % faculty profile pages (~79
  people, regex-parsed), all `medium`, years 2016–2025. Uneven units: Civil, Mechanical, Mining, Biochemical, Humanities
  over-represented; Computer Science 6 rows, Electrical 1, Electronics / Metallurgy / Physical AI thin or empty. BHU recall is
  reported only for units with enough rows and labelled lower-confidence; a supplement from lab pages / arXiv / annual reports
  is listed as open work (like Jodhpur's, which is under way).
* IIT Goa roster accepted (2026-10-27): 113 people (69 current, 13 former, 25 visiting incl. 14 IIT Bombay mentor faculty, 6
  adjunct). Gaps: NIRF 2019–2024 PDFs were error pages (only 2025/2026 usable), two annual-report PDFs truncated, no 2022–2024
  archived snapshots parsed → regular faculty who left 2021–2024 and are not in NIRF 2025/26 may be missing; former-faculty ends
  are lower bounds. Two people still on the live site were marked former from NIRF leave dates; one Dean-listed person kept as an
  IIT Bombay mentor (ambiguous).
* IIT Kanpur roster accepted (2026-10-28): 858 people (607 current, 127 former, 94 visiting, 23 adjunct, 7 emeritus); 382 ORCIDs
  from the offline index; size matches NIRF 2026 (615 working vs 607 current + ad hoc as visiting/adjunct). An initials-matching bug
  (NIRF names attached to the wrong page names) was found and fixed with a strict compatibility check; 5 true duplicates merged.
  Gaps: 115 rows have no department (NIRF-only people); leavers of 2016–2020 may be missing (archive covers 2016–2021, NIRF from
  2021); 12 ORCID cases with several qualifying iDs left blank; four same-name pairs kept as different people on join dates only.
* IIT Madras roster accepted (2026-10-28): 996 people (670 current, 60 visiting, 266 former), 16 departments + 259 NIRF-only rows
  without a department; 337 ORCIDs from the offline index (73 ambiguous left blank, department fit not checked). Gaps: no Zanzibar
  campus (site unreachable, not in NIRF), no archived faculty-page pass so former-faculty last years are NIRF lower bounds, no
  emeritus/adjunct rows, Engineering Design (12) and CSE (37) department lists look low against NIRF, current count confirmed by
  NIRF 2026 only.

### 15.8 First complete v2 results, pipelined run (2026-10-28)
| Institute | Records | Verified | Golden n | Recall | DOI recall |
|---|---|---|---|---|---|
| IIT Palakkad (no verify stage) | 2,115 | 1,331 | 308 | 67.2 % | 83.3 % |
| IIT Goa | 1,016 | 730 | 287 | 69.0 % (70.2 % w/o 5 refuted) | 83.8 % (n=37) |
| IIT Tirupati | 1,743 | 1,265 | 313 | 55.9 % (56.6 % w/o 4 refuted) | 63.6 % (n=44) |
Tirupati diagnosis: of 138 misses, 104 were never discovered, 28 sit in the unconfirmed-candidates file, 4 are refuted by
publisher affiliations, 2 were dropped after discovery. Recall is 0 % for 2016–2017 (7 papers) and 28 % for 2018, 72 % for 2023;
annual-report rows 45 %, conferences 56 %, books 0 % (8). So the shortfall is mostly early years and sources the affiliation
channels do not reach, not a classifier effect. Not yet investigated: whether early-year roster tenure (joining years) or a
Crossref author-name search gap explains the undiscovered early papers.
* IIT Madras golden set, first pass (2026-10-28): 230 papers against a 650 target, **not accepted as the benchmark**: 69 %
  annual-report rows from only two usable reports (2017-18, 2019-20), so 2017 and 2019 hold ~75 % of rows and other years are
  thin; no department/lab pages; 3 news rows. A supplement agent adds faculty homepages, lab and department pages, and the
  years the first pass misses. Madras recall is reported only after it.
* IIT Bhubaneswar roster accepted (2026-10-28): 312 people (226 current, 44 former, 26 visiting, 15 adjunct, 1 emeritus), 7 schools;
  216 of 230 live-list entries confirmed in NIRF 2026; 143 ORCIDs (142 offline index, 1 profile page). Decision for the reader: 22
  NIRF people with designation "Other" (Adhoc/Contractual) were excluded as guest-lecturer-like, against the brief's "include
  NIRF-only people"; names are in the notes. Gaps: no archived capture after 2023-12, no annual reports, NIRF before 2023 unavailable,
  no per-school former-faculty pass; 2016-only people have uncertain last years.
* IIT Hyderabad roster accepted (2026-10-28): 558 people (358 current, 153 adjunct, 19 visiting, 26 former, 2 emeritus), 18 units;
  330 of 358 current confirmed in NIRF 2026; 228 ORCIDs (offline index). Gaps: no archived faculty list for 2018-19 (dynamic page),
  no adjunct list for 2017–2019, 8 people dropped (all NIRF leaving dates before 2016), so the former count (26) is low and is a
  floor. A name change (Pritha Bhattacharya = Pritha Chatterjee) is assumed. One IIIT-H person (P. Kumaraguru) is on IIT-H's own
  adjunct list and kept as adjunct, flagged in the notes. The golden set (398) predates this roster and used its own NIRF tenure.
* IIT Bhubaneswar golden set accepted with a flagged source (2026-10-28): 450 papers, 29 high / 421 medium, 2016–2026 (about 37 per
  year to 2023, 46–53 for 2024–2026, because lists run newest-first). Source mix: faculty pages 44 %, Central Library publications
  list 27 % (122 rows, stored as evidence_source `websearch`), department pages 12 %, annual reports 11 %, arXiv 6 %, news 0.2 %.
  The library list (library.iitbbs.ac.in/publications.php) is an institute-hosted list, which the brief allows, but its feed is not
  documented; if it is Scopus- or IRINS-backed it would breach the independence rule, so the 122 rows are separable by their
  `websearch` tag and recall is also computed without them. They over-represent HSSM, MMME and EOCS.
* IIT Madras golden set accepted as partial (2026-10-28): 501 papers (target 650), 25 high / 476 medium, 2016–2026 (2017 and 2019
  now 34 % instead of ~75 %). Source mix ≈ annual reports 32 %, faculty pages 32 %, department pages 32 %, arXiv 4 %, news 0.6 %
  (brief: 50/15/15/10/10), DOI printed on 35 %. Sampling bent on purpose: 2017/2019 entries excluded from the new rows and
  department pages capped per page, to lift thin years. Chemistry pages are behind a CAPTCHA (not bypassed), Biotech lists none,
  WSAI shows only the first three authors. Parse risks (comma-split titles on two faculty pages; initial-only name matches) are in
  the notes. Two Applied Mechanics labels merged here.
* IIT Kanpur golden set accepted with caveats (2026-10-28): 432 papers (target 600), 37 high / 395 medium, 22 units, 204 authors,
  2016–2026. Source mix far from the brief: faculty pages 66 %, department pages 24 %, arXiv 8 %, annual reports 1.4 % (the
  annual reports contain no publication lists), news 0.7 %. DOI printed on ~21 %. Thin units: Biological Sciences & Bioengineering 2,
  Photonics 2, Earth Sciences 1, Sustainable Energy 1; 2024–25 over-represented (EE pages). One over-cap author trimmed to 8.
  The original search strings were lost with the interrupted agent.
* IIT Patna golden set accepted as a weak benchmark (2026-10-28): 391 papers (target 450), 17 high / 374 medium, all ten academic
  units (CSE 69 … Metallurgical 21), years 2016–2026 (thin 2016–17 and 2026). Source mix: faculty-page fields 89 % (the
  per-department faculty profile fields are labelled faculty_page, not dept_page), annual report 2017-18 only (24 rows), arXiv 17,
  department pages 0, news 0 (no dated lists or coverage found). No roster, so joining years are upper bounds from personal pages
  or the 2016 archived list; three faculty with unresolved tenure excluded. Only ~21 % print a DOI.
* IIT Guwahati golden set accepted with caveats (2026-10-28): 576 papers, 46 high / 530 medium, 189 authors, 16 units, 2016–2026
  (21–93 per year), DOI printed on 25 %. Source mix: faculty pages 66.7 %, annual reports 12.5 % (only 2016–2019 list papers),
  department pages 12 %, arXiv 8 %, news 0.9 %. The library PDFs at iitg.ac.in/lib/IITCouncil/* were excluded because they are a
  Scopus export (independence rule); they would have covered 2023–2026 and can be admitted only by an explicit decision. The roster
  lacks joining years for many faculty, so the tenure rule drops their papers. 2017–18 and Physics (half the arXiv rows) are heavy.
* IIT Gandhinagar roster accepted (2026-10-28): 404 people (165 current, 53 former, 163 visiting, 23 adjunct), 18 units; 136 ORCIDs
  (offline index). Everything comes from archived pages (the live site returns 403 to the fetcher); joining years (122) are first
  archived appearance, i.e. upper bounds; last years may be off by up to a year; people who joined and left between the
  semi-annual snapshots are missed; several people last seen in 2025 are marked former only because they are absent from the
  March 2026 list. The NIRF file cached is a count-only summary (171 faculty), so current rows (165) cannot be NIRF-confirmed.
* IIT Jodhpur roster accepted (2026-10-28): 443 people (324 current, 74 former, 44 adjunct, 1 visiting), 17 units, 52 without a
  department; 235 ORCIDs (offline index); 267 NIRF-2026 distinct people all present in the current set, 57 current rows are on the
  website lists but not in NIRF (probably recent joiners). Gaps: the old-site faculty endpoints hold no names, so former faculty
  come from NIRF only and sciences / humanities / management leavers before ~2021 are missing; annual-report staff could not be
  separated from faculty; NIRF name order (surname-first vs given-first) was kept as printed, so some former rows read
  surname-first; two people named Jitendra Kumar are not separable; Ajay Agarwal's NIRF join 2021 vs annual-report tenure to 2024.
* IIT Gandhinagar golden set accepted with caveats (2026-10-28): 349 papers (target 450), 22 high / 327 medium, all 13 units
  (Earth Sciences 7 rows), 2016–2026 with 2018–2020 over-represented (66 / 90 / 53) and 2016 (4), 2017 (15) thin. Source mix:
  faculty pages 65 %, annual reports 29 % (only 2018-19 and 2019-20 list papers), arXiv 6 %, department/lab pages and news 0
  (archived news pages 404). DOIs printed on 31 %; annual-report DOIs whose text extraction had lost a character were blanked
  rather than kept as printed. Roster joining years are upper bounds; blank = on the June 2016 page, treated as 2015. Papers listed
  by physicists from earlier employers were dropped.
* IIT Delhi roster accepted as PARTIAL (2026-10-28): 738 people (648 current, 51 former, 17 emeritus, 18 adjunct, 4 visiting), 24
  units, 324 ORCIDs (offline index). The current count is ~185 (22 %) below NIRF 2025's 833 (NIRF 2021/22/23: 682/880/745), and no
  row can be NIRF-confirmed (the NIRF PDFs hold counts only, no names). Only 5 joining years (retired faculty), so tenure-based
  steps cannot use this roster. No former-faculty discovery for CSE, EE, Mechanical (the largest gap); no lists for CAS, CRDT, ETSC,
  TRIPP, CARE, Bharti, SIT; Abu Dhabi, Sonipat and Jhajjar not covered. Consequence for the pipeline: the strict roster pass
  cannot find papers by Delhi faculty missing from this roster, so Delhi recall is expected to be lower and must be read together
  with this coverage figure.
* IIT Jodhpur golden set accepted as a weak benchmark (2026-10-28): 192 papers (target 450; first pass 126 + supplement 66), 67
  high / 125 medium. Source mix: arXiv 32 %, annual reports 32 %, department/lab pages 25 %, faculty pages 8 %, news 3 %. The
  supplement came from Google-Sites lab and personal pages that exist mainly for recent hires, so 2021–2026 got all new rows and
  2016–2020 only the first pass's annual-report rows (2016–2019). No Bioscience, Design, CETSD or Aerospace rows (only
  forbidden IRINS-style portals surfaced). 14 supplement rows pass the tenure rule only because lists are newest-first; one author's
  rows (Sarkar) were not checked against place of work; one name (Kothadia) is inferred from the roster. News titles were
  recovered by web search, not from the news item. Jodhpur recall is small-sample (192) and skewed to recent years and to
  Civil, Chemical, Materials; read it as indicative only.

### 15.9 Working order: depth first (2026-10-28, user decision)
Breadth-first ran too many agents and pipelines at once (three usage-limit stops, four arXiv passes sharing one host). From now on a
few institutes are taken to the end (roster → golden → pipeline → recall/precision review → notes) before the next ones start.
Wave 1 (inputs complete): Palakkad, Goa, Tirupati, Bombay, Hyderabad, Madras. Wave 2 (inputs complete, pipeline pending): Kanpur,
Guwahati, Gandhinagar, Jodhpur, Bhubaneswar. Wave 3 (inputs unfinished): Delhi (golden), Patna, Indore, Mandi, BHU (rosters), then
ISM, Bhilai, Jammu, Dharwad (rosters) and Indore, ISM (golden). Paused agents keep their saved work and are resumed one at a time.

### 15.10 IIT Palakkad end-to-end result (2026-10-28)
Pipeline run: 2,136 records (1,613 verified, 522 unverified-likely, 1 ambiguous), 505 further candidates in the unconfirmed file.
Recall against the 308-paper golden set 69.5 % (69.9 % without 2 entries refuted by publisher affiliations); DOI recall 84.4 %.
Precision audit (65 records, one agent, `v2/golden/precision_audit_iit_palakkad.csv`): verified 25/25 yes (100 %); unverified-likely
11 yes / 3 no / 26 unknown (79 % on the 14 decidable rows; 26 unknown because Elsevier, IEEE, AIP, APS and SSRN pages are stubs or
bot-challenged and were not bypassed — the figure is weak evidence). All three "no" rows had only `orcid_tenure` (± `roster_orcid`)
as evidence: two are papers from before the person's move (ORCID employment dates too loose), one is a wrong person at NIT
Rourkela. Rows with `roster_crossref_author` plus a printed affiliation were all yes. Open question, not acted on: whether
`orcid_tenure`-only rows should leave the main file; to be decided after Goa and Tirupati are audited, on all three institutes.
* IIT Delhi golden set accepted as a weak, skewed benchmark (2026-10-28): 213 papers (target 650), 21 high / 192 medium. Source mix:
  faculty pages 80 %, department pages 10 %, arXiv 8 %, news 2 %, annual reports 0 (rti.iitd.ac.in fails TLS; archived copies 404 or
  HTML wrappers). Covered: Mechanical, Chemistry, Textile, Physics (over-represented), a few EE / Energy / Applied Mechanics / Maths /
  Chemical pages; Civil, Biological Sciences, Design, Management, HSS, Public Policy and most of the School of AI have no rows, CSE
  and biomedical one each. Only people with a joining year on their own page are included (about half of the Mechanical, Chemistry
  and Textile profiles excluded). 2016 has 34 rows, 2018 14, 2026 7. Delhi recall will be reported per covered department only, and
  together with the roster's 22 % shortfall against NIRF; it is not an institute-wide figure.

### 15.11 Precision audit, three IITs pooled (2026-10-28)
Seeded samples of 25 verified + 40 unverified-likely records per institute, checked against the affiliation printed on the paper
(Crossref, Europe PMC, publisher meta tags, open-access / arXiv PDFs; no bot challenge bypassed; Unpaywall was used by the Goa and
Tirupati agent only to locate an open copy of a known DOI, not to discover records).

| Institute | verified yes/no/unk | precision | likely yes/no/unk | precision (decidable rows) |
|---|---|---|---|---|
| Palakkad | 25 / 0 / 0 | 100 % | 11 / 3 / 26 | 79 % (n=14) |
| Goa | 24 / 0 / 1 | 100 % | 12 / 5 / 23 | 71 % (n=17) |
| Tirupati | 25 / 0 / 0 | 100 % | 11 / 1 / 28 | 92 % (n=12) |
| pooled | 74 / 0 / 1 | 100 % | 34 / 9 / 77 | 79 % (n=43) |

Of the 120 likely rows, 77 (64 %) could not be decided (Elsevier, IEEE, APS, SSRN, AIP pages blocked or bare), so the likely-tier
figure is a weak estimate; the verified tier held on every institute. Failure types in the 9 "no" rows: papers printed at another
institution before the person joined (4), namesakes (3), person printed elsewhere (2). By evidence (pooled, decidable rows only):
roster_arxiv 16 yes / 2 no; roster_crossref_author alone 4 / 1; orcid_tenure alone 4 / 2; the combinations with orcid_tenure
1–4 yes / 1 no. Samples of ≤ 6 rows per combination do not separate the channels reliably.
Decision: **no change to the main/unconfirmed split.** Evidence for dropping `orcid_tenure`-only rows (4/6 yes) is too thin; the
precision of the "likely" tier is reported as 79 % on the decidable rows with 64 % undecidable, the verified tier as 100 %. A larger
audit of orcid_tenure-only rows (~40 rows from the six IITs finished by then) is listed as open work.
* IIT Patna roster accepted (2026-10-28): 217 people (162 current, 50 former, 4 visiting, 1 adjunct), 10 departments; 151 of 162
  current NIRF-confirmed; 118 ORCIDs (offline index); 174 joining years, all NIRF. Gaps: live NIRF links are 404 and only the 2016
  (names), 2018, 2022 and 2025 submissions are archived, so last years of former faculty can be up to ~2 years early; ~26 former
  rows rest on the 2016 names table only (year and unit unknown); 34 former rows have no department; 110 NIRF rows with designation
  "Other"/blank excluded as non-faculty (some genuine visitors may be among them); four CEE people marked former on the live-page
  absence alone; annual reports unusable. With its golden set (391) Patna now has both inputs.
* IIT (BHU) roster accepted (2026-10-28): 596 people (412 current, 70 former, 114 visiting); 374 of 412 current NIRF-2026-confirmed
  (NIRF 2026: 409 rows); 320 ORCIDs (210 from the institute profile pages, 110 offline index); 487 joining years from NIRF.
  Inconsistency to resolve: the 114 NIRF "Other" rows (re-employed senior people, ad hoc/contractual faculty) are kept here as
  `visiting`, while Bhubaneswar (22) and Guwahati (72) excluded the same NIRF category. Gaps: 82 former/visiting rows without a
  department (archive queries failed), NIRF 2018 is an image PDF (not OCR'd) and 2020 a stub, 36 former last years are lower
  bounds, two people retired in 2025 but still "working" in NIRF were set former, former names kept surname-first as NIRF prints.
* IIT Mandi roster accepted (2026-10-28): 322 people (216 current, 50 former, 42 visiting, 14 adjunct), 12 current units + 2 defunct
  schools; all 189 NIRF-2026 Regular people present, 188 current rows NIRF-confirmed (27 more current than NIRF-Regular: late
  joiners and people NIRF omits); 128 ORCIDs (123 offline index, 5 pages); 280 joining years (NIRF). Gaps: no archived faculty lists
  for six schools between the 2020 reorganisation and 2024-11, so faculty who left 2019–2021 and are not in NIRF 2019/2021 are
  probably missing and Wayback-only ranges understate tenure; 38 rows without a department; ORCID matches use name + role and
  were not checked against employment dates; the live directory omits the Director and a few others (treated as current from
  school pages / NIRF, ~4 rows). NIRF "Other/Contractual" rows are labelled visiting (as BHU; unlike Bhubaneswar and Guwahati).
* IIT (ISM) Dhanbad golden set accepted (2026-10-28): 541 papers (target 550), 53 high / 488 medium, all 17 departments, 179
  authors (max 7 each), 2016–2026 (2016: 28, 2024–26 heavy), DOI printed on 36 %. Source mix: faculty pages 72 %, department pages
  12 %, arXiv 10 %, news 6 % (department newsletters), annual reports 0 (only 2024-25 is published, image pages, counts only).
  About 246 of 445 profiled people have no joining year on their page and were skipped (no NIRF or archive lookup yet), so
  older faculty without a dated page are missed; the ISM roster should widen that. Only 6 of 17 departments yielded
  department-page rows. One image-only newsletter PDF skipped (no OCR).
* IIT Indore roster accepted (2026-10-28): 302 people (229 current, 34 former, 31 visiting, 8 adjunct), 13 units; all 213 NIRF-2026
  Regular present as current, 16 more current rows from 2026 department pages; 135 ORCIDs (offline index); 257 joining years
  (NIRF; may be regularisation dates, 13 people appear on archived lists earlier). Gaps: most department sites return a 403
  bot challenge (archive used instead); no archive for Mechanical (meche.iiti.ac.in) and AASE is a JS shell, HSS 2016–2020 pages
  are empty iframes, so former faculty 2016–2020 are under-covered there; 41 rows without department. 25 NIRF "Other" people
  (postdocs, project staff) excluded and six undated or pre-2016 former members left out — the "Other" handling here follows the
  Bhubaneswar/Guwahati exclusion and differs from BHU/Mandi (visiting); to be unified.
* IIT Indore golden set, first pass (2026-10-28): 171 papers against a 450 target, **not accepted as the benchmark**: 28 high /
  143 medium; source mix department pages 60, annual reports 43, faculty pages 40 (23 %), arXiv 28, news 0; years thin after 2021
  (2022: 9, 2024: 5 against 35 in 2019); Metallurgical Engineering and Materials Science and Chemical Engineering have no rows; CSE
  list is a stale archived copy. Untouched sources: ~70 saved faculty home pages and the 2021-22 to 2024-25 annual reports. A
  supplement agent mines them.
* IIT (ISM) Dhanbad roster accepted (2026-10-28): 755 people (425 current, 181 visiting, 131 former, 15 adjunct, 3 emeritus), 17
  departments; 400 of the 446 people on the site list link to a NIRF-2026 row (NIRF: 508 rows, 469 working); 716 joining years
  (708 from 10 NIRF editions, 8 from pages; automatic reading of profile dates was wrong in 10 of 14 disagreements, so NIRF stands);
  310 ORCIDs (309 offline index). 178 NIRF "Other" people kept as `visiting` (as BHU and Mandi). Gaps: 212 non-listed rows without
  department; no archived department lists for 2018–2021 (site redesign), so people who joined and left between NIRF editions are
  missed; former years ±1; 12 people "working" in NIRF 2026 but not on the site were set former (site list wins), some may just
  be missing from the site; heuristic name clustering may mix histories of repeated names.
* IIT Indore golden set accepted with caveats (2026-10-28): 417 papers (target 450; first pass 171 + supplement 246), 33 high / 384
  medium, 129 authors (max 8). Source mix: faculty pages 44 %, annual reports 34 % (best-three-publications blocks of the
  2018-19 to 2020-21 reports), department pages 14 %, arXiv 8 %, news 0. DOI printed on 11 %. Years: 2020 has 85 rows (only
  2018-19 to 2020-21 reports carry publication lists), 2022 has 23, 2024 25. Chemical Engineering (department founded July 2023)
  has 0 rows: its two lab pages list papers only up to 2024 and both authors joined in 2024. The 2021-22 annual report is an
  image PDF (no OCR); 2022-25 reports give counts and a best-paper table without years. Faculty with a maintained publications
  page are over-represented; HEP/astro collaboration papers under-represented.
* IIT Jammu roster accepted (2026-10-28): 229 people (157 current, 42 visiting, 29 former, 1 adjunct), 12 units; current list from
  the institute's public faculty JSON; 138 of 157 current in NIRF 2026 (142 working, 137 Regular), 19 are 2026 joiners; 95 ORCIDs
  (90 offline index, 5 pages); 155 joining years. Data-quality flag: the NIRF 2026 PDF is image-only and no OCR is installed, so
  the 150-row faculty table (tenure dates, who left) was transcribed by eye; NIRF 2021–2025 PDFs do not exist on the site, so NIRF is
  a single snapshot. Gaps: former faculty who left between Oct 2019 and ~2025 are mostly invisible (no archive after 2019-10);
  10 former rows rest on one annual-report listing; last years for people last seen in 2019 are lower bounds; four NIRF Regular
  people missing from the site kept as current (unconfirmed); two joining-year overrides (Riya Bhowmik 2020, four 2019 visitors).

### 15.12 Why the arXiv pass was slow, and the fix (2026-10-28)
The arXiv stage queries `export.arxiv.org/api/query` once per roster person. It ran as four parallel processes (one per
institute), each pacing itself at 5 s but not coordinated with the others, so arXiv saw ~0.8 requests/s against its stated limit
of 1 request per 3 s and answered 429. `common.get` then backs off exponentially (up to 120 s, 8 tries) *while holding the
pacing lock*, so one throttled query stalled that process for minutes. Measured: ~50 people per 30 min per process; a probe from
this machine was answered 429 within 0.4 s. The `Crawl-delay: 15` in arxiv.org/robots.txt concerns the web site (/abs, /pdf), not the
API, and the pass was already below it for the API; going faster would only have raised the 429 rate and risked blocking the
machine's IP, so no limit was exceeded or relaxed. Fix: `roster_channels.arxiv_gate()` — a machine-wide file-lock gate
(`logs/arxiv_gate`) allowing one in-flight request and ≥ 3.5 s between request starts across all processes — and one serial queue
for the remaining institutes (`pq_master_serial`), started after Bombay's running pass ends. Expected ≈ 1,000 people per hour
against ≈ 100 before. The abandoned passes (Hyderabad 150/558, Kanpur, Gandhinagar) lost their partial progress because the pass
writes its output only at the end.
* IIT Bhilai roster accepted (2026-10-28): 157 people (91 current, 12 former, 48 visiting incl. 42 IIT Hyderabad mentor faculty,
  6 adjunct); 64 ORCIDs (59 offline index); 86 joining years. Current exceeds NIRF 2025 (72 working) by ~20 joiners seen only on 2026
  department pages. Gaps: the live site is dead (SSL), everything is archived; NIRF only for 2023–2025; earliest department pages
  2019-07, so 2016–2018 rests on mentor pages, the 2017-18 annual report and a 2019 directory; former faculty of 2018–2019 probably
  under-counted (ORCID index shows Bhilai employment for people no institute source lists; not added: self-declared dates);
  the mentor page "Jan–June 2016" read as 2017; five adjunct/distinguished professors without department.
* IIT Dharwad roster accepted (2026-10-28): 209 people (96 current, 20 former, 75 visiting incl. 49 IIT Bombay mentor faculty, 18
  adjunct), 10 units; NIRF 2023–2026 PDFs were text-based (nothing hand-transcribed; row counts match the PDFs' own numbering);
  100 current rows link to a NIRF 2026 row (105 regular working in NIRF); 78 ORCIDs (offline index); 123 joining years. Gaps: former
  last years are the last archived appearance (true departure up to a year later); mentor years depend on the 2019–2020 course
  tables; visiting assistant professors and fellows have no joining year; four people current in NIRF 2026 but former on the live site
  were set former (site wins). ALL 40 INPUT FILES NOW EXIST (20 rosters, 20 golden sets); quality tiers per institute are in the
  entries above.
* IIT (BHU) golden set supplemented and accepted (2026-10-28): 543 papers (target 550; first pass 365, supplement 178), 24 high /
  519 medium. Source mix: faculty profile pages 67 %, department/lab pages 14 %, annual reports 14 % (2016-17 to 2023-24 department
  "refereed international journals" lists), arXiv 4 % (PDF prints IIT (BHU) on page 1), news 0 (the institute news page has only
  notices; press articles returned 403, not bypassed). CSE 6 → 65 rows, Electronics 0 → 30, Electrical 1 → 17, Metallurgical 0 → 7;
  Physical AI still empty; 2016–2017 thinnest. Annual-report and department-list rows match authors to the roster by surname +
  initials (unique match, voted department, year after joining), so a few may belong to a same-initial outsider; the per-person cap
  is enforced for roster people only (some arXiv rows are led by students). DOI printed on 23 %.
