# IIT Indore (iit_indore) faculty roster, 2016-2026: lab notebook

Output: `rosters/iit_indore_faculty.csv` (302 rows). Built from NIRF data submissions (spine), Wayback snapshots of department faculty pages 2016-2026, annual reports, and live department pages / one JSON endpoint. No git writes, all fetches through the shared polite fetcher.

## Size check and per-unit extraction against NIRF (first, as requested)

| source | number |
|---|---|
| NIRF 2026 "Faculty Details" table (Overall, submitted late 2025), rows | 229 |
| of which Currently working = Yes | 225 (Regular 213, Visiting 9, Adhoc/Contractual 3) |
| Annual report 2024-25, faculty positions as of 31-3-2025 | 212 (regular posts) |
| This roster: current (regular, website/NIRF) | 229 |
| of which NIRF-2026-confirmed (Regular, working=Yes) | 213 |
| current not in NIRF 2026 (on a 2026 department page only: new joiners after the submission, Chemical Engineering core members, MFSOS core members, CE 2025 page) | 16 |
| visiting / adjunct rows | 31 / 8 (12 of them NIRF-2026 working=Yes: 9 Visiting + 3 Adhoc, all three Adhoc rows have designation Professor and became `adjunct`) |

The 213 regular working rows in NIRF 2026 are all in the roster as `current` (0 missing); 212 in the annual report agrees to within 1. The 16 extra current people are on the live department pages but not in the NIRF table (it was submitted before they joined, or the institute left them out). NIRF Faculty tables do not carry a department, so per-unit NIRF comparison is impossible; the table below is the unit split of this roster (what each department page yielded), compared to the NIRF total above.

| unit (current name) | current | visiting | adjunct | former |
|---|---|---|---|---|
| Electrical Engineering | 24 | 0 | 0 | 3 |
| Computer Science and Engineering | 21 | 3 | 1 | 3 |
| Mathematics | 21 | 1 | 0 | 4 |
| Metallurgical Engineering and Materials Science (MEMS) | 21 | 0 | 0 | 2 |
| Physics | 20 | 0 | 0 | 4 |
| Chemistry | 19 | 0 | 0 | 2 |
| Biosciences and Biomedical Engineering | 15 | 0 | 0 | 4 |
| Civil Engineering | 15 | 3 | 2 | 4 |
| Humanities and Social Sciences | 15 | 0 | 0 | 3 |
| Mechanical Engineering | 13 | 1 | 0 | 3 |
| Chemical Engineering (new department, JSON API) | 12 | 4 | 0 | 0 |
| Mehta Family School of Sustainability | 8 | 0 | 0 | 0 |
| Astronomy, Astrophysics and Space Engineering | 6 | 1 | 2 | 1 |
| department blank (NIRF-only people, see gaps) | 19 | 17 | 3 | 2 |

Sum of current = 229. Units found on the website but without own rows: Centre for Advanced Electronics (CAE), CEVITS, CRDT, JPN centre, School of Innovation, Center of Futuristic Defense and Space Technology. Their listed people are members of other departments (EE, Mechanical, BSBE ...); per the "associated faculty never create membership" rule they never set a person's department (a person seen only on a centre page has a blank department).

Known undercounts: Mechanical (13 vs the AR/NIRF experience of about 25 in 2026) and AASE (6 vs about 10 per AR 2023-24), HSS: their current department pages were not obtainable (see problems), so most of their members sit in the blank-department row (19 current with no department).

## Sources and endpoints

