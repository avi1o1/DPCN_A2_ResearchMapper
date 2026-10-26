# Golden set: IIT Tirupati (iit_tirupati), 2016-2026, lab notebook

Built 2026-10-25/26 by an independent sub-agent. No bibliographic API was used for discovery (no Crossref, OpenAlex, Semantic Scholar, Europe PMC, DOAJ, ORCID, DBLP, Google Scholar, Scopus, IRINS, DataCite, arXiv API). `WebScrape/iit_tirupati.json` and other pipeline outputs were not read. Every URL went through the shared fetcher `scratchpad/tools/polite_get.py` (about 245 fetch calls, logged in `work/iit_tirupati_golden/data/fetch.log`; one stream at a time). Downloads are in `work/iit_tirupati_golden/data/`, scripts in `work/iit_tirupati_golden/code/` (one `*_rows.py` per source, `merge.py` writes the CSV).

**Result:** 313 distinct papers in `golden/golden_iit_tirupati.csv`.

| evidence_source | rows | confidence | rows with DOI |
|---|---|---|---|
| faculty_page (dept-site profile pages, mostly Wayback copies; personal/facweb homepages linked from dept sites) | 134 (43 %) | all medium | 22 |
| dept_page (institute Publications page, Maths/CSE/EE/CEE/HSS dept publication pages, PPL lab site) | 69 (22 %) | all medium | 17 |
| annual_report (9 annual reports 2016-17 .. 2024-25) | 58 (19 %) | all medium | 2 |
| news (institute news page + 15 issues of the Samvid newsletter) | 29 (9 %) | 3 high, 26 medium | 3 |
| arxiv (PDF affiliation checked) | 23 (7 %) | all high | 0 |
| **total** | **313** | 287 medium / 26 high | 44 (14 %) |

Types: journal 219, conference 52, preprint 25, book-chapter 9, book 8. Years 2016-2026 all covered (2016: 2, 2017: 5, 2018: 18, 2019: 25, 2020: 46, 2021: 41, 2022: 44, 2023: 39, 2024: 45, 2025: 30, 2026: 18).

## Departments x years coverage
| Department | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 | total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Chemical Engineering |  |  |  |  | 3 | 3 | 6 | 4 | 1 | 2 |  | 19 |
| Chemistry |  |  | 2 | 2 | 3 | 2 | 5 |  | 3 | 2 |  | 19 |
| Civil and Environmental Engineering |  |  | 8 | 6 | 14 | 5 | 7 | 5 | 1 | 3 | 1 | 50 |
| Computer Science and Engineering |  |  | 2 | 2 | 7 | 8 | 4 | 3 | 2 |  | 1 | 29 |
| Electrical Engineering |  |  | 1 | 4 | 5 | 10 | 9 | 4 | 4 | 2 | 3 | 42 |
| Humanities and Social Sciences |  |  |  | 4 | 1 | 3 | 3 | 7 | 5 | 1 |  | 24 |
| Mathematics and Statistics |  |  |  | 2 | 3 | 1 | 3 | 6 | 9 | 5 | 6 | 35 |
| Mechanical Engineering |  | 2 | 4 | 2 | 7 | 6 | 3 | 4 | 4 | 3 |  | 35 |
| Physics | 2 | 3 | 1 | 3 | 3 | 3 | 4 | 6 | 16 | 12 | 7 | 60 |

All 9 academic departments are covered; about 90 distinct IIT Tirupati people appear as first-listed IITTP author. Former faculty included: R. M. Oinam (left 2021), T. S. Natarajan (left 2022), P. C. Deshmukh (early faculty, 2015-). Non-faculty: arXiv postdocs/students and 3 student-led news items.

