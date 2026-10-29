# IIT Gandhinagar golden set - lab notebook

Run resumed after an interruption (usage limit). Inherited from the first run: Wayback copies of the 165 current-faculty profile pages (`https://web.archive.org/web/20260301000000/https://iitgn.ac.in/faculty/<unit>/<slug>`, 206 fetched, 165 with a parseable "Recent Publications" block), 38 arXiv abs pages + PDFs, annual-report PDFs 2018-19 .. 2023-24 (2016-17 and 2017-18 and 2022-23 not retrievable: ConnectionError / HTML stub). Live iitgn.ac.in returns 403 to the fetcher: not bypassed, Wayback only.

## Result
349 rows (target 450 not reached). Source: faculty_page 227, annual_report 100, arxiv 22 (dept_page 0, news 0, websearch 0). Confidence: high 22 (arXiv PDF page 1 shows IIT Gandhinagar), medium 327. DOI printed on source for 110 rows (31 %); no lookups. Planned mix (50/15/15/10/10) missed: faculty 65 %, AR 29 %, arXiv 6 %, dept/news 0 %.

## Method and counts
* Faculty pages: 791 list lines from 165 profiles; 520 had a year 2016-2026; 209 rejected as year <= joining year; heuristic title extraction + manual reading for the rest; 33 selected lines dropped (non-papers such as positions/editorships, titles truncated in the page text, DOI-only lines, duplicates across co-authors, and papers whose printed affiliation shows another institute, e.g. INSPIRE-style lines listing IIT Bombay for a person, and Penn State / Tuebingen-era papers of two physicists). Up to 8 per person, taken evenly through the list. Tenure rule: joining_year from the roster (first archived appearance, upper bound); blank = already listed on the June 2016 page, treated as 2015. Strictly year > joining year -> `medium`.
* arXiv: 38 papers (reached from profile/lab links, no arXiv API/search); 22 kept: affiliation visible in PDF first 2 pages and year >= joining year; 10 rejected (no "Gandhinagar" on pp. 1-2), 5 (no roster author matched), 1 before joining. Year = v1 submission.
* Annual reports: only AR 2018-19 and 2019-20 contain per-paper lists (parsed from pdftotext; 2019-20 layout is irregular, 'book' labels there were wrong and set to journal). AR 2020-21, 2021-22, 2023-24 give counts only. Entries matched to a current roster person by surname + first-name prefix (unmarked authors; starred = student, # = staff). 345 entries without a current-faculty match, 23 outside tenure. Selected <=3 per person, round-robin over units until 100. AR listing = `medium`. Some AR DOIs lost a dot in text extraction (e.g. ...ndteint.2019102150); kept as printed in extracted text.
* Search strings used (WebSearch): "IIT Gandhinagar researchers published study journal news"; "IIT Gandhinagar lab group publications 2023 2024 journal papers list site"; "\"IIT Gandhinagar\" researchers paper titled published in journal 2024". Fetched: theprint.in (seawater / graphite, no title printed; paper already in set from Gopinadhan page), theprint hydrogel page, navjeevanexpress (409). News pieces gave no exact titles, aggregate pages (Nature Index, Rankless) are Scopus/OpenAlex-like and not used. Wayback of iitgn.ac.in/news and /research/highlights: 404. Hence dept/lab and news shares are 0.

## Coverage (unit x year)
| Unit | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 | total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Biological Sciences and Engineering | 1 | 1 | 7 | 5 | 3 | 5 | 0 | 0 | 0 | 0 | 0 | 22 |
| Chemical Engineering | 0 | 2 | 10 | 3 | 1 | 0 | 1 | 6 | 1 | 0 | 0 | 24 |
| Chemistry | 0 | 1 | 5 | 12 | 2 | 0 | 0 | 3 | 1 | 2 | 0 | 26 |
| Civil Engineering | 0 | 0 | 4 | 8 | 5 | 1 | 5 | 6 | 7 | 4 | 0 | 40 |
| Cognitive and Brain Sciences | 0 | 4 | 3 | 7 | 5 | 1 | 1 | 0 | 2 | 0 | 0 | 23 |
| Computer Science and Engineering | 0 | 0 | 1 | 8 | 6 | 0 | 1 | 0 | 3 | 2 | 0 | 21 |
| Earth Sciences | 0 | 1 | 3 | 2 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 7 |
| Electrical Engineering | 0 | 1 | 4 | 3 | 6 | 2 | 3 | 4 | 5 | 6 | 3 | 37 |
| Humanities and Social Sciences | 0 | 0 | 3 | 9 | 3 | 1 | 2 | 0 | 2 | 4 | 0 | 24 |
| Materials Engineering | 1 | 1 | 9 | 8 | 8 | 3 | 0 | 0 | 1 | 1 | 0 | 32 |
| Mathematics | 2 | 2 | 7 | 9 | 7 | 2 | 0 | 4 | 2 | 3 | 0 | 38 |
| Mechanical Engineering | 0 | 1 | 4 | 9 | 4 | 1 | 6 | 2 | 1 | 2 | 0 | 30 |
| Physics | 0 | 1 | 6 | 7 | 3 | 0 | 1 | 0 | 0 | 2 | 5 | 25 |

## Biases
* Years 2018-2020 over-represented (AR 2018-19/2019-20); 2016, 2017 and 2021 thin. Earth Sciences thin; former/visiting faculty and students are absent (profiles only for current faculty; AR matching restricted to current faculty).
* Faculty lists favour senior people with maintained pages; many profiles list papers without year (skipped) or only pre-joining work.
* Rows mostly `medium` (tenure inferred); roster join years are upper bounds, so true joining may be earlier (papers of the joining year are excluded).
* Venue strings abbreviated as printed on pages; some blank where truncated. `type` for Arpan Bhattacharyya items set to other (venue not printed).

## Supplement (extension run, 349 -> 450 rows)
Rows added: 101 (annual_report 82 from AR 2016-17 / 2017-18, 8 from library "Staff Publications" in AR 2020-21 .. 2023-24, arxiv 11). Totals now: faculty_page 227, annual_report 190, arxiv 33, dept_page 0, news 0, websearch 0. Confidence high 33 / medium 417. DOI printed for 165 rows (37 %).

### Sources and yields
* Annual reports retried: AR-2016-17, AR-2017-18, AR-2022-23 were "not retrievable" earlier because the fetched capture (timestamp 20200923, 1 MiB) was truncated by Wayback. Using the CDX listing (`web.archive.org/cdx/search/cdx?url=iitgn.ac.in/assets/pdfs/AnnualReport/AR-<yr>.pdf&output=txt`) other captures were found: 2016-17 at 20220107230806 (8.0 MB), 2017-18 at 20220108031522 (2.9 MB), 2022-23 at 20231010234435 (3.0 MB). `pdftotext -raw` gives clean text.
  * AR 2016-17: per-unit lists (journal 232, conferences 161 in the report's own totals); 379 entries parsed (journal + conference), 277 matched to roster people, 256 passed tenure/dedupe; 50 selected (<= 2 per person, round-robin over units, years 2016/2017 preferred).
  * AR 2017-18: bullet-style per-unit lists (journal 273 in the totals); 484 parsed, 407 matched; only 2017-dated items (plus Earth Sciences) considered; 32 selected, 82 AR rows in total after dedupe/cap.
  * AR 2022-23: only counts (574 journal articles etc.) plus library staff publications (3 used). Library "Staff Publications" also in AR 2020-21 (1), 2021-22 (1), 2023-24 (3): 8 rows, department "Central Library", non-faculty authors (not on the faculty roster).
  * AR 2024-25 (Annual-Report-2024-25-English-Web.pdf, 7.5 MB) and Annual Letters 2016-2024 exist in the CDX list; not fetched (letters have no paper lists; 2020-21, 2021-22, 2023-24 reports re-checked with -raw: still counts only).
* arXiv (web search restricted to arxiv.org, no /search or API; abs + PDF via the fetcher): 19 ids examined, 11 kept (IIT Gandhinagar printed on the PDF or acknowledgement; 2021: 4, 2025: 1, 2026: 5, 2018: 1). Rejected: 1907.12036, 2411.04610, 2112.12966 (no IITGN on PDF), 2203.01596 and 1811.10122 (acknowledgement only), 1702.06568 (not fetched, no IITGN evidence in search snippet), 2406.16324 (a thesis, not a paper). Search strings: "arxiv.org Indian Institute of Technology Gandhinagar Earth Sciences ...", "IIT Gandhinagar arxiv 2016 OR 2017 ...", "IIT Gandhinagar arxiv 2021 Gandhinagar, Gujarat ...", "arxiv 2021 iitgn.ac.in email ...", Earth-science/glacier variants. No 2016/2017/Earth-Sciences arXiv paper with IITGN printed was found.
* Lab / department / news pages: none found. Web search surfaced no archived lab publication lists or news pieces with titled papers; iitgn.ac.in/news and /research/highlights Wayback copies are 404 (earlier run). dept_page and news stay 0. IRINS/Vidwan pages appeared in search results and were not used.

### Rule application
* AR rows: `medium`; year strictly > roster joining year (blank = on June 2016 page, treated as 2015); at most 2 per person per report, 8 per person overall (counted over all rows; arXiv rows by the printed author). Authors marked `*` (student) or `#` (staff) without roster match were dropped (heading assignment and name parsing unreliable); library staff rows are the only non-roster, non-arXiv authors.
* DOIs: as printed in the report text; line-break spaces removed (e.g. "10.1117/1. JRS...").
* Dept = roster department of the matched person (AR headings were unreliable for two-column pages).

### Coverage change
Year: 2016 4->35, 2017 15->66, 2021 17->21, 2026 8->13 (AR 2020-21/2021-22 have no paper lists, so 2021 gains are only arXiv + library). Earth Sciences 7->14 (AR 2016-17 and 2017-18 lists; Vikrant Jain, V. N. Prabhakar, Prem Chand Pandey). Central Library 0->8.

### Biases and caveats (new)
* 2016/2017 now over-represented relative to 2022-2025 (report lists only cover those years); AR 2016-17 lists include conference papers (112 of the eligible entries) so the conference share rose.
* Report listings can include papers written before a person joined; tenure rule uses roster upper bounds (join year may be earlier) and drops joining-year papers.
* 2021 remains thin (21) and 2022-2025 rely on faculty pages; arXiv rows include non-roster postdocs/students (Rajat Gupta, Rahul Kumar, Soumyarup Banerjee, Mrinal Anand, Aditya Garg, Aakash Gupta, Joydip Saha), whose tenure is shown only by the printed affiliation. Urjit Yajnik is a roster visiting professor.
* Parser quirk: a few venues for conference rows include the city and date as printed.
