# Lab notebook: independent golden set, IIIT Guwahati (iiit_guwahati)

Operator: Arihant Tripathy. Rows: 150. Years 2016-2026. DOI printed on source: 9 (6%).

## Institute facts used
Indian Institute of Information Technology Guwahati (PPP IIIT), Bongora 781015 (permanent campus from July 2018; transit campus at Ambari 2013-2018). Look-alikes excluded: IIT Guwahati, Gauhati University, IIM Guwahati, NIT Silchar (most search hits were IIT Guwahati and were discarded).

## Sources used and yield
| Source | Visited | Rows |
|---|---|---|
| Faculty profile pages (iiitg.ac.in/<unit>/<name>; cached copies from the roster agent, plain institute pages) | 62 profile pages; 47 with a parseable publication list | 105 |
| Annual reports: 2015-16, 2016-17, 2018-19, 2019-20, 2022-23 parsed (2017-18 text parsed badly) | 6 PDFs with a text layer | 30 (122 list entries parsed, 54 rejected) |
| arXiv abstract pages and PDFs (affiliation read in the PDF) | 23 papers fetched, 13 accepted | 13 |
| Web search (Rupkatha article PDF) | 1 | 1 |
| News (Careers360, IIIT Guwahati co-author) | 1 | 1 |
| Department / lab pages | research-1 (sponsored-project table only, no paper lists); no lab publication pages found | 0 |

Source-mix deviation from the brief (faculty 50, dept 15, annual reports 15, arXiv 10, news 10 percent): faculty pages 70%, annual reports 20%, arXiv 8%, news/web 1%, dept pages 0%. Reasons: no department publication pages exist (share moved to faculty pages); the institute news page has only notices and admissions (no research highlights) and press coverage of IIIT Guwahati papers is almost absent (searches returned IIT Guwahati); annual reports 2020-21 and 2021-22 are image-only PDFs, 2023-24 and 2024-25 are 80-190 MB scans whose download timed out; 2017-18 is two-column and parsed badly.

## Search strings (web search tool)
arxiv "Indian Institute of Information Technology Guwahati" abstract; arxiv "IIIT Guwahati" Computer Science and Engineering authors pdf; same for Electronics and Communication Engineering; mathematics (Harun, Jha, Khandakar); faculty-name queries (Sudip Biswas; Ghose/Matam/Barbhuiya/Roy; Nag/Borah/Chakraborty/Jana; Barma/Dasgupta/Jajodia/Das); arxiv 2019-2021 "Indian Institute of Information Technology Guwahati" Bongora Assam; IIIT Guwahati researchers publish paper journal news; "IIIT Guwahati" professor research study 2023-2025 news; title lookup for the Anirban Das paper; Humanities queries (Barua, Deb, Saha, Roy); title searches for Barbhuiya arXiv papers and the Rupkatha article. Crossref, OpenAlex, Semantic Scholar, DBLP, Scholar, Scopus, IRINS, ORCID were not used; some DBLP and Crossref URLs appeared in a search listing and were not opened or used.

## Rules applied
Tenure rule: faculty and annual-report rows require year strictly after the joining year on the person's own page (roster agent cur.json). Persons without a joining year (Kuntal Dey, Rekha Deka, Shanta Bhar, Nandana Bhardwaj, Sangita Talukdar, Snehasis Banerjee) were excluded. Faculty-page and annual-report rows are medium; arXiv/web rows with the affiliation visible in the PDF are high. Per-person cap 8 (soft cap 3 first, raised only when needed). Entries were taken evenly spread through each list (farthest-point order from the middle), then chosen greedily by year deficit against a target profile. Titles deduplicated across sources. Annual-report author matching used first initial plus surname against the roster; non-paper items (workshop sessions, invited talks, op-eds) were dropped.

## Counts
By source: {'arxiv': 13, 'websearch': 1, 'news': 1, 'annual_report': 30, 'faculty_page': 105}. By confidence: {'high': 15, 'medium': 135}. Distinct first-named IIIT authors: 55.

