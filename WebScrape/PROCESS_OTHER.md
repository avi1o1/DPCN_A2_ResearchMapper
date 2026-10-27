# Publication scrape v2 — other institutes (NITs, universities, IISc/TIFR/IISERs, premier institutes, CSIR, DAE)

Lab notebook of the other-institutes team, kept as `PROCESS.md` §15 is kept: every step, decision, number and incident in
order. Method and rules: `PROCESS.md` (which wins if anything here disagrees) and `handoff/HANDOFF_other_institutes.md`.
Operator: Varun Shastry (with Claude Code). Branch `v2-other` (from `v2-all-institutes`). Outputs: `WebScrape/v2/`.

## 1. Setup (2026-10-27)

* Machine: Windows 11, Git Bash. Separate clone outside OneDrive (`C:\Users\varun\rm_v2`): the run writes several GB of
  caches (`raw/`) and uses file locks, which a synced folder would upload and could interfere with.
* Python 3.12 in a dedicated virtual environment (`requests` installed there). Reason: the agents call the shared fetcher as
  `python3 -I polite_get.py`, and `-I` ignores user-installed packages; a venv's own packages are still visible.
* Environment (handoff §3): `RM_MAILTO=varun.shastry@research.iiit.ac.in` (this machine's contact in every User-Agent),
  `RM_OUT=v2`, `PYTHONUTF8=1` (several scripts open text files without an encoding; Windows would otherwise read the UTF-8
  briefs as cp1252).
* **Shared-script change (separate commit, IIT team informed):** `common.py` (Crossref slot lock) and `agents/polite_get.py`
  (per-host gap lock) used `fcntl`, which does not exist on Windows, so every Crossref call and agent fetch failed at import.
  Both now use `msvcrt` byte-range locks on Windows and the unchanged `fcntl` calls elsewhere. Tests on this machine:
  12 processes competing for Crossref slots -> peak concurrency 3 (34 uses); 4 parallel `polite_get` fetches to one host ->
  ~1 s apart, all HTTP 200; `test_affil.py` 63/63 before any registry change.
* `scripts/recon_probe.py` (new, ours): Crossref hit count 2016–2026 per token plus a sample of real affiliation strings
  containing it; counts appended to `logs/recon_<label>.tsv`.

## 2. Pilot: CSIR-CECRI, Karaikudi (key `csir_cecri`)

Chosen as the pilot (operator decision): a mid-sized CSIR lab with a distinctive name and a realistic trap (Alagappa
University shares its town and PIN codes). The whole procedure is run on it before the CSIR/DAE wave.

### 2.1 Reconnaissance
* ROR `https://ror.org/01qek3q18` (`chosen: true`, score 1.0, active, Karaikudi); names "CSIR-CECRI", "Central
  Electrochemical Research Institute"; GRID `grid.417628.e`; parent Council of Scientific and Industrial Research.
* INSPIRE-HEP: two institution records, "CECRI, Karaikudi" and the legacy "Karaikkudi, CERI" (both queried, as for IIT
  Hyderabad / ISM).
* Units known from the probe strings: Karaikudi campus (PINs 630003 and 630006 both printed by CECRI); Chennai unit in the
  CSIR Madras Complex, Taramani 600113.

### 2.2 Crossref token probes (`query.affiliation`, 2016–2026, `logs/recon_csir_cecri.tsv`)

| Token | Hits | What the sample strings show | Role |
|---|---|---|---|
| Karaikudi | 2,436 | mostly Alagappa University; CECRI | sweep; `city` |
| 630003 | 842 | CECRI and Alagappa University | sweep; `city` |
| 630006 | 110 | CECRI and Alagappa University | sweep; `city` |
| CECRI | 551 | CECRI, often without any place ("CSIR-CECRI , , , ,") | sweep; name counts on its own (`units`) |
| Karaikkudi / Karikudi | 2 / 4 | CECRI / Alagappa spelling variants | sweep; `city` |
| Karaikudy | 0 | — | rejected |
| Taramani | 599 | CSIR Madras Complex (SERC, CEERI centre, CECRI Chennai unit), University of Madras, IMSc | sweep; `shared` |
| 600113 | 712 | IMSc, SERC, AcSIR, IIT Madras HTIC, MSSRF, VHS hospital, CECRI Chennai unit | sweep; `shared` |
| Mandapam | 61 | ICAR-CMFRI, fisheries; (CSIR-CSMCRI has a station there) | sweep; `shared` |
| Tuticorin / Thoothukudi | 177 / 486 | colleges, CMFRI, medical college | sweep; `shared` |

No token is unique to the CECRI campus, so `anchor` is empty: the department-only rule is never applied to CECRI.

### 2.3 Registry entry and rules (`scripts/institutes_other.py`, tests in `scripts/test_affil_cases_other.tsv`)
* Family `csir`; type mention `\bcsir\b | Council of Scientific and Industrial Research`. AcSIR is not a mention ("AcSIR" has
  no word boundary before "csir") and names no place: AcSIR alone counts for no lab; AcSIR + "CECRI" counts through the name.
* The lab's name (typo-tolerant: "Electro Chemical", "Reseach Inst.") and "CECRI" count without a place.
* `city` (no lab name -> at most `uncertain`): Karaikudi and variants, 630003, 630006, the e-mail domain (scope only).
* `shared` (in scope only with a CSIR mention): Taramani, 600113, Mandapam, Tuticorin, Thoothukudi.
* `confusable`: "Madras Complex", "Mandapam" — a bare "CSIR" there is ambiguous between labs -> `uncertain`.
* `exclude` (never CECRI, checked before the mention rule): SERC, CLRI, CEERI, CSMCRI, IMSc, University of Madras.
* `other`: Alagappa University and colleges of Karaikudi, CMFRI and fisheries bodies, plus the IIT team's generic list
  (`institutes.GENERIC_OTHER`: universities, colleges, hospitals, companies, IISERs, NITs ...).
* No state rule: Tamil Nadu has several CSIR labs.
* `test_affil.py`: 78/78 (63 IIT cases unchanged + 15 CECRI cases). Mirror note: CECRI's explicit name now also takes part
  in the IIT entries' "another institute named explicitly" check; no IIT case changed.

### 2.4 Harvest and classifier review (2026-10-27)
* Harvest (`scripts/run_harvest_other.sh`, our queue runner: Crossref sweeps 3 at a time, the other channels in parallel, every
  job under `timeout 2h`, ORCID retried from its checkpoint): Europe PMC 689 records, DOAJ 160, INSPIRE 0 (no CECRI papers in
  INSPIRE — expected for an electrochemistry lab), DBLP 1 person / 0 papers 2016–2026, ORCID 555 profiles, 11 Crossref sweeps.
  Incident: the first Crossref run failed instantly — on Windows Python wrote the token list with CRLF, so every token
  carried a `\r` (invalid cache file name). Runner fixed (`tr -d '\r'`), sweeps re-run; nothing else affected.
* Review aid added: `scripts/review_notexplicit.py` lists strings classified as the institute **without** its explicit name.
  `review_strings.py`'s `iitnoname` covers only verdicts without any type mention; for CSIR a bare "CSIR" + a place is the
  riskiest verdict and is not in that list.
* First review: 1,502 distinct strings classified CECRI, 71 of them without the name. ~65 were false positives: the CSIR
  Campus, CSIR Road, Taramani 600113 is AcSIR's old head office ("Training and Development Complex") and hosts CSIR-NML's
  Madras Centre, CSIR-CSIO's Chennai Centre, CSIR-NEERI's zonal lab and the National Biodiversity Authority; CSIR authors
  of NCL Pune, IICT Hyderabad, CDRI Lucknow, IGIB Delhi, IIP Dehradun, CMERI Durgapur, NPL Delhi print AcSIR's Taramani
  address next to their lab ("CSIR-NCL Pune | AcSIR, Chennai 600113"), and the whole-string rescue credited them to CECRI.
  Decisions:
  1. Taramani, 600113, Mandapam, Tuticorin, Thoothukudi are **sweep tokens only** (`shared=None`): a string there counts
     only if it names CECRI. The Chennai unit always prints the name in the strings seen.
  2. `confusable` = "another CSIR lab is named" (`CSIR_OTHER_LAB`: "CSIR-<lab>" for any lab other than this one, and the names
     and abbreviations of the CSIR labs and centres): a bare CSIR mention plus our place is then not decisive. Reused for
     every CSIR entry of the wave.
  3. Typos of the name in Karaikudi ("Electrochemcial", "Research Centre", "CSIR-Electrochemical Research Institute",
     "CSIR-CERCI") count through CSIR + Karaikudi (CECRI is the only CSIR lab there); "CERCI" is exempted from decision 2.
  4. CECRI's electrochemistry divisions (electro-organic, electrochemical power / process / materials, materials
     electrochemistry, electrodics, corrosion and materials protection) count together with Karaikudi / 630003 / 630006: no
     other electrochemistry division exists in Karaikudi (Alagappa University has bioelectronics, chemistry, industrial
     chemistry departments; they stay `other`).
  5. `other` additions: Universidad del Quindío, Armenia, Colombia (postcode 630003), BioMe Live Analytical Centre (private
     lab), KIT & KIM Technical Campus, ACCET, Karunya, GCE Srirangam, Kumaragiri (Salem), MAVMM School of Management.
  6. Kept `uncertain`: "AcSIR, Karaikudi 630003" (AcSIR without a lab named counts for no lab, handoff §6, even where only one
     lab exists), "Center for Education, Karaikudi" (CECRI has a Centre for Education, but so do colleges), bare places.
