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
  downloaded once with curl (resumed, full Content-Length) and placed in the shared cache under the fetcher's key.
* Result (re-run with the network up): roster names 17 found on the cited page + 3 in image-only PDFs, each checked by the
  operator: KJ Sreeram (Director's message of AR 2022–23, p.7, signed "डॉ. के. जे. श्रीराम"; ORCID: CECRI Director 2022-08 to
  2023-04), Harshal Agarwal (CECRI profile page, Chennai unit), R Mayandi (AR 2017–18 p.192, "New Appointments") — 20/20.
  ORCIDs 10/10 (name matches, employment names CECRI). Golden titles 10 found on the cited page + 10 on image-only report
  pages, all 10 found in Crossref with the same title and year — 0 problems. Roster and golden set accepted.
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
* Recall gap found after the first pass (5,232 records, 4,029 verified): strings printing only "Indian Institute of Chemical
  Technology, Hyderabad" contain none of the campus tokens. Added Hyderabad (62,988 hits), Hyderbad, Hydrabad, Hyderabd,
  Secunderabad as sweep-only tokens (`shared=None`: they never count without IICT's name). The Hyderabad file
  (`raw/crossref_aff/Hyderabad.light.jsonl.gz`) is shared with CCMB and later UoH.
* Incident: the operator's session restarted at ~10:48 and killed the background jobs (CECRI `final` at 100/156 roster
  names, the Hyderabad sweep at 33,000/62,988; crossref_aff has no resume, the `.part` file was restarted). Long jobs are
  now started as detached processes (`Start-Process bash <script>`), scripts in `rm_v2_work/run_*.sh`.

### 3.2 CSIR-CCMB, Hyderabad (key `csir_ccmb`)
* Agent draft (recon brief) reviewed by the operator: ROR 05shq4n12 / grid.417634.3 checked; all 29 test strings found in the
  agent's probe output (28) or in the existing test file (1).
* Name and "CCMB" count only with a CCMB context word in the same part (Cologne, CancerCare Manitoba, Brown, Bahia use
  "CCMB"; Deakin and Amity print "Centre for Cellular and Molecular Biology"). LaCONES counts alone (11 hits, all CCMB).
  AIC-CCMB (incubator hosted by CCMB) -> uncertain. 500048 (LaCONES, shared with ZSI / BSI) is `city`.
