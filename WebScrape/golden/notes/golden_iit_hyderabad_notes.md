# Golden set: IIT Hyderabad (iit_hyderabad), 2016-2026, lab notebook

Built 2026-10-27 by sub-agents; the work was interrupted once by a usage limit and continued from the saved state. No bibliographic API was used for discovery (no Crossref, OpenAlex, Semantic Scholar, Europe PMC, DOAJ, ORCID, DBLP, Google Scholar, Scopus, IRINS, DataCite, arXiv API); pipeline outputs were not read. All fetches went through the shared polite fetcher; the full fetch log is in the scratchpad work folder `iit_hyderabad_golden/data/fetch.log`.

Result: 398 rows (target ~650 not reached; see Bias). Sources: annual_report: 58, arxiv: 20, dept_page: 88, faculty_page: 232. All rows `medium` except arXiv rows (`high`, affiliation visible in the PDF).

## Sources and yield
* Faculty/lab homepages (about 330 pages fetched, 45 usable publication lists): entries spaced evenly through each list, cap 8 per person. Only entries with a year strictly after the person's joining year were taken.
* Department pages: CSE publications tables, Mathematics publications page (IITH authors highlighted), Liberal Arts research-publications page. Matching of authors by full name (CSE/Math) or surname plus initial (LA); tenure rule applied.
* Annual reports 2016-17 to 2018-19 (publication lists per faculty): hand-reviewed sample; report listings alone are `medium`.
* arXiv: abs pages and PDFs reached through general web search restricted to arxiv.org (never /search); 55 papers fetched, 20 kept where the PDF first pages show an IIT Hyderabad address and an IITH faculty author. Year = v1.
* News/highlights: iith.ac.in news, highlights and press-release pages were fetched; they list awards and events, almost no papers with titles, so the news share is 0 (no rows). Annual reports 2021-22 to 2024-25 are text-extracted but their publication lists are scrambled two-column text, so they were not used.

## Tenure rule
Joining year: NIRF joining date in the roster, else the first annual report that lists the person (an upper bound), else own page (Sanghi Oct 2025, Dandapat Sep 2025). Paper year must be strictly greater. People with no joining year anywhere were excluded (except where the own page gave one).

## Coverage
Years: 2016: 32, 2017: 48, 2018: 23, 2019: 32, 2020: 21, 2021: 29, 2022: 32, 2023: 33, 2024: 70, 2025: 40, 2026: 38
Departments: Artificial Intelligence: 3, BioTechnology: 1, Biomedical Engineering: 10, Chemical Engineering: 10, Chemistry: 38, Civil Engineering: 36, Computer Science & Engineering: 86, Design: 5, Electrical Engineering: 76, Liberal Arts: 30, Materials Science and Metallurgical Engineering: 7, Mathematics: 33, Mechanical & Aerospace Engineering: 52, Physics: 11

## Rejected / dropped
* ~17 parsed rows dropped for broken title/venue parsing; patents, awards, talks, grants and theses lines filtered out.
* Papers by "IIIT Hyderabad" (International Institute of Information Technology) were rejected; one arXiv candidate (2410.08285) is IIIT and was not used.
* arXiv candidates whose first pages did not show IIT Hyderabad (large collaborations such as DES, DUNE, Belle II, ProtoDUNE) were not used.
* Kundu (Physics) skipped: no joining year found.

## Bias
Physics, Chemical Engineering, MSME, Design, Biotech, BME and AI are under-represented because few faculty there have scrapable publication lists (many use Google Scholar/IRINS links). CSE, EE and MAE are over-represented. 2016-2020 and 2018/2020 are thinner than 2024. DOI coverage is low for list-based sources.
