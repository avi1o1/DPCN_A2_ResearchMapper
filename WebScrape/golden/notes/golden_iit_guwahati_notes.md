# IIT Guwahati golden set: lab notebook

Final: 576 papers, 189 distinct IITG authors, 2016-2026, 144 with a DOI (25%). Built by two agent sessions (the first lost to a usage limit; its saved intermediate data was reused and the missing parts, arXiv verification, news and assembly, were completed).

## Sources (found -> kept)
| source | share | rows | confidence | how |
|---|---|---|---|---|
| faculty_page | 66.7% | 384 | medium | 179 personal pages on fac.iitg.ac.in reached from iitg.ac.in faculty-details pages (92 people yielded entries). Per person: parsed publication entries, dropped any with year <= joining year, de-duplicated, then took up to 5 entries spread evenly through the list (not first N). Pre-capped at 5, global cap 8. |
| annual_report | 12.5% | 72 | medium | Annual reports 2016-17, 2017-18, 2018-19 (iitg.ac.in/report/docs/AR/*.pdf) publication tables, pdftotext; authors matched to the roster, tenure rule applied. Reports 2015-16 and 2019-20 onward have no usable publication tables (checked 2019-20..2022-23: no tables), so this source is confined to 2016-2019. |
| dept_page | 12.0% | 69 | medium | Mechanical Engineering publications pages (/mech/research/publications/, 15), Chemistry yearly PDFs 2016-17 and 2017-18 (31), Physics /phy/publication.php (23). Other departments' pages either had no lists or were already covered via faculty pages. |
| arxiv | 8.0% | 46 | high | 60 arXiv abs pages + PDFs fetched via the polite fetcher (found by web search restricted to arxiv.org and arXiv links on faculty pages); kept only when "Guwahati" is printed on PDF page 1. 13 rejected (no IITG on page 1). First-version year from the id. |
| news | 0.9% | 5 | medium | Institute press releases (iitg.ac.in/iitg_press_all, 226 items; 119 research-looking ones fetched). 25 link a paper; publisher pages for ~18 returned 403/202 challenges and were skipped (never bypassed). Only 6 publisher pages gave a title; 5 kept. |

Deviation from the target mix (50/15/15/10/10): faculty pages are over-represented because they are the only source that covers 2020-2026; annual reports stop at 2018-19; external news coverage rarely names the paper title, so the news share is about 1%. Web searches for DOIs of news-linked papers returned nothing useful.

## Search strings / page types used
Web search: "IIT Guwahati researchers published journal study news", "IIT Guwahati research highlights published in journal 2024" (iitg.ac.in), "IIT Guwahati press release research paper DOI", "IIT Guwahati news the paper titled", plus targeted lookups (Gopal Das fuel adulteration, Rajiv Kar graphene oxide, Sil dark matter PRL) and 8 exact-DOI searches (no hits). Page types: iitg.ac.in faculty list/details, fac.iitg.ac.in homepages, department pages, annual report PDFs, arXiv abs/pdf, institute press pages.

## Rules applied
Tenure: joining year from the roster (own page, else NIRF, else first archived list snapshot: an upper bound). A rule-(b) paper must have year strictly after joining year. Faculty-page, annual-report, dept-page and news rows are `medium`; arXiv with affiliation on the PDF are `high`. DOIs are only those printed on the source page or reached publisher page (faculty-page DOIs as printed; arXiv DOI only when shown on the abs page).

## Rejected / excluded
- Institute library "Journal publication data" PDFs (iitg.ac.in/lib/IITCouncil/2324, 2425, 2526): downloaded one listing check only; they are a Scopus export ("Source: Scopus"), so excluded as Scopus-backed. They were not used for any row.
- IRINS (iitg.irins.org) links in the roster: never used.
- 13 arXiv papers with no IITG on page 1; 1 arXiv paper (Ranjan et al., 2204.01848) dropped after assembly: only "alumni.iitg.ac.in" email, no clear IITG affiliation at the time.
- Mech: 2 Ravi Sankar Mamilla papers (2018, 2019) failed tenure; Physics: 1 A.K. Das paper failed tenure; many faculty-page entries with year <= joining year (counted by the selector).
- Exact title duplicates across sources (kept the higher-evidence copy; priority arxiv > news > faculty_page > dept_page > annual_report) and papers beyond 8 per author (cap rows, e.g. D. Maity, U. S. Dixit).
- News item with a roster-unmatched author (Ankur Verma, 2026) dropped.

## Coverage (department x year)
|dept|2016|2017|2018|2019|2020|2021|2022|2023|2024|2025|2026|tot|
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Biosciences and Bioengineering|12|7|6|8|7|10|9|3|4|5|1|72|
| Centre for Disaster Management and Research|1|1|1|0|1|0|1|0|0|0|0|5|
| Centre for Linguistic Science and Technology|0|0|1|0|0|0|0|0|0|0|0|1|
| Chemical Engineering|7|8|8|12|6|1|4|7|6|5|0|64|
| Chemistry|6|26|11|1|2|7|0|3|3|1|1|61|
| Civil Engineering|3|10|3|4|3|4|1|0|5|4|3|40|
| Computer Science and Engineering|3|6|6|3|6|7|2|3|6|3|1|46|
| Design|0|2|3|1|3|4|2|5|0|2|1|23|
| Electronics and Electrical Engineering|5|4|6|5|2|4|5|7|4|5|3|50|
| Humanities and Social Sciences|3|7|7|4|6|2|5|3|6|2|3|48|
| Mathematics|3|1|2|1|0|1|1|3|1|2|1|16|
| Mechanical Engineering|3|14|18|4|1|1|2|3|2|2|0|50|
| Mehta Family School of Data Science and Artificial Intelligence|0|0|0|0|0|0|2|0|3|1|1|7|
| Physics|9|7|14|15|6|4|2|5|6|7|2|77|
| School of Agro and Rural Technology|0|0|0|0|1|0|1|1|1|7|4|15|
| School of Energy Science and Engineering|0|0|0|0|0|0|0|0|0|1|0|1|

## Known biases
- 2017-2018 over-represented (annual reports and Chemistry/Mechanical PDFs); Chemistry 2017 and Mechanical 2017-18 spikes.
- 90% medium confidence: affiliation not visible on the paper; a paper by a person who held a second affiliation could be included. Faculty without a joining year in the roster (and former faculty) are largely absent from tenure-based sources.
- Only rosters' persons with own web pages (92 of 179 pages yielded entries); units without faculty pages (several schools, centres) are thin.
- arXiv is physics-heavy (23 of 46); arXiv-sampled papers are only those a web search surfaced.
- The "department" for faculty-page rows is the roster/institute listing for the person; faculty with several listings get the first one.
- Most rows have no DOI (not printed on the source lists); DOI coverage 25%, strongly skewed to faculty pages that print them and arXiv abs pages.
- Annual reports 2019-20 onward and the fixed 8-per-person cap (5 from pages) cap prolific authors.