## Site situation (why the source mix looks the way it does)
* `www.iittp.ac.in` is a React single-page app. Faculty profiles are rendered from `https://iittp.ac.in/api/faculty/<slug>`, which returned **502 Bad Gateway** on 2026-10-25 and 2026-10-26 (fetcher retried with backoff); Wayback has 0 captures of `/api/faculty/`. `old.iittp.ac.in` serves the same SPA. So the institute's own faculty profile pages were unavailable.
* Department sites `cee`, `chemical`, `cse`, `cy`, `hss`, `mech` `.iittp.ac.in` return "Website Under Maintenance". **Wayback copies** (2024-2025 captures) were used for them (allowed by the brief), found via CDX listings of each host. `ee`, `mast`, `physics` sites are live.
* The site bundle (`/static/js/main.*.js`, fetched once) contains as static data: the faculty lists per department (reused from the roster agent's parsed `site_faculty.json`), the institute **Publications** page list (245 entries, `iittp.ac.in/publications`), the **News** page arrays (2017-2025) and all annual-report and newsletter PDF links.
* robots.txt of iittp.ac.in allows everything. No bot challenge was met anywhere.

## Tenure rule (b) as applied
* J = joining year from the person's own page when stated (Reetesh Gangwar 11/2018, S. Gorthi Aug 2016, R. K. S. S. Gorthi Jul 2017, D. Mondal 2017, A. K. Manna 2017, V. Chintalapudi Dec 2021, C. P. Rao Jul 2019); else the **NIRF** faculty tables (NIRF 2022-2026 PDFs, parsed by the roster agent into `nirf_rows.json`; earliest join date per person); else / and the first **Wayback faculty-list snapshot** (roster agent's cached snapshots 2015-11..2024).
* Deviation: when the Wayback first-seen year is **earlier** than the NIRF date, the Wayback year was used (NIRF dates can be regularisation/re-appointment dates). Cases: P. C. Deshmukh (on 2015-11 list; NIRF 2019), T. S. Natarajan (2015-11), N. Venkaiah, M. M. Avulapati, K. N. Satyanarayana (2016-08), A. Raghuramaraju (2018-06; NIRF 2020). Checked by name in snapshot text (e.g. "sai gorthi" in 2016 matched Subrahmanyam, not R.K.S.S. Gorthi, so the latter kept J=2017).
* Accept only year > J (joining-year papers rejected unless affiliation seen). The rule is written into each row's `notes`.

## 1. Faculty pages (`faculty_page`, 134 rows)
* Physics live pages `physics.iittp.ac.in/Dr*.html` (15 pages, "Selected Publications", 5-8 entries each): 28 rows from 10 faculty, up to 4 spread over in-tenure entries. Rejected wholesale: A. Joglekar (J 2022, list <= 2020), K. Dolui (J 2024), L. G. Kolla (joined Nov 2025 per own page), A. Patsha (no join date; Weizmann-era list), V. Vasudeva Rao (adjunct 2024); M. Singh 2022 entries (= J).
* EE live pages `ee.iittp.ac.in/Faculty_*.html` (21 pages): 18 list only pre-joining papers (hiring-time CV extracts) -> 0 rows; K. P. Naveen (4) and P. S. Saikrishna (4) used. Prateek Kumar Sharma's facweb list: all GlobalFoundries-era (joined 2025) -> rejected.
* Personal homepages linked from dept sites (Google Sites / weebly / github.io / facweb.iittp.ac.in, 33 pages fetched): S. Gorthi (6), R. K. S. S. Gorthi (6), P. Mohapatra (5), P. Vyavahare (5), I. Das (4), Krishna Kishore (3), Shilpak Banerjee (3), Srijanani A. Prasad (4), R. Modak (3), S. Aravinda (3), K. P. Biligiri (2). V. Khaire (J 2024, list <= 2024) and the ViSAL lab page (R.K.S.S. Gorthi, capped) gave 0.
* Wayback copies of dept faculty profiles (cee 14 pages, chemical 6, mech 9, cy 19, hss 8; CSE profile captures are empty JS shells): 50 rows. Many CEE/ME/HSS profiles list only pre-joining work (A. Murali Krishna, A. B. Narayan, B. K. Prapoorna, J. Pancheti, B. Balakrishnan, A. Dutta, D. V. Kiran, S. Sundar, L. Shyamsunder, T. S. Kumar, A. Vir, A. K. Pandey, Bharath Kumar, B. M. Kachhap, S. Bhupatiraju, C. R. Vishnu, S. Haldar, S. Bera, S. Sanapala, S. Chakraborty, P. Mondal, G. Roy, M. K. Sharma, K. Pal) -> 0 rows each.
* Sampling: faculty chosen to cover every unit; within a list, entries spread evenly over in-tenure entries (lists newest first), duplicates skipped, max 5 per person per page and max 8 per person across all sources (Chimalakonda, Biligiri, R.K.S.S. Gorthi, Deshmukh, Modak, Aravinda, I. Das reached 8; further entries skipped).

