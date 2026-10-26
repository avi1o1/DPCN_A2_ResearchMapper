# Golden set: IIT Palakkad (iit_palakkad), 2016-2026, lab notebook

Built on 2026-10-25 by an independent sub-agent. No bibliographic API was used for discovery: no Crossref, OpenAlex, Semantic Scholar, Europe PMC, DOAJ, ORCID, DBLP, Google Scholar, Scopus, IRINS, DataCite or the arXiv API.
`WebScrape/iit_palakkad.json` and the other pipeline outputs were not read. Every URL went through the shared fetcher `scratchpad/tools/polite_get.py` (392 fetch calls, logged in `work/iit_palakkad_golden/data/fetch.log`). Downloads are in `work/iit_palakkad_golden/data/` and scripts are in `work/iit_palakkad_golden/code/`.

**Result:** 308 distinct papers in `golden/golden_iit_palakkad.csv`.

| evidence_source | rows | confidence | rows with DOI |
|---|---|---|---|
| faculty_page | 161 (52 %) | all medium | 63 |
| annual_report | 56 (18 %) | 46 high, 10 medium | 10 |
| dept_page (CE dept page + 5 lab sites) | 40 (13 %) | all medium | 17 |
| arxiv (PDF affiliation checked) | 34 (11 %) | all high | 0 (no arXiv DOIs recorded) |
| news (institute news + newsletters) | 17 (6 %) | all high | 0 |
| **total** | **308** | 211 medium / 97 high | 90 (29 %) |

Types: journal 213, conference 51, preprint 34, book-chapter 6, book 2, other 2 (an IEEE standard and an IBC paper).

## Departments x years coverage
| Department | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 | total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Biological Sciences and Engineering |  |  |  |  |  |  | 3 | 4 | 2 | 3 | 3 | 15 |
| Chemistry | 1 | 1 |  | 2 | 1 | 2 | 5 | 13 | 7 | 6 | 4 | 42 |
| Civil Engineering |  | 2 | 4 | 5 | 7 | 7 | 6 | 9 | 11 | 6 | 3 | 60 |
| Computer Science and Engineering | 1 | 1 |  | 6 | 5 | 2 | 4 | 4 | 4 | 2 | 4 | 33 |
| Data Science |  |  |  | 2 | 1 |  |  | 3 | 2 | 10 | 4 | 22 |
| Electrical Engineering | 1 | 1 | 2 | 3 | 7 | 4 | 5 | 7 | 5 | 2 | 2 | 39 |
| Environmental Sciences and Sustainable Engineering Centre |  |  |  |  |  |  | 1 | 1 | 1 | 2 |  | 5 |
| Humanities and Social Sciences |  |  |  | 2 | 1 |  |  | 1 |  |  |  | 4 |
| Mathematics |  | 1 | 2 |  | 1 | 1 | 2 | 1 | 1 | 3 | 3 | 15 |
| Mechanical Engineering |  |  |  | 4 | 4 | 6 | 6 | 5 | 4 | 7 | 3 | 39 |
| Physics | 3 |  | 1 | 1 | 1 | 2 | 5 | 4 | 4 | 8 | 5 | 34 |

Materials and Metallurgical Engineering has 0 rows. Its 2 current faculty (Aramanda Shanmukha Kiran and Ravi K R) both joined in 2026: neither appears on any Wayback faculty list up to 2026-06, and Ravi K R was at IIT Jodhpur until 2026. Every paper they list is from before they joined. The MME research page (mme.iitpkd.ac.in/research) lists projects, not papers. Kali Prasad (ME, also listed on the MME research page) is in the set.

## 1. Faculty pages (iitpkd.ac.in/people/<id>), source "faculty_page"
* Roster: `https://iitpkd.ac.in/faculty-list` has 161 current faculty in 12 units. All 161 profile pages were fetched (200).
* Page types:
  * 83 pages have a structured "Publications" view: title linked to doi.org or the publisher, then authors, then "venue (year)". These look hand-entered in Drupal (each entry has upload-preprint and edit-node fields).
  * The rest have free-text "Selected publications" lists, a link to Google Scholar only, or nothing.
* Sampling:
  * Per department, the eligible faculty are those with 3 or more structured entries or a free-text list with 15 or more year mentions. They were taken evenly spaced through the alphabetical roster: 5 each for ME, CE, EE and CSE; 3 each for Maths, Physics, Chemistry and DS; 2 each for HSS and BSE; 1 each for MME and ESSENCE (38 initially).
  * Faculty with zero in-tenure papers were replaced by the next eligible person: sagi to santhakumar, spchoudhury to divyapv, biren to mkj, srimanta to vivek, manojgopal to smanni, debabratadhara to sushabhan, garima to sahely, biswajit to anoop, prasannabhat to bayry, mayank to sovan, msm to revathyp. askiran (MME) had no replacement.
  * Per faculty: up to 5 in-tenure entries, spread evenly over the list in list order (not the first 5, because lists are newest-first). The brief's cap is 8, so 5 is stricter. This gives 39 faculty, at most 5 papers each.
