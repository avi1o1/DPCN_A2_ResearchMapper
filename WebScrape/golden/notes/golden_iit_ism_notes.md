# IIT (ISM) Dhanbad golden set: lab notebook

Output: `WebScrape/golden/golden_iit_ism.csv` (541 rows, 179 distinct IIT (ISM) authors, max 7 per person; 194 rows = 36% carry a DOI printed on the source).
Work was resumed after an interrupted run; the saved fetches (faculty profiles, department publication pages, newsletters, arXiv abs/PDF) were reused. No roster exists for ISM.

## Sources used (all fetched via polite_get.py; no forbidden databases)
| Source | Page type / URL pattern | Found | Used | Rows | Confidence |
|---|---|---|---|---|---|
| faculty_page | `iitism.ac.in/faculty-details?faculty=<uid>` (445 profiles fetched; 199 give a joining year on the own page) | publication lists of 199 people | picked evenly through each list, 1-5 per person | 389 | medium |
| dept_page | `departments-publications-list?event=<b64 id>` (17 depts) and `<dept>-research-achievements` (17 pages) | 406 tenure-matched candidates | 66 (per-dept quotas; only Physics, HSS, Applied Geophysics, Electronics, Petroleum, FMME pages yielded matches) | 66 | medium |
| news | department newsletter PDFs `storage/newsletter-documents/newsletter<ts>.pdf` (5 per department sampled, 74 PDFs; one image-only PDF skipped, no OCR available) | 42 candidates | 33 | 33 | medium |
| arxiv | arXiv abs pages + PDFs reached via web search (58 fetched) | 58 | 53 (5 dropped, see below) | 53 | high |
| annual_report | Annual Report 2024-25 PDF (239 pp.) | 0 | 0 | 0 | n/a |

Web-search strings used for arXiv: `"IIT (ISM) Dhanbad" site:arxiv.org`, `"Indian School of Mines" Dhanbad site:arxiv.org`, and department-specific variants (physics, mathematics and computing, geophysics, CSE); plus arXiv links on faculty pages. arXiv obeyed the 15 s limit via the fetcher; abs-page metadata (title, authors, first-version date, journal ref) and the PDF first pages were used. arXiv DOIs (10.48550) were not recorded; a DOI is recorded only when the abs page prints a journal DOI.

## Tenure rule applied
Joining year = the person's own faculty page (CV text on the profile: appointment dates; some manual overrides in `code/people.py`). People without a stated joining year on their own page were skipped (246 of 445), since NIRF / archived faculty lists were not fetched; so the faculty and dept sets cover only people with a datable page. A paper counts only when year > joining year, so the joining year is excluded (strict rule). Where the joining date is the first ISM-era appointment (e.g. Indian School of Mines before the 2016 IIT conversion) that is the tenure start used. Several rows are by people who have since left or moved (e.g. a few 2026 arrivals are excluded because paper year must be after joining).

## Deviations from the brief (Brief issues)
* **Annual reports:** the only annual report on the site (2024-25) contains no per-paper publication list (only Scopus/WoS counts and sponsored-project tables, as image pages); other years are not published. Share 0 % instead of 15 %.
* Source mix achieved: faculty 72 %, dept pages 12 %, arXiv 10 %, news (institute newsletters) 6 %. News is department newsletters only (no external coverage sought).
* Target 550 reached ~ (541). Departments with no matchable publications page (Chemical Engineering, CSE, Environmental, Mining, Civil, ...) are covered via faculty pages and newsletters instead.
* Year distribution is skewed to 2024-2026 because many faculty joined recently and the strict tenure rule excludes earlier years; 2016 is thin (28).
* arXiv papers: 3 rows have department `unspecified` (PDF shows only the institute); ISM author for arXiv rows is taken from roster-name matching or the PDF affiliation numbering, and for 3 papers is the first author (flagged only here: 1803.09461, 2503.07570 resolved to the named ISM author; others via roster match).
* Titles and venues of faculty/dept rows were parsed heuristically from free-text lists; some venue strings are abbreviations or truncated (e.g. "Org", resolved by dropping short venues) and a few titles may keep minor trailing/leading noise.

