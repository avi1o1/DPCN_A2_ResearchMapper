# Lab notebook: IIIT Bhagalpur golden set (81 papers; target 100 not reached)

## Sources used (all via polite_get.py; operator Arihant Tripathy)
* https://iiitbh.ac.in/faculty (faculty list page, 1 page) -> 35 linked faculty CV PDFs (faculty_page). 33 had text; 1 scanned (Anita Chandra, no text), 1 non-academic (industry CV). Yield: 38 rows from 12 CVs that give a publication list plus a joining year.
* Annual reports 2019-20, 2020-21, 2021-22, 2022-23 (iiitbh.ac.in/audit-and-annual-report). 2019-20 has no publication list (counts only); the other three have "Published Journal Papers / Conferences / Book Chapters" lists. Yield: 41 rows. Annual Report 2023-24 and later were not found on the page.
* Web search (2 queries): "IIIT Bhagalpur faculty research paper published arXiv", restricted to arxiv.org, and "IIIT Bhagalpur researchers publish paper journal news". Gave 2 arXiv papers (abs page + PDF read: 2410.16411, 2606.28083); the news query gave nothing. No institute news/research-highlight page with paper lists was found (iiitbh.ac.in/about-research fetched, no lists).
* No Wayback fetches; no arXiv 403 encountered. Not used: dept pages (the site has no per-person publication lists), IRINS (forbidden), Google Scholar etc.
* Search strings: see above. Note: first fetch loop on CVs failed (CRLF in URL list, 404s); redone with cleaned list, all 35 returned 200.

## Source mix achieved vs plan
faculty_page 38 (47%), annual_report 41 (51%), arxiv 2 (2%), dept_page 0, news 0, websearch 0. Deviations: no dept/lab pages with lists, no news coverage; annual-report share enlarged because it was the only other list source. The arXiv share is far below 10% because arXiv-affiliation search is thin for a young institute.

## Confidence
79 medium (tenure rule b: year strictly after joining year, joining year from faculty-list snapshots = upper bound; roster file iiit_bhagalpur_faculty.csv), 2 high (arXiv PDFs with printed IIIT Bhagalpur affiliation). Annual-report-only rows are medium and also satisfy the tenure rule. DOI recorded only when printed on the CV/report: 28 of 81 (35%).

## Coverage (department x year)
Departments: ECE 34, CSE 29 (incl. STAG, department assumed from topic, not stated on paper), MEA 10, BSH 9. Years: 2018:1, 2019:4, 2020:12, 2021:15, 2022:21, 2023:10, 2024:11, 2025:5, 2026:2. 2016 and 2017 are empty by construction: the earliest joining year is 2017 and the strict "after joining year" rule excludes them. Rule (a) could have admitted them only with visible affiliation, which no source showed.
Faculty per unit: ECE 7 (Jha, Sinha, Sanjay Kumar, Ranjan, A. Choubey, S. Raj, D. Bhattacharya); CSE 6 (Choubey, Biswal, Om Prakash Singh, Thejaswini, Tewari, Bhattacharyya) + Varun Sharma; MEA 4 (Sunil Singh, Nath, Gautam, Vishal Soni); BSH 2 (Tiwari, Nayak). Max per person <= 8 (Choubey 8, Tiwari 8, Sanjay Kumar 7).
Humanities and Social Sciences (visiting only) is not covered.

## Rejected / skipped candidates
* Pre-joining or joining-year papers (excluded by tenure rule): e.g. Dilip Choubey 2020 and earlier (joined Nov 2020), Suraj (CV papers all 2014-2018, joined 2019), Abhinav Gautam (CV papers 2016-2019, joined 2020), Purnendu Mandal (2018), Sateeshkumar Kanakannavar (2023 paper = joining year), Chetan Barde (joined 2023; pre-2023 papers listed on his CV), Thejaswini 2019 papers, Pankaj Tiwari 2021 and earlier, Dheeraj Sinha 2016-2017, Sunil Singh 2018 conference.
* No joining year in roster (guest/adjunct/visiting: Nehal Ahmad, Subhayu Ghosh, Vishnu Bayari, Rounak Biswas, Sumit Raj, Uttam Kumar etc., CVs without tenure evidence) or joining 2025-26 with only older papers: excluded (no on-page tenure evidence). Himadri Nayak CV has no publication list; only one co-authored paper from the annual report.
* Pankaj Tiwari's list is long; took 8 spread over 2022-2024 (cap). Dilip Choubey, Om Prakash Singh also capped/subsampled.
* Annual-report items whose IIIT author is not in the roster (Rashmi Sinha, Santosh Mahto, Komal Roy, Debolina Das, Ranjeet/Praveen Kumar etc.) were not used unless a rostered IIIT author co-authored.
* Pradeep Biswal 2022 TENSYMP paper marked "under publication"; skipped.

## Biases
1. Heavy reliance on self-reported CVs and annual reports: affiliation at time of work is inferred from tenure only (medium); some "joining years" are upper bounds from archived lists, so some papers may pre-date actual joining (false positives) or the rule may exclude genuine early papers (false negatives; 2016-2017 missing).
2. Skewed to faculty that publish CVs (12 of ~60 roster names) and to 2020-2023 (annual reports exist for those years only). 2024-2026 under-sampled.
3. Papers by students/postdocs without a faculty co-author are almost absent (only 2 arXiv items).
4. Annual-report lists are partly sampled per person with small caps but are not sampled evenly in all cases (several people had only 1-5 eligible entries).
5. DOI coverage is low (35%) because CVs seldom print DOIs; no DOI lookups were made.
6. Hindi-language annual report not used.
