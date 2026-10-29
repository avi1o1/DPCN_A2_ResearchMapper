# IIT Dharwad roster, lab notebook (built 2026-10-28)

Output: `WebScrape/rosters/iit_dharwad_faculty.csv`, 209 rows: current 96, former 20, visiting 75, adjunct 18 (emeritus 0).
Scripts and downloaded pages are under `scratchpad/work/iit_dharwad_roster/{code,data}` and the golden-set folder `work/iit_dharwad_golden/data` (reused). All fetches went through the shared `polite_get.py`.

## Sources and endpoints
* Institute site (Drupal): `https://www.iitdh.ac.in/faculty` (131 cards, reused from the golden-set fetch of 2026-10-26, parsed in `fac.json`), `https://iitdh.ac.in/former-faculty` (35 names, with "(Former)" designation and unit but no dates), `/user-profile/<slug>` profile pages.
* NIRF data submissions (own page `/national-institutional-ranking-framework-nirf`): 2023, 2024, 2025, 2026 PDFs. All four are text PDFs, so `pdftotext -layout` worked and nothing was hand-transcribed. Faculty tables carry joining date, leaving date, currently-working flag and association type.
* Wayback: 41 snapshots of the faculty list, 2017-02 to 2026-06. Patterns: `iitdh.ac.in/faculty.php` (2017, 2019-10 to 2020-12), `faculty_dept.php` (2018-06 to 2023-09), `iitdh.ac.in/faculty` (2024-01 to 2026-06). The CDX listings of the golden agent were reused; I added 26 snapshots (around the years where membership changed). Raw form `/web/<ts>id_/<url>`.
* The 2019-2020 `faculty.php` pages contain a "Visiting Professors" table with the semesters taught (for example "Autumn: 2016-17", "Spring: 2018,2019"). This is the only dated source for the IIT Bombay mentor/visiting faculty and gives their years (49 people).
* Annual reports 2017-18 (faculty profile pages; adds S Sivaji Ganesh, Shyamprasad K, Sushil Mishra as visiting) and the golden notes (Prasanna on the lien from Jul 2017).
* Offline ORCID index (`iit_dharwad_orcid_index.tsv`, 329 employment rows).

## Per-unit extraction vs NIRF (size check)
Site faculty page, current rows by unit (status current): BSBE 6, Chemical 7, Chemistry 7, CIE 6, CSE 13, EECE 21, HEART 5, Maths 6, MMAE 20, Physics 5 = 96. Visiting/adjunct people currently listed add about 40 more rows with status visiting/adjunct.
NIRF 2026 (Regular, "currently working" = Yes): 105 persons; 2025: 104 of 112; 2024: 86; 2023: 66. NIRF 2026 has no unit column, so a per-unit comparison is not possible.
Difference of 105 vs 96 current: NIRF 2026 was submitted on 2025 data and still counts people who have left since (Satavisha Kayal, Vandana Bharti, Shiv Prakash Patel, Narayan Punekar, Pradeep Yammiyavar, Prahlad Joshi and others counted as adjunct or visiting on the site), while the site list adds the Ramanujan/Ramalingaswami fellows. 100 roster rows from the site list are matched to a NIRF 2026 row (every NIRF 2026 name that could not be matched to a site row is a leaver, listed under former). No misparse found: NIRF row numbering ends at 66/86/112/114 and equals my parsed counts.
Excluded from the site's 131 cards: research associates, iPDFs and post-docs (not faculty).

## Method for former faculty and years
* Former = the 35 on the `former-faculty` page, plus people who are on NIRF with a leaving date or "No", plus people found only on archived lists (Laxman Gouda, Narasamma Nipatlapalli, Mahitosh Mandal, Rajesh Mahanand, Nagesh Iyer, P Seshu, Prasenjit Das, Tejas Bodas, R Santhosh, Mandar Patil, Sundar Ram Krishnan, Venkata Krishna Kishore, Rimi Banerjee).
* FIRST = NIRF joining year, else first dated snapshot or course year; LAST = NIRF leaving year, else last snapshot year, else the NIRF data year (NIRF 2023 = 2022, 2024 = 2023, 2025 = 2024, 2026 = 2025).
* `joining_year` is filled for 123 rows: NIRF date for most; own page for Prasanna (2017, golden notes); first archived appearance for Shashwata Ghosh (2025) and Ambarish Kulkarni (2025), stated as upper bounds. Visiting people with no NIRF row (visiting assistant professors, fellows, mentors) are left blank rather than guessed.
* Window rule: people evidenced only before 2016 are not included. Mentors of 2016-17 are included because the course table dates them to 2016-17.

