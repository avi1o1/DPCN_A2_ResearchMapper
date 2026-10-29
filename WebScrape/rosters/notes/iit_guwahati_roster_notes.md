# IIT Guwahati faculty roster (2016-2026): lab notebook

Built 2026-10-27. Output: `WebScrape/rosters/iit_guwahati_faculty.csv` (655 rows). All fetches went through the shared `polite_get.py`. Pages, parsing scripts and intermediate JSON are in the session scratchpad (`work/iit_guwahati_roster/{data,code}`), not in the repo.

## 1. Result summary
| status | rows |
|---|---|
| current | 488 (475 on the institute faculty list + 13 NIRF-2026-only professorial people) |
| emeritus | 1 |
| visiting | 101 (NIRF visiting / non-professorial foreign scholars, mostly 2020-2024; no unit printed) |
| former | 65 |
| total | 655 |

Identifiers: ORCID 276 rows (all from the offline ORCID affiliation index, 0 from institute pages, 0 from live API, no per-person API calls); IRINS (Vidwan) link 416 and homepage 412 (both printed on the institute profile page); e-mail 473; Google Scholar, DBLP, Scopus: none (not on institute pages). joining_year 640 rows (476 of 488 current) from NIRF joining dates.

## 2. Per-unit counts against NIRF (size check, early)
Institute list (`resources/model/faculty-fetch`) = 477 entries (2 duplicate entries without a detail page removed -> 475 people). NIRF 2026 (Overall PDF, data as of early 2026) lists 544 rows, 543 "currently working": 471 with professorial designation, 73 "Other". NIRF 2025 = 460 rows, NIRF 2024 = 539 rows (incl. 69 visiting). Annual report 2024-25: faculty strength 464 (31 Mar 2025), plus 70+ honorary/visiting. Roster current 488 vs NIRF-2026 professorial 471 vs list 475: the 13 NIRF-only people are added on top of the list; 470 of 488 current rows are NIRF-2026-confirmed (the other 18: on the institute list but absent from NIRF 2026, e.g. recent joiners or people on lien).
The 73 NIRF-2026 "Other" people (designation Other, Regular, joined 1999-2024, mostly Assamese names, not on the institute faculty list) were treated as non-faculty staff and excluded (72 excluded rows after merging). If the reviewer prefers them included, NIRF-only people would be +72 current.

| unit | current | former | emeritus | visiting | total |
|---|---|---|---|---|---|
| Biosciences and Bioengineering | 40 | 3 | 0 | 1 | 44 |
| Centre for Disaster Management and Research | 1 | 0 | 0 | 0 | 1 |
| Centre for Linguistic Science and Technology | 2 | 0 | 0 | 0 | 2 |
| Chemical Engineering | 37 | 3 | 0 | 0 | 40 |
| Chemistry | 43 | 0 | 0 | 0 | 43 |
| Civil Engineering | 49 | 4 | 1 | 0 | 54 |
| Computer Science and Engineering | 34 | 4 | 0 | 1 | 39 |
| Design | 19 | 9 | 0 | 1 | 29 |
| Electronics and Electrical Engineering | 52 | 8 | 0 | 3 | 63 |
| Humanities and Social Sciences | 33 | 6 | 0 | 1 | 40 |
| Mathematics | 40 | 2 | 0 | 0 | 42 |
| Mechanical Engineering | 48 | 14 | 0 | 1 | 63 |
| Mehta Family School of Data Science and Artificial Intelligence | 8 | 0 | 0 | 0 | 8 |
| Physics | 46 | 2 | 0 | 7 | 55 |
| School of Agro and Rural Technology | 6 | 0 | 0 | 0 | 6 |
| School of Business | 11 | 0 | 0 | 0 | 11 |
| School of Energy Science and Engineering | 7 | 0 | 0 | 0 | 7 |
| (unit not established) | 12 | 10 | 0 | 86 | 108 |

