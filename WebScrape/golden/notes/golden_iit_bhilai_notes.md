# Golden set: IIT Bhilai (iit_bhilai), 2016-2026, lab notebook

Built 2026-10-26/27 by an independent sub-agent. No bibliographic API was used for discovery (no Crossref, OpenAlex, Semantic Scholar, Europe PMC, DOAJ, ORCID, DBLP, Google Scholar, Scopus, IRINS, DataCite, arXiv API). `WebScrape/iit_bhilai.json` and other pipeline output were not read. Every URL went through `scratchpad/tools/polite_get.py` (log: `work/iit_bhilai_golden/data/fetch.log`; scripts in `.../code/`).

**Result: 287 distinct papers** (target 300 not reached; see "Shortfall").

| evidence_source | rows | confidence | with DOI |
|---|---|---|---|
| faculty_page (institute profiles via Wayback + personal pages) | 191 | mostly medium (a few high) | |
| dept_page (dept research pages + 3 lab sites) | 38 | all medium | |
| annual_report / R&D office yearly lists | 26 | all medium | |
| arxiv (PDF affiliation read) | 26 | all high | 0 (none recorded) |
| news (institute news + newsletters) | 6 | all high | |
| **total** | **287** | 250 medium / 37 high | **48 (17 %)** |

Mix actually achieved: faculty 67 %, dept/lab 13 %, annual report 9 %, arXiv 9 %, news 2 % (brief: 50/15/15/10/10). Types: journal 202, conference 53, preprint 26, book-chapter 5, book 1. Years 2018-2026 only (no 2016-2017 rows; see below).

## Sources and access
* **Live institute site is unreachable**: `www.iitbhilai.ac.in`, `iitbhilai.ac.in`, `cse.iitbhilai.ac.in` all return `DEAD:SSLError` through the fetcher. Everything from the institute site therefore comes from **Wayback copies** (3 s gap), recorded in `source_url` and notes. Personal/lab sites (weebly, wix, google sites, github.io, research.iitbhilai.ac.in via Wayback) were fetched live where reachable.
* Wayback CDX listings (`cdx_dom.txt`, 3,809 URLs for the domain) were used to find page ids (`index.php?pid=...`). No bot challenge was met on Wayback; accounts.google.com sign-in redirect for one Google Sites page was not followed.
* Search strings (web search, restricted to arxiv.org where noted): `IIT Bhilai faculty profile publications list`; `site:iitbhilai.ac.in faculty publications`; `IIT Bhilai annual report pdf publications`; `"IIT Bhilai" faculty homepage publications department of computer science and engineering`; `"Indian Institute of Technology Bhilai" arxiv`; `"IIT Bhilai" Raipur arxiv preprint physics`; `"IIT Bhilai" Durg Chhattisgarh 491001 arxiv`; `... "Computer Science and Engineering" arxiv 2018 2019`; `... "Electrical Engineering" arxiv`; `... mathematics arxiv 2017 2018`; `"IIT Bhilai" chemistry OR "mechanical engineering" arxiv preprint`; `"IIT Bhilai" arxiv 2017 Sabyasachi Ghosh OR Sudhanwa Patra OR Souradyuti Paul`; `... 2019 arxiv neural OR networks OR cryptanalysis`; `... 2018/2019/2020 Department of Mathematics OR Physics`; `... heat transfer OR fluid OR droplet arxiv`; `... graph algorithms OR distributed ... Gorain OR Reddy OR Dhar`; `Sudhanwa Patra 2017 arXiv "IIT Bhilai" left-right model`; `"Indian Institute of Technology Bhilai" 2017 arXiv`; news: `IIT Bhilai researchers study published journal`; `"IIT Bhilai" research paper published news professor team develops`.

