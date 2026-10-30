# IIIT Manipur golden set: lab notebook

Operator: Arihant Tripathy (IIIT team). Run date 2026-10-30. Output golden/golden_iiit_manipur.csv (49 rows, target was 100, NOT reached). Work data in C:/Users/Arihant/rm_work/iiit_manipur_golden/data/, code in .../code/.

## Why only 49
Sources were exhausted, not skipped. (1) 28 of 49 roster faculty joined 2023-2025, and the tenure rule (year strictly after joining, or affiliation visible on the paper) removes nearly every paper on their pages (they list pre-joining work). (2) Only 3 annual reports exist (AR16-17, 17-18, 18-19); the links for 2019-20 to 2022-23 return 404 on the live site. (3) The institute site has no publications page or lab pages (R&D pages /pages/center/rnd/projects.php and texmin.php hold no papers; rnd.php and research_board.php 404). (4) The IRINS portal (iiitmanipur.irins.org) is forbidden and was not used. (5) Web search returned almost no author-affiliation text for IIIT Manipur outside arXiv.

## Sources and yield (found / used)
* Live faculty profiles (cached by roster agent, 19 pages: iiitmanipur.ac.in/pages/FACULTY%20PROFILE/*.html): about 150 list items read; 15 rows used (Saharia 3, Motilal 7, Kamalesh 2, Monica Devi 1, Sanjib Choudhury 1 live + 1 shared with AR, plus rows counted under old pages). Most others rejected by tenure (below).
* Wayback copies of old per-person pages (web.archive.org snapshots of Dec 2019 / Sep 2019 of *_FAC.html: Navanath, Kishorjit, Murli, Bhargab, Sarbajit used; Kabita, Nagesh, Ramesh, Subasit, Gaurav had no usable 2016+ papers; Doren_FAC and Kishor_FAC 404 in Wayback). Cached Prerna and Himangshu pages also read. 12 rows (faculty_page).
* Annual reports (AR16-17, AR17-18, AR18-19 PDFs, text via roster cache): 3 highlighted-publication lists, 11+13+11 = about 35 entries; 17 rows used, rest duplicates of faculty pages or not papers (talks/workshops) or 2015. Report listings alone are medium by rule.
* arXiv (abs/PDF via polite fetcher only; arXiv never answered 403): 9 PDFs opened, 6 kept (high, affiliation in PDF). Rejected: 2508.06870 (NIT Manipur), 2410.20064 (Rajiv Gandhi Univ), 2410.21192 (IIT Delhi/IIIT Delhi), 2506.03606 (IIT Guwahati), 2301.09849 and 2312.12011 (Saikia, Ahmedabad University affiliation).
* Other pages opened: mindailab.github.io (NIT Manipur lab, not IIIT), sunitawarjri.github.io (no paper list), manjilsaikia.in and /research (used only to find arXiv IDs and tenure Dec 2022-May 2023), journal.waocp.org colon-polyp paper (no IIIT Manipur affiliation seen).
* News: institute home page carries banners only; no paper-level news found. News share (target 10%) = 0.
* Dept pages (academicCSE/ECE/HBS): no publication lists. dept_page share = 0.

Source mix achieved: faculty_page 27 (55%), annual_report 17 (34%), arxiv 6 (12%), dept_page 0, news 0, websearch 0. Deviation due to unavailability, as the brief allows. Confidence: high 6, medium 43. DOI on source: 8 of 49 (16%).

## Web search strings used (about 14)
arxiv "Indian Institute of Information Technology Senapati, Manipur" OR "IIIT Manipur"; "IIIT Senapati" Navanath Saharia arxiv Manipuri; "Indian Institute of Information Technology Senapati" Manipur paper 2024/2025/2023 journal; arxiv "IIIT Senapati" OR "IIIT Manipur" Imphal ECE OR Humanities; Manjil Saikia OR Kaushal Bhardwaj OR Dennis Singh OR Jennil Thiyam OR Kabita Thaoroijam IIIT Manipur arxiv; "Indian Institute of Information Technology Senapati" Springer OR IEEE OR Elsevier; "IIIT Manipur" aclanthology Saharia OR Kishorjit OR Thaoroijam OR Warjri; Saharia "Indian Institute of Information Technology Senapati" tweets OR euphemism; "IIIT Manipur" pmc OR nature OR mdpi; Subasit Borah OR Murli Manohar OR Ramesh Mishra OR Nagesh Ch IIIT Manipur; Khoirom Motilal Singh OR Kishorjit OR Sunita Warjri full text; Sarbajit Singh OR Sanjib Choudhury OR Bhargab Deka OR Gaurav Saxena; Kaushal Bhardwaj OR Dennis Singh OR Prerna Mohit OR Himangshu Sarma OR Gaurav Saxena arxiv; Department of CSE IIIT Manipur arxiv abs; IIIT Manipur math/physics/electronics preprint; arxiv 2020/2021/2022 IIIT Manipur deep learning OR antenna OR speech OR cryptography.

## Departments x years (rows)
| Unit | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Computer Science and Engineering | 0 | 4 | 7 | 2 | 0 | 1 | 0 | 1 | 3 | 3 | 6 |
| Electronics and Communication Engineering | 1 | 3 | 3 | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 0 |
| Humanities and Basic Sciences | 5 | 1 | 2 | 0 | 0 | 0 | 0 | 2 | 0 | 1 | 2 |

Gaps: 2020 and 2022 have no rows; 2021 has one. ECE is almost absent after 2019. Faculty per unit: CSE 6 first-named IIIT authors (Saharia, Kishorjit, Motilal, Salam Michael Singh, Kabita, Ethari/Bhardwaj students), ECE 4 (Murli, Borah, Saxena, Monica Devi), HBS 5 (Deka, Sarbajit, Sanjib, Kamalesh, Saikia). Cap of 8 per person never reached (Saharia 8 and Kishorjit 8).

## Rejected / not used
* Tenure rule: Pothan (2025 chapter, joined 2025), Anup Dey, Dilip Singh, Partha Deb, Prabhat Singh, Somaraju Boda, Neelamegam, Sumit Rano (2025 papers equal to joining year, rest earlier), Sunita Warjri (joined 2025), Rahul Lahkar (Oct 2025), Teressa Longjam (Sept 2025), Pradipkanti Devi (2023 paper equals joining year 2023), Inunganbi (2024 review equals joining year 2024), Bidyalakshmi (2020-21 only), Ramesh Mishra (joined June 2017; page papers 2016-17), Himangshu Sarma (joined July 2019; papers 2017-18 on page; the 2018 conference papers kept under Saharia as first IIIT author), Prerna Mohit (joined Aug 2018; papers 2016-17), Kabita Thaoroijam page (no 2016+ papers).
* Motilal 2023 papers (4) excluded: equal to joining year 2023, no affiliation visible.
* Saharia 2016 conference papers (COMM-2016, I3CS-2016) and Kishorjit ICON 2016: joining year 2016, affiliation not visible.
* 2015 items (Borah AEMC 2015, Sarbajit HLS21 Nov 2015) are outside 2016-2026. Saharia/Doren Reg-ICON 2017 Tangkhul paper dropped to respect the 8-per-person cap. Non-paper items (workshop talks, Kishorjit book, patents, reviewer roles) dropped.
* People with no profile page or no joining year (Kaushal Bhardwaj, Dennis Singh, Jennil Thiyam, Michael Singh, Heigrujam Manas Singh etc.) have no source with their papers; Dennis Singh's lab is at NIT Manipur (homonym/affiliation risk).
* Nagesh Ch, Kabita, Ramesh, Subasit, Gaurav old pages: no 2016+ publication entries.

## Biases
* 33% of rows rest on annual-report listings (self-selected "highlighted" papers, 2016-2019 only) and 55% on faculty pages; all but 6 are medium (tenure inferred, affiliation not seen on the paper).
* Heavy skew to 2016-2019 (old pages and ARs) and 2024-2026 (new joiners and 2026 arXiv); 2020-2022 are nearly empty because ARs after 2018-19 are unavailable.
* Joining years for Borah, Murli and Sarbajit are upper bounds from the first (2015-12-14) snapshot / old pages "Joined on".
* arXiv rows are CSE/HBS only; ECE and physics work is under-sampled. Student-led papers (3) are the only non-faculty-led rows.
* Search tool could not query by affiliation string, so papers that only appear on publisher pages are missed; the pipeline's recall measured against this set is therefore an upper bound on true recall for these years.