## Identifiers
ORCID: 78 from the offline "ORCID affiliation record" route; 0 from institute pages; 0 from live API (no per-person searches: the offline index was built by affiliation search, so an unmatched person has no IIT Dharwad employment record to accept). Not accepted: Vandana Bharti (ORCID "VANDANA", unit mismatch), "Nikhil" (single name), a student "santosh kumar", "Samartha", and the second hits for Ravi Chandra Dutta (belongs to C Ravikumar) and Piyush Kumar Verma. Ruma Ghosh has two qualifying iDs (0000-0001-8691-5516, 0000-0002-1163-4012): left blank. Added by hand after name variants: Sairam (Sai Ram Boggavarapu), Sandeep R B (RB Sandeep), Shesh Narayan Dhurandar. D Narasimha matches "Delampady Narasimha" with no unit given: accepted on name only. Google Scholar: 18 links from the site cards; homepages 94; DBLP, Scopus, IRINS: none seen on institute pages. Emails 118.
ORCID lookup pending: everyone without an ORCID in the CSV was not searched live.

## Decisions and ambiguous people
* Mentors: IIT Bombay faculty who only taught are `visiting`, designation "Mentor faculty from IIT Bombay (Y1-Y2)". IIT Bombay affiliation was taken from the 2017 mentor list or an `@iitb.ac.in` address on the page; others on the visiting table (for example Khemani, Yegnanarayana, Azeemuddin) keep "Visiting Professor (Y1-Y2)".
* S V Prabhu: listed as "Professor, Mechanical Engineering" 2018-2021 and a mentor in 2017; classified visiting (no evidence of an appointed post). Ambiguous.
* Narayan S Punekar: mentor 2016-17, Visiting Professor and Dean (AP) 2022/23-2025; one row, status visiting, joining 2022 (NIRF). Not on the page now.
* P Seshu (Director) and Nagesh R Iyer (Dean IPS) held posts, so they are `former`. Seshu LAST 2022 (the archived lists to 2023-09 are stale; NIRF 2023 lists him; V R Desai joined 2022-05-30). Uncertain 2022 vs 2023. Iyer NIRF leaving date 2024-01-08.
* S R M Prasanna: on lien as Director IIIT Dharwad but still on the site list, so `current`; NIRF date 2020-03-02 is a later date, 2017 taken from his own page.
* Dhriti Sundar Ghosh: archived 2021-09 list shows "Dhriti S. Ghosh", absent 2022, back 2023; NIRF 2023-03-01. Joining 2021 (earlier documented). Possible rejoining.
* Satavisha Kayal, Vandana Bharti, Shiv Prakash Patel, Jivnesh Sandhan, Pradeep Yammiyavar: current in NIRF 2026 but on the site's former list; treated as former (Jivnesh visiting; Pradeep honorary adjunct, listed until 2026-01).
* NIRF type "Other" (re-employed/contractual): kept as visiting/adjunct by designation (Sarbani Banerjee Belur, Mantrala, Siddhartha Das adjunct; Rajkumar Ram NIRF-only, unit blank, visiting).
* Rimi Banerjee (Ramanujan Fellow, Physics): in the 2026-04 and 2026-06 archived lists, not on the live page; `former` (2026-2026). G Ravindran (visiting) and Akhil Ranjan (adjunct), Mathematics, likewise 2026 only.
* Fellows on the live page (Anmol Kumar, Supriya Rej, Dubey: Ramanujan/Ramalingaswami) are `current` as in Palakkad.
* Name fixes: "VenkappayyA R. dEsAi" -> "Venkappayya R. Desai"; "Group Captain" stripped.
* Units renamed: Electrical Engineering -> EECE, Mechanical Engineering -> MMAE, Humanities and Social Sciences (and English) -> HEART, Civil Engineering -> CIE, Computer Science Engineering -> CSE. Second unit not recorded for anyone. SVD Nageswara Rao (IITB Shailesh J. Mehta School of Management) has a blank unit.
* Not included: Nivedita Kasturi (ORCID "Lecturer, CSE 2017-2018", not on any faculty list), research associates, iPDFs, postdocs, staff.

## Known gaps
* Archive gaps: LAST for former people is the last snapshot where seen; true departure can be up to a year later (about 2 snapshots per year).
* 2017-06 to 2018-05 lists contain mentors only, so first years for 2017 joiners without a NIRF row are not established.
* Mentor years for many mentors come only from the 2019-2020 course table (2016-2020), so earlier or later teaching is not captured.
* Visiting assistant professors currently on the site have no joining year.
* The Dec 2018-Jun 2019 faculty list names a few visiting faculty only as "Spring/Autumn" semesters without years.