* After the review: 1,439 distinct strings CECRI (7,107 author slots), 1,365 other, 4 uncertain (10 slots); 8 CECRI verdicts
  without the explicit name, all read and genuine (typos, one division string). Checks: all `other` strings mentioning
  "electro" are Alagappa University (bioelectronics) or Alagappa's engineering college; no `other` string mentions CSIR;
  a random sample of 25 CECRI strings (seed 20261027) is 25/25 correct. `test_affil.py` 89/89 (63 IIT + 26 CECRI).

### 2.5 First pipeline pass (`sh run_v2.sh merge csir_cecri`, 2026-10-27, no rosters yet)
* Candidates 3,026 (2,761 with DOI) -> DOI resolution by exact title: 67 of 265 DOI-less resolved -> 2,992 candidates.
  Evidence: aff:crossref 1,216, aff:europepmc 664, aff:doaj 152, orcid_tenure 1,938, orcid_untimed 378, aff_uncertain 2.
  Rejected affiliation strings: Crossref other organisation 1,781 (mostly Alagappa University), Europe PMC 25, DOAJ 8.
* `v2/csir_cecri.json`: **2,226 records** (1,583 verified, 642 unverified-likely); 494 moved to the unconfirmed file;
  242 person-channel records rejected as contradicted by the deposited affiliation; 12 out of window. Per year 159–234;
  journal 2,092, book chapter 56, conference 44, preprint 11, book 6, other 9, type TODO 8.