## 1. Faculty pages (source "faculty_page"; 191 rows)
* Roster: the 2026 Wayback copies of the 10 department `dept_*_people` pages give 147 listed names (about 85 faculty; the MSME page also lists students). Profile pages `index.php?pid=<id>` were fetched for 106+ candidate ids (62 returned 200; the rest 404/503 in the archive: e.g. Henu Verma, Neetika, A. Tripathi, A. Upadhyay (BSBME), Shobhit Singh, Arvind Singh, Milan Jena, Amit Mishra, Yagnesh Shadangi, Nithin, Swati Yadav, Lalit Sahu, Torsha Moitra, Mehboob (alt id), Avijit Saha, Bhaskar Ghawri). Also fetched: archived profiles of former faculty Radeef Chundakkadan, Anuj Jakhar, Sonal Jha.
* 39 faculty/persons yielded rows. Profiles without a usable publication list (only a Google Scholar link, or none): Santosh Biswas, Anil Sao, Nitin Khanna, Anshul Faye (Scholar only), Mahavir Sharma, Purnendu Das, Ganesh KG, Anindita Ghosh, Rekha/Sruthi (one in-tenure item each), Praveen Kumar and Anjali Chaudhary (only pre-joining papers), Ritika Verma (joined April 2026, all earlier); Dhriti Ghosh appears only via report/dept pages.
* Sampling: per person up to 5-6 in-tenure entries spread evenly through the list order (lists are newest-first), cap 8 across all sources. Dates strictly after joining year J.
* Tenure J: from the person's own profile where stated; otherwise first archived faculty/department list snapshot showing the person (upper bound): Gagan Raj Gupta (CSE page 2021-05-14, J=2021), Sreejith T.V. (list 2019-08-23, J=2019), Kaushik Bandyopadhyay, Pravesh Shukla (ME page 2019-07-20, J=2019); Raghavender Medishetty (news image archived 2020-03, J=2020).
* Same-year rule: papers in the joining year were excluded (e.g. Krishna Murari joined Dec 2024: only 2025 papers; Shailendra Kumar joined May 2024: only 2025-26; Nanaji 2023: 2024+). All rows are medium except 2 Springer rows (below).
* Personal homepages (linked from the institute profile) used for Mayilmurugan, Medishetty, Suchetan Pal, Satyajit Gupta, Mehta, Patil, Souradyuti Paul (rows counted as faculty_page or dept_page per the page type; lab sites as dept_page).
* Two Souradyuti Paul rows (Inscrypt 2017 ring signature; CANS 2017 Bitcoin deanonymization) are **high**: the Springer chapter pages list "Indian Institute of Technology Bhilai" as affiliation (Springer year 2018). DOIs printed on the personal page.
* Rejected (examples): Nanaji 2018-23 papers (pre-joining); Raghavender Medishetty 2017-2022 (J unknown, upper bound 2020; papers with only pre-IIT Bhilai co-authors); Gagan Gupta pre-2021 papers (Purdue/Ohio State era); Vishwesh Jatala 2016-2019 (IIT Kanpur/Austin); Subidh Ali 2013-2016 (NYU Abu Dhabi); Avijit Pal 2017-18; Anuj Jakhar 2016-2020; Dhiman Saha's pre-2018 items; Pawan Mishra 2015-2019 (before Dec 2019); Sonal Jha 2017-2019; Ashutosh Kumar before 2024.