Department = first department-type unit on the person's profile (the 11 academic departments take priority over schools/centres). Second units (e.g. Centre for the Environment, Centre for Nanotechnology, Centre for Intelligent Cyber-Physical Systems) are printed on profile pages but not recorded as CSV columns; e.g. Harshal B. Nemade: EEE primary, plus CICPS, Nanotechnology, Drone Technology. Centres without a primary person (Environment, Nanotechnology, Rural Technology, CICPS, Drone Technology, Sustainable Polymers, Water Research, Indian Knowledge Systems, Manekshaw, Interdisciplinary Studies) therefore have no rows of their own. No rename mapping was needed except that the faculty-list unit "Jyoti & Bhupat Mehta School of Health Sciences & Technology" had no primary-unit person. Former/NIRF-only people without a unit: department established from annual-report department tables when matched, else blank.

## 3. Sources and endpoints
* Institute list: `https://www.iitg.ac.in/iitg_faculty_all` loads `https://www.iitg.ac.in/resources/model/faculty-fetch` via AJAX (POST in the page; the plain GET returns the whole list, 684 KB, 477 entries: name, designation, e-mail, profile link). No per-department filter is possible with GET (the department filter `search_by_dept` is POST only and the fetcher is GET-only), so departments come from the profile pages.
* Profile pages `https://www.iitg.ac.in/iitg_faculty_details?name=...&fac=...` (475 of 477 fetched; the 2 failures are the duplicate entries without units): designation, e-mail, Personal Website, Vidwan/IRINS link, Department/Centre/School list.
* NIRF data submissions (institute page `https://www.iitg.ac.in/nirf/`): "Faculty Details" tables parsed from the Overall PDFs for 2018 (IR-O-U-0053), 2019 (IR-2-O-OE-U-0053), 2020, 2022, 2023, 2024, 2025, 2026 (also Engineering 2018, 2022-2026 as cross-check). NIRF 2021 Overall/Engineering PDFs are image-only (no text layer, no OCR attempted), the 2017 edition has names only. Columns: name, designation, joining/leaving date, currently-working flag, association type (age column in 2018-2020).
* Annual reports (`https://www.iitg.ac.in/report/reports.php`, PDFs 2015-16 to 2024-25): "FACULTY MEMBERS" department tables parsed (surname-first, noisy layout) to assign departments to former people and to add presence years.
* Wayback CDX: `iitg_faculty_details*` has 10,807 captures (about 508 distinct profile names, 2021-2026); not used as tenure evidence (profile pages may stay captured after a person leaves). Old department sites (iitg.ac.in/<dept>/faculty.php etc., 2016-2020) were discovered through a domain CDX query (list in `data/wb/cdx_dom_faculty.json`), but Wayback answered very slowly (shared 3 s slot, one CDX query per ~30 minutes), so the old per-department list pages were NOT fetched (see gaps).
* ORCID: offline index `iit_guwahati_orcid_index.tsv` only (employments rows; role faculty-like, or blank role with matching department; name strongly compatible with >=2 full name tokens). No live ORCID API calls.

## 4. How status, tenure and years were established
* current: on the institute faculty list (list wins over NIRF); "Emeritus Professor" on the list -> emeritus. Further current: NIRF 2026 "currently working", professorial designation, no leaving date, not on the list (13 people, department blank unless found in AR).
* former: in NIRF 2018-2025 but not currently working / not in NIRF 2026 and not on the list. FIRST = earliest NIRF joining date year (may be a re-joining/regularisation date; could precede 2016), else first evidence year. LAST = year of the NIRF leaving date if given, else (last NIRF edition with the person) minus 1, or annual-report fiscal-year start year if later. Because NIRF editions are annual with a gap (2021 PDF unreadable), LAST can be 1 year early (cluster at edition-1 values such as 2024 for people present in NIRF 2025 but absent in 2026).
* visiting: NIRF "Visiting" association, or all-NIRF designation "Other" with blank/visiting association (foreign visiting scholars, e.g. Ken Ono, Meyya Meyyappan). Designation = "Visiting faculty (Y1-Y2)"; for these, LAST = NIRF edition year (capped at 2026). Honorary / adjunct people listed in the annual report (70+: 8 Professor of Practice, 7 VF, 6 AF, 53 HP, 6 DP in 2024-25) have no names in the sources used, so `adjunct` has 0 rows (gap).
* joining_year only from NIRF joining dates (earliest across editions) - no profile page prints a joining year. For visiting rows it is the NIRF visiting start.
* Window: people evidenced only before 2016 dropped; FY 2015-16 annual-report-only people were dropped (FY ends March 2016).