* Operator changes to the draft: (1) `exclude` had `\biict\b`, which would drop CCMB's own address "Uppal Road, IICT Colony,
  Habsiguda" (seen 12× in the IICT review) -> `\biict\b(?!\s*colony)`, test case added for both labs; (2) Hyderabad +
  misspellings as sweep-only tokens (the agent's open question on strings with only "CCMB, Hyderabad"); (3) Europe PMC
  query bracketed (AND/OR precedence); (4) NEERI added to `exclude` (mirror of IICT).
* With CCMB registered, every reviewed IICT string was re-classified: 0 changes. test_affil 141/141.

### 3.3 CSIR-NCL, Pune (key `csir_ncl`)
* Agent draft reviewed: ROR 057mn3690 / grid.417643.3 checked; all 27 test strings found in the probe output or test file; no
  IIT entry mentions NCL.
* Full name counts alone; "NCL" only with CSIR / Pune / Pashan / Homi Bhabha Road / 411008 context and never in "NCL
  Innovation Park / Venture Center / Colony" (tenants, C-DAC, IISER print them). Pashan, 411008, Homi Bhabha Road are `city`
  (IISER Pune, IITM, C-MET, C-DAC, NCCS share them -> `exclude`). "Pune" is not a place (CSIR-URDIP, AcSIR's HRDC campus).
* Operator changes: Pune (51,761 hits) and Poona (542) as sweep-only tokens (same recall gap as IICT); NEERI in `exclude`.
  test_affil 168/168.

### 3.4–3.10 CFTRI, NIIST, SERC, NPL, CRRI, IGIB, CDRI (agent drafts, operator review 2026-10-27)
Every draft passed `agents/check_draft.py` before merging: ROR id resolves and its GRID equals the draft's; every test string
is found in the agent's own probe output or an existing test file (0 missing in all seven); the full test suite passes with
the draft merged into a temporary copy of the registry. Merged with `agents/merge_draft.py <key> <section>`. Then the
operator read every `exclude` / `other` / place rule. Summary per lab (details in the agents' `<key>_recon.md`, kept in
`rm_v2_work/registry_drafts/`):
* **3.4 CFTRI** (01d7fn555): "CFTRI" is unique (189 hits, all CFTRI) and counts alone; 570020 / Cheluvamba Mansion `city`
  (shared with JSS, PHRII); Mysuru / Mysore sweep-only. Collision: Ghana's CSIR Food Research Institute — Ghana / Accra /
  South Africa in `exclude`. Accepted unchanged.
* **3.5 NIIST** (05bkc5375): "NIIST" also = NRI Institution of Information Science & Technology, Bhopal -> acronym needs
  CSIR / Kerala context; Pappanamcode / 695019 `city`; Thiruvananthapuram / Trivandrum sweep-only. Accepted unchanged.
* **3.6 SERC** (00pyevk91): "SERC" has many owners (IIIT Hyderabad, VIT, Stevens, South Wales, Chile ...) -> counts only as
  "CSIR-SERC" or with CSIR + a Chennai place; the full name needs CSIR / Chennai / India context (IIEES Tehran, Shandong, TU
  Wien). Taramani / 600113 sweep-only as for CECRI. **Operator change:** removed `steel structures` and `geotechnical` from
  `exclude` — the agent's own recon lists a Steel Structures Laboratory among SERC's divisions; TU Wien and Shandong are
  excluded by name.
* **3.7 NPL** (0307k1x46; ROR's affiliation matcher picks the UK NPL — id used directly): name / acronym only with CSIR / India
  / Delhi / PIN context (UK NPL Teddington, UBC, Toulouse ...); 110012 `shared`; K.S. Krishnan Marg `city`; CSIR-NIScPR /
  NISTADS (same street and PIN) excluded. **Operator changes:** Delhi (106,963 hits) sweep-only; ICAR / IARI moved into
  `exclude` (they share 110012, and `other` is checked only after the CSIR-mention rule, so "CSIR, ICAR-IARI ... 110012"
  would have counted). Open: ~100 strings "National Physical Laboratory (NPL)" without a place stay None.
* **3.8 CRRI** (01pdb1x94): "CRRI" mostly = Compulsory Rotatory Residential Internship (TN dental / medical) and ICAR-NRRI
  "formerly CRRI" -> excluded; division names are `units`; an AcSIR part naming CRRI without a CRRI staff word -> `other`
  (other labs' authors print AcSIR's Delhi office in CRRI's campus). **Operator change:** Delhi sweep-only.
* **3.9 IGIB** (05ef28661): both campuses (Mall Road 110007, shared with University of Delhi -> `shared`; Sukhdev Vihar ->
  `city`); TRISUTRA / INGEN-HOPE units; old name Centre for Biochemical Technology with context. **Operator change:** Delhi
  sweep-only. Test expectation changed: "CSIR-NPL ... | University of Delhi" is now None for IGIB (NPL registered).
* **3.10 CDRI** (04t8qjg16): Jankipuram / 226031 `city` (AKTU's Centre for Advanced Studies, Biotech Park share them);
  Lucknow sweep-only; CSIR-NBRI / IITR / CIMAP excluded; "CDRI" collisions (Cambodia, Korea CBRN, Coalition for Disaster
  Resilient Infrastructure, Karachi) need context. Accepted unchanged.
* Incident: a shell heredoc turned `\b` into backspace characters in the NPL draft; found by inspecting the bytes, fixed, all
  drafts and repository files checked for control characters (0).
* All registered: 11 CSIR labs, test_affil 348/348.
* `run_harvest_other.sh`: a token already swept today is reused (SKIP in the log), a token being swept by another job is waited
  for; FORCE=1 re-sweeps. Saves repeated Delhi / Hyderabad / 500007 sweeps.

### 3.11–3.19 IMTECH, CSIO, CBRI, CEERI, AMPRI, CGCRI, NML, CMERI, CIMFR (agent drafts, operator review 2026-10-27)
Same procedure (`check_draft.py` -> operator reading -> `merge_draft.py`); 0 test strings missing in all nine (three IMTECH
mirror strings were in the CSIO probe file: the checker now searches every probe file). ROR / GRID checked for each:
IMTECH 055rjs771, CSIO 04bfs6764, CBRI 03gjr0792, CEERI 01hh45364, AMPRI 02x351n42, CGCRI 039d1mp60, NML 0211zmf46,
CMERI 059h0ng81, CIMFR 03vkfy293. Bare cities are sweep-only (Chandigarh, Roorkee, Pilani, Bhopal, Kolkata / Calcutta,
Jamshedpur via `city`, Durgapur via `city`, Dhanbad `shared`, Nagpur / Bilaspur for CIMFR's regional centres).
* **Rule-order finding (applies to every lab with a `city` / `shared` token):** `other` is consulted only after the
  CSIR-mention rule, so a neighbour that shares the place token and prints "CSIR" (a CSIR fellowship, a collaboration)
  would be counted. Neighbours of that kind moved to `exclude`: CSIO / IMTECH — GMCH-32, TBRL, PGIMER, DGRE (share
  160030 / 160036); CGCRI — Jadavpur University; CMERI — NIT Durgapur (same street and PIN); NML — Tata Steel, NIT
  Jamshedpur, XLRI. For CGCRI / CMERI / NML the exclusion is guarded (`^(?![\s\S]*<lab name>)...`) so a joint string that
  also names the lab still counts. Checked: "NIT Durgapur ... Council of Scientific and Industrial Research ... 713209" ->
  other; "CSIR-CGCRI and Jadavpur University, 700032" -> CGCRI. IIT (ISM) needs no exclusion for CIMFR: it is a registered
  institute, so the classifier's "another institute named" step already handles it.
* IMTECH: "Microbial" (35,590 hits, half Shandong University's Institute of Microbial Technology) dropped as a sweep token —
  the Chandigarh sweep reaches "<name>, Chandigarh".
* CIMFR: Digwadih, 828108, 826015, Barwa Road are `anchor` (complete scans of their hits: only CIMFR). Old names CMRI / CFRI
  count only with Dhanbad context (CMRI = China Mobile RI, Sydney Children's MRI; CFRI = China Fire and Rescue ...).
* Incident (again): `\b` became a backspace character when a Python non-raw string was used in a shell heredoc (CSIO / IMTECH
  exclude). Effect: those alternatives could never match (no wrong data). Fixed; every edit is now followed by a
  control-character check; raw strings only.
* All 20 CSIR labs of the handoff registered; test_affil 592/592.

### 3.20 The rule-order finding applied to the earlier entries
* The six entries merged before §3.11 had the same exposure: a neighbour sharing a `city` / `shared` token, listed only in
  `other`. New helper `_unless_named(name, neighbours)` in institutes_other.py (excluded unless the same part names the lab);
  applied by `scripts/oneoff_apply_unless_named.py` to CECRI (Alagappa University and Karaikudi colleges), IICT (Osmania,
  Sarojini Naidu pharmacy college, NIPER), CCMB (ZSI, BSI at 500048), CFTRI (JSS, PHRII), CDRI (AKTU and Jankipuram
  neighbours), IGIB (University of Delhi and colleges at 110007).
* Test run found one real problem in the new guard: CECRI's own locality is "**Alagappa**puram, Karaikudi", and a CECRI string
  with a misspelled name ("Electrochemcial") was excluded -> `alagappa(?!puram)`. Three IGIB test expectations None -> other
  (University of Delhi strings; both mean "not IGIB"). test_affil 592/592.
* Effect on real data: every reviewed IICT `iit` string (2,963) and every matched string of CECRI's 1,568 verified records
  re-classified — **0 changes**. The guards close a possible error; no observed record depended on it.
* Golden set (agent, 2026-10-27): 400 rows, but iict.res.in does not answer from this machine (operator check: every variant
  times out after 21 s), so the agent used Wayback copies: 392 rows from the IICT Biennial Report 2018-20 (sampled evenly
  through the institute-wide list of 2018 and 2019, no authors printed), 8 from one scientist's own page. 0 DOIs. Earlier /
  later reports came back truncated from Wayback. Verification: check_outputs passes (warning: 387 rows without an author
  name — expected, the report prints none); verify_agent_outputs 25/25 titles found on the cited pages. **Accepted as a
  partial benchmark: recall for IICT is reported for 2018–2019 only.** A re-run is needed if the site becomes reachable.

## 4. DAE units (agent drafts, operator review 2026-10-27)
Shared patterns (in the BARC draft, merged first): `DAE_MENTION` = "Department of Atomic Energy" + a guarded `\bdae\b`
(of 993 distinct Crossref strings with "DAE": ~600 UGC-DAE CSR, ~300 Korean "Dae-jeon / Dae-gu", the rest Bangladesh DAE,
Brazil); `HBNI_ONLY` (HBNI, the DAE's university, names no unit — like AcSIR); `DAE_OTHER_UNIT`. Out of scope and never
claimed: TMC / ACTREC, UGC-DAE CSR, TIFR, AERB, NPCIL, BRIT, Heavy Water Board, IOP, BHAVINI.
* **4.1 BARC** (05w6wfp17): name / "BARC" with context (the acronym also = USDA Beltsville ARC, Copenhagen, Barts,
  Bangladesh, "bARC" Australian Research Council ...); all BARC outstations (Vizag, BARCF Kalpakkam, Tarapur, NCCCM) and
  BARC Hospital count (operator: hospital is a BARC unit). Sweeps: BARC, Trombay, 400085, Anushaktinagar, Anushakti, 400094,
  Bhabha (14,912 — reaches name-only strings); Mumbai / Bombay / Atomic not swept (BARC strings print the name, Trombay or a
  PIN). **Operator change:** the draft placed "DAE mention + Anushaktinagar / 400094" at BARC (`shared`); a test showed
  "HBNI, Anushaktinagar, 400094, Department of Atomic Energy" counted as BARC. Anushaktinagar also holds AERB, NPCIL, the
  Heavy Water Board, all DAE -> `shared=None` (count only if BARC is named). Three test expectations other -> None; a real
  AERB + HBNI probe string added as a test. (A constructed test string was added first and replaced by the real one — test
  strings stay real.)
* **4.2 IGCAR** (05tkzma19): Kalpakkam / 603102 / 603127 `city`; BARCF, AERB-SRI, BHAVINI, NPCIL, the UGC-DAE node excluded
  unless IGCAR is named; Indira (7,633) swept for name-only strings; Chennai not swept. Checked: "Department of Atomic Energy,
  BHAVINI, Kalpakkam 603102" -> other.
* **4.3 RRCAT** (02378jc90): 452013 `anchor` (508 of 515 distinct strings name RRCAT; the other 7 checked: a BARC string with a
  wrong PIN, UGC-DAE CSR — both handled by name / exclude); "Raja Ramanna Fellow / Chair" (a DAE fellowship held anywhere)
  excluded from the name; Indore sweep-only. BARC beamline staff at RRCAT count for both (both printed).
* **4.4 NISER** (02r2k1c68): Jatni campus (752050, Padanpur `anchor`: 0 of 167 strings lack the name) and the transit campus
  at IOP (751005); "NISER" also = Nigerian / Nepal institutes -> acronym needs Bhubaneswar / Odisha / HBNI context; IIT
  Bhubaneswar, IOP, XIM, Centurion excluded unless NISER is named; Bhubaneswar (23,787) sweep-only. Checked: an IOP + HBNI +
  DAE string at 751005 -> other.
* All 24 CSIR + DAE units registered; test_affil 717/717. ROR / GRID checked for all four; 118 test strings, 0 missing.
