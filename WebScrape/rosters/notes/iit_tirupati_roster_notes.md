# IIT Tirupati faculty roster (2016–2026): lab notebook

Built 2026-10-25/26. Output: `WebScrape/rosters/iit_tirupati_faculty.csv` (248 rows). Every fetch went through the shared
`polite_get.py` (rate-limited, cached). Downloaded pages and parsing scripts are in the session scratchpad
(`work/iit_tirupati_roster/data` and `.../code`), not in the repo.

## Totals

| status | rows | joining_year filled | ORCID | Google Scholar | e-mail |
|---|---|---|---|---|---|
| current | 139 | 139 | 85 | 22 | 139 |
| former | 25 | 24 | 9 | 3 | 9 |
| visiting | 72 | 39 | 0 | 0 | 17 |
| adjunct | 12 | 7 | 0 | 1 | 12 |
| **total** | **248** | **209** | **94** | **26** | **177** |

Visiting breakdown: NIRF "Other" 5, guest / visiting / other 42, mentor (IIT Madras) 25.

| department | current | former | visiting | adjunct |
|---|---|---|---|---|
| (not printed; NIRF-only) | 0 | 0 | 5 | 0 |
| Chemical Engineering | 15 | 2 | 1 | 1 |
| Chemistry | 14 | 3 | 7 | 1 |
| Civil and Environmental Engineering | 18 | 5 | 8 | 0 |
| Computer Science and Engineering | 13 | 3 | 10 | 1 |
| Ecology and Environment (course, listed under faculty/others) | 0 | 0 | 3 | 0 |
| Electrical Engineering | 19 | 2 | 3 | 4 |
| Entrepreneurship, Innovation & Incubation | 0 | 0 | 1 | 0 |
| Humanities and Social Sciences | 11 | 4 | 9 | 1 |
| Life Sciences (courses, listed under faculty/others) | 0 | 0 | 2 | 0 |
| Mathematics and Statistics | 13 | 2 | 9 | 0 |
| Mechanical Engineering | 22 | 0 | 13 | 3 |
| Physics | 14 | 4 | 1 | 1 |

Identifier counts: ORCID 94 (institute/department profile pages 4, ORCID API affiliation search + employment check 90, ORCID API name search + employment check 0), Google Scholar 26, DBLP 0, Scopus 0, IRINS 0, homepage 17, profile_url 158.

Unit names are the current official ones as used on the institute site: "Civil and Environmental Engineering" (2016-2019 pages:
"Civil Engineering"), "Mathematics and Statistics" (2016-2020 pages: "Mathematics"), "Computer Science and Engineering" (2017-18 URL
"computer-science-department"). There is no separate management/design school; the Master of Public Policy is run by Humanities and
Social Sciences. Pseudo-units used for people the institute lists under `people/faculty/others`: "Life Sciences (courses ...)",
"Ecology and Environment (course ...)" and "Entrepreneurship, Innovation & Incubation". Both campuses (transit campus near Renigunta
until ~2022, permanent campus at Yerpedu since) are covered: the institute always had one faculty list per department, not per campus.
Second units: none are printed on the current site (one row per person was never ambiguous). K. Krishnaiah was listed under Chemical
Engineering and (2015-16) under "Concepts in Engineering & Design" / Mechanical; primary unit Chemical Engineering.

## Sources and endpoints

1. **Current lists (live site).** `https://www.iittp.ac.in/` is a React single-page app (index HTML is an empty shell). The faculty
   lists are not served by an API: they are hard-coded arrays inside the JS bundle `https://www.iittp.ac.in/static/js/main.c5692a0b.js`
   (3.4 MB). The routes `/people/faculty/<dept>` redirect to `/<dept>` (e.g. `/chemistry-department`), whose components map arrays
   `{Name, NameLink, Position, Email, ...}` under h3 headings ("Head of the Department", "Faculty", "Visiting Faculty", "Adjunct Faculty",
   "Professors of Practice", "Guest Faculty", "Former Faculty"; `/people/faculty/others`: "Entrepreneurship, Innovation & Incubation",
   "LifeSciences"). They were extracted with a small JS-literal parser (no JS execution): 173 entries, 139 in Faculty/HoD sections.
   * Profile pages `/<slug>` (e.g. `/dr-arijit-sharma`) are rendered from `https://iittp.ac.in/api/faculty/<slug>`. That endpoint
     **timed out repeatedly** (no response within 90 s, 6 retries; another agent saw the same), so profile data could not be read live.
     `profile_url` therefore points at the SPA route `https://www.iittp.ac.in/<slug>` (or the department profile) as printed.
   * Department sites: `cse/cee/chemical/hss/mech/cy.iittp.ac.in` all return an identical "Website Under Maintenance" page (not a bot
     wall); `ee.iittp.ac.in/Faculty.html` (+ 18 `Faculty_*.html` profiles), `physics.iittp.ac.in/{RegularFaculty,FormerFaculty,VisitingFaculty}.html`
     (+ 15 `Dr*.html` profiles) and `mast.iittp.ac.in/People-Faculty.html`, `People-GuestFaculty.html` were live and used
     (lists cross-checked against the main site: no person on them is missing from the main site; Bivas Dutta is absent from both).
2. **NIRF data submissions** (live PDFs, links found in the site bundle): `files.iittp.ac.in/pdfs/nirf/NIRF_Report-2022.pdf`,
   `NIRF_Report-2023.pdf`, `2024/NIRF_Overall_2024.pdf`, `2025/NIRF_Overall_2025.pdf`, `2026/NIRF_Overall_2026.pdf`. Faculty tables
   (name, designation, joining date, leaving date, "currently working", association type) parsed with `pdftotext -layout`
   (107/116/119/124/146 rows; srno sequences complete). Names wrap over several lines and are often reversed or partly abbreviated
   ("GORTHI VRMS SUBRAHMANYAM", "GORTI R K S S MANYAM", "RAVISANKAR M", "P V RAMAN"); all 612 NIRF rows were matched to a roster person
   (automatic token matching plus 45 hand aliases/ignores, `code/aliases.json`) – no NIRF name is unexplained. No NIRF faculty table exists before the 2022 edition.
3. **Annual reports** (links in the site bundle; live PDFs): 2015-16 (`AT-TIP-English.pdf`, first AR, Nov 2016), 2016-17, 2017-18,
   2018-19, 2019-20, 2020-21, 2021-22, 2022-23 (`Annual_Report_2023.pdf`), 2023-24, 2024-25. The "Faculty profile" chapter (department-wise
   "Faculty Members" / "Guest Faculty Members" blocks) and, from 2020-21, the "New faculty and staff entrants" tables were scanned; every
   `Dr./Prof.` cell was matched against the roster (AR-only names were reviewed by hand; staff such as a Medical Officer and a Technical
   Officer were dropped). AR evidence is dated to the **end year of the financial year** (AR 2017-18 → 2018).
4. **Internet Archive.** CDX domain query `cdx?url=iittp.ac.in&matchType=domain&from=2015&to=2026&filter=statuscode:200&filter=original:.*[Ff]acult.*&collapse=urlkey`
   (290 URLs) found four site generations:
   * 2015-2017 WordPress page `iittp.ac.in/faculty/`: all 15 monthly captures (2015-11 … 2017-06) fetched.
   * 2017-2018 Joomla pages `iittp.ac.in/people/faculty/{chemistry,civil-engineering,computer-science-department,electrical-engineering-department,humanities-and-social-sciences,mathematics,mechanical-engineering-department,physics,chemical-engineering,others}`: ~2 per year (first capture + latest per half-year), 2017-07 … 2018-12.
   * 2020-2024 server-rendered pages `iittp.ac.in/people/faculty/*-department` (+ `others`): first capture 2020-11 and the latest per half-year to 2024-03/04 (8–12 per page). From 2024-04 the same URLs return the SPA shell (≈1 kB).
   * 2024-2026 SPA: the CDX prefix query `iittp.ac.in/static/js/` lists 592 archived `main.*.js` bundles; one per quarter was fetched
     (2024-06, 2024-09, 2024-12, 2025-03, 2025-06, 2025-09, 2025-12, 2026-03, 2026-07, 2026-09) and parsed like the live bundle.
   * Archive gap: **no capture of any faculty list between 2019-01 and 2020-10** (only the home page); ARs 2018-19 … 2020-21 and NIRF 2022 cover it.
   * 132 list snapshots + 10 bundles were fetched as raw `id_` captures. HTML comments were stripped before parsing: the 2018-2024 pages
     keep departed people inside `<!-- -->` blocks (e.g. Sarvagya Dwivedi, EE, never visible), which must not count as presence.
   * Archived server-rendered profile pages `iittp.ac.in/dr-<slug>` (2020-2024; CDX prefix `iittp.ac.in/dr-`, 117 slugs with an HTML
     capture) were fetched for identifiers, prioritising former faculty and current faculty without ORCID (63 fetched; the shared
     Wayback slot was very slow, see Problems).
