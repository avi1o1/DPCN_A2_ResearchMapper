# IIIT Agartala (iiit_agartala) faculty roster notes

Operator: Arihant Tripathy (IIIT team). Run date 2026-10-30. Output: `rosters/iiit_agartala_faculty.csv` (39 rows). Working data: `C:/Users/Arihant/rm_work/iiit_agartala_roster/{data,code}` (build script `code/build.py`).

## Result in one table
| status | n | notes |
|---|---|---|
| current (regular) | 4 | Director Abhay Kumar + 3 CSE assistant professors (Sushmita Sharma, Syeda Zeenat Marshoodulla, Prarthana Dutta) |
| former (regular) | 3 | Parijata Majumdar, Arijit Datta, Sanasam Chanu Inunganbi (all CSE, all 2024-2025) |
| visiting (mentor faculty / post-holders from NIT Agartala) | 32 | 11 CSE mentors/coordinators, 19 deans/associate deans/Mentor Director, 2 Career Development Cell (T&P) post-holders |
| adjunct / emeritus | 0 | none listed anywhere |

Departments: Computer Science and Engineering (only academic department; 3 current + 3 former regular, 11 visiting). Other visiting rows carry "Administration" (deans, mentor director, examination faculty) or "Training & Placement" (CCD) as the unit the institute site files them under; they are NIT Agartala faculty and the unit is a post, not a department. Joining years: 2 filled (Abhay Kumar 2023 from ORCID; Arijit Datta 2024 from his own current-employer profile). Identifiers: ORCID 2 (see below), Google Scholar 6, DBLP/Scopus/IRINS 0.

## Institute facts (campus, address, years)
* IIIT Agartala is an IIIT-PPP Act 2017 institute of national importance, mentored by NIT Agartala; classes began 2018 ("Est. 2018" in the site footer). One campus only: temporary campus inside NIT Agartala, "IIIT Agartala, NIT Agartala Campus, Barjala, Jirania, Tripura (W) - 799046" (site footer, archived 2022 pages and annual reports all agree). Permanent campus at Bodhjungnagar is not built (foundation-stone gallery/event pages only). No second campus; the PPP partner has no separate faculty site.
* Single academic department: Computer Science & Engineering, B.Tech intake 70-100. The 2022-2024 archived CSE page says "currently the only branch ... mentored by the CSE department of NIT Agartala where the faculties are in charge of conducting the course". So **until about 2024 the institute had no faculty of its own; teaching was done by NIT Agartala mentor faculty.** Annual report 2023-24 and 2024-25: "The BoG has sanctioned 10 faculty posts for IIIT Agartala". Contract assistant-professor adverts: July 2023, June 2024, June 2025 (rolling), 2026 (10 posts, applications to 10 Sep 2026; not fetched, from web search only).