## 2. Annual reports / R&D yearly lists (source "annual_report"; 26 rows)
* Institute R&D page `index.php?pid=rd_journals` (Wayback 2026-04-19): yearly publication lists 2018-19..2022-23 (328 entries incl. headings). Sampled evenly (step 12) and filtered for tenure: 22 rows; 3 further rows were dropped on duplicates/tenure.
* Annual Report 2017-18 PDF (Wayback, text via pdftotext): "Research Outputs > Journals" (4 entries) gave 1 row (Patra, PRD 97); other entries pre-date or are duplicates.
* Other annual-report PDFs (2016-17, 2018-19, 2021-22, 2022-23, 2023-24) were truncated by the fetcher's 5 MB body limit (xref damaged) and could not be text-extracted; 2019-20 and 2020-21 PDFs and the 2017-18 "pub2324" institute-library page returned image-only text or 404. Library page `institute_publications` (2023-24 list) was read but not sampled (it duplicates faculty lists).
* Rule applied: a report listing alone is medium and must satisfy tenure. Entries with only pre-joining authors or pre-joining years were rejected (the lists include e.g. Udayraj's 2016-2019 IIT Bhilai-external papers).

## 3. Department / lab pages (source "dept_page"; 38 rows)
Physics publications page (2018-21), ME, Chemistry, Mathematics and MSME research pages (Wayback 2026), MIST lab (Subidh Ali), plus the personal lab sites above. BSBME, ECE, Liberal Arts, EE research pages list no papers. CSE department site (`cse.iitbhilai.ac.in`) is SSL-dead; its only archived page (phd/) lists no papers.

## 4. arXiv (source "arxiv"; 26 rows, all high)
* arXiv robots.txt disallows /search: discovery only through web search restricted to arxiv.org. 52 PDFs fetched (5 s fetcher gap plus 10 s sleeps), no 403, no `ARXIV_BLOCKED`.
* Affiliation read from PDF text (first two pages, or whole text for end-of-paper address blocks: 2106.10863, 2411.17169, 2607.00719).
* Rejected: 2411.05478, 2512.00915, 2608.08030 (no Bhilai), 1710.03178 (Gorain was at IIIT Vadodara then; the Bhilai e-mail appears only in the 2019 v2 text, kept via the faculty row instead), 1701.02107, 1701.08675, 1705.04125, 1711.00627, 1805.01848, 2206.07414 (no Bhilai affiliation or other institute), 2609.32786 (author's work done at IIT Bhilai but PDF has no affiliation line; acknowledgement only). arXiv listings of papers not found by search are a known gap (recall of arXiv share depends on search engine).
* Duplicates of faculty rows (fybrrLink, Higher matching complexes): faculty rows kept and upgraded to high.

## 5. News (source "news"; 6 rows, all high)
Institute news pages (Wayback): dp_paper_published, smart_insulin, quantumExpression, best_paper_award; newsletters July 2021 and July 2025 (30 newsletter PDFs fetched; 8 were truncated at 1 MB and unreadable; most newsletters mention no paper). Other items (anti-cancer drug JACS Au, MOF Dalton, perovskite ACS AEM, Chem Asian J CO2) print a link/DOI but not the paper title; the JACS Au one was used only to upgrade Sanjib Banerjee's matching faculty-list row to high (DOI printed). No external press coverage found by web search (no `websearch` rows).

## Departments x years
| Department | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 | total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Biosciences and Biomedical Engineering |  |  |  |  |  |  | 3 | 2 |  |  |  | 5 |
| Chemistry |  |  | 1 | 2 | 3 | 9 | 5 | 8 | 7 | 8 | 6 | 49 |
| Computer Science and Engineering |  |  | 5 | 6 | 7 | 9 | 5 | 8 | 13 | 9 | 5 | 67 |
| Electrical Engineering |  |  |  | 2 | 4 | 3 | 1 | 2 |  | 8 | 2 | 22 |
| Electronics and Communication Engineering |  |  |  | 1 |  |  | 2 |  | 2 |  |  | 5 |
| Liberal Arts |  |  |  |  | 4 | 4 |  |  | 4 | 1 |  | 13 |
| Materials Science and Metallurgical Engineering |  |  |  |  |  |  |  |  | 1 | 3 | 2 | 6 |
| Mathematics |  |  |  | 2 |  | 8 | 8 | 6 | 6 | 8 | 6 | 44 |
| Mechanical Engineering |  |  |  | 6 | 7 | 4 | 8 | 8 | 9 | 4 | 3 | 49 |
| Physics |  |  | 1 | 3 | 6 | 4 | 3 | 4 | 3 | 1 | 2 | 27 |

Unit names: the institute lists ECE (from 2024; EE earlier), MSME (Materials Science and Metallurgical Engineering), BSBME (Biosciences and Biomedical Engineering) and Liberal Arts; the CSE/EE units were "EECS" before the split (rows use the faculty member's current unit). No row for 2016-2017: the institute started in 2016 with a handful of faculty and every person's tenure-strict rule (year > J, J >= 2017) excludes them; the 2016-17 annual report could not be read.

## Shortfall and known biases
* 287 of 300: the live site is down, 40+ profile pages are unarchived, several PDFs are unreadable, so the per-person lists available are limited. No department/year cell was filled artificially.
* **Recency / no 2016-17 rows** (tenure rule and short history); 2018 has 5 rows.
* **Wayback snapshots** are dated 2019-2026 and show current faculty; former faculty are visible only through 3 archived profiles (Chundakkadan, Jakhar, Jha), one annual report, one arXiv paper and the Faye profile (Scholar link only), so survivorship bias is strong. Visiting/adjunct faculty are excluded except Nikhil Chander (now ECE).
* Student/postdoc-led papers appear through arXiv (6 student-first rows) and co-author lists, not as separate authors.
* Faculty-list and R&D-list entries are hand-maintained and tilt to journal papers; DOIs are present for only 17 % because the sources rarely print them (none looked up).
* Medium-confidence share is 87 %: affiliation rarely visible on listings; tenure J for 5 people is an upper bound (first archived snapshot).
