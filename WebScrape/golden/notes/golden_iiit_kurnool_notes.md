# Golden set IIITDM Kurnool (iiit_kurnool), lab notebook (operator Arihant Tripathy, 2026-10-29)

Output: `golden/golden_iiit_kurnool.csv`, 44 papers (target 150 NOT reached; see "Why short"). Raw data and code: `C:\Users\Arihant\rm_work\iiit_kurnool_golden\{data,code}`. No forbidden source was used; DOIs are only those printed on the source page.

## Sources and yield
| Source | Pages visited | Papers kept | Note |
|---|---|---|---|
| Faculty profile pages `iiitk.ac.in/<Dr.-Name>/page` (45 pages, all roster profile links) | 45 | 29 (Sastry 8, Eswaramoorthy 5 + 2 conference, Akhtar Khan 6, Sathya Babu 4, plus 4 overlapping rows kept once) | Only Sastry and Eswaramoorthy pages separate "before joining" from "after joining IIITDM-K" lists; most other pages list papers up to or before the joining year. |
| Institute list `Research-Publications/page` (journals, conferences, book chapters, 2019-2022 only, ~45 entries) | 1 | 13 | Page is frozen at 2022; most entries fail the tenure rule (joining year = paper year). |
| arXiv PDFs found by general web search (12 candidates fetched, abs/PDF only, no `/search`, no 403) | 12 | 6 | Affiliation printed in the PDF. Rejected: 2407.05440, 2408.04940, 2505.18019, 2506.17911, 1908.10674 (no Kurnool affiliation in text), 2609.06690 (Kancheepuram). |
| Press releases, newsletter, patents, four research-scholar pages, research-projects page, placement brochure PDF, Deccan Chronicle PCB patent story | 10 | 0 | Contain no paper lists (scholars pages are name lists; patents are patents; news item is a patent). |
| Annual reports | 0 | 0 | None with publication lists found (NAAC/AICTE/NIRF pages are links to count-only PDFs; not pursued). |
| News (external) | 1 | 0 | No external coverage of a specific paper. |

Source mix achieved: faculty pages 25 rows (57 %), dept/institute page 13 (30 %), arXiv 6 (14 %), annual report 0, news 0. Annual-report and news shares were moved to faculty/institute pages as instructed.

## Search strings (web search tool)
`arxiv "IIITDM Kurnool" Department of Computer Science and Engineering`; `"Indian Institute of Information Technology Design and Manufacturing Kurnool" arXiv paper` (both restricted to arxiv.org); `"IIITDM Kurnool" arxiv electronics communication engineering OR mechanical OR deep learning`; `"IIITDM Kurnool, Andhra Pradesh" arXiv preprint authors`; `IIITDM Kurnool researchers publish paper news`; three name-based queries (Murali/Katta/Amaranatha Reddy; Sathya Babu/Srinivas Naik/Naresh Babu; Nagaraju/Chakraborty/Anil Kumar/Kabaleeshwaran). The search tool returns few paper pages for this institute; the last three returned no usable paper.

## Tenure handling
Joining years come from the roster (`rosters/iiit_kurnool_faculty.csv`, an institute-web product); Akhtar Khan's own page gives July 2018 and Sathya Babu's gives leaving NIT Rourkela Sep 2021. A paper counts only if its year is strictly after the joining year, except the 6 arXiv rows where the printed affiliation (rule a, `high`) is the evidence. All other rows are `medium`. Faculty-page "after joining" sections are the person's own statement, not affiliation on the paper, so they are kept `medium`.

## Rejected candidates
* Papers in the joining year without visible affiliation: Sastry 2020 list (Wire-EDM Metals; broaching; trepanning DSS 2507), Murali D 2019 RSC Advances and J. Mater. Chem. A, Asan Basiri 2019 (Microprocessors and Microsystems; VDAT 2019 x2), Bhogilla 2019 (Int. J. Hydrogen Energy), Srilakshmi 2019 (IJAERD; ICMPT; NMIT), Singha 2019 (IEEE Access), Somayajulu 2019 (Applied Intelligence; ICCCNT), Shounak Chakraborty 2020 (soft-computing conference, award at IIT Indore; before 2021 joining).
* Authors not in the roster, tenure unknown: Satya Kamal Chirauri (WIREs, J. Alloys Compd, J. Mater. Sci. Mater. Electron., ACEL device conference, Nova book chapter), appear on the institute list but no tenure evidence.
* Faculty pages whose lists end at or before the joining year (so nothing could be kept): Kuila, Halder, Chandra Mohan D, Anil Kumar R, Majumdar, Krishna Naik (project lists only), Nagaraju, Kishore, Pandiyarajan, Vipindas, Rohit Das, Visweswara Reddy (2023 entries are visiting-faculty management papers, outside tenure evidence), Naresh Babu, Srinivas Naik, Rangababu, others with no or too short lists. Newly joined 2025-2026 faculty (Kuila, Halder, Rai, Rabani, Hazarika, Manoj Kumar, Yeduri, Joy Mukherjee) have pre-joining lists only.
* Sathya Babu items dated 2021 (equal to joining year).

## Coverage (rows by unit x year)
| Unit | 2016 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 | total |
|---|---|---|---|---|---|---|---|---|---|---|
| Mechanical Engineering | | 1 | 5 | 2 | 1 | 2 | 2 | 2 | | 15 |
| Electronics and Communication Engineering | | | 2 | 5 | 3 | 4 | 1 | | | 15 |
| Computer Science and Engineering | 1 | | 2 | 1 | 5 | | | | | 9 |
| Department of Sciences | | | | 2 | | | 1 | 1 | | 4 |
| Not stated (student arXiv) | | | | | | | | | 1 | 1 |
Exact totals per year: 2016 1, 2019 1, 2020 9, 2021 10, 2022 9, 2023 6, 2024 4, 2025 3, 2026 1. Years 2017, 2018 are empty (no tenure-verified paper; the permanent campus works from July 2018 and the earlier faculty are a known roster gap). 2023-2026 are thin because recent faculty pages list pre-joining work and the institute list stops in 2022.

## Why short
(1) The institute has about 60 current faculty, most joined 2021-2026, and their pages mostly list work from before they joined; (2) the institute's own publication list is a ~45-entry page frozen at 2022; (3) IRINS/Scopus-style listings are forbidden and no annual report with publication lists or news coverage exists; (4) general web search returns almost no paper-level pages for this institute. Time was not the limit; the accessible independent sources were exhausted.

## Biases
Heavy weight on two faculty (Sastry, Eswaramoorthy, whose pages carry post-joining lists) and on the Mechanical and ECE units; CSE 2023-2026 is nearly empty although CSE is the largest unit. Strict tenure rule excludes joining-year papers. Chapter/conference items skew to 2020-2022. DOI coverage 18/44 (41 %): journal entries on faculty pages usually print DOIs, institute list entries do not. Venues taken as printed (conference names abbreviated in a few rows). The 2016 Renjith arXiv row relies on the latest PDF version printing the Kurnool affiliation. Om Chiddarwar row: department not printed.