## 2. Department / lab pages (`dept_page`, 69 rows)
* Institute Publications page (bundle data behind `iittp.ac.in/publications`, 245 free-text entries, 2017-2026): 16 even points, next in-tenure entry -> 16 rows (point 16 = 2017 entries all in joining years except Venkaiah).
* Maths dept `mast.iittp.ac.in/Publications.html` (table of 66 rows): 14 spread rows (1 rejected outside tenure).
* CSE dept Wayback `journal-publications/` and `conference-publications/` (both headed "with IIT Tirupati affiliation, since 2018"): 9 + 8 rows, Chimalakonda skipped (cap).
* EE dept Wayback `publications` (5), CEE dept Wayback `research/publications` (7, every 5th line), HSS Wayback `research/journal-papers`, `book-chapters`, `books` (7), Plasma Physics Lab site `ppliittp.com/publications` (3).

## 3. Annual reports (`annual_report`, 58 rows)
* All 9 English annual reports linked from `iittp.ac.in/annualreports` (2016-17 .. 2024-25), all 200. `pdftotext` raw mode (layout mode garbles the 2-column appendices).
* 5 (2016-20) or 6 (2021-25) evenly spaced points through the publication section; first complete in-tenure non-duplicate entry after each point. 49 rows. Skipped on the way: newspaper op-eds (Telegraph), a magazine piece (pcquest), a conference talk without proceedings (APS March Meeting), joining-year entries (Srivastav 2018, P. Mohapatra 2018, A. K. Jha 2021, Gumma 2020, Balakrishna 2023, Ganguli 2017, Kumarswamyreddy 2021), duplicates.
* Stratified supplement (9 rows) from the Chemistry and HSS sections of the 2021-22..2024-25 appendices, because those units were under-covered after the main pass.

## 4. arXiv (`arxiv`, 23 rows)
* arXiv robots.txt disallows /search; discovery by web search restricted to arxiv.org. Strings: `"Indian Institute of Technology Tirupati" arxiv`; `"IIT Tirupati" arXiv preprint Tirupati 517619`; `"Indian Institute of Technology Tirupati" "Computer Science" arxiv 2019 2020 2021`; `"IIT Tirupati" arxiv electrical engineering wireless OR communication OR signal processing` (0 relevant); `"Indian Institute of Technology Tirupati" mathematics OR statistics arxiv`; `"IIT Tirupati" arxiv mechanical OR civil OR chemical engineering flow OR concrete OR combustion` (1 relevant); `"Tirupati" "Indian Institute of Technology" arxiv 2018 OR 2019 OR 2020 physics OR quantum`; `Deshmukh "IIT Tirupati" photoionization time delay arXiv 2016 OR 2017 OR 2018`; `Chimalakonda "IIT Tirupati" arXiv 2019 OR 2020 software engineering`; `"IIT Tirupati" arXiv reinforcement learning OR deep learning Joseph OR Mopuri OR Yeturu OR Vyavahare OR Mohapatra` (0).
* 33 PDFs fetched (`arxiv.org/pdf/<id>`, fetcher gap 5 s, no ARXIV_BLOCKED). Affiliation checked in PDF text. Accepted 23. Rejected: 1606.03780 (Deshmukh at IIT Madras), 2209.08014, 2210.05219 (no IITTP author), 2410.16696 (IITTP only in acknowledgement), 2512.10063 (thesis, no IITTP), 2401.02366 and 2505.00532 (only "CAMOST, joint initiative of IIT Tirupati & IISER Tirupati": ambiguous, excluded), 2602.16344, 2609.37643 (A. Sharma cap). Not fetched because of the per-person cap: 2508.17344, 2011.03449, 2610.17578, 2306.04892, 2501.05724 (Chimalakonda). Year = v1 year from identifier.
* Two arXiv authors are not on the faculty roster (V. S. Prasannaa, Arpita Goswami: likely postdocs) and two rows are student-led (2603.11645, 2110.11424).

