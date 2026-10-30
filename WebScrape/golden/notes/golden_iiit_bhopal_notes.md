# Golden set notes: IIIT Bhopal (operator Arihant Tripathy, run 2026-10-30)
Output: golden/golden_iiit_bhopal.csv, 59 papers, all confidence `medium` (rule b: tenure), 35 with DOI (59%). Target of 100 NOT reached (see below).

## Sources used and yield
* Faculty profile pages and API descriptions (cached by roster agent in rm_work/iiit_bhopal_roster/data/ff and fac.json; 46 pages + 38 API records, institute web pages, no new fetches made): 45 papers.
* Annual reports 2022-23 and 2023-24 (cached text ar4/ar5, "Publications" / "Research Outcome" lists): 14 papers. Reports 2018-19, 2019-20, Jan-Dec 2020 have no publication lists; 2024-25 report is an image-only PDF (unreadable); no reports exist for other years.
* arXiv, news, department/lab pages: 0. The institute has no research-highlight/news pages with papers (file folders Magazine, Events, research talk contain no paper lists). Web search (WebSearch, queries: `arxiv "Indian Institute of Information Technology Bhopal" paper`, `"IIIT Bhopal" research paper 2019 Department of Computer Science and Engineering Bhopal affiliation`) returned only IISER Bhopal and other institutes' pages, so no arXiv papers or rule-(a) papers were found. No arXiv fetching was done. No live fetches at all (polite fetcher unused; everything came from the roster cache).
* Source mix deviates from design (faculty 50/dept 15/AR 15/arXiv 10/news 10): the unavailable shares were moved to faculty pages and annual reports.

## Method
Extracted paper-like lines from profile texts (code/ext.py), kept entries with year strictly after the person's joining year (roster, itself from own page/annual reports), dropped workshops/awards/patents, deduplicated, took up to 8 per person spread evenly (the pages are lists of mixed order; the actual entries chosen are listed in code/build.py). Annual-report entries added only when an author's tenure satisfied the rule. DOIs only as printed on the profile page or report; 24 rows have none printed.
Per first-named IIIT author counts: {'Bhupendra Singh Kirar': 8, 'Afreen Khursheed': 8, 'Yatendra Sahu': 8, 'Deepa Sharma': 5, 'Dharmendra Dangi': 5, 'Nisha Singhal': 5, 'Shalini Stalin': 5, 'Nikhil Kumar Singh': 6, 'Sonal Telang Chandel': 2, 'Vishakha Chourasia': 3, 'Neeraj Kumar': 1, 'Anjani Kumar': 1, 'Rekha Kaushik': 1, 'Gaurav Khanna': 1}.

## Coverage (department x year)
| Department | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 | total |
|---|---|---|---|---|---|---|---|---|
| Computer Science and Engineering |  |  | 2 | 9 | 4 | 1 |  | 16 |
| Electronics and Communication Engineering | 1 | 3 | 7 | 6 | 3 | 2 |  | 22 |
| Information Technology |  | 2 | 2 | 3 | 5 | 2 | 1 | 15 |
| Mathematics |  |  |  | 3 | 2 |  |  | 5 |
| Physics |  |  |  |  | 1 |  |  | 1 |

No papers for 2016-2019: the institute started teaching in 2017 and almost all faculty on the roster joined 2020 or later (joining years: 2019 Kirar; 2020 Sahu, Khursheed, Sharma, Stalin; 2022 Chandel, Singh, Chourasia, Singhal; most others 2023-2026). With rule (b) (year strictly after joining year) nothing earlier can qualify, and no paper with visible IIIT Bhopal affiliation (rule a) was found. Humanities has no entries (no current faculty; former Humanities staff have no usable sources). Physics only 1 paper (Kumar), ECE and IT most.

## Rejected / skipped candidates
* All entries dated up to the joining year (about 70% of what profile pages list; e.g. Chaurasia 2019-2024 papers, Subhrajyoti Deb, Chandrabhan Patel, Sunil Kumar, Anjani Kumar pre-2024), because they were probably written elsewhere and affiliation on paper was not checked.
* Joining-year papers (e.g. Nandanwar/Vishwakarma 2024 MTA papers, Director A.K. Singh 2023 papers, Neeraj Kumar 2023 IETE paper, Nikita Acharya 2023 AIP paper).
* Gaurav Kumar Bharti, Gagan Vishwakarma, other former staff: no institute-stated joining year (ORCID only) so excluded.
* Non-paper items on profile pages (webinars, STTPs, awards, patents, reviews), duplicates between profile page and report.
* Papers by A. K. Singh (Director, joined 2023) in report 2022-23 excluded (2023 = joining year).

## Known biases
Heavy skew to 2021-2025 and to the few faculty who joined 2019-2022 (Kirar and Khursheed and Sahu at the 8-paper cap); medium confidence only; year of some entries is the volume/proceedings year printed on the source (online-first earlier); some co-authors are MANIT visiting faculty or students whose own affiliation was not checked; one DOI is an SSRN preprint DOI (Stalin, Computer Networks, as printed on source); no publisher pages were visited so DOIs are unverified against the paper.
