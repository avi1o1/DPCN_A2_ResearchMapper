# IIIT Kalyani golden set: lab notebook

Run 30 Oct 2026, operator Arihant Tripathy. Output `golden/golden_iiit_kalyani.csv` (101 rows). Working files: `C:\Users\Arihant\rm_work\iiit_kalyani_golden\` (data, code/build.py holds every row).

## Sources and yield
| source | pages visited | rows | notes |
|---|---|---|---|
| Annual reports 2014-17 ... 2022-23 (7 PDFs, text cached by the roster run, reused) | 7 | 53 | faculty "Recent publications" lists and student-publication lists; all `medium` (listing alone) |
| Institute own list `iiitkalyani.ac.in/publications` (58 items, per-faculty, no venues, no DOIs; not IRINS) | 1 | 12 | labelled dept_page |
| Faculty sites: Sanjoy Pratihar, Amit Ranjan Azad, Rinky Sha (publication pages) | 3 | 26 | Soumen Pandit page fetched (lists only up to 2022, all before his Jul 2024 joining: 0 rows); Uma Das, Hafizul Islam subpages 404; Imon Mukherjee site is JS-only (empty) |
| Institute news: students-achievement pages (main, PhD, M.Tech, B.Tech), faculty-achievements | 5 | 5 | many items lack a year or full title, skipped (Sayan De ESWA, Soumen Bajpayee ICSP 2024, Subhendu Mandal, Soumen Santra) |
| arXiv abs/PDF (found by web search, never /search) | 7 PDFs/abs | 4 | 2007.07482, 2304.12730, 2603.13791, 2606.01806; affiliation printed on PDF = `high`. arXiv never returned 403. |
| Web search other | 1 | 1 | ACL Anthology 2023.nlp4dh-1.18, `high` |

Search strings: `"Indian Institute of Information Technology Kalyani" arXiv paper` (arxiv.org), `IIIT Kalyani researchers paper published news`, `arxiv "IIIT Kalyani" <faculty names>` (x2, arxiv.org), `"iiitkalyani.ac.in" arxiv.org pdf`. Hits from other Kalyani institutions (Kalyani Govt Engg College, University of Kalyani) were rejected as homonyms.

Dead or empty: `/php/publication.php` and `/php/facultymainpage/bk.html` (404 on the live site), faculty profile pages' "Publications" link is the same institute list.

## Source mix vs brief
Achieved: annual report 52 %, faculty page 26 %, dept/institute page 12 %, arXiv 4 %, news 5 %, websearch 1 %. Deviation: faculty profile pages have no lists and most personal sites are empty or JS-only, so annual reports (which have per-person lists with DOIs and venues) carry more weight; arXiv yield is low because few IIIT Kalyani authors post preprints. The institute publication list was used as the department-level source. IRINS and Wayback were not needed.

## Coverage: department x year (rows)
Unit totals: CSE 52, ECE 36, Physics 9, Mathematics 4.
Years: 2016: 0, 2017: 3, 2018: 9, 2019: 8, 2020: 12, 2021: 15, 2022: 13, 2023: 11, 2024: 9, 2025: 13, 2026: 8.
2016 is empty on purpose: the first faculty joined mid-2016 and no 2016 paper shows the affiliation (joining-year rule). Mathematics is thin (two faculty, one of whom joined 2023). 16 distinct faculty/visitor authors appear; the per-person cap of 8 is respected (counted against the first-named IIIT author; student-first papers count against the student).

## Rejected candidates
* Uma Das 2016 STOTEN and 2015 papers; Imon/Hafizul/Sanjay/Sanjoy/Dalia/Tamal Ghosh papers dated before or in the joining year, listed in 2014-17 and 2017-18 reports (pre-joining or joining-year without affiliation).
* Soumen Pandit (joined 04.07.2024): every listed paper 2017-2023 (incl. POSTECH 2023 IEEE items on the institute list) is outside tenure.
* Sudeshna Mondal (joined 02.01.2023): all 2022 and the 2023 Filomat paper (joining year, no affiliation seen).
* Amit Ranjan Azad (joined 31.05.2022): 2015-2021 papers and the ICSC 2022 conference paper (joining year, no affiliation).
* Pratik Chakraborty 2016-2021 items, Rinky Sha 2016-2021 items (joined 2020/2021).
* Bapi Kar 2018 arXiv preprints (before 2023), Bhaskar Biswas (report says "Nil"), Devdas Ghosh and Madhumita Sengupta (tenure ends 2016), Sandip Karmakar pre-2016 items.
* Dalia Nandi / Imon Mukherjee / Hafizul Islam papers beyond the cap of 8; Debika Chaudhuri et al. ISDCS 2020 (Tamal Ghosh left 2019, Dalia cap full).
* arXiv hits with other Kalyani institutions (2510.22874, 2609.12303).
* Imon's "IPSI BgD" 2015 and old-DOI mismatch: the 2018-19 report prints DOI 10.1007/s11042-016-3319-0 for the video-clips paper (it belongs to the Keyless paper); the video-clips DOI was taken from the 2014-17 report.

## Known biases
* Annual-report lists are "recent publications" selected by faculty, so they favour journal papers and the report years 2017-2023; nothing after 2023 comes from reports (no later report online).
* Only 24 % of rows carry a DOI because the institute list and faculty sites mostly print none and no lookups were allowed; reports print DOIs unevenly.
* Venues are missing (publisher only) for the 12 institute-list rows.
* 96 of 101 rows are `medium` (tenure rule or report listing); only arXiv/PDF rows are `high`.
* Tenure is an annual-report date, so for long-serving staff a paper from the first months after joining is excluded; Santanu Chattopadhyay rows rely on his post as Director.
* Computer Science and ECE dominate; Physics/Mathematics mirror their staffing (1 and 2 faculty).
* Year of "accepted" items (ICCTE 2025 volume published 2026, PIMRC 2026, Quad-port July 2026) follows the source; Imon video-clips paper year 2018 (volume) vs 2017 (online).
