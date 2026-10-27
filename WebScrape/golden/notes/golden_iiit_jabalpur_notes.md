# Golden set: PDPM IIITDM Jabalpur (iiit_jabalpur), 2016-2026, lab notebook

Built on 2026-10-27 by an independent sub-agent for operator Arihant Tripathy. No bibliographic API was used for discovery (no Crossref, OpenAlex, Semantic Scholar, Europe PMC, DOAJ, ORCID, DBLP, Google Scholar, Scopus, IRINS, DataCite, arXiv API or arXiv /search). `WebScrape/iiit_jabalpur.json` and other pipeline output were not read. All fetches went through `agents/polite_get.py` (wrapper `work/iiit_jabalpur_golden/code/pg.py` only decodes brotli, because the fetcher cached raw brotli bodies, and strips HTML). Downloads: `rm_work/iiit_jabalpur_golden/data/`; scripts: `work/iiit_jabalpur_golden/code/` (row files in `rows/*.psv`, `compile.py` builds the CSV).

**Result:** 274 distinct papers in `golden/golden_iiit_jabalpur.csv` (target 300 not reached: see Shortfall).

| evidence_source | rows | confidence |
|---|---|---|
| faculty_page | 167 | medium |
| dept_page | 32 | medium |
| annual_report | 38 | medium |
| arxiv (affiliation read on the PDF first page) | 12 | high |
| news (institute achievements page) | 25 | high |

Types: journal ~176, conference 68, book-chapter 12, preprint 12, book 6. DOI printed on the source for about 25 % of rows (DOIs only as printed; truncated or mangled DOIs were dropped).

## Departments x years (rows)
| Department | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 | total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Computer Science and Engineering | 5 | 5 | 3 | 5 | 6 | 10 | 12 | 2 | 6 | 6 | 1 | 61 |
| Design | 1 |  |  | 1 | 2 | 2 | 1 | 3 |  | 3 | 1 | 14 |
| Electronics and Communication Engineering | 2 | 10 | 4 | 5 | 9 | 12 | 9 | 4 | 11 | 6 | 1 | 73 |
| Liberal Arts |  |  |  |  |  | 3 | 2 | 1 | 2 | 1 | 1 | 10 |
| Mechanical Engineering | 5 | 4 | 7 | 8 | 6 | 5 | 9 | 12 | 8 | 5 | 8 | 77 |
| Natural Sciences (Mathematics) | 1 | 1 | 1 | 2 | 1 |  | 2 | 4 | 1 | 2 |  | 15 |
| Natural Sciences (Physics) | 1 | 3 | 1 | 2 | 1 | 4 | 7 | 4 |  | 1 |  | 24 |

Smart Manufacturing has 0 rows: sm.iiitdmj.ac.in is an 85-byte page with no faculty or publication content.

## Sources, search strings, yield
1. **Institute faculty portal** `faculty.iiitdmj.ac.in` (roster page + profile pages). The roster lists only 65 unique faculty (the "All" tab and department tabs repeat each person; some profiles are external links to scholar/Google Sites and were not used). 59 profiles were fetched (all 200). Page type: Drupal-style profile with "Professional Experience" (dates, used for tenure), "Books/Book chapter" and "Publications" sections, in free text of very varied formats. Profiles with usable publication lists and a joining year: 24 persons used. Sampling: entries spread evenly through each list (not first N), at most 8 per person across all sources, in-tenure only. Patents and conference-organiser entries on profiles were excluded.
2. **Department pages**: CSE `publication.php?year=2016..2022` (per-year lists with DOIs; years 2023+ not offered), ECE `pdf/ece-d/publications.pdf` (2020-2022), ME `Publications.html` (2018-2021), NS `pub.php` (2018-2023), LA `Journals.html`/homepage news. ECE `journals.html` only links per-year PDFs up to 2018 (not fetched). Yield per page: CSE 7 rows used, ECE 4, ME 3, NS 16, LA 2.
3. **Annual reports** (`iiitdmj.ac.in/downloads/Annual Report/...`): 2016-17, 2019-20, 2021-22, 2022-23, 2024-25 have text publication lists; 2017-18, 2018-19, 2020-21 and 2023-24 are image-only PDFs (pdftotext returns nothing), so were not usable (no OCR). 2019-20 entries carry no year, so only two of its entries with a year known from another page were used. Each row's IIIT author was checked to appear in that report's departmental faculty roster (grep). 
4. **arXiv**: web search (queries such as `site:arxiv.org "IIITDM Jabalpur"`, `arxiv "PDPM IIITDM Jabalpur"` plus topic or faculty names, `arxiv "iiitdmj.ac.in"`), then PDF first page read through the fetcher. 17 candidates examined: 12 kept (affiliation visible), rejected: 1512.06232 (Dec 2015, out of range), 1302.2718 and 1507.06056 (2013, 2015), 2407.17512 (no IIITDM affiliation on PDF), 1906.06117 (withdrawn, 404). No 403 from arXiv occurred.
5. **News**: the institute's `achievement.php` page (award notices that give exact paper titles, venue and the IIITDMJ scholar or faculty). Used in place of external news, which the web search did not surface. Yield 25 rows, years 2017-2026; student-led papers are mostly here.