* TODO fields: affiliation 643 (the likely tier), references 122, authors 23, ISSN 17, DOI 15, citations 15, type 8, venue 6.
* Not yet run: roster channels, arXiv pass, Europe PMC / Springer verification, TODO resolution, OpenCitations, recall,
  precision audit, validation (they need the roster and golden set, being built by the agents).

### 2.6 Independent output check and the "CECRI" acronym collision (2026-10-27)
* Operator requirement: no wrong or fabricated data. Before any further stage, 30 random verified records (seed 20261027)
  were re-fetched live from Crossref. Diagnosis of every non-match: matched strings did contain CECRI (the quick check had
  printed the first Karaikudi string of an author list that also had Alagappa authors), Europe PMC- / DOAJ-only evidence
  (no affiliations deposited in Crossref) — and **one false positive**: 10.1701/4669.46825, an Italian wound-care paper,
  matched through "Centre of Excellence for Nursing Scholarship (**CECRI**), Board of Nursing (OPI) of Rome".
* Scan of every harvested string containing "CECRI": the acronym also belongs to Rome's nursing centre, the "CECRI
  Evidence-Based Practice Group for Nursing Scholarship" (JBI group) and a Milan nursing centre (San Raffaele) — all
  arrived through the Europe PMC query `AFF:"CECRI"`.
* Fix: `CECRI_NAME` — the full name counts alone; the acronym "CECRI" only with a CECRI context word in the same part
  (CSIR, electro…, Karaikudi, Chennai, Madras, Tamil, India); the Italian nursing names in `exclude`. Test case added.
  Cost: one string consisting of only "CECRI" no longer counts.
* Re-run (`run_v2.sh merge csir_cecri`): **2,193 records (1,550 verified, 642 likely)**; the verified count fell by 33 — all
  33 were Italian nursing papers. Strings containing "CECRI" that do not count (73 distinct): Italian nursing bodies,
  "AcSIR + …@cecri.res.in" (e-mail is not affiliation evidence, AcSIR alone names no lab: `uncertain`), Texas A&M + CECRI
  e-mail (`other`), the bare "CECRI". No CECRI affiliation is lost.
* New output check `scripts/review_verified_noname.py`: verified records none of whose matched strings name the institute.
  CECRI: 9 of 1,550, all read and genuine (name typos, "CSIR-CERCI", a division with Karaikudi).
* Fresh live check after the fix: 30 random verified records (seed 271026) — **30/30 confirmed**: CECRI affiliation printed
  in Crossref (25), Europe PMC (3) or DOAJ (2), title and year matching.

### 2.7 Verification of the agent outputs (2026-10-27, `agents/verify_agent_outputs.py`)
* Seeded sample (20 roster rows, 10 ORCIDs, 20 golden rows, seed 20261027); every cited source re-fetched.
* First run during a network outage: all ORCID look-ups `DEAD:ConnectionError` (not data errors). Verifier changes: a failed
  fetch is retried with `--refresh`; PDFs with < 80 words per page count as image-only (`IMAGE`, visual check by the
  operator); a golden row whose page cannot be text-checked is looked up in Crossref (title overlap ≥ 0.9 both ways,
  |year| ≤ 1) and a failed look-up is reported as `LOOKUP-FAILED`, never as "does not exist".
