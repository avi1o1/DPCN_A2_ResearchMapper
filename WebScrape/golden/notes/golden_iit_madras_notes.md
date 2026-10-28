# IIT Madras golden set - lab notebook

Status: PARTIAL (230 of 650 target). Built over two agent sessions; the first was lost to a usage limit and the second finished from saved work.

## Sources and yield
| source | pages/files visited | rows kept | notes |
|---|---|---|---|
| Annual reports | 2017-18 and 2019-20 reports (PDF, publication lists), via institute site and a Wayback copy of 2017-18 | 158 | Reports 2016-17, 2018-19, 2020-21 to 2024-25 downloaded from the institute site were HTML/blocked pages, not PDFs, so unusable. Hence the 2017 and 2019 skew. |
| Faculty pages | home.iitm.ac.in/ ~pallab, ~skdas, ~aarajan, ed.iitm.ac.in/~gsaravana and similar (r2d2, shankarram, saran: some 404 or unparsable) | 47 | entries spread evenly through each list, max 8 per person |
| arXiv | abs pages and PDFs found by web search restricted to arxiv.org (not the API) | 22 | affiliation quoted from the PDF, confidence high |
| News | institute press releases / research highlights (30 pages listed); publisher pages for 5 linked papers fetched, 2 returned 403 (not bypassed), 3 kept | 3 | affiliation seen on publisher page, confidence high |
| Dept/lab pages | not done | 0 | |

No Crossref/OpenAlex/Scholar/Scopus/IRINS/ORCID/DBLP/API was used for discovery. DOIs are only those printed on the source page; DOIs in annual-report lines that were truncated by line wrapping (suffix under 8 chars) were blanked.

## Tenure handling
Annual-report and faculty-page rows are confidence medium: the author name was matched to the accepted roster (WebScrape/rosters/iit_madras_faculty.csv) and the paper year must be strictly after the roster joining year (from NIRF; an upper bound for tenure start). Rows without a unique roster match or a joining year were rejected.

## Rejected candidates
Of 248 candidate rows: 15 no unique roster match, 2 ambiguous or no joining year, 4 paper year not after joining year. Annual-report names are in 'Surname Initials' form, which caused most no-match rejections (e.g. several 2019 entries).

## Coverage (department x year)
| dept | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 | total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Aerospace Engineering |  | 6 |  | 5 |  |  |  |  | 2 |  |  | 13 |
| Applied Mechanics |  | 6 | 1 | 5 |  | 1 | 1 | 1 |  | 1 | 2 | 18 |
| Applied Mechanics and Biomedical Engineering |  |  |  |  |  |  |  | 1 |  |  |  | 1 |
| Biotechnology |  | 5 |  | 5 |  |  | 1 |  |  |  |  | 11 |
| Chemical Engineering |  | 6 |  | 5 |  |  |  |  | 1 |  |  | 12 |
| Chemistry |  | 6 |  | 4 |  |  |  |  |  |  |  | 10 |
| Civil Engineering |  | 5 |  | 5 |  |  |  |  |  |  |  | 10 |
| Computer Science and Engineering | 2 | 5 |  | 5 |  | 1 |  |  |  |  |  | 13 |
| Data Science and AI |  |  |  |  |  |  |  |  |  | 1 |  | 1 |
| Electrical Engineering |  | 5 |  | 5 |  | 1 |  |  | 1 |  |  | 12 |
| Engineering Design | 1 | 8 | 1 | 5 | 1 | 1 | 1 | 1 |  |  |  | 19 |
| Humanities and Social Sciences |  | 4 |  | 5 |  |  |  |  |  |  |  | 9 |
| Management Studies |  | 6 |  | 7 | 1 | 1 | 2 | 1 | 6 | 3 |  | 27 |
| Mathematics |  | 5 |  | 5 |  |  |  | 1 |  |  |  | 11 |
| Mechanical Engineering | 1 | 8 | 1 | 5 |  | 2 | 2 | 1 | 3 | 3 | 1 | 27 |
| Metallurgical and Materials Engineering |  | 4 |  | 6 |  |  |  | 1 |  |  |  | 11 |
| Ocean Engineering |  | 5 |  | 4 |  |  |  |  |  |  |  | 9 |
| Physics |  | 5 |  | 6 |  | 1 |  |  | 1 | 3 |  | 16 |

## Known biases
- Strong skew to 2017 and 2019 (annual reports), thin 2016, 2018, 2020-2026; every year is covered but unevenly.
- Source mix deviates from target: annual reports 69 %, faculty pages 20 %, arXiv 10 %, news 1 %, dept pages 0 %.
- Mostly medium confidence (89 %); affiliation not visible on those entries.
- Only about half of the rows have a DOI; annual-report DOIs can be truncated, so DOI coverage is understated.
- Roster joining year from NIRF can be later than the actual join, so some in-tenure papers were rejected (conservative).
- 160 distinct people; cap of 8 per person respected.

---
## SUPPLEMENT (second extension pass): 230 -> 501 rows (target 650 NOT reached; status PARTIAL)
Rows added: 271 (faculty_page +113, dept_page +158). Existing 230 rows kept unchanged. All added rows are confidence medium (affiliation not printed on the listing; tenure rule b via roster joining year, paper year strictly after). DOI present for 35 % of all rows now (down from 53 %: new sources mostly do not print DOIs).

