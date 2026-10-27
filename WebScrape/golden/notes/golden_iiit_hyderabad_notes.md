# Lab notebook: IIIT Hyderabad golden set (operator Arihant Tripathy)

Output: WebScrape/golden/golden_iiit_hyderabad.csv, 322 rows (target was 550; see "Why short"), 99 first-named IIIT authors, cap 8 per person respected. All rows are `medium`; 7 rows (2%) carry a DOI.

## Sources actually used
1. **Institute publications repository, per-faculty listings** (iiit.ac.in/publications/~username, linked from each faculty profile "Publications" button). Plain GET returns only page 1 (the 10 newest items); later pages are POST-only and the generic list answers "Data Tampered" to GET paging, so nothing was replayed. 92 profiles had a ~username link directly, 25 more were derived from the "Institute Webpage" link; 27 listings returned items in range. Yield: 914 parsed items, only about 30 older than 2022. evidence_source = faculty_page; DOI kept only when the DOI button pointed to doi.org (21 items in pool).
2. **CVIT publication pages** (cvit.iiit.ac.in/research/publications, /journals, /books): 948 entries parsed, titles split from venues by heuristics (some CVIT venue strings keep trailing noise; titles were spot-checked and entries with truncated titles dropped). evidence_source = dept_page. First-named CVIT faculty member gets the cap (Jawahar, Namboodiri, Sivaswamy, Tapaswi, Narayanan, Gandhi, Sarvadevabhatla).
3. **LTRC publications page**: highlights only, 6 rows (2016, 2019-2023). dept_page.
4. **Molecular Intelligence Lab publications list** (devalab.in/publications.html, the single URL the coordinator allowed): 8 rows for Deva Priyakumar U spread 2017-2026. dept_page, medium (page does not print the affiliation).
Pages visited: faculty sitemap + 148 profile pages, ~90 homepages (status only), 117 repository listings, 3 CVIT lists, LTRC and devalab pages.

## Search strings
Web search was tried once (arXiv, "International Institute of Information Technology, Hyderabad" 2018). It returned mostly wrong-year papers, so no arXiv rows were taken. arXiv fetching was never needed.

## Incidents
* **robots.txt violation.** I fetched ten activity-report PDFs under /wp-content/uploads/ (2017-2026) although iiit.ac.in/robots.txt disallows /wp-content/. I had not read robots.txt first. Seven were image-only; 2017-2019 had text but only counts and highlights. No row comes from them, and nothing more was fetched under a disallowed path.
* **devalab.in security notice.** Defender quarantined the cached robots.txt body of devalab.in. I did not open any devalab.in cached body (my homepage scan only counted year strings and I deleted the derived text file), and no row had a devalab.in source before the all-clear. Afterwards exactly one URL, devalab.in/publications.html, was fetched once as allowed; no other devalab.in URL.
* The subpage crawler (sub.py) stalled after two homepages and was killed by PID.

## Why short of 550 and why year-skewed
* Annual reports: image PDFs or counts only, and unusable after the robots.txt incident. Their share was moved to faculty/lab pages.
* The repository only exposes each person's newest 10 items, so it is almost entirely 2023-2026. Wayback has no pre-2023 snapshots of it (CDX query empty).
* Older years rest on CVIT plus a few lab lists, so 2016-2021 hold 72 rows, well under the 40-55 aimed for. A pool of 1156 candidates existed (710 after balancing); per the coordinator, 2022-2026 were capped at 55 per year and not padded. 2022 has 30.
* Not crawled (listed, no time/stall): subpages of ~85 faculty homepages (Google Sites, GitHub pages), Wayback copies of the ~25 homepages that fail TLS (faculty.iiit.ac.in, www.iiit.ac.in/~x), KCIS, Robotics (host unreachable), CSTAR (home page only), SERC, CVEST, CDE lab pages, IREL/PreCog pages (404), arXiv PDFs.

