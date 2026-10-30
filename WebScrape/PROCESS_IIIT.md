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

### 4.5 ORCID identifiers for the rosters, and the full roster-stage runs (2026-10-28)
* **ORCID quota.** The anonymous Public API quota ran out again on the first roster-stage run. The operator registered a
  personal ORCID Public API client (free; `client_credentials`, scope `/read-public`). The token lives in the git-ignored
  `WebScrape/.env`, and `common.get()` sends it on `pub.orcid.org` calls (shared-code commit 3ab0f3c; without a token the
  behaviour is the anonymous one as before). Pitfall: in Git Bash the scope must be URL-encoded (`%2Fread-public`), because MSYS
  rewrites `/read-public` into a Windows path and ORCID answers `invalid_scope`.
* **ORCID column filled.** As with DBLP, the roster brief accepts only ORCIDs printed on institute pages, so the ORCID-works
  channel (B4) ran for few people. New IIIT-team tool `scripts/orcid_roster_ids.py` fills empty `orcid` cells (visiting and
  adjunct people skipped) when (R1) the same ORCID is deposited for a matching institute author on ≥ 2 affiliation-verified
  records and no other ORCID is deposited for that name, or else (R2) the person is the unique name match among all ORCID
  records that list the institute's ROR id (expanded search, includes students; several matches leave the cell blank). Every
  decision is in `rosters/notes/<inst>_orcid_ids.tsv`. Accepted (R1 / R2): Kancheepuram 18 / 2, Jabalpur 23 / 2, Gwalior 21 / 0,
  Allahabad 16 / 2, Bangalore 18 / 0, Pune 2 / 9, Delhi 72 / 37, Hyderabad 50 / 28; 345 in all.
* **Shared bug found:** `datacite_enrich.py` raised `KeyError` on DataCite ORCID `nameIdentifiers` without a value, which killed
  its worker threads. Fixed in a separate commit (8002355); IIT behaviour is unchanged for well-formed records.
* **Incident:** the laptop restarted during the run with the ORCID ids (exit 4). The strict and `--loose` roster passes had
  finished for all eight; the run was resumed with the `--arxiv-only` pass for the seven institutes it had not reached, then
  `run_v2.sh refresh` for all eight.

Recall (all golden papers) through the roster-stage runs:

| IIIT | morning (4.2) | run 3: + DBLP ids | run 4: + ORCID ids |
|---|---|---|---|
| Kancheepuram | 45.5 % | 47.1 % | 48.8 % |
| Jabalpur | 66.1 % | 70.1 % | 71.2 % |
| Gwalior | 73.8 % | 79.8 % | 80.9 % |
| Allahabad | 78.9 % | 82.3 % | 82.3 % |
| Bangalore | – | 76.2 % | 77.4 % |
| Pune | – | 57.4 % | 60.6 % |
| Delhi | – | 82.9 % | 83.8 % |
| Hyderabad | – | 71.1 % | 70.5 % |

Kancheepuram stays lowest: of its 157 misses after run 4, 125 were never discovered (mostly faculty-page papers in venues with
no index coverage; some golden titles carry the venue inside the title, which defeats title matching), and 29 sit in the
unconfirmed file because their year falls outside the person's verified-paper window (the "possible" rule of `finalize.py`, an
IIT-team precision rule left unchanged; e.g. a 2016 N. Sadagopan ENDM paper found through his DBLP profile).

### 4.6 Verification and TODO resolution (2026-10-28/29)
`verify_epmc.py` (13,891 records checked) and `verify_springer.py` (4,755 Springer pages, robots-permitted paths only) ran for
all eight, then `resolve_todos.py` per institute and `run_v2.sh refresh`.
* **Incident:** on the first attempt every `resolve_todos.py` call died with `GET failed after 8 tries` on a Crossref single-DOI
  lookup (`10.1109/wispnet.8299896` and others). The same URLs answered a normal 404 minutes later, so this was a network
  outage on this machine (the last Springer request also failed then), not a code fault. The half-done refresh was stopped by
  PID and both steps re-run (`raw/verify_iiit_2.log`).
