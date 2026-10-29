# Golden set: ABV-IIITM Gwalior (iiit_gwalior), 2016-2026, lab notebook

Built by an independent sub-agent (operator: Arihant Tripathy). No bibliographic API or aggregator was used for discovery: no Crossref, OpenAlex, Semantic Scholar, Europe PMC, DOAJ, ORCID, DBLP, Google Scholar, Scopus, IRINS, DataCite or arXiv API/search. `WebScrape/iiit_gwalior.json` and other pipeline output were not read. Every URL was fetched through `WebScrape/agents/polite_get.py` (log: `rm_work/iiit_gwalior_golden/data/fetch.log`, about 190 calls); scripts are in `rm_work/iiit_gwalior_golden/code/`, downloads in `.../data/`.

**Result:** 268 distinct papers in `golden/golden_iiit_gwalior.csv` (target 300 not reached, see "Why 268").

| evidence_source | rows | confidence | with DOI |
|---|---|---|---|
| faculty_page (iiitm.ac.in profiles + 2 personal sites) | 170 (63 %) | medium | most of the 65 |
| annual_report (2015-16, 2017-18, 2018-19, 2020-21, 2021-22, 2022-23) | 58 (22 %) | medium | 0 (reports print no DOIs) |
| news (Gunjan institute newsletters 2022-I, 2024-I) | 19 (7 %) | medium | 0 |
| arxiv (PDF affiliation checked) | 21 (8 %) | high | 1 (printed in PDF) |
| dept_page | 0 | | |
| **total** | **268** | 247 medium / 21 high | 65 (24 %) |

Types: journal 185, conference 59, preprint 21, book-chapter 2, book 1. 71 distinct first-named ABV-IIITM authors (cap 8 per person respected, counted against the first-named one). Year range 2016-2026.

## Source reconnaissance and what each yielded
* Faculty list `https://iiitm.ac.in/staff` (79 faculty cards, incl. one "Retired" and one "On Deputation"; adjunct list not used): 79 profile pages fetched. Only ~50 profiles carry a publication list (section "Selected Publications"/similar, 7-20 items); 29 have counts only. Candidates parsed: about 1,240 lines; sampled evenly (up to 5 per person, newest-first lists, so every k-th entry rather than the first N).
* Department pages (CSE, IT, EEE, Management, Engineering Sciences), centre pages (Rekhi, CAS, CBR) and lab pages (Generic Lab 1/2, 5G, Robotics, IoS): fetched, they hold only overviews and faculty lists, no publications. Hence **no dept_page rows**; that share (planned 15 %) was moved to faculty/annual-report/newsletter rows.
* `old.iiitm.ac.in` (linked "for internal users"): connection failed repeatedly (outage and then no answer); skipped.
* Personal homepages linked from profiles (Google Sites): 12 fetched; most are JS shells with no text. Publication pages used: Santosh S. Rathore (3 rows) and Rakesh Chowdhury (2 rows); Ajay Kumar's publications page was empty. trustlab.netlify.app returned an empty shell.
* Annual reports (iiitm.ac.in/annual-reports): 2015-16 (Scopus list, used for 2016 rows), 2017-18, 2018-19 (selected lists), 2020-21 to 2022-23 (long lists), 2019-20 (accounts only, no list), 2023-24 (faculty profiles only, no paper list). About 795 roster-matched candidate entries, 58 selected spread evenly within each report (max 2-3 per person).
* Newsletters "Gunjan": 10 PDFs fetched; only 2022 Vol.1 and 2024 Vol.1 have a text "Publications" list (99 roster-matched candidates); 2022-II, 2023-I/II, 2025-II, 2026-I, issues 21/23 are image-only PDFs (no text layer); 2025-I lists only counts. No external news coverage was searched (institute "Media Coverage" page lists only month names), so the institute newsletter fills the news share (7 %, below the planned 10 %).
* arXiv (general web search restricted to arxiv.org, queries below; abs/PDF fetched through the fetcher at 5 s spacing, never `/search`, no 403): 30 PDFs fetched; 21 kept where the PDF itself shows ABV-IIITM/IIITM Gwalior; the rest rejected (see below).
* Search strings used (WebSearch, allowed_domains arxiv.org): `"ABV-Indian Institute of Information Technology and Management Gwalior"`; `"ABV-IIITM Gwalior" India preprint`; `"Indian Institute of Information Technology and Management, Gwalior" Pattanaik OR Tapaswi OR Singh OR Trivedi OR Dhar`; `"ABV-IIITM" Gwalior deep learning wireless communication physical layer security Shukla Pandey`; `"IIITM Gwalior" management supply chain OR finance OR marketing ...`; `"ABV-IIITM" Gwalior mathematics OR physics OR "Engineering Sciences"`; four author-name OR-queries (Arya/Kala/Sadhya/Rathore; Shukla/Yadav/Punn/Singya; Shukla/Mishra/Jeevaraj/Singh/Kant/Dhar; Prasad/Patel/Sharma/Trivedi/Kumar/Ansari); `"Indian Institute of Information Technology and Management" Gwalior "Morena Link Road" 2017 OR 2018 OR 2021 OR 2022`; `"ABV-IIITM" Gwalior wireless sensor network OR VLSI OR image watermarking OR blockchain OR reinforcement learning`; `"ABV-IIITM" Gwalior "Department of ..." 2023 2024`. The search tool is a general web search, results are snippets; recall for arXiv is certainly incomplete (physics/maths and early years almost absent).
* No Wayback copies and no bot-walled pages were needed. No evidence_source `websearch` rows.

