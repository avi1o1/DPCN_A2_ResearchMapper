# Golden set: IIT Jodhpur (iit_jodhpur), 2016-2026, lab notebook

Built 2026-10-26/27 by two successive independent sub-agents (the first was stopped for a model change, the second finished). No bibliographic API was used for discovery (no Crossref, OpenAlex, Semantic Scholar, Europe PMC, DOAJ, ORCID, DBLP, Google Scholar, Scopus, IRINS, DataCite, arXiv API). `WebScrape/iit_jodhpur.json` and other pipeline output were not read. All URLs went through `scratchpad/tools/polite_get.py` (log `work/iit_jodhpur_golden/data/fetch.log`, scripts in `.../code/`, final assembly `code/build.py`).

**Result: 126 distinct papers (target 450 NOT reached; see Shortfall).**

| evidence_source | rows | confidence | with DOI |
|---|---|---|---|
| arxiv (PDF affiliation read) | 61 | all high | 0 (none recorded) |
| annual_report (IITJ annual reports 2016-17 .. 2022-23) | 62 | all medium | 45 |
| news | 3 | all high | 1 |
| faculty_page / dept_page | 0 | | |
| **total** | **126** | 64 high / 62 medium | **47 (37 %)** |

Years: 2016: 7, 2017: 17, 2018: 16, 2019: 14, 2020: 11, 2021: 8, 2022: 4, 2023: 17, 2024: 11, 2025: 8, 2026: 13. Types: preprint 66 (incl. 4 arXiv items listed in annual reports), journal 37, conference 18, book-chapter 4, book 1. Per-person cap 8 respected (max: Vatsa and Singh at 8 each, counting co-authored rows for each).

## Sources and access
* **Live institute site is unreachable** (`iitj.ac.in`, `www.iitj.ac.in`: SSLError). Everything from iitj.ac.in comes from Wayback copies (3 s gap; no bot challenge met).
* **IITJ profile pages** (`/People/Profile/<uuid>`, 262 roster entries from the 17 Wayback department list pages; 11 profiles fetched) carry no publication list (only bio / "Web Profile"), so they yield no faculty_page rows; they were used only for roster names. **Department "Journal Publications" pages** (e.g. civil-and-infrastructure-engineering/en/journal-publications, Wayback) are empty shells (content is an external portal). `research.iitj.ac.in` (connection error) and `scholar.iitj.ac.in` (request hung, killed) could not be read; the former looks IRINS-style and was not pursued. The institute repository page lists only senate minutes, newsletters, annual reports, brochures. Therefore **no faculty-page share** and almost no dept/lab share (one lab page, iab-rubric.org/publications, was fetched; its 2 candidate rows were dropped because Vatsa and Singh were already at the cap of 8).
* **Annual reports** (Wayback of iitj.ac.in/PageImages/Gallery/...): FY2014-15 .. 2024-25 PDFs fetched and converted with pdftotext (2020-21 and the FY2023-24 research-publications PDF returned error pages; 2023-24 and 2024-25 reports contain only counts, no lists). APA-style department lists were parsed for 2016-17..2019-20 (833 entries: 122/182/209/320 plus unparsed); 2021-22 and 2022-23 lists have mangled column order, so the 18 hand-checked entries by the first agent (`data/ar_rows.tsv`) were used for those two years (10 kept after tenure check).
* **arXiv**: search is disallowed by robots.txt; 71 PDFs located through web search restricted to arxiv.org were fetched (5 s fetcher gap, no 403), first-page text read with pdftotext. The affiliation (IIT Jodhpur) is printed in each kept PDF. Rejected: 1906.00063, 2003.02488, 2606.24269 (no Jodhpur on pages 1-2), 2106.04960 (IIT Bombay), 2604.27698 (no IITJ author); dropped for the per-person cap: 2001.07444, 2002.02942, 2610.11356 (Vatsa/Singh), 2403.04813, 2411.18687, 2501.15148, 2412.14913 (Banerjee). Not fetched/not read: 2109.09759, 2205.01384, 2112.06522, 2207.02962, 2204.08149, 2112.04519, 2206.13938, 2112.04958 (candidates from search results).
* **News**: 29 candidate URLs; 10 fetched OK, 10+ PIB/bweducation/sustainable-carbon pages returned 403 (not bypassed). Articles rarely print paper titles, so only 3 rows could be built (title via general web search): CODE device (Sci Rep 2023), PLC/DCSK (IEEE OJCOMS 2023), DomainAdapt (MICCAI 2024; DOI printed on papers.miccai.org). Two further news items identified papers already in the set (Pattern Recognition COVID X-ray = arXiv 2008.03205; Nature Machine Intelligence = arXiv 2310.15848). Not usable for lack of a title: TiAl-CA alloy (Materials Horizons, Nene), SERS cytokine nanosensor, ZnO-caterpillar wastewater (Ankur Gupta), indoor-air/Prakriti items.
* Web search strings used: `"Indian Institute of Technology Jodhpur" arxiv` (+ department / year / topic variants, e.g. physics, mathematics, civil, bioscience, `"Jodhpur 342037"`, `"IIT Jodhpur" Alok neutrino`, `Subhashish Banerjee ... arXiv 2016`); `IIT Jodhpur researchers develop ... published journal` (2018-2025 variants); and title look-ups for the three news rows.

