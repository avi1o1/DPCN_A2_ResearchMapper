# Publication Scrape (IIITs): Process & Decision Log

Project: DPCN Research Mapping 2026, v2 all-institutes run, **IIIT part** (course brief Groups 9–11).
Institutions: IIIT Hyderabad, IIIT Delhi, IIIT Allahabad, IIIT Bangalore, ABV-IIITM Gwalior, PDPM IIITDM Jabalpur, IIIT Pune,
IIITDM Kancheepuram.
Window: publications dated **2016-01-01 … 2026-12-31**.
Operator: Arihant Tripathy (with Claude Code as research assistant). Handoff from the IIT team (Aviral Gupta), 2026-10-26:
[`handoff/HANDOFF_IIITs.md`](handoff/HANDOFF_IIITs.md).

This notebook follows [PROCESS.md](PROCESS.md) §15, which is the specification for the method. Only IIIT-specific decisions,
numbers and incidents are recorded here, in chronological order. Where this file and PROCESS.md disagree, PROCESS.md wins.

---

## 0. Setup (2026-10-26/27)

* Branch `v2-iiit`, made from `origin/v2-all-institutes` at 8c0fe2e. All outputs go to `WebScrape/v2/` (`RM_OUT=v2`).
  Without `RM_OUT`, `common.OUT` is `WebScrape/`, where the v1 files live.
* Machine: Windows 11 with Git Bash, unlike the IIT team's Linux machine. Python 3.12.13 runs in a uv venv (`~/.venvs/rm`, with
  `requests`), because the system Python 3.14 is externally managed. A `python3.exe` copy in the venv lets the shell scripts'
  `python3` calls resolve to it. Every command runs with `PATH=~/.venvs/rm/Scripts:$PATH`, `PYTHONUTF8=1` (the shared scripts
  open text files without an encoding, so Windows would otherwise use cp1252), `RM_OUT=v2` and `RM_MAILTO=<operator address>`.
  `pdftotext` comes from Git Bash's mingw64. git's `core.autocrlf=true` normalises line endings on commit.
* `test_affil.py`: 63/63 before any IIIT change.
* **Shared-code change** (commit 5a8ebda, reported to the IIT team): `common.py` (Crossref concurrency slots) and
  `agents/polite_get.py` (per-host gap) used `fcntl`, which does not exist on Windows, so every Crossref call and every agent fetch
  failed. When `fcntl` is missing, both now fall back to `msvcrt` byte-range locks with the same semantics. The `fcntl` path is
  the same as before, so IIT behaviour on Linux does not change. Tested on Windows: 12 parallel callers reached a peak of 3
  Crossref slots, and 6 parallel `polite_get` fetches to one host took 6.9 s (the 1 s gap held). The operator chose this
  route over installing WSL.
* Not available in Git Bash: `pgrep` and `bc`. The watchdog runners (`raw/run_*.sh`) need Windows equivalents (§ to follow).

## 1. Source reconnaissance (2026-10-27)

### 1.1 ROR
ROR v2 `affiliation=<official name>` returned a `chosen: true` record for five of the eight. For the other three, the top
(unchosen) match was **a different organisation**: IIIT Hyderabad matched *IIIT Naya Raipur*, IIITDM Jabalpur matched the
*Institute of Information Technology, Hanoi*, and IIIT Pune matched the *Institute of Information Technology, Baku*. Their ids
were taken from ROR `query=` searches and checked against name, city and website.

| key | ROR | GRID | est. | route | ROR names worth noting |
|---|---|---|---|---|---|
| iiit_hyderabad | https://ror.org/05f11g639 | grid.419361.8 | 1998 | query | alias "IIIT" (bare; also IIIT Naya Raipur, the Herndon *Islamic Thought* institute) |
| iiit_delhi | https://ror.org/03vfp4g33 | grid.454294.a | 2008 | chosen | IIIT-D |
| iiit_allahabad | https://ror.org/03rgjt374 | grid.417946.9 | 1999 | chosen | IIIT-A |
| iiit_bangalore | https://ror.org/05h9eqy10 | grid.435284.c | 1999 | chosen | IIIT-B |
| iiit_gwalior | https://ror.org/008b3ap06 | grid.444426.4 | 1997 | chosen | ABV-IIITM; "Indian Institute of Information Technology and Management, Gwalior" |
| iiit_jabalpur | https://ror.org/00gmd7q80 | grid.444467.1 | 2005 | query | alias "IIITDM" (shared with Kancheepuram and Kurnool) |
| iiit_pune | https://ror.org/01f8qyw75 | grid.503420.0 | 2016 | query | IIITP |
| iiit_kancheepuram | https://ror.org/023c9pb11 | grid.504246.1 | 2007 | chosen | alias "IIITDM" (shared, see above) |

