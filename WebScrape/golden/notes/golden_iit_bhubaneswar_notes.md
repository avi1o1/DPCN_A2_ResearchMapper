# Golden set notes: IIT Bhubaneswar (450 papers, 2016-2026)

Built independently of the harvest sources (no Crossref/OpenAlex/S2/EPMC/DOAJ/ORCID/DBLP/Scholar/Scopus/IRINS/arXiv API). All fetches through polite_get.py. The run was resumed after an interruption; earlier saved work was reused (faculty-page and annual-report selections, arXiv pages/PDFs, department-page parses).

## Sources and yield
| source | rows | how |
|---|---|---|
| faculty_page | 197 | own profile pages (secs/sbs/sms/sif/seocs/smmme/shssm.iitbbs.ac.in, 232 profile pages cached); entries spread evenly through each newest-first list, cap 8 per person, 82 faculty |
| annual_report | 48 | IIT Bhubaneswar annual reports 2017-18 to 2022-23 (publication sections; 3294 entries parsed, even spread, one-two per person) |
| dept_page | 54 | SBS Chemistry/Mathematics/Physics publications pages (20; these pages list 2025 only), SMS research publications page (32, 3-4 per year 2016-2025), SECS publications-and-patents page (2) |
| arxiv | 28 | arXiv abs page + PDF reached from web search / institute pages; affiliation line quoted from the PDF. 32 candidates fetched; 4 rejected (2404.09215, 2412.11083, 2601.06430, 2602.20267: no IIT Bhubaneswar affiliation in PDF). 2 duplicates of other rows dropped |
| news | 1 | institute press release (Nature Cities, May 2024). Institute "media coverage" pages and IITBBS Express newsletters (12 volumes) were fetched but contain image clips / no citable paper details; web searches (4) surfaced only the Nature Cities paper and a bauxite paper (Journal of Geochemical Exploration, Jan 2026) whose title was not confirmed, so not included |
| websearch | 122 | Central Library research-publications list (library.iitbbs.ac.in/publications.php, 42 of 277 pages fetched, 1258 entries parsed); see bias note |

Web search strings: "IIT Bhubaneswar researchers study published in journal"; "IIT Bhubaneswar researchers study findings published Nature Cities urbanization warming Indian cities"; "IIT Bhubaneswar study published journal arsenic OR landfill OR lakes OR schizophrenia researchers"; "IIT Bhubaneswar professor team study published in journal 2025".

## Confidence
high = 29 (28 arXiv PDFs with affiliation printed + 1 press release). medium = 421: faculty/dept/annual-report listings satisfy tenure rule (b) only (joining year from NIRF submitted-data, earliest across 2023/2024/2026 submissions, an upper bound on joining; paper year strictly after joining year); library rows are medium (institute list, affiliation not checked on paper).

## Coverage (rows)
Units: Electrical and Computer Sciences 110, Basic Sciences 110, Infrastructure 68, Mechanical Sciences 58, MMME 37, Earth Ocean and Climate Sciences 35, HSSM 32.
Years: 2016 38, 2017 37, 2018 37, 2019 38, 2020 38, 2021 38, 2022 37, 2023 37, 2024 51, 2025 53, 2026 46.
DOI printed on source for 134 rows (30%); DOI-less rows kept as listed.

## Rejected / skipped
- arXiv: 4 candidates above. Faculty entries before/at joining year dropped by tenure rule. Library entries: retraction notices, "Message", editorials, forewords, titles < 25 chars excluded; at most 2 library rows per author string.
- Not used: IRINS (iitbbs.irins.org), Scopus-backed widgets, IIT BBS Express newsletters (no paper details).

## Biases
- Faculty-page and report rows are medium only; arXiv skews to physics/maths and to few groups (Ghosh/Bandyopadhyay appear several times; arXiv rows are not subject to the per-person cap beyond 8).
- Library rows were chosen greedily to fill thin units/years, so they over-represent HSSM, MMME, EOCS relative to output, and exceed the 10-15% target share for non-faculty sources; faculty pages are 44% rather than 50%; news 0.2% (not available).
- 2024-2026 are over-represented because profile lists are newest-first and recent people dominate.
- Library list ordering is not strictly by year; only 42 pages sampled, so coverage of its 8295 entries is partial.
