# Golden set: IIT Dharwad (iit_dharwad), 2016-2026, lab notebook

Built on 2026-10-26 by an independent sub-agent. No bibliographic API was used for discovery: no Crossref, OpenAlex, Semantic Scholar, Europe PMC, DOAJ, ORCID, DBLP, Google Scholar, Scopus, IRINS, DataCite or the arXiv API. Faculty links that point to Google Scholar, ORCID, INSPIRE, ResearchGate or LinkedIn were not followed. `www.iitdh.ac.in/all-publications` (source "Scopus") and `iitdh.irins.org` were not used.
`WebScrape/iit_dharwad.json` and the other pipeline outputs were not read. Every URL went through the shared fetcher `scratchpad/tools/polite_get.py`: 376 logged calls in `work/iit_dharwad_golden/data/fetch.log`, plus the arXiv PDFs fetched by `code/arx.sh`, which logs to `data/arx.out`. All arXiv requests returned 200 and ARXIV_BLOCKED was never raised. On top of the fetcher's 5 s gap, an extra 10 s sleep was added between arXiv requests, which honours robots.txt's 15 s. Downloads are in `work/iit_dharwad_golden/data/` and scripts are in `work/iit_dharwad_golden/code/`.

**Result:** 297 distinct papers in `golden/golden_iit_dharwad.csv`. The target was 300; see "Shortfall" below.

| evidence_source | rows | share | confidence | rows with DOI |
|---|---|---|---|---|
| faculty_page (personal homepages linked from the institute profile) | 167 | 56 % | all medium | 26 |
| annual_report (2017-18 to 2024-25) | 58 | 20 % | all medium | 40 |
| dept_page (Physics and BSBE department pages + 9 lab sites) | 35 | 12 % | all medium | 18 |
| arxiv (affiliation checked in the PDF) | 25 | 8 % | all high | 1 |
| news (institute news, Research Updates page, SAMBANDH newsletters) | 12 | 4 % | all high | 0 |
| **total** | **297** | | 260 medium / 37 high | 85 (28.6 %) |

Types: journal 185, conference 65, preprint 33, book-chapter 13, book 1.
Years: 2018: 2, 2019: 17, 2020: 19, 2021: 16, 2022: 26, 2023: 35, 2024: 72, 2025: 64, 2026: 46. There are no rows for 2016 or 2017 (see biases).
Students, postdocs or staff lead about 20 rows: arXiv preprints by students and postdocs, newsletter and news items, a postdoc in the 2024-25 annual report, and a technical superintendent. 10 rows come from people who are no longer regular faculty: S R M Prasanna (8 rows, IIT Dharwad Jul 2017 to Apr 2024, now on lien to IIIT Dharwad), former faculty Prabuchandran K J (1) and honorary adjunct D. Narasimha (1).

## Departments x years coverage
| Department | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 | total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Biosciences and Bioengineering |  |  |  | 3 | 1 | 1 | 1 | 3 | 6 | 4 | 3 | 22 |
| Chemical Engineering |  |  |  |  |  |  |  | 1 | 3 | 6 | 8 | 18 |
| Chemistry |  |  |  |  |  | 1 |  | 4 | 4 | 5 | 8 | 22 |
| Civil & Infrastructure Engineering |  |  |  |  |  |  | 1 | 1 | 7 | 4 | 1 | 14 |
| Computer Science and Engineering |  |  | 1 | 3 | 3 | 3 | 3 | 6 | 6 | 12 | 4 | 41 |
| Electrical, Electronics and Communication Engineering |  |  |  | 5 | 6 | 4 | 13 | 10 | 21 | 15 | 8 | 82 |
| Humanities, Economics, Arts and Rural Technologies |  |  |  | 1 | 2 |  | 4 | 3 |  | 2 | 2 | 14 |
| Mathematics |  |  |  |  | 2 | 4 | 1 | 5 | 7 | 4 | 5 | 28 |
| Mechanical, Materials and Aerospace Engineering |  |  | 1 | 4 | 3 | 2 | 2 | 1 | 13 | 6 | 4 | 36 |
| Physics |  |  |  | 1 | 2 |  | 1 | 1 | 4 | 5 | 3 | 17 |
| Not stated (student authors) |  |  |  |  |  | 1 |  |  | 1 | 1 |  | 3 |

All 10 academic units are covered. The 3 "Not stated" rows are arXiv papers whose IIT Dharwad author is a student with no department printed.