## 5. News (`news`, 29 rows)
* Institute News page data (9 yearly arrays 2017-2025, 144 items) filtered with `publish|journal|paper|article|cover|doi`: 12 items; only 3 name a paper/book title -> 3 rows (high: the institute states the IITTP affiliation of the new work; two are student-led). Rejected: Bera JACS 2025 item (topic description, not a title; DOI printed but no lookup), award/editorship items, op-ed list.
* 15 Samvid newsletters (2018-2025; 16 PDFs fetched) carry "Recent Faculty Publications" lists: 2 points per issue (1/4, 3/4) -> 26 rows, medium (a listing, like the annual reports). Jan 2018 issue gave 0 (all 2017 joining-year papers).
* External press search was not attempted beyond the institute sources (the Palakkad and Kharagpur pilots found it near-zero yield); the brief's fallback (institute news/newsletters) was used.

## Known biases
* **Affiliation:** 92 % of rows are medium (tenure rule only). Dept/faculty lists and reports demonstrably contain pre-joining work; such entries were removed only when they failed the date rule. Papers written just after joining may still report a previous affiliation (e.g. Nabil 2020 with Alberta co-authors, Manna 2018 with Weizmann co-authors, Gandeepan 2020 Göttingen review). These are kept as the rule prescribes, but they are likely "golden-set errors" when matched against affiliation-based harvesting.
* **Source availability:** the main faculty-profile API was down and six dept sites were in maintenance, so faculty pages are Wayback copies frozen in 2024-25 and personal homepages; recent (2025-26) work of faculty without homepages is under-represented, and faculty whose profile lists only hiring-time papers contribute nothing from their own page.
* **Recency / early years:** 2016-2017 have 7 rows only: the institute started in 2015 with mentor faculty from IIT Madras and most regular faculty joined 2017-2018 (joining-year rule removes their 2017 papers).
* **Department mix:** Physics (60) and CEE (50) are large because physics pages and many arXiv hits exist; Chemistry and Chemical Engineering (19 each) and HSS (24) are thinner even after the stratified supplement.
* **DOI coverage** is low (14 %) because most sources print no DOI; DOIs were recorded only as printed.
* **Duplicates of record:** arXiv preprints may later appear under a different title; matching should allow title variants and ±1 year.

## Brief issues
* Faculty profile pages unavailable (API 502, dept sites in maintenance): Wayback copies and dept-linked personal homepages substituted; faculty_page share 43 % instead of ~50 %, dept_page 22 % (>15 %), annual_report 19 %, news 9 %, arXiv 7 % (<10 %).
* Tenure source priority: Wayback first-seen used when earlier than NIRF (NIRF can be a re-appointment date); otherwise own page > NIRF > Wayback as briefed.
* Newsletters labelled `news` but treated as listings (medium + tenure), like annual reports.
* CAMOST ("joint initiative of IIT Tirupati & IISER Tirupati") affiliations excluded as ambiguous.