## Rejected candidates / drops
* arXiv: 1509.04221 (2015, out of range); 1711.02324 (conference header only, ISM affiliation of authors not clear); 2208.14091, 2501.00899 (PDF shows no ISM affiliation; ISM = interstellar medium), 2601.06430 (no affiliation text in PDF).
* Entries before the person's joining year, patents, theses, abstracts, talks and entries without parseable year were removed by the filters in `select_fac.py` / `dept_extract.py`.
* Dept-page candidates whose names matched no dated profile (`notenure`) were dropped.

## Coverage (department x year)
| Department | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 | Total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Applied Geology | 1 | 3 | 4 | 2 | 4 | 3 | 3 | 3 | 5 | 9 | 13 | 50 |
| Applied Geophysics | 0 | 0 | 1 | 5 | 4 | 1 | 2 | 4 | 4 | 2 | 1 | 24 |
| Chemical Engineering | 0 | 0 | 1 | 0 | 0 | 0 | 2 | 5 | 0 | 1 | 7 | 16 |
| Chemistry and Chemical Biology | 0 | 1 | 1 | 0 | 1 | 1 | 1 | 1 | 0 | 3 | 0 | 9 |
| Civil Engineering | 0 | 1 | 5 | 2 | 2 | 4 | 5 | 3 | 7 | 8 | 2 | 39 |
| Computer Science and Engineering | 0 | 0 | 1 | 1 | 2 | 2 | 2 | 2 | 0 | 1 | 3 | 14 |
| Electrical Engineering | 0 | 5 | 6 | 3 | 4 | 5 | 2 | 5 | 6 | 3 | 1 | 40 |
| Electronics Engineering | 3 | 2 | 6 | 6 | 6 | 2 | 6 | 4 | 7 | 16 | 2 | 60 |
| Environmental Science and Engineering | 3 | 3 | 1 | 2 | 4 | 2 | 5 | 1 | 3 | 0 | 0 | 24 |
| Fuel, Minerals and Metallurgical Engineering | 2 | 0 | 0 | 1 | 1 | 1 | 1 | 2 | 1 | 2 | 1 | 12 |
| Humanities and Social Sciences | 3 | 5 | 1 | 1 | 2 | 5 | 1 | 1 | 2 | 2 | 5 | 28 |
| Management Studies and Industrial Engineering | 0 | 1 | 1 | 1 | 2 | 1 | 3 | 3 | 1 | 0 | 1 | 14 |
| Mathematics & Computing | 2 | 2 | 2 | 2 | 2 | 4 | 3 | 1 | 7 | 16 | 13 | 54 |
| Mechanical Engineering | 1 | 3 | 4 | 6 | 2 | 7 | 4 | 3 | 9 | 3 | 6 | 48 |
| Mining Engineering | 0 | 2 | 2 | 2 | 0 | 1 | 1 | 2 | 5 | 4 | 1 | 20 |
| Petroleum Engineering | 1 | 2 | 1 | 0 | 1 | 1 | 4 | 3 | 3 | 2 | 1 | 19 |
| Physics | 3 | 3 | 8 | 6 | 3 | 7 | 9 | 7 | 5 | 7 | 9 | 67 |
| unspecified | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 1 | 3 |

## Biases
* Only people with an explicit joining date on their profile can enter the faculty/dept/news sets; people appointed before 2016 with no explicit date are missed.
* Physics, HSS, Geophysics and Electronics pages have the most structured lists, so they supply the dept-page share.
* Faculty with long, well-maintained lists contribute up to 5 papers; sparse pages 1-2. List order follows each page (newest first), sampling spread evenly through it.
* Medium confidence dominates (90 %): affiliation visible only for arXiv rows.
