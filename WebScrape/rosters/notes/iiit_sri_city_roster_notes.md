# IIIT Sri City faculty roster, notes (operator Arihant Tripathy, run date 2026-10-29)

Output: `rosters/iiit_sri_city_faculty.csv` (143 rows: 56 current, 22 former, 64 visiting, 1 adjunct). Raw data: `C:\Users\Arihant\rm_work\iiit_sri_city_roster\data`, scripts in `.../work/iiit_sri_city_roster/code` (`cur.py` page parser, `emp.py` ORCID, `build.py` builder, `mat.py`/`old*.py`/`tok.py` snapshot presence checks).

## Campuses, addresses, years
* Indian Institute of Information Technology Sri City, Chittoor (PPP IIIT). Present campus: 630 Gnan Marg, Sri City, Satyavedu Mandal, Chittoor District, Andhra Pradesh 517646 (Contact-Us page). Permanent campus occupied from July 2018 (annual report 2020-21 text: "campus in July 2018").
* Early batches (2013/2015-2018) were taught at a temporary location in Sri City, not at IIIT Hyderabad: the Nov-2017 archived faculty page gives the address "C/o Institute for Financial Management & Research, 5655 Central Express way, Sri City, Satyavedu Mandal, Chittoor District, AP - 517646". Academic mentoring came from IIIT Hyderabad ("mentored by IIIT Hyderabad in the first 5-6 years", annual reports 2021-22 onwards); Prof. Uday B Desai (IIT Hyderabad Director) was Mentor Director 2013-2018 (former-directors page). IIIT Hyderabad faculty taught as visiting faculty (2017 list); they are recorded as `visiting` mentor faculty. No other campus found.
* Look-alikes ignored: Krea University (also in Sri City), IIT Tirupati, IIIT Hyderabad.

## Sources and URL patterns
* Current: `https://iiits.ac.in/people/regular-faculty/` (63 entries; filter groups cse / ece / mds / "full-time visiting"; the group tag gives the unit), `/people/lecturers/` (1), `/people/visiting-faculty/` (dated course tables Monsoon 2019 - Spring 2021). Director page, former-directors page.
* NIRF 2026 DCS reports (Overall and Engineering, linked from the site): `.../uploads/2026/05/Overall-IIITSRICITY-20260509.pdf` (50 faculty rows with joining/leaving dates, "currently working" flag). No older NIRF submissions were found on the site.
* Annual reports 2021-22, 2022-23, 2023-24, 2024-25 (faculty, lecturer and visiting-faculty tables, section 7).
* Wayback (CDX, 52 snapshots fetched): `iiits.ac.in/faculty.html`, `/lecturers.html` (2015-17, content is an image: no names), `/faculty/` (Nov 2017), `/home/faculty/` and `/home/visiting-faculty/` (2018-2020), `/faculty-backup/` (2018-20, a stale mix, not used for tenure), `/people/regular-faculty/` (2020-2026, ~15 snapshots), `/people/lecturers/`, `/people/visiting-faculty/`. The site moved from `iiits.in`/`iiits.ac.in` static pages (2015-17) to WordPress in 2017-18.
* ORCID public API (see below).

## Counts by unit (current rows)
CSE 31 current (+1 adjunct), ECE 16, Mathematics and Data Science (M&DS) 7, blank unit 2 (Director, NIRF-only "Prasanna"). Former: CSE 12, ECE 4, M&DS 1, blank 5 (Nagesh Kolagani, Uma Garimella, two additional-charge Directors, Aneel Y). Visiting 64 (62 with blank unit). The group-tag-to-unit mapping on the site: "M & DS" = Mathematics and Data Science (humanities/English lecturers also sit there).
Extraction check: 63 + 1 entries parsed from the live pages against 54 non-visiting names kept as current; NIRF 2026 matches 44 of the page rows (joining year taken from it) plus 3 NIRF-only people.