## 5. Identifier counts by route
* ORCID: affiliation-record route (offline index) 276; institute-page route 0; live API route 0. 7 people have several qualifying iDs and were left blank: Shaik Rafi Ahamed, Sachin Kumar, Manish Kumar, Anil Mahanta, Anamika Barua, Rohini Mokashi-Punekar, Dipankar Mandal. ORCID lookup pending: none queued (live API not used at all).
* IRINS 416 / homepage 412 / e-mail 473 from the profile pages (e-mail de-obfuscated from "x @ iitg . ac. in").

## 6. Problems, ambiguity, decisions
* The AJAX list is POST-driven; GET on the endpoint returns everything (used as is).
* Name matching across NIRF editions/list: custom matcher (initials, "Kr"=Kumar, prefix/fuzzy tokens, joined-string ratio); two-pass (exact token set first). Hand merges: Dipankar Mondal (NIRF) = Dipankar Mandal (list); Reshmi Suresh SP (NIRF 2022-25) = Resmi Suresh (list); Karl F Mac Dorman = MacDorman; Saurav Geol = Goel.
* Two different people named Gautam Barua exist: current Civil Engineering Professor (list) and the former (1995-2019, left 17-04-2019, apparently the CSE professor/IIIT-G director); NIRF rows were assigned to the former, joining_year of the current one left blank.
* "Manish Kumar" (BSBE) and "Manish Kumar Goyal" (Civil, former) are different people; likewise "Selvaraju Narayanasamy" (BSBE) vs "N. Selvaraju" (Mathematics) assumed different.
* Duplicate list entries (Manoj B R, Sriram Bhyravarapu) each appear twice (one entry without unit); kept once.
* NIRF 2018-2020 designations carry an age column glued to the designation; stripped. NIRF names may be surname-first (e.g. "Garg Ankit"); kept as printed.
* Excluded 72 NIRF-only "Other"/Regular people as presumed non-faculty (see section 2).
* Skipped by design: associated/affiliated faculty of centres.

## 7. Known gaps
* Former faculty are certainly under-counted (65): the old (2016-2020) department faculty pages on Wayback were not fetched; people who joined and left, or left before the NIRF 2018 data (2016-2017 leavers), appear only when listed in annual-report tables (added by hand: J. S. Sahambi, Jaideep Chatterjee, Subrata Kumar Mazumdar; many other AR-only names, e.g. Zakir Hussain Rather, Samarjit Das, Anupam Saxena, Basudev Chatterji, evidenced only in FY 2015-16, were not added). NIRF 2021 is missing, so leavers between the 2020 and 2022 editions have LAST up to 1 year off.
* Retirees/leavers of 2025 and 2026 may carry LAST = 2024 (edition minus 1).
* Honorary/adjunct/visiting names not in NIRF are absent; visiting rows have no unit.
* Annual-report department assignment is heuristic (majority department of matched section); 11 former and 12 current rows have no unit.
* No Google Scholar/DBLP/Scopus identifiers; 12 current people lack a profile page entry with a unit (NIRF-only or failed detail fetch).

## 8. Brief issues
* The brief asks for per-year Wayback snapshots of department faculty lists; Wayback throughput on the shared slot was too low to complete them (one CDX query per ~30 minutes under load), so the former-faculty pass is NIRF + annual-report based, not Wayback based.
* "Include NIRF-only people" conflicts with "exclude non-faculty": 73 NIRF-2026 "Other" designation people were excluded; included only if the reviewer decides otherwise.
* NIRF 2021 PDFs are scans (no OCR tool run).
