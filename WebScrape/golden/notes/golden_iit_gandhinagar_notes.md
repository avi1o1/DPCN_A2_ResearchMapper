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