* `resolve_todos.py` (R1 Crossref retry / R2 CSL / R3 DOI-less candidates resolved / R4 venue ISSNs / R5 Semantic Scholar ids
  found): Kancheepuram 0 / 0 / 5 / 5 / 174; Jabalpur 1 / 3 / 8 / 10 / 266; Gwalior 1 / 4 / 18 / 22 / 296; Allahabad 4 / 4 / 21 / 20 /
  367; Bangalore 1 / 1 / 11 / 11 / 259; Pune 0 / 2 / 2 / 5 / 62; Delhi 2 / 0 / 55 / 11 / 1,164; Hyderabad 1 / 4 / 67 / 8 / 1,343.
* `validate.py`: **0 violations for all eight** (200-record Crossref spot check per institute: titles, years and venues agree;
  the few `not_in_crossref_now` are DOIs registered elsewhere).

Result after verification (main file = verified + unverified-likely; "possible" candidates are in
`candidates_unconfirmed_<inst>.json`):

| IIIT | main records | verified | likely | unconfirmed | recall | DOI recall (n) |
|---|---|---|---|---|---|---|
| Delhi | 4,670 | 2,567 | 2,103 | 1,007 | 84.8 % (367/433) | 86.6 % (247) |
| Allahabad | 3,137 | 2,107 | 1,030 | 557 | 83.8 % | 100 % (2) |
| Gwalior | 2,146 | 1,378 | 768 | 713 | 81.3 % | 87.7 % (65) |
| Bangalore | 1,642 | 1,091 | 549 | 329 | 79.7 % | 88.3 % (137) |
| Jabalpur | 3,027 | 1,849 | 1,178 | 433 | 73.4 % | 88.4 % (69) |
| Hyderabad | 5,187 | 2,895 | 2,292 | 1,013 | 70.8 % | 57.1 % (7) |
| Pune | 272 | 163 | 109 | 93 | 61.7 % | 70.0 % (10) |
| Kancheepuram | 1,856 | 1,265 | 591 | 378 | 50.8 % | 66.0 % (47) |

Verification raised the verified count from 1,030 to 1,265 for Kancheepuram and from 1,264 to 1,849 for Jabalpur. Bangalore's main file also holds 2 `ambiguous` records (an IIHS Bangalore + IIIT Delhi string).

## 5. Precision audits and the fixes they triggered (2026-10-29)

### 5.1 Method
`precision_sample.py <key>` (seed 20261007) draws 25 verified and 40 likely records from the main file. The shared sampler reads
only the main file, so the 40 "possible" rows were drawn from `candidates_unconfirmed_<key>.json` with the same seed by a
scratch script (shared script unchanged), to match the layout of the IIT audits. One Sonnet sub-agent per institute (two at a
time) judged every row against the affiliation printed on or deposited for the paper: OpenAlex raw affiliation strings,
Crossref, Europe PMC, then arXiv / open-access PDFs or publisher pages where robots.txt allowed. Anything behind a 403, a
Cloudflare or IEEE challenge, or a CAPTCHA stayed `unknown`. Files: `golden/precision_audit_<key>.csv` (verdict yes / no /
unknown, evidence URL, quoted affiliation).

### 5.2 Fixes
* **arXiv co-author route on collaboration papers.** The Jabalpur audit found a LIGO/Virgo/KAGRA paper (about 1,770 authors)
  credited to the roster's "Anil Kumar": the arXiv person channel (B6) accepts a paper when one co-author name matches, which
  on such lists happens by chance. 23 Jabalpur and 1 Delhi likely records had this shape. `roster_channels.py` now reads an
  optional registry field `arxiv_coauthor_max_authors` (shared commit 76a5cd0; no IIT entry sets it, so IIT behaviour is
  identical); every IIIT entry sets 50 (ec69ebc). Papers above the cap enter only through the printed affiliation. After the
  rerun Jabalpur lost the 23 records and recall was unchanged.