5. **ORCID public API.** `expanded-search/?q=affiliation-org-name:"Indian Institute of Technology Tirupati"` (551 records, 3 pages of 200)
   and `affiliation-org-name:"IIT Tirupati"` (27) → 572 unique iDs. Roster names were matched to these (token match, initials checked),
   giving 100 candidate iDs; each was checked with `/v3.0/<id>/employments` and accepted only if an employment organisation is IIT Tirupati
   (name "Indian Institute of Technology"/"IIT" + Tirupati), the role is not a student/scholar/postdoc/project role, the name matches, and
   exactly one iD survives for the person. 10 candidates were rejected by hand (different person or student; listed in `assemble.py`).
   For 73 regular faculty without a candidate, `given-and-family-names:"<name>"` searches were run (59 plausible iDs checked); **none**
   had an IIT Tirupati employment entry, so the name-search route contributed 0. (The first day's attempt hit the anonymous daily quota –
   HTTP 429 – and was redone the next day.)

## Status and classification rules applied

* **current** = in a Faculty/HoD section of the live site bundle (139). The institute-wide site is the only institute list; department
  sites agree with it (EE/physics/maths live pages checked; conflicts below).
* **former** = held a faculty post (regular, contract, full-time visiting, INSPIRE, re-employed retired professor) at some point and is
  not on the current site, or is on a department "Former Faculty" list (Sampath, Deshmukh, Natarajan).
* **visiting**: (a) *Mentor faculty from IIT Madras* – serving IIT Madras faculty who taught as visiting/guest faculty (2015-2019 mainly,
  plus Neelesh Upadhye 2020-21, C. Pandu Rangan, and the current guests K. Vidyasagar and G. L. Samuel); (b) guest faculty that the
  institute lists on its faculty pages / AR faculty chapter / NIRF (retired IITM professors, S. V. University, ISI, IISER Tirupati etc.);
  (c) KSMS Raghavarao (site section "Visiting Faculty"; NIRF calls him Regular Professor since 2020); (d) five people known only as NIRF
  faculty rows with association "Other" (no unit or designation printed); (e) Hiranmayee Vedam (Senior Project Advisor, listed on
  `people/faculty/others`).
* **adjunct**: "Adjunct Faculty" and "Professors of Practice" sections, plus V R Ganesan (printed as "Professor of Practice" inside the
  Mechanical guest list).