## Tenure rule
No roster was available (`rosters/iit_jodhpur_faculty.csv` absent). For annual-report rows the joining year is an upper bound = end year of the first IITJ annual report (FY2014-15 onward) whose text names the person (`code/firstar.py`); a paper counts only if its year is strictly greater. Roster names were matched to APA author strings by surname + first initial, unique matches only, and the department heading in the report had to agree with the roster department. Annual-report listings are medium (no affiliation on the entry). arXiv and news rows are high (affiliation visible). Rejected for tenure/data issues: Mukerji 2022 and Ranjan 2022 (first named in AR2021-22), people whose first report could not be determined (Chandramouli, Hiremath K R, Gandi, B. Singh in the 2021-23 lists), two 2019 entries whose volume numbers show 2014 (Pal: Magnetic Resonance in Chemistry 52; sperm biotin paper dropped alongside) and the duplicate Jha Cytokine paper.

## Departments x years
| Department | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 | total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Bioscience and Bioengineering |  | 1 | 2 | 1 |  | 1 |  |  |  |  |  | 5 |
| Chemistry | 1 | 2 | 2 | 2 | 1 | 1 | 2 | 2 |  | 1 |  | 14 |
| Civil and Infrastructure Engineering |  |  |  |  |  | 1 |  |  |  |  |  | 1 |
| Computer Science and Engineering | 2 |  | 2 |  | 4 | 2 | 2 | 3 | 2 | 2 | 6 | 25 |
| Electrical Engineering |  | 3 | 3 | 2 | 2 | 1 |  | 2 |  |  | 1 | 14 |
| Mathematics | 2 | 2 | 1 | 3 |  |  |  |  |  | 4 | 2 | 14 |
| Mechanical Engineering | 1 | 3 | 2 | 3 | 1 | 1 |  | 2 | 1 |  |  | 14 |
| Metallurgical and Materials Engineering |  |  |  | 1 |  |  |  |  | 1 |  |  | 2 |
| Physics | 1 | 5 | 4 | 1 | 3 | 1 |  | 9 | 6 | 1 | 2 | 33 |
| School of Liberal Arts (Humanities and Social Sciences) |  | 1 |  | 1 |  |  |  |  |  |  |  | 2 |
| Other units (AI and Data Science, Management, Interdisciplinary Research Division, QIC platform) |  |  |  |  |  |  |  |  | 1 |  | 3 | 4 |

(Chemical Engineering, School of Design, CETSD, Energy/Environment units: no rows.)

