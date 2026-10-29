# Golden set notebook: IIIT Delhi (iiit_delhi), 2016-2026

Operator: Arihant Tripathy (IIIT team). All fetching through `WebScrape/agents/polite_get.py`. Not used: Crossref, OpenAlex, Semantic Scholar, Europe PMC, DOAJ, ORCID (API or site), DBLP, Google Scholar, Scopus, IRINS, DataCite, arXiv API/search. Pipeline output for this institute not read. Roster-agent files used: only the cached institute faculty-list snapshots and NIRF PDFs/parsed tables under `rm_work/iiit_delhi_roster/data` (institute web pages, not pipeline output).

**Result:** 433 papers (target 450 not reached, see "Why 433"). confidence: {'medium': 420, 'high': 13}. DOI printed on the source for 247 rows (57 %). Types: {'conference': 131, 'journal': 288, 'preprint': 11, 'book-chapter': 3}. Evidence source: {'dept_page': 375, 'annual_report': 28, 'arxiv': 11, 'news': 11, 'faculty_page': 8}. 101 distinct first-named IIITD author strings, max 8 per person. Years 2016-2026 with 41 rows each except 2016 (24) and 2026 (40).

## Hosts that do not resolve (Wayback used)
`iiitd.ac.in`, `www.iiitd.ac.in`, `faculty.iiitd.ac.in` answered `DEAD:SSLError` from the fetcher on this machine (TLS failure, not a bot wall); `ece.iiitd.ac.in` was only read via Wayback as well. Every institute page below was therefore read from a Wayback copy (`web.archive.org/web/<ts>id_/...`; the snapshot timestamp is in each `source_url`). arXiv PDFs were fetched directly (status 200, no 403).

## Sources, counts, yield
| source | pages visited | entries parsed | rows kept |
|---|---|---|---|
| Institute year-wise "Research > Publications" page (dept_page): Wayback 2018-12-30 (lists 2016-2018, faculty-supplied) and Wayback 2026-07-31 (lists 2019-2026, APA style, about 2900 entries) | 2 | 2018 copy 273 (2015-18); 2026 copy 2885 | bulk of the 375 dept_page rows |
| Ph.D./Masters scholar publications pages, Wayback 2017-01-29 (2016 block only) | 2 | 33 | within dept_page |
| ECE department publications page (ece.iiitd.ac.in/publications.html), Wayback 2025-12-15 (2017-2020 blocks) | 1 | 182 | within dept_page |
| Annual reports 2015-16 and 2016-17 (Appendix A per-faculty lists), Wayback | 2 | 169 + 86 quoted-title entries | 28 |
| Faculty/lab pages (Wayback): WISE lab (Arani Bhattacharya, 2026-04), Bagler publications (2024-10); also fetched Saket Anand, Shad Akhtar, Arun Balaji Buduru, Debajyoti Bera homepages (no parseable list in static HTML) | 7 | 21 usable | 8 |
| ECE department news (ece.iiitd.ac.in/news.html, Wayback 2026-07-01); only items carrying a year in their text used | 1 | 55 paper items | 11 |
| Institute research-news page (iiitd.ac.in/research/rsnews, Wayback 2026-06) | 1 | 0 usable (events/awards only) | 0 |
| arXiv PDFs (page 1 read with pdftotext) | 14 | 11 accepted | 11 |

Web searches (search tool): `IIIT Delhi annual report publications list faculty journal conference papers pdf` (iiitd.ac.in); `arxiv "IIIT Delhi" "Indraprastha Institute of Information Technology Delhi" 2019 paper`; `arxiv.org abs "IIIT-Delhi" computational biology OR mathematics OR "human-centered design" 2020 2021 2022`; `IIIT-Delhi researchers paper published news research highlight faculty professor study`; `arxiv "Indraprastha Institute of Information Technology" Delhi 2017 OR 2018 OR 2016 abstract`; `faculty.iiitd.ac.in publications list selected publications journal conference`; `IIIT Delhi lab publications page mathematics OR social sciences OR "computational biology" faculty publications`; `arxiv "IIIT-Delhi" Department of Computational Biology OR "Department of Mathematics" OR "Social Sciences and Humanities" 2019 OR 2020 OR 2021 OR 2022`; `arxiv "Indraprastha Institute of Information Technology Delhi" "Electronics and Communications Engineering" OR "Human Centered Design" 2019 2020 2021`. Page types: year-wise institute publications page, faculty lab page, department page, annual-report appendix, department news, arXiv PDF.