## Decisions and tenure handling
* Tenure rule as in the brief: year strictly after the joining year (rule b, `medium`), or affiliation visible (rule a, `high`).
* No joining year on page (accepted with on-page evidence, noted `tenure: on-page evidence`): Asish Kundu (head of NS 2012-14 and continuing), Neeraj Jaiswal (committees from Aug 2014), Fareen (institute FIG project Feb 2021, so 2021+ only), Mamta Anand (dated LA news 2021-22, Head of LA in 2024-25 report).
* Excluded for unknown tenure: Ayan Seal, Nihar Jena, Mukesh Roy, Sachin Kumar, Sanjeev N. Sharma, Koushik Dutta, Akshay Pandey (profile lists IIT Roorkee-era papers), Himansu Nanda on faculty page (bio says IIITDMJ 2017-19 then "currently" truncated; used only through annual report 2024-25 roster and news). Recent joiners (Avinash Raja Mar 2024, Satish Tiwari Jan 2024, Syam Kumar 2024, Nitish Andola 2024, Shivansh Mishra): only papers after joining year via reports. Entries inside the joining year were rejected unless affiliation visible.
* Rejected candidates (examples): Ponappa's 2020-21 papers (Kongu affiliation likely, kept only 2022 and 2023 items), Tushar Choudhary's 2013-2019 items, CSE 2022 dept entries whose first IIIT author has no tenure data, entries with truncated titles and no DOI (e.g. Wafi, Rao, Deepmala "On Kantorovich form of generalized Sz..."), Durgesh Singh patents, "Machine Vision and Augmented Intelligence" proceedings volumes by non-IIIT editors.
* Former faculty: none identified (the portal lists current faculty only); students and scholars appear as lead authors in the news and some report rows.
* Authorship attribution: for student-led papers the cap is counted against the first-named IIIT author that is faculty; Tushar Choudhary is at 8 (one annual-report row dropped to respect the cap).

## Shortfall and deviations from the brief
* 274 vs 300: stopped because remaining sources were exhausted or unusable (image-only annual reports, per-year pages missing after 2022 for CSE, NS and ECE, faculty profiles that stop around 2023, only ~65 faculty on the portal).
* Source mix differs: faculty 61 % (target 50), dept 12 % (15), annual report 14 % (15), arXiv 4 % (10; web search finds few IIITDMJ arXiv papers), news 9 % (10).
* Year skew: faculty profiles are mostly last updated in 2022-2023, so 2023-2026 are thinner on the faculty/dept side, and 2026 has only 12 rows.

## Known biases
* Over-represents faculty who maintain a detailed profile, and CSE/ECE/ME (large units) over Design, LA, Mathematics.
* Medium-confidence rows rely on the person's tenure, not on affiliation printed on the paper, so a few may carry other affiliations (e.g. coauthor-led papers).
* Annual-report and news items favour conference and student papers; DOI coverage is low (≈25 %).
* Brief issues: the brief's "IIT" wording read as "this institute"; the fetcher stores brotli bodies undecoded (worked around in `pg.py`, fetcher untouched).