## 0. Roster and tenure
* Roster: `https://www.iitdh.ac.in/faculty` is one Drupal page with 131 cards: 107 professors of any rank, plus visiting and adjunct staff, research associates and fellows. Former faculty come from `https://iitdh.ac.in/former-faculty` (34 names).
* All 125 institute profile pages (`/node/N`) were fetched. They hold no publication lists, only research areas and a "Personal page" link.
* Of the 88 non-blocked personal links, all were fetched, and so were 59 publication subpages.
* Joining year J was taken, in order of preference:
  1. from the person's own page, for example "since Dec 2018", "Jul 2017 - Feb 2024", or "Before joining IIT Dharwad" sections;
  2. otherwise from the first Wayback snapshot of the institute faculty list that shows the person. 15 snapshots were used: `faculty.php` 2017-02 and 2017-09, `faculty_dept.php` 2018-06 to 2023-09, `/faculty` 2024-06 to 2026-01.
* The 2017 snapshots list only IIT Bombay mentor faculty. So "first seen 2018-06" is an upper bound for the 2017 joiners.
* NIRF was not needed.
* Rule applied: year > J, or year = J only when the affiliation is visible on the paper (one case: arXiv 1803.03358, Sandeep, 2018).
* Two personal pages split their list explicitly, with "From IIT Dharwad" or "Before joining IIT Dharwad" (Rajeswara Rao, Supriya Rej; also Shukla's and Mehto's lab sites). Those splits were used, and they override the tenure rule where the two disagree.