* **DBLP catch-all profiles.** Pune's likely tier was 55 % (18 yes / 15 no): 13 of its wrong rows came from the DBLP id
  `166/1095` accepted for Sushant Kumar. That is DBLP's undisambiguated "Sushant Kumar" profile (120 papers of several people,
  4 of them ours), which got through the homonym exemption of §4.3, because it is the only DBLP person with exactly that name.
  The exemption now also requires that no other DBLP name extends the matched one (11 "Sushant Kumar …" persons exist); see
  beb270c. Re-derived for all eight rosters: removed Sushant Kumar (Pune), Aman Kumar (Delhi; catch-all `77/4697`) and Abhishek
  Kumar (Delhi; the DBLP ORCID differs from the roster ORCID filled in §4.5); newly accepted on the grown verified set: Sonam
  Maurya (Pune), 2 Jabalpur, 3 Delhi, 3 Hyderabad ids. Roster stage rerun for Pune, Jabalpur, Delhi, Hyderabad
  (`raw/final_iiit_5.log`), then `run_v2.sh refresh` for all eight: 0 violations.
* Pune's sample was redrawn from the corrected output; 67 of 105 rows carried their verdicts over by DOI (the verdict depends on
  the paper only) and the 38 new rows were audited. The Jabalpur and Delhi audits describe the output before these two fixes
  (Delhi: after the arXiv cap); both fixes only remove person-channel matches, so those figures are lower bounds for the likely
  tier.

### 5.3 What the audits show
* Verified: 25 / 25 at every institute.
* The wrong likely rows fall into three groups: (a) roster people credited with papers from before they joined or after they
  left (Kancheepuram: Dixit at IIT Madras 2019, Gajrani at IIT Bombay 2021; Allahabad: Bhattacharjee at IIT Gandhinagar, Dubey at IIIT Chittoor; Hyderabad: Roy at
  TU Delft 2019); (b) common-name namesakes (Jabalpur "Sanjeev Jain" at SMVDU; Allahabad "Manish Kumar" ×3); (c) the two
  channel faults fixed above.