* Tenure rule:
  * A paper is accepted only if its year is strictly greater than the joining year J.
  * J comes from the person's own page bio where it is stated. Otherwise J is the year of the first Wayback snapshot of the institute faculty list that shows the person (40 snapshots, 2015-07 to 2026-06, all through the fetcher).
  * Papers published in the joining year are rejected as ambiguous.
  * This is stricter than the brief's "inside tenure" rule. The tenure source is quoted in `notes`.
* Yield: 161 profiles visited, 39 used, 161 rows (2 duplicates merged between Jasine Babu and Krithika Ramaswamy).
* Rejected: 324 structured entries were outside tenure or had no year (the largest counts were mintu 26, sushabhan 22, vivek 21, amit 20, smanni 19). All listed papers were rejected for 11 recent joiners or people with unclear tenure:
  * spchoudhury: joined Jul 2026; all papers from IIT Guwahati.
  * manojgopal: joined Jul 2026, from IIT Madras.
  * garima, debabratadhara, prasannabhat, biswajit, sagi, mayank: joined 2024-25; their lists stop before they joined.
  * msm: joined Jan 2022; his list stops at 2020.
  * srimanta: first seen 2022-05; his list stops at 2021.
  * askiran: joining date unknown; papers carry Michigan co-authors.
  * biren: no list, only a Google Scholar link.

## 2. Annual reports, source "annual_report"
* The live page `https://iitpkd.ac.in/reports-brochures` returned a JavaScript (eval-packed) bot challenge. It was **not** bypassed.
* PDF URLs came from (a) web search (query: `IIT Palakkad annual report pdf publications list`, restricted to iitpkd.ac.in) and (b) a Wayback copy of reports-brochures (2025-12-07), which gave the 2016-17 and 2015-16 English PDFs.
* Reports used: 2016-17, 2017-18, 2018-19, 2019-20, 2020-21, 2021-22, 2022-23 and 2023-24. The 2015-16 report has no publication list. The 2024-25 report was not found.
* Text was extracted with `pdftotext`. The bilingual layout meant using the English section, which runs from the "Research Publications" heading to the "Conferences/Workshops" heading.
* Sampling: 7 points evenly spaced through the English section of each report; at each point, the first complete entry was taken. Duplicates of rows already collected, "under review" items and items without a title were skipped (an author-ambiguous item was resolved from the section heading).
* 2020-21 text has damaged ligatures ("CalibraFon"); titles were reconstructed by hand and this is noted in those rows.
* Confidence: high (rule (a), institute report). It was lowered to medium (10 rows) when the paper is from the person's joining year or clearly from a previous affiliation, for example Technion, Florida, NUS, Mainz, IGCAR or KAUST co-authors only. The annual reports demonstrably list such papers.
* Yield: 8 reports, 56 rows.

## 3. Department and lab pages, source "dept_page"
* Department sites fetched:
  * ce.iitpkd.ac.in/publications: 12 paginated pages, 244 entries. Used.
  * cse.iitpkd.ac.in/publications: only a link "for an updated list". Not used.
  * ee.iitpkd.ac.in: its publications link points to publications.iitpkd.ac.in, which is **IRINS** and forbidden. Not used.
  * math.iitpkd.ac.in/research.html: lists areas only.
  * mme.iitpkd.ac.in/research: lists projects only.
  * iitpkd.ac.in/publications: an aggregate of the same Drupal entries as the faculty pages. Not used, because it is not independent of section 1.
* CE department page: 16 points evenly spaced over the 244 entries. From each point, the next entry was taken that names a matched CE faculty member, is inside that person's tenure and is not a duplicate. That gave 15 rows. 26 entries were rejected on the way: 6 duplicates and 20 outside tenure. The department list contains many pre-joining papers, for example 2016 Texas A&M and Auburn work.
* Lab sites. These were linked from faculty pages, and the labs were chosen for faculty not sampled in section 1:
  * 2D Materials Group (Jayakumar B)
  * theo-chemistry@iitpkd (Padmesh A): its section is headed "Publications From IIT Palakkad"
  * CompCat Group (Rositha K)
  * Sarmistha Singh's Water Resources lab
  * HydroClimate Analytics (Subhasis Mitra)
* PKLAB (pklabiitpkd) renders by JavaScript, so its page was empty. creds.iitpkd.ac.in failed with an SSL error. cci-iitpkd.github.io had no publications.
* From each lab: 5 published in-tenure entries spread over the list (submitted and under-revision items skipped). 25 rows.