Departments x years:

| Department | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 | Total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Computer Science and Engineering | 2 | 2 | 1 | 6 | 6 | 7 | 8 | 5 | 11 | 14 | 5 | 67 |
| Science and Mathematics | 0 | 0 | 1 | 0 | 0 | 2 | 0 | 2 | 2 | 3 | 2 | 12 |
| Humanities and Social Sciences | 1 | 1 | 0 | 2 | 2 | 2 | 3 | 1 | 3 | 4 | 5 | 24 |
| Electronics and Communication Engineering | 4 | 2 | 6 | 7 | 5 | 2 | 5 | 4 | 6 | 3 | 3 | 47 |

## Rejected candidates
Annual-report entries rejected: {'outside tenure': 14, 'no roster author matched': 36, 'talk/workshop session, not a publication': 4}. The 2022-23 report lists papers by people who joined in 2023 (e.g. Nilotpal Chakraborty, Pawan K. Mishra), written before joining. Examples:
* Towards more robust hate speech detection: using social context and us (2023): outside tenure: Kuntal Dey (joined None)
* RTT-based Rogue UAV Detection in IoV Networks (2022): outside tenure: Nilotpal Chakraborty (joined 2023)
* Learning and Annotating Activities for Home Automation using LSTM (2019): outside tenure: Snehasis Banerjee (joined None)
* Activity Recognition through Feature Learning and Annotations using LS (2019): outside tenure: Snehasis Banerjee (joined None)
* Performance of Adaptive OMA/Cooperative-NOMA Scheme With User Selectio (2018): outside tenure: Komal Janghel (joined 2018)
* Cooperative Spectrum Sensing using Quantized Energy Statistics in the  (2018): outside tenure: Kukil Khanikar (joined 2018)
* A Preliminary Study of CNNs for Iris and Periocular Verification in th (2016): outside tenure: Kuntal Dey (joined None)
* Parametric Reconstruction of Diffuse Optical Tomography using Gaussian (2016): outside tenure: Rusha Patra (joined 2016)
* Analysis of Neural Electrical Activities During Elicitation of Human E (2016): outside tenure: Shovan Barma (joined 2016)
* SUFFERING Understanding System Based on Facial Expression and Human Ac (2016): outside tenure: Shovan Barma (joined 2016)
* On Some Dielectric Resonator Antennas (2015): outside tenure: Bidisha Dasgupta (joined 2014)
* Segmented Hemispherical DRA in Composite Form for Radiation Pattern Di (2015): outside tenure: Bidisha Dasgupta (joined 2014)

arXiv candidates rejected: 2505.03839 (IIT Patna / IIT Indore affiliations), 2404.00412 (PDF could not be fetched), 2510.26156, 2604.07275, 2502.01363 (Khandakar; no affiliation line in the PDF text, only a search snippet), 1502.07938 (acknowledgement only), 2610.29943 and similar hits (IIT Guwahati). Faculty pages of Mansoor Khan, Sounak Roy, Shilpa, Valmik Tilwari and Mohd Harun use free-text formats and yielded no rows (Khan and Roy appear via annual reports).

## Known biases and caveats
* About 90% of rows (faculty page + annual report) are medium: the affiliation is established by tenure, not by the paper. DOI coverage is 6% because institute pages rarely print DOIs.
* Annual reports could be read for only 6 of 12 years, so those rows lie in 2016-2020 and 2023; 2017 is thin.
* Faculty pages cover current faculty only (as cached by the roster agent); former faculty and students enter only through arXiv, annual reports and the one news item. Dipendu Maity, Soumi Chattopadhyay, Srinibas Swain are not on the cached roster.
* Venue strings are as printed; some carry trailing volume text or are cut at line breaks in annual reports.
* Profile pages were reused from the roster agent cache (no live refetch).
* The title of the Anirban Das paper comes from a web-search result, not from a page reached from the news link; no DOI recorded.
* The first batch of annual-report downloads stalled and was stopped; they were redone one at a time through the polite fetcher.