* The possible tier is right for only 21–58 % of decided rows, which is what keeping it out of the main file is for. Much of it
  comes from ORCID records that list the institute without dates (S. Kannadhasan of Tamil Nadu colleges: 233 Gwalior candidates,
  2 in the main file; Partha Pratim Roy, IIT Roorkee, for Allahabad) and from faculty who moved on (Tanmoy Chakraborty's IIT
  Delhi papers for IIIT Delhi; M. Mohamed Asan Basiri's IIITDM Kurnool papers for Kancheepuram).
* Classifier-level confusables seen only in the possible tier: VIT Chennai prints the Kancheepuram PIN 600127 (registered as
  `shared`, not an anchor); bare "Indian Institute of Information Technology, Design and Manufacturing" without a city
  (Kancheepuram, Jabalpur or Kurnool) was judged unknown.

## 6. Final results (2026-10-29)

Main file = verified + unverified-likely (`v2/<key>.json`); unconfirmed = "possible" candidates
(`v2/candidates_unconfirmed_<key>.json`). Recall against the independent golden sets; precision = yes / (yes + no) in the audit
(n = 25 / 40 / 40; unknowns excluded; at n = 40 a likely-tier figure carries about ±10 points).

| IIIT | main | verified | likely | unconfirmed | recall | DOI recall (n) | P verified | P likely | P possible |
|---|---|---|---|---|---|---|---|---|---|
| Delhi | 4,695 | 2,568 | 2,127 | 1,003 | 85.0 % (368/433) | 86.6 % (247) | 100 % | 97 % (34/35) | 21 % |
| Allahabad | 3,137 | 2,107 | 1,030 | 557 | 83.8 % (222/265) | 100 % (2) | 100 % | 80 % (28/35) | 30 % |
| Gwalior | 2,146 | 1,378 | 768 | 713 | 81.3 % (217/267) | 87.7 % (65) | 100 % | 85 % (28/33) | 21 % |
| Bangalore | 1,642 | 1,091 | 549 | 329 | 79.7 % (208/261) | 88.3 % (137) | 100 % | 97 % (32/33) | 29 % |
| Jabalpur | 3,064 | 1,849 | 1,215 | 398 | 74.5 % (204/274) | 88.4 % (69) | 100 % | 91 % (30/33) | 58 % |
| Hyderabad | 5,237 | 2,895 | 2,342 | 1,004 | 71.7 % (231/322) | 57.1 % (7) | 100 % | 92 % (35/38) | 24 % |
| Pune | 235 | 164 | 71 | 87 | 62.8 % (59/94) | 70.0 % (10) | 100 % | 71 % (24/34) | 23 % |
| Kancheepuram | 1,856 | 1,265 | 591 | 378 | 50.8 % (151/297) | 66.0 % (47) | 100 % | 76 % (29/38) | 45 % |

Bangalore's main file also holds 2 `ambiguous` records. `validate.py`: 0 violations for all eight.

### 6.1 Open problems
* **Kancheepuram recall (50.8 %).** Most misses are papers on faculty pages in venues no index covers; some golden titles carry
  the venue inside the title. 29 more misses sit in the unconfirmed file because of the year-window "possible" rule.
* **Hyderabad and Allahabad golden sets have almost no DOIs** (7 and 2), so their DOI recall says little; Hyderabad's set is thin
  for 2016–2021 (§4.3) and Allahabad's is 2023-heavy.
* **Delhi golden set** is 87 % from the institute's year-wise list, which looks Scopus-derived: weaker independence.
* **Likely tier** still contains tenure-boundary errors (people credited with papers from other employers). A per-person
  check of the printed affiliation where one exists would remove them, but needs a change to the IIT team's `finalize.py`.
* **Pune likely tier (71 %).** After the DBLP fix, 7 of its 10 wrong likely rows come from Sandeep Mishra's DBLP profile
  (`180/4051`), accepted correctly by his ORCID (R1), into which DBLP has merged papers of namesakes at UT Austin, BAE Systems,
  Microsoft and Jaypee. No identifier rule can catch an ORCID-linked profile that DBLP itself conflates; dropping the id would
  also drop his DBLP-only papers, so it is left and reported here. Pune is small (71 likely records), so one person moves the
  tier by many points.
* **Shared-code items for the IIT team:** 5a8ebda (Windows file locks), 3ab0f3c (optional ORCID token), 8002355 (DataCite
  KeyError), 76a5cd0 (optional arXiv co-author cap); and, not changed: `split_name()` on Tamil patronymic-initial names (§4.2),
  `polite_get` caching transient DNS failures as dead, `python3 -I` ignoring PYTHONUTF8, and the I.I.I.T. pattern in the IIT
  explicit rule.

### 6.2 Comparison with DPCN Group 9's dataset (2026-10-29)
A sub-agent compared our Hyderabad and Delhi data with Group 9's "IIIT-H × IIIT-D Research Map"
(github.com/ShreeLite/Citation-Network-Analysis, `site/src/data/papers.json`). That pipeline starts from a faculty roster and pulls each person's works
from OpenAlex (primary), DBLP, the IIIT-H portal and Crossref, and keeps a work if it prints the institute **or** falls after the
person's joining year. It holds journals and conferences only, without author lists or per-paper references.

| | IIIT-H | IIIT-D |
|---|---|---|
| theirs / ours (all types) / ours (journal + conference) | 4,678 / 5,237 / 4,027 | 4,309 / 4,695 / 3,667 |
| overlap (DOI, then title + year) | 3,815 | 3,143 |
| only theirs: institute in OpenAlex/Crossref metadata (yes / no / unknown) | 330 / 332 / 58 | 274 / 770 / 55 |
| only ours: same check | 855 / 185 / 278 (82 % of decided) | 977 / 154 / 265 (86 %) |
| golden-set recall (fuzzy title), theirs vs ours | 73.6 % vs 70.8 % | 86.4 % vs 83.8 % |

* Our extra records are far more often affiliated (82–86 % vs 28–59 %). Ours also have author lists and references.
* Theirs find **604 affiliated papers we lack**. In our pipeline: 364 never discovered, 208 in the unconfirmed file, 32 rejected
  candidates. The cause is the handoff rule that keeps OpenAlex out of discovery (HANDOFF_IIITs §8; PROCESS.md §1: OpenAlex
  needs a key). Using OpenAlex is a method decision for both teams and is not taken here. The list is kept outside the repository
  (`rm_work/compare_shreelite/missed_by_us.csv`).
* Their citation counts are higher on ~40 % of shared papers (OpenAlex counts vs our Crossref counts).

## 7. The 22 further IIITs (from 2026-10-29)
The handoff assigned eight IIITs (course brief Groups 9–11). On 2026-10-29 the operator extended the run to every IIIT named
"IIIT" by the Government of India: IIITDM Kurnool, the two state IIITs Bhubaneswar and Naya Raipur, and the 19 PPP IIITs. It
leaves out the RGUKT campuses (Basar, Nuzvid, RK Valley, Ongole) and IIITM-K / Digital University Kerala. The method is
unchanged (§1–6).

### 7.1 Reconnaissance
* **ROR** (v2 `query=`, checked against name, city and website). There is no ROR record for **IIIT Tiruchirappalli, IIIT Bhagalpur,
  IIIT Agartala, IIIT Raichur** (searched by name, "IIIT <city>" and "Information Technology <city>"). Their `ror` is None:
  `orcid_people` matches only by name and city, and `orcid_roster_ids` skips its ROR route (R2).
* **Campuses.** Two sub-agents gathered campus facts from the institutes' sites, NIRF, annual reports and Wikipedia. Most PPP IIITs
  spent years at a mentor's campus and printed its address. Those that did:
  - Kota: MNIT Jaipur, 2013 to now (since 2023 only years 1 and 2 are at Ranpur).
  - Una: NIT Hamirpur.
  - Sonepat: NIT Kurukshetra, then IIT Delhi's Sonepat Techno Park.
  - Lucknow: IIIT Allahabad, Jhalwa, until 2019.
  - Kurnool: IIITDM Kancheepuram, until 2018.
  - Raichur: IIT Hyderabad, 2019–2020/21.
  - Agartala: NIT Agartala.
  - Surat: SVNIT.
  - Bhopal: MANIT.
  - Ranchi: NIT Jamshedpur, then the JUT campus, Namkum.
  - Tiruchirappalli: BIT, then NIT Trichy, then Oxford Engineering College.
  - Kottayam: Amal Jyothi College, then the GIFT campus in Thiruvananthapuram.
  - Vadodara: Gandhinagar throughout, plus Diu since 2020.
  The facts and their sources are in the registry comments.
* **Crossref sweeps** (light records, 80 tokens: city names, campus localities, PINs and abbreviations; `raw/run_sweeps_iiit2.sh`
  and `raw/run_sweeps_iiit3.sh`). "Sri City" is not swept, because Crossref treats it as an OR on "city" (595k hits); Chittoor, 517646 and
  Satyavedu stand in for it. Mentor cities are not swept: papers from those years name the IIIT with its own city ("IIIT Kota,
  MNIT Campus, Jaipur").

### 7.2 Registry
* Same design as §2.3: anchors are e-mail domains only, every place token is `shared` (it needs an IIIT mention), and mentor
  cities are not place tokens. Adding them would make every loose IIIT string of Prayagraj, Hyderabad or Chennai ambiguous for the
  IIIT registered there.
* The first eight used one list of "unregistered IIITs named with their city" as a strong exclusion and as confusables. Each new
  IIIT drops only its own city and abbreviations from those lists (`_own_lists`). The first eight's lists are byte-identical to
  before.
* Ambiguous abbreviations stay confusable for everyone: IIITK (Kota / Kottayam / Kalyani / Kurnool), IIITR (Ranchi / Raichur),
  IIITBH / IIIT-BH (Bhubaneswar / Bhagalpur) and IIITS (Sri City / Surat / Sonepat).
* **Regression check.** Every swept author string that names an IIIT, "information", or any of the new place tokens was
  classified for all 31 institutes registered before. That is 179,096 strings, classified with the old and the new
  `institutes_iiit.py`. **One verdict changed:** `iit_delhi` went from uncertain to None on "Indian Institute of Information
  Technology (IIIT) Sonepat, Techno Park, IITD Sonipat Campus", which is correct. `test_affil.py`: 112/112.
* **String review** (`review_strings.py`, all 22). Accepted strings were sampled for each institute, and all `other`, `uncertain`
  and `iitnone` strings were read. There were no false positives. The rules leave 5 strings uncertain in total. One is
  "IIITK, Dept. of ECE, Kottayam", left uncertain because IIITK is ambiguous. Three strings print "Indian Institute of Information
  Technology, Sri City 441108", which is IIIT Nagpur's PIN. They are left as `other` for Nagpur.

### 7.3 Progress (2026-10-30, interim: pushed for review)
Rosters, golden sets and precision audits are built by Sonnet sub-agents with the same briefs as §3 and §5.1. The
pipeline is `raw/pipeline_one.sh` (first pass → `orcid_roster_ids` → `dblp_roster_ids` → `run_v2.sh final`) followed by
`raw/verify_one.sh` (verify_epmc → verify_springer → resolve_todos → refresh + validate). `validate.py` reports 0
violations for every institute below.

| IIIT | main | verified | likely | unconfirmed | recall (golden) | DOI recall (n) | P verified | P likely | P possible |
|---|---|---|---|---|---|---|---|---|---|
| Bhubaneswar | 1,123 | 702 | 421 | 396 | 67.3 % (72/107) | 72.3 % (47) | 100 % | 91 % (32/35) | 13 % |
| Naya Raipur | 1,195 | 822 | 373 | 96 | 76.2 % (96/126) | 91.7 % (36) | 100 % | 81 % (25/31) | 19 % |
| Guwahati | 1,231 | 805 | 426 | 187 | 55.3 % (83/150) | 55.6 % (9) | 100 % | 82 % (28/34) | 21 % |
| Sri City | 879 | 568 | 311 | 288 | 69.7 % (99/142) | 62.9 % (35) | 100 % | 71 % (25/35) | 36 % |
| Lucknow | 240 | 176 | 64 | 70 | 81.5 % (44/54) | 85.7 % (21) | 100 % | 61 % (19/31) | 24 % |
| Kurnool | 562 | 410 | 152 | 203 | 61.4 % (27/44) | 72.2 % (18) | 100 % | 50 % (15/30) | 15 % |
| Vadodara | 364 | 241 | 123 | 153 | 63.6 % (63/99) | 81.0 % (21) | 100 % | 66 % (25/38)* | 7 % |
| Dharwad | 426 | 295 | 131 | 140 | 68.8 % (55/80) | 77.8 % (27) | 100 % | 74 % (25/34) | 36 % |
| Kota | 225 | 148 | 77 | 161 | 58.1 % (43/74) | 56.0 % (25) | 100 % | 48 % (15/31) | 6 % |
| Sonepat | 188 | 153 | 35 | 14 | 88.2 % (15/17) | 92.3 % (13) | 100 % | 82 % (23/28) | 0 % |
| Una | 246 | 183 | 63 | 100 | 57.0 % (57/100) | 63.0 % (54) | 100 % | 63 % (22/35) | 23 % |
| Tiruchirappalli | 187 | 148 | 39 | 65 | 61.5 % (24/39) | 70.6 % (17) | 100 % | 69 % (22/32) | 24 % |
| Kalyani | 439 | 289 | 150 | 85 | 76.2 % (77/101) | 70.8 % (24) | 100 % | 87 % (34/39) | 14 % |
| Kottayam | 716 | 566 | 150 | 129 | 59.3 % (86/145) | 69.8 % (43) | 100 % | 76 % (28/37) | 12 % |
| Manipur | 132 | 95 | 37 | 84 | 49.0 % (24/49) | 87.5 % (8) | 100 % | 64 % (18/28) | 17 % |

\* Vadodara was audited before the conflated DBLP profile of Pratik Shah (8 of its 13 likely `no`) was removed; the rebuilt
file has 20 fewer likely records. Kota's verified 25/25 includes one operator correction (a Springer page prints IIIT Kota as
the second affiliation; OpenAlex lists only the first). Golden sets under ~60 papers (Kurnool, Lucknow, Sonepat, Tiruchirappalli,
Manipur) give recall with wide uncertainty.

**IIIT Hyderabad with the institute repository (2026-10-30, operator decision):** `iiith_publist.py` adds the 6,667 items of
https://www.iiit.ac.in/publications/index.php as evidence `institute_list` (tier likely, main file; contradicted records still
rejected). Main file 5,237 → 6,352 (2,957 verified, 3,395 likely). Recall against the golden set rises to 95.3 %, but 260 of its
322 papers came from that repository, so the independent figure stays 71.7 % (§6).