Planned mix was faculty 50 / dept 15 / annual report 15 / arXiv 10 / news 10. Actual: dept_page 86 %, annual_report 6 %, arxiv 2 %, news 2 %, faculty_page 1 %. Reasons: the new IIITD faculty profile pages carry no publication lists (publications are delegated to IRINS, forbidden); personal homepages are mostly dynamic or stale; annual reports 2017-18 onward could not be downloaded whole (Wayback copies truncated at 1 MiB / 5 MiB or timed out; 2015-16 and 2016-17 read fine); web search surfaces few arXiv abstract pages by affiliation without the forbidden arXiv search.

## Tenure handling
Joining year: NIRF faculty tables 2022-2025 (roster agent cache, earliest dated row per name), else first archived faculty-list snapshot 2016-2020 (an upper bound; stated in notes). Current faculty: year strictly after the NIRF joining year (medium). Faculty seen in the 2016-2020 snapshots but absent from the 2026 list (former; leaving year unknown): accepted only for years between first and last snapshot in which they appear (note says "on-page evidence"). Annual-report and institute-list entries never print the affiliation, so those rows are `medium`; `high` only for arXiv PDFs (affiliation on page 1) and ECE news items that state "IIIT Delhi" beside the author.

## Matching authors to faculty
Authors on list entries were matched to a faculty table (2026 list + snapshot names) by surname + first initial or full name. Common surnames (Kumar, Singh, Gupta, Sharma, Shah, Das, Roy, Ray, Sen, Bose, Mitra, Jain, Garg, Arora, Goyal, Nair, Kaur, Mukherjee, Ghosh, Bhattacharya, Prasad, Sinha, Banerjee, Mishra, Dutta, Ram, Kar) were accepted only on a full-name match, which drops many true IIITD papers by such faculty (bias below) but avoids homonym false positives.

## Coverage (department x year, rows)
| dept | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 | total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Computational Biology | 1 | 5 | 9 | 2 | 8 | 4 | 7 | 7 | 7 | 7 | 7 | 64 |
| Computer Science and Engineering | 4 | 14 | 11 | 16 | 11 | 11 | 11 | 11 | 11 | 11 | 13 | 124 |
| Electronics and Communications Engineering | 19 | 15 | 12 | 15 | 10 | 10 | 10 | 10 | 10 | 10 | 16 | 137 |
| Human-Centered Design | 0 | 0 | 0 | 0 | 4 | 5 | 4 | 3 | 3 | 6 | 1 | 26 |
| Mathematics | 0 | 7 | 3 | 4 | 3 | 5 | 5 | 5 | 5 | 4 | 1 | 42 |
| Social Sciences and Humanities | 0 | 0 | 6 | 4 | 5 | 6 | 4 | 5 | 5 | 3 | 2 | 40 |

HCD rows start in 2020 and SSH rows in 2018 because those units have no matched faculty in the snapshots/NIRF before then; Mathematics has none in 2016 (department founded 2017).

## Rejected / skipped
List entries before the person's joining year or after the last snapshot (former faculty); entries with quote marks inside the title (two titles on one line); titles under 12 characters; 2015 entries; annual reports 2017-18 and later (download truncated); arXiv 1603.06527 (Samrith Ram: no IIITD affiliation visible on PDF page 1), 2309.09126 (NUS authors only), 2109.01936 (unit of the IIITD students not stated, supervisor unknown). IRINS/Scopus-backed portals were never opened. The 2016 "top conference" highlight list (no author names) was not used.

## Why 433
Per-person cap (8) over about 100 usable first-named authors, a 2016 pool of only about 100 matched entries (2016 page lists are sparse and ECE-heavy) and the strict common-surname rule.

## Known biases
1. The 2019-2026 year-wise institute page is APA-style with Scopus-like venue strings; it is a static institute page, but its content may be Scopus-derived. It supplies 86 % of rows, so independence from Scopus-fed sources is weaker than for a faculty-page-based set. These rows are flagged `dept_page` and can be separated.
2. Venue type is heuristic (journal 288, conference 131): APA entries without proceedings words default to journal, so conference papers are probably under-counted for a CS-heavy institute.
3. Faculty with common surnames under-represented; former faculty only through the 2016-2020 snapshots; 2016 thin and ECE-heavy; 2026 covers to about July 2026.
4. APA titles are cut at the first sentence end (a few may be truncated at an abbreviation); venue strings cleaned heuristically; one `Findings of ... ACL` item may be typed book-chapter.
5. Rows carry the faculty member's department, not necessarily the unit of student first authors.