## Former faculty and tenure years
* Method: presence matrix over archived faculty lists (2017-11, 2018-04/08/12, 2019-06/12, 2020-04 `/home/faculty/`; 15 snapshots of `/people/regular-faculty/` 2020-05 to 2026-07) plus annual reports 2021-22 to 2024-25 and NIRF 2026. FIRST = first list in which the person appears; LAST = last list. Years before the Nov-2017 page cannot be established (2015-17 pages show faculty only as an image), so people who left before Nov 2017 are an unrecoverable gap and FIRST for the 2017 cohort is 2017 even if they joined earlier (joining_year left blank).
* Annual-report-only evidence (Balaji Raman, B. Krishna Priya, Padmini Singh): LAST set to 2023 (report year 2022-23 ends March 2023, absent from the 2023-24 report and the 2023-07 snapshot); this may overstate by up to a year.
* Chandra Mohan D: the live and archived website pages still list him as current, NIRF 2026 gives leaving date 20-05-2025. Decision: `former (2022-2025)` (dated leaving date outranks a stale page). Odelu Vanga (listed to 2025-07-06, NIRF leaving 16-07-2025) and Abhishek Hazra (NIRF leaving 15-12-2025) are former; the site no longer lists them.
* Odelu Vanga: first on the Nov-2017 list and absent from 2018-19 snapshots, then NIRF joining date 24-02-2020 (rejoining). joining_year 2017 (earlier documented appointment).
* Directors: Kannabiran (Director 10 Jul 2018 - 23 Jul 2023 per former-directors page; the faculty page still prints "Professor (HAG) & Director") is kept `current` because the faculty page lists him (page wins), joining_year 2018. Additional-charge Directors Somayajulu (2023-24), Kartikeyan (2024-25) are `former`; S. R. Mahadeva Prasanna (from 6 Aug 2025) is `current`. Uday B Desai is `visiting` (mentor).
* Stale-page doubt (conflict recorded, not acted on because the website list wins): Amit Praseed, Chiranjit Ray, Namitha A. S., Balasubramanian Kandaswamy, R. Shathanaa, Girish G N, Nikhil Tripathi, Arijit Roy and others on the page are absent from NIRF 2026 (47 working) and several from the 2023-24/2024-25 annual reports; ORCID self-declared end dates (Praseed 2022, Ray 2023, Roy 2023) are not evidence. These people may have left; they remain `current` with no joining year unless NIRF supplies one.
* Odd merges: NIRF "Dr K Siva Prasad" (Associate Professor, joined 2014-11-17) = Sivaprasad Kotamraju (annual reports list "K.Siva Prasad" ECE; page lists Sivaprasad Kotamraju). Page "G. Kannabiran" = "Ganesan Kannabiran" (2020 page). NIRF "Mr Prasanna" (MBA, other, joined 2025-07-01) is kept as a separate NIRF-only row because it may or may not be S. Prasannna Gandhi (visiting 2018-2020).

## Visiting / mentor / adjunct
* Nov-2017 visiting list (9 people; IIIT Hyderabad staff Gangashetty, Govindarajulu, Jawahar, Namboodiri recorded as mentor faculty), 2018-12 to 2020-04 visiting page (10 people), course tables 2019-2021 and annual-report visiting tables 2021-22 to 2024-25 (22 more). Ranges for the latter use first appearance and last annual report; they are lower bounds. Many are industry or guest instructors; they are included because the institute lists them under "Visiting Faculty". "Art of Living Trust" (organisation) and "Industry Experts" were skipped; Dr R. Selvi / Vinay Kumar / Rosemaria Mathew (page lecturers) are `current`.
* `Full-time Visiting Faculty` entries on the regular-faculty page (Shiv Mohan, Rafi, Hemanta Kumar, Sakthi Swarrup, Somalatha, Mansoori, Jahnabi, Febin former) are `visiting`; Prasenjit Mukherjee "Adjunct Faculty CSE" is `adjunct`.
* Page lists the Dean/Head roles in the second line; designation holds only the first line.

## Identifiers
* ORCID: 29 rows, all via the single affiliation search (expanded-search, 223 hits, 3 pages) then `/employments` for 30 name-matched candidates: all 29 accepted showed employment at IIIT Sri City. 0 from institute pages. Paul Braineard has two qualifying iDs (0000-0002-9357-7874, 0000-0002-1210-5200): left blank. No per-person searches; no 429.
* Google Scholar, DBLP, Scopus, IRINS, homepage, email: not collected (not on listing pages; profile URLs given). profile_url present for all page entries.
* joining_year: 52 rows (NIRF joining date for 44 current, Kannabiran 2018 director page, Odelu 2017, 3 former via NIRF/page, NIRF-only 3 and 2 Directors). Blank elsewhere.

## Size check
Latest NIRF (2026) faculty table: 50 rows, 47 currently working (includes 8 "Other" visiting/adhoc). The website lists 63 regular/visiting entries plus 1 lecturer. 44 page rows are NIRF-confirmed; the remaining ~20 page rows are mostly 2026 joiners (Kanakavalli, Chaudhri, Sharma, Kuchipudi, Lachure, Nongmaithem, Bollipo joined after the May 2026 submission) or the suspected stale entries above. The 2024-25 annual report lists 38 regular faculty. Difference explained, not resolved.

## Known gaps
No faculty list recoverable before Nov 2017 (2015-17 pages are images; people who left before then are missing, e.g. founding-era faculty). No NIRF submissions before 2026 found. Departure years for stale-page people unverified. Visiting-faculty tenure years are lower bounds; department blank for visiting staff. Wayback density about 2 per year only from 2020.
