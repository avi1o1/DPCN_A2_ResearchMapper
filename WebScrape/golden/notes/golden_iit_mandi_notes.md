# Golden set: IIT Mandi (iit_mandi), 2016-2026, lab notebook

Built 2026-10-26/27 by independent sub-agents (the work was interrupted once by a model change and continued by a second agent from the saved state). No bibliographic API was used for discovery (no Crossref, OpenAlex, Semantic Scholar, Europe PMC, DOAJ, ORCID, DBLP, Google Scholar, Scopus, IRINS, DataCite or the arXiv API); `WebScrape/iit_mandi.json` and other pipeline outputs were not read. Every URL went through the shared fetcher `scratchpad/tools/polite_get.py` (about 430 logged fetches in `/tmp/claude-1000/-home-avilol-Downloads-GitHub-ANLP-A2-ResearchMapper/995e1c99-7243-44f2-a3b6-c40300a778f4/scratchpad/work/iit_mandi_golden/data/fetch.log`; the file also contains lines from before the interruption). Data are in `/tmp/claude-1000/-home-avilol-Downloads-GitHub-ANLP-A2-ResearchMapper/995e1c99-7243-44f2-a3b6-c40300a778f4/scratchpad/work/iit_mandi_golden/data/`, scripts in `/tmp/claude-1000/-home-avilol-Downloads-GitHub-ANLP-A2-ResearchMapper/995e1c99-7243-44f2-a3b6-c40300a778f4/scratchpad/work/iit_mandi_golden/code/` (`build.py` merges `rows/*.tsv` into the CSV and applies the tenure rule and the per-person cap), transcribed rows in `/tmp/claude-1000/-home-avilol-Downloads-GitHub-ANLP-A2-ResearchMapper/995e1c99-7243-44f2-a3b6-c40300a778f4/scratchpad/work/iit_mandi_golden/rows/`.

**Result: 300 distinct papers in `golden/golden_iit_mandi.csv` (target 400; shortfall explained below).**

| evidence_source | rows | confidence | with DOI |
|---|---|---|---|
| faculty_page (faculty.iitmandi.ac.in profiles, 22 via Wayback) | 119 | medium | 12 |
| annual_report (institute Annual Reports 2017-18 to 2024-25 publication lists) | 90 | medium | 26 |
| dept_page (SCENE journal/conference/book-chapter lists, AMRC and IKSMHA centre publication pages, SBBE research page) | 51 | medium | 17 |
| arxiv (PDF first page / abs page, Mandi affiliation seen) | 38 | high | 9 |
| news (institute press releases) | 2 | high | 0 |
| **total** | **300** | 260 medium / 40 high | 64 (21 %) |

Types: see CSV. About 140 distinct IIT Mandi people (faculty plus some students/postdocs on arXiv). At most 8 rows per person (enforced in `build.py`; surplus rows were dropped, see below).

## Departments x years
| Unit | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 | total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Centre of Artificial Intelligence and Robotics (CAIR) | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 1 | 0 | 0 | 0 | 2 |
| School of Biosciences & Bio Engineering | 0 | 2 | 2 | 6 | 0 | 1 | 1 | 1 | 1 | 1 | 0 | 15 |
| School of Chemical Sciences | 2 | 2 | 0 | 3 | 2 | 1 | 2 | 5 | 7 | 1 | 0 | 25 |
| School of Civil & Environmental Engineering | 0 | 0 | 4 | 2 | 1 | 4 | 10 | 12 | 8 | 9 | 0 | 50 |
| School of Computing & Electrical Engineering | 1 | 3 | 3 | 6 | 5 | 4 | 6 | 6 | 10 | 16 | 14 | 74 |
| School of Humanities & Social Sciences | 0 | 0 | 1 | 2 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 4 |
| School of Mathematical & Statistical Sciences | 3 | 1 | 1 | 2 | 2 | 2 | 3 | 0 | 1 | 3 | 1 | 19 |
| School of Mechanical & Materials Engineering | 2 | 0 | 3 | 2 | 5 | 5 | 9 | 8 | 2 | 3 | 4 | 43 |
| School of Physical Sciences | 4 | 1 | 8 | 9 | 5 | 5 | 5 | 15 | 7 | 3 | 6 | 68 |
| **all** | 12 | 9 | 22 | 32 | 20 | 22 | 37 | 49 | 36 | 36 | 25 | 300 |

"School of Computing & Electrical Engineering" etc. are the units named on the institute faculty list (roster cached by the roster agent). Not covered at all: School of Management, Center for Quantum Science and Technologies, IKSMHA Center (only through faculty of other schools), no row has IKSMHA as department. Humanities (4 rows) and CAIR (a few arXiv rows) are thin. Years 2016-2017 are thin because the tenure rule (year strictly after the joining year, upper bounded by the first annual report that names the person) removes pre-joining papers of the many people who joined 2016-2018, and because the 2016-17 and 2017-18 reports are image-only.