As with the IITs, ROR aliases are never used as match strings ("IIIT" and "IIITDM" each name several institutes).

### 1.2 INSPIRE-HEP institutions
* IIIT Hyderabad: `Hyderabad, IIIT` (194 papers; address "Gachibowli, Hyderabad 500 046").
* IIIT Allahabad: `IIIT, Allahabad` (39 papers; "Devghat, Jhalwa, 211015").
* **`Pune, IIIT` is not IIIT Pune**: it is the private *International Institute of Information Technology (I²IT)*, Hinjawadi,
  Pune 411057 (isquareit.ac.in). IIIT Pune therefore has no INSPIRE record.
* No record: IIIT Delhi, IIIT Bangalore, ABV-IIITM Gwalior, IIITDM Jabalpur, IIITDM Kancheepuram (searched by name, city and
  abbreviation).

### 1.3 Crossref hit counts (`query.affiliation=<token>`, 2016-01-01…2026-12-31, `rows=0`)

| institute | token: hits |
|---|---|
| IIIT Hyderabad | Hyderabad 62,984 · Gachibowli 869 · 500032 529 · IIITH 20 · Telangana 33,205 |
| IIIT Delhi | Indraprastha 3,622 · Okhla 346 · 110020 438 · IIITD 110 · (IIIT-Delhi 110,174 = OR-search on "IIIT"/"Delhi", unusable) |
| IIIT Allahabad | Allahabad 6,411 · Prayagraj 4,627 · Jhalwa 80 · Deoghat 12 · Devghat 12 · 211015 193 · 211012 111 · IIITA 18 |
| IIIT Bangalore | Bangalore 51,283 · Bengaluru 45,061 · 560100 402 · IIITB 58 · (Electronic 326,560, unusable) |
| ABV-IIITM Gwalior | Gwalior 4,245 · 474015 114 · IIITM 416 · ABV-IIITM 830 · ABV 740 |
| IIITDM Jabalpur | Jabalpur 3,151 · 482005 233 · Dumna 30 · IIITDM 727 (shared) · PDPM 770 · IIITDMJ 28 |
| IIIT Pune | Pune 51,759 · IIITP 1 · Ambegaon 35 · 411041 162 · Talegaon 272 · Nanded 891 (also the city of Nanded) |
| IIITDM Kancheepuram | Kancheepuram 1,360 · Kanchipuram 1,059 · Melakottaiyur 19 · 600127 1,175 · Vandalur 378 · IIITDM 727 (shared) · Kelambakkam 1,171 |

### 1.4 PINs and strings printed next to an IIIT name (Crossref sample, ≤ 400 records per token)
PINs found in strings that mention "Information Technology"/"IIIT" together with the city token (most frequent first):
Hyderabad 500032 (133); Delhi 110020 (672); Allahabad 211015 (332), 211012 (133); Bangalore 560100 (112); Gwalior 474015 (386);
Jabalpur 482005 (836); Kancheepuram 600127 (292); Pune 411041 (4), 411048 (2), 412109 (1).

Look-alikes found in the same samples (to become `other` / `confusable` entries and test cases):
* Hyderabad: "Department of Information Technology" of local engineering colleges (MLR, Vardhaman, GNITS, CBIT …) has the
  highest frequency of all.
* Pune: Vishwakarma Institute of (Information) Technology, AISSMS Institute of Information Technology, PICT, and **I²IT
  ("International Institute of Information Technology, Pune")**. The sample held only ~80 IIIT Pune author slots, so the
  institute is small and its campus history (transit campus; PINs 411041 / 411048 / 412109) still has to be established from
  primary sources.
* Bangalore: REVA University's "School of Computing and Information Technology".
* Kancheepuram: Sri Venkateswara College of Engineering's IT department.

## 2. Registry and classifier review (2026-10-27)