### Sources and yields (new rows kept / entries parsed)
| source | type | parsed | kept |
|---|---|---|---|
| math.iitm.ac.in/mainpublications.php | dept page | 359 in 2016-26 | 45 |
| wsai.iitm.ac.in/publications/ | dept (school) page | 417 | 45 |
| ee.iitm.ac.in ICS/VLSI group publications (Wayback 2024 copy; live www.ee.iitm.ac.in fails TLS, ee.iitm.ac.in without www answers but this page was taken from Wayback) | lab page | 77 | 33 |
| hss.iitm.ac.in/research-publication/ | dept page | 50 | 21 |
| theory.cse.iitm.ac.in publications (CSE Theory Group) | group page | 21 | 12 |
| doe.iitm.ac.in/publications (Ocean Eng.) | dept page | 9 (2026 only) | 2 |
| Faculty pages (home.iitm.ac.in: anand_k, gphani, pshakya, manu.jaiswal, hariharan, anubhab, murgi; ae.iitm.ac.in/~parama; civil.iitm.ac.in/faculty/{vc,sp,alagappan,saran,pillai,arnepalli,vivek,surender}/publication.php; che.iitm.ac.in/faculty.php Pushpavanam) | faculty pages | ~900 | 113 |
| Institute press releases (18 further pages from the cached list pages) | news | 18 fetched (5 failed), 1 mentions a paper | 0 |
Search strings (WebSearch, restricted to iitm.ac.in subdomains) were generic ("IIT Madras professor publications page journal articles ... 2020 2024", per-department variants for EE, CSE, civil, ocean, aerospace, chemical, physics, biotech/HSS, MME/APM/ED). Fetches only via polite_get; no Crossref/OpenAlex/Scholar/Scopus/IRINS/ORCID/DBLP/arXiv API. publications.iitm.ac.in (IRINS-style portal) surfaced in search and was NOT used.

### Sampling choices (deliberate deviations)
- To lift thin years, 2017 and 2019 entries were excluded from all new rows; selection was spread evenly through the remaining eligible list, max 8 per person across all rows (roster-matched counts including the old rows).
- Dept-page rows were capped per page (math 45, WSAI 45, ICS 33-40, HSS 30, theory 12) so no page dominates; picks thinned by spreading across years.
- Dept/lab-page authors matched to the accepted roster by name; only unique matches with a joining year; roster dept must equal the page's dept or be blank; WSAI required a full first name. WSAI shows only the first 3 authors ("& more"), so IIT Madras authors later in the list were missed. `department` for WSAI rows is the page's unit, "Data Science and AI", not the author's home department.
- Year = year printed on the page (WSAI/ICS pages: listing year; may differ from publication year for some workshop entries).

### Rejected / not used
- chem.iitm.ac.in faculty pages (123 cached pages) are behind a CAPTCHA validation wall: skipped, not bypassed.
- cse.iitm.ac.in/publications.php and publications.cse.iitm.ac.in: 404 / hung; not used. che.iitm.ac.in/publications/: 404. www.ee.iitm.ac.in pages: TLS failure (mahesh, lakshmin, sarathi, kmitra, srsrini12); Mahesh Mishra, Lakshminarasamma, Sarathi pages not parsed (messy or "accepted" lists).
- Pages fetched but not parsed (free-form lists): K. Ramesh (roster lists him under Mathematics, conflicting dept), P. Ramkumar, Pramoda Nayak, Srinivasan (srinivar), vijay2028, Satish Kumar S.R. (no roster entry), anand_k entries with comma-containing titles (dropped by sanity filter).
- Entries dropped: patents, "accepted/submitted/to appear", year outside 2016-2026 or <= roster joining year, numeric-only venue, no unique roster match.
- Press releases: almost none cite a titled paper; the 5 fetches that failed were not retried.

### Known biases / parse risks
- Still skewed: 2017 (89) and 2019 (82) hold 34 % of rows from the old annual-report rows; 2016 has 27 and 2026 has 25. Source mix now: annual reports 32 %, faculty pages 32 %, dept/lab pages 32 %, arXiv 4 %, news 0.6 % (target 15/50/15/10/10).
- Departments still thin (<= 12 rows): Biotechnology 11, Chemistry 10, Ocean Engineering 11, Applied Mechanics (two labels, 26 total), Aerospace/ChemE/ED ~20. Chemistry is blocked by CAPTCHA; Biotechnology pages carry no lists.
- Several faculty-page entries with commas in titles may have a venue field that contains part of the title (e.g. Piyush Shakya, Hariharan K); titles are as printed but the title/venue split can be off. Manual review recommended.
- Roster joining years come from NIRF (upper bounds) so some valid papers were rejected; initial-only author matches on dept pages (e.g. "A. Ghosh", "R D Kumar") may be false roster matches although unique in the roster.
- Both department names "Applied Mechanics" (old rows) and "Applied Mechanics and Biomedical Engineering" (new) exist; should be merged by the consumer.

### Coverage after supplement (department x year, 2016..2026)
Totals by year: 2016:27 2017:89 2018:43 2019:82 2020:41 2021:32 2022:32 2023:38 2024:48 2025:44 2026:25. Department totals: Civil 61, Mathematics 56, Mechanical 50, Data Science and AI 46, Electrical 45, HSS 30, Management 27, CSE 25, Aerospace 24, Physics 22, MME 19, ChemE 19, ED 19, Biotech 11, Ocean 11, Chemistry 10, Applied Mechanics (both labels) 26.