**Roster corrections after audits or on review:** Pratik Shah's DBLP id removed (Vadodara); MNIT post-holders `adjunct` (Kota);
the IIT Roorkee Director-in-charge `adjunct` (Sonepat); 31 lab faculty `adjunct` (Kottayam); later roster briefs ask agents to file
post-holders employed elsewhere and lab-only staff as `adjunct` directly.

In progress (2026-10-30): Nagpur, Ranchi, Surat; not started: Bhopal, Bhagalpur, Agartala, Raichur.

**Main finding: the likely tier is weaker at young, high-turnover IIITs** (50–91 %, against 71–97 % for the first eight).
Almost every `no` is a paper from the joining or leaving year, or from an ORCID employment window, that prints the person's
previous or next employer. Examples are Din Bandhu (Kurnool 2022–23, then Manipal), Chandranath Adak (Lucknow, then Patna and
JIS) and Ruhul Amin (Naya Raipur, earlier Thapar and IIT (ISM)). Crossref holds no affiliation for these papers, so
`finalize`'s contradiction check (`rejected_contradicted`) cannot fire. The audits saw the other employer in OpenAlex's raw
affiliation strings. An OpenAlex-based contradiction check would remove most of these errors. That is the same method
decision as §6.2 (OpenAlex is out of discovery by handoff rule) and is left to the operator and the IIT team. The verified
tier is 100 % in every audit.

**Roster corrections made after audits:**
* Kurnool: joining year 2025 for two people absent from NIRF 2026. This has no practical effect: `roster_channels`
  already bounds a blank joining year by the first verified paper minus one.
* Kota: ten post-holders (Director, Deans, Coordinators) are MNIT Jaipur faculty holding IIIT Kota posts. They are now
  `adjunct`, so they contribute only papers that print IIIT Kota. Details are in the roster notes.

**Golden sets are thin for the young IIITs**: Kurnool 44 and Lucknow 54 papers, because faculty pages list work from before
joining and the institutes' own publication lists stop early. Their recall figures have wide uncertainty.