## Shortfall and known biases
* 126 of 450: no usable faculty-page or department publication lists (see above); news seldom names papers; 2020-21 and 2023-25 annual reports have no lists. No cell was filled artificially.
* Source mix is 49 % annual report, 48 % arXiv, 2 % news, vs the planned 50/15/15/10/10.
* **arXiv bias**: found by web search; heavily physics (Banerjee/Alok/Sinha/Ghosh groups), CSE (Vatsa/Singh) and mathematics; physical sciences/CS are overrepresented, life sciences, civil, chemical, design, liberal arts underrepresented; DOIs not recorded for arXiv rows. Years 2022 and 2020-21 are thin (annual reports for 2020-21 unavailable).
* **Annual reports 2016-20**: lists are by department, English-language APA entries; matching only to current faculty (roster is the 2026 Wayback list), so former faculty are absent; common surnames (Kumar, Singh, Sharma...) were excluded from matching.
* DOI coverage 37 % only because annual reports print DOIs (arXiv rows carry none); none was looked up.

---
## SUPPLEMENT (2026-10-28): faculty/lab pages and news; 126 -> 192 rows (+66; target 450 NOT reached)

Method: web search (strings such as "IIT Jodhpur chemical engineering faculty homepage publications list", "sites.google.com iitj.ac.in publications", "IIT Jodhpur researchers study published in journal 2024/2025", per-person name searches) to find lab/personal Google Sites; every page fetched via the shared polite fetcher and read as text (helper scripts in /tmp/sup, not in repo). Roster `homepage` column was empty for all 443 rows, so no roster-listed homepages were available. Per-person cap 8 respected; entries sampled spread across the post-tenure part of each (newest-first) list.

| source page | unit | rows | rule |
|---|---|---|---|
| ptadlab (S. M. Hasan; A. N. Gandi) | Materials Engineering | 8 | medium, year > 2021 (Hasan joined 2021) |
| raviprakash personal site | Civil and Infrastructure | 8 | medium, joined Mar 2021 (own page) |
| wact-lab (M. K. Jena) | Chemical Engineering | 4 | medium, joined Feb 2025, only 2026 papers |
| dr-krunal-m-gangawane | Chemical Engineering | 8 | medium, joined 2023 |
| ecsrlab (Shobhana Singh) | Energy and Automotive | 8 | medium, joined 2019 |
| sarkar-research-group (Suresh Sarkar) | Chemistry | 6 | medium, joined 2022 (several papers done at previous employer; tenure rule only) |
| tstmlab (Ranju Mohan) | Civil and Infrastructure | 7 | medium, joined 2020 |
| shahabahmad1 | Physics | 6 | medium, joined 2019 |
| ankurguptaiit (Ankur Gupta) | Mechanical | 8 | medium, joined 2019 |
| news (Nagaland Tribune, Free Press Journal, Careers360) | Civil, Materials, CSE | 3 | high (news names IITJ authors); titles from web-search hits on paper pages; no DOIs recorded |

New rows by unit: Chemical Engineering 12, Civil 16, Materials 9, Energy and Automotive 8, Mechanical 8, Chemistry 6, Physics 6, CSE 1. Years: 2021: 4, 2022: 7, 2023: 4, 2024: 15, 2025: 17, 2026: 19 (2016-2020 none: all new sources are post-2020 hires; 2024-2025 and 2021-2022 thinly improved). DOI printed on page for 16 of 66.

Rejected / unusable: Anurag Sharma ACMM lab (joined 2026 per own page; no post-tenure published papers); Sajan Pillai site (all papers pre-2016-2015, joined Dec 2024); Jena papers 2021-2025 (before/at his Feb 2025 joining; no affiliation on entries); Gangawane, Hasan, Ravi Prakash papers at or before joining year; Mukerji NAR 2022 news item (no title found); Bioscience, Design, CETSD/Environment, Aerospace: no accessible lab or personal publication pages found (search returns only research.iitj.ac.in, which is an IRINS-style portal and forbidden, and iitj.irins.org). home.iitj.ac.in (S. Ghosh CV) unreachable (SSLError). Dept pages: none with lists beyond the above. TechScape issues and FY2023-24 research-publications PDF: Wayback returns error pages.