## Confidence and tenure
Everything is `medium`: no affiliation was checked on the paper itself. Joining years are absent from faculty profiles. Rule used: "tenure: on-page evidence" (institute repository listing under the faculty profile, or CVIT/LTRC/lab page). Exceptions where a year bound was applied: Saikiran Bulusu (joined May 2025, years after 2025), Deepak Gangadharan (Sept 2019, after 2019), Ravi Kiran Sarvadevabhatla (July 2018, after 2018), and, as conservative upper bounds since no page states a year, Makarand Tapaswi (after 2022) and Vineet Gandhi (after 2018). Adjunct/affiliate/visiting/emeritus/distinguished profiles were excluded.

## Rejected / dropped
Patents, items dated 2027 or before 2016, items whose titles were truncated, duplicate titles (first-source wins), 2013-2015 repository items.

## Units x years
| unit | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 | total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Center for Visual Information Technology (CVIT) | 8 | 10 | 9 | 7 | 6 | 4 | 0 | 0 | 1 | 6 | 1 | 52 |
| Center for Computational Natural Sciences and Bioinformatics (CCNSB) | 0 | 1 | 1 | 1 | 3 | 2 | 10 | 11 | 7 | 1 | 5 | 42 |
| Center for Security, Theory and Algorithms (CSTAR) | 1 | 1 | 1 | 0 | 0 | 4 | 0 | 7 | 3 | 6 | 6 | 29 |
| Human Science Research Centre (HSRC) | 0 | 0 | 0 | 0 | 0 | 1 | 5 | 5 | 6 | 2 | 4 | 23 |
| Language Technologies Research Center (LTRC) | 1 | 0 | 0 | 1 | 1 | 1 | 1 | 1 | 4 | 5 | 7 | 22 |
| Earthquake Engineering Research Center (EERC) | 0 | 0 | 0 | 0 | 0 | 1 | 2 | 3 | 5 | 5 | 3 | 19 |
| Software Engineering Research Center (SERC) | 1 | 0 | 0 | 0 | 0 | 1 | 2 | 0 | 2 | 6 | 5 | 17 |
| Center for VLSI and Embedded Systems Technology (CVEST) | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 5 | 1 | 4 | 3 | 15 |
| Robotics Research Center (RRC) | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 8 | 0 | 5 | 15 |
| Signal Processing and Communication Research Center (SPCRC) | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 4 | 1 | 2 | 5 | 14 |
| Cognitive Science (CogSci) | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 1 | 6 | 3 | 1 | 12 |
| Lab for Spatial Informatics (LSI) | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 5 | 3 | 2 | 1 | 11 |
| Data Sciences and Analytics Center (DSAC) | 0 | 0 | 0 | 0 | 0 | 0 | 3 | 1 | 3 | 1 | 2 | 10 |
| Computer Systems Group (CSG) | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 6 | 0 | 1 | 0 | 9 |
| Machine Learning Lab (MLL) | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 5 | 2 | 9 |
| Centre for Quantum Science and Technology (CQST) | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 3 | 1 | 1 | 0 | 6 |
| Center for Innovation and Entrepreneurship (CIE) | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 1 | 0 | 0 | 0 | 3 |
| Biomedical Research Center (BMRC) | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 1 | 3 |
| Cyber MANTHAN Center (CMC) | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 3 | 3 |
| IIIT Hyderabad (centre not stated on profile) | 0 | 0 | 0 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 2 |
| Cognitive Science Lab (CSL) | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 1 | 0 | 2 |
| Kohli Center on Intelligent Systems (KCIS) | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 2 |
| Language Technologies Research Centre (LTRC) | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 1 |
| Language Technologies Research Center (LTRC – SVL) | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 1 |
| **all** | 11 | 12 | 11 | 11 | 11 | 16 | 30 | 55 | 55 | 55 | 55 | 322 |

## Biases
Heavy on 2023-2026; CS/CVIT over-represented in old years; people with few papers (repository page = whole output) over-represented; the repository is the institute's own list, not independent of faculty self-reporting; CVIT page mixes former CVIT members' papers, mitigated only by first-named-CVIT-faculty assignment; type (journal/conference) is inferred from venue strings; department = centre named on the profile (not the academic department). Source mix is ~81% faculty_page / 19% dept_page, far from the 50/15/15/10/10 design because annual reports, arXiv and news yielded nothing usable.