1. NIRF data submissions, "Overall" PDFs linked from `https://www.iiti.ac.in/about/ranking` (`/uploads/nirf_data/2026/{Mar,Apr}/<hash>.pdf`), NIRF 2018-2026 downloaded. Faculty Details tables (name, designation, joining date, leaving date, currently working, association type) exist for 2021-2026 only: 171, 171, 205, 204, 229, 229 rows (working=Yes: 166, 165, 195, 195, 222, 225); the 2018, 2019 and 2020 PDFs are two-page summaries without a faculty table. Parsed with `pdftotext -layout` and a regex per year (`code/nirf.py`); column layout changes between years (age column 2021-2025, wrapped names/designations); row counts equal the last serial number in all six years. 277 persons after entity merge (norm. of names, 4 manual merges for truncated/misspelt names).
2. Department faculty pages (live, archived): CSE `faculty.html` (2016-18), `faculty.php`, `faculty-members.js` (Vue data file, parsed `name:` entries), `formar-faculty-members.js` (former faculty WITH years), `Visiting-faculty-members.js`, `past_faculty.html`; EE `faculty.html` (2016-2024) and `people/faculty` (Next.js RSC payload, 2026-03); Physics `page3.html` (2016-17), `faculty.html` (2018-21), `faculty/` (2022-26); Chemistry `faculty.htm(l)` and `people/faculty/`; Civil `faculty.php`, `afaculty.php` (adjunct), `vfaculty.php` (visiting); MEMS `faculty.html`; BSBE `faculty.php`; Mathematics `faculty.html`, `faculty/`, `former/`; HSS `People_faculty.php` (2025-26); CRDT `faculty/`; Mechanical `me.iiti.ac.in/Faculty.html` (2016). 198 snapshots saved, about two per year per page (last capture before 30 June and last of the year, from the CDX list with host filters). The CDX call used `matchType` host queries with a URL regex filter, listings kept under `data/cdxf_*.json`.
3. Live pages: `chemical.iiti.ac.in/api/faculty` (JSON endpoint called by the Vite page; core / visiting / advisory categories), MFSOS `faculty1.php`, CAE `main/faculty`, CEVITS `faculty-members/`, BSBE `main/faculty`, HSS `People_faculty.php`, Mathematics `people/` (pages saved by the golden-set agent, reused).
4. Old institute-wide list `www.iiti.ac.in/people/people.php` (Wayback 2018-07-14): per-discipline faculty with designation and e-mail (116 entries, incomplete for Chemistry, Physics, Civil).
5. Annual reports 2016-17 .. 2024-25 (saved by the golden agent, reused): joiner tables with department and joining date for 2018-19, 2019-20, 2020-21 (66 parsed rows, all matched to roster persons, used as department fallback and cross-check) and "relieved" lists for 2022-23, 2023-24, 2024-25 with dates (Murthy deputation 2022-07, Chaudhari deputation 2022-09 and superannuation 2025-03-31, Garain 2023-02-24, Sarkar 2023-05-11, Mishra 2023-07-15, Ghosh 2023-10-27, Mandal 2023-12-29, Chanda 2024-07-22, Balakrishnan 2024-08-17, Boda 2024-09-02, Gupta 2024-09-22), all consistent with NIRF leaving dates. AR 2016-17 and 2021-22 are scanned images (no text).
6. ORCID: offline index `work/orcid_index/iit_indore_orcid_index.tsv` only (no live API calls).
Not used: IRINS, Scopus, OpenAlex, Google Scholar.

## How tenure and status were established

* Entity resolution: names normalised (titles, punctuation, initials), matched by token sets with an initial-expansion rule and a conservative fuzzy rule; common surnames (Kumar, Singh ...) never match alone. Manual aliases: Md./Mohammad Aquil Khan, Sanjram Premjit Khanganba = Premjit Khangamba Sanjram, Anand Parkash = Anand Prakash, Anupam Pal Choudhary = Anupampal Choudhury, Munir Ahmad/Ahmed Nayak. "M. Ashok Kumar" (Mathematics, left) is kept separate from Ashok Kumar Mocherla (HSS, NIRF join 2018) although the names collide.
* Status: NIRF 2026 working=Yes and Regular -> `current`; Visiting association -> `visiting`; Adhoc/Contractual with designation Professor -> `adjunct`; department-page-only people: on a 2026 (or mid-2025-or-later for maintained pages) department page -> current; CSE former-faculty file and archived lists otherwise -> `former`; designations containing Visiting/Adjunct/Honorary -> that status. Nobody is `emeritus` in the evidence found.
* former tenure: FIRST = min(NIRF joining year, first archived listing year); LAST = NIRF leaving-date year when working=No, otherwise the year of the last NIRF row minus 1 (NIRF year Y is submitted in autumn of Y-1) or the last archived listing, whichever is later. Archived pages after a documented leaving date were not used.
* joining_year only from NIRF joining dates (257 rows). They may be regularisation/rejoining dates: 13 people were on an archived list earlier than their NIRF joining date (e.g. Abhijeet Joshi 2016 vs 2018, Kiran Bala 2016 vs 2017, M. Tanveer 2016 vs 2017, Hem Chandra Jha, Mirza Saqib Baig, Parasharam Shirage, Parimal Kar, Sunil Kumar Boda 2017 vs 2018, Manoneeta Chakraborty and Srimanta Pakhira 2018 vs 2019, Charitha Cherugondi 2016 vs 2020, Santanu Manna 2016 vs 2019). For these the designation FIRST year is the archived first year and joining_year keeps the NIRF date. The Charitha Cherugondi and Santanu Manna cases look like different earlier postings or a name collision (Santanu Manna is listed on Mathematics 2016-17 and Civil 2018 pages; AR 2019-20 gives joining 20-Sep-2019 in Mathematics) and are uncertain.
* Window: undated former lists (Mathematics "Former Faculty Members": K.D. Joshi, G. A. Patwardhan, M. G. Nadkarni (visiting), V. N. Dogga) and CSE former members with years only before 2016 (Monalisa Sarma 2011-2013, Sushmita Ruj 2011-2013), and Tanima Dutta (no dates) were excluded.
* Tie-break "current": there is no institute-wide current list reachable (directory.iiti.ac.in answers 403 to the fetcher); NIRF 2026 plays that role. No conflicts found between NIRF and department pages, other than differing name spellings.