* CECRI's 2022–23 annual report (cited by the roster) is a 272 MB PDF; the shared fetcher has no total-time limit, so it was
  downloaded once with curl for the check. (open: result of the re-run)
* Brief issues seen on the pilot: golden set has no repository `evidence_source` (use `dept_page` + note); image-only
  annual reports (transcription risk for long chemical names); roster: two people named "S Mohan"; CLRI directors holding
  CECRI's additional charge listed as `former`.

## 3. Wave 1: CSIR and DAE labs

Agents (2026-10-27): recon drafts for all 22 remaining labs were started, then stopped (operator: fewer parallel agents
because of usage limits). Token counts of all 22 labs are in `logs/recon_<key>.tsv`; only the IICT draft was written.

### 3.1 CSIR-IICT, Hyderabad (key `csir_iict`)
* ROR 040dky007 (GRID grid.417636.1, checked against the ROR record); no INSPIRE institution record.
* Crossref token counts 2016–2026: IICT 950, Tarnaka 729, 500607 50, Habsiguda 98, 500007 2,535, Uppal 907.
  Sample strings (operator's own probe, `rm_v2_work/review/iict_probe.txt`): "IICT" is mostly DA-IICT Gandhinagar, also
  SUST (Bangladesh); Tarnaka is shared with Osmania University and Sarojini Naidu Vanita Pharmacy college; Habsiguda /
  Uppal Road / 500007 with CSIR-CCMB, CSIR-NGRI, ICMR-NIN, Osmania, Anand Eye Institute and Uppal colleges
  (Keshav Memorial, Neil Gogte, Drugparadigm); 500607 is IICT's own PIN misprint.
* Rules: the full name counts alone; "IICT" only with a Hyderabad / CSIR / Tarnaka / Uppal / Habsiguda / PIN / RMIT context
  in the same part and never after "DA-"; Tarnaka and 500607 are `city` (with a CSIR mention -> IICT, without -> uncertain);
  Habsiguda / Uppal / 500007 are sweep tokens only (`shared=None`, as Taramani for CECRI); confusable = CSIR_OTHER_LAB with
  IICT's own fragments removed. Changes to the agent draft: ICT Mumbai's name in `exclude` tied to its places (a bare
  "institute of chemical technology" also occurs inside IICT's name); `heig` -> `\bheig\b` (matched "height").
* All 129 probe strings classified and read: IICT strings `iit`, Osmania / pharmacy college `other`, CCMB, NGRI, NIN,
  DA-IICT, SUST, Uppal colleges not counted; CECRI's verdicts unchanged. "CSIR-Indian Institute of Technology, Tarnaka" is
  counted (a typo of IICT: there is no IIT at Tarnaka). 16 test cases; test_affil 106/106.
* Harvest (2026-10-27, `run_harvest_other.sh csir_iict`): all Crossref tokens, Europe PMC, DOAJ, DBLP, ORCID done; INSPIRE
  exits 1 by design (no INSPIRE institution).
* Classifier review (`review_strings.py`): 2,963 distinct strings `iit` (11,617 occurrences), 107 `other`, 9 `uncertain`.
  Note: strings containing line breaks span several lines of the review TSV; read them with a parser that joins lines up to
  the `\t<count>\t<dois>` ending (a line-by-line read shows false "fragments").
  - All 9 uncertain read: Tarnaka residents, clinics, "Indian Institute of Technology, Hyderabad, Tarnaka", NEERI — none IICT.
  - Top 40 other read: Osmania University, ICMR-NIN, CSIR-CCMB ("Uppal Road, IICT Colony, Habsiguda" is CCMB's address),
    the Tarnaka pharmacy college — all correct.
  - All 10 `iit` strings without an explicit name read: the "CSIR-Indian Institute of Technology, Uppal Road, Tarnaka"
    typo of IICT's Applied Biology division — correct.
  - All 107 acronym-only `iit` strings read: genuine IICT, except **CSIR-NEERI's Hyderabad Zonal Centre, whose address is
    "IICT Campus, Tarnaka"** (7 strings): false positive. Fix: NEERI in `exclude` (per part, so an IICT co-author in a
    separate entry still counts). Re-classification: exactly those 7 strings changed. Every `iit` string naming another
    Hyderabad lab (18) read: the other 11 have IICT and NEERI-Nagpur / CCMB as separate entries — correct.
  - 3 test cases added; test_affil 110/110.