* Re-employed retired professors (K. Krishnaiah, N. N. Kishore, V. Raghavendra, T. S. Natarajan, P. C. Deshmukh; AR 2016-17: "five
  senior Professors recently retired from IIT Kanpur and IIT Madras have been re-employed") held posts at IIT Tirupati, so they are
  regular faculty (former), except N. N. Kishore who is currently listed as Adjunct (status adjunct).
* **Window**: people listed only in Nov–Dec 2015 would be excluded; every 2015 name also appears in Jan 2016 or later, so none was dropped.

## Former faculty and tenure years

* FIRST = earliest year with evidence from any source (NIRF joining date, faculty-page capture year, AR end-year, bundle year);
  values < 2016 (2015) occur for the founding group, as the brief allows.
* LAST (in this order): NIRF leaving date; otherwise the latest of: faculty-list capture, JS bundle, AR end-year, NIRF "currently
  working" (edition E → E-1, the NIRF data year, as in the Palakkad roster). For guests and mentors, captures of the 2017-2024
  department pages' guest sections were **not** used for LAST when they post-date all AR/NIRF/bundle evidence, because those sections
  were never pruned (e.g. P. R. Parthasarathy still listed in 2023) even though the faculty sections were maintained (new joiners added,
  leavers commented out).
* Every NIRF 2022-2026 name and every AR 2015-16 … 2024-25 faculty-chapter name was matched to a roster person: no unexplained
  leftovers. Former faculty found: 25.

## Joining year (never guessed)

* NIRF joining date (earliest across editions) is the default.
* **Earlier documented appointment wins**: NIRF gives 23-06-2017 … 10-07-2017 (regularisation) for the 2016 contract cohort; their first
  listing on the 2016 faculty page is used (Nithyadharan, Subrahmanyam Gorthi, Madan Mohan Avulapati, N. Venkaiah, S. Rajesh 2016;
  Sridhar Chimalakonda, Janaki Ramaiah, V. Mahendran, Ishapathik Das 2017 as visiting faculty before their 2018 regular date;
  A. Raghuramaraju 2017 vs NIRF contract date 2020).
* First appearance on an archived list is used only when the previous capture of the same list is ≤ 9 months older (7 new 2025-26
  joiners, from the quarterly JS bundles).
* K. N. Satyanarayana: 2015 (Professor-in-Charge from 2015, AR 2015-16; Director since 18-01-2017).
* Mentor faculty from IIT Madras: joining_year left blank (mentoring excluded). Guests: first listing / NIRF date where available.

## Independent size check

* **NIRF 2026 Overall** (data year 2024-25): 146 faculty rows, 143 "currently working" (Regular 137, Other 4, Visiting 2), 3 left in the
  year (Ashish Kulkarni 15-12-2025, Kaushalya Jhuria 14-05-2025, Shikha Baghel 31-07-2025 – all `former` here).
* **This roster**: 139 `current`. Reconciliation: 131 current are NIRF-2026 Regular-working + A. Raghuramaraju (NIRF "Visiting") = 132; plus 7 joiners of 2025-26 not yet in NIRF 2026 (Bijoy Kumar Das, Payel Sen, Avinash Patsha 2025; Ajay Kumar Kalyani,
  Hemant Kumar Aggarwal, Venkata Sai Charan Putrevu, Lakshmi Ganapathi Kolla 2026) = 139.
  The other NIRF-2026 Regular-working names are 5 people absent from the current site (Saranya Kshatriya, Prabha Shankar Dwivedi,
  Sanchayan Nath, Bivas Dutta, Prasanna Venkatesh Sampath → `former`, flagged) and KSMS Raghavarao (site: Visiting Professor).
  The remaining NIRF "Other"/"Visiting" working rows are Anil Kapoor and V. Vasudeva Rao (adjunct), GSR Murthy (guest), M Shoaib and V I Prasanna Deep (NIRF-only).
* AR 2024-25 states "a team of 134 faculty members" and 27 joiners in 2024-25; AR 2023-24: 114; AR 2022-23: 110 – consistent with
  NIRF regular counts (NIRF 2025: 113 Regular).
* **Conclusion**: the current count matches the institute's own numbers once 2025-26 joiners and the five site/NIRF conflicts are accounted for.

## Problems and decisions

* `iittp.ac.in/api/faculty/<slug>` timed out (not a bot wall) → no live profile data; archived 2020-2024 profiles used for identifiers.
* Six department sub-sites are "under maintenance" → used their Wayback copies only indirectly (main-site archives cover the same lists).
* Wayback was shared by several agents and slow (single profile captures took 2–10 min; several 600-s timeouts). Profile fetching was
  prioritised and time-boxed; remaining profiles are a known gap for identifiers only.
* My own `pkill -f` patterns once matched my shell and killed a fetch loop; it was restarted (cached results reused).
* **Site vs NIRF conflicts** (site wins for status, NIRF used for LAST): Saranya Kshatriya (absent from site since mid-2024, NIRF 2026
  working), Prabha Shankar Dwivedi (on bundles until 2025-12), Sanchayan Nath (bundles until 2024-09), Bivas Dutta (on 2023-11/2024-03
  physics page only), Prasanna Venkatesh Sampath (civil "Former Faculty" section). Any of them may in fact be on leave rather than gone.
* K P Naveen is printed as "Head & Associate Professor" while the EE HoD block shows Prashanth Vooka; designation kept as printed.
  Abhishek Kumar Jha's site e-mail is a Gdańsk University of Technology address (pg.edu.pl); kept as printed.
* K. Vidyasagar's site link points to another IITM professor's page (mangalasunderkrishnan) → not used as homepage.
* Swatantra Pratap Singh appears only on the Dec-2018 civil faculty page (then commented out), never in an AR or NIRF → kept as
  `former (2018-2018)` with a flag; he may have accepted an offer and not joined.
* Hiranmayee Vedam (Senior Project Advisor) is staff-like but listed by the institute on its faculty/others page → included as visiting, flagged.

## Known gaps

* No faculty list capture between 2019-01 and 2020-10; someone who joined and left inside that window and is absent from AR 2018-19,
  AR 2019-20, AR 2020-21 and NIRF 2022 would be missed (none expected: NIRF 2022 lists leavers back to 2020).
* No NIRF faculty table before the 2022 edition; LAST for 2016-2019 leavers rests on captures and ARs.
* Live profile API unavailable; Google Scholar / DBLP / Scopus are sparse (archived and physics/EE profiles only). IRINS deliberately not used.
* 54 current faculty without ORCID (no IIT Tirupati employment on ORCID, or no ORCID).
* Guest faculty lists of 2015-2019 are complete only as far as the faculty pages and ARs printed them; guests who taught single courses
  without being listed are not recoverable.

## ORCID lookup pending

None. Every ORCID API call for this roster had already returned before the quota was exhausted. That is 4 affiliation-search pages, 73 name searches and 159 `/employments` records, and none of the cached responses is a 429. The 54 current faculty without an ORCID were all looked up. They are blank because no ORCID record matched the name with an IIT Tirupati employment, not because a lookup failed.

## Per-person notes

| name | status | note |
|---|---|---|
| Bijoy Kumar Das | current | joining_year: first appearance on archived faculty list 2025-12 (site JS bundle), previous snapshot <=9 months earlier |
| Payel Sen | current | joining_year: first appearance on archived faculty list 2025-06 (site JS bundle), previous snapshot <=9 months earlier |
| B. Janaki Ramaiah | current | joining_year: first appearance on archived faculty list 2017-12 (faculty page), previous snapshot <=9 months earlier; NIRF joining date 12-06-2018 |
| K. N. Satyanarayana | current | joining_year: AR 2015-16: appointed Professor-in-Charge of IIT Tirupati in 2015; Director from 18-01-2017 (NIRF) |
| M. Nithyadharan | current | joining_year: first appearance on archived faculty list 2016-08 (faculty page), previous snapshot <=9 months earlier; NIRF joining date 23-06-2017 |
| Hemant Kumar Aggarwal | current | joining_year: first appearance on archived faculty list 2026-07 (site JS bundle), previous snapshot <=9 months earlier |
| Sridhar Chimalakonda | current | joining_year: first appearance on archived faculty list 2017-05 (faculty page), previous snapshot <=9 months earlier; NIRF joining date 05-06-2018 |
| V. Mahendran | current | joining_year: first appearance on archived faculty list 2017-12 (faculty page), previous snapshot <=9 months earlier; NIRF joining date 01-06-2018 |
| Venkata Sai Charan Putrevu | current | joining_year: first appearance on archived faculty list 2026-07 (site JS bundle), previous snapshot <=9 months earlier |
| Subrahmanyam Gorthi | current | joining_year: first appearance on archived faculty list 2016-09 (faculty page), previous snapshot <=9 months earlier; NIRF joining date 23-06-2017 |
| A Raghuramaraju | current | joining_year: first appearance on archived faculty list 2017-12 (faculty page), previous snapshot <=9 months earlier; NIRF joining date 07-02-2020 |
| Ishapathik Das | current | joining_year: first appearance on archived faculty list 2017-12 (faculty page), previous snapshot <=9 months earlier; NIRF joining date 12-06-2018 |
| S. Rajesh | current | joining_year: Visiting Faculty on Aug-2016 faculty page (earlier Senior Project Officer, a staff post, from Feb 2016); NIRF regular date 23-06-2017 |
| Ajay Kumar Kalyani | current | joining_year: first appearance on archived faculty list 2026-03 (site JS bundle), previous snapshot <=9 months earlier |
| Madan Mohan Avulapati | current | joining_year: first appearance on archived faculty list 2016-08 (faculty page), previous snapshot <=9 months earlier; NIRF joining date 23-06-2017 |
| N. Venkaiah | current | joining_year: first appearance on archived faculty list 2016-08 (faculty page), previous snapshot <=9 months earlier; NIRF joining date 10-07-2017 |
| Avinash Patsha | current | joining_year: first appearance on archived faculty list 2025-12 (site JS bundle), previous snapshot <=9 months earlier |
| Lakshmi Ganapathi Kolla | current | joining_year: first appearance on archived faculty list 2026-07 (site JS bundle), previous snapshot <=9 months earlier |
| K Raghunathan | adjunct | FIRST=2025 from AR 2024-25 faculty list; LAST=2026 from current site, site JS bundle 2026-07, site JS bundle 2026-09; ARs: 2024-25 |
| Chebrolu Pulla Rao | adjunct | FIRST=2019 from NIRF joining date 04-07-2019; LAST=2026 from current site, site JS bundle 2026-03, site JS bundle 2026-07; NIRF: NIRF joining date 04-07-2019; NIRF 2022 "currently working"; NIRF 2023 "currently working"; NIRF 2024 "currently working"; ARs: 2019-20, 2020-21, 2021-22, 2022-23 ; joining_year: NIRF 2022 joining date 04-07-2019 |
| B. Yegnanarayana | adjunct | FIRST=2019 from AR 2018-19 faculty list; LAST=2026 from current site, site JS bundle 2026-03, site JS bundle 2026-07; NIRF: NIRF joining date 01-01-2020; NIRF joining date 04-08-2021; NIRF 2022 "currently working"; NIRF joining date 01-07-2023; NIRF 2024 "currently working"; NIRF 2025 "currently working"; ARs: 2018-19, 2019-20, 2020-21, 2021-22, 2022-23, 2023-24, 2024-25 ; joining_year: NIRF 2022 joining date 01-01-2020 |
| Anil Kapoor | adjunct | FIRST=2022 from NIRF 2023 "currently working", NIRF joining date 10-01-2022; LAST=2026 from current site, site JS bundle 2026-03, site JS bundle 2026-07; NIRF: NIRF joining date 10-01-2022; NIRF 2023 "currently working"; NIRF joining date 01-07-2023; NIRF 2024 "currently working"; NIRF 2025 "currently working"; NIRF 2026 "currently working"; ARs: 2023-24 ; joining_year: NIRF 2023 joining date 10-01-2022 |
| M. V. Kartikeyan | adjunct | FIRST=2020 from NIRF joining date 03-10-2020, faculty page 2020-11; LAST=2026 from current site, site JS bundle 2026-03, site JS bundle 2026-07; NIRF: NIRF joining date 03-10-2020; NIRF 2022 "currently working"; NIRF leaving date 06-10-2022; ARs: 2020-21, 2021-22, 2024-25 ; joining_year: NIRF 2022 joining date 03-10-2020 |
| R. Muralidharan | adjunct | FIRST=2025 from site JS bundle 2025-03, site JS bundle 2025-06, site JS bundle 2025-09; LAST=2026 from current site, site JS bundle 2026-03, site JS bundle 2026-07 |
| Rajesh Langoju | adjunct | FIRST=2025 from site JS bundle 2025-12; LAST=2026 from current site, site JS bundle 2026-03, site JS bundle 2026-07 |
| C. Rajendran | adjunct | FIRST=2025 from site JS bundle 2025-12; LAST=2026 from current site, site JS bundle 2026-03, site JS bundle 2026-07 |
| Ahmad Al-Mallahi | adjunct | FIRST=2024 from AR 2023-24 faculty list, site JS bundle 2024-09, site JS bundle 2024-12; LAST=2026 from current site, site JS bundle 2026-03, site JS bundle 2026-07; ARs: 2023-24 |
| N. N. Kishore | adjunct | FIRST=2016 from AR 2015-16 faculty list, faculty page 2016-02, faculty page 2016-03; LAST=2026 from current site, site JS bundle 2026-03, site JS bundle 2026-07; NIRF: NIRF joining date 01-07-2019; NIRF 2022 "currently working"; NIRF joining date 01-07-2022; NIRF 2023 "currently working"; NIRF joining date 01-07-2023; NIRF 2024 "currently working"; NIRF 2025 "currently working"; ARs: 2015-16, 2016-17, 2017-18, 2018-19, 2019-20, 2020-21, 2021-22, 2022-23, 2023-24, 2024-25 ; joining_year: first appearance on archived faculty list 2016-02 (faculty page), previous snapshot <=9 months earlier; NIRF joining date 01-07-2019 |
| V R Ganesan | adjunct | FIRST=2021 from NIRF joining date 19-08-2021; LAST=2026 from current site, site JS bundle 2026-03, site JS bundle 2026-07; NIRF: NIRF joining date 19-08-2021; NIRF 2023 "currently working"; NIRF joining date 01-07-2023; NIRF 2024 "currently working"; NIRF 2025 "currently working"; ARs: 2022-23, 2023-24, 2024-25 ; joining_year: NIRF 2023 joining date 19-08-2021 |
| V Vasudeva Rao | adjunct | FIRST=2024 from NIRF 2025 "currently working", NIRF joining date 01-01-2024, site JS bundle 2024-06; LAST=2026 from current site, site JS bundle 2026-03, site JS bundle 2026-07; NIRF: NIRF joining date 01-01-2024; NIRF 2025 "currently working"; NIRF 2026 "currently working"; ARs: 2024-25 ; joining_year: NIRF 2025 joining date 01-01-2024 |
| B. Vamsi Krishna | visiting | FIRST=2021 from NIRF 2022 "currently working", NIRF joining date 01-01-2021; LAST=2021 from NIRF 2022 "currently working", NIRF joining date 01-01-2021; NIRF: NIRF joining date 01-01-2021; NIRF 2022 "currently working" ; joining_year: NIRF 2022 joining date 01-01-2021 |
| D. Venkat Reddy | visiting | FIRST=2021 from NIRF joining date 01-07-2021, NIRF leaving date 31-12-2021; LAST=2021 from NIRF joining date 01-07-2021, NIRF leaving date 31-12-2021; NIRF: NIRF joining date 01-07-2021; NIRF leaving date 31-12-2021 ; joining_year: NIRF 2022 joining date 01-07-2021 |
| M Shoaib | visiting | FIRST=2024 from NIRF joining date 01-08-2024; LAST=2025 from NIRF 2026 "currently working"; NIRF: NIRF joining date 01-08-2024; NIRF 2026 "currently working" ; joining_year: NIRF 2026 joining date 01-08-2024 |
| Shatakumar Mohan | visiting | FIRST=2020 from NIRF joining date 01-07-2020, NIRF leaving date 31-12-2020; LAST=2020 from NIRF joining date 01-07-2020, NIRF leaving date 31-12-2020; NIRF: NIRF joining date 01-07-2020; NIRF leaving date 31-12-2020 ; joining_year: NIRF 2022 joining date 01-07-2020 |
| V I Prasanna Deep | visiting | FIRST=2024 from NIRF joining date 01-08-2024; LAST=2025 from NIRF 2026 "currently working"; NIRF: NIRF joining date 01-08-2024; NIRF 2026 "currently working" ; joining_year: NIRF 2026 joining date 01-08-2024 |
| KSMS Raghavarao | visiting | FIRST=2020 from NIRF joining date 07-10-2020, faculty page 2020-11; LAST=2026 from current site, site JS bundle 2026-03, site JS bundle 2026-07; NIRF: NIRF joining date 07-10-2020; NIRF 2022 "currently working"; NIRF 2023 "currently working"; NIRF 2024 "currently working"; NIRF 2025 "currently working"; NIRF 2026 "currently working"; ARs: 2020-21, 2021-22, 2022-23, 2023-24, 2024-25 ; joining_year: NIRF 2022 joining date 07-10-2020 |
| G. Ranga Rao | visiting | FIRST=2015 from faculty page 2015-11, faculty page 2015-12; LAST=2017 from AR 2016-17 faculty list, faculty page 2017-05, faculty page 2017-06; ARs: 2015-16, 2016-17 ; legacy department pages (2017-2024) kept listing this guest after the last AR/NIRF/JS-bundle evidence; those stale listings were not used for LAST |
| K. K. Balasubramanian | visiting | FIRST=2015 from faculty page 2015-11, faculty page 2015-12; LAST=2017 from AR 2016-17 faculty list, faculty page 2017-05, guest/visiting section 2017-06; ARs: 2015-16, 2016-17 ; legacy department pages (2017-2024) kept listing this guest after the last AR/NIRF/JS-bundle evidence; those stale listings were not used for LAST ; joining_year: first appearance on archived faculty list 2015-11 (faculty page), previous snapshot <=9 months earlier |
| K. Mangala Sunder | visiting | FIRST=2016 from faculty page 2016-08, faculty page 2016-09, faculty page 2016-10; LAST=2017 from AR 2016-17 faculty list, faculty page 2017-05, faculty page 2017-06; ARs: 2016-17 ; legacy department pages (2017-2024) kept listing this guest after the last AR/NIRF/JS-bundle evidence; those stale listings were not used for LAST |
| K. Vidyasagar | visiting | site link points to another person's page; not used ; FIRST=2022 from guest/visiting section 2022-12; LAST=2026 from current site, site JS bundle 2026-03, site JS bundle 2026-07 |
| M. N. Sudheendra Rao | visiting | FIRST=2016 from AR 2015-16 faculty list, faculty page 2016-01, faculty page 2016-02; LAST=2017 from AR 2016-17 faculty list, faculty page 2017-05, guest/visiting section 2017-06; ARs: 2015-16, 2016-17 ; legacy department pages (2017-2024) kept listing this guest after the last AR/NIRF/JS-bundle evidence; those stale listings were not used for LAST ; joining_year: first appearance on archived faculty list 2016-01 (faculty page), previous snapshot <=9 months earlier |
| S. Subramanian | visiting | FIRST=2015 from faculty page 2015-11, faculty page 2015-12; LAST=2017 from faculty page 2017-05, guest/visiting section 2017-06, guest/visiting section 2017-07; ARs: 2015-16 ; legacy department pages (2017-2024) kept listing this guest after the last AR/NIRF/JS-bundle evidence; those stale listings were not used for LAST ; joining_year: first appearance on archived faculty list 2015-11 (faculty page), previous snapshot <=9 months earlier |
| Vijayamohanan K Pillai | visiting | FIRST=2022 from guest/visiting section 2022-12; LAST=2026 from current site, site JS bundle 2026-03, site JS bundle 2026-07 ; joining_year: first appearance on archived faculty list 2022-12 (faculty page), previous snapshot <=9 months earlier |
| B. S. Murty | visiting | FIRST=2017 from AR 2016-17 faculty list, guest/visiting section 2017-07, guest/visiting section 2017-12; LAST=2017 from AR 2016-17 faculty list, guest/visiting section 2017-07, guest/visiting section 2017-12; ARs: 2016-17 ; legacy department pages (2017-2024) kept listing this guest after the last AR/NIRF/JS-bundle evidence; those stale listings were not used for LAST |
| J. Karthekeyan | visiting | FIRST=2017 from AR 2016-17 faculty list; LAST=2018 from AR 2017-18 faculty list; ARs: 2016-17, 2017-18 |
| Kalai Selvi | visiting | FIRST=2016 from faculty page 2016-08, faculty page 2016-09, faculty page 2016-11; LAST=2026 from current site, site JS bundle 2026-03, site JS bundle 2026-07; NIRF: NIRF joining date 01-01-2020; NIRF 2022 "currently working"; ARs: 2016-17, 2017-18, 2018-19, 2019-20 ; joining_year: first appearance on archived faculty list 2016-08 (faculty page), previous snapshot <=9 months earlier; NIRF joining date 01-01-2020 |
| Manu Santhanam | visiting | FIRST=2018 from AR 2017-18 faculty list; LAST=2018 from AR 2017-18 faculty list; ARs: 2017-18 |
| R. G. Robinson | visiting | FIRST=2017 from AR 2016-17 faculty list, faculty page 2017-05, faculty page 2017-06; LAST=2017 from AR 2016-17 faculty list, faculty page 2017-05, faculty page 2017-06; ARs: 2016-17 ; legacy department pages (2017-2024) kept listing this guest after the last AR/NIRF/JS-bundle evidence; those stale listings were not used for LAST |
| Radhakrishna G. Pillai | visiting | FIRST=2016 from faculty page 2016-08, faculty page 2016-09, faculty page 2016-10; LAST=2017 from AR 2016-17 faculty list, faculty page 2017-05, faculty page 2017-06; ARs: 2016-17 ; legacy department pages (2017-2024) kept listing this guest after the last AR/NIRF/JS-bundle evidence; those stale listings were not used for LAST |
| T. V. Krishna Reddy | visiting | FIRST=2020 from AR 2019-20 faculty list; LAST=2020 from AR 2019-20 faculty list; ARs: 2019-20 |
| Vidya Bhushan Maji | visiting | FIRST=2017 from AR 2016-17 faculty list, faculty page 2017-05, faculty page 2017-06; LAST=2017 from AR 2016-17 faculty list, faculty page 2017-05, faculty page 2017-06; ARs: 2016-17 ; legacy department pages (2017-2024) kept listing this guest after the last AR/NIRF/JS-bundle evidence; those stale listings were not used for LAST |
| Anil R Nair | visiting | FIRST=2020 from AR 2019-20 faculty list; LAST=2026 from current site, site JS bundle 2026-03, site JS bundle 2026-07; ARs: 2019-20, 2024-25 ; joining_year: first appearance on archived faculty list 2022-05 (faculty page), previous snapshot <=9 months earlier |
| C. Pandu Rangan | visiting | FIRST=2017 from AR 2016-17 faculty list, guest/visiting section 2017-07, guest/visiting section 2017-12; LAST=2021 from NIRF 2022 "currently working", NIRF joining date 04-01-2021, guest/visiting section 2021-05; NIRF: NIRF joining date 04-01-2021; NIRF 2022 "currently working"; ARs: 2016-17, 2017-18 ; legacy department pages (2017-2024) kept listing this guest after the last AR/NIRF/JS-bundle evidence; those stale listings were not used for LAST |
| C. S. Rahul | visiting | FIRST=2016 from faculty page 2016-08, faculty page 2016-09, faculty page 2016-11; LAST=2017 from AR 2016-17 faculty list, faculty page 2017-05, guest/visiting section 2017-06; ARs: 2016-17 ; legacy department pages (2017-2024) kept listing this guest after the last AR/NIRF/JS-bundle evidence; those stale listings were not used for LAST ; joining_year: first appearance on archived faculty list 2016-08 (faculty page), previous snapshot <=9 months earlier |
| N. S. Narayanaswamy | visiting | FIRST=2015 from faculty page 2015-11, faculty page 2015-12; LAST=2017 from AR 2016-17 faculty list, faculty page 2017-05, faculty page 2017-06; ARs: 2015-16, 2016-17 ; legacy department pages (2017-2024) kept listing this guest after the last AR/NIRF/JS-bundle evidence; those stale listings were not used for LAST |
| Noor Mohamed | visiting | FIRST=2022 from guest/visiting section 2022-12; LAST=2026 from current site, site JS bundle 2026-03, site JS bundle 2026-07 ; joining_year: first appearance on archived faculty list 2022-12 (faculty page), previous snapshot <=9 months earlier |
| P. Sreenivasa Kumar | visiting | FIRST=2016 from faculty page 2016-08, faculty page 2016-09, faculty page 2016-10; LAST=2017 from AR 2016-17 faculty list, faculty page 2017-05, faculty page 2017-06; ARs: 2016-17 ; legacy department pages (2017-2024) kept listing this guest after the last AR/NIRF/JS-bundle evidence; those stale listings were not used for LAST |
| S. Lakshmivarahan | visiting | FIRST=2022 from guest/visiting section 2022-05, guest/visiting section 2022-12; LAST=2026 from current site, site JS bundle 2026-03, site JS bundle 2026-07; ARs: 2024-25 ; joining_year: first appearance on archived faculty list 2022-05 (faculty page), previous snapshot <=9 months earlier |
| Srinivas Padmanabhuni | visiting | FIRST=2019 from AR 2018-19 faculty list; LAST=2026 from current site, site JS bundle 2026-03, site JS bundle 2026-07; NIRF: NIRF joining date 01-01-2021; NIRF 2022 "currently working"; ARs: 2018-19, 2019-20, 2024-25 ; joining_year: NIRF 2022 joining date 01-01-2021 |
| Venkatesh Raman | visiting | FIRST=2022 from guest/visiting section 2022-12; LAST=2026 from current site, site JS bundle 2026-03, site JS bundle 2026-07 ; joining_year: first appearance on archived faculty list 2022-12 (faculty page), previous snapshot <=9 months earlier |
| W. I. Suresh Kumar | visiting | FIRST=2017 from AR 2016-17 faculty list, faculty page 2017-05, guest/visiting section 2017-06; LAST=2017 from AR 2016-17 faculty list, faculty page 2017-05, guest/visiting section 2017-06; ARs: 2016-17 ; legacy department pages (2017-2024) kept listing this guest after the last AR/NIRF/JS-bundle evidence; those stale listings were not used for LAST ; joining_year: first appearance on archived faculty list 2017-05 (faculty page), previous snapshot <=9 months earlier |
| Jayasree Venkatesan | visiting | FIRST=2017 from AR 2016-17 faculty list, guest/visiting section 2017-07, guest/visiting section 2017-12; LAST=2017 from AR 2016-17 faculty list, guest/visiting section 2017-07, guest/visiting section 2017-12; ARs: 2016-17 ; legacy department pages (2017-2024) kept listing this guest after the last AR/NIRF/JS-bundle evidence; those stale listings were not used for LAST ; joining_year: first appearance on archived faculty list 2017-12 (faculty page), previous snapshot <=9 months earlier |
| Nandini Rajamani | visiting | FIRST=2018 from AR 2017-18 faculty list; LAST=2018 from AR 2017-18 faculty list; ARs: 2017-18 |
| Robin V. | visiting | FIRST=2018 from AR 2017-18 faculty list; LAST=2018 from AR 2017-18 faculty list; ARs: 2017-18 |
| Bijoy Krishna Das | visiting | FIRST=2018 from AR 2017-18 faculty list; LAST=2019 from AR 2018-19 faculty list; ARs: 2017-18, 2018-19 |
| K. M. M. Prabhu | visiting | FIRST=2016 from faculty page 2016-08, faculty page 2016-09, faculty page 2016-11; LAST=2019 from AR 2018-19 faculty list; ARs: 2016-17, 2018-19 ; joining_year: first appearance on archived faculty list 2016-08 (faculty page), previous snapshot <=9 months earlier |
| R. Sundar | visiting | FIRST=2016 from faculty page 2016-09, faculty page 2016-10, faculty page 2016-11; LAST=2018 from AR 2017-18 faculty list, guest/visiting section 2018-06, guest/visiting section 2018-12; ARs: 2016-17, 2017-18 ; joining_year: first appearance on archived faculty list 2016-09 (faculty page), previous snapshot <=9 months earlier |
| Hiranmayee Vedam | visiting | FIRST=2018 from guest/visiting section 2018-11; LAST=2026 from current site, site JS bundle 2026-03, site JS bundle 2026-07 ; joining_year: first appearance on archived faculty list 2018-11 (faculty page), previous snapshot <=9 months earlier |
| Arniker Hamsa | visiting | FIRST=2017 from AR 2016-17 faculty list, guest/visiting section 2017-07, guest/visiting section 2017-12; LAST=2026 from current site, site JS bundle 2026-03, site JS bundle 2026-07; NIRF: NIRF joining date 01-01-2021; NIRF 2022 "currently working"; ARs: 2016-17, 2024-25 ; joining_year: first appearance on archived faculty list 2017-12 (faculty page), previous snapshot <=9 months earlier; NIRF joining date 01-01-2021 |
| Devaki Reddy | visiting | FIRST=2016 from faculty page 2016-08, faculty page 2016-09, faculty page 2016-10; LAST=2017 from AR 2016-17 faculty list, faculty page 2017-05, faculty page 2017-06; ARs: 2016-17 ; legacy department pages (2017-2024) kept listing this guest after the last AR/NIRF/JS-bundle evidence; those stale listings were not used for LAST |
| M. H. Rao | visiting | FIRST=2018 from AR 2017-18 faculty list; LAST=2018 from AR 2017-18 faculty list; ARs: 2017-18 |
| O.G.P. Kalyana Sastry | visiting | FIRST=2018 from guest/visiting section 2018-12; LAST=2026 from current site, site JS bundle 2026-03, site JS bundle 2026-07; NIRF: NIRF joining date 01-01-2021; NIRF 2022 "currently working"; ARs: 2024-25 ; joining_year: first appearance on archived faculty list 2018-12 (faculty page), previous snapshot <=9 months earlier; NIRF joining date 01-01-2021 |
| Prema Rajagopalan | visiting | FIRST=2016 from faculty page 2016-08, faculty page 2016-09, faculty page 2016-10; LAST=2017 from AR 2016-17 faculty list, faculty page 2017-05, faculty page 2017-06; ARs: 2016-17 ; legacy department pages (2017-2024) kept listing this guest after the last AR/NIRF/JS-bundle evidence; those stale listings were not used for LAST |
| Sabuj Kumar Mandal | visiting | FIRST=2016 from faculty page 2016-08, faculty page 2016-09, faculty page 2016-10; LAST=2018 from AR 2017-18 faculty list, guest/visiting section 2018-06; ARs: 2016-17, 2017-18 |
| Srikanth Reddy | visiting | FIRST=2018 from AR 2017-18 faculty list; LAST=2018 from AR 2017-18 faculty list; ARs: 2017-18 |
| T. Sreenivasa Reddy | visiting | FIRST=2015 from faculty page 2015-12; LAST=2016 from faculty page 2016-01, faculty page 2016-02, faculty page 2016-03 ; joining_year: first appearance on archived faculty list 2015-12 (faculty page), previous snapshot <=9 months earlier |
| Vedaparayana | visiting | FIRST=2017 from AR 2016-17 faculty list, guest/visiting section 2017-07, guest/visiting section 2017-12; LAST=2018 from AR 2017-18 faculty list, guest/visiting section 2018-06, guest/visiting section 2018-12; ARs: 2016-17, 2017-18 ; legacy department pages (2017-2024) kept listing this guest after the last AR/NIRF/JS-bundle evidence; those stale listings were not used for LAST ; joining_year: first appearance on archived faculty list 2017-12 (faculty page), previous snapshot <=9 months earlier |
| Ambrish Saxena | visiting | FIRST=2021 from guest/visiting section 2021-05, guest/visiting section 2021-12; LAST=2026 from current site, site JS bundle 2026-03, site JS bundle 2026-07 ; joining_year: first appearance on archived faculty list 2021-05 (faculty page), previous snapshot <=9 months earlier |
| Mousumi Banerjee | visiting | FIRST=2016 from faculty page 2016-09, faculty page 2016-11, guest/visiting section 2016-10; LAST=2026 from current site, site JS bundle 2026-03, site JS bundle 2026-07; ARs: 2016-17, 2017-18, 2018-19 ; joining_year: first appearance on archived faculty list 2016-09 (faculty page), previous snapshot <=9 months earlier |
| G. Ravindran | visiting | FIRST=2017 from AR 2016-17 faculty list; LAST=2021 from NIRF 2022 "currently working", guest/visiting section 2021-12; NIRF: NIRF joining date 01-07-2020; NIRF 2022 "currently working"; ARs: 2016-17, 2017-18, 2019-20 ; legacy department pages (2017-2024) kept listing this guest after the last AR/NIRF/JS-bundle evidence; those stale listings were not used for LAST ; joining_year: NIRF 2022 joining date 01-07-2020 |
| GSR Murthy | visiting | FIRST=2022 from guest/visiting section 2022-05; LAST=2026 from current site, site JS bundle 2026-03, site JS bundle 2026-07; NIRF: NIRF joining date 01-08-2024; NIRF 2026 "currently working"; ARs: 2024-25 ; joining_year: first appearance on archived faculty list 2022-05 (faculty page), previous snapshot <=9 months earlier; NIRF joining date 01-08-2024 |
| Kuntal Som | visiting | FIRST=2022 from guest/visiting section 2022-05; LAST=2022 from guest/visiting section 2022-05 ; joining_year: first appearance on archived faculty list 2022-05 (faculty page), previous snapshot <=9 months earlier |
| N. Egambaram | visiting | FIRST=2020 from NIRF joining date 01-07-2020; LAST=2021 from NIRF leaving date 31-12-2021, guest/visiting section 2021-12; NIRF: NIRF joining date 01-07-2020; NIRF leaving date 31-12-2021 ; legacy department pages (2017-2024) kept listing this guest after the last AR/NIRF/JS-bundle evidence; those stale listings were not used for LAST ; joining_year: NIRF 2022 joining date 01-07-2020 |
| Neelesh S. Upadhye | visiting | FIRST=2020 from AR 2019-20 faculty list, NIRF joining date 01-07-2020; LAST=2021 from NIRF leaving date 31-12-2021, guest/visiting section 2021-12; NIRF: NIRF joining date 01-07-2020; NIRF leaving date 31-12-2021; ARs: 2019-20 ; legacy department pages (2017-2024) kept listing this guest after the last AR/NIRF/JS-bundle evidence; those stale listings were not used for LAST |
| P. R. Parthasarathy | visiting | FIRST=2015 from faculty page 2015-11, faculty page 2015-12; LAST=2017 from faculty page 2017-05, guest/visiting section 2017-06, guest/visiting section 2017-07; ARs: 2015-16 ; legacy department pages (2017-2024) kept listing this guest after the last AR/NIRF/JS-bundle evidence; those stale listings were not used for LAST ; joining_year: first appearance on archived faculty list 2015-11 (faculty page), previous snapshot <=9 months earlier |
| R. Usha | visiting | FIRST=2017 from AR 2016-17 faculty list, faculty page 2017-05, faculty page 2017-06; LAST=2024 from guest/visiting section 2024-03, site JS bundle 2024-06; ARs: 2016-17 |
| S. G. Kamath | visiting | FIRST=2015 from faculty page 2015-11, faculty page 2015-12; LAST=2019 from AR 2018-19 faculty list; ARs: 2015-16, 2016-17, 2017-18, 2018-19 ; legacy department pages (2017-2024) kept listing this guest after the last AR/NIRF/JS-bundle evidence; those stale listings were not used for LAST ; joining_year: first appearance on archived faculty list 2015-11 (faculty page), previous snapshot <=9 months earlier |
| Sudheesh Kumar Kattumannil | visiting | FIRST=2020 from NIRF joining date 01-07-2020; LAST=2024 from guest/visiting section 2024-03, site JS bundle 2024-06; NIRF: NIRF joining date 01-07-2020; NIRF 2022 "currently working" ; joining_year: NIRF 2022 joining date 01-07-2020 |
| Dhiman Chatterjee | visiting | FIRST=2017 from AR 2016-17 faculty list, faculty page 2017-05, guest/visiting section 2017-06; LAST=2017 from AR 2016-17 faculty list, faculty page 2017-05, guest/visiting section 2017-06; ARs: 2016-17 ; legacy department pages (2017-2024) kept listing this guest after the last AR/NIRF/JS-bundle evidence; those stale listings were not used for LAST |
| G. L. Samuel | visiting | FIRST=2022 from guest/visiting section 2022-05, guest/visiting section 2022-12; LAST=2026 from current site, site JS bundle 2026-03, site JS bundle 2026-07 |
| G. Venkatarathnam | visiting | FIRST=2016 from AR 2015-16 faculty list, faculty page 2016-02, faculty page 2016-03; LAST=2017 from AR 2016-17 faculty list, faculty page 2017-05, guest/visiting section 2017-06; ARs: 2015-16, 2016-17 ; legacy department pages (2017-2024) kept listing this guest after the last AR/NIRF/JS-bundle evidence; those stale listings were not used for LAST |
| K. L. Narayana | visiting | FIRST=2015 from faculty page 2015-11, faculty page 2015-12; LAST=2026 from current site, site JS bundle 2026-03, site JS bundle 2026-07; ARs: 2015-16, 2016-17, 2017-18, 2018-19, 2019-20 ; joining_year: first appearance on archived faculty list 2015-11 (faculty page), previous snapshot <=9 months earlier |
| K. Ramamurthi | visiting | FIRST=2018 from AR 2017-18 faculty list; LAST=2018 from AR 2017-18 faculty list; ARs: 2017-18 |
| Manoj Pandey | visiting | FIRST=2017 from AR 2016-17 faculty list, faculty page 2017-05, guest/visiting section 2017-06; LAST=2017 from AR 2016-17 faculty list, faculty page 2017-05, guest/visiting section 2017-06; ARs: 2016-17 ; legacy department pages (2017-2024) kept listing this guest after the last AR/NIRF/JS-bundle evidence; those stale listings were not used for LAST |
| P. K. Ghosh | visiting | FIRST=2022 from guest/visiting section 2022-05, guest/visiting section 2022-12; LAST=2026 from current site, site JS bundle 2026-03, site JS bundle 2026-07 ; joining_year: first appearance on archived faculty list 2022-05 (faculty page), previous snapshot <=9 months earlier |
| Prasad Patnaik B. S. V. | visiting | FIRST=2016 from faculty page 2016-08, faculty page 2016-09, faculty page 2016-10; LAST=2019 from AR 2018-19 faculty list; ARs: 2016-17, 2018-19 |
| S. Kumaraswamy | visiting | FIRST=2018 from AR 2017-18 faculty list; LAST=2018 from AR 2017-18 faculty list; ARs: 2017-18 |
| Shyama Prasad Das | visiting | FIRST=2017 from AR 2016-17 faculty list, faculty page 2017-05, guest/visiting section 2017-06; LAST=2017 from AR 2016-17 faculty list, faculty page 2017-05, guest/visiting section 2017-06; ARs: 2016-17 ; legacy department pages (2017-2024) kept listing this guest after the last AR/NIRF/JS-bundle evidence; those stale listings were not used for LAST |
| Somashekhar S. H. | visiting | FIRST=2018 from AR 2017-18 faculty list; LAST=2018 from AR 2017-18 faculty list; ARs: 2017-18 |
| Suresh Varadarajan | visiting | FIRST=2020 from AR 2019-20 faculty list; LAST=2026 from current site, site JS bundle 2026-03, site JS bundle 2026-07; NIRF: NIRF joining date 01-01-2021; NIRF leaving date 30-06-2021; ARs: 2019-20 ; joining_year: NIRF 2022 joining date 01-01-2021 |
| V. Raghavan | visiting | FIRST=2016 from AR 2015-16 faculty list, faculty page 2016-02, faculty page 2016-03; LAST=2017 from AR 2016-17 faculty list, faculty page 2017-05, guest/visiting section 2017-06; ARs: 2015-16, 2016-17 ; legacy department pages (2017-2024) kept listing this guest after the last AR/NIRF/JS-bundle evidence; those stale listings were not used for LAST |
| Suresh Kumar Rayala | visiting | FIRST=2020 from AR 2019-20 faculty list; LAST=2021 from NIRF 2022 "currently working", NIRF joining date 01-01-2021; NIRF: NIRF joining date 01-01-2021; NIRF 2022 "currently working"; ARs: 2019-20 ; joining_year: NIRF 2022 joining date 01-01-2021 |
| K. Krishnaiah | former | Emeritus Professor IIT Madras in 2015-16; re-employed Professor from 01-07-2016 (NIRF 2022); later listed as Adjunct Faculty (Chemical Engg) until Dec 2024 ; FIRST=2015 from faculty page 2015-11, faculty page 2015-12; LAST=2024 from site JS bundle 2024-06, site JS bundle 2024-09, site JS bundle 2024-12; NIRF: NIRF joining date 01-07-2016; NIRF 2022 "currently working"; ARs: 2015-16, 2016-17, 2018-19, 2019-20, 2020-21, 2021-22 ; joining_year: first appearance on archived faculty list 2015-11 (faculty page), previous snapshot <=9 months earlier; NIRF joining date 01-07-2016 |
| R. Harikrishnan | former | Associate Professor & Head (AR 2018-19, 2019-20) ; FIRST=2019 from AR 2018-19 faculty list; LAST=2020 from AR 2019-20 faculty list; ARs: 2018-19, 2019-20 |
| Ashish Kulkarni | former | FIRST=2025 from AR 2024-25 faculty list, NIRF joining date 03-03-2025, NIRF leaving date 15-12-2025; LAST=2025 from AR 2024-25 faculty list, NIRF joining date 03-03-2025, NIRF leaving date 15-12-2025; NIRF: NIRF joining date 03-03-2025; NIRF leaving date 15-12-2025; ARs: 2024-25 ; joining_year: NIRF 2026 joining date 03-03-2025 |
| Kumar Swamy Reddy N | former | DST-INSPIRE Faculty ; FIRST=2021 from AR 2020-21 faculty list, NIRF joining date 08-01-2021, faculty page 2021-05; LAST=2024 from NIRF 2025 "currently working"; NIRF: NIRF joining date 08-01-2021; NIRF 2023 "currently working"; NIRF joining date 13-05-2023; NIRF 2025 "currently working"; ARs: 2020-21, 2021-22 ; joining_year: NIRF 2023 joining date 08-01-2021 |
| Somrita Ray | former | DST-INSPIRE Faculty ; FIRST=2021 from AR 2020-21 faculty list, NIRF joining date 11-01-2021, faculty page 2021-05; LAST=2024 from NIRF 2025 "currently working", faculty page 2024-03; NIRF: NIRF joining date 11-01-2021; NIRF 2023 "currently working"; NIRF 2025 "currently working"; ARs: 2020-21, 2021-22 ; joining_year: NIRF 2023 joining date 11-01-2021 |
| Abhijit Ganguli | former | FIRST=2017 from NIRF joining date 24-07-2017, faculty page 2017-12; LAST=2022 from AR 2021-22 faculty list; NIRF: NIRF joining date 24-07-2017; NIRF 2022 "currently working"; ARs: 2017-18, 2018-19, 2019-20, 2020-21, 2021-22 ; joining_year: NIRF 2022 joining date 24-07-2017 |
| B. Radhika | former | DST-INSPIRE Faculty ; FIRST=2017 from faculty page 2017-12; LAST=2021 from NIRF 2022 "currently working", faculty page 2021-05, faculty page 2021-12; NIRF: NIRF joining date 01-07-2019; NIRF 2022 "currently working"; ARs: 2017-18, 2018-19, 2019-20 ; joining_year: first appearance on archived faculty list 2017-12 (faculty page), previous snapshot <=9 months earlier; NIRF joining date 01-07-2019 |
| Prasanna Venkatesh Sampath | former | FIRST=2016 from faculty page 2016-08, faculty page 2016-09, faculty page 2016-10; LAST=2025 from AR 2024-25 faculty list, NIRF 2026 "currently working", site JS bundle 2025-03; NIRF: NIRF joining date 23-06-2017; NIRF 2022 "currently working"; NIRF 2023 "currently working"; NIRF 2024 "currently working"; NIRF 2025 "currently working"; NIRF 2026 "currently working"; ARs: 2016-17, 2017-18, 2018-19, 2019-20, 2020-21, 2021-22, 2022-23, 2023-24, 2024-25 ; joining_year: first appearance on archived faculty list 2016-08 (faculty page), previous snapshot <=9 months earlier; NIRF joining date 23-06-2017 ; CONFLICT: NIRF 2026 says "currently working" but the person is absent from the current institute site; treated as former, LAST from NIRF data year |
| Romanbabu Oinam | former | NIRF name: Oinam Romanbabu Meetei ; FIRST=2018 from NIRF joining date 20-06-2018, faculty page 2018-12; LAST=2021 from AR 2020-21 faculty list, NIRF 2022 "currently working", NIRF leaving date 15-12-2021; NIRF: NIRF joining date 20-06-2018; NIRF leaving date 15-12-2021; NIRF 2022 "currently working"; ARs: 2018-19, 2019-20, 2020-21 ; joining_year: NIRF 2022 joining date 20-06-2018 |
| Swatantra Pratap Singh | former | listed only on the Dec-2018 civil faculty page (later commented out); not in any AR or NIRF; may never have joined ; FIRST=2018 from faculty page 2018-12; LAST=2018 from faculty page 2018-12 ; joining_year: first appearance on archived faculty list 2018-12 (faculty page), previous snapshot <=9 months earlier |
| G. Ravi Prakash Iyer | former | Full-time Visiting Faculty / Visiting Professor ; FIRST=2018 from AR 2017-18 faculty list, faculty page 2018-06, faculty page 2018-12; LAST=2022 from AR 2021-22 faculty list, faculty page 2022-05; ARs: 2017-18, 2018-19, 2019-20, 2020-21, 2021-22 ; joining_year: first appearance on archived faculty list 2018-06 (faculty page), previous snapshot <=9 months earlier |
| Konda Reddy Mopuri | former | Full-time Visiting Faculty (NIRF association 'Visiting') ; FIRST=2020 from NIRF joining date 05-08-2020, faculty page 2020-11; LAST=2021 from AR 2020-21 faculty list, NIRF 2022 "currently working", NIRF leaving date 20-12-2021; NIRF: NIRF joining date 05-08-2020; NIRF leaving date 20-12-2021; NIRF 2022 "currently working"; ARs: 2020-21, 2021-22 ; joining_year: NIRF 2022 joining date 05-08-2020 |
| Sk Subidh Ali | former | FIRST=2016 from faculty page 2016-09, faculty page 2016-10, faculty page 2016-11; LAST=2017 from AR 2016-17 faculty list, faculty page 2017-05, faculty page 2017-06; ARs: 2016-17 ; joining_year: first appearance on archived faculty list 2016-09 (faculty page), previous snapshot <=9 months earlier |
| Sai Kiran Oruganti | former | FIRST=2016 from faculty page 2016-08, faculty page 2016-09, faculty page 2016-10; LAST=2017 from AR 2016-17 faculty list, faculty page 2017-05, guest/visiting section 2017-06; ARs: 2016-17 ; joining_year: first appearance on archived faculty list 2016-08 (faculty page), previous snapshot <=9 months earlier |
| Shikha Baghel | former | FIRST=2024 from NIRF joining date 06-12-2024; LAST=2025 from AR 2024-25 faculty list, NIRF leaving date 31-07-2025, site JS bundle 2025-03; NIRF: NIRF joining date 06-12-2024; NIRF leaving date 31-07-2025; ARs: 2024-25 ; joining_year: NIRF 2026 joining date 06-12-2024 |
| Prabha Shankar Dwivedi | former | FIRST=2017 from NIRF joining date 07-08-2017, faculty page 2017-12; LAST=2025 from AR 2024-25 faculty list, NIRF 2026 "currently working", site JS bundle 2025-03; NIRF: NIRF joining date 07-08-2017; NIRF 2022 "currently working"; NIRF 2023 "currently working"; NIRF 2024 "currently working"; NIRF 2025 "currently working"; NIRF 2026 "currently working"; ARs: 2017-18, 2018-19, 2019-20, 2020-21, 2021-22, 2022-23, 2023-24, 2024-25 ; joining_year: NIRF 2022 joining date 07-08-2017 ; CONFLICT: NIRF 2026 says "currently working" but the person is absent from the current institute site; treated as former, LAST from NIRF data year |
| Sanchayan Nath | former | FIRST=2021 from NIRF joining date 08-07-2021, faculty page 2021-12; LAST=2025 from NIRF 2026 "currently working"; NIRF: NIRF joining date 08-07-2021; NIRF 2023 "currently working"; NIRF 2024 "currently working"; NIRF 2025 "currently working"; NIRF 2026 "currently working"; ARs: 2021-22, 2022-23, 2023-24 ; joining_year: NIRF 2023 joining date 08-07-2021 ; CONFLICT: NIRF 2026 says "currently working" but the person is absent from the current institute site; treated as former, LAST from NIRF data year |
| Saranya Kshatriya | former | FIRST=2018 from NIRF joining date 17-08-2018, faculty page 2018-12; LAST=2025 from NIRF 2026 "currently working"; NIRF: NIRF joining date 17-08-2018; NIRF 2022 "currently working"; NIRF 2023 "currently working"; NIRF 2024 "currently working"; NIRF 2025 "currently working"; NIRF 2026 "currently working"; ARs: 2018-19, 2019-20, 2020-21, 2021-22, 2022-23 ; joining_year: NIRF 2022 joining date 17-08-2018 ; CONFLICT: NIRF 2026 says "currently working" but the person is absent from the current institute site; treated as former, LAST from NIRF data year |
| V. Vamshi Krishna Reddy | former | FIRST=2017 from faculty page 2017-12; LAST=2021 from AR 2020-21 faculty list; ARs: 2017-18, 2018-19, 2019-20, 2020-21 ; joining_year: first appearance on archived faculty list 2017-12 (faculty page), previous snapshot <=9 months earlier |
| Sumit Giri | former | FIRST=2018 from NIRF joining date 03-09-2018, faculty page 2018-12; LAST=2022 from AR 2021-22 faculty list, NIRF leaving date 28-10-2022, faculty page 2022-05; NIRF: NIRF joining date 03-09-2018; NIRF 2022 "currently working"; NIRF leaving date 28-10-2022; ARs: 2018-19, 2019-20, 2020-21, 2021-22 ; joining_year: NIRF 2022 joining date 03-09-2018 |
| V. Raghavendra | former | Retired IIT Kanpur professor re-employed at IIT Tirupati (AR 2016-17) ; FIRST=2016 from NIRF joining date 01-08-2016, faculty page 2016-08, faculty page 2016-09; LAST=2021 from AR 2020-21 faculty list, NIRF 2022 "currently working", NIRF leaving date 31-12-2021; NIRF: NIRF joining date 01-08-2016; NIRF leaving date 31-12-2021; NIRF 2022 "currently working"; ARs: 2016-17, 2017-18, 2018-19, 2019-20, 2020-21, 2021-22 ; joining_year: NIRF 2022 joining date 01-08-2016 |
| Bivas Dutta | former | FIRST=2023 from NIRF joining date 22-08-2023, faculty page 2023-11; LAST=2025 from NIRF 2026 "currently working"; NIRF: NIRF joining date 22-08-2023; NIRF 2025 "currently working"; NIRF 2026 "currently working" ; joining_year: NIRF 2025 joining date 22-08-2023 ; CONFLICT: NIRF 2026 says "currently working" but the person is absent from the current institute site; treated as former, LAST from NIRF data year |
| Kaushalya Jhuria | former | FIRST=2024 from NIRF joining date 20-12-2024; LAST=2025 from AR 2024-25 faculty list, NIRF leaving date 14-05-2025, site JS bundle 2025-03; NIRF: NIRF joining date 20-12-2024; NIRF leaving date 14-05-2025; ARs: 2024-25 ; joining_year: NIRF 2026 joining date 20-12-2024 |
| P. C. Deshmukh | former | Retired IIT Madras professor re-employed at IIT Tirupati from 2016 (AR 2016-17); later listed as adjunct; physics dept 'Former Faculty' page ; FIRST=2015 from faculty page 2015-11, faculty page 2015-12; LAST=2024 from AR 2023-24 faculty list, NIRF 2025 "currently working", guest/visiting section 2024-03; NIRF: NIRF joining date 01-07-2019; NIRF 2022 "currently working"; NIRF joining date 01-05-2022; NIRF 2023 "currently working"; NIRF joining date 01-07-2023; NIRF 2024 "currently working"; NIRF 2025 "currently working"; ARs: 2015-16, 2016-17, 2017-18, 2018-19, 2019-20, 2020-21, 2021-22, 2022-23, 2023-24 ; joining_year: first appearance on archived faculty list 2015-11 (faculty page), previous snapshot <=9 months earlier; NIRF joining date 01-07-2019 |
| T. S. Natarajan | former | Retired IIT Madras professor re-employed at IIT Tirupati (AR 2015-16: 're-employed at IIT Tirupati'); NIRF 2023 left 28-03-2022 ; FIRST=2015 from faculty page 2015-11, faculty page 2015-12; LAST=2022 from AR 2021-22 faculty list, NIRF leaving date 28-03-2022, guest/visiting section 2022-05; NIRF: NIRF joining date 11-08-2016; NIRF 2022 "currently working"; NIRF leaving date 28-03-2022; ARs: 2015-16, 2016-17, 2017-18, 2018-19, 2019-20, 2020-21, 2021-22 ; joining_year: first appearance on archived faculty list 2015-11 (faculty page), previous snapshot <=9 months earlier; NIRF joining date 11-08-2016 |