## Identifiers

* ORCID: 135 of 302 rows, all from the offline "ORCID affiliation record" route (kind=employments; same name; role not intern/student/scholar; department compatible, or exact name match with 3+ name tokens). 0 from the live API (quota; not needed, but no per-person lookups were done for the remaining people: ORCID lookup pending for the 167 rows without a match). One person with two qualifying iDs left blank: Rajesh Kumar (0000-0001-7977-986X and 0009-0009-5442-2114). Matches for very common names with one hit (e.g. Amit Kumar, Sunil Kumar) carry some namesake risk although department compatibility was required.
* e-mail: 141 rows (from department pages, only when the local part resembles the name). google_scholar, dblp, scopus_id, irins, homepage, profile_url left blank (not collected from institute pages in this pass).

## Problems and how they were handled

* Most department sites (physics, chemistry, ce, cse, ee, meche, aase, directory) answer 403 with a SafeLine challenge to the fetcher: not bypassed; Wayback copies used instead. `me.iiti.ac.in` has a broken TLS chain (DEAD).
* `meche.iiti.ac.in` is not in the Wayback CDX at all (empty result) and `aase.iiti.ac.in` pages are JavaScript shells without names: Mechanical has only the 2016 `me.iiti.ac.in/Faculty.html` and the 2018 institute list, AASE only the 2018 list. HSS `people.html` (2016-2020) is an iframe shell with no names. Hence the weak coverage of leavers 2016-2020 in these three units.
* SPA departments: Chemical Engineering (Vite, solved via `/api/faculty`), MEMS (CRA bundle without a data endpoint; Wayback `faculty.html` 2016-2023 used), EE 2025/26 (Next.js; RSC payload parsed).
* Two CSE Wayback captures (`faculty-members.js` 2022, 2024) returned ConnectionError; other captures cover the same years.
* Snapshot dates in file names for the Physics `page3.html` fetches are the requested dates (Wayback served the nearest capture).
* The Chemical Engineering API lists "advisory" members (Khakhar, Gudi, Y. M. Joshi, ...) and staff: only core, HOD and visiting categories were taken.
* NIRF persons with designation "Other" and association "Other" or "Visiting" (project scientists / postdocs / guest staff; 25 people, e.g. Anjali Rao, E G Rini, Rajkumar Hajra, Tonmay Ghosh) were excluded as non-faculty; NIRF "Visiting Professor" rows kept as `visiting`.
* Pradeep Mathur (Director until 2019, Chemistry professor) is `former` (2010-2019) with designation Director; Narendra S. Chaudhari: 2009-2025, deputation 2022, superannuated 2025-03-31, `former`.

## Ambiguous people

* Sanjram Premjit Khanganba: BSBE page 2016-2021, HSS 2018-2026; one row, primary unit = latest listing (HSS).
* M. Anbarasu: listed on EE and MEMS pages 2016-2018; row under MEMS (latest sighting).
* Pritee Sharma, Manish Kumar Goyal, Kiran Bala, Saurabh Das: now core members of the Mehta Family School of Sustainability (MFSOS); the row's unit is MFSOS. Maitreya Natu: CSE 2016-17, later on the CSE "former" page as Assistant Professor-Adjunct (no dates): `adjunct`, range 2016-2017 (last uncertain, can be later).
* Anurag Mehra: joint HSS / Chemical Engineering visiting; one row (Chemical Engineering).
* Visiting Advanced Joint Research (VAJRA) adjuncts of Civil (Surampalli, Reddy): `adjunct`.

## Known gaps

1. 19 current and 22 visiting/adjunct/former rows have a blank department (NIRF has no department; no 2026 department page for Mechanical, AASE, MEMS (stale after 2023), CE (2026 capture unparseable), HSS history). Each is a real NIRF-listed faculty member.
2. Former faculty 2016-2020 are probably under-covered in Mechanical, AASE and HSS (no archived lists); in the other units the 2016-2020 lists are the only source. Annual-report joiner tables are not complete lists of leavers (AR 2018-19/2019-20 give counts of relieved faculty, 5 and 5, without names), so people who joined and left between archived snapshots (2016-2020) can be missing.
3. Last year of former people who left before NIRF 2021 rests on the last archived list (snapshots were dense about every 6 months), so can be one half-year late.
4. Emeritus / Institute Chair / Distinguished professors: not found as a separate list; none recorded.
5. ORCID lookup pending for rows without an index match; scholar/dblp/scopus/irins/homepage not collected.