## 4. arXiv PDFs, source "arxiv"
* `https://arxiv.org/robots.txt` **disallows /search** and asks for a 15 s crawl delay. So arXiv listing search on the website was not used. The fetcher enforces 5 s for arXiv; an extra 10 s sleep was added between arXiv requests.
* Discovery came from web search restricted to arxiv.org, with these strings:
  * `"Indian Institute of Technology Palakkad" arxiv`
  * `"IIT Palakkad" arxiv.org`
  * `Palakkad Kerala 678623 arxiv preprint`
  * `"Palakkad" "Department of Mathematics" arxiv`
  * `"Palakkad" "Department of Electrical Engineering" OR "Mechanical Engineering" OR "Chemistry" arxiv`
  * `"Indian Institute of Technology Palakkad" "Computer Science" arxiv 2019 2020 2021`
  * `"IIT Palakkad" OR "Indian Institute of Technology Palakkad" arXiv 2017 2018 preprint physics`
* Also used: arXiv ids linked from faculty pages and lab pages (6 ids; 1 was from 2014 and out of range).
* 38 PDFs were fetched, all 200. The affiliation was checked in the first 2 pages of text, or the full text when needed.
* Accepted 35; 1 was a duplicate of a faculty-page row, so 34 rows remain. Rejected:
  * 1807.00735 and 2212.07621: no Palakkad affiliation.
  * 2512.10885: duplicate of a lab-page row.
* Year is the arXiv v1 year from the identifier.

## 5. News and web, source "news"
* Institute news (iitpkd.ac.in/news): 77 listing pages were fetched, giving 919 unique items. Item titles were filtered with the regex `publish|journal|cover|paper|article|research work|spotlight|featured|highlight`, which matched 36 items. 25 were opened after excluding sports, colloquium, advisory-board and similar items; 2 more items found by web search were also opened.
* Items naming a paper title produced 12 rows. Items without a paper title were rejected: the ACS Bio & Med Chem Au cover, the Sens. Diagn. 2024 cover (it has a DOI but no title), the Dalton 2026 cover, Bayry's Cell Rep Med and Nature Reviews editorials, the stroke BCI press item, the EMBC finalist item, "Sensing Sulfamethazine" (a highlight name, not a paper title), and the NSF item on Jaiswal (DOI 10.1111/gcbb.12937 printed, but no title, and no Crossref lookup allowed).
* Newsletters:
  * The `iitpkd.ac.in/newsletter` index gave the Sahyadri TechXpress issues Jan 2024, May 2024, Sep 2024, Jan 2025 and Jun 2025. They produced 2 rows. Their feature articles mostly give no paper titles.
  * The MFSDSAI (Data Science school) newsletter, Dec 2025 issue, has a Publications section. It produced 3 new rows (2 others were duplicates).
* External web search for press coverage had nearly zero yield. These strings returned only IRINS (publications.iitpkd.ac.in) listings or unrelated pages, so no rows came from them:
  * `IIT Palakkad researchers study published journal`
  * `"IIT Palakkad" study published thehindu OR newindianexpress OR "times of india" researchers paper`
  * `IIT Palakkad professor paper journal 2019 research finds`
  * `"IIT Palakkad" researchers paper published news research highlight`
  * `iitpkd.ac.in news research paper published journal faculty IIT Palakkad team`
* There is no row with evidence_source=websearch. Web-search-discovered arXiv papers are labelled "arxiv", because that is where the affiliation evidence was seen. Their notes say "found via web search".

## Known biases
* **Recency:** 69 % of rows are from 2021-2026, and 2016-2018 has 21 rows. This reflects the institute's growth (it was founded in 2015 and had about 40 faculty in 2017) and the strict tenure rule, but it also comes from faculty-page lists that favour recent work and from arXiv web search returning recent preprints.
* **Survivorship:** faculty pages exist only for current faculty. Former faculty appear only through the annual reports, the CE page and arXiv: K. L. Sebastian, P. B. Sunil Kumar, Satyajit Das, H. V. R. Mittal, M. C. Valsakumar, and visiting faculty Sunitha K Nayar.
* **Indexing:** the faculty-page structured lists are hand-entered and DOI-linked (63 of 161 rows have a DOI). They may favour indexed journal papers over conference papers in CS and EE. The free-text and lab lists are less biased this way.
* **Affiliation:**
  * About 2/3 of the rows are medium confidence (tenure-based, affiliation not seen).
  * Annual reports and department pages demonstrably include papers from before a person joined. These were downgraded or excluded where visible, but some may remain.
  * The Wayback "first seen" date is only an upper bound on the joining date. It is conservative for acceptance but may let through papers written just after joining that were done elsewhere.
* **Department mix:** Civil Engineering is over-represented (60 rows) because it is the only department with a usable publication page. HSS (4) and MME (0) are thin. BSE and ESSENCE are small units.
* **Students and postdocs:** they appear only as co-authors, plus 4 student-led news items and several arXiv preprints with student first authors.
* **Duplicates of record:** some arXiv preprints may also exist as published versions with different titles. Matching should allow title variants.
