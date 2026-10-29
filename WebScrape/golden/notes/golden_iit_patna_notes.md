# IIT Patna golden set: lab notebook

Final: 391 distinct papers, 2016-2026, 10 academic departments. Build interrupted twice (usage limit, network); the second agent reused the first agent's saved candidate rows and added annual-report and arXiv rows.

## Sources and yield
| source | label | found/visited | rows kept |
|---|---|---|---|
| Faculty profile publication fields on iitp.ac.in department pages (Next.js pages `/departments/<dept>`, parsed from the embedded JSON) | faculty_page | 10 department pages, ~118 faculty | ~290 |
| Faculty personal homepages `www.iitp.ac.in/~<id>/` (publication sub-pages) | faculty_page | ~70 homepages fetched, 48 publication pages | ~60 |
| Annual Report 2017-18 (Wayback copy of the iitp.ac.in PDF, per-department "Papers Published in Journals") | annual_report | 1 of 6 reports usable | 24 |
| arXiv abs pages + PDF first page (found via web search restricted to arxiv.org) | arxiv | ~30 IDs searched, 17 with IIT Patna affiliation printed | 17 |
| news / research highlights | none | 4 web searches + institute news and "latest research in news" pages | 0 |

Search strings used: arxiv "Indian Institute of Technology Patna" Department of CSE/Physics/Mathematics/Mechanical/Civil/EE (several variants); "IIT Patna researchers study published in journal research highlight news"; iitp.ac.in news/research published.

## Rules applied
* Tenure rule (b): joining year from the person's own page (list in code), else the first archived (2016) faculty-list snapshot that shows them (upper bound; Wayback). Paper kept only if year is strictly after the joining year (and before a stated departure year).
* Faculty-page rows are `medium` (no affiliation on the paper). arXiv rows are `high` (affiliation printed on PDF page 1). Annual-report rows are `medium`.
* Max 8 papers per person (non-arXiv); within a list entries were taken evenly spaced, newest-first order not truncated. Years 2023 and 2024 were trimmed to ~60 rows each (from the most-represented people) to even the year spread.
* DOIs only where printed in the source list or on the arXiv abs page (81 of 391, ~21%).
* Excluded faculty with unresolved/ambiguous tenure (Amit Kumar Singh, Rahul Kumar Singh, Lokman Hakim Choudhury) from the faculty-page rows.

## Rejected / skipped
* Entries marked "accepted", "under review", "to appear": skipped.
* arXiv hits with no IIT Patna affiliation on the PDF (2404.09215, 2404.19360, 2306.09198 coauthor-only, 1909.00669 PDF text had no match): skipped.
* Annual reports 2016-17, 2019-20 (Wayback copies truncated at 1 MB, unreadable), 2020-21, 2021-22, 2022-23, 2023-24 (live iitp.ac.in links return 404; Wayback fetches timed out): not used. 2018-19 report downloaded but two-column layout garbled authors/titles: not used.
* Department / lab sites (me.iitp.ac.in, alpananayak.org, a Google-Sites lab page): no publication lists with years; no dept_page rows.

## Coverage (rows by department)
CSE 69, Physics 65, HSS 45, Chemistry 42, Civil 39, Mechanical 29, Chemical 28, Electrical 26, Mathematics 26, Metallurgical 21 (plus a handful moved by dedup). Years: 2016: 3, 2017: 17, 2018: 38, 2019: 40, 2020: 35, 2021: 39, 2022: 55, 2023: 59, 2024: 64, 2025: 39, 2026: 2.

## Known biases
* About 90% of rows come from faculty profile pages, far from the brief's 50% mix; dept pages, news and later annual reports were unavailable. Source mix is therefore skewed and tenure-based (medium confidence).
* Years 2016-2017 and 2026 are thin: faculty lists are newest-first and tenure filtering removes pre-joining papers; the 2016 archived list gives upper-bound joining years.
* Faculty with no own publication list online are absent; former faculty and non-faculty-led papers are almost absent (only via arXiv).
* Faculty with 0 hits in parsed lists were not covered (Computer Center, Endangered-language centre have no faculty data).

<!-- SUPPLEMENT 2026-10-28 (extension pass) -->
## Supplement: extension pass (+49 rows)
* Annual Report 2018-19 (complete 31 MB Wayback PDF, `pdftotext -raw` fixes the two-column garbling): 711 journal+conference entries parsed from the 10 department sections; 42 kept as new annual_report rows (medium; tenure rule (b) via roster joining_year strictly before paper year; max 8/person across all rows; entries already present skipped; entries with ambiguous initial-only author matches skipped).
* Annual Report 2017-18 (1 MB truncated copy, text via Ghostscript txtwrite): most entries had lost text after column splitting; only 8 fully intact entries (3 from 2016, 5 from 2017, conference/journal) kept. 313 entries without a printed year were skipped.
* Annual Reports 2016-17, 2019-20: truncated copies unreadable (no xref; gs/pdftotext fail). 2020-21 to 2023-24: iitp.ac.in copies return 404; Wayback fetches of the 2021-22/2022-23/2023-24 PDFs failed with connection errors. Not used.
* Not done (session interrupted twice, time): new faculty homepages, department/centre dated lists, further arXiv PDFs, news pages. Source mix therefore remains faculty_page-dominated; no dept_page/news rows; 2026 still thin.
* Bias: new rows are tenure-based medium; added mostly 2018-2019 (the readable report), small gain for 2016-17.