### 2.1 Registry (`scripts/institutes_iiit.py`)
* `family="iiit"`; `mention` = "International / Indian / Indraprastha Institute of Information Technology" (fuzzy: Institue,
  "Institute for", "Information, Technology", "Information and Technology", Tecchnology, Int'l, Indaprastha) or `IIIT…` or dotted
  `I.I.I.T.`. `confusable` = IIT names + unregistered IIITs named with their city (Lucknow, Kota, Vadodara, Sri City, Guwahati,
  Kalyani, Bhagalpur, Agartala, Bhubaneswar, Naya Raipur, Dharwad, Una, Sonepat, Kottayam, Manipur, Nagpur, Ranchi, Bhopal,
  Surat, Raichur, Tiruchirappalli, Kurnool, Kerala/IIITM-K, Basar, Nuzvid …) and their abbreviations.
* `explicit_full`: the institute's name followed by its city with only punctuation or a bracketed abbreviation in between, or
  `IIIT<city>`. A 60-character window (first version) matched "Indian Institute of Information Technology, Dharwad, Pune"; the
  tightened rule leaves looser strings to the mention rule (mention + place in the same part, nothing else named).
* A named unregistered IIIT is a strong exclusion (`exclude`) for every IIIT ("IIITDM Kurnool … CVRDE, Avadi, Chennai").
* IIIT Pune's `mention` deliberately excludes "International Institute of Information Technology": in Pune that is the private
  I²IT (Hinjawadi), and ORCID/DBLP person matching accepts "city AND mention". I²IT strings are excluded explicitly.
* `state=None` for all eight: every state concerned has a second IIIT (MP: Gwalior+Jabalpur; UP: Allahabad+Lucknow; Karnataka:
  Bangalore+Dharwad+Raichur; TN: Kancheepuram+Trichy; Maharashtra: Pune+Nagpur; Telangana: Hyderabad+Basar). No broad sweeps
  are used (the `Telangana` sweep was run before this decision and is not in the registry).
* IIT regression: every distinct author-affiliation string of the three v1 datasets (46,021) classified for all 23 IITs with and
  without `institutes_iiit.py`: **0 changed verdicts** (first version and again after review round 2).

### 2.2 Crossref sweeps
44 tokens, all completed on 2026-10-27 (light records, 3 lanes, watchdog runner `raw/run_sweeps_iiit.sh`).

### 2.3 Review findings (`review_strings.py`; all `uncertain`, all `iitnoname`, all `iitnone`, top `other`, random `iit` samples)
**No campus PIN or locality of the eight IIITs is campus-unique.** Every one was dominated by other organisations in the
uncertain lists, so the department rule is not used for any IIIT (anchors = e-mail domains only), and the location tokens are
`shared` (without an IIIT mention a string there is not about the IIIT) except where noted:

| IIIT | token | shared with (examples from the uncertain lists) | role |
|---|---|---|---|
| Jabalpur | 482005, Dumna | Hitkarini colleges (HCET, dental, pharmacy), MITS Gwalior typo | city |
| Gwalior | 474015, Morena Link Road | (no conflicts found; kept conservative) | city |
| Allahabad | Jhalwa, Devghat/Deoghat, 211015, 211012 | Shambhunath Institute (SIET), VKS Agritech | city |
| Bangalore | 560100, Electronics City | IBAB, C-DAC, Centre for Human Genetics, XIME, Bangalore Bioinnovation Centre, companies | shared |
| Pune | 411041, 411048, 412109, Ambegaon, Nanoli | NBNSSOE, JSPM, SKNCOE (Narhe); VIIT, NIBM, PCCM (Kondhwa); SKNMC; CFSL (Nanoli) | shared |
| Kancheepuram | 600127, Melakottaiyur, Vandalur, Kelambakkam | VIT Chennai, Bharath Institute, PSVPEC, Tagore colleges, TNPESU; CMI, Chettinad; BSA Crescent | shared |
| Delhi | Okhla, 110020 | DSEU G.B. Pant campus, AcSIR, INCLEN, IHD, Sightsavers, Fortis Escorts | shared |
| Hyderabad | Gachibowli, 500032, 500046 | NIAB, AIG hospitals, University of Hyderabad, CR Rao AIMSCS, DRILS, MANUU, TIFR-H | shared |

Other decisions: "Indian Institute of Design and Manufacturing Jabalpur" (IT dropped) = IIITDM Jabalpur; "ABV-IITM" = ABV-IIITM;
"IIIDM Kancheepuram" = IIITDM; an IIT name printed with an IIIT's token is another organisation (PIN typo); Kohli Centre and
CVIT are IIIT-H units. Each decision is a test case in `scripts/test_affil_cases_iiit.tsv` (49 IIIT cases; 112/112 pass).

Effect (distinct strings / author slots classified as the institute, end of round 2): Jabalpur 923 / 5,489; Gwalior 670 / 4,254;
Allahabad 816 / 5,654; Pune 73 / 164; Kancheepuram 755 / 4,318; Bangalore 402 / 2,685; Delhi 1,079 / 8,343; Hyderabad 1,084 / 5,598.
Remaining `uncertain`: 0–2 distinct strings per institute (garbled multi-institute strings).

**Bug reported to the IIT team (not fixed here, shared code):** the IIT explicit rule `I.I.T. <city>` matches inside the dotted
"I.I.I.T. Hyderabad", so `classify("iit_hyderabad", "I.I.I.T. Hyderabad, Telangana, India")` returns `iit`.

### 2.4 Discovery channels
Europe PMC, DOAJ, DBLP, INSPIRE (Allahabad 26 records; Hyderabad), ORCID harvested for all eight (`raw/run_channels_iiit.sh`);
Europe PMC and DOAJ re-run after review round 2 because their queries derive from the token roles (`raw/run_epmc_doaj_iiit.sh`).
Europe PMC records (final queries): Jabalpur 199, Gwalior 87, Kancheepuram 968, Allahabad 440, Bangalore 575, Pune 479, Delhi 1,313,
Hyderabad 805.

## 3. Rosters and golden sets (sub-agents, Sonnet)
* Briefs: `agents/iiits.json` + `fill.py`; each filled brief gets a "machine environment" section (Windows, venv, RM_MAILTO,
  operator) and the instruction to read "IIT" as "this institute".
* Incidents (2026-10-27): (1) the IIITDM Jabalpur CDN serves brotli-compressed bodies that `polite_get.py` cached undecoded,
  because `brotli` was missing in the venv; installed (urllib3 then decodes transparently; no code change). (2) A DNS outage
  stopped all four agents; resumed from their saved state. (3) The session usage limit stopped all agents; the operator asked
  for fewer parallel agents: **at most two agents at a time** from then on.
* **IIITDM Jabalpur roster** (accepted): 129 people (73 current, 28 former, 28 visiting); NIRF 2018–2026 tables (joining/leaving
  dates) + 16 Wayback snapshots + annual reports; 72 of 73 current rows NIRF-confirmed; ORCID 46. The 8 currently listed
  visiting people carry no year range (open tenure); harmless because visiting people only contribute papers that print the
  institute's affiliation (PROCESS.md §15.6). Known gaps: four image-only annual reports not read.
* **IIITDM Jabalpur golden set** (accepted): 274 papers (target 300; four image-only annual reports, faculty pages mostly end
  ~2023), 37 high / 237 medium, every year 2016–2026, all units with content; ~25 % with a printed DOI; independence confirmed in
  its notes.
* **ABV-IIITM Gwalior roster** (accepted): 137 people (78 current, 12 former, 44 adjunct, 3 visiting); NIRF 2026 72 regular −3
  leavers +9 missing = the 78 on the live site; 69 current rows NIRF-confirmed; ORCID 44. NIRF calls adjuncts "Visiting": the
  site's term was kept. The 25 currently listed adjuncts carry no range (open tenure).

## 4. Pipeline runs

### 4.1 First pass (`run_v2.sh merge`, affiliation channels + ORCID + DBLP, no roster channels), 2026-10-27
* IIITDM Jabalpur: 2,264 records (1,268 verified, 996 unverified-likely; 663 in the unconfirmed file). **Recall 51.8 %** (142/274;
  60.2 % if the unconfirmed file were included). Misses: 107 not discovered (93 without a printed DOI; Springer/Elsevier journals,
  book chapters, conference papers: publishers without deposited affiliations, i.e. the gap the roster channels address), 23 in
  the unconfirmed file, 1 rejected, 1 dropped. Comparable to v1 iteration 0 (Ropar 77.9 %, Kharagpur 63.9 %) before roster channels.
* All eight (records / verified / likely / unconfirmed file): Jabalpur 2,264 / 1,268 / 996 / 663; Gwalior 1,664 / 1,001 / 662 /
  964; Kancheepuram 1,506 / 1,029 / 477 / 441; Allahabad 2,436 / 1,610 / 824 / 989; Bangalore 1,134 / 943 / 188 / 496; Pune 183 /
  114 / 69 / 90; Delhi 3,243 / 2,237 / 1,006 / 1,784; Hyderabad 3,301 / 2,438 / 862 / 2,153. Hyderabad and Delhi look low for
  their size: CS conference output without DOI or deposited affiliations (CVF open access, ACL Anthology, NeurIPS) depends on
  the DBLP / arXiv / roster channels.

### 4.2 Roster stage (`run_v2.sh final`), Jabalpur, Gwalior, Kancheepuram, Allahabad (2026-10-27)
Recall (all golden papers; DOI-subset; incl. the unconfirmed file):

| IIIT | recall | DOI recall | incl. unconfirmed | not discovered |
|---|---|---|---|---|
| Jabalpur | 66.1 % (181/274) | 78.3 % | 74.1 % | 69 |
| Gwalior | 73.8 % (197/267) | 78.5 % | 84.6 % | 38 |
| Allahabad | 78.9 % (209/265) | (2 DOIs) | 83.8 % | 42 |
| Kancheepuram | 45.5 % (135/297) | 61.7 % | 55.2 % | 130 |

Allahabad's golden set is 2023-heavy (110 of 265 rows from one annual report): its recall must be read per year.

**Finding: the DBLP person channel was empty for every IIIT.** `roster_channels.py` (B5) runs only for roster people with a
DBLP pid, and the roster brief accepts only identifiers printed on institute pages, which IIITs rarely show (0–1 pids per
roster; `dblp_works` = 0 for all 157 Kancheepuram people, including prolific CS faculty). Kancheepuram's misses concentrated on
exactly those people. New IIIT-team tool `scripts/dblp_roster_ids.py` fills empty `dblp` cells from the DBLP SPARQL endpoint when
the DBLP name matches and (R1) the DBLP ORCID equals the roster ORCID, (R2) a DBLP affiliation classifies as the institute, or
(R3) ≥ 2 and ≥ 5 % of the DBLP person's DOIs are affiliation-verified records of the institute with a matching institute author.
A different ORCID is never accepted; ties stay blank; every decision is in `rosters/notes/<inst>_dblp_ids.tsv`. The 5 % rule
was added after an audit of the first run: common names ("Amit Kumar" 3 of 229 DOIs, "Sunil Kumar" 3 of 277) had attached to
prolific namesake profiles. Accepted: Kancheepuram 16, Jabalpur 28, Gwalior 47, Allahabad 44, Bangalore 36, Pune 5.

**Also observed (shared code, reported to the IIT team, not changed):** `split_name()` takes the last token as family name, so
Tamil patronymic-initial names ("Sadagopan N", 61 of 157 Kancheepuram rows) get the family name "N"; the swapped-order rule in
`name_match` partly compensates, but the data-driven common-surname list then contains single initials (a, b, k, m, p, r, s, v).
The IIT Madras / Tirupati / Palakkad rosters have the same pattern.

**Incident (2026-10-27, ~17:30): ORCID daily quota exhausted** (HTTP 429 "exceeded the daily quota for anonymous usage"), first
reported by the Pune roster agent. The roster-stage re-run with DBLP ids, started 17:06, was stopped (`roster_channels.py` does not
cache ORCID responses, so the run would have lost every roster ORCID channel); its outputs from the morning run were untouched
(the stage writes at the end). Re-run after the quota resets. Agents told not to call ORCID meanwhile.
Incident: the Pune roster agent stopped its own duplicate fetches with a process-name filter that also matched other agents'
`polite_get.py` processes (the `pkill` pitfall of PROCESS.md §10); agents are now told to stop only PIDs they started.

### 4.3 Rosters and golden sets accepted later on 2026-10-27
* Kancheepuram roster 157 (103 current; operator change: the director in additional charge, a regular ABV-IIITM professor, set
  to `adjunct (2026-2026)`, so his Gwalior papers cannot enter through person channels); golden set 297 (22 high).
* Allahabad roster 121 (87 current; acting director 2022–23 = adjunct); golden set 265 (20 high; 2023-heavy, see above).
* Bangalore roster 132 (49 current, 38 adjunct); golden set 261, year-balanced (23–24 per year); its `/publications` source is a
  static institute-maintained page (checked: no Scopus / OpenAlex / IRINS backing).
* Pune roster 109 (31 current); **campus history**: transit Sadumbare, Talegaon–Chakan Road 412109 (2016–2018); Kondhwa Annexe,
  Yewalewadi 411048 (by 2019–2020); Ambegaon Budruk 411041 (by 2023–2025); permanent Nanoli-Tarf Chakan, Talegaon 410507 (from
  2025); mentor institute COEP. Tokens added to the registry as `shared`; new sweeps (410507 75, Talegaon 272, Sadumbare 0,
  Yewalewadi 1 records) added no IIIT Pune strings. Golden set 94 (founded 2016; no 2016–2017 rows possible under the tenure rule).
  Ritu Tiwari appears in the Gwalior (current) and Pune (former 2019–2025, "on lien") rosters; deposited affiliations decide
  her papers, only the "likely" tier could double-credit.
* Delhi golden set 433 (13 high). `iiitd.ac.in` fails TLS for the fetcher, so every institute page came from Wayback. 87 % of
  rows come from the institute's year-wise publication list (2019–2026), whose APA-style entries look Scopus-derived:
  independence is weaker than for the other sets, and the rows are separable via `source_type = dept_page`.
* Delhi roster 360: 97 current, 1 emeritus, 154 former, 81 adjunct, 27 visiting. Built from quarterly Wayback faculty lists
  (2016-03 to 2026-08) plus the institute's NIRF PDFs 2017–2025. 97 NIRF-only lecturer / ad hoc rows have no department.
* `dblp_roster_ids.py` change: the 5 % namesake guard rejected real faculty with long careers elsewhere (Mayank Vatsa 3 of 441
  DOIs, Vinayak Naik, Tammam Tillo, M. S. Hashmi). The guard now applies only when the matched name is held by several DBLP
  persons. Re-run for all rosters (tool-set ids unset first, roster-printed ids kept). Accepted: Delhi 101, Gwalior 49,
  Allahabad 45, Bangalore 40, Jabalpur 29, Kancheepuram 16, Pune 7; later Hyderabad 77.
* Hyderabad roster 211: 131 current, 25 former, 9 emeritus, 31 adjunct, 15 visiting. Sources: faculty sitemap, NIRF 2019–2026
  via Wayback (the PDFs sit under robots-disallowed `/wp-content/`), 16 Wayback faculty-list snapshots 2016-08 to 2024-07.
  No snapshot exists between 2017-07 and 2019-05.
* Hyderabad golden set 322, all medium, 7 DOIs (2 %). Older years are thin: 11–16 per year for 2016–2021, against 55 per year
  for 2023–2026.
  - The institute repository (`iiit.ac.in/publications/`) pages only through POST, and per person it exposes only the newest
    10 papers. Wayback has no snapshot of it before 2023.
  - The older years therefore rest on the CVIT and other lab lists. Recall for 2016–2021 will have wide intervals.
  - Incident: the agent fetched ten activity-report PDFs under the robots-disallowed `/wp-content/`. No row uses them, and
    agents are now told to read robots.txt first.

### 4.4 Security incident: devalab.in (2026-10-28 00:22)
The Hyderabad roster agent requested `https://devalab.in/robots.txt` (U. Deva Priyakumar's lab). The site has no robots.txt
and answered with its server-wide 404 page. Windows Defender quarantined the cached body
(`agents/.runtime/shared_cache/01b04850….body`) as a Severe "Trojan", and at 00:26 also quarantined two shell-output files of
the investigating agent that had printed the page.

A sub-agent then analysed the site in memory only (8 requests):
* The 404 page is a 583-byte loader. It sets `_skz_pid` and pulls `http://cdn.jsinit.directfwd.com/…`, an ad / redirect
  script, the same pattern reported elsewhere as `Trojan.HTML.MALINK`.
* It is not a webshell or a dropper: no eval, base64, iframe or PHP.
* The real pages (home page, `publications.html`) are clean static Mobirise HTML that loads only local scripts.
* Likely cause: a host-level or injected nginx error page. The risk is to browsers that hit a 404, not to our data.

Nothing was executed on this machine. Afterwards agents were allowed exactly one URL on the host, `publications.html` (8
golden rows). All fetched content is treated as data only.