## Sources and URL patterns used
1. Current site (new CMS, fetched 2026-10-30): `/academics/faculty` (CSE faculty, Associated Faculty, Technical Assistants), `/team-members` (+ `?department=Administration|Associated Faculty|Training & Placement|...`; one page with all cards, email/phone links only, no profile pages), `/deans`, `/senate-members`, `/director`, `/registrar`, `/board-members`, `/sitemap`, `/pages/mandatory-disclosure`, `/pages/faculty-recruitment`, `/departments/cse` (no faculty). No JSON/AJAX endpoint (server-rendered).
2. Wayback CDX for `iiitagartala.ac.in/<page>.html` (old static site, only archived from 2021-07; nothing earlier on this host). Pages used: `computerScienceandEngineering.html` (6 captures 2022-10, 2024-07, 2024-10, 2025-01, 2025-04, 2026-01), `coordinator.html` (2022-10, 2024-09, 2025-12, 2026-01), `t&p.html` (2022-12, 2023-12, 2024-10, 2025-09, 2026-06), `director.html` (2022-10, 2024-08, 2025-01), `academicSection.html`, `studentWelfare.html`, `examinationSection.html` (2022-10 to 2026-06), `registrar.html`, `chairman.html`. That is every capture CDX lists for these pages, so snapshot density is the archive's, not a choice. The 2021-07 home page and 2019 `nita.ac.in/IIITAgartala/` page (only a faculty recruitment advert on deputation/short-term contract basis) list no people.
3. Annual reports 2023-24 and 2024-25 (S3 PDFs linked from the site; only these two exist online): administration list (Mentor Dean AA, Coordinator, HOD, UG Coordinator), sanctioned posts.
4. ORCID public API (affiliation search, then name search and employments check, see below).
5. rgnau.ac.in/en/user/89 (Arijit Datta's present-employer profile, dates his IIIT Agartala stint).
Not fetchable/used: NIRF (nirfindia.org answers 403 to the fetcher, not bypassed; NIT Agartala's code IR-E-U-0493 is a look-alike, and IIIT Agartala's own submission could not be located), scanned CCD/coordinator notification PDFs (no text layer, no OCR on this machine), IRINS/Scopus/OpenAlex (not allowed).

## Per-unit extraction counts against the archive
Page-by-page membership (regular faculty only): 2022-10 none (mentors only); 2024-07 Inunganbi, Datta; 2024-10 Datta, Majumdar, Sharma, Marshoodulla; 2025-01 and 2025-04 same four; 2026-01 Sharma, Marshoodulla; current site (2026-10) Sharma, Marshoodulla, Dutta.

## How tenure was established (all "first/last" are archive evidence, not appointment dates)
* Regular former faculty: Inunganbi appears only in the 2024-07 capture, absent 2024-10: range 2024-2024; joining year blank (upper bound 2024). Majumdar first appears 2024-10 (upper bound 2024), still on 2025-01 and 2025-04, absent 2026-01: range 2024-2025; last year uncertain because there is no capture between 2025-04 and 2026-01. Support for her leaving: her ORCID record shows Assistant Professor at Tripura University from 2025 (self-declared, not used as evidence). Datta: first appears 2024-07 (upper bound); his RGNAU profile gives "Assistant Professor, CSE, IIIT Agartala (Jan 2024 - July 2025)", used for joining_year 2024 and last year 2025 (also on 2025-04 capture).
* Current: Sushmita Sharma and Zeenat Marshoodulla first appear 2024-10 (upper bound 2024); Prarthana Dutta appears only on the current site (upper bound 2026). joining_year blank for all three.
* Abhay Kumar (Director): ORCID employment "Director & Professor, IIIT Agartala, start 2023" and a LinkedIn entry April 2023 (unverified) agree; used 2023 per instruction, flagged as ORCID-based. Archive: Mentor Director H. K. Sharma on the 2022-10 page, Abhay Kumar on 2024-08 and the annual reports. A director advert dates from Feb 2021 (the 2021 home page lists "Appointment of Director").
* Visiting rows: the range is the first and last archived year in which the page that names them was demonstrably maintained (a newer name present). Rows without a range are on the current site now. Examples: Tribid Debbarma and Ajoy Kumar Das only in 2022-10 (replaced in the 2024-07 captures); Swapan Bhaumik 2024-07/2024-12, replaced by Rajib Saha (Annual report 2024-25, 2026-03 capture); Mrinmoy Majumder 2022-2024, replaced by Srimanta Ray by 2026-01; Nirmalya Kar 2023 (annual report 2023-24 names him UG coordinator) to 2026-01, no longer on the 2026-10 site; Suman Deb only in 2024-07.
* All visiting ranges are therefore lower bounds of true tenure (NIT faculty mentoring since 2018); joining_year left blank for them.

## Decisions on ambiguous people
* NIT Agartala mentors who hold only an IIIT Agartala coordinator/dean/HOD post are `visiting` ("Mentor faculty from NIT Agartala ...") per instruction, including the Mentor Director (H. K. Sharma) and deans. Kept in the roster because their publications are filed under NIT Agartala and the downstream use needs to know they are NOT regular IIITA faculty.
* Associated Faculty on the current site (Ranjita Das, Awnish Kumar, Kamanasish Bhattacharjee, Rajesh Basak, Abhishek Hazra, Ashim Saha, Mrinal Kanti Deb Barma): visiting/current. Ashim Saha is listed in two units (Administration as Coordinator, and CSE associated faculty); one row, unit CSE.
* Kaju Nath, Jawahar Paulraj, John Deb Barma: CCD post-holders shown in the institute-wide list; NIT Agartala faculty (Kaju Nath confirmed by web search; the other two from the "nita" email handles and the NIT mentor pattern). Visiting, department "Training & Placement" for the first two, John Deb Barma "Administration" (Dean/CCD chair). Kaju Nath is on the current site only.
* Rabindra Narayan Mahapatra ("Prof. R.N. Mahapatra" on /deans, full name on /senate-members), Arvind Kumar Jain ("Prof. Arvind Jain"), Biswajit Saha (Mentor Dean R&C, senate page; the "Biswajit Saha, Institute Engineer" on the Administration card is judged a different person, an engineer without Dr.; 2022 examination page "Dr. Biswajit Saha, faculty attached" assumed the same as the Dean): names harmonised, affiliation to NIT Agartala assumed from the "Mentor Dean" title and not individually verified.
* Excluded as non-faculty: Mentor Registrar Col. (Dr.) Ashish Badola (administrative, NIT registrar), Krishanu Gupta (AR Academic / Nodal Officer), OSD, administrative officers, institute engineer, technical assistants, physical education/sports officers (Sukanta Goswami, Anupam Pal), student coordinators, BoG chairman, external senate/BoG members (directors/VCs of other institutes).
* NIT Agartala faculty who merely teach IIIT courses are not listed on any IIITA page and are not included (not identifiable).
* Look-alikes avoided: NIT Agartala, Tripura University, IIIT Allahabad. ORCID matches with only NIT Agartala affiliations were rejected.

## Identifiers (by route)
* ORCID total 2: Abhay Kumar 0000-0002-9809-7087 via the one affiliation search (expanded-search `affiliation-org-name:"Indian Institute of Information Technology Agartala"`; 1 hit; employments confirm IIIT Agartala; name matches); Nirmalya Kar 0000-0002-7371-232X taken from the institute CSE page (profile link). Route counts: institute page 1, ORCID affiliation search 1, name-search leftovers 0.
* Other affiliation queries (`IIIT AND Agartala`: 0 hits; `Information AND Technology AND Agartala`: 12, all NIT Agartala except Abhay Kumar). Leftover name searches for the 5 regular faculty without ORCID (Sharma 17 candidates, Marshoodulla 1, Majumdar 1, Datta 6, Inunganbi 1, Dutta 3): employment checks on Marshoodulla 0009-0002-0322-3974, Majumdar 0000-0002-2324-7685 (Tripura University 2025 only), Datta 0000-0002-0459-1368 and 0000-0002-8505-7633, Inunganbi 0000-0002-7879-1039: none shows IIIT Agartala, so none accepted. Sharma's candidates and Dutta's had no plausible institution; not checked further. No 429 from ORCID. ORCID lookup pending: none, except the 5 visiting-only checks not made (mentors are NIT Agartala people).
* Google Scholar (from institute page): Sharma, Marshoodulla, Majumdar, Datta, Mrinal Kanti Deb Barma (6). ResearchGate link for Sharma kept in `homepage`. Datta's contact@arijitdatta.in is an email, not a homepage.
* A first query used the wrong ORCID field name (`family-names`), returning HTTP 500; corrected to `family-name`.

## Problems and how they were handled
* CDX requests with `filter=statuscode:200&collapse=...` on single pages failed with ConnectionError several times from the fetcher; the same CDX without filter/collapse (limit 300) worked and was filtered locally.
* The system `python3 -I` ignores PYTHONUTF8; scripts run with `-X utf8`.
* NIRF 403 (see above). Scanned PDFs have no text.

## Independent size check
* The institute's own number: the annual reports 2023-24 and 2024-25 say 10 faculty posts are sanctioned for IIIT Agartala; the site's faculty page shows 3 regular assistant professors (+ Director) on 2026-10-30 and 4 in 2025-01/04. A web search found a 2026 advertisement for 10 contractual Assistant Professor Grade II posts, consistent with most posts being vacant. NIRF faculty counts were not obtainable (403), so NIRF-confirmed current rows: 0 of 4 (not a mismatch). The 3+1 current regular count is therefore below the sanctioned 10 and is explained by vacancies, the heavy use of NIT mentor faculty, and the turnover of 2025.
* Associated faculty on the site (7 current visiting) are NIT Agartala staff and not counted against sanctioned posts.

## Known gaps
* No captures of the CSE faculty page between 2022-10 and 2024-07 and between 2025-04 and 2026-01: regular faculty who joined and left inside those windows are invisible (the 2023 contract adverts suggest hires after July 2023). Majumdar's and Datta's last-year values and all joining years are bounds.
* No NIRF, no 2016-2021 faculty lists (the site was not archived before 2021-07; the 2018-2021 teaching was by NIT mentors). Mentor faculty of 2018-2021 are therefore not in the roster, so mentor coverage starts 2022.
* Scanned CCD and coordinator notification PDFs (2021-22, 2022-23) were not OCR'd.
* Affiliations of Mentor Deans other than the NIT Agartala convention were not individually verified.