## Sources, strings and yields
* **Faculty pages.** `iitmandi.ac.in/allfaculty` roster (230 people, `data/roster.tsv`); each `faculty.iitmandi.ac.in/~uid/` page fetched. About 47 live pages returned 403/timeouts (bot or server challenge, never bypassed); for those the Wayback copy was used and recorded (`FACWB`, source_url is the web.archive.org URL). Papers were taken evenly spaced through each list (not first N), at most 8 per person across all sources.
* **Annual reports.** The reports are on `cloud.iitmandi.ac.in` (links from `iitmandi.ac.in/annualreports`, `data/ar_links.tsv`); 2016-17 to 2024-25 PDFs fetched, text via `pdftotext`; the 2017-18 and 2019-20 lists are images and were read page by page. A report listing alone is only `medium` and the tenure rule was applied.
* **Department / lab / centre pages (this session).** Found by site-restricted web search ("IIT Mandi lab publications page", "School of Mathematical and Statistical Sciences IIT Mandi publications", "School of Biosciences and Bioengineering IIT Mandi publications", ...). Fetched: `amrc.iitmandi.ac.in/publications.php` (13 rows taken), `iksmha.iitmandi.ac.in/publications.php` (9 rows), `scene.iitmandi.ac.in/pages/{journal,conference,book_chapter}` (442 journal, 255 conference, 49 book-chapter entries with printed DOIs; 31 rows taken, evenly spaced, for 7 faculty with unambiguous surname+initials and a known tenure bound), `sbb.iitmandi.ac.in/research.php` (representative publications; 1 row taken, most entries pre-date the faculty member's joining). Dead or unusable: `scs.iitmandi.ac.in/publications` and `research.iitmandi.ac.in/scs/publications` (404/empty), `scee.iitmandi.ac.in/journals.php` (stale 2020-21 list with non-Mandi authors), `scee.iitmandi.ac.in/publications.php` (404), `iksmha` second URL (404), `odr.iitmandi.ac.in` repository (not tried, see biases).
* **News.** Institute press releases (`iitmandi.ac.in/pdf/pressreleases/*.pdf`) and the June 2022 newsletter fetched; they name the journal and the Mandi author with affiliation but rarely the title, so a paper was kept only when its title could be recovered from a general web search hit: 2 rows (dengue mosquito eggs, PLOS Biology 2023; landslide data imbalance, Landslides 2023). Not kept (title not found): WS2-PDMS Advanced Functional Materials 2025 (Balakrishnan), Virology spike endodomain 2022 (Giri), ASCE railway embankment paper. Homepage news-PDF set (`iitmandi.ac.in/pdf/news/*.pdf`) and `/news`, `/iitinnews` were queued but not mined (awards, not papers). The news share is therefore ~1 % instead of 10 %.
* **arXiv.** 45 arXiv ids (listed in `code/arxiv_ids.txt`, found by general web search restricted to arxiv.org and from arXiv links on institute pages) each fetched as abs page and PDF (15 s spacing; never blocked). Affiliation line grepped in the first pages (`code/arx_check.py`). 38 kept; 6 rejected because no IIT Mandi affiliation is printed (1807.00735, 1901.05123, 2007.13737, 1908.00195, 2403.15977, 2512.02512). Search strings used included: "IIT Mandi arxiv" + topic words (hot QCD, thermoelectric, Dirac semimetal, image despeckling, massive MIMO, ...); the exact queries of the first session were not logged.

## Rejected / dropped (details in `data/rejected_build.json`)
* Outside tenure or tenure unknown: 14 candidates, e.g. 2017 papers of Shukla, Balakrishnan, Dhir, Bhavsar, S. K. Pal, Satinder Sharma (joined or first named in the FY 2017-18 report), 2021 papers of Nilamber Chhetri, 2016-2018 papers of Manu Devadevan and Rajeev Kumar.
* Per-person cap (8) exceeded: 7 rows (K. V. Uday, Rahul Vaish x2, Ajay Soni, Arnav Bhavsar x2, Varun Dutt) dropped by `build.py`; later-listed rows were dropped first. Co-authored rows count toward each named Mandi author.
* Duplicates of earlier rows (same title via another source): 4.
* arXiv without visible Mandi affiliation: 6 (above).

## Tenure rule
Joining year from the person's own page where given; otherwise the first annual report (FY 2017-18, 2018-19, 2021-22, ...) naming the person, which is an upper bound (so the rule is conservative: it can only exclude too much). Directors page: L. Behera director since January 2022, so only 2023+ papers were taken from his page and the IKSMHA list. Papers from centre/department lists are `medium` and marked "page is not affiliation evidence by itself".

## Known biases and caveats
* Pre-existing rows from the first session (about 215 rows from faculty pages and annual reports) were not re-verified line by line; spot checks only. Faculty-page papers lack independent affiliation proof (medium).
* Faculty-page and annual-report picks come from people with an accessible page; 47 live pages were unreachable (Wayback copy, possibly stale). Humanities, Management and centres are under-represented.
* SCENE list matching used surname plus initials; ambiguous names (Kumar A., Sharma R., Gupta V., Sen S., Sarkar S.) were skipped, so Civil sampling favours faculty with distinctive names.
* arXiv rows cover mostly physics and mathematics (arXiv culture), and the IDs came from web search, which favours papers with 'IIT Mandi' in indexed text; DOI shown only when printed on the arXiv abs page (9 rows).
* Some IIT Mandi co-authors on arXiv rows are named only partially (the author whose Mandi affiliation is certain); for 1809.03530 the Mandi affiliation belongs to A. Taraphder (primary IIT Kharagpur, dual affiliation); for 1808.04178 only Bhavya Bhatt. Department for a few arXiv rows is inferred from topic (noted in the row).
* Target of 400 not reached: sources of acceptable evidence thinned out (SCS/SCEE pages dead, news pages without titles, odr.iitmandi.ac.in repository and other school sites not mined) and time was lost to the interruption and shared-fetcher queues (arXiv 15 s limit shared with other agents).
* Time-of-build: 2026 papers are partial (year not over).