## 1. Faculty pages, source "faculty_page"
* Page types: Google Sites, GitHub pages, `iitdh.ac.in/~user` pages and Wix. Lists come in several forms: year-grouped, numbered [J#]/[C#], BibTeX blocks, or free text.
* 42 faculty were used, across 9 departments. BSBE faculty publish only through lab sites, which are counted as dept_page.
  * Up to 5 in-tenure entries were taken per person, evenly spaced through each list (offsets round(i*N/k), lists newest-first).
  * Entries were skipped only for duplicates, missing year, or a year outside the range.
  * A few people have fewer than 5 because their lists hold fewer in-tenure items.
  * Two people (Satish Naik, Sairam) were added late to approach 300.
* People sampled, by department:
  * EECE: Mulla, Bharath, Kadayinti, R V Bhat, Ruma Ghosh, Mondal, Prasanna, Vigneshwara Raja, Animesh Sahoo, Kamath, Satish Naik, Sairam.
  * CSE: Sandeep, Rajshekar K, Phawade, Tripathi, Tamal Das, Swain.
  * HEART: Chakravarty, Parashari, Jolly Thomas.
  * MMAE: Keerthi, Rakesh Lingam, Dhiraj Patil, Sudheer, Sethi, Anbukkarasi, Bembalge.
  * CIE: Hegde, Bande, Nayaka.
  * Chemistry: Rajeswara Rao, Gudem, Rej.
  * ChemE: Dutta.
  * Maths: Sen, Dolai, Srivastava, Veekesh Kumar.
* Pages looked at but given 0 rows, with the reason:
  * Meenatchidevi (list stops at 2020, joined Dec 2020).
  * Vyom Sharma (nothing after joining in 2023).
  * Kundan Singh (joined 02/2024; the 2024 items are US work).
  * Anmol Kumar (not on any faculty list snapshot; all papers are from Maryland).
  * Jayakumar K V (NIT Warangal papers; joined 2024).
  * Kataware and Raut (home pages without a usable dated list).
  * Ridhima Tewari (her page needs a Google sign-in; not bypassed).
  * Gayathri (publication page is rendered by JavaScript).
  * Mahanta (home page last updated 2022, no list).
  * Kavita Devi's lab list (stops at 2019, before her Dec 2019 joining).
  * Dubey (first seen 2026-01; nothing strictly after joining).
  * Santosh Kumar's personal page (used through the Physics department page instead).
* Rejected entries were mainly outside tenure; the largest losses were Hegde, Shukla, Rej, Gudem and Sethi. One Tamal Das entry dated 2027 was out of range.

## 2. Department and lab pages, source "dept_page"
* Department sites:
  * `physics.iitdh.ac.in/publications` (Google Sites, 41 entries): 10 points evenly spaced (every 4th entry). 10 rows. Point 37 (Mandar Patil, PRD 2020) was skipped because his tenure is unclear: he appears on faculty lists 2018-12 to 2019-07 only.
  * `bsbe.iitdh.ac.in/research/publications`: 160 merged entries going back to 2008. 8 points were tried and 5 rows taken. Points 101, 121 and 141 had no in-tenure entry: all 2018 or earlier, before the authors joined.
  * `cse.iitdh.ac.in`, `ee.iitdh.ac.in` and `maths.iitdh.ac.in` are JavaScript single-page apps with empty HTML and could not be read. `mmae.iitdh.ac.in` and the Chemistry, CIE and HEART institute pages have no publication lists.
* Lab sites (all linked from faculty profiles), with rows taken:
  * Cancer Biology Lab (Shukla): 5
  * IVM Lab (Chaube): 3
  * Immunobiology Lab (Mehto): 3
  * Swanand Lab (Marathe): 1
  * Colloids and Nanomaterials Lab (Ravikumar): 3
  * MFM Lab (Sontti): 4
  * CEES Lab (Ummireddi): 1
  * thinpvlab.in (D S Ghosh): renders by JavaScript, so it was not used; Ghosh comes through the Physics page.

## 3. Annual reports, source "annual_report"
* Index: `https://www.iitdh.ac.in/iit-dharwad` lists the 2016-17 to 2024-25 reports. The 2019-20 PDF came from the www host; the beta2 host returned 502.
* 2016-17: no publication list.
* 2017-18: 4 entries, all rejected. 3 are from the joining year 2017/2018. The fourth, Rajeswara Rao JOC 2018, appears on his own page under "Before joining IIT Dharwad".
* 2018-19: 36 entries, 7 points, 7 rows.
* 2019-20: 56 entries, 7 points, 7 rows.
* 2020-21, 2021-22 and 2022-23 are image-only PDFs: CorelDRAW output, and `pdftotext` gives no text. Pages were rendered with `pdftoppm` and read visually. No OCR tool was installed.
  * 2020-21: 62 entries on pp. 41-44, 6 points, 6 rows.
  * 2021-22: one point at the top of each of pp. 53-59, 6 rows.
  * 2022-23: one point on every second page of pp. 49-59, 6 rows, minus 1 removed for the per-person cap.
* 2023-24 (221 entries) and 2024-25 (166 entries) were parsed with `code/arparse.py`. Each got 16 points in two passes (8 plus 8 at half-step offsets). This gave 14 and 13 rows; one more 2023-24 row was removed for the cap.
* These two reports print DOIs in APA style, and those DOIs were recorded as printed. Their lists look machine-generated, but they are institute reports, so they were allowed.
* Every annual-report row is medium confidence and had to pass the tenure rule, as the brief requires. Typical rejections were joining-year papers, unidentifiable authors ("Mahanta N." in a Tezpur-style author list; S. Basavarajappa), and people at the cap.

## 4. arXiv PDFs, source "arxiv"
* robots.txt disallows `/search`, so discovery used web search restricted to arxiv.org, plus arXiv ids linked from faculty pages (Bharath, Kadayinti) and from the 2018-19 annual report (Sandeep).
* Search strings:
  * `"Indian Institute of Technology Dharwad" arxiv`
  * `"IIT Dharwad" arxiv.org preprint`
  * `Dharwad 580011 Karnataka arxiv`
  * `"Indian Institute of Technology Dharwad" "Department of Physics" OR "Department of Mathematics" arxiv 2019 2020 2021`
  * `"Indian Institute of Technology Dharwad" "Computer Science" OR "Electrical Engineering" arxiv 2018 2019 2020 2022`
  * `"Indian Institute of Technology Dharwad" arXiv 2018 2019 graph OR quantum OR speech OR caching`
  * `"IIT Dharwad" "Dharwad, India" arxiv abs 2020 2021 2022`
  * `"Indian Institute of Technology Dharwad" arXiv 2017 OR 2018 OR 2019 pdf`
  * `"IIT Dharwad" arxiv physics OR chemistry OR mechanical 2020 2021 2022 2023`
* 37 PDFs were fetched, all 200. The affiliation was checked in the PDF text: the first 2 pages, or the full text when needed. 25 rows were accepted. Year = the v1 year from the identifier.
* Rejected:
  * 2205.15563 and 2601.03194: IIIT Dharwad, not IIT.
  * 2401.01319 and 2404.02724: IIT Ropar and IIT Roorkee theses.
  * 2510.16236: IIT Guwahati.
  * 2306.00821: IIT Dharwad given only as a "present address".
  * 1701.02560: PESIT affiliation.
  * 2309.07529, 2511.14448, 2512.11337 and 2509.14599: versions of papers already in the set.
  * 2302.13209, 2508.01034 and 2610.03227: per-person cap of 8 reached (Prasanna, Sen).
  * 1409.7195: v1 is from 2014.
* Students, postdocs and staff lead several of these rows: Agarwal, Deshpande, Taruni, Roy, Ravuru, Prince, Mukherjee, Ayush Agarwal, Kamath.

## 5. News and web, source "news"
* `iitdh.ac.in/research-updates`: the page shows about 16 items and has no pager. `iitdh.ac.in/news` plus `?page=1..8` gave 135 items.
* News titles were filtered with `publish|journal|paper|article|cover|accepted|research work`. 13 items were opened. Two SAMBANDH newsletters were also read: Jan 2026 and Apr 2026, found by web search on iitdh.ac.in.
* 12 rows. Items were rejected when they gave no title (the Ghosh JAP Editor's Pick item), no year (Ramjee Repaka's JTAC paper, Ridhima Tewari's South Asian Diaspora essay, Punekar's ENZYMES 2nd edition), or were duplicates (Gudem's JPCA cover, Sethi, Sontti, Ravikumar x2, Mulla). The alumni paper (VIT-AP) is not IIT Dharwad work.
* Shikha Kumari's TCAD paper was dropped because of the per-person cap (Vigneshwara Raja).
* Where the news item gives no year, the year was taken from the faculty's own page, and that is noted in the row. DOIs that appear only on other pages were not recorded for news rows.
* News pages carry no dates.
* External press web search (`IIT Dharwad researchers study published journal`) returned only institute pages. So there is no `websearch` row, and the news share is below the brief's 10 %.

## Shortfall and source-mix deviations
* 297 rows instead of 300. The arXiv share is 8 % instead of 10 % and news is 4 % instead of 10 %. The cause is a scarce supply of in-tenure items with an affiliation and a title, combined with the cap of 8. The faculty-page share (56 %) and annual-report share (20 %) were raised to compensate.
* Per-person cap of 8: 8 people are at the cap: R V Bhat, Prasanna, D V Patil, Rajeswara Rao, Sen, Shukla, Vigneshwara Raja and Satish Naik. Two rows were removed after merging to enforce it.

## Known biases
* **No 2016-2017 rows.**
  * The institute started in 2016 with mentor faculty from IIT Bombay. Its own faculty joined from late 2017.
  * Under the strict year > J rule, papers from the joining year need visible affiliation, and the 2016-17 and 2017-18 reports contribute nothing.
  * 2018 has only 2 rows.
  * The set is strongly recent: 61 % of rows are from 2024-2026. Part of this is real growth (the 2024-25 report lists about 260 publications). Part is page bias, since personal pages favour recent work and recent joiners.
* **Upper-bound tenure:** for about half the faculty, J is the first Wayback snapshot (2018-06, 2019-07, 2020-09, ...). Snapshots are sparse, with gaps of up to 14 months. This is conservative for acceptance, but it can admit papers written elsewhere soon after joining. Several such papers are visible, for example IIT Patna, Alberta, Yale and IIT Guwahati student work by Hegde, Sontti, Chaube and Prasanna; they are kept as medium per the brief's rule.
* **Survivorship:** faculty and lab pages exist only for current faculty. Former faculty (Prabuchandran, Mandar Patil, Narasimha; Prasanna is on lien) appear only through the reports and arXiv.
* **Department mix:** EECE is the largest unit with usable pages (82 rows, 28 %). CIE (14), HEART (14) and Physics (17) are thinner: CIE pages often lack years, Ridhima Tewari's page is locked, and Physics faculty pages are thin. CSE, EE and Maths department sites are JavaScript apps and could not be read.
* **DOI coverage:** DOIs come mainly from the 2023-24 and 2024-25 report lists, which print DOIs, and from a few pages (Hegde, Rej, Vigneshwara, Satish Naik, Sontti). 141 of 167 faculty_page rows have no DOI. DOI coverage is therefore source-driven, not quality-driven.
* **Affiliation:** 260 of 297 rows are medium (tenure-based). The faculty pages and reports demonstrably include pre-joining work; it was excluded where it was visible.
* **Title variants:** some arXiv preprints and conference versions may match journal rows only through title variants (for example Veekesh Kumar's arXiv 2512.11337 against Forum Math 2026). Matching should allow fuzzy titles.