Biases: all lab-page rows are `medium` (affiliation not on the entry) and lists on these pages are often Google-Scholar exports; sites exist mostly for recent hires, so 2016-2020 is not helped; chemistry/civil/materials/mechanical/physics overrepresented vs bioscience/design/liberal arts (no sites found). Source mix now: arXiv 32%, annual report 32%, dept_page 25%, faculty_page 8%, news 3%.

---
## SUPPLEMENT 2 (2026-10-28): annual-report re-mining with the new roster; 192 -> 486 rows (+294; target 450 reached)

Method (scripts in scratchpad `work/iit_jodhpur_golden/code2/`; no bibliographic APIs; fetches via polite_get):
* **AR FY2016-17..2019-20 (APA lists, saved `AR*.apa.jsonl` parsed from the PDFs)**: re-matched authors to the 443-row roster (`rosters/iit_jodhpur_faculty.csv`) by surname + first initial; common surnames allowed when the report department equals the roster department (the old matching excluded them and used the 262-name 2026 list). Joining year = roster `joining_year`, else first annual report naming the person (upper bound). Paper counts if year > joining year. 524 candidates / 58 people; 205 selected (even spacing in list order, per-person cap 8 across all rows). Years: 2016: 11, 2017: 43, 2018: 64, 2019: 52, 2020: 35. Units: Chemistry 43, Mechanical 39, Electrical 30, Bioscience 23 (first report-based Bioscience rows), CSE 22, Physics 20, Mathematics 19, Liberal Arts 7, Materials 2.
* **AR FY2021-22 and FY2022-23 ("too mangled")**: the saved `*.raw.txt` (pdftotext -raw) are readable: entries are intact though columns interleave and numbering is lost. Parsed by anchoring on "(YYYY)", reading authors before and title/venue after; only roster surname+initial pairs that are unique and not on a common-surname list were matched. 179 candidates, 110 selected, 86 kept after a sanity filter (spliced title/venue dropped, e.g. quoted-title Sahney entries, Kapoor, Balaraman). Mostly 2021-2022; schools (Management, Liberal Arts, Civil, Aerospace) now appear. Title/venue splitting is heuristic; a few venues may be truncated.
* **FY2023-24, FY2024-25 reports**: re-read in raw text: counts only, no lists. **FY2020-21 report**: Wayback CDX shows the PDF (`https://www.iitj.ac.in/PageImages/Gallery/03-2025/IITJ%20Annual%20Report_English_FY2020_21.pdf`, 20250612035618, 200) but the fetch with id_ did not complete and was killed; not mined, so 2020-21 stays thin.
* **Lab pages**: Vinod Vijay Kumar (TMSR, SME, joined 2023): 3 rows (2025, 2025, 2026 chapter; 2026 "under review" item skipped). Rajit Ranjan D2F (Mechanical, joined 2025): no later papers, 0 rows.
* Web search for Aerospace, Design and Bioscience lab/faculty publication pages returned only research.iitj.ac.in (IRINS-style, forbidden) or personal sites without lists. Design, CETSD, Environment: no rows; Aerospace 2 rows (from AR2223).

Departments after: Physics 73, Chemistry 68, Mechanical 67, Electrical 59, CSE 53, Mathematics 41, Bioscience 28, Civil 22, Materials 18, Chemical 15, Management 14, Liberal Arts 11, Energy and Automotive 8, Aerospace 2, others 6. Years: 2016: 18, 2017: 60, 2018: 80, 2019: 66, 2020: 46, 2021: 65, 2022: 40, 2023: 25, 2024: 26, 2025: 27, 2026: 33. DOI printed on 264 of 486 (broken line-wrapped DOIs left empty).

Biases: annual_report is 73% of rows (353/486) vs planned 15%, all medium (no affiliation on entries); 2023-2026 under-represented; unambiguous-name matching favours uncommon surnames (Singh/Kumar/Sharma etc. under-represented); roster joining years may be upper bounds; per-person usage vs earlier arXiv/news rows counted by surname+initial (approximate).
