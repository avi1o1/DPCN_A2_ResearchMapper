# IIIT Lucknow golden set: lab notebook

Built 2026-10-29 for Arihant Tripathy (IIIT team) by a Claude agent. Output `WebScrape/golden/golden_iiit_lucknow.csv` (54 rows; target 150 NOT reached, see "Why 54"). All fetches through `polite_get.py`; work files in `C:/Users/Arihant/rm_work/iiit_lucknow_golden/`.

## Sources used (no Crossref/OpenAlex/S2/EuropePMC/DOAJ/ORCID/DBLP/Scholar/Scopus/IRINS/DataCite/arXiv API; pipeline output for this institute not read)
| source | type | visited | rows kept |
|---|---|---|---|
| 52 faculty profile pages iiitl.ac.in/index.php/personnel/* (cached by the roster agent, institute pages) | faculty_page | 52 (about 24 carry publication lists) | 30 |
| https://iiitl.ac.in/index.php/publication-2020/ ("Publication 2020-2026", institute list, about 55 entries) | dept_page | 1 | 15 |
| Annual Report 2022-23 (text layer; department publication lists IT/CS/Math) | annual_report | 1 | 9 |
| Annual reports 2015-16 .. 2021-22 | annual_report | 7 | 0: scans, no text layer (no OCR tool), gap |
| Wayback copies of personnel pages (Adak, Saini, V. K. Singh, Chaurasia, Dey, Vinod Kumar, Muskaan Singh, Mishra, Kumud Tripathi etc., from roster cache) | faculty_page | 13 | 0 new rows (lists pre-date tenure or carry no years) |
| cdsai page, news-updates, press-and-media | dept/news | 3 | 0 (no publication content; news-updates only admissions/courses) |
| cro.iiitl.ac.in | - | 1 | redirects to a login page (522), skipped; wcarl.iiitl.ac.in: connection error |
| Web search (2 queries): `"Indian Institute of Information Technology Lucknow" arxiv.org abs` (allowed domain arxiv.org); `IIIT Lucknow researchers paper published journal news` | websearch | 2 | 0 rows. arXiv search found no paper with IIIT Lucknow affiliation (hits were IIIT Allahabad, Lucknow-based but other institute, bibliometric studies). The second query only returned the institute's own per-paper posts, which duplicate the publication-2020 page. No arXiv fetch was made, so no 403 issue. |

Search strings above are the only ones used; no news-media coverage was found, so the news share is 0 (institute per-paper posts are the same list as the publication page).

## Rules applied
Tenure start (upper bound) per person; a paper counts only if year is strictly after it (rule b), so every row is `medium`. Start used: Rahul Verma 2021 (page), Shubhra Jain 2023 (page), Soumendu Chakraborty 2018 and Niharika Anand 2018 (profile text per roster), Mary Samuel 2018 (dated role "Faculty-in-Charge Student Activity Dec 2018"), Mainak Adhikari / Deepshikha Agarwal / Dhananjoy Dey / Indira Mishra 2021 (first faculty-list snapshot Sep 2021, upper bound), Vishal Krishna Singh and Brijesh K. Chaurasia 2019 (first snapshot Dec 2019, upper bound). Cap 8 per first-named IIIT author (Soumendu 8 + 4 student-led papers counted to the students; Mainak 8; Deepshikha 8). Where a paper appears on several sources it is listed once. No `high` rows: affiliation text was not visible on any source page, and no paper PDFs were opened.
DOI only where printed on the source (21 of 54, 39%).

## Coverage (rows by department x year)
| department | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 |
|---|---|---|---|---|---|---|---|---|
| Information Technology | 0 | 3 | 4 | 9 | 8 | 3 | 3 | 6 |
| Computer Science | 0 | 2 | 0 | 2 | 1 | 0 | 2 | 2 |
| Mathematics | 1 | 0 | 0 | 4 | 3 | 1 | 0 | 0 |
| Management and Humanities | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
Years 2016, 2017, 2018: 0 rows.

## Why 54, not 150
* The institute was run from the IIIT Allahabad campus until about 2019 and faculty pages list mostly pre-IIITL papers; with the strict tenure rule almost nothing before 2020 qualifies. Annual reports for 2015-16 to 2021-22 are scans.
* Most faculty pages give no joining year; people with a first snapshot of 2021-24 therefore only qualify for years after that.
* The institute publication page lists only 2020-2026 and is dominated by IT department (Mainak Adhikari, Soumendu Chakraborty).
* Management and Humanities: faculty pages list papers from before joining (Chaturvedi, V. Sharma, B. Singh, Pandey, Neelu, R. Soni, R. Srivastava) or by visiting faculty; Vinod Kumar's 2020 papers fail "year strictly after 2020". Zero rows. No arXiv/news material found. Sources are exhausted for allowed discovery methods given the tenure rule; this is the reason for stopping.

## Rejected candidates (examples)
* Outside tenure: Mainak Adhikari 2021 papers (about 12, upper bound Sep 2021); Rahul Verma 2019-2021 papers; Shubhra Jain 2019-2022 papers (joined 2023); Niharika Anand 2017-2018 papers; Mary Samuel 2017 papers; Soumendu Chakraborty pre-2019 papers; Vinod Kumar 2020; Naveen Saini 2019-2021 (joined 2022); Ankita Srivastava (joined 2024) and Rajat Soni / Rashi Srivastava / Nitin Kumar / Ramprasad Sarkar (joined 2026) all pre-tenure; Saurabh Shukla 2023 papers (first snapshot Nov 2023); Anshika Srivastava 2024 paper (Ankita Srivastava, joined 2024).
* Not eligible: Vishal K. Singh 2026 (left 2023); Chandranath Adak (no years); visiting/adjunct faculty lists (Chaturvedi, Chatterjee, Kanojia, Murthy etc.: primary affiliation elsewhere); undated entries (Mehta & Verma QoS-aware edge server placement, Prashant Yadav et al. SARIMA/LSTM).

## Known biases
IT-department heavy (67% of rows); 2022-2023 over-represented (institute list and annual report 2022-23); all rows are `medium`; recall for 2016-2019 is essentially untested; faculty-page lists are self-reported; per-year counts of listed papers are affected by what the institute chose to post. Dates of joining are upper bounds so true in-tenure papers in the joining year are dropped.
Row numbers: faculty_page 30, dept_page 15, annual_report 9, arxiv 0, news 0, websearch 0.