## Tenure rule and evidence
* Joining dates come from NIRF "Faculty Details" tables on the institute site (NIRF 2025 and 2026 Engineering/Management PDFs, e.g. Arya 1 Sep 2008, Dhar 30 Nov 2006, Sadhya 21 Feb 2019, Kaur 26 Dec 2022, Pandey 23 Jan 2024), supplemented by the person's own page (Rathore March 2019; Ajay Kumar July 2009). A paper counts only if its year is strictly after the joining year (rule b, confidence medium). Same-year papers were excluded unless affiliation is visible on the paper (arXiv rows, high).
* Annual-report and newsletter rows: author matched by surname+initials against the roster (ambiguous cases `Kumar, A.`, `Singh, V.` etc. deliberately not matched); tenure rule applied; listing alone is not affiliation evidence, hence medium.
* Gopal Krishan Sharma (retired): no joining date; accepted as medium with tenure "on-page evidence" (listed in the 2015-16 annual-report faculty list and co-authoring with current faculty).
* Excluded: Ritu Tiwari (page says "since 2008" but NIRF lists a 2025 visiting appointment: conflicting), Anupam Shukla in report/newsletter matching (on deputation, initial `A.` ambiguous; only kept via faculty-profile rows where the profile lists the paper, one row), faculty with no joining date anywhere (Neelesh Yadav, Yannam, Swain, Parihar, Neeraj Jaiswal, Narendra Dewangan, Tsering Thargay, Ankur Jaiswal, Kumbhare), and faculty who joined 2025 or later unless a 2026 paper exists.
* Faculty who joined 2023-2024: their listed 2024-2026 papers may report pre-joining work done elsewhere; they pass the strict-after rule but are the likeliest false positives (flagged in notes for the Tartu case). Former faculty are represented only indirectly (e.g. Prasenjit Chanak appears as co-author in report entries but has no tenure evidence, so no row is credited to him).

## Quality of extraction
Titles/venues of profile and report rows were parsed semi-automatically from citation strings and then hand-patched for ~60 cases. Annual-report PDFs lose the "tt" ligature; titles were repaired heuristically (Pattern, Letters, attack, attention...), so a few titles may differ from the printed form by a ligature. A handful of venue strings are conference names without proceedings title. DOIs were recorded only if printed in the source line (65 rows); none was looked up.

## Rejected candidates (examples)
* arXiv 2604.18148 (KIIT authors; only mentions ANTIC at IIITM), 2212.05319, 2005.13694, 2105.xxxx-unrelated hits, 2001.02669, 2303.06310, 2112.13553, 2210.00275, 2601.20678, 1811.06567 (JNU thesis, acknowledgement only): no ABV-IIITM author affiliation in the PDF. 2101.02819, 0909.0245: outside scope (bio-note of alumnus; 2009).
* Profile items that were not papers (calendar text, patents, grants, invited talks): dropped by filter. Profile items by homonyms (three `Shukla, A.` items on chemistry/power topics): dropped.
* Items at or before the joining year (e.g. Gaurav Pandey's 2020/2016 papers, Irshad Ansari's 2020-2023 list, Dewangan 2021-2023): excluded by rule (b).

## Departments x years coverage (rows)
| Department | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 | total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Computer Science & Engineering | 1 | 3 | 4 | 2 | 3 | 6 | 19 | 8 | 14 | 5 | 2 | 67 |
| Electrical & Electronics Engineering | 0 | 2 | 0 | 0 | 5 | 8 | 11 | 5 | 18 | 9 | 7 | 65 |
| Management Studies | 2 | 2 | 4 | 3 | 3 | 7 | 9 | 7 | 11 | 9 | 2 | 59 |
| Information Technology | 3 | 4 | 2 | 1 | 1 | 3 | 5 | 3 | 9 | 9 | 5 | 45 |
| Engineering Sciences (incl. 1 "Applied Sciences") | 4 | 3 | 3 | 1 | 1 | 1 | 5 | 1 | 5 | 2 | 3 | 29 |
| Not stated (student-only arXiv papers) / mixed IT+Mgmt | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 1 | 3 | 0 | 5 |

Counts of the first six columns were taken before removing two malformed 2016 rows and the final dedupe; totals above are the final CSV (268). All five academic units and all eleven years are covered; 2019 (7) and 2016 (10) are the thinnest years because the 2019-20 annual report has no list and 2016 papers are rarely in profile lists. The two research centres (CBR, CAS, Rekhi) have no separate publication lists.

## Why 268 and not 300
Profile publication lists exist for only ~50 of 79 faculty and mostly cover recent years; new joiners (2022-2025, about half of the faculty) have few papers that satisfy the strict-after-joining rule; department/lab pages and old.iiitm.ac.in yielded nothing; most newsletters are image-only. Remaining sources would require forbidden aggregators.

## Known biases
* Recency: 2022 and 2024 are over-represented (profile lists are newest-first and the two text newsletters are 2022 and 2024).
* Faculty-centric: former faculty and PhD/postdoc-only papers are almost absent; student-led papers appear only through arXiv (5 rows).
* Tenure rule (b) rows (249 of 268) are medium: affiliation was not verified on the paper itself; collaboration-heavy faculty pages (e.g. EEE antenna groups, Management case/bibliometric papers) may list work done at other institutes.
* Only papers listed by the institute (profiles, reports, newsletters) can enter; institute reports are Scopus-derived, so Scopus-uncovered output (many Management conference papers, books) is under-represented. Some papers appear in several faculty lists but are credited once to the first-named ABV-IIITM author.
* Department assigned from the faculty roster, not from the paper.


## Post-check fix (operator, 2026-10-27)
`check_outputs.py` found one duplicate title; the duplicate row was removed (kept the row with higher confidence / a printed DOI). Rows: 268 -> 267.
