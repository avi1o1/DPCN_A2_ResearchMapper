# Golden set notes: IIIT Ranchi (iiit_ranchi)

Operator: Arihant Tripathy (IIIT team). Built 2026-10-30. Output: golden/golden_iiit_ranchi.csv.

## Result
82 papers (target 100 not reached; see below). evidence_source: faculty_page 53, annual_report 27, websearch 2, dept_page 0, arxiv 0, news 0.
confidence: high 2, medium 80. DOI printed on source: 24 (29%). Types: {'journal': 49, 'conference': 29, 'book': 1, 'book-chapter': 3}.

## Why fewer than 100 and why the mix deviates
* Institute started 2016; most faculty joined 2018 or later and the many current faculty joined 2024-2025, so most profile-listed papers pre-date their joining and fail the tenure rule (strictly after joining year). Rejected on this ground: Jayadeep Pati's 2017-2018 profile papers (joined 2018; IIT BHU co-author), Priyabrat Garanayak, Puja Ghosh, Chandra Prakash Singh, Ankita Kumari, Kishore Babu (profile lists only pre-joining work), Syed Sadique Anwer Askari (all listed papers 2023 or earlier = joining year 2023, affiliation not shown), Dinesh Kotary, Rishikesh Tiwary, Ravi Shanker, Noopur, Nitika Nigam (no valid entries or no list), Bharat Singh's 2019 ICACSE paper (before 2021), Mahto's 2017 entries (joining year 2017).
* dept_page: the department pages (CSE.aspx, ECE.aspx, Sciences.aspx, HM.aspx) contain no publication lists; share moved to faculty pages and annual reports.
* news: institute Press page links only event news; Achievements page has no papers; the four newsletters (Jul 2025 to Jul 2026) give only counts (e.g. 23 journals, 16 conferences, 4 patents, 7 book chapters Nov 2025-Feb 2026) and no titles; Jul 2025 newsletter is an image-only PDF. External news coverage not found. Share moved to faculty pages.
* arXiv: general web search (3 queries restricted to arxiv.org / affiliation strings) surfaced no arXiv paper with an IIIT Ranchi affiliation (hits were BIT Mesra, IIITDM Jabalpur). Zero arXiv rows. No arXiv fetches were made, so no 403 occurred.
* Annual reports: docs/rti/*_english.pdf. 2016-17, 2017-18, 2018-19 (image scans) have no publication list (2018-19 page 14 faculty list used as tenure evidence: Priye director; Mishra, Sharma, Mahto, Pati, Bhakta assistant professors; Malviya, Panda, Sandeep Kumar, Nitin Chandra, Nibedita Mandal temporary). 2019-20 is an image scan, pages 17-19 read visually (pdftoppm + image viewer; no OCR installed). 2020-21 and 2022-23 have text; 2021-22 is a scan that was not read (time). 2020-21 and 2022-23 listings are pooled lists of faculty papers, many with non-IIIT first authors.
* Years 2016 and 2017 are empty: no paper in the sources satisfies the strict tenure rule for those years.

## Pages fetched (all via polite_get.py)
Faculty profile PDFs Faculty02..39 (31 returned 200, 9 numbers returned 404: 01, 03, 08, 14, 29, 33, 35, 38, 40), text extracted with pypdf (glyph names such as /one.onum cleaned) because pdftotext dropped digits and the letter l. iiitranchi.ac.in: default, RnD, achievements, Newsletter, Press, CSE, ECE, Sciences, HM, NIRF, Events pages; 4 newsletters; annual reports 2016-17 to 2022-23. Pages with list entries seen: profile lists ~600 entries, annual reports ~100 entries; yield: 53 profile rows from 25 profiles, 27 annual-report rows, 2 web-search rows.
Web search strings: `arxiv "Indian Institute of Information Technology Ranchi" paper` (arxiv.org); `IIIT Ranchi researchers paper published journal faculty news`; `"IIIT Ranchi" arxiv.org Kirti Kumari OR ...`; `"Department of Computer Science and Engineering, IIIT Ranchi" arXiv preprint`; `"Indian Institute of Information Technology Ranchi" Mathematics OR Physics arxiv ...`; `"IIIT Ranchi" DravidianLangTech Kirti Kumari fake news aclanthology`; `Mahto "Indian Institute of Information Technology Ranchi" MIMO antenna ...`; `"Shashi Kant Sharma" "IIIT Ranchi" TFET ...`. The two high-confidence rows came from the search results (SPIE page showing IIIT Ranchi affiliation; ACL Anthology paper whose title contains IIITRanchi); those pages were not fetched separately.

## Tenure used
Joining years from rosters/iiit_ranchi_faculty.csv (NIRF, archived lists; some are regularisation dates, hence conservative; Malviya and Panda appear as temporary faculty in the 2018-19 report, earlier than the roster's 2019). Former faculty rows (Acharyya 2021, B. B. Sinha 2022, S. Mahato 2023, Priye 2022, Biswas 2022-2024) restricted to years inside archived tenure; Biswas's leaving year unknown (2024 paper is a risk).

## Coverage (department x year, counts)
| Department | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 | total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Electronics and Communication Engineering | 0 | 0 | 1 | 4 | 5 | 4 | 11 | 7 | 3 | 3 | 3 | 41 |
| Computer Science and Engineering | 0 | 0 | 0 | 0 | 0 | 2 | 9 | 6 | 3 | 7 | 1 | 28 |
| Sciences (Physics) | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 1 | 2 | 0 | 5 |
| Sciences (Mathematics) | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 7 | 8 |

No Humanities and Management paper (Noopur has no papers in profile; Shahid Shadab Hassan's and Manju Mathew's PDFs have no usable list).

## Per-person counts (first-named IIIT author, cap 8)
{'Santosh Kumar Mahto': 8, 'Shashi Kant Sharma': 8, 'Jitendra Kumar Mishra': 8, 'Ranjan Kumar Behera': 7, 'Kirti Kumari': 6, 'Nishit Malviya': 6, 'Rohit Kandulna': 5, 'Anuj Singh': 5, 'Bharat Singh': 4, 'Bam Bahadur Sinha': 3, 'Tarun Biswas': 3, 'Akash Srivastava': 3, 'Rajiv Kumar': 2, 'Jayadeep Pati': 2, 'Puja Ghosh': 2, 'Shalini Mahato': 2, 'Shashi Kant': 2, 'Rashmi Panda': 1, 'Vishnu Priye': 1, 'Debanjan Acharyya': 1, 'Amit Kumar Singh': 1, 'N Kishore Babu': 1, 'Chandra Prakash Singh': 1}

## Biases
* Heavy on ECE and CSE; 2022-2026 carry 66 of the rows. Years 2016-2017 empty.
* Rows are what the institute chose to list (profile CVs, annual reports): self-reported, likely favour journal papers and well-indexed venues; conferences and abstracts included. Few DOIs because profiles print DOIs inconsistently; DOI coverage reflects the source, not selection.
* Almost all rows are medium confidence (affiliation not visible on the paper). Co-author-only listings from annual reports include papers whose first authors are outside IIIT Ranchi (e.g. Gupta et al.), included only when an IIIT Ranchi person on the roster is an author and within tenure.
* Profile titles are as printed (APA sentence-case lower-casing in Mahto's profile, e.g. 'mimo', 'ghz'); some venue strings were abbreviated or normalised by hand. Some DOIs left empty where the printed DOI was truncated.
* Pipeline-independence: no Crossref/OpenAlex/S2/EPMC/DOAJ/ORCID/DBLP/Scholar/Scopus/IRINS used; roster file (institute list pages) reused. The DBLP page for Kirti Kumari showed up in a web search result list but was not opened or used.
